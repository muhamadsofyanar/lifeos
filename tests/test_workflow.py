import datetime,importlib.util,json,os,sqlite3,subprocess,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('workflow',ROOT/'workflow.py');workflow=importlib.util.module_from_spec(spec);spec.loader.exec_module(workflow)
class WorkflowTest(unittest.TestCase):
    def test_validation(self):
        base={'routines':[],'routineLogs':[],'timeEntries':[]}
        routine={'id':'r','title':'Praktik','days':[1,3,5],'start':'2026-11-01','minutes':20}
        workflow.validate_workflow({**base,'routines':[routine]})
        for invalid in [{**routine,'days':[7]},{**routine,'minutes':float('inf')},{**routine,'start':'2026-99-99'}]:
            with self.assertRaises(ValueError):workflow.validate_workflow({**base,'routines':[invalid]})
        log={'id':'a','routine':'r','date':'2026-11-01','status':'done'}
        with self.assertRaises(ValueError):workflow.validate_workflow({**base,'routineLogs':[log,{**log,'id':'b'}]})
        with self.assertRaises(ValueError):workflow.validate_workflow({**base,'timeEntries':[{'id':'t','date':'2026-11-01','minutes':-5,'title':'No'}]})
    def test_migration_from_v13_preserves_audio_and_data(self):
        kinds=['inbox','tasks','projects','notes','events','sessions','reviews','areas','goals','quran','quranSessions','plans','preferences','quranUnits','quranUnitSessions','quranChecks','learning','practiceLogs','dayPlans','metricLogs']
        old={k:[] for k in kinds};old['notes']=[{'id':'old','title':'Catatan tetap ada'}];old['quran']=[{'id':'101:1','surah':101,'ayah':1,'status':'self'}]
        with tempfile.TemporaryDirectory() as directory:
            db=sqlite3.connect(Path(directory)/'lifeos.db');db.execute('CREATE TABLE state(id INTEGER PRIMARY KEY,revision INTEGER,body TEXT)');db.execute('INSERT INTO state VALUES(1,40,?)',(json.dumps(old),));db.execute('CREATE TABLE recordings (id TEXT PRIMARY KEY,filename TEXT,mime TEXT,size INTEGER,sha256 TEXT UNIQUE,metadata TEXT,created REAL)');db.execute('INSERT INTO recordings VALUES(?,?,?,?,?,?,?)',('a'*32,'a.wav','audio/wav',4,'hash','{}',1));db.commit();db.close()
            folder=Path(directory)/'recordings';folder.mkdir();(folder/'a.wav').write_bytes(b'data')
            for _ in range(2):subprocess.run(['python3','-c','import server'],cwd=ROOT,env={**os.environ,'DATA_DIR':directory,'LIFEOS_PASSWORD':'integration-test-password'},check=True)
            db=sqlite3.connect(Path(directory)/'lifeos.db');rev,body=db.execute('SELECT revision,body FROM state').fetchone();new=json.loads(body)
            self.assertEqual(rev,41)
            for k in old:self.assertEqual(old[k],new[k])
            for k in ['routines','routineLogs','timeEntries']:self.assertEqual(new[k],[])
            self.assertEqual(db.execute('SELECT COUNT(*) FROM recordings').fetchone()[0],1)
            self.assertEqual((folder/'a.wav').read_bytes(),b'data');db.close()
