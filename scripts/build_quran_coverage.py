"""Build coverage indices from the bundled, attributed Tanzil XML metadata."""
import hashlib,json,xml.etree.ElementTree as ET
from pathlib import Path
root=Path(__file__).resolve().parents[1]
x=ET.parse(root/'sources/quran-data.xml').getroot()
chapters=[{'number':int(s.attrib['index']),'name':s.attrib['tname'],'arabic':s.attrib['name'],'count':int(s.attrib['ayas']),'start':int(s.attrib['start'])} for s in x.find('suras')]
starts=lambda tag:[[int(e.attrib['sura']),int(e.attrib['aya'])] for e in x.find(tag)]
raw=(root/'static/quran-uthmani.txt').read_bytes()
assert len([s for s in raw.decode().splitlines() if s and not s.startswith('#')])==6236
meta={'source':'Tanzil Project · Quran metadata v1.0','url':'https://tanzil.net/docs/Quran_Metadata','textSource':'Tanzil Quran Text (Uthmani, Version 1.1)','textUrl':'https://tanzil.net','textSha256':hashlib.sha256(raw).hexdigest(),'chapters':chapters,'juzs':starts('juzs'),'rubs':starts('hizbs'),'pages':json.loads((root/'static/quran-meta.json').read_text())['pages'],'bookRubu30':[[101,114],[94,100],[90,93],[87,89],[84,86],[82,83],[80,81],[78,79]]}
assert len(meta['rubs'])==240 and len(meta['juzs'])==30
(root/'static/quran-coverage.json').write_text(json.dumps(meta,ensure_ascii=False,separators=(',',':'))+'\n')
print('Built coverage metadata; raw text SHA256',meta['textSha256'])
