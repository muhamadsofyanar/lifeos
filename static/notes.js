/* Folder/tag browsing uses existing note fields; no migration or duplicate records. */
let notesFolder='', notesTag='';
const noteFolder=n=>(n.folder||'').trim();
function noteTags(n){return [...new Set((n.tags||'').split(',').map(t=>t.trim()).filter(Boolean))]}
function notesVisible(){return data.notes.filter(n=>matching(n)&&(!notesFolder||(notesFolder===':none:'?!noteFolder(n):noteFolder(n)===notesFolder))&&(!notesTag||noteTags(n).includes(notesTag)))}
function notesChoices(){return {folders:[...new Set(data.notes.map(noteFolder).filter(Boolean))].sort((a,b)=>a.localeCompare(b,'id')),tags:[...new Set(data.notes.flatMap(noteTags))].sort((a,b)=>a.localeCompare(b,'id'))}}
function notePreview(n){const text=(n.body||'').replace(/^#{1,6}\s+/gm,'').replace(/\[\[([^\]]+)\]\]/g,'$1').trim();return text.length>260?text.slice(0,260)+'…':text||'Belum ada isi catatan.'}
function notesContent(){
 const {folders,tags}=notesChoices(),visible=notesVisible();
 const opts=(items,value)=>items.map(s=>`<option value="${esc(s)}" ${s===value?'selected':''}>${esc(s)}</option>`).join('');
 return `<div class="panel notes-intro"><p><b>Folder</b> untuk tempat utama catatan, misalnya IZINHUKUM. <b>Tag</b> untuk penanda lintas folder, misalnya klien, tindak-lanjut. Satu catatan dapat memiliki beberapa tag.</p>${btn('Buka / buat Daily Note hari ini','daily-note')}</div>${toolbar('new-note','Catatan baru')}<div class="notes-filters"><label>Folder<select id="notes-folder"><option value="">Semua folder (${data.notes.length})</option><option value=":none:" ${notesFolder===':none:'?'selected':''}>Tanpa folder (${data.notes.filter(n=>!noteFolder(n)).length})</option>${opts(folders,notesFolder)}</select></label><label>Tag<select id="notes-tag"><option value="">Semua tag</option>${opts(tags,notesTag)}</select></label>${btn('Reset filter','notes-reset')}</div><p role="status" class="notes-count">${visible.length} dari ${data.notes.length} catatan${notesFolder||notesTag||query?' · filter aktif':''}</p><div class="grid notes-grid">${visible.map(n=>`<article class="panel note"><div class="note-meta"><span class="pill">${esc(noteFolder(n)||'Tanpa folder')}</span>${noteTags(n).map(t=>`<button class="tag-chip" data-action="notes-tag" data-id="${esc(t)}">#${esc(t)}</button>`).join('')}</div><h2>${esc(n.title)}</h2><p class="note-preview">${esc(notePreview(n))}</p>${n.project?`<p class="note-project">Proyek: ${esc(name('projects',n.project))}</p>`:''}<div class="actions">${btn('Baca','notes-read',n.id,'primary')}${btn('Edit','edit-note',n.id)}${btn('Markdown ↓','export-note',n.id)}${btn('Hapus','delete-note',n.id)}</div></article>`).join('')||empty('Tidak ada catatan yang cocok','Ubah pencarian atau reset filter. Catatan baru dapat dibuat melalui tombol di atas.')}</div>`;
}
function readNote(id){const n=data.notes.find(n=>n.id===id);if(!n)throw Error('Catatan tidak ditemukan.');const links=data.notes.filter(x=>(x.body||'').includes('[['+n.title+']]'));showInfo(esc(n.title),`<p>${esc(noteFolder(n)||'Tanpa folder')}${noteTags(n).map(t=>' · #'+esc(t)).join('')}</p><div class="note-reader">${markdown(n.body||'Belum ada isi catatan.')}</div>${n.project?'<p>Proyek: '+esc(name('projects',n.project))+'</p>':''}<hr><p>Catatan yang menautkan ke sini:</p><div class="actions">${links.map(x=>btn(esc(x.title),'notes-read',x.id)).join('')||'Belum ada tautan masuk.'}</div><div class="actions">${btn('Edit catatan','edit-note',id)}${btn('Tutup','close')}</div>`)}
const beforeNotesContent=content;
content=function(){return page==='Notes'?notesContent():beforeNotesContent()};
const beforeNotesEditor=editor;
editor=function(kind,id='',initial={}){
 beforeNotesEditor(kind,id,initial);if(kind!=='note')return;
 const form=$('#editor'),{folders,tags}=notesChoices();
 form.classList.add('note-editor');
 const folder=form.querySelector('[name="folder"]'),tag=form.querySelector('[name="tags"]'),body=form.querySelector('[name="body"]');
 folder.setAttribute('list','note-folder-options');folder.placeholder='Contoh: IZINHUKUM';
 tag.placeholder='Contoh: klien, tindak-lanjut';
 body.rows=14;
 folder.insertAdjacentHTML('afterend',`<datalist id="note-folder-options">${folders.map(f=>`<option value="${esc(f)}"></option>`).join('')}</datalist><small>Pilih folder yang sudah ada atau ketik nama baru. Kosongkan jika belum dikelompokkan.</small>`);
 tag.insertAdjacentHTML('afterend',`<small>Pisahkan dengan koma. Tag yang tersedia: ${esc(tags.join(', ')||'belum ada')}.</small>`);
};
const beforeNotesAction=consolidatedAction;
consolidatedAction=async function(a,id,event){
 if(a==='mobile-menu'){const nav=$('#main-nav'),button=$('#mobile-menu');const open=button.getAttribute('aria-expanded')!=='true';button.setAttribute('aria-expanded',String(open));nav.classList.toggle('mobile-open',open);return true}
 if(a==='notes-reset'){notesFolder='';notesTag='';query='';render();return true}
 if(a==='notes-tag'){notesTag=id;render();return true}
 if(a==='notes-read'){readNote(id);return true}
 if(a==='note-link'){const n=data.notes.find(n=>n.title===id);if(n){readNote(n.id);return true}}
 if(a==='nav'){notesFolder='';notesTag=''}
 return beforeNotesAction(a,id,event);
};
document.addEventListener('change',e=>{if(e.target.id==='notes-folder'||e.target.id==='notes-tag'){if(e.target.id==='notes-folder')notesFolder=e.target.value;else notesTag=e.target.value;$('#content').innerHTML=content()}});
