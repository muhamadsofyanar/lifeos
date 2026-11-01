import datetime,math,re

def valid_date(value):
    if not isinstance(value,str) or not re.fullmatch(r'\d{4}-\d{2}-\d{2}',value):return False
    try:datetime.date.fromisoformat(value);return True
    except (ValueError,TypeError):return False

def number(v,lo=0,hi=1440):return isinstance(v,(int,float)) and not isinstance(v,bool) and math.isfinite(v) and lo<=v<=hi

def validate_workflow(data):
    for r in data['routines']:
        if not isinstance(r.get('title'),str) or not r['title'].strip():raise ValueError('Nama rutinitas diperlukan.')
        days=r.get('days')
        if not isinstance(days,list) or not days or any(type(d) is not int or not 0<=d<=6 for d in days) or len(set(days))!=len(days):raise ValueError('Pilih hari rutinitas yang valid.')
        if not valid_date(r.get('start')) or not number(r.get('minutes'),1,1440):raise ValueError('Tanggal/durasi rutinitas tidak valid.')
    seen=set()
    for l in data['routineLogs']:
        if not valid_date(l.get('date')) or not isinstance(l.get('routine'),str) or l.get('status') not in ['done','skip']:raise ValueError('Catatan rutinitas tidak valid.')
        key=(l['routine'],l['date'])
        if key in seen:raise ValueError('Rutinitas hanya dapat dicatat sekali per tanggal.')
        seen.add(key)
    for t in data['timeEntries']:
        if not valid_date(t.get('date')) or not number(t.get('minutes'),1,1440) or not isinstance(t.get('title'),str) or not t['title'].strip():raise ValueError('Catatan waktu tidak valid.')
