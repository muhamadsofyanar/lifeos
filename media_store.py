"""Authenticated personal recordings, persistent files, range playback, portable archive."""
import contextlib, hashlib, json, math, os, re, secrets, shutil, sqlite3, tempfile, threading, time, zipfile
from pathlib import Path
from urllib.parse import unquote
from workflow import valid_date, number
from hifz import validate_verse_range, unit_ids
from quran_coverage import coverage

MEDIA_LOCK=threading.RLock()
MAX_FILE=50*1024*1024
MAX_TOTAL=512*1024*1024
MAX_ARCHIVE=600*1024*1024
DIRECTORY=None

def setup(data_dir):
    global DIRECTORY
    DIRECTORY=Path(data_dir)
    (DIRECTORY/'recordings').mkdir(exist_ok=True)
    with db() as conn:
        conn.execute('CREATE TABLE IF NOT EXISTS recordings (id TEXT PRIMARY KEY, filename TEXT NOT NULL, mime TEXT NOT NULL, size INTEGER NOT NULL, sha256 TEXT NOT NULL UNIQUE, metadata TEXT NOT NULL, created REAL NOT NULL)')

def db(): return sqlite3.connect(DIRECTORY/'lifeos.db',timeout=20)

def detect_audio(body):
    if body[:4]==b'\x1aE\xdf\xa3':return 'audio/webm','webm'
    if body[:4]==b'OggS':return 'audio/ogg','ogg'
    if len(body)>12 and body[4:8]==b'ftyp':return 'audio/mp4','m4a'
    if body[:4]==b'RIFF' and body[8:12]==b'WAVE':return 'audio/wav','wav'
    if body[:3]==b'ID3' or (len(body)>2 and body[0]==255 and body[1]&224==224):return 'audio/mpeg','mp3'
    raise ValueError('Format audio tidak dikenali. Gunakan WebM, OGG, M4A/MP4 audio, WAV, atau MP3.')

def clean_metadata(meta):
    if not isinstance(meta,dict):raise ValueError('Metadata audio tidak valid.')
    juz=meta.get('juz')
    if type(juz) is not int or not 1<=juz<=30:raise ValueError('Pilih juz rekaman.')
    if not isinstance(meta.get('title'),str) or not meta['title'].strip() or len(meta['title'])>250:raise ValueError('Judul rekaman diperlukan, maksimal 250 karakter.')
    if not valid_date(meta.get('date')):raise ValueError('Tanggal audio tidak valid.')
    duration=meta.get('duration',0)
    if not number(duration,0,86400):raise ValueError('Durasi audio tidak valid.')
    for key in ['target','note','session']:
        if not isinstance(meta.get(key,''),str) or len(meta.get(key,''))>4000:raise ValueError('Catatan audio terlalu panjang.')
    result={k:meta.get(k,'') for k in ['title','date','juz','target','note','session']};result['duration']=duration
    if type(meta.get('targetVersion')) is int and meta['targetVersion']==2:
        c=coverage(juz,meta.get('scope'))
        if meta.get('session'):raise ValueError('Gunakan catatan murajaah untuk cakupan utuh, bukan sesi potongan latihan.')
        ref=meta.get('reviewSession','')
        if not isinstance(ref,str) or len(ref)>250:raise ValueError('Hubungan murajaah tidak valid.')
        result.update(targetVersion=2,scope=c['scope'],target=c['label'],reviewSession=ref)
        return result
    if 'targetVersion' in meta:
        if type(meta['targetVersion']) is not int or meta['targetVersion']!=1:raise ValueError('Versi target audio tidak dikenali.')
        result['targetVersion']=1
        if juz==30:
            validate_verse_range(meta.get('surah'),meta.get('from'),meta.get('to'))
            result.update({key:meta[key] for key in ['surah','from','to']})
        else:
            unit=meta.get('unit')
            if not isinstance(unit,str) or unit not in unit_ids(juz):raise ValueError('Unit audio tidak sesuai juz.')
            result['unit']=unit
    return result

def validate_session_reference(conn,meta):
    if meta.get('targetVersion')==2:
        if not meta.get('reviewSession'):return
        row=conn.execute('SELECT body FROM state WHERE id=1').fetchone()
        if row is None:raise ValueError('Data catatan murajaah belum tersedia.')
        logs=json.loads(row[0]).get('quranChecks',[])
        selected=next((l for l in logs if l.get('coverageVersion')==1 and l.get('id')==meta['reviewSession'] and l.get('juz')==meta['juz']),None)
        if selected is None:raise ValueError('Catatan murajaah tidak ditemukan untuk juz ini.')
        parent=coverage(selected['juz'],selected.get('scope'));child=coverage(meta['juz'],meta['scope'])
        if child['start']<parent['start'] or child['end']>parent['end']:raise ValueError('Cakupan audio berada di luar catatan murajaah.')
        return
    if not meta.get('session'):return
    row=conn.execute('SELECT body FROM state WHERE id=1').fetchone()
    if row is None:raise ValueError('Data catatan sesi belum tersedia.')
    state=json.loads(row[0]);juz=meta['juz']
    sessions=state['quranSessions'] if juz==30 else [s for s in state['quranUnitSessions'] if s.get('juz')==juz]
    selected=next((s for s in sessions if s['id']==meta['session']),None)
    if selected is None:raise ValueError('Catatan sesi tidak ditemukan untuk juz ini. Muat ulang dan pilih sesi yang sesuai.')
    if meta.get('targetVersion')==1:
        if juz==30:
            validate_verse_range(selected.get('surah'),selected.get('from'),selected.get('to'))
            if meta['surah']!=selected['surah'] or meta['from']<selected['from'] or meta['to']>selected['to']:
                raise ValueError('Rentang audio berada di luar rentang catatan sesi.')
        elif meta['unit'] not in selected.get('units',[]):raise ValueError('Unit audio tidak termasuk catatan sesi.')

def rows(conn):
    return [dict(zip(['id','filename','mime','size','sha256','metadata','created'],r)) for r in conn.execute('SELECT id,filename,mime,size,sha256,metadata,created FROM recordings ORDER BY created DESC')]

def public(row):return {**json.loads(row['metadata']),'id':row['id'],'mime':row['mime'],'size':row['size'],'created':row['created']}

def insert_audio(conn,body,meta,created=None):
    if created is not None and not number(created,0,253402300799):raise ValueError('Waktu pembuatan audio tidak valid.')
    mime,ext=detect_audio(body)
    if not 16<=len(body)<=MAX_FILE:raise ValueError('Audio harus berukuran 16 byte–50 MB.')
    sha=hashlib.sha256(body).hexdigest()
    duplicate=conn.execute('SELECT id FROM recordings WHERE sha256=?',(sha,)).fetchone()
    if duplicate:return duplicate[0],False
    total=conn.execute('SELECT COALESCE(SUM(size),0),COUNT(*) FROM recordings').fetchone()
    if total[0]+len(body)>MAX_TOTAL or total[1]>=2000:raise ValueError('Penyimpanan audio aplikasi penuh (512 MB / 2000 rekaman). Download backup dan hapus rekaman yang tidak diperlukan.')
    rid=secrets.token_hex(16);filename=rid+'.'+ext;path=DIRECTORY/'recordings'/filename
    path.write_bytes(body)
    try:conn.execute('INSERT INTO recordings VALUES(?,?,?,?,?,?,?)',(rid,filename,mime,len(body),sha,json.dumps(clean_metadata(meta)),time.time() if created is None else created))
    except BaseException:path.unlink(missing_ok=True);raise
    return rid,True

class MediaMixin:
    def media_auth(self,write=False):
        _,session=self.session()
        if not session:self.reply(401,{'error':'Silakan masuk.'});return False
        if write:
            import hmac
            if self.headers.get('Sec-Fetch-Site')=='cross-site' or not hmac.compare_digest(self.headers.get('X-CSRF-Token',''),session['csrf']):
                self.reply(403,{'error':'Token keamanan tidak sesuai. Muat ulang.'});return False
        return True

    def media_get(self,path):
        if not (path=='/api/recordings' or path=='/api/recordings/export' or re.fullmatch(r'/api/recordings/[a-f0-9]{32}',path)):return False
        if not self.media_auth():return True
        if path=='/api/recordings':
            with db() as conn:items=rows(conn)
            self.reply(200,{'recordings':[public(r) for r in items]});return True
        if path.endswith('/export'):
            self.export_audio();return True
        rid=path.rsplit('/',1)[1]
        with db() as conn:items=[r for r in rows(conn) if r['id']==rid]
        if not items:self.reply(404,{'error':'Audio tidak ditemukan.'});return True
        row=items[0]
        try:
            with MEDIA_LOCK:
                file=open(DIRECTORY/'recordings'/row['filename'],'rb')
        except FileNotFoundError:self.reply(404,{'error':'File audio tidak ada di volume. Periksa backup.'});return True
        with file:
            size=os.fstat(file.fileno()).st_size;start,end=0,size-1;status=200
            header=self.headers.get('Range')
            if header:
                match=re.fullmatch(r'bytes=(\d*)-(\d*)',header)
                if not match or not any(match.groups()):return self.range_error(size)
                a,b=match.groups()
                if not a:
                    length=int(b)
                    if length<=0:return self.range_error(size)
                    start=max(0,size-length)
                else:
                    start=int(a);end=min(int(b),size-1) if b else size-1
                if start>=size or end<start:return self.range_error(size)
                status=206
            self.send_response(status);self.headers_common(row['mime'])
            self.send_header('Accept-Ranges','bytes');self.send_header('Content-Length',str(end-start+1))
            self.send_header('Content-Disposition',f'inline; filename="lifeos-{rid}.{row["filename"].rsplit(".",1)[1]}"')
            if status==206:self.send_header('Content-Range',f'bytes {start}-{end}/{size}')
            self.end_headers();file.seek(start);remaining=end-start+1
            while remaining:
                chunk=file.read(min(65536,remaining))
                if not chunk:break
                self.wfile.write(chunk);remaining-=len(chunk)
        return True

    def range_error(self,size):
        self.send_response(416);self.headers_common('application/json');self.send_header('Content-Range',f'bytes */{size}');self.send_header('Content-Length','0');self.end_headers();return True

    def read_body(self,maximum):
        length=int(self.headers.get('Content-Length','0'))
        if not 0<length<=maximum:raise ValueError('Ukuran upload melebihi batas.')
        body=self.rfile.read(length)
        if len(body)!=length:raise ValueError('Upload tidak lengkap.')
        return body

    def media_post(self,path):
        if path not in ['/api/recordings','/api/recordings/delete','/api/recordings/import']:return False
        if not self.media_auth(True):return True
        if path=='/api/recordings':
            meta=clean_metadata(json.loads(unquote(self.headers.get('X-Recording-Metadata','{}'))))
            if not self.headers.get('Content-Type','').startswith(('audio/','video/mp4','application/octet-stream')):raise ValueError('Upload harus berupa audio.')
            body=self.read_body(MAX_FILE)
            with MEDIA_LOCK,db() as conn:
                conn.execute('BEGIN IMMEDIATE');validate_session_reference(conn,meta);rid,created=insert_audio(conn,body,meta)
            self.reply(200,{'id':rid,'created':created});return True
        if path.endswith('/delete'):
            if self.headers.get('Content-Type','').split(';')[0]!='application/json':raise ValueError('JSON diperlukan.')
            rid=json.loads(self.read_body(4096)).get('id','')
            if not re.fullmatch('[a-f0-9]{32}',rid):raise ValueError('ID audio tidak valid.')
            with MEDIA_LOCK,db() as conn:
                row=conn.execute('SELECT filename FROM recordings WHERE id=?',(rid,)).fetchone()
                conn.execute('DELETE FROM recordings WHERE id=?',(rid,));conn.commit()
                if row:(DIRECTORY/'recordings'/row[0]).unlink(missing_ok=True)
            self.reply(200,{'ok':True});return True
        self.import_audio();return True

    def export_audio(self):
        with tempfile.TemporaryFile(dir=DIRECTORY) as temp:
            with MEDIA_LOCK,db() as conn,zipfile.ZipFile(temp,'w',compression=zipfile.ZIP_STORED) as archive:
                items=rows(conn)
                manifest={'version':1,'kind':'lifeos-recordings','recordings':[]}
                for row in items:
                    path=DIRECTORY/'recordings'/row['filename']
                    if not path.exists():self.reply(409,{'error':'Ada file audio hilang. Periksa volume sebelum backup.'});return
                    name='audio/'+row['filename'];archive.write(path,name)
                    manifest['recordings'].append({'file':name,'metadata':json.loads(row['metadata']),'created':row['created']})
                archive.writestr('recordings.json',json.dumps(manifest,ensure_ascii=False,indent=2))
            length=temp.tell();temp.seek(0)
            self.send_response(200);self.headers_common('application/zip');self.send_header('Content-Length',str(length));self.send_header('Content-Disposition','attachment; filename="lifeos-recordings.zip"');self.end_headers();shutil.copyfileobj(temp,self.wfile,65536)

    def import_audio(self):
        length=int(self.headers.get('Content-Length','0'))
        if not 0<length<=MAX_ARCHIVE:raise ValueError('Arsip audio maksimal 600 MB.')
        with tempfile.TemporaryFile(dir=DIRECTORY) as temp:
            remaining=length
            while remaining:
                chunk=self.rfile.read(min(65536,remaining))
                if not chunk:raise ValueError('Upload arsip terputus.')
                temp.write(chunk);remaining-=len(chunk)
            temp.seek(0)
            try:archive=zipfile.ZipFile(temp)
            except zipfile.BadZipFile:raise ValueError('Arsip ZIP tidak valid.')
            with archive:
                infos=archive.infolist()
                if len(infos)>2001 or len({x.filename for x in infos})!=len(infos) or sum(x.file_size for x in infos)>MAX_TOTAL+2*1024*1024:raise ValueError('Isi arsip terlalu besar atau tidak valid.')
                try:
                    if archive.getinfo('recordings.json').file_size>2*1024*1024:raise ValueError('Manifest terlalu besar.')
                    manifest=json.loads(archive.read('recordings.json'))
                    entries=manifest['recordings']
                    if manifest.get('kind')!='lifeos-recordings' or manifest.get('version')!=1 or not isinstance(entries,list) or len(entries)>2000:raise ValueError('Format arsip audio tidak sesuai.')
                except (KeyError,TypeError,json.JSONDecodeError):raise ValueError('Manifest arsip tidak sesuai.')
                created_files=[];added=0
                with MEDIA_LOCK:
                    try:
                        with db() as conn:
                            conn.execute('BEGIN IMMEDIATE')
                            for entry in entries:
                                if not isinstance(entry,dict):raise ValueError('Entri arsip harus berupa objek.')
                                filename=entry.get('file','')
                                if not re.fullmatch(r'audio/[a-f0-9]{32}\.(webm|m4a|mp3|ogg|wav)',filename):raise ValueError('Nama file arsip tidak valid.')
                                try:info=archive.getinfo(filename)
                                except KeyError:raise ValueError('File audio dalam manifest tidak ditemukan.')
                                if not 16<=info.file_size<=MAX_FILE:raise ValueError('Ukuran file dalam arsip tidak valid.')
                                body=archive.read(filename)
                                rid,is_new=insert_audio(conn,body,clean_metadata(entry.get('metadata')),entry.get('created'))
                                if is_new:
                                    row=conn.execute('SELECT filename FROM recordings WHERE id=?',(rid,)).fetchone()
                                    created_files.append(row[0]);added+=1
                    except BaseException:
                        for filename in created_files:(DIRECTORY/'recordings'/filename).unlink(missing_ok=True)
                        raise
            self.reply(200,{'ok':True,'added':added})
