"""Metadata constraints for Sullamul Hifz. Page locations refer to 604-page Madinah mushaf."""
import math
from workflow import number

def page_range(juz):
    if juz == 1: return 1,21
    if juz == 30: return 582,604
    return (juz-1)*20+2,juz*20+1

def unit_ids(juz):
    start,end=page_range(juz)
    parts=5 if juz==29 else 3 if juz==28 else 2 if juz==27 else 1
    return {f'{juz}:{page}:{part}' for page in range(start,end+1) for part in range(1,parts+1)}

def validate_units(data):
    statuses={'practiced','strengthen','self','teacher'}
    for item in data['quranUnits']:
        juz=item.get('juz')
        if type(juz) is not int or not 1<=juz<=29 or item['id'] not in unit_ids(juz):
            raise ValueError('Unit hafalan tidak sesuai halaman/tahap.')
        if item.get('status') not in statuses:raise ValueError('Status hafalan tidak valid.')
        if item.get('status')=='teacher' and not str(item.get('teacher','')).strip():raise ValueError('Isi nama penyimak.')
    for item in data['quranUnitSessions']:
        if 'sessionVersion' in item and (type(item['sessionVersion']) is not int or item['sessionVersion']!=2):raise ValueError('Versi catatan sesi tidak dikenali.')
        if not number(item.get('minutes'),1,240):
            raise ValueError('Durasi hafalan harus 1–240 menit.')
        juz=item.get('juz')
        if type(juz) is not int or not 1<=juz<=29:raise ValueError('Juz sesi tidak valid.')
        if not isinstance(item.get('units'),list) or not item['units'] or len(item['units'])>2 or any(not isinstance(u,str) or u not in unit_ids(juz) for u in item['units']) or len(set(item['units'])) != len(item['units']):
            raise ValueError('Rentang sesi hafalan tidak valid.')
        if 'status' in item and item['status'] not in statuses:raise ValueError('Penilaian sesi tidak valid.')
        if item.get('status')=='teacher' and not item.get('teacher','').strip():raise ValueError('Isi nama penyimak sesi.')
        if item.get('sessionVersion') == 2:
            units=item['units'];load=item.get('load');connection=item.get('connection','not_checked')
            if load not in (['N','S','S2'] if juz<=25 else ['sesuai tahap','kecil']):raise ValueError('Beban sesi tidak sesuai tahap.')
            if load=='S2':
                if len(units)!=2 or int(units[1].split(':')[1])!=int(units[0].split(':')[1])+1:raise ValueError('S2 harus mencakup dua halaman berurutan dalam juz yang sama.')
            elif len(units)!=1:raise ValueError('Beban ini hanya mencakup satu unit.')
            if connection not in ['not_checked','strengthen','self','teacher'] or (load!='S2' and connection!='not_checked'):raise ValueError('Penilaian sambungan tidak valid.')
            if connection=='teacher' and not item.get('teacher','').strip():raise ValueError('Isi nama penyimak sambungan.')
            if load in ['N','kecil'] and item.get('status') in ['self','teacher']:raise ValueError('Potongan kecil belum membuktikan kelancaran seluruh unit.')
    for item in data['dayPlans']:
        for key in ['work','rest','contemplation','quran','fixed','buffer']:
            val=item.get(key,0)
            if not number(val,0,1440):raise ValueError('Alokasi waktu tidak valid.')
        if sum(item.get(k,0) for k in ['work','rest','contemplation','quran','fixed','buffer'])>1440:raise ValueError('Alokasi melebihi 24 jam.')
    for item in data['metricLogs']:
        if isinstance(item.get('value'),bool) or not isinstance(item.get('value'),(int,float)) or not math.isfinite(item['value']):raise ValueError('Nilai indikator harus angka valid.')
