'use strict';
function practiceBounds(j,kind,target){
 if(kind==='lines'){const [a,b]=pageRange(j);if(j===30||target<a||target>b)throw Error('Pilih halaman sesuai juz.');return [1,15]}
 const seg=mCoverage(j,{kind:'juz',value:j}).segments.find(s=>s[0]===target);if(!seg)throw Error('Surah di luar juz pilihan.');return [seg[1],seg[2]];
}
function practiceTargets(j,kind){if(kind==='lines'){const [a,b]=pageRange(j);return Array.from({length:b-a+1},(_,i)=>[a+i,'Halaman '+(a+i)])}return mCoverage(j,{kind:'juz',value:j}).segments.map(([s])=>[s,s+'. '+mMeta.chapters[s-1].name])}
function practiceRange(j,scope){
 const {kind,value,from,to}=scope;if(!['verses','lines'].includes(kind)||![value,from,to].every(Number.isInteger))throw Error('Rentang tidak valid.');
 const [a,b]=practiceBounds(j,kind,value);if(from<a||to<from||to>b)throw Error('Rentang di luar batas ayat/baris yang dipilih.');
 if(kind==='verses')return {scope:{kind,value,from,to},label:mCoverage(j,scope).label,verseIds:j===30?Array.from({length:to-from+1},(_,i)=>value+':'+(from+i)):[],unitIds:[]};
 return {scope:{kind,value,from,to},label:'Halaman '+value+' · baris '+from+'–'+to,verseIds:[],unitIds:juzUnits(j).filter(u=>u.page===value&&from<=u.start&&u.end<=to).map(u=>u.id)};
}
function practiceRangeFields(j,scope){const {kind,value,from,to}=scope,[a,b]=practiceBounds(j,kind,value);return `<div data-practice-range data-juz="${j}">${field('Pilih jenis rentang','rangeKind',kind,'select',selectOptions([['verses','Rentang ayat'],...(j===30?[]:[['lines','Rentang baris mushaf']])],kind))}${field(kind==='verses'?'Nomor dan nama surah':'Halaman mushaf','rangeTarget',value,'select',selectOptions(practiceTargets(j,kind),value))}${field(kind==='verses'?'Dari ayat':'Dari baris','rangeFrom',from,'select',selectOptions(Array.from({length:b-a+1},(_,i)=>[a+i,a+i]),from))}${field(kind==='verses'?'Sampai ayat':'Sampai baris','rangeTo',to,'select',selectOptions(Array.from({length:b-from+1},(_,i)=>[from+i,from+i]),to))}<p class="range-hint notice" data-range-hint></p></div>`}
function bindPracticeRange(form){
 const group=form?.querySelector?.('[data-practice-range]');if(!group||form.practiceRangeController)return;
 const j=Number(group.dataset.juz),get=n=>form.querySelector('[name='+n+']'),kind=get('rangeKind'),target=get('rangeTarget'),from=get('rangeFrom'),to=get('rangeTo'),hint=form.querySelector('[data-range-hint]');
 const update=(resetTarget=false,resetBounds=false)=>{
  const choices=practiceTargets(j,kind.value),candidate=Number(target.value),value=!resetTarget&&choices.some(([v])=>v===candidate)?candidate:choices[0][0];
  target.innerHTML=selectOptions(choices,value);target.value=String(value);
  target.parentElement.firstChild.textContent=kind.value==='verses'?'Nomor dan nama surah':'Halaman mushaf';
  from.parentElement.firstChild.textContent=kind.value==='verses'?'Dari ayat':'Dari baris';to.parentElement.firstChild.textContent=kind.value==='verses'?'Sampai ayat':'Sampai baris';
  const [a,b]=practiceBounds(j,kind.value,value),x=Number(from.value),y=Number(to.value),start=!resetBounds&&Number.isInteger(x)&&x>=a&&x<=b?x:a,end=!resetBounds&&Number.isInteger(y)&&y>=start&&y<=b?y:start;
  from.innerHTML=selectOptions(Array.from({length:b-a+1},(_,i)=>[a+i,a+i]),start);from.value=String(start);
  to.innerHTML=selectOptions(Array.from({length:b-start+1},(_,i)=>[start+i,start+i]),end);to.value=String(end);
  const r=practiceRange(j,{kind:kind.value,value,from:start,to:end});
  hint.textContent=r.label+'. '+(kind.value==='lines'?r.unitIds.length+' unit tahap tercakup utuh. Potongan unit di tepi tidak diubah. Nomor baris mengikuti mushaf 15 baris, bukan baris teks di layar.':j===30?r.verseIds.length+' ayat dapat diperbarui jika pilihan mutabaah dicentang.':'Rentang ayat dicatat sebagai sesi; mutabaah unit baris tidak diubah karena batas baris dan ayat berbeda.');
 };
 const refresh=(resetTarget=false,resetBounds=false)=>{update(resetTarget,resetBounds);if(typeof Event==='function'&&form.dispatchEvent)form.dispatchEvent(new Event('input',{bubbles:true}))};
 kind.addEventListener('change',()=>refresh(true,true));target.addEventListener('change',()=>refresh(false,true));from.addEventListener('change',()=>refresh());to.addEventListener('change',()=>refresh());
 form.practiceRangeController={setRange:v=>{kind.value=v.rangeKind||kind.value;update(true,true);target.value=String(v.rangeTarget);update(false,true);from.value=String(v.rangeFrom);update();to.value=String(v.rangeTo);update()},refresh:()=>update()};update();
}
const beforePracticeDraft=prepareVerseRangeDraft;
prepareVerseRangeDraft=function(form,values){beforePracticeDraft(form,values);if(form?.practiceRangeController&&values?.rangeKind)form.practiceRangeController.setRange(values)};
function practiceDefault(j,initial={}){
 if(initial.kind)return initial;
 if(j===30){const n=qnext();return {kind:'verses',value:n?.surah||101,from:n?.ayah||1,to:n?.ayah||1}}
 const u=juzUnits(j).find(u=>!learned(hstate(u)))||juzUnits(j)[0];return {kind:'lines',value:u.page,from:u.start,to:u.end};
}
function practiceForm(j,initial={},id=''){
 const old=data.quranChecks.find(l=>l.coverageVersion===2&&l.id===id),scope=old?.scope||practiceDefault(j,initial),range=practiceRange(j,scope),current=scope.kind==='verses'&&j===30?verseState(scope.value,scope.from):range.unitIds.length===1?data.quranUnits.find(u=>u.id===range.unitIds[0]):{};
 draftScope='practice:'+j+':'+scope.kind+':'+scope.value+':'+scope.from+':'+(id||'new');
 showForm((old?'Koreksi':'Catat')+' rentang latihan · Juz '+j,
 practiceRangeFields(j,scope)+field('Tanggal','date',old?.date||today(),'date')+field('Durasi aktual (1–240 menit)','minutes',old?.minutes||qsettings().minutes,'number')+field('Cara latihan','readingMode',old?.readingMode||'hafalan','select',selectOptions([['hafalan','Dari hafalan'],['melihat','Membaca dengan melihat']],old?.readingMode||'hafalan'))+field('Penilaian rentang yang dilatih','status',old?.status||current?.status||'practiced','select',selectOptions(Object.entries(QSTATUS),old?.status||current?.status||'practiced'))+field('Nama penyimak (wajib jika disimak guru)','assessor',old?.assessor||current?.teacher||'')+field('Catatan kesalahan / sambungan','note',old?.note||current?.note||'','textarea')+`<label><input name="applyProgress" type="checkbox" ${old?'':'checked'}> Terapkan penilaian ke ayat / unit yang tercakup utuh.</label><p class="muted">Simpan mencatat satu sesi beserta durasinya. Koreksi rentang tidak menghapus status bagian lama. Rentang ayat pada Juz 1–29 tidak otomatis mengubah unit baris.</p>`+(j!==30?btn('Gunakan sesi tahap / S2','r-stage'):'')+field('Murajaah berikutnya (opsional)','nextReview',old?.nextReview||'','date'),v=>{
  const selected={kind:v.rangeKind,value:Number(v.rangeTarget),from:Number(v.rangeFrom),to:Number(v.rangeTo)},range=practiceRange(j,selected),minutes=Number(v.minutes);
  if(!v.date||!Number.isFinite(minutes)||minutes<1||minutes>240)throw Error('Isi tanggal dan durasi 1–240 menit.');
  if(!Object.hasOwn(QSTATUS,v.status))throw Error('Pilih penilaian.');if(v.applyProgress&&v.readingMode==='melihat'&&learned({status:v.status}))throw Error('Membaca dengan melihat belum membuktikan hafalan lancar. Pilih dilatih/penguatan atau lepaskan penerapan ke mutabaah.');if(v.status==='teacher'&&!v.assessor.trim())throw Error('Isi nama penyimak.');
  return change(()=>{
   const log={id:old?.id||uid(),coverageVersion:2,juz:j,scope:range.scope,date:v.date,minutes,readingMode:v.readingMode,status:v.status,assessor:v.status==='teacher'?v.assessor:'',note:v.note,nextReview:v.nextReview||'',kind:'Latihan rentang',decision:'Catatan rentang',created:old?.created||Date.now()},index=data.quranChecks.findIndex(l=>l.id===log.id);
   if(index<0)data.quranChecks.push(log);else data.quranChecks[index]=log;
   if(v.applyProgress){
    for(const key of range.verseIds){const [s,a]=key.split(':').map(Number);upsertVerse(s,a,v.status,v.note,v.assessor,v.date)}
    for(const key of range.unitIds){const value={id:key,juz:j,status:v.status,teacher:v.status==='teacher'?v.assessor:'',note:v.note,date:v.date},i=data.quranUnits.findIndex(u=>u.id===key);if(i<0)data.quranUnits.push(value);else data.quranUnits[i]=value}
   }
  });
 });
}
function practicePanel(){const logs=data.quranChecks.filter(l=>l.coverageVersion===2&&l.juz===hifzJuz).slice().sort((a,b)=>b.date.localeCompare(a.date)||(b.created||0)-(a.created||0));return `<section class="panel range-launch"><span class="pill">LANGKAH HARI INI</span><div class="section-title"><div><h2>Catat bagian yang benar-benar dilatih</h2><p>Pilih rentang ayat${hifzJuz!==30?' atau baris':''}, lalu nilai hasilnya.</p></div>${btn('+ Catat rentang','r-new','','primary')}</div><details><summary>Riwayat rentang Juz ${hifzJuz} (${logs.length})</summary>${logs.slice(0,20).map(l=>`<article class="audio-item"><b>${esc(l.date)} · ${esc(mMeta?practiceRange(l.juz,l.scope).label:'Rentang latihan')}</b><p>${l.minutes} menit · ${esc(QSTATUS[l.status]||l.status)} · ${l.readingMode==='melihat'?'Dengan melihat':'Dari hafalan'}</p>${l.note?'<p>'+esc(l.note)+'</p>':''}<div class="actions">${btn('Koreksi rentang','r-edit',l.id)}${l.scope.kind==='verses'?btn('Baca / rekam rentang','r-read',l.id):''}${btn('Hapus catatan','r-delete',l.id)}</div></article>`).join('')||'<p>Belum ada catatan rentang.</p>'}${logs.length>20?'<p>Menampilkan 20 terbaru; seluruh catatan tetap masuk backup.</p>':''}</details></section>`}
const beforePracticeContent=quranContent;
quranContent=function(){return practicePanel()+beforePracticeContent()};
const beforePracticeAction=consolidatedAction;
consolidatedAction=async function(a,id,event){
 if(['r-new','q-verse','h-unit','q-log','h-log'].includes(a)){
  await ensureMurajaahMeta();let scope={};
  if(a==='q-verse'){const [s,v]=id.split(':').map(Number);scope={kind:'verses',value:s,from:v,to:v}}
  if(a==='h-unit'){const u=juzUnits(hifzJuz).find(u=>u.id===id);if(!u)throw Error('Unit tidak ditemukan.');scope={kind:'lines',value:u.page,from:u.start,to:u.end}}
  practiceForm(a==='q-verse'||a==='q-log'?30:hifzJuz,scope);return true;
 }
 if(a==='r-stage'){if(confirm('Buka formulir sesi tahap/S2? Isian rentang yang belum disimpan tetap sebagai draft perangkat.'))hLog();return true}
 if(a==='r-edit'||a==='r-read'){await ensureMurajaahMeta();const l=data.quranChecks.find(l=>l.id===id&&l.coverageVersion===2);if(!l)throw Error('Catatan tidak ditemukan.');if(a==='r-read')await murajaahDialog(l.juz,l.scope);else practiceForm(l.juz,l.scope,l.id);return true}
 if(a==='r-delete'){if(confirm('Hapus catatan rentang ini? Status mutabaah tetap tersimpan.'))await change(()=>{data.quranChecks=data.quranChecks.filter(l=>l.id!==id)});return true}
 return beforePracticeAction(a,id,event);
};
