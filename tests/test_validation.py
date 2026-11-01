import importlib.util
import os
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class StateValidationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        old = os.environ.get('DATA_DIR')
        os.environ['DATA_DIR'] = cls.tmp.name
        sys.path.insert(0, str(ROOT))
        try:
            spec = importlib.util.spec_from_file_location('validation_server', ROOT / 'server.py')
            cls.server = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(cls.server)
        finally:
            if old is None:
                os.environ.pop('DATA_DIR', None)
            else:
                os.environ['DATA_DIR'] = old

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def state(self, kind, item):
        data = {k: [] for k in self.server.KINDS}
        data[kind] = [item]
        return data

    def test_rejects_renderer_breaking_shapes(self):
        invalid = [
            ('events', {'id': 'e', 'date': '2026-11-01', 'time': None}),
            ('events', {'id': 'e', 'date': '2026-11-01', 'time': '10:00', 'until': '09:00'}),
            ('goals', {'id': 'g', 'title': 'Goal', 'indicators': {}}),
            ('goals', {'id': 'g', 'title': 'Goal', 'indicators': [{'id': 'i', 'title': None}]}),
            ('preferences', {'id': 'pomodoro', 'rounds': 0}),
            ('preferences', {'id': 'pomodoro', 'enabled': 'yes'}),
            ('quranSessions', {'id': 'q', 'minutes': True}),
            ('quranSessions', {'id': 'q', 'minutes': 20, 'date': '2026-02-30'}),
            ('quranSessions', {'id': 'q', 'minutes': 20, 'surah': 101, 'from': 1, 'to': 99}),
            ('sessions', {'id': 's', 'start': 'bad timestamp', 'end': None}),
            ('notes', {'id': 'n', 'title': 'Note', 'body': []}),
            ('plans', {'id': 'p', 'step': 99}),
        ]
        for kind, item in invalid:
            with self.subTest(kind=kind, item=item), self.assertRaises(ValueError):
                self.server.validate(self.state(kind, item))

    def test_legacy_optional_fields_remain_accepted(self):
        for kind, item in [
            ('tasks', {'id': 'old', 'title': 'Legacy task', 'status': 'todo'}),
            ('quranSessions', {'id': 'q', 'minutes': 25, 'date': '2026-11-01'}),
            ('quranUnitSessions', {'id': 'h', 'juz': 1, 'minutes': 25, 'units': ['1:2:1']}),
        ]:
            self.server.validate(self.state(kind, item))

    def test_two_page_session_contract(self):
        good = {'id': 's2', 'sessionVersion': 2, 'juz': 1, 'minutes': 25,
                'date': '2026-11-01', 'units': ['1:2:1', '1:3:1'],
                'load': 'S2', 'status': 'self', 'connection': 'self'}
        self.server.validate(self.state('quranUnitSessions', good))
        for update in [{'units': ['1:2:1']}, {'units': ['1:2:1', '1:4:1']},
                       {'connection': 'teacher', 'teacher': ''}, {'connection': 'bogus'},
                       {'load': 'N', 'units': ['1:2:1']}]:
            with self.subTest(update=update), self.assertRaises(ValueError):
                self.server.validate(self.state('quranUnitSessions', {**good, **update}))

    def test_new_measurement_definition(self):
        item = {'id': 'g', 'title': 'Goal', 'measurementVersion': 1,
                'metric': 'Waktu respons', 'unit': 'jam', 'baseline': '48',
                'target': '24', 'period': 'per pekan', 'source': 'Log layanan'}
        self.server.validate(self.state('goals', item))
        for key in ['unit', 'baseline', 'target', 'period', 'source']:
            with self.subTest(key=key), self.assertRaises(ValueError):
                self.server.validate(self.state('goals', {**item, key: ''}))

    def test_academy_preferences_validate_nested_shapes(self):
        valid={'id':'academy-learning-v1','results':{'smart':{'answer':1,'evidence':'Cakupan dan sumber perlu diperiksa.','savedDate':'2026-11-01'}}}
        self.server.validate(self.state('preferences',valid))
        self.server.validate(self.state('preferences',{'id':'academy-smart-draft-v1','draft':{'outcome':'Draft tujuan','goalId':''},'step':2}))
        for pref in [{'id':'academy-learning-v1','results':None},
                     {'id':'academy-learning-v1','results':{'unknown':{}}},
                     {'id':'academy-smart-draft-v1','draft':[],'step':0},
                     {'id':'academy-smart-draft-v1','draft':{'outcome':42},'step':0},
                     {'id':'academy-smart-draft-v1','draft':{},'step':5}]:
            with self.subTest(pref=pref),self.assertRaises(ValueError):
                self.server.validate(self.state('preferences',pref))
