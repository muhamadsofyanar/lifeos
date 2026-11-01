const assert=require('node:assert/strict'),fs=require('node:fs'),vm=require('node:vm');
const nodes=new Map(),listeners={};
function node(s){if(!nodes.has(s))nodes.set(s,{innerHTML:'',textContent:'',dataset:{},values:{},open:false,showModal(){this.open=true},close(){this.open=false},classList:{add(){},remove(){}},querySelector(){return null},querySelectorAll(){return []},insertAdjacentHTML(_p,h){this.innerHTML+=h}});return nodes.get(s)}
const ctx=vm.createContext({console,Date,structuredClone,TextEncoder,crypto:require('node:crypto').webcrypto,document:{querySelector:node,addEventListener(k,cb){(listeners[k]??=[]).push(cb)}},setInterval(){},setTimeout(){},clearInterval(){},clearTimeout(){},URL,Blob,confirm:()=>true,FormData:class{constructor(f){this.values=f.values}[Symbol.iterator](){return Object.entries(this.values)[Symbol.iterator]()}},fetch:async path=>({ok:true,json:async()=>JSON.parse(fs.readFileSync('static'+path,'utf8')),text:async()=>fs.readFileSync('static'+path,'utf8')})});
for(const f of ['app','features','hifz','wellbeing','recordings','consolidated','transfer','academy','notes','murajaah'])vm.runInContext(fs.readFileSync('static/'+f+'.js','utf8'),ctx);
const run=s=>vm.runInContext(s,ctx),plain=s=>JSON.parse(JSON.stringify(run(s)));
ctx.metaFixture=JSON.parse(fs.readFileSync('static/quran-coverage.json','utf8'));
run(`data=normalizeClient(Object.fromEntries(['inbox','tasks','projects','notes','events','sessions','reviews','areas','goals'].map(k=>[k,[]])));mMeta=metaFixture;revision=1;persist=async()=>{};render=()=>{};attachDraft=()=>{};`);
assert.deepEqual(plain("mCoverage(29,{kind:'page',value:562}).segments"),[[67,1,12]]);
assert.deepEqual(plain("mCoverage(29,{kind:'surah',value:67}).segments"),[[67,1,30]]);
assert.equal(run("mCoverage(30,{kind:'juz',value:30}).count"),564);
assert.equal(run("mCoverage(30,{kind:'rubu',value:1}).segments[0][0]"),101);
assert.equal(run("mCoverage(30,{kind:'rubu',value:1}).segments.at(-1)[0]"),114);
assert.equal(run("mCoverage(1,{kind:'surah',value:2}).count"),286);
assert.equal(run("mCoverage(1,{kind:'surah',value:2}).crossJuz"),true);
assert.throws(()=>run("mCoverage(29,{kind:'page',value:582})"),/luar juz/);
const recordsBefore=run('JSON.stringify(data)');
run('hifzJuz=29');assert.ok(run('murajaahPanel()').includes('Murajaah')||run('murajaahPanel()').includes('murajaah'));
for(let j=1;j<=30;j++){
 const c=plain(`mCoverage(${j},{kind:'juz',value:${j}})`),parts=plain(`Array.from({length:8},(_,i)=>mCoverage(${j},{kind:'rubu',value:i+1}))`);
 assert.equal(parts.reduce((sum,p)=>sum+p.count,0),c.count,'all eight rubu must cover the juz');
 for(const kind of ['page','surah'])for(const [value] of plain(`mOptions(${j},'${kind}')`))assert.ok(run(`mCoverage(${j},{kind:'${kind}',value:${value}}).count`)>0);
}
assert.equal(run('JSON.stringify(data)'),recordsBefore,'Choosing and reading must not update memorization');
(async()=>{
 await run('ensureMurajaahText()');
 const cExpr="mCoverage(29,{kind:'page',value:562})";
 const html=run(`murajaahReading(${cExpr})`);
 assert.equal((html.match(/data-verse=/g)||[]).length,12);
 assert.ok(html.includes('data-verse="67:12"'));assert.ok(!html.includes('data-verse="67:13"'));
 assert.ok(html.includes('dir="rtl"'));assert.ok(html.includes('https://tanzil.net'));
 assert.equal((run("murajaahReading(mCoverage(29,{kind:'surah',value:67}))").match(/data-verse=/g)||[]).length,30);
 assert.equal((run("murajaahReading(mCoverage(30,{kind:'juz',value:30}))").match(/data-verse=/g)||[]).length,564);
 // Real form save callback stores a review only, without modifying verse/unit progress.
 run('let savedReview;showForm=(title,html,save)=>{savedReview=save};murajaahLogForm(29,{kind:"surah",value:67})');
 await run(`savedReview({date:'2026-11-01',minutes:'45',readingMode:'hafalan',status:'self',assessor:'',note:'Ulangi sambungan',nextReview:'2026-11-03'})`);
 assert.equal(run('data.quranChecks.length'),1);assert.equal(run('data.quran.length'),0);assert.equal(run('data.quranUnits.length'),0);
 assert.equal(run("summaryData('2026-11-01','2026-11-01').quran"),45);
 run('murajaahLogForm(29,{kind:"surah",value:67},data.quranChecks[0].id)');
 await run(`savedReview({date:'2026-11-01',minutes:'40',readingMode:'melihat',status:'practiced',assessor:'',note:'',nextReview:''})`);
 assert.equal(run('data.quranChecks.length'),1,'Correction must update same record');assert.equal(run('data.quranChecks[0].minutes'),40);
 const form=node('#recording-form');form.dataset={juz:'29',coverage:'1',scope:'{"kind":"page","value":562}'};
 form.values={title:'Murajaah halaman',date:'2026-11-01',reviewSession:run('data.quranChecks[0].id'),note:''};
 const metadata=plain('recordingMetadata()');assert.equal(metadata.targetVersion,2);assert.equal(metadata.scope.value,562);assert.equal(metadata.target,'Halaman 562 utuh');
 form.dataset.scope='{"kind":"juz","value":29}';assert.throws(()=>run('recordingMetadata()'),/tidak sesuai/);
 // Opening reads source text but does not activate microphone or persist state.
 const saved=run('JSON.stringify(data)');await run('murajaahDialog(29,{kind:"page",value:562})');
 assert.ok(node('#modal').innerHTML.includes('data-max-minutes="60"'));
 assert.ok(node('#modal').innerHTML.includes('value="120"'));
 assert.equal(run('rec.stream'),null);assert.equal(run('JSON.stringify(data)'),saved);
 // A whole-scope clip uses the selected 120-minute limit and the normal upload lifecycle.
 const delays=[];ctx.setTimeout=(_fn,ms)=>{delays.push(ms);return 1};ctx.isSecureContext=true;
 let micStops=0,postedMetadata;
 ctx.navigator={mediaDevices:{getUserMedia:async()=>({getTracks:()=>[{stop(){micStops++}}]})}};
 ctx.MediaRecorder=class{static isTypeSupported(t){return t==='audio/mp4'}constructor(_stream,options){this.mimeType=options.mimeType;this.state='inactive'}start(){this.state='recording'}stop(){this.state='inactive';this.ondataavailable({data:new Blob(['fake audio fixture'],{type:'audio/mp4'})});this.onstop()}};
 form.dataset={juz:'29',coverage:'1',scope:'{"kind":"page","value":562}',maxMinutes:'120'};
 form.values={title:'Murajaah halaman',date:'2026-11-01',reviewSession:'',note:''};
 await run('beginRecording()');assert.equal(run('recordingActive()'),true);assert.ok(delays.includes(120*60*1000));
 run('finishRecording()');assert.equal(micStops,1);assert.equal(run('rec.blob.size>0'),true);
 const fileFetch=ctx.fetch;ctx.fetch=async(path,request)=>{assert.equal(path,'/api/recordings');postedMetadata=JSON.parse(decodeURIComponent(request.headers['X-Recording-Metadata']));return {ok:true,json:async()=>({created:true})}};
 run('loadRecordings=async()=>{}');await run('saveRecording()');assert.equal(postedMetadata.targetVersion,2);assert.equal(postedMetadata.scope.value,562);assert.equal(run('rec.blob'),null);ctx.fetch=fileFetch;
 // A modified corpus must not be displayed.
 run('mVerses=null');const oldFetch=ctx.fetch;ctx.fetch=async()=>({ok:true,text:async()=>fs.readFileSync('static/quran-uthmani.txt','utf8').replace('ٱللَّهِ','ٱللَّهَ')});
 await assert.rejects(()=>run('ensureMurajaahText()'),/Integritas/);ctx.fetch=oldFetch;
 console.log('Murajaah UI passed: whole scopes, all juz/rubu partitions, RTL text and integrity, read/record dialog, scoped metadata, log/correction, no automatic mutabaah, duration summary and session containment.');
})().catch(e=>{console.error(e);process.exitCode=1});
