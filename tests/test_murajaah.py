import json, sqlite3, unittest
from pathlib import Path
from quran_coverage import coverage
from media_store import clean_metadata, validate_session_reference
ROOT=Path(__file__).resolve().parents[1]

def audio(j=29,kind='page',value=562,**kw):
    return {'title':'Murajaah','date':'2026-11-01','juz':j,'targetVersion':2,
            'scope':{'kind':kind,'value':value},'duration':3600,**kw}

class MurajaahTest(unittest.TestCase):
    def test_whole_page_is_not_one_training_unit(self):
        c=coverage(29,{'kind':'page','value':562})
        self.assertEqual(c['segments'],[[67,1,12]])
        self.assertEqual(c['count'],12)
    def test_full_surah_and_juz(self):
        self.assertEqual(coverage(29,{'kind':'surah','value':67})['segments'],[[67,1,30]])
        c=coverage(30,{'kind':'juz','value':30})
        self.assertEqual(c['count'],564)
        self.assertEqual(c['segments'][0],[78,1,40])
        self.assertEqual(c['segments'][-1],[114,1,6])
        # Full Baqarah must not be truncated at the end of the selected juz.
        self.assertEqual(coverage(1,{'kind':'surah','value':2})['count'],286)
    def test_book_rubu_differs_from_standard(self):
        c=coverage(30,{'kind':'rubu','value':1})
        self.assertEqual(c['segments'][0],[101,1,11])
        self.assertEqual(c['segments'][-1],[114,1,6])
        all_parts=[coverage(30,{'kind':'rubu','value':i}) for i in range(1,9)]
        self.assertEqual(sum(x['count'] for x in all_parts),564)
        self.assertIn('buku',c['label'])
        c=coverage(29,{'kind':'rubu','value':1})
        self.assertEqual(c['segments'],[[67,1,30]])
        self.assertIn('standar',c['label'])
    def test_invalid_cross_context_and_nonintegers(self):
        for j,scope in [(29,{'kind':'page','value':-1}),(29,{'kind':'page','value':582}),
                        (29,{'kind':'surah','value':101}),(30,{'kind':'rubu','value':9}),
                        (30,{'kind':'juz','value':29}),(True,{'kind':'juz','value':1}),
                        (29,{'kind':'page','value':True}),(29,{'kind':'page','value':'562'}),
                        (29,{'kind':'unit','value':1}),(29,None)]:
            with self.subTest(j=j,scope=scope),self.assertRaises(ValueError):coverage(j,scope)
    def test_all_juz_partition_6236_verses_and_standard_rubu_partition(self):
        cs=[coverage(j,{'kind':'juz','value':j}) for j in range(1,31)]
        self.assertEqual(sum(c['count'] for c in cs),6236)
        for a,b in zip(cs,cs[1:]):self.assertEqual(a['end'],b['start'])
        for j in range(1,30):
            parts=[coverage(j,{'kind':'rubu','value':i}) for i in range(1,9)]
            self.assertEqual(parts[0]['start'],cs[j-1]['start'])
            self.assertEqual(parts[-1]['end'],cs[j-1]['end'])
            self.assertEqual(sum(c['count'] for c in parts),cs[j-1]['count'])
    def test_text_count_license_and_offsets(self):
        raw=(ROOT/'static/quran-uthmani.txt').read_text()
        lines=[l for l in raw.splitlines() if l and not l.startswith('#')]
        self.assertEqual(len(lines),6236)
        self.assertIn('Tanzil Quran Text (Uthmani, Version 1.1)',raw)
        meta=json.loads((ROOT/'static/quran-coverage.json').read_text())
        self.assertEqual(sum(s['count'] for s in meta['chapters']),6236)
        self.assertEqual(meta['chapters'][66]['count'],30)
        self.assertEqual(len(lines[meta['chapters'][66]['start']:meta['chapters'][66]['start']+30]),30)
    def test_server_canonical_metadata_and_scope_session_containment(self):
        cleaned=clean_metadata(audio(target='client label must not be trusted'))
        self.assertEqual(cleaned['target'],'Halaman 562 utuh')
        self.assertEqual(cleaned['scope'],{'kind':'page','value':562})
        with sqlite3.connect(':memory:') as conn:
            conn.execute('CREATE TABLE state(id INTEGER PRIMARY KEY,body TEXT)')
            conn.execute('INSERT INTO state VALUES(1,?)',(json.dumps({'quranChecks':[{'id':'m1','coverageVersion':1,'juz':29,'scope':{'kind':'surah','value':67}}]}),))
            validate_session_reference(conn,clean_metadata(audio(reviewSession='m1')))
            with self.assertRaises(ValueError):validate_session_reference(conn,clean_metadata(audio(kind='juz',value=29,reviewSession='m1')))
            with self.assertRaises(ValueError):validate_session_reference(conn,clean_metadata(audio(reviewSession='missing')))
        with self.assertRaises(ValueError):clean_metadata(audio(session='old-training-session'))
