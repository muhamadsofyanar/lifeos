import json
from pathlib import Path
import sqlite3
import unittest
from media_store import clean_metadata, validate_session_reference

ROOT=Path(__file__).resolve().parents[1]


def meta(**updates):
    return {'title':'Fixture audio','date':'2026-11-01','juz':30,'target':'Al-Qari’ah ayat 1–11',
            'targetVersion':1,'surah':101,'from':1,'to':11,'duration':20,**updates}


class AudioTargetTest(unittest.TestCase):
    def setUp(self):
        self.conn=sqlite3.connect(':memory:')
        self.conn.execute('CREATE TABLE state(id INTEGER PRIMARY KEY,body TEXT)')
        state={'quranSessions':[{'id':'q1','surah':101,'from':1,'to':5}],
               'quranUnitSessions':[{'id':'u29','juz':29,'units':['29:562:1']},{'id':'u28','juz':28,'units':['28:542:1']}]}
        self.conn.execute('INSERT INTO state VALUES(1,?)',(json.dumps(state),))

    def tearDown(self):
        self.conn.close()

    def test_verse_limits_match_bundled_metadata_for_every_juz30_surah(self):
        chapters=json.loads((ROOT/'static/quran-meta.json').read_text())['surahs']
        for chapter in chapters:
            if chapter['number']<78:continue
            number,count=chapter['number'],chapter['ayahs']
            with self.subTest(surah=number):
                accepted=clean_metadata(meta(surah=number,**{'from':1,'to':count}))
                self.assertEqual(accepted['to'],count)
                with self.assertRaises(ValueError):clean_metadata(meta(surah=number,**{'from':1,'to':count+1}))

    def test_negative_zero_boolean_and_reversed_ranges_are_rejected(self):
        for update in [{'from':-1},{'to':-1},{'from':0},{'from':True},{'to':True},{'from':8,'to':3},
                       {'surah':102,'to':9},{'targetVersion':True}]:
            with self.subTest(update=update),self.assertRaises(ValueError):
                clean_metadata(meta(**update))

    def test_session_must_exist_in_correct_juz(self):
        for bad in [meta(session='missing',to=1),meta(session='u29',to=1),
                    meta(juz=29,unit='29:562:1',session='u28')]:
            with self.subTest(meta=bad),self.assertRaises(ValueError):
                validate_session_reference(self.conn,clean_metadata(bad))

    def test_linked_recording_may_cover_a_subset_but_not_outside_session(self):
        validate_session_reference(self.conn,clean_metadata(meta(session='q1',to=2)))
        for bad in [meta(session='q1',to=6),meta(session='q1',surah=102,to=2)]:
            with self.subTest(meta=bad),self.assertRaises(ValueError):
                validate_session_reference(self.conn,clean_metadata(bad))

    def test_unit_must_belong_to_juz_and_selected_session(self):
        valid=clean_metadata(meta(juz=29,unit='29:562:1',session='u29'))
        validate_session_reference(self.conn,valid)
        with self.assertRaises(ValueError):clean_metadata(meta(juz=29,unit='28:542:1'))
        with self.assertRaises(ValueError):validate_session_reference(self.conn,clean_metadata(meta(juz=29,unit='29:562:2',session='u29')))

    def test_legacy_audio_metadata_remains_readable(self):
        old={'title':'Old audio','date':'2026-11-01','juz':29,'target':'Old label','session':'u29','duration':0}
        cleaned=clean_metadata(old)
        self.assertNotIn('targetVersion',cleaned)
        validate_session_reference(self.conn,cleaned)
