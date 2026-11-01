import unittest, subprocess, tempfile, os, time, urllib.request, urllib.error, json, socket
from pathlib import Path

class AppTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp=tempfile.TemporaryDirectory()
        sock=socket.socket(); sock.bind(('127.0.0.1',0)); cls.port=sock.getsockname()[1]; sock.close()
        cls.proc=subprocess.Popen(['python3','server.py'],cwd=Path(__file__).resolve().parents[1],env={**os.environ,'DATA_DIR':cls.tmp.name,'LIFEOS_PASSWORD':'integration-password-123','COOKIE_SECURE':'false','PORT':str(cls.port)},stdout=subprocess.DEVNULL)
        cls.cookie='';cls.csrf=''
        for _ in range(50):
            try: cls.request('health'); break
            except Exception: time.sleep(.1)
    @classmethod
    def tearDownClass(cls): cls.proc.terminate();cls.proc.wait();cls.tmp.cleanup()
    @classmethod
    def request(cls,path,body=None,csrf=True):
        headers={'Cookie':cls.cookie}
        if body is not None:
            headers['Content-Type']='application/json'
            if csrf: headers['X-CSRF-Token']=cls.csrf
        req=urllib.request.Request(f'http://127.0.0.1:{cls.port}/api/{path}',data=json.dumps(body).encode() if body is not None else None,headers=headers)
        try:
            with urllib.request.urlopen(req) as r:
                if r.headers.get('Set-Cookie'):cls.cookie=r.headers['Set-Cookie'].split(';')[0]
                return r.status,json.load(r)
        except urllib.error.HTTPError as e:return e.code,json.load(e)
    def test_workflow(self):
        self.assertEqual(self.request('state')[0],401)
        self.assertEqual(self.request('login',{'password':'wrong'})[0],401)
        self.assertEqual(self.request('login',{'password':'integration-password-123'})[0],200)
        _,state=self.request('state');type(self).csrf=state['csrf'];d=state['data']
        d['tasks'].append({'id':'t1','title':'Write portfolio','status':'todo'})
        self.assertEqual(self.request('state',{'revision':0,'data':d},csrf=False)[0],403)
        self.assertEqual(self.request('state',{'revision':0,'data':d})[0],200)
        self.assertEqual(self.request('state',{'revision':0,'data':d})[0],409)
        self.assertEqual(self.request('state')[1]['data']['tasks'][0]['title'],'Write portfolio')
        d['sessions']=[{'id':'s1','end':None},{'id':'s2','end':None}]
        self.assertEqual(self.request('state',{'revision':1,'data':d})[0],400)
        self.assertEqual(self.request('history')[1]['history'][0]['revision'],0)
        d['sessions']=[];d['tasks']=[]
        self.assertEqual(self.request('state',{'revision':1,'data':d})[0],200)
        self.assertEqual(self.request('logout',{})[0],200)
        self.assertEqual(self.request('state')[0],401)
if __name__=='__main__':unittest.main()
