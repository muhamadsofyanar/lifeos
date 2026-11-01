"""Canonical whole-page/surah/book-rubu/standard-rubu/juz coverage, zero-based offsets."""
import json
from pathlib import Path
from functools import lru_cache

@lru_cache(maxsize=1)
def metadata():
    return json.loads((Path(__file__).resolve().parent/'static/quran-coverage.json').read_text())

def coverage(juz,scope):
    if type(juz) is not int or not 1<=juz<=30 or not isinstance(scope,dict):raise ValueError('Pilih juz dan cakupan murajaah.')
    kind,value=scope.get('kind'),scope.get('value')
    if type(value) is not int:raise ValueError('Nilai cakupan harus bilangan bulat.')
    m=metadata();chapters=m['chapters']
    def ordinal(pair):return chapters[pair[0]-1]['start']+pair[1]-1
    ja=ordinal(m['juzs'][juz-1]);jb=ordinal(m['juzs'][juz]) if juz<30 else 6236
    if kind=='juz':
        if value!=juz:raise ValueError('Juz cakupan tidak sesuai juz pilihan.')
        a,b=ja,jb;label=f'Juz {juz} utuh'
    elif kind=='page':
        parts=m['pages'].get(str(value))
        if not parts:raise ValueError('Halaman harus 1–604.')
        a=ordinal([parts[0]['surah'],parts[0]['from']]);b=ordinal([parts[-1]['surah'],parts[-1]['to']])+1
        label=f'Halaman {value} utuh'
    elif kind=='surah':
        if not 1<=value<=114:raise ValueError('Surah harus 1–114.')
        s=chapters[value-1];a=s['start'];b=a+s['count'];label=f"Surah {s['name']} utuh"
    elif kind=='verses':
        if not 1<=value<=114:raise ValueError('Surah harus 1–114.')
        s=chapters[value-1];first,last=scope.get('from'),scope.get('to')
        if type(first) is not int or type(last) is not int or not 1<=first<=last<=s['count']:raise ValueError('Rentang ayat tidak sesuai surah.')
        a=s['start']+first-1;b=s['start']+last;label=f"{value}. {s['name']} · ayat {first}–{last}"
    elif kind=='rubu':
        if not 1<=value<=8:raise ValueError('Rubu harus 1–8.')
        if juz==30:
            first,last=m['bookRubu30'][value-1];a=chapters[first-1]['start'];b=chapters[last-1]['start']+chapters[last-1]['count'];label=f'Rubu {value} buku utuh · Juz 30'
        else:
            i=(juz-1)*8+value-1;a=ordinal(m['rubs'][i]);b=ordinal(m['rubs'][i+1]) if i<239 else 6236;label=f'Rubu {value} standar utuh · Juz {juz}'
    else:raise ValueError('Jenis cakupan murajaah tidak dikenal.')
    if not a<jb or not b>ja:raise ValueError('Cakupan tidak bersinggungan dengan juz pilihan.')
    segments=[]
    for s in chapters:
        lo=max(a,s['start']);hi=min(b,s['start']+s['count'])
        if lo<hi:segments.append([s['number'],lo-s['start']+1,hi-s['start']])
    cleaned={'kind':kind,'value':value}
    if kind=='verses':cleaned.update({'from':first,'to':last})
    return {'scope':cleaned,'label':label,'segments':segments,'count':b-a,'start':a,'end':b,'crossJuz':a<ja or b>jb}
