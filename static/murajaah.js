'use strict';
/* Whole-scope review is separate from the staged new-memorization units. */
let mMeta=null,mVerses=null,mSelection=null,mLoading=null,mOpening=false;
function mOrdinal(pair){return mMeta.chapters[pair[0]-1].start+pair[1]-1}
function mCoverage(juz,scope){
 if(!mMeta)throw Error('Metadata bacaan belum dimuat.');
 if(!Number.isInteger(juz)||juz<1||juz>30||!scope||!Number.isInteger(scope.value))throw Error('Pilih juz dan cakupan.');
 const {kind,value}=scope,chapters=mMeta.chapters,ja=mOrdinal(mMeta.juzs[juz-1]),jb=juz<30?mOrdinal(mMeta.juzs[juz]):6236;
 let start,end,label;
 if(kind==='juz'){if(value!==juz)throw Error('Juz cakupan tidak sesuai.');start=ja;end=jb;label='Juz '+juz+' utuh'}
 else if(kind==='page'){const p=mMeta.pages[value];if(!p)throw Error('Halaman harus 1–604.');start=mOrdinal([p[0].surah,p[0].from]);end=mOrdinal([p.at(-1).surah,p.at(-1).to])+1;label='Halaman '+value+' utuh'}
 else if(kind==='surah'){const s=chapters[value-1];if(!s)throw Error('Surah tidak valid.');start=s.start;end=start+s.count;label='Surah '+s.name+' utuh'}
 else if(kind==='rubu'){
  if(value<1||value>8)throw Error('Rubu harus 1–8.');
  if(juz===30){const [a,b]=mMeta.bookRubu30[value-1];start=chapters[a-1].start;end=chapters[b-1].start+chapters[b-1].count;label='Rubu '+value+' buku utuh · Juz 30'}
  else{const i=(juz-1)*8+value-1;start=mOrdinal(mMeta.rubs[i]);end=i<239?mOrdinal(mMeta.rubs[i+1]):6236;label='Rubu '+value+' standar utuh · Juz '+juz}
 }else throw Error('Jenis cakupan tidak dikenal.');
 if(start>=jb||end<=ja)throw Error('Cakupan berada di luar juz pilihan.');
 const segments=chapters.flatMap(s=>{const a=Math.max(start,s.start),b=Math.min(end,s.start+s.count);return a<b?[[s.number,a-s.start+1,b-s.start]]:[]});
 return {scope:{kind,value},label,start,end,segments,count:end-start,crossJuz:start<ja||end>jb};
}
function mOptions(j,kind){
 if(kind==='juz')return [[j,'Juz '+j+' utuh']];
 if(kind==='rubu')return Array.from({length:8},(_,i)=>[i+1,mCoverage(j,{kind,value:i+1}).label]);
 const values=kind==='page'?Object.keys(mMeta.pages).map(Number):mMeta.chapters.map(s=>s.number);
 return values.flatMap(value=>{try{return [[value,mCoverage(j,{kind,value}).label]]}catch{return []}});
}
function mSelected(){if(!mSelection||mSelection.juz!==hifzJuz)mSelection={juz:hifzJuz,kind:'page',value:mOptions(hifzJuz,'page')[0][0]};return mSelection}
function mSpanLabel(c){return c.segments.map(([s,a,b])=>mMeta.chapters[s-1].name+' '+a+'–'+b).join(' · ')}
function murajaahPanel(){
 if(!mMeta)return `<section id="murajaah-panel" class="panel"><h2>Murajaah utuh: baca dan rekam</h2><p>Pilih halaman, surah, rubu, atau juz penuh.</p>${btn('Muat pilihan murajaah','m-load','','primary')}</section>`;
 const sel=mSelected(),c=mCoverage(sel.juz,sel),logs=data.quranChecks.filter(l=>l.coverageVersion===1&&l.juz===sel.juz).slice().sort((a,b)=>b.date.localeCompare(a.date)||(b.created||0)-(a.created||0));
 return `<section id="murajaah-panel" class="panel murajaah-panel"><span class="pill">MURAJAAH UTUH</span><h2>Baca dan rekam bagian yang ingin diulang</h2><p>Pilihan ini memakai bagian penuh, terpisah dari potongan latihan hafalan baru.</p><div class="notes-filters"><label>Cakupan<select id="m-kind">${selectOptions([['page','Satu halaman penuh'],['surah','Satu surah penuh'],['rubu',sel.juz===30?'Satu rubu buku penuh':'Satu rubu standar penuh'],['juz','Satu juz penuh']],sel.kind)}</select></label><label>Pilihan bagian<select id="m-value">${selectOptions(mOptions(sel.juz,sel.kind),sel.value)}</select></label></div><p><b>${esc(c.label)}</b> · ${c.count} ayat<br><small>${esc(mSpanLabel(c))}</small></p>${c.crossJuz?'<p class="notice">Cakupan utuh ini melintasi batas juz pilihan. Seluruh bagian tetap ditampilkan dan direkam, termasuk ayat di juz lain.</p>':''}<p><small>${sel.juz===30?'Rubu mengikuti delapan kelompok buku: rubu 1 Al-Qari’ah–An-Nas.':'Rubu mengikuti 1/4 hizb standar (delapan bagian per juz), bukan kelompok rubu buku Juz 30.'}</small></p><div class="actions">${btn('Baca / rekam bagian penuh','m-open','','primary')}${btn('Catat murajaah','m-log')}</div><details class="murajaah-history"><summary>Riwayat murajaah utuh (${logs.length})</summary>${logs.slice(0,20).map(l=>{let title;try{title=mCoverage(l.juz,l.scope).label}catch{title='Cakupan perlu diperiksa'}return `<article class="audio-item"><b>${esc(l.date)} · ${esc(title)}</b><p>${l.minutes} menit · ${l.readingMode==='melihat'?'Membaca dengan melihat':'Mengulang dari hafalan'} · ${esc(QSTATUS[l.status]||l.status)}</p>${l.note?'<p>'+esc(l.note)+'</p>':''}<div class="actions">${btn('Baca / rekam lagi','m-from-log',l.id)}${btn('Koreksi','m-edit',l.id)}${btn('Hapus catatan','m-delete',l.id)}</div></article>`}).join('')||'<p>Belum ada catatan murajaah utuh.</p>'}${logs.length>20?'<p>Menampilkan 20 terbaru. Seluruh catatan tetap masuk backup JSON.</p>':''}</details></section>`;
}
async function ensureMurajaahText(){
 if(mVerses)return;
 const r=await fetch('/quran-uthmani.txt');if(!r.ok)throw Error('Teks bacaan gagal dimuat. Coba lagi.');
 const raw=await r.text(),verses=raw.split(/\r?\n/).filter(l=>l&&!l.startsWith('#'));
 if(verses.length!==6236||!raw.includes('Tanzil Quran Text (Uthmani, Version 1.1)'))throw Error('Berkas bacaan tidak lengkap. Periksa paket deployment.');
 if(globalThis.crypto?.subtle&&globalThis.TextEncoder){const bytes=new TextEncoder().encode(raw),digest=await crypto.subtle.digest('SHA-256',bytes),hash=Array.from(new Uint8Array(digest),b=>b.toString(16).padStart(2,'0')).join('');if(hash!==mMeta.textSha256)throw Error('Integritas teks bacaan gagal diperiksa. Unggah ulang berkas sumber.');}
 mVerses=verses;
}
async function ensureMurajaahMeta(){
 if(mMeta)return;
 if(!mLoading)mLoading=(async()=>{const r=await fetch('/quran-coverage.json');if(!r.ok)throw Error('Metadata murajaah gagal dimuat.');const m=await r.json();if(m.chapters?.length!==114||m.juzs?.length!==30||m.rubs?.length!==240)throw Error('Metadata murajaah tidak lengkap.');mMeta=m})().finally(()=>{mLoading=null});
 return mLoading;
}
function murajaahReading(c){
 if(!mVerses)throw Error('Teks belum dimuat.');
 return `<section class="murajaah-reading" aria-label="Bacaan Al-Qur’an"><p class="notice">Teks lengkap sesuai cakupan halaman Mushaf Madinah 604 halaman. Susunan baris menyesuaikan layar; bukan gambar halaman mushaf.</p><label>Ukuran huruf<select id="m-font"><option value="28">Sedang</option><option value="34" selected>Besar</option><option value="42">Sangat besar</option></select></label><div id="m-arabic" class="quran-arabic quran-size-34" dir="rtl" lang="ar">${c.segments.map(([s,a,b])=>{const chapter=mMeta.chapters[s-1];return `<section><h3>${esc(chapter.arabic)}</h3><p>${Array.from({length:b-a+1},(_,i)=>{const aya=a+i;return `<span class="quran-ayah" data-verse="${s}:${aya}">${esc(mVerses[chapter.start+aya-1])}<span class="ayah-number" aria-label="آية ${aya}">﴿${String(aya).replace(/\d/g,d=>'٠١٢٣٤٥٦٧٨٩'[Number(d)])}﴾</span></span>`}).join(' ')}</p></section>`}).join('')}</div><p class="quran-attribution">Tanzil Quran Text (Uthmani, Version 1.1) · © 2007–2026 Tanzil Project · CC BY 3.0. <a href="https://tanzil.net" target="_blank" rel="noopener noreferrer">Tanzil Project</a> · <a href="/quran-uthmani.txt" target="_blank" rel="noopener noreferrer">Teks sumber dan lisensi</a>. Teks ditampilkan tanpa penyuntingan.</p></section>`;
}
function mSessionOptions(j,c,selected=''){
 return selectOptions([['','Tanpa hubungan ke catatan murajaah'],...data.quranChecks.filter(l=>{if(l.coverageVersion!==1||l.juz!==j)return false;const p=mCoverage(j,l.scope);return c.start>=p.start&&c.end<=p.end}).map(l=>[l.id,l.date+' · '+mCoverage(j,l.scope).label+' · '+l.minutes+' menit · #'+l.id.slice(-8)])],selected);
}
async function murajaahDialog(j,scope,logId=''){
 if(mOpening){toast('Bacaan sedang dimuat.');return}
 mOpening=true;try{
 const requestedScope={kind:scope.kind,value:scope.value},originalGeneration=rec.generation,originalBlob=rec.blob;
 if(recordingActive()||rec.saving)throw Error('Hentikan rekaman dan selesaikan penyimpanan dahulu.');
 if(rec.blob&&!confirm('Ganti audio sementara yang belum disimpan?'))return;
 await ensureMurajaahMeta();await ensureMurajaahText();
 if(recordingActive()||rec.saving||rec.generation!==originalGeneration||rec.blob!==originalBlob)throw Error('Keadaan perekam berubah saat memuat bacaan. Coba lagi setelah selesai.');
 const c=mCoverage(j,requestedScope);releaseRecording(true);rec.dialog=true;
 $('#modal').innerHTML=`<div class="section-title"><h2>${esc(c.label)}</h2>${btn('✕','close')}</div><form id="recording-form" class="murajaah-recorder" data-juz="${j}" data-coverage="1" data-scope="${esc(JSON.stringify(c.scope))}" data-max-minutes="60">${field('Judul rekaman','title','Murajaah '+c.label)}${field('Tanggal rekaman','date',today(),'date')}${field('Hubungkan ke catatan murajaah (opsional)','reviewSession',logId,'select',mSessionOptions(j,c,logId))}<p><small>Hubungan ini tidak membuat atau mengubah catatan murajaah. Catat sesi secara terpisah melalui tombol Catat murajaah. Simpan audio tidak mengubah kelancaran mutabaah.</small></p><label>Batas waktu rekaman<select id="m-record-limit"><option value="30">30 menit</option><option value="60" selected>60 menit</option><option value="120">120 menit</option></select></label><div class="rec-controls murajaah-controls">${btn('● Mulai rekam','audio-start','','primary')}${btn('■ Hentikan','audio-stop')}${btn('Simpan audio','audio-save','','primary')}<span id="rec-time" role="status">00:00</span></div><p id="rec-message" role="status">Baca langsung di bawah. Mikrofon aktif setelah Mulai rekam; batas ukuran audio 50 MB. Jangan tutup atau kunci perangkat selama merekam.</p><label>Atau unggah audio dari perangkat (maks. 50 MB)<input id="audio-file" type="file" accept="audio/*,.m4a,.webm,.ogg,.mp3,.wav"></label><div id="audio-preview"></div>${field('Catatan kesalahan / sambungan','note','','textarea')}<div class="actions">${btn('Tutup','close')}</div>${murajaahReading(c)}</form>`;
 if(!$('#modal').open)$('#modal').showModal();
 $('#recording-form').onsubmit=e=>e.preventDefault();updateRecorderControls();
 }finally{mOpening=false}
}
function murajaahLogForm(j,scope,id=''){
 draftScope='murajaah:'+j+':'+scope.kind+':'+scope.value+':'+id;
 const old=data.quranChecks.find(l=>l.id===id&&l.coverageVersion===1)||{},c=mCoverage(j,scope);
 showForm('Catat murajaah: '+esc(c.label),'<p>'+c.count+' ayat · '+esc(mSpanLabel(c))+'</p><p>Catat bagian penuh hanya jika seluruh cakupan benar-benar dibaca/diulang. Jika belum selesai, tutup dan pilih cakupan lebih kecil. Catatan ini tidak menandai ayat/unit otomatis lancar.</p>'+field('Tanggal','date',old.date||today(),'date')+field('Durasi aktual (1–240 menit)','minutes',old.minutes||20,'number')+field('Cara murajaah','readingMode',old.readingMode||'hafalan','select',selectOptions([['hafalan','Mengulang dari hafalan'],['melihat','Membaca dengan melihat mushaf']],old.readingMode||'hafalan'))+field('Penilaian sesi','status',old.status||'practiced','select',selectOptions(Object.entries(QSTATUS),old.status||'practiced'))+field('Penyimak (wajib jika disimak guru)','assessor',old.assessor||'')+field('Bagian lemah / sambungan','note',old.note||'','textarea')+field('Murajaah berikutnya (opsional)','nextReview',old.nextReview||'','date'),async v=>{
  const minutes=Number(v.minutes);if(!v.date||!Number.isFinite(minutes)||minutes<1||minutes>240)throw Error('Isi tanggal dan durasi 1–240 menit.');if(v.status==='teacher'&&!v.assessor.trim())throw Error('Isi nama penyimak.');
  return change(()=>{const log={...old,...v,id:old.id||uid(),juz:j,scope:c.scope,coverageVersion:1,minutes,kind:'Murajaah utuh',decision:'Catatan sesi murajaah',created:old.created||Date.now()},i=data.quranChecks.findIndex(l=>l.id===log.id);if(i<0)data.quranChecks.push(log);else data.quranChecks[i]=log});
 });
}
const beforeMurajaahContent=quranContent;
quranContent=function(){return murajaahPanel()+beforeMurajaahContent()};
const beforeMurajaahMetadata=recordingMetadata;
recordingMetadata=function(){
 const form=$('#recording-form');if(form.dataset.coverage!=='1')return beforeMurajaahMetadata();
 const v=Object.fromEntries(new FormData(form)),j=Number(form.dataset.juz),c=mCoverage(j,JSON.parse(form.dataset.scope));
 if(!v.title?.trim()||!v.date)throw Error('Isi judul dan tanggal.');
 if(v.reviewSession){const log=data.quranChecks.find(l=>l.coverageVersion===1&&l.id===v.reviewSession&&l.juz===j);if(!log)throw Error('Catatan murajaah tidak ditemukan.');const p=mCoverage(j,log.scope);if(c.start<p.start||c.end>p.end)throw Error('Cakupan tidak sesuai catatan murajaah.');}
 return {title:v.title,date:v.date,juz:j,target:c.label,targetVersion:2,scope:c.scope,reviewSession:v.reviewSession||'',session:'',note:v.note||'',duration:rec.seconds};
};
const beforeMurajaahSessionText=recordingSessionText;
recordingSessionText=function(r){if(r.targetVersion!==2)return beforeMurajaahSessionText(r);if(!r.reviewSession)return 'Murajaah utuh · tanpa hubungan catatan sesi.';const l=data.quranChecks.find(l=>l.id===r.reviewSession&&l.coverageVersion===1&&l.juz===r.juz);return l?'Catatan murajaah: '+l.date+' · '+(mMeta?mCoverage(l.juz,l.scope).label:r.target)+' · '+l.minutes+' menit':'Catatan murajaah terkait tidak tersedia; audio tetap tersimpan.'};
const beforeMurajaahAction=consolidatedAction;
consolidatedAction=async function(a,id,event){
 if(a==='m-load'){await ensureMurajaahMeta();render();return true}
 if(a==='m-open'||a==='m-log'){await ensureMurajaahMeta();const s=mSelected();if(a==='m-open')await murajaahDialog(s.juz,s);else murajaahLogForm(s.juz,s);return true}
 if(a==='m-from-log'||a==='m-edit'){const l=data.quranChecks.find(l=>l.id===id&&l.coverageVersion===1);if(!l)throw Error('Catatan murajaah tidak ditemukan.');if(a==='m-from-log')await murajaahDialog(l.juz,l.scope,l.id);else murajaahLogForm(l.juz,l.scope,l.id);return true}
 if(a==='m-read-audio'){const r=recordings.find(r=>r.id===id&&r.targetVersion===2);if(!r)throw Error('Rekaman tidak ditemukan.');await murajaahDialog(r.juz,r.scope);return true}
 if(a==='m-delete'){if(confirm('Hapus catatan murajaah ini? Audio dan mutabaah tetap tersimpan.'))await change(()=>{data.quranChecks=data.quranChecks.filter(l=>l.id!==id)});return true}
 return beforeMurajaahAction(a,id,event);
};
document.addEventListener('change',e=>{
 try{
  if(e.target.id==='m-kind'||e.target.id==='m-value'){const s=mSelected();if(e.target.id==='m-kind'){s.kind=e.target.value;s.value=mOptions(s.juz,s.kind)[0][0]}else s.value=Number(e.target.value);$('#murajaah-panel').outerHTML=murajaahPanel()}
  if(e.target.id==='m-font'){$('#m-arabic').classList.remove('quran-size-28','quran-size-34','quran-size-42');$('#m-arabic').classList.add('quran-size-'+e.target.value)}
  if(e.target.id==='m-record-limit'){if(recordingActive()){e.target.value=$('#recording-form').dataset.maxMinutes;toast('Batas rekaman dapat diubah sebelum mulai.')}else $('#recording-form').dataset.maxMinutes=e.target.value}
 }catch(error){toast(error.message)}
});
document.addEventListener('DOMContentLoaded',()=>{ensureMurajaahMeta().then(()=>{if(data&&page==='Sullamul Hifz')render()}).catch(()=>{})});
