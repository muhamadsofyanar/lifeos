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
        for filename in ['app.js','features.js','hifz.js','wellbeing.js','recordings.js','quran-meta.json','consolidated.js','transfer.js','academy.js','notes.js','murajaah.js','quran-coverage.json','quran-uthmani.txt','AmiriQuran-Regular.ttf']:
            with urllib.request.urlopen(f'http://127.0.0.1:{self.port}/{filename}') as asset:
                self.assertEqual(asset.status,200)
                self.assertGreater(len(asset.read()),100)
        self.assertEqual(self.request('state')[0],401)
        self.assertEqual(self.request('login',{'password':'wrong'})[0],401)
        self.assertEqual(self.request('login',{'password':'integration-password-123'})[0],200)
        _,state=self.request('state');type(self).csrf=state['csrf'];d=state['data']
        # A rejected restore must not modify either data or the revision.
        malformed=json.loads(json.dumps(d));malformed['events']=[{'id':'broken','date':'2026-11-01','time':None}]
        self.assertEqual(self.request('state',{'revision':0,'data':malformed})[0],400)
        unchanged=self.request('state')[1]
        self.assertEqual(unchanged['revision'],0)
        self.assertEqual(unchanged['data'],d)
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
        # Old v1 backup is accepted and new collections are filled without dropping legacy tasks.
        legacy={k:d[k] for k in ['inbox','tasks','projects','notes','events','sessions','reviews','areas','goals']}
        legacy['tasks']=[{'id':'old-backup','title':'Legacy restored task','status':'todo'}]
        self.assertEqual(self.request('state',{'revision':2,'data':legacy})[0],200)
        restored=self.request('state')[1]['data']
        self.assertEqual(restored['tasks'][0]['id'],'old-backup')
        self.assertEqual(restored['quran'],[])
        restored['quran']=[{'id':'101:1','surah':101,'ayah':1,'status':'teacher'}]
        self.assertEqual(self.request('state',{'revision':3,'data':restored})[0],400)
        restored['quran'][0]['teacher']='Penyimak'
        restored['quranSessions']=[{'id':'q1','minutes':25,'date':'2026-11-01'}]
        self.assertEqual(self.request('state',{'revision':3,'data':restored})[0],200)
        self.assertEqual(self.request('state')[1]['data']['quran'][0]['teacher'],'Penyimak')
        restored['quran'][0]['ayah']=12
        self.assertEqual(self.request('state',{'revision':4,'data':restored})[0],400)
        restored=self.request('state')[1]['data']
        restored['routines']=[{'id':'r1','title':'Follow-up','days':[1,3,5],'minutes':20,'start':'2026-11-01'}]
        restored['routineLogs']=[{'id':'r1:2026-11-02','routine':'r1','date':'2026-11-02','status':'done'}]
        restored['timeEntries']=[{'id':'time1','title':'Koordinasi','minutes':30,'date':'2026-11-01'}]
        self.assertEqual(self.request('state',{'revision':4,'data':restored})[0],200)
        self.assertEqual(self.request('state')[1]['data']['routineLogs'][0]['status'],'done')
        self.assertEqual(self.request('logout',{})[0],200)
        self.assertEqual(self.request('state')[0],401)
if __name__=='__main__':unittest.main()

class MigrationTest(unittest.TestCase):
    def test_existing_database_migrates_without_losing_tasks(self):
        import sqlite3
        root=Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory() as directory:
            db=sqlite3.connect(Path(directory)/'lifeos.db')
            legacy={k:[] for k in ['inbox','tasks','projects','notes','events','sessions','reviews','areas','goals']}
            legacy['tasks']=[{'id':'existing','title':'Data sebelum update','status':'todo'}]
            db.execute('CREATE TABLE state (id INTEGER PRIMARY KEY, revision INTEGER, body TEXT)')
            db.execute('INSERT INTO state VALUES(1,7,?)',(json.dumps(legacy),));db.commit();db.close()
            env={**os.environ,'DATA_DIR':directory,'LIFEOS_PASSWORD':'integration-password-123'}
            for _ in range(2):
                subprocess.run(['python3','-c','import server'],cwd=root,env=env,check=True)
            db=sqlite3.connect(Path(directory)/'lifeos.db');rev,body=db.execute('SELECT revision,body FROM state').fetchone()
            migrated=json.loads(body)
            self.assertEqual(rev,8,'Migration runs exactly once')
            self.assertEqual(migrated['tasks'],legacy['tasks'])
            for k in ['quran','quranSessions','plans','preferences']:self.assertEqual(migrated[k],[])
            self.assertEqual(json.loads(db.execute('SELECT body FROM history WHERE revision=7').fetchone()[0]),legacy)
            db.close()

class HifzValidationTest(unittest.TestCase):
    def test_units_days_metrics(self):
        import sys
        sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
        from hifz import validate_units,unit_ids,page_range
        base={'quranUnits':[],'quranUnitSessions':[],'dayPlans':[],'metricLogs':[]}
        self.assertEqual(len(unit_ids(29)),100)
        self.assertEqual(len(unit_ids(28)),60)
        self.assertEqual(len(unit_ids(27)),40)
        self.assertEqual(page_range(1),(1,21))
        self.assertEqual(page_range(25),(482,501))
        for j in range(1,30):
            entry={**base,'quranUnits':[{'id':next(iter(unit_ids(j))),'juz':j,'status':'self'}]}
            validate_units(entry)
        with self.assertRaises(ValueError):validate_units({**base,'quranUnits':[{'id':'29:562:6','juz':29,'status':'self'}]})
        with self.assertRaises(ValueError):validate_units({**base,'quranUnits':[{'id':'29:562:1','juz':29,'status':'teacher'}]})
        with self.assertRaises(ValueError):validate_units({**base,'dayPlans':[{'id':'day','work':1000,'rest':800}]})
        with self.assertRaises(ValueError):validate_units({**base,'metricLogs':[{'id':'m','value':float('nan')}]})
        validate_units({**base,'quranUnitSessions':[{'id':'s','juz':1,'units':['1:2:1','1:3:1'],'minutes':25}]})

    def test_v11_data_preserved(self):
        import sqlite3
        root=Path(__file__).resolve().parents[1]
        old={k:[] for k in ['inbox','tasks','projects','notes','events','sessions','reviews','areas','goals','quran','quranSessions','plans','preferences']}
        old['quran']=[{'id':'101:1','surah':101,'ayah':1,'status':'self'}]
        old['plans']=[{'id':'draft','idea':'Keep my idea','step':2}]
        with tempfile.TemporaryDirectory() as directory:
            db=sqlite3.connect(Path(directory)/'lifeos.db');db.execute('CREATE TABLE state(id INTEGER PRIMARY KEY,revision INTEGER,body TEXT)');db.execute('INSERT INTO state VALUES(1,12,?)',(json.dumps(old),));db.commit();db.close()
            for _ in range(2):subprocess.run(['python3','-c','import server'],cwd=root,env={**os.environ,'DATA_DIR':directory,'LIFEOS_PASSWORD':'integration-password-123'},check=True)
            db=sqlite3.connect(Path(directory)/'lifeos.db');rev,body=db.execute('SELECT revision,body FROM state').fetchone();db.close();new=json.loads(body)
            self.assertEqual(rev,13)
            for key in old:self.assertEqual(old[key],new[key])
            self.assertEqual(new['learning'],[])
            self.assertEqual(new['quranUnits'],[])
