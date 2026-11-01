const assert=require('node:assert/strict'),fs=require('node:fs'),vm=require('node:vm');
const nodes=new Map(),listeners={};
function node(key){if(!nodes.has(key))nodes.set(key,{innerHTML:'',textContent:'',value:'all',open:false,
 showModal(){this.open=true},close(){this.open=false},querySelectorAll(){return []},querySelector(){return null},
 insertAdjacentHTML(_p,html){this.innerHTML+=html},addEventListener(){},classList:{add(){},remove(){}}});return nodes.get(key)}
const ctx=vm.createContext({console,Date,structuredClone,crypto:require('node:crypto').webcrypto,document:{querySelector:node,addEventListener(k,fn){(listeners[k]??=[]).push(fn)}},setInterval(){},setTimeout(){},clearInterval(){},clearTimeout(){},confirm:()=>true,URL,Blob});
for(const f of ['app','features','hifz','wellbeing','recordings','consolidated','transfer'])vm.runInContext(fs.readFileSync(`static/${f}.js`,'utf8'),ctx);
const run=code=>vm.runInContext(code,ctx);
ctx.fixture={kind:'lifeos-import',version:'1.0',purpose:'starter',name:'Starter fixture',data:{areas:[{id:'a',title:'Area'}],goals:[{id:'g',title:'Goal',area:'a'}],projects:[{id:'p',title:'Project',area:'a',goal:'g'}],tasks:Array.from({length:42},(_,i)=>({id:'t'+i,title:'Task '+i,project:'p',status:'todo'})),notes:[{id:'n',title:'Note',project:'p'}]}};
ctx.catalogFixture=JSON.parse(fs.readFileSync('templates/catalog.json','utf8'));
run(`data=normalizeClient(Object.fromEntries(['inbox','tasks','projects','notes','events','sessions','reviews','areas','goals'].map(k=>[k,[]])));revision=7;let messages=[],downloads=[],calls=[];toast=x=>messages.push(x);download=(...args)=>downloads.push(args);render=()=>{};`);
(async()=>{
 assert.equal(run('Object.keys(emptyImportTemplate().data).length'),23);
 assert.equal(run('typeof emptyImportTemplate().version'),'string');
 run('page="Settings"');assert.ok(run('content()').includes('Impor data &amp; template')||run('content()').includes('Impor data & template'));
 run('importDialog();stageImport(fixture)');
 assert.equal(run('importSelected.length'),5);
 assert.ok(node('#import-selection').innerHTML.includes('42'));
 assert.equal(run('importPreview'),null);
 run(`api=async(path,body)=>{calls.push({path,body});if(path==='import/templates')return catalogFixture;return {revision:path==='import/apply'?8:7,report:{added:91,skipped:0,collections:{tasks:{added:42,skipped:0}},items:[],example:false}}};load=async()=>{revision=8};`);
 await run("transferAction('import-preview')");
 assert.equal(run('importPreview.revision'),7);
 assert.equal(run('data.tasks.length'),0,'Preview must not mutate local state');
 assert.ok(node('#import-preview').innerHTML.includes('91 data baru'));
 await run("transferAction('import-apply')");
 assert.equal(run('busy'),false);
 assert.equal(run('importPreview'),null);
 assert.equal(run("calls.find(c=>c.path==='import/apply').body.revision"),7);
 assert.ok(run('messages.at(-1)').includes('91 data ditambahkan'));
 // Re-selecting collections invalidates a previous preview.
 run('stageImport(fixture);importPreview={revision:8};');
 nodes.set('#modal',{querySelectorAll:()=>[{dataset:{importKind:'notes'}}],open:true,close(){this.open=false}});
 for(const fn of listeners.change||[])await fn({target:{id:'',dataset:{importKind:'tasks'}}});
 assert.equal(run('importSelected.join(",")'),'notes');
 assert.equal(run('importPreview'),null);
 // Generic examples include dependencies, with clear fictional provenance.
 node('#import-template-kind').value='metricLogs';
 await run("transferAction('import-example')");
 const example=JSON.parse(run('downloads.at(-1)[1]'));
 assert.equal(example.purpose,'example');
 assert.deepEqual(Object.keys(example.data).sort(),['areas','goals','metricLogs']);
 run('stageImport(catalogFixture.example)');
 assert.ok(node('#import-selection').innerHTML.includes('FIKTIF'));
 // The restore handler must refuse the merge package rather than replace all data.
 const snapshot=run('JSON.stringify(data)');
 const file={size:100,text:async()=>JSON.stringify(ctx.fixture)};
 for(const fn of listeners.change||[])await fn({target:{id:'restore',files:[file],dataset:{}}});
 assert.equal(run('JSON.stringify(data)'),snapshot);
 assert.ok(run('messages.at(-1)').includes('bukan Restore backup'));
 // Rejected apply does not leave a usable stale preview or a busy lock.
 run(`stageImport(fixture);importPreview={revision:8,report:{added:91}};api=async()=>{throw Error('conflict')}`);
 await assert.rejects(run("transferAction('import-apply')"),/conflict/);
 assert.equal(run('busy'),false);
 assert.equal(run('importPreview'),null);
 console.log('Transfer UI regressions passed: 23 templates, staging/selection, preview without mutation, explicit apply, dependency examples, fictional labels, restore refusal and conflict recovery.');
})().catch(e=>{console.error(e);process.exitCode=1});
