import copy
import json
import unittest
from data_transfer import merge_import

KINDS = ['inbox', 'tasks', 'projects', 'notes', 'events', 'sessions', 'reviews', 'areas', 'goals', 'quran', 'quranSessions', 'plans', 'preferences', 'quranUnits', 'quranUnitSessions', 'quranChecks', 'learning', 'practiceLogs', 'dayPlans', 'metricLogs', 'routines', 'routineLogs', 'timeEntries']


def empty():
    return {kind: [] for kind in KINDS}


def package(data):
    return {'kind': 'lifeos-import', 'version': '1.0', 'purpose': 'starter', 'data': data}


class TransferTest(unittest.TestCase):
    def test_merge_preserves_existing_and_remaps_links(self):
        current = empty()
        current['areas'] = [{'id': 'old-area', 'title': 'Bisnis dan Penghasilan', 'body': 'Keep my description'}]
        current['goals'] = [{'id': 'old-goal', 'title': 'IZINHUKUM — Menuntaskan pekerjaan klien yang tertunda', 'area': 'old-area'}]
        source = package({
            'areas': [{'id': 'seed-area', 'title': 'bisnis dan penghasilan', 'body': 'Different'}],
            'goals': [{'id': 'seed-goal', 'title': current['goals'][0]['title'], 'area': 'seed-area'}],
            'projects': [{'id': 'seed-project', 'title': 'IZINHUKUM — Daftar klien', 'goal': 'seed-goal', 'area': 'seed-area'}],
            'tasks': [{'id': 'seed-task', 'title': 'Kumpulkan daftar', 'project': 'seed-project', 'status': 'todo'}],
            'notes': [{'id': 'seed-note', 'title': 'Hasil pemeriksaan', 'project': 'seed-project', 'body': ''}]
        })
        original = copy.deepcopy(current)
        merged, report = merge_import(current, source)
        self.assertEqual(current, original)
        self.assertEqual(merged['areas'], original['areas'])
        self.assertEqual(merged['goals'], original['goals'])
        self.assertEqual(merged['projects'][0]['goal'], 'old-goal')
        self.assertEqual(merged['projects'][0]['area'], 'old-area')
        self.assertEqual(report['added'], 3)
        self.assertEqual(report['skipped'], 2)
        again, second = merge_import(merged, source)
        self.assertEqual(again, merged)
        self.assertEqual(second['added'], 0)

    def test_selected_collections_only(self):
        source = package({'notes': [{'id':'n','title':'Note'}], 'tasks':[{'id':'t','title':'Task','status':'todo'}]})
        merged, report = merge_import(empty(), source, ['notes'])
        self.assertEqual(len(merged['notes']), 1)
        self.assertEqual(merged['tasks'], [])
        self.assertEqual(report['added'], 1)

    def test_missing_dependency_is_rejected(self):
        source = package({'tasks':[{'id':'t','title':'Task','project':'missing'}]})
        with self.assertRaisesRegex(ValueError, 'project'):
            merge_import(empty(), source)

    def test_duplicate_input_ids_and_unknown_types_are_rejected(self):
        for source in [package({'notes':[{'id':'n'},{'id':'n'}]}), package({'unknown':[]}),
                       package({'notes':{}}), {'kind':'other','version':1,'data':{}},
                       package({'notes':[{'id':'n','title':'A'},42]})]:
            with self.subTest(source=source), self.assertRaises(ValueError):
                merge_import(empty(), source)

    def test_existing_id_is_never_overwritten(self):
        current = empty(); current['notes']=[{'id':'n','title':'Old','body':'Important'}]
        merged, report=merge_import(current, package({'notes':[{'id':'n','title':'New','body':'Changed'}]}))
        self.assertEqual(merged, current)
        self.assertEqual(report['skipped'],1)

    def test_natural_routine_log_key_and_parent_links(self):
        current=empty()
        current['routines']=[{'id':'old-r','title':'Routine'}]
        current['routineLogs']=[{'id':'old-log','routine':'old-r','date':'2026-11-01','status':'done'}]
        source=package({'routines':[{'id':'new-r','title':'Routine'}],
                        'routineLogs':[{'id':'new-log','routine':'new-r','date':'2026-11-01','status':'skip'}]})
        merged, report=merge_import(current, source)
        self.assertEqual(merged,current)
        self.assertEqual(report['added'],0)

    def test_task_titles_in_different_projects_are_distinct(self):
        current=empty(); current['projects']=[{'id':'p1','title':'One'},{'id':'p2','title':'Two'}]
        current['tasks']=[{'id':'t1','title':'Review','project':'p1'}]
        merged, _=merge_import(current,package({'tasks':[{'id':'t2','title':'Review','project':'p2'}]}))
        self.assertEqual(len(merged['tasks']),2)

    def test_active_timer_cannot_start_from_import(self):
        with self.assertRaisesRegex(ValueError,'timer'):
            merge_import(empty(),package({'sessions':[{'id':'s','start':1,'end':None}]}))

    def test_backup_v4_can_be_merged_without_replacement(self):
        current=empty();current['notes']=[{'id':'old','title':'Old'}]
        source={'version':4,'data':empty()};source['data']['notes']=[{'id':'new','title':'New'}]
        merged, _=merge_import(current,source)
        self.assertEqual(len(merged['notes']),2)

    def test_ambiguous_title_requires_exact_existing_id(self):
        current=empty();current['areas']=[{'id':'a1','title':'Business'},{'id':'a2','title':'Business'}]
        with self.assertRaisesRegex(ValueError,'lebih dari satu'):
            merge_import(current,package({'areas':[{'id':'new','title':'Business'}]}))
        merged,report=merge_import(current,package({'areas':[{'id':'a1','title':'Business'}]}))
        self.assertEqual(merged,current)
        self.assertEqual(report['skipped'],1)

    def test_nested_indicator_remaps_to_existing_definition(self):
        current=empty();current['goals']=[{'id':'g0','title':'Goal','indicators':[{'id':'i0','title':'Response','unit':'hours'}]}]
        source=package({'goals':[{'id':'g1','title':'Goal','indicators':[{'id':'i1','title':'Response','unit':'hours'}]}],
                        'metricLogs':[{'id':'m','goal':'g1','indicator':'i1','date':'2026-11-01','value':1}]})
        merged,_=merge_import(current,source)
        self.assertEqual(merged['metricLogs'][0]['goal'],'g0')
        self.assertEqual(merged['metricLogs'][0]['indicator'],'i0')


# HTTP contract covers preview, persistence, stale revisions and validation rollback.
class TransferHTTPTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import os, socket, subprocess, tempfile, time, urllib.request
        from pathlib import Path
        cls.root=Path(__file__).resolve().parents[1]
        cls.tmp=tempfile.TemporaryDirectory()
        with socket.socket() as s:s.bind(('127.0.0.1',0));cls.port=s.getsockname()[1]
        cls.proc=subprocess.Popen(['python3','server.py'],cwd=cls.root,env={**os.environ,'PORT':str(cls.port),'DATA_DIR':cls.tmp.name,'LIFEOS_PASSWORD':'import-fixture-password','COOKIE_SECURE':'false'},stdout=subprocess.DEVNULL)
        cls.cookie='';cls.csrf=''
        for _ in range(60):
            try:cls.request('health');break
            except Exception:time.sleep(.05)

    @classmethod
    def tearDownClass(cls):
        cls.proc.terminate();cls.proc.wait();cls.tmp.cleanup()

    @classmethod
    def request(cls,path,body=None):
        import urllib.request,urllib.error
        headers={'Cookie':cls.cookie,'X-CSRF-Token':cls.csrf}
        if body is not None:headers['Content-Type']='application/json'
        req=urllib.request.Request(f'http://127.0.0.1:{cls.port}/api/{path}',data=json.dumps(body).encode() if body is not None else None,headers=headers)
        try:r=urllib.request.urlopen(req)
        except urllib.error.HTTPError as e:r=e
        with r:
            if r.headers.get('Set-Cookie'):cls.cookie=r.headers['Set-Cookie'].split(';')[0]
            return r.status,json.load(r)

    def test_import_lifecycle_and_all_templates(self):
        self.assertEqual(self.request('import/templates')[0],401)
        self.assertEqual(self.request('import/apply',{'revision':0,'package':package({})})[0],401)
        self.assertEqual(self.request('login',{'password':'import-fixture-password'})[0],200)
        _,state=self.request('state');type(self).csrf=state['csrf']
        code,catalog=self.request('import/templates');self.assertEqual(code,200)
        self.assertEqual(set(catalog['guide']['collections']),set(state['data']))
        # Every generic example, its dependencies and the starter must validate.
        for path in sorted((self.root/'templates').glob('*.json')):
            value=json.loads(path.read_text())
            if value.get('kind')!='lifeos-import':continue
            with self.subTest(template=path.name):
                code,result=self.request('import/preview',{'revision':state['revision'],'package':value})
                self.assertEqual(code,200,result)
        starter=package({'areas':[{'id':'starter-area','title':'Starter area'}],
                         'goals':[{'id':'starter-goal','title':'Starter goal','area':'starter-area'}],
                         'projects':[{'id':'starter-project','title':'Starter project','area':'starter-area','goal':'starter-goal'}],
                         'tasks':[{'id':'starter-task','title':'Starter task','project':'starter-project','status':'todo','due':''}],
                         'notes':[{'id':'starter-note','title':'Starter note','project':'starter-project'}]})
        starter['data']={**empty(),**starter['data']}
        self.assertIsInstance(starter['version'],str,'Legacy restore must reject an import package version')
        for kind in ['events','sessions','quran','quranSessions','quranUnits','quranUnitSessions','quranChecks','practiceLogs','metricLogs','routineLogs','timeEntries']:
            self.assertEqual(starter['data'][kind],[],f'{kind} must not invent historical activity')
        preview=self.request('import/preview',{'revision':0,'package':starter})
        self.assertEqual(preview[0],200)
        self.assertEqual(preview[1]['report']['added'],5)
        self.assertEqual(self.request('state')[1]['revision'],0,'Preview must not save')
        # CSRF is required even for authenticated preview.
        csrf=type(self).csrf;type(self).csrf='wrong'
        self.assertEqual(self.request('import/preview',{'revision':0,'package':starter})[0],403)
        type(self).csrf=csrf
        applied=self.request('import/apply',{'revision':0,'package':starter})
        self.assertEqual(applied[0],200,applied)
        self.assertEqual(applied[1]['revision'],1)
        _,saved=self.request('state')
        self.assertEqual(len(saved['data']['tasks']),1)
        self.assertEqual(len(saved['data']['projects']),1)
        self.assertTrue(all(t.get('status')=='todo' and not t.get('bigDate') and not t.get('due') and 'estimate' not in t for t in saved['data']['tasks']))
        self.assertEqual(self.request('import/apply',{'revision':0,'package':starter})[0],409)
        repeated=self.request('import/apply',{'revision':1,'package':starter})
        self.assertEqual(repeated[0],200)
        self.assertEqual(repeated[1]['report']['added'],0)
        self.assertEqual(repeated[1]['revision'],1,'No-op import must not create revision/history')
        self.assertEqual(self.request('state')[1]['data'],saved['data'])
        invalid=package({'events':[{'id':'bad','title':'Bad','date':'2026-11-01','time':None}]})
        self.assertEqual(self.request('import/apply',{'revision':1,'package':invalid})[0],400)
        orphan=package({'notes':[{'id':'orphan','title':'Orphan','project':'absent'}]})
        self.assertEqual(self.request('import/apply',{'revision':1,'package':orphan})[0],400)
        self.assertEqual(self.request('state')[1]['data'],saved['data'])
        self.assertEqual(self.request('state')[1]['revision'],1)
        self.assertEqual(self.request('history')[1]['history'][0]['revision'],0)

if __name__ == '__main__':
    unittest.main()
