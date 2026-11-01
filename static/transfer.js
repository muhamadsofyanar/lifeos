'use strict';
const IMPORT_LABELS={areas:'Area kehidupan',goals:'Goal / Tujuan',projects:'Projects',tasks:'Tasks',notes:'Notes',inbox:'Inbox',events:'Calendar',sessions:'Riwayat Focus',reviews:'Review',plans:'Idea Planner',preferences:'Pengaturan',quran:'Mutabaah ayat Juz 30',quranSessions:'Sesi Juz 30',quranUnits:'Mutabaah unit',quranUnitSessions:'Sesi unit',quranChecks:'Evaluasi & murajaah utuh',learning:'Belajar & Praktik',practiceLogs:'Riwayat praktik',dayPlans:'Anggaran hari',metricLogs:'Angka indikator Goal',routines:'Rutinitas',routineLogs:'Catatan rutinitas',timeEntries:'Catatan waktu manual'};
let importPackage=null,importSelected=[],importPreview=null,importCatalog=null;
function importPanel(){return `<div class="panel"><h2>Impor data & template</h2><p>Gabungkan data dari file JSON. Data yang sudah ada dipertahankan; pratinjau menunjukkan data baru dan duplikat sebelum disimpan.</p><div class="actions">${btn('Buka impor & template','import-open','','primary')}${btn('Download template kosong','import-blank')}</div><p><small>Mencakup Area, Goal, Project, Task, Note, rutinitas, jadwal, hafalan, pengaturan, dan seluruh catatan. Today dan Analytics dihitung dari data tersebut. File audio memakai impor ZIP audio yang terpisah.</small></p></div>`}
const beforeImportContent=content;
content=function(){const html=beforeImportContent();return page==='Settings'?importPanel()+html:html};
function resetImportPreview(){importPreview=null;const target=$('#import-preview');if(target)target.innerHTML='<p>Buat pratinjau setelah memilih data.</p>'}
function emptyImportTemplate(){return {kind:'lifeos-import',version:'1.0',purpose:'blank',name:'Template kosong LifeOS',data:Object.fromEntries(Object.keys(IMPORT_LABELS).map(k=>[k,[]]))}}
function importDialog(){
 if(!data)return;
 importPackage=null;importSelected=[];importPreview=null;
 showInfo('Impor gabung & template',`<p>1. Pilih file. 2. Periksa jenis data. 3. Buat pratinjau. 4. Simpan hasil penggabungan.</p><label>File impor JSON (maksimal 8 MB)<input id="merge-import-file" type="file" accept=".json,application/json"></label><div id="import-selection"></div><div id="import-preview"><p>Belum ada file dipilih.</p></div><hr><h3>Template seluruh fitur</h3><p>Template kosong siap diisi. Contoh fiktif menjelaskan bentuk kolom; jangan menganggapnya sebagai riwayat pribadi.</p><label>Pilih jenis data<select id="import-template-kind">${selectOptions([['all','Seluruh jenis data'],...Object.entries(IMPORT_LABELS)],'all')}</select></label><div class="actions">${btn('Template kosong','import-blank')}${btn('Contoh kolom fiktif','import-example')}${btn('Panduan kolom JSON','import-guide')}</div><hr><h3>Audio</h3><p>JSON tidak memuat file audio. Gunakan kontrol backup/impor ZIP audio di Settings atau unggah melalui perekam.</p>`);
}
function stageImport(packageData){
 if(!packageData||typeof packageData!=='object'||!packageData.data||typeof packageData.data!=='object'||Array.isArray(packageData.data))throw Error('File harus memiliki objek data.');
 const kinds=Object.keys(packageData.data);
 if(kinds.some(k=>!Object.hasOwn(IMPORT_LABELS,k)||!Array.isArray(packageData.data[k])))throw Error('Jenis data tidak dikenali atau isi bukan array.');
 importPackage=packageData;importSelected=kinds.filter(k=>packageData.data[k].length);importPreview=null;
 $('#import-selection').innerHTML=`<h3>${esc(packageData.name||'Isi file')}</h3>${packageData.purpose==='example'?'<p class="notice">Ini contoh FIKTIF. Mengimpornya akan menambahkan data contoh, bukan kejadian nyata.</p>':''}<p>Pilih data yang ingin ditambahkan. Data terkait harus ikut dipilih jika belum ada di aplikasi.</p>${kinds.filter(k=>packageData.data[k].length).map(k=>`<label><input type="checkbox" data-import-kind="${k}" checked> ${esc(IMPORT_LABELS[k])} · ${packageData.data[k].length}</label>`).join('')||'<p>Template kosong belum memiliki baris. Isi file dahulu sebelum diimpor.</p>'}<div class="actions">${btn('Buat pratinjau','import-preview','','primary')}</div>`;
 resetImportPreview();
}
function importReportHtml(report){
 const rows=Object.entries(report.collections).map(([k,r])=>`<tr><td>${esc(IMPORT_LABELS[k]||k)}</td><td>${r.added}</td><td>${r.skipped}</td></tr>`).join('');
 return `<h3>Pratinjau penggabungan</h3><p><b>${report.added} data baru</b> · ${report.skipped} data dilewati. Isian lama tidak ditimpa.</p><div class="table-wrap"><table><thead><tr><th>Jenis</th><th>Tambah</th><th>Lewati</th></tr></thead><tbody>${rows}</tbody></table></div><details><summary>Rincian data (${report.items.length})</summary>${report.items.slice(0,100).map(item=>`<p>${item.action==='add'?'Tambah':'Lewati'} · ${esc(IMPORT_LABELS[item.collection]||item.collection)} · ${esc(item.title)}<br><small>${esc(item.reason)}</small></p>`).join('')}${report.items.length>100?'<p>Menampilkan 100 rincian pertama; hitungan tabel mencakup semua data.</p>':''}</details>${report.added?btn(report.example?'Simpan contoh FIKTIF':'Simpan hasil impor','import-apply','','primary'):'<p>Tidak ada data baru untuk disimpan.</p>'}`;
}
async function transferAction(a){
 if(a==='import-open'){importDialog();return true}
 if(['import-blank','import-example','import-guide'].includes(a)){
  const key=$('#import-template-kind')?.value||'all';
  if(a==='import-blank'){
   const template=emptyImportTemplate();if(key!=='all')template.data={[key]:[]};
   download('lifeos-template-'+key+'.json',JSON.stringify(template,null,2),'application/json');
  }else{
   if(!importCatalog)importCatalog=await api('import/templates');
   if(a==='import-guide')download('lifeos-panduan-kolom.json',JSON.stringify(importCatalog.guide,null,2),'application/json');
   else{
    const template=structuredClone(importCatalog.example);
    if(key!=='all'){
     // Include dependencies so a per-feature example can pass reference checks.
     const needed=new Set([key]);let changed=true;
     while(changed){changed=false;for(const k of [...needed])for(const dependency of importCatalog.guide.collections[k].dependencies||[])if(!needed.has(dependency)){needed.add(dependency);changed=true}}
     template.data=Object.fromEntries([...needed].map(k=>[k,template.data[k]]));
    }
    download('lifeos-contoh-fiktif-'+key+'.json',JSON.stringify(template,null,2),'application/json');
   }
  }return true;
 }
 if(a==='import-preview'){
  if(!importPackage||!importSelected.length)throw Error('Pilih file dan minimal satu jenis data.');
  if(busy)throw Error('Tunggu penyimpanan yang sedang berjalan.');
  importPreview=null;
  const result=await api('import/preview',{revision,package:importPackage,selected:importSelected});
  importPreview=result;
  $('#import-preview').innerHTML=importReportHtml(result.report);
  return true;
 }
 if(a==='import-apply'){
  if(!importPreview)throw Error('Buat pratinjau terlebih dahulu.');
  if(busy)throw Error('Tunggu penyimpanan yang sedang berjalan.');
  if(!confirm(`Tambahkan ${importPreview.report.added} data${importPreview.report.example?' CONTOH FIKTIF':''}? Data yang sudah ada tetap dipertahankan.`))return true;
  busy=true;
  try{
   const result=await api('import/apply',{revision:importPreview.revision,package:importPackage,selected:importSelected});
   $('#modal').close();importPackage=null;importPreview=null;
   await load();toast(`${result.report.added} data ditambahkan; ${result.report.skipped} dilewati.`);
  }catch(error){resetImportPreview();throw error}finally{busy=false}
  return true;
 }
 return false;
}
const beforeTransferAction=consolidatedAction;
consolidatedAction=async function(a,id,event){if(await transferAction(a))return true;return beforeTransferAction(a,id,event)};
document.addEventListener('change',async event=>{
 try{
  if(event.target.id==='merge-import-file'){
   const file=event.target.files[0];if(!file)return;
   if(file.size>8000000)throw Error('File maksimal 8 MB.');
   importPackage=null;importPreview=null;importSelected=[];
   $('#import-selection').innerHTML='';resetImportPreview();
   stageImport(JSON.parse(await file.text()));
  }
  if(event.target.dataset?.importKind){
   importSelected=[...$('#modal').querySelectorAll('[data-import-kind]:checked')].map(el=>el.dataset.importKind);
   resetImportPreview();
  }
 }catch(error){toast(error.message)}
});
