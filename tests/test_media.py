import io,json,os,sqlite3,subprocess,tempfile,time,unittest,urllib.request,urllib.error,urllib.parse,zipfile,socket
from pathlib import Path

# Tiny valid PCM WAV fixture, not a recording of a person.
def wav():
    import wave
    stream=io.BytesIO()
    with wave.open(stream,'wb') as file:
        file.setnchannels(1);file.setsampwidth(2);file.setframerate(8000);file.writeframes(b'\x00\x00'*800)
    return stream.getvalue()

class MediaTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp=tempfile.TemporaryDirectory();cls.root=Path(__file__).resolve().parents[1]
        with socket.socket() as sock:sock.bind(('127.0.0.1',0));cls.port=sock.getsockname()[1]
        cls.env={**os.environ,'PORT':str(cls.port),'DATA_DIR':cls.tmp.name,'LIFEOS_PASSWORD':'recording-test-password','COOKIE_SECURE':'false'}
        cls.cookie='';cls.csrf='';cls.start()
    @classmethod
    def start(cls):
        cls.proc=subprocess.Popen(['python3','server.py'],cwd=cls.root,env=cls.env)
        for _ in range(50):
            try:
                with urllib.request.urlopen(f'http://127.0.0.1:{cls.port}/api/health'):break
            except Exception:time.sleep(.05)
    @classmethod
    def tearDownClass(cls):cls.proc.terminate();cls.proc.wait();cls.tmp.cleanup()
    @classmethod
    def request(cls,path,body=None,headers=None):
        h={'Cookie':cls.cookie,**(headers or {})}
        if body is not None:h['X-CSRF-Token']=cls.csrf
        req=urllib.request.Request(f'http://127.0.0.1:{cls.port}/api/{path}',data=body,headers=h)
        try:r=urllib.request.urlopen(req)
        except urllib.error.HTTPError as e:r=e
        with r:
            cookie=r.headers.get('Set-Cookie')
            if cookie:cls.cookie=cookie.split(';')[0]
            return r.status,r.read(),dict(r.headers)
    @classmethod
    def login(cls):
        cls.request('login',json.dumps({'password':'recording-test-password'}).encode(),{'Content-Type':'application/json'})
        cls.csrf=json.loads(cls.request('state')[1])['csrf']
    def test_complete_recording_lifecycle(self):
        self.assertEqual(self.request('recordings')[0],401)
        self.assertEqual(self.request('recordings',wav(),{'Content-Type':'audio/wav'})[0],401)
        self.login()
        meta={'title':'Al-Mulk latihan','date':'2026-11-01','juz':29,'target':'Al-Mulk 1–2 · Hal.562 baris 1–3','duration':.1}
        headers={'Content-Type':'audio/wav','X-Recording-Metadata':urllib.parse.quote(json.dumps(meta))}
        old=type(self).csrf;type(self).csrf='wrong'
        self.assertEqual(self.request('recordings',wav(),headers)[0],403)
        type(self).csrf=old
        self.assertEqual(self.request('recordings',b'not an audio file',headers)[0],400)
        status,body,_=self.request('recordings',wav(),headers);self.assertEqual(status,200)
        rid=json.loads(body)['id'];self.assertTrue(json.loads(body)['created'])
        self.assertFalse(json.loads(self.request('recordings',wav(),headers)[1])['created'])
        listed=json.loads(self.request('recordings')[1])['recordings'];self.assertEqual(len(listed),1)
        self.assertEqual(listed[0]['target'],meta['target'])
        self.assertEqual(self.request('recordings/'+rid)[1],wav())
        code,partial,h=self.request('recordings/'+rid,headers={'Range':'bytes=4-11'})
        self.assertEqual(code,206);self.assertEqual(partial,wav()[4:12]);self.assertIn('Content-Range',h)
        self.assertEqual(self.request('recordings/'+rid,headers={'Range':'bytes=999999-'} )[0],416)
        self.assertEqual(self.request('recordings/'+rid,headers={'Range':'bytes=-4'})[1],wav()[-4:])
        code,backup,_=self.request('recordings/export');self.assertEqual(code,200)
        with zipfile.ZipFile(io.BytesIO(backup)) as z:
            manifest=json.loads(z.read('recordings.json'));self.assertEqual(z.read(manifest['recordings'][0]['file']),wav())
        # Invalid late archive entry must roll back imports and remove staged files.
        self.assertEqual(self.request('recordings/delete',json.dumps({'id':rid}).encode(),{'Content-Type':'application/json'})[0],200)
        malicious=io.BytesIO()
        with zipfile.ZipFile(malicious,'w') as z:
            one=manifest['recordings'][0];z.writestr(one['file'],wav());z.writestr('recordings.json',json.dumps({**manifest,'recordings':[one,{'file':'../../escape.wav','metadata':meta}]}))
        self.assertEqual(self.request('recordings/import',malicious.getvalue(),{'Content-Type':'application/zip'})[0],400)
        self.assertEqual(json.loads(self.request('recordings')[1])['recordings'],[])
        self.assertEqual(list((Path(self.tmp.name)/'recordings').iterdir()),[])
        code,result,_=self.request('recordings/import',backup,{'Content-Type':'application/zip'});self.assertEqual(code,200);self.assertEqual(json.loads(result)['added'],1)
        self.assertEqual(json.loads(self.request('recordings/import',backup,{'Content-Type':'application/zip'})[1])['added'],0)
        # Database and audio survive server restart; session deliberately expires.
        type(self).proc.terminate();type(self).proc.wait();type(self).start();self.assertEqual(self.request('recordings')[0],401);self.login()
        rid=json.loads(self.request('recordings')[1])['recordings'][0]['id']
        self.assertEqual(self.request('recordings/'+rid)[1],wav())
        cookie=type(self).cookie;type(self).cookie='';self.assertEqual(self.request('recordings/'+rid)[0],401);type(self).cookie=cookie
