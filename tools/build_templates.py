"""Generate documented generic templates for every supported collection."""
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'templates'
KINDS=['inbox','tasks','projects','notes','events','sessions','reviews','areas','goals','quran','quranSessions','plans','preferences','quranUnits','quranUnitSessions','quranChecks','learning','practiceLogs','dayPlans','metricLogs','routines','routineLogs','timeEntries']
LABELS=['Inbox','Tasks','Projects','Notes','Calendar','Riwayat Focus','Review','Area kehidupan','Goal / Tujuan','Mutabaah Juz 30','Sesi Juz 30','Idea Planner','Pengaturan','Mutabaah unit','Sesi unit','Evaluasi hafalan','Belajar & Praktik','Riwayat praktik','Anggaran hari','Angka indikator Goal','Rutinitas','Catatan rutinitas','Catatan waktu manual']

def write(name,value):
    (OUT/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')

def empty():return {k:[] for k in KINDS}
def pack(name,data,purpose):return {'kind':'lifeos-import','version':'1.0','purpose':purpose,'name':name,'data':data}

example=empty(); day='2000-01-01'
example['areas']=[{'id':'demo-area','title':'CONTOH FIKTIF — Area belajar','body':'Hanya contoh bentuk kolom; bukan data pribadi.'}]
example['goals']=[{'id':'demo-goal','title':'CONTOH FIKTIF — Memperbaiki hasil latihan','body':'Contoh fiktif, ubah sebelum digunakan.','area':'demo-area','due':'','metric':'Hasil latihan','unit':'poin','baseline':'Belum diketahui','target':'Tentukan setelah pengukuran awal','period':'per evaluasi','source':'Catatan latihan contoh','measurementVersion':1,'indicators':[{'id':'demo-indicator','title':'CONTOH FIKTIF — Nilai latihan','unit':'poin','baseline':'Belum diketahui','target':'Tentukan setelah pengukuran awal','period':'per evaluasi','source':'Lembar latihan contoh','measurementVersion':1}]}]
example['projects']=[{'id':'demo-project','title':'CONTOH FIKTIF — Menyiapkan latihan','body':'Selesai ketika bahan latihan tersedia.','area':'demo-area','goal':'demo-goal'}]
example['tasks']=[{'id':'demo-task','title':'CONTOH FIKTIF — Tulis bahan latihan','project':'demo-project','status':'todo','priority':'normal','estimate':'25','due':'','repeat':'none','result':'Bahan contoh tersedia.','parent':''}]
example['inbox']=[{'id':'demo-inbox','title':'CONTOH FIKTIF — Ide yang belum diurai','body':'Tulis pikiran mentah di sini.'}]
example['notes']=[{'id':'demo-note','title':'CONTOH FIKTIF — Referensi latihan','body':'# Informasi\nIsi catatan di sini.','project':'demo-project','folder':'Contoh','tags':'contoh,fiktif'}]
example['events']=[{'id':'demo-event','title':'CONTOH FIKTIF — Jadwal latihan','date':day,'time':'09:00','until':'09:30','task':'demo-task','category':'Belajar'}]
example['sessions']=[{'id':'demo-focus','task':'demo-task','start':946684800000,'end':946686300000,'duration':25,'day':day,'energy':'3','distraction':'CONTOH FIKTIF — bukan sesi nyata'}]
example['reviews']=[{'id':'demo-review','type':'Harian','date':day,'good':'CONTOH FIKTIF — hasil latihan','lesson':'Pelajaran contoh','next':'Tindakan contoh','feeling':'Catatan contoh','reduce':'Yang dikurangi','recovery':'Ruang istirahat'}]
example['quran']=[{'id':'101:1','surah':101,'ayah':1,'status':'practiced','teacher':'','date':day,'note':'CONTOH FIKTIF — bukan penilaian hafalan nyata'}]
example['quranSessions']=[{'id':'demo-qsession','date':day,'minutes':20,'surah':101,'from':1,'to':1,'mode':'Murajaah saja','status':'practiced','teacher':'','note':'CONTOH FIKTIF — bukan sesi nyata','created':946684800000}]
example['plans']=[{'id':'demo-plan','source':'demo-inbox','idea':'CONTOH FIKTIF — Menyiapkan latihan','step':0,'minutes':25,'capacity':120,'area':'demo-area','applied':False}]
example['preferences']=[{'id':'pomodoro','enabled':False,'short':5,'long':15,'rounds':4}]
example['quranUnits']=[{'id':'29:562:1','juz':29,'status':'practiced','teacher':'','date':day,'note':'CONTOH FIKTIF — bukan penilaian nyata'}]
example['quranUnitSessions']=[{'id':'demo-usession','sessionVersion':2,'juz':29,'units':['29:562:1'],'date':day,'minutes':20,'load':'sesuai tahap','status':'practiced','connection':'not_checked','teacher':'','note':'CONTOH FIKTIF — bukan sesi nyata','created':946684800000}]
example['quranChecks']=[{'id':'demo-check','juz':30,'date':day,'kind':'Penjagaan setelah jeda','score0':'belum','score1':'belum','score2':'belum','score3':'belum','score4':'belum','decision':'Kuatkan dahulu','assessor':'','note':'CONTOH FIKTIF — bukan pemeriksaan nyata','nextReview':''}]
example['learning']=[{'id':'demo-learning','title':'CONTOH FIKTIF — Pelajaran latihan','source':'Bahan contoh','insight':'Hal yang dipahami','exercise':'Latihan yang akan dicoba','evidence':'Tanda hasil dapat diperiksa','area':'demo-area','project':'demo-project','nextReview':''}]
example['practiceLogs']=[{'id':'demo-practice','learning':'demo-learning','date':day,'action':'CONTOH FIKTIF — tindakan latihan','result':'Hasil contoh','lesson':'Perbaikan contoh','nextReview':''}]
example['dayPlans']=[{'id':day,'date':day,'work':60,'rest':540,'contemplation':15,'quran':20,'fixed':120,'buffer':30}]
example['metricLogs']=[{'id':'demo-metric','goal':'demo-goal','indicator':'demo-indicator','date':day,'value':1,'note':'CONTOH FIKTIF — bukan angka hasil nyata','created':946684800000}]
example['routines']=[{'id':'demo-routine','title':'CONTOH FIKTIF — Latihan berkala','kind':'Belajar','goal':'demo-goal','days':[1],'start':day,'time':'','minutes':20,'target':'Latihan contoh','active':False}]
example['routineLogs']=[{'id':'demo-routine:2000-01-01','routine':'demo-routine','date':day,'status':'skip','note':'CONTOH FIKTIF — bukan catatan nyata'}]
example['timeEntries']=[{'id':'demo-time','title':'CONTOH FIKTIF — Waktu latihan','date':day,'minutes':15,'category':'Belajar','task':'demo-task','area':'demo-area','note':'CONTOH FIKTIF — bukan waktu nyata'}]
fields={
'inbox':('id title','body'), 'areas':('id title','body'),
'goals':('id title','body area due metric unit baseline target period source measurementVersion indicators smartReview'),
'projects':('id title','body area goal'),
'tasks':('id title status','project result priority estimate due repeat parent learning'),
'notes':('id title','body project folder tags'),
'events':('id title date time until','task category'),
'sessions':('id start end','task duration day energy distraction'),
'reviews':('id type date','good lesson next feeling reduce recovery'),
'quran':('id surah ayah status','teacher date note'),
'quranSessions':('id minutes date surah from to status','mode teacher note created'),
'plans':('id idea step','source minutes capacity area applied outcome why due metric unit baseline target period measurementSource process frequency steps estimates reviewDate'),
'preferences':('id','enabled short long rounds minutes newMinutes time results draft step'),
'quranUnits':('id juz status','teacher date note'),
'quranUnitSessions':('id sessionVersion juz units minutes date load status connection','teacher note created'),
'quranChecks':('id juz date','kind score0 score1 score2 score3 score4 decision assessor note nextReview'),
'learning':('id title exercise','source insight evidence area project nextReview academyLessonId'),
'practiceLogs':('id learning date action result','lesson nextReview'),
'dayPlans':('id date','work rest contemplation quran fixed buffer'),
'metricLogs':('id goal date value','indicator note created'),
'routines':('id title days start minutes','kind goal time target active'),
'routineLogs':('id routine date status','note'),
 'timeEntries':('id title date minutes','category task area note')}
deps={'goals':['areas'],'projects':['areas','goals'],'tasks':['projects'],'notes':['projects'],'events':['tasks'],'sessions':['tasks'],'plans':['areas','inbox'],'learning':['areas','projects'],'practiceLogs':['learning'],'metricLogs':['goals'],'routines':['goals'],'routineLogs':['routines'],'timeEntries':['tasks','areas']}
guide={'format':{'kind':'lifeos-import','version':'1.0','data':'Objek berisi satu atau beberapa array jenis data.'},
       'rules':['ID harus unik dalam setiap jenis data dan stabil untuk impor ulang.','Tanggal memakai YYYY-MM-DD; jam HH:MM.','Tidak ada data lama yang ditimpa. ID atau judul/kunci yang cocok akan dilewati.','Judul Goal dicocokkan dalam Area yang sama; judul Project dalam Area dan Goal yang sama; Task/Note dalam Project yang sama.','Relasi memakai ID, bukan nama. Sertakan dependensi yang belum ada di aplikasi.','Sesi Focus yang diimpor harus selesai; impor tidak memulai timer.','Angka baseline, target, jadwal, dan riwayat harus diisi berdasarkan data pengguna.'],
       'collections':{k:{'label':label,'required_for_template':fields[k][0].split(),'optional':fields[k][1].split(),'dependencies':deps.get(k,[]),'example':example[k][0]} for k,label in zip(KINDS,LABELS)},
       'learning_support':{'lessons':'Belajar LifeOS berisi materi dalam kode aplikasi. Catatan latihan tersimpan di preferences academy-learning-v1, results per ID materi.','smart_draft':'preferences academy-smart-draft-v1 memakai draft objek string dan step 0–4. draft.goalId mengacu ke Goal yang perlu ikut tersedia.','cards':'Kartu dari materi disimpan pada learning dengan academyLessonId; tanggal review tetap ditentukan pengguna.','smart_review':'goals.smartReview menyimpan status draft/review-ready, required=true, scope, capacity dan why. Status ini bukan sertifikasi SMART.'},
       'derived_features':{'Today':'Dihitung dari tugas, bigDate, agenda, rutinitas dan catatan hari. Pilih prioritas melalui bintang setelah impor.','Analytics':'Dihitung dari data aktivitas dan hasil; tidak memiliki baris impor tersendiri.','Cari Semua':'Mencari entitas yang diimpor; tidak membutuhkan file tersendiri.','Panduan':'Konten bantuan aplikasi; tidak memiliki data impor pengguna.'},
       'audio':{'route':'Settings → impor ZIP audio atau unggah melalui perekam','manifest':{'version':1,'kind':'lifeos-recordings','recordings':[]},'note':'File audio tidak dapat dimasukkan ke JSON ini. ZIP memuat recordings.json dan file audio yang sebenarnya. Untuk arsip berisi audio, gunakan format hasil ekspor aplikasi.'}}
write('catalog.json',{'guide':guide,'example':pack('CONTOH FIKTIF — Seluruh jenis data',example,'example')})
write('00-template-kosong-semua-fitur.json',pack('Template kosong seluruh jenis data',empty(),'blank'))
write('01-contoh-FIKTIF-semua-fitur.json',pack('CONTOH FIKTIF — Seluruh jenis data',example,'example'))
write('02-panduan-kolom.json',guide)
for k in KINDS:
    needed={k};changed=True
    while changed:
        changed=False
        for a in list(needed):
            for b in deps.get(a,[]):
                if b not in needed:needed.add(b);changed=True
    write('contoh-'+k+'.json',pack('CONTOH FIKTIF — '+guide['collections'][k]['label'],{a:example[a] for a in KINDS if a in needed},'example'))

print('Generated',len(KINDS),'generic collection templates.')
