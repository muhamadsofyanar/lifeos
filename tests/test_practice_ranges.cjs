const assert=require('node:assert/strict'),fs=require('node:fs'),vm=require('node:vm');
const nodes=new Map();function node(s){if(!nodes.has(s))nodes.set(s,{innerHTML:'',textContent:'',dataset:{},showModal(){},close(){},classList:{add(){},remove(){}}});return nodes.get(s)}
const ctx=vm.createContext({console,Date,structuredClone,crypto:require('node:crypto').webcrypto,document:{querySelector:node,addEventListener(){}},setInterval(){},setTimeout(){},clearInterval(){},clearTimeout(){},URL,Blob,confirm:()=>true});
for(const f of ['app','features','hifz','wellbeing','recordings','consolidated','transfer','academy','notes','murajaah','practice-ranges'])vm.runInContext(fs.readFileSync('static/'+f+'.js','utf8'),ctx);
const run=s=>vm.runInContext(s,ctx),plain=s=>JSON.parse(JSON.stringify(run(s)));
ctx.meta=JSON.parse(fs.readFileSync('static/quran-coverage.json','utf8'));
run(`mMeta=meta;data=normalizeClient(Object.fromEntries(['inbox','tasks','projects','notes','events','sessions','reviews','areas','goals'].map(k=>[k,[]])));render=()=>{};persist=async()=>{};let savePractice,formHtml;showForm=(title,html,save)=>{savePractice=save;formHtml=html};`);
assert.deepEqual(plain("practiceRange(29,{kind:'lines',value:562,from:2,to:7}).unitIds"),['29:562:2']);
assert.equal(run("practiceRange(29,{kind:'lines',value:562,from:1,to:2}).unitIds.length"),0);
assert.equal(run("practiceRange(28,{kind:'lines',value:542,from:1,to:10}).unitIds.length"),2);
assert.equal(run("practiceRange(27,{kind:'lines',value:522,from:1,to:7}).unitIds.length"),1);
assert.equal(run("practiceRange(26,{kind:'lines',value:502,from:1,to:14}).unitIds.length"),0);
assert.deepEqual(plain("practiceBounds(2,'verses',2)"),[142,252]);
assert.ok(run("practiceRangeFields(30,{kind:'verses',value:107,from:1,to:3})").includes('>107. '));
assert.ok(run('verseRangeFields(107,1,3)').includes('107. Al-Ma'));
assert.throws(()=>run("practiceRange(29,{kind:'lines',value:562,from:1,to:16})"),/batas/);
function select(options,value){let html=options||'',v=String(value||'');const listeners={};return {parentElement:{firstChild:{textContent:''}},addEventListener(k,fn){(listeners[k]??=[]).push(fn)},fire(k){for(const f of listeners[k]||[])f()},get innerHTML(){return html},set innerHTML(s){html=s;const opts=[...s.matchAll(/<option value="([^"]*)"([^>]*)>/g)];v=opts.find(x=>x[2].includes('selected'))?.[1]||opts[0]?.[1]||''},get value(){return v},set value(x){x=String(x);v=[...html.matchAll(/<option value="([^"]*)"/g)].some(m=>m[1]===x)?x:''}}}
const opts=a=>a.map(x=>`<option value="${x}">${x}</option>`).join('');
const kind=select(opts(['lines','verses']),'lines'),target=select(opts([562]),562),from=select(opts(Array.from({length:15},(_,i)=>i+1)),2),to=select(opts(Array.from({length:15},(_,i)=>i+1)),7),hint={textContent:''};
ctx.formFixture={querySelector(s){return {'[data-practice-range]':{dataset:{juz:'29'}},'[name=rangeKind]':kind,'[name=rangeTarget]':target,'[name=rangeFrom]':from,'[name=rangeTo]':to,'[data-range-hint]':hint}[s]}};
run('bindPracticeRange(formFixture)');assert.equal(from.value,'2');assert.equal(to.value,'7');assert.ok(hint.textContent.includes('1 unit'));
from.value='15';from.fire('change');assert.equal(to.value,'15');assert.equal((to.innerHTML.match(/<option /g)||[]).length,1);
kind.value='verses';kind.fire('change');assert.equal(target.value,'67');assert.equal(from.value,'1');assert.equal((from.innerHTML.match(/<option /g)||[]).length,30);
run("prepareVerseRangeDraft(formFixture,{rangeKind:'lines',rangeTarget:'563',rangeFrom:'4',rangeTo:'9'})");assert.equal(target.value,'563');assert.equal(from.value,'4');assert.equal(to.value,'9');
(async()=>{
 run("practiceForm(30,{kind:'verses',value:107,from:1,to:3})");
 await run("savePractice({rangeKind:'verses',rangeTarget:'107',rangeFrom:'1',rangeTo:'3',date:'2026-11-01',minutes:'15',readingMode:'hafalan',status:'self',assessor:'',note:'',applyProgress:'on'})");
 assert.equal(run('data.quran.length'),3);assert.deepEqual(plain('data.quran.map(v=>v.id)'),['107:1','107:2','107:3']);
 run("practiceForm(29,{kind:'lines',value:562,from:2,to:7})");
 await run("savePractice({rangeKind:'lines',rangeTarget:'562',rangeFrom:'2',rangeTo:'7',date:'2026-11-01',minutes:'20',readingMode:'hafalan',status:'self',assessor:'',note:'',applyProgress:'on'})");
 assert.deepEqual(plain('data.quranUnits.map(u=>u.id)'),['29:562:2']);assert.equal(run('data.quranChecks.length'),2);
 assert.equal(run("summaryData('2026-11-01','2026-11-01').quran"),35);
 run("practiceForm(29,{},data.quranChecks[1].id)");assert.ok(!run('formHtml').includes('name="applyProgress" type="checkbox" checked'));
 await run("savePractice({rangeKind:'lines',rangeTarget:'562',rangeFrom:'1',rangeTo:'2',date:'2026-11-01',minutes:'5',readingMode:'melihat',status:'practiced',assessor:'',note:''})");
 assert.equal(run('data.quranChecks.length'),2);assert.equal(run('data.quranUnits[0].status'),'self');assert.equal(run('data.quranChecks[1].scope.to'),2);
 assert.throws(()=>run("savePractice({rangeKind:'lines',rangeTarget:'562',rangeFrom:'1',rangeTo:'16',date:'2026-11-01',minutes:'5',status:'self'})"),/batas/);
 console.log('Practice range checks passed: bounded selectors/draft recovery, numbered surahs, multi-verse apply, partial-unit protection, stages, history correction, actual minutes and invalid ranges.');
})().catch(e=>{console.error(e);process.exitCode=1});
