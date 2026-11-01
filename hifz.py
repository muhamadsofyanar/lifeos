"""Metadata constraints for Sullamul Hifz. Page locations refer to 604-page Madinah mushaf."""
import math

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
        if not isinstance(item.get('minutes'),(int,float)) or not math.isfinite(item['minutes']) or not 0<item['minutes']<=240:
            raise ValueError('Durasi hafalan harus 1–240 menit.')
        juz=item.get('juz')
        if type(juz) is not int or not 1<=juz<=29:raise ValueError('Juz sesi tidak valid.')
        if not isinstance(item.get('units'),list) or not item['units'] or len(item['units'])>2 or any(u not in unit_ids(juz) for u in item['units']):
            raise ValueError('Rentang sesi hafalan tidak valid.')
    for item in data['dayPlans']:
        for key in ['work','rest','contemplation','quran','fixed','buffer']:
            val=item.get(key,0)
            if not isinstance(val,(int,float)) or not math.isfinite(val) or not 0<=val<=1440:raise ValueError('Alokasi waktu tidak valid.')
        if sum(item.get(k,0) for k in ['work','rest','contemplation','quran','fixed','buffer'])>1440:raise ValueError('Alokasi melebihi 24 jam.')
    for item in data['metricLogs']:
        if not isinstance(item.get('value'),(int,float)) or not math.isfinite(item['value']):raise ValueError('Nilai indikator harus angka valid.')
