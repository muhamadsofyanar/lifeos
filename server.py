"""LifeOS single-user service. Run behind a TLS reverse proxy."""
import os, json, sqlite3, secrets, hashlib, hmac, time, threading
from pathlib import Path
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from http.cookies import SimpleCookie
from urllib.parse import urlsplit
from media_store import MediaMixin, setup as setup_media
from data_transfer import merge_import, unpack
from hifz import JUZ30_COUNTS

ROOT = Path(__file__).parent
DATA = Path(os.environ.get('DATA_DIR', str(ROOT / 'data')))
DATA.mkdir(parents=True, exist_ok=True)
PASSWORD = os.environ.get('LIFEOS_PASSWORD', '')
SECURE = os.environ.get('COOKIE_SECURE', 'true').lower() == 'true'
SALT = secrets.token_bytes(16)
PASSWORD_HASH = hashlib.scrypt(PASSWORD.encode(), salt=SALT, n=16384, r=8, p=1)
SESSIONS, ATTEMPTS = {}, []
LOCK = threading.Lock()
LEGACY_KINDS = ['inbox', 'tasks', 'projects', 'notes', 'events', 'sessions', 'reviews', 'areas', 'goals']

KINDS = LEGACY_KINDS + ['quran', 'quranSessions', 'plans', 'preferences', 'quranUnits', 'quranUnitSessions', 'quranChecks', 'learning', 'practiceLogs', 'dayPlans', 'metricLogs', 'routines', 'routineLogs', 'timeEntries']
def counts_for_surah(surah):
    return JUZ30_COUNTS[surah]

def normalize(data):
    if isinstance(data, dict) and set(LEGACY_KINDS).issubset(data) and set(data).issubset(KINDS):
        return {k: data.get(k, []) for k in KINDS}
    return data

def connect():
    db = sqlite3.connect(DATA / 'lifeos.db', timeout=20)
    db.execute('PRAGMA journal_mode=WAL')
    return db

with connect() as db:
    db.execute('CREATE TABLE IF NOT EXISTS state (id INTEGER PRIMARY KEY CHECK(id=1), revision INTEGER NOT NULL, body TEXT NOT NULL)')
    db.execute('CREATE TABLE IF NOT EXISTS history (revision INTEGER PRIMARY KEY, created TEXT DEFAULT CURRENT_TIMESTAMP, body TEXT NOT NULL)')
    db.execute('INSERT OR IGNORE INTO state VALUES(1,0,?)', (json.dumps({k: [] for k in KINDS}),))

    rev, body = db.execute('SELECT revision,body FROM state WHERE id=1').fetchone()
    migrated = normalize(json.loads(body))
    if migrated != json.loads(body):
        validate_keys = set(migrated) == set(KINDS)
        if not validate_keys: raise RuntimeError('Schema data tidak dikenali; hentikan migrasi.')
        db.execute('INSERT OR IGNORE INTO history(revision,body) VALUES(?,?)', (rev,body))
        db.execute('UPDATE state SET revision=?,body=? WHERE id=1', (rev+1,json.dumps(migrated)))

def validate(data):
    if not isinstance(data, dict) or set(data) != set(KINDS):
        raise ValueError('Struktur backup tidak sesuai.')
    for k in KINDS:
        if not isinstance(data[k], list) or len(data[k]) > 20000:
            raise ValueError('Data tidak valid atau terlalu besar.')
        ids = set()
        for item in data[k]:
            if not isinstance(item, dict) or not isinstance(item.get('id'), str) or item['id'] in ids:
                raise ValueError('ID data tidak valid atau duplikat.')
            ids.add(item['id'])
    from validation import validate_shapes
    validate_shapes(data)
    for item in data['quran']:
        if type(item.get('surah')) is not int or item['surah'] not in range(78,115) or type(item.get('ayah')) is not int:
            raise ValueError('Surah hafalan di luar Juz 30.')
        if not 1 <= item['ayah'] <= counts_for_surah(item['surah']) or item.get('status') not in ['practiced','strengthen','self','teacher']:
            raise ValueError('Ayat atau status hafalan tidak valid.')
        if item['id'] != str(item['surah'])+':'+str(item['ayah']):
            raise ValueError('ID ayat tidak sesuai.')
        if item.get('status') == 'teacher' and not str(item.get('teacher','')).strip():
            raise ValueError('Status disimak guru memerlukan nama penyimak.')
    for item in data['quranSessions']:
        from workflow import number, valid_date
        if not number(item.get('minutes'), 1, 240):
            raise ValueError('Durasi hafalan harus 1–240 menit.')
        if any(k in item for k in ['surah', 'from', 'to']):
            surah, start, end = item.get('surah'), item.get('from'), item.get('to')
            if type(surah) is not int or not 78 <= surah <= 114 or type(start) is not int or type(end) is not int or not 1 <= start <= end <= counts_for_surah(surah):
                raise ValueError('Rentang ayat sesi tidak valid.')
        if 'status' in item and item['status'] not in ['practiced','strengthen','self','teacher']:
            raise ValueError('Penilaian sesi tidak valid.')
        if item.get('status') == 'teacher' and not item.get('teacher', '').strip():
            raise ValueError('Isi nama penyimak sesi.')
    from hifz import validate_units
    validate_units(data)
    from workflow import validate_workflow
    validate_workflow(data)
    active = [s for s in data['sessions'] if not s.get('end')]
    if len(active) > 1:
        raise ValueError('Hanya satu timer boleh aktif.')

setup_media(DATA)

class Handler(MediaMixin, BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        pass

    def reply(self, code, obj, cookie=None):
        body = json.dumps(obj, ensure_ascii=False).encode()
        self.send_response(code)
        self.headers_common('application/json; charset=utf-8')
        if cookie: self.send_header('Set-Cookie', cookie)
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def headers_common(self, mime):
        self.send_header('Content-Type', mime)
        self.send_header('Cache-Control', 'no-store')
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.send_header('X-Frame-Options', 'DENY')
        self.send_header('Referrer-Policy', 'same-origin')
        self.send_header('Content-Security-Policy', "default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; connect-src 'self'; media-src 'self' blob:; frame-ancestors 'none'; base-uri 'self'; form-action 'self'")

    def session(self):
        try:
            c = SimpleCookie(self.headers.get('Cookie', ''))
            token = c['lifeos'].value
            with LOCK:
                entry = SESSIONS.get(token)
                if entry and entry['expires'] > time.time(): return token, entry
        except (KeyError, ValueError): pass
        return None, None

    def do_GET(self):
        path = urlsplit(self.path).path
        if self.media_get(path): return
        if path == '/api/health': return self.reply(200, {'ok': True})
        if path.startswith('/api/'):
            _, session = self.session()
            if not session: return self.reply(401, {'error': 'Silakan masuk.'})
            if path == '/api/import/templates':
                return self.reply(200, json.loads((ROOT / 'templates' / 'catalog.json').read_text()))
            if path == '/api/state':
                with connect() as db: row = db.execute('SELECT revision,body FROM state WHERE id=1').fetchone()
                return self.reply(200, {'revision': row[0], 'data': json.loads(row[1]), 'csrf': session['csrf']})
            if path == '/api/history':
                with connect() as db: rows = db.execute('SELECT revision,created FROM history ORDER BY revision DESC LIMIT 30').fetchall()
                return self.reply(200, {'history': [{'revision': r, 'created': d} for r,d in rows]})
            return self.reply(404, {'error': 'Tidak ditemukan.'})
        files = {'/academy.js': ('academy.js', 'text/javascript; charset=utf-8'), '/transfer.js': ('transfer.js', 'text/javascript; charset=utf-8'), '/': ('index.html', 'text/html; charset=utf-8'), '/consolidated.js': ('consolidated.js', 'text/javascript; charset=utf-8'), '/recordings.js': ('recordings.js', 'text/javascript; charset=utf-8'), '/quran-meta.json': ('quran-meta.json', 'application/json; charset=utf-8'), '/wellbeing.js': ('wellbeing.js', 'text/javascript; charset=utf-8'), '/hifz.js': ('hifz.js', 'text/javascript; charset=utf-8'), '/features.js': ('features.js', 'text/javascript; charset=utf-8'), '/app.js': ('app.js', 'text/javascript; charset=utf-8'), '/style.css': ('style.css', 'text/css; charset=utf-8'), '/manifest.json': ('manifest.json', 'application/manifest+json'), '/icon.svg': ('icon.svg', 'image/svg+xml')}
        if path not in files: return self.reply(404, {'error': 'Tidak ditemukan.'})
        filename, mime = files[path]
        content = (ROOT / 'static' / filename).read_bytes()
        self.send_response(200); self.headers_common(mime)
        self.send_header('Content-Length', str(len(content))); self.end_headers(); self.wfile.write(content)

    def do_POST(self):
        try:
            path = urlsplit(self.path).path
            if self.media_post(path): return
            # Require same-origin JSON; cross-site HTML forms cannot write.
            if self.headers.get('Sec-Fetch-Site') == 'cross-site': return self.reply(403, {'error': 'Origin ditolak.'})
            if self.headers.get('Content-Type', '').split(';')[0] != 'application/json': return self.reply(415, {'error': 'JSON diperlukan.'})
            size = int(self.headers.get('Content-Length', '0'))
            if not 0 < size <= 8_000_000: return self.reply(413, {'error': 'Ukuran data tidak sesuai.'})
            obj = json.loads(self.rfile.read(size))
            if not isinstance(obj, dict): raise ValueError('JSON object diperlukan.')
            path = urlsplit(self.path).path
            if path == '/api/login':
                now = time.time()
                with LOCK:
                    ATTEMPTS[:] = [t for t in ATTEMPTS if t > now-300]
                    if len(ATTEMPTS) >= 15: return self.reply(429, {'error': 'Terlalu banyak percobaan. Tunggu 5 menit.'})
                    ATTEMPTS.append(now)
                candidate = obj.get('password', '')
                if not isinstance(candidate, str) or len(candidate)>1024: raise ValueError('Password tidak valid.')
                digest = hashlib.scrypt(candidate.encode(), salt=SALT, n=16384, r=8, p=1)
                if not PASSWORD or not hmac.compare_digest(digest, PASSWORD_HASH): return self.reply(401, {'error': 'Password salah.'})
                token = secrets.token_urlsafe(32)
                with LOCK:
                    for key in list(SESSIONS):
                        if SESSIONS[key]['expires'] < now: del SESSIONS[key]
                    SESSIONS[token] = {'expires': now+604800, 'csrf': secrets.token_urlsafe(32)}
                return self.reply(200, {'ok': True}, f'lifeos={token}; HttpOnly; SameSite=Strict; Path=/; Max-Age=604800' + ('; Secure' if SECURE else ''))
            token, session = self.session()
            if not session: return self.reply(401, {'error': 'Silakan masuk.'})
            if not hmac.compare_digest(self.headers.get('X-CSRF-Token',''), session['csrf']): return self.reply(403, {'error': 'Token keamanan tidak sesuai. Muat ulang.'})
            if path == '/api/logout':
                with LOCK: SESSIONS.pop(token, None)
                return self.reply(200, {'ok':True}, 'lifeos=; Path=/; Max-Age=0; HttpOnly; SameSite=Strict')
            if path in ['/api/import/preview', '/api/import/apply']:
                package = obj.get('package')
                incoming = unpack(package, set(KINDS))
                # Validate the file itself, including skipped records, before merging.
                validate({k: incoming.get(k, []) for k in KINDS})
                selected = obj.get('selected')
                with connect() as db:
                    if path.endswith('/apply'): db.execute('BEGIN IMMEDIATE')
                    rev, old = db.execute('SELECT revision,body FROM state WHERE id=1').fetchone()
                    if type(obj.get('revision')) is not int or obj['revision'] != rev:
                        return self.reply(409, {'error': 'Data berubah sejak pratinjau. Muat ulang data lalu buat pratinjau impor lagi.'})
                    merged, report = merge_import(json.loads(old), package, selected)
                    validate(merged)
                    if path.endswith('/apply') and report['added']:
                        db.execute('INSERT INTO history(revision,body) VALUES(?,?)', (rev,old))
                        db.execute('DELETE FROM history WHERE revision < ?', (rev-29,))
                        db.execute('UPDATE state SET revision=?,body=? WHERE id=1', (rev+1,json.dumps(merged)))
                        rev += 1
                return self.reply(200, {'revision': rev, 'report': report})
            if path == '/api/state':
                obj['data'] = normalize(obj.get('data'))
                validate(obj.get('data'))
                with connect() as db:
                    db.execute('BEGIN IMMEDIATE')
                    rev, old = db.execute('SELECT revision,body FROM state WHERE id=1').fetchone()
                    if obj.get('revision') != rev: return self.reply(409, {'error': 'Ada perubahan dari tab/perangkat lain. Muat ulang sebelum mengedit.'})
                    db.execute('INSERT INTO history(revision,body) VALUES(?,?)', (rev,old))
                    db.execute('DELETE FROM history WHERE revision < ?', (rev-29,))
                    db.execute('UPDATE state SET revision=?,body=? WHERE id=1', (rev+1,json.dumps(obj['data'])))
                return self.reply(200, {'revision': rev+1})
            return self.reply(404, {'error':'Tidak ditemukan.'})
        except (ValueError, TypeError) as e: self.reply(400, {'error':str(e)})
        except Exception: self.reply(500, {'error':'Server gagal menyimpan. Coba lagi.'})

if __name__ == '__main__':
    if len(PASSWORD) < 12: raise SystemExit('Set LIFEOS_PASSWORD minimal 12 karakter sebelum menjalankan server.')
    ThreadingHTTPServer(('0.0.0.0', int(os.environ.get('PORT','8000'))), Handler).serve_forever()
