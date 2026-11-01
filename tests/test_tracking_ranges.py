import unittest
from tracking_ranges import tracking_range

class TrackingRangesTest(unittest.TestCase):
    def test_three_verses(self):
        r=tracking_range(30,{'kind':'verses','value':107,'from':1,'to':3})
        self.assertEqual(r['verseIds'],['107:1','107:2','107:3'])
        self.assertIn('107.',r['label'])
    def test_lines_cover_only_complete_units(self):
        r=tracking_range(29,{'kind':'lines','value':562,'from':2,'to':7})
        self.assertEqual(r['unitIds'],['29:562:2'])
        self.assertIn('2–7',r['label'])
        self.assertEqual(tracking_range(29,{'kind':'lines','value':562,'from':1,'to':2})['unitIds'],[])
    def test_other_stages(self):
        for j,page,end,expected in [(28,542,10,2),(27,522,7,1),(26,502,14,0),(1,1,15,1)]:
            with self.subTest(j=j):self.assertEqual(len(tracking_range(j,{'kind':'lines','value':page,'from':1,'to':end})['unitIds']),expected)
        self.assertEqual(tracking_range(29,{'kind':'verses','value':67,'from':5,'to':12})['unitIds'],[])
    def test_invalid_ranges(self):
        for j,scope in [(30,{'kind':'verses','value':107,'from':1,'to':8}),(29,{'kind':'lines','value':562,'from':0,'to':4}),
                        (29,{'kind':'lines','value':562,'from':1,'to':16}),(29,{'kind':'lines','value':562,'from':6,'to':3}),
                        (29,{'kind':'lines','value':542,'from':1,'to':3}),(30,{'kind':'lines','value':582,'from':1,'to':3}),
                        (29,{'kind':'lines','value':562,'from':True,'to':3})]:
            with self.subTest(scope=scope),self.assertRaises(ValueError):tracking_range(j,scope)
