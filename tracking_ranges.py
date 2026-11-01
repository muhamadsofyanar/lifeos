"""Exact practice ranges; only complete staged units may update unit progress."""
from quran_coverage import coverage
from hifz import page_range

def tracking_range(juz,scope):
    if type(juz) is not int or not 1<=juz<=30 or not isinstance(scope,dict):raise ValueError('Pilih juz dan rentang latihan.')
    kind=scope.get('kind');value=scope.get('value');first,last=scope.get('from'),scope.get('to')
    if any(type(v) is not int for v in [value,first,last]):raise ValueError('Rentang harus bilangan bulat.')
    if kind=='verses':
        c=coverage(juz,scope)
        whole=coverage(juz,{'kind':'juz','value':juz})
        if c['start']<whole['start'] or c['end']>whole['end']:raise ValueError('Rentang ayat harus berada dalam juz pilihan.')
        return {'scope':c['scope'],'label':c['label'],'verseIds':[f'{value}:{a}' for a in range(first,last+1)] if juz==30 else [],'unitIds':[]}
    if kind!='lines' or juz==30:raise ValueError('Rentang baris tersedia pada tahap Juz 1–29.')
    a,b=page_range(juz)
    if not a<=value<=b or not 1<=first<=last<=15:raise ValueError('Pilih halaman sesuai juz dan baris 1–15 berurutan.')
    parts=5 if juz==29 else 3 if juz==28 else 2 if juz==27 else 1
    spans=[(1,7),(8,15)] if parts==2 else [(i*15//parts+1,(i+1)*15//parts) for i in range(parts)]
    ids=[f'{juz}:{value}:{i+1}' for i,(lo,hi) in enumerate(spans) if first<=lo and hi<=last]
    return {'scope':{'kind':kind,'value':value,'from':first,'to':last},'label':f'Halaman {value} · baris {first}–{last}','verseIds':[],'unitIds':ids}
