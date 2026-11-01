"""Validate persisted shapes at the HTTP/backup boundary without inventing legacy values."""
import math
import re
from workflow import number, valid_date


def text_fields(item, keys, context):
    for key in keys.split():
        if key in item and not isinstance(item[key], str):
            raise ValueError(f'{context}.{key} harus teks.')


def date_fields(item, keys, context):
    for key in keys.split():
        if key not in item or item[key] == '' or (key in ['completedDay', 'bigDate', 'reviewCompleted'] and item[key] is None):
            continue
        if not valid_date(item[key]):
            raise ValueError(f'{context}.{key} harus tanggal YYYY-MM-DD yang valid.')


def measurement(item, context):
    text_fields(item, 'metric title unit baseline target period source', context)
    if 'measurementVersion' in item and (type(item['measurementVersion']) is not int or item['measurementVersion'] != 1):
        raise ValueError('Versi definisi pengukuran tidak dikenali.')
    if item.get('measurementVersion') == 1:
        keys = ['unit', 'baseline', 'target', 'period', 'source']
        keys.append('metric' if context == 'goals' else 'title')
        if any(not isinstance(item.get(k), str) or not item[k].strip() for k in keys):
            raise ValueError('Lengkapi indikator, satuan, kondisi awal, target, periode, dan sumber data. Isi belum diketahui secara eksplisit bila data belum tersedia.')


def json_values(value, depth=0):
    if depth > 30:
        raise ValueError('Struktur data terlalu dalam.')
    if isinstance(value, float) and not math.isfinite(value):
        raise ValueError('Angka harus bernilai hingga; NaN/Infinity tidak diizinkan.')
    if isinstance(value, dict):
        for item in value.values():
            json_values(item, depth + 1)
    elif isinstance(value, list):
        for item in value:
            json_values(item, depth + 1)


def validate_shapes(data):
    json_values(data)
    common = 'title body note teacher source measurementSource project area goal task parent folder tags result priority repeat mode load status kind decision assessor nextReview learning action lesson exercise evidence insight metric baseline target unit period frequency outcome why idea steps estimates reviewDate time'
    # Every listed field is rendered or used as text by the browser. Missing legacy
    # optional fields remain missing; malformed types must never enter new state.
    for kind, records in data.items():
        for item in records:
            if not item['id'] or len(item['id']) > 250 or any(ord(c) < 32 for c in item['id']):
                raise ValueError(f'{kind}: ID kosong, terlalu panjang, atau mengandung karakter kontrol.')
            text_fields(item, common, kind)
            date_fields(item, 'date due day startDate nextReview reviewDate completedDay bigDate reviewCompleted', kind)
            for key in ['created', 'updated']:
                if key in item and not number(item[key], 0, 253402300799999):
                    raise ValueError(f'{kind}.{key} harus timestamp valid.')

    for event in data['events']:
        if not valid_date(event.get('date')):
            raise ValueError('Tanggal agenda tidak valid.')
        if any(not isinstance(event.get(k), str) or not re.fullmatch(r'(?:[01]\d|2[0-3]):[0-5]\d', event[k]) for k in ['time', 'until']):
            raise ValueError('Jam agenda harus HH:MM.')
        if event['until'] <= event['time']:
            raise ValueError('Waktu selesai agenda harus setelah mulai pada tanggal yang sama.')

    for task in data['tasks']:
        if task.get('status', 'todo') not in ['todo', 'doing', 'done', 'later', 'waiting']:
            raise ValueError('Status tugas tidak valid.')
        if 'estimate' in task:
            try:
                estimate = float(task['estimate'])
            except (ValueError, TypeError):
                raise ValueError('Estimasi tugas harus angka.')
            if isinstance(task['estimate'], bool) or not math.isfinite(estimate) or not 0 <= estimate <= 10080:
                raise ValueError('Estimasi tugas harus 0–10080 menit.')

    for session in data['sessions']:
        start, end = session.get('start'), session.get('end')
        if not number(start, 0, 253402300799999):
            raise ValueError('Waktu mulai sesi fokus tidak valid.')
        if end is not None and (not number(end, start, 253402300799999)):
            raise ValueError('Waktu selesai sesi fokus tidak valid.')
        if 'duration' in session and not number(session['duration'], 1, 240):
            raise ValueError('Target fokus harus 1–240 menit.')

    for plan in data['plans']:
        if 'step' in plan and (type(plan['step']) is not int or not 0 <= plan['step'] <= 5):
            raise ValueError('Langkah planner tidak valid.')
        for key in ['minutes', 'capacity']:
            if key in plan:
                try:
                    value = float(plan[key])
                except (ValueError, TypeError):
                    raise ValueError('Durasi planner harus angka.')
                if isinstance(plan[key], bool) or not math.isfinite(value) or value <= 0:
                    raise ValueError('Durasi planner harus positif dan hingga.')

    for kind in ['metricLogs', 'practiceLogs']:
        for item in data[kind]:
            if not valid_date(item.get('date')):
                raise ValueError(f'{kind}: tanggal pencatatan diperlukan.')

    for check in data['quranChecks']:
        if type(check.get('juz')) is not int or not 1 <= check['juz'] <= 30 or not valid_date(check.get('date')):
            raise ValueError('Juz/tanggal evaluasi tidak valid.')
        scores = [check.get('score' + str(i), 'belum') for i in range(5)]
        if any(score not in ['belum', 'kuat', 'cukup', 'ulang'] for score in scores):
            raise ValueError('Nilai evaluasi hafalan tidak valid.')
        if check.get('decision') == 'Siap melanjutkan' and any(score in ['belum', 'ulang'] for score in scores):
            raise ValueError('Lengkapi evaluasi sebelum menyatakan siap melanjutkan.')

    for goal in data['goals']:
        measurement(goal, 'goals')
        indicators = goal.get('indicators', [])
        if not isinstance(indicators, list) or len(indicators) > 200:
            raise ValueError('Daftar indikator Goal harus berupa array (maksimal 200).')
        ids = set()
        for indicator in indicators:
            if not isinstance(indicator, dict) or not isinstance(indicator.get('id'), str) or not indicator['id'] or indicator['id'] in ids:
                raise ValueError('ID indikator tidak valid atau duplikat.')
            ids.add(indicator['id'])
            measurement(indicator, 'indicators')

    for pref in data['preferences']:
        pid = pref['id']
        if pid == 'pomodoro':
            if 'enabled' in pref and type(pref['enabled']) is not bool:
                raise ValueError('Status Pomodoro harus boolean.')
            for key, upper in [('short', 120), ('long', 120), ('rounds', 12)]:
                if key in pref and (type(pref[key]) is not int or not 1 <= pref[key] <= upper):
                    raise ValueError('Pengaturan durasi/ronde Pomodoro tidak valid.')
        if pid == 'quran':
            for key, low, high in [('minutes', 20, 30), ('newMinutes', 0, 10)]:
                if key in pref and not number(pref[key], low, high):
                    raise ValueError('Pengaturan durasi Al-Qur’an tidak valid.')
        if pid == 'focus-rounds' and (type(pref.get('count')) is not int or pref['count'] < 0):
            raise ValueError('Jumlah ronde fokus tidak valid.')
        if pid == 'focus-break':
            if any(not number(pref.get(k), 0, 253402300799999) for k in ['start', 'until']) or pref['until'] < pref['start']:
                raise ValueError('Waktu jeda fokus tidak valid.')
            if not number(pref.get('duration'), 1, 120) or type(pref.get('done')) is not bool:
                raise ValueError('Durasi/status jeda fokus tidak valid.')
