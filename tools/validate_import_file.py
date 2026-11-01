"""Validate a local import package without touching application data."""
import json
import os
from pathlib import Path
import sys
import tempfile

root=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(root))
if len(sys.argv)!=2:raise SystemExit('Usage: python3 tools/validate_import_file.py FILE.json')
package=json.loads(Path(sys.argv[1]).read_text())
with tempfile.TemporaryDirectory() as temp:
    os.environ['DATA_DIR']=temp
    import server
    incoming=server.unpack(package,set(server.KINDS))
    server.validate({k:incoming.get(k,[]) for k in server.KINDS})
    empty={k:[] for k in server.KINDS}
    merged,report=server.merge_import(empty,package)
    server.validate(merged)
    second,again=server.merge_import(merged,package)
    assert second==merged and again['added']==0
    print(json.dumps({'valid':True,'added':report['added'],'collections':{k:len(v) for k,v in merged.items() if v},'repeat_added':again['added']},ensure_ascii=False))
