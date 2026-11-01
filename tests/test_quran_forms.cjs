const assert=require('node:assert/strict'),fs=require('node:fs'),vm=require('node:vm');
const nodes=new Map();function node(s){if(!nodes.has(s))nodes.set(s,{innerHTML:'',textContent:'',dataset:{juz:'30'},open:false,showModal(){this.open=true},close(){this.open=false},classList:{add(){},remove(){}}});return nodes.get(s)}
const ctx=vm.createContext({console,Date,structuredClone,crypto:require('node:crypto').webcrypto,document:{querySelector:node,addEventListener(){}},FormData:class{constructor(form){this.form=form}[Symbol.iterator](){return Object.entries(this.form.values)[Symbol.iterator]()}},setInterval(){},setTimeout(){},clearInterval(){},clearTimeout(){},confirm:()=>true,URL,Blob});
for(const f of ['app','features','hifz','wellbeing','recordings','consolidated'])vm.runInContext(fs.readFileSync('static/'+f+'.js','utf8'),ctx);
const run=s=>vm.runInContext(s,ctx);
run(`data=normalizeClient(Object.fromEntries(['inbox','tasks','projects','notes','events','sessions','reviews','areas','goals'].map(k=>[k,[]])));render=()=>{};persist=async()=>{};data.quranSessions=[{id:'same-prefix-aaaa-one',date:'2026-11-01',minutes:20,surah:101,from:1,to:11,status:'practiced'},{id:'same-prefix-aaaa-two',date:'2026-11-01',minutes:20,surah:102,from:1,to:8,status:'practiced'}];data.quranUnitSessions=[{id:'j29',juz:29,date:'2026-11-01',minutes:20,units:['29:562:1'],status:'practiced'},{id:'j28',juz:28,date:'2026-11-01',minutes:20,units:['28:542:1'],status:'practiced'}];`);
function select(initialOptions,value){
 const listeners={};let html=initialOptions||'',selected=value||'';
 return {tagName:'SELECT',listeners,addEventListener(type,fn){(listeners[type]??=[]).push(fn)},
  get innerHTML(){return html},set innerHTML(v){html=v;const options=[...html.matchAll(/<option value="([^"]*)"([^>]*)>/g)];const explicit=options.find(x=>x[2].includes('selected'));selected=explicit?.[1]??(options.some(x=>x[1]===selected)?selected:options[0]?.[1]||'')},
  get value(){return selected},set value(v){v=String(v);selected=[...html.matchAll(/<option value="([^"]*)"/g)].some(x=>x[1]===v)?v:''},
  fire(type){for(const fn of listeners[type]||[])fn({target:this})}
 };
}
const options=(values)=>values.map(x=>`<option value="${x}">${x}</option>`).join('');
const surah=select(options(Array.from({length:37},(_,i)=>i+78)),'101'),from=select(options([1]),'1'),to=select(options([1]),'1');
const hint={textContent:''},sessionHint={textContent:''},session=select(options(['','same-prefix-aaaa-one','same-prefix-aaaa-two']),'');
const title={value:'Latihan Juz 30'},date={value:'2026-11-01'};
const elements={'[name=surah]':surah,'[name=from]':from,'[name=to]':to,'[data-verse-hint]':hint,'[name=session]':session,'[data-session-detail]':sessionHint,'[name=title]':title,'[name=date]':date};
const form={dataset:{juz:'30',autoTitle:'Latihan Juz 30'},querySelector:s=>elements[s]||null};ctx.formFixture=form;
run('bindVerseRange(formFixture)');
assert.equal((from.innerHTML.match(/<option /g)||[]).length,11);
assert.equal((to.innerHTML.match(/<option /g)||[]).length,11);
assert.ok(hint.textContent.includes('11'));
surah.value='114';surah.fire('change');
assert.equal((from.innerHTML.match(/<option /g)||[]).length,6);
assert.equal(from.value,'1');assert.equal(to.value,'1');
from.value='6';from.fire('change');
assert.equal((to.innerHTML.match(/<option /g)||[]).length,1);
assert.equal(to.value,'6');
to.value='-1';assert.equal(to.value,'');
surah.value='102';surah.fire('change');
assert.equal((from.innerHTML.match(/<option /g)||[]).length,8);
run("prepareVerseRangeDraft(formFixture,{surah:'78',from:'25',to:'40'})");
assert.equal(from.value,'25');assert.equal(to.value,'40');
assert.equal((to.innerHTML.match(/<option /g)||[]).length,16);
surah.value='102';surah.fire('change');
const html=run('hifzJuz=30;audioTargetFields("")');
assert.ok(html.includes('Al-Qari'));
assert.ok(html.includes('At-Takatsur'));
assert.ok(html.includes('ayat 1–11'));
assert.ok(html.includes('ayat 1–8'));
const code1=run('hSessionCode(data.quranSessions[0],data.quranSessions)');
const code2=run('hSessionCode(data.quranSessions[1],data.quranSessions)');
assert.notEqual(code1,code2,'Even same-prefix IDs must produce distinguishable codes');
assert.ok(run('hLogs(30)').includes('Rekam sesi ini'));
run('bindRecordingSession(formFixture)');
session.value='same-prefix-aaaa-two';session.fire('change');
assert.equal(surah.value,'102');assert.equal(from.value,'1');assert.equal(to.value,'8');
assert.ok(sessionHint.textContent.includes('At-Takatsur'));
assert.equal(date.value,'2026-11-01');
to.value='4';to.fire('change');
assert.equal(session.value,'same-prefix-aaaa-two');
assert.ok(title.value.endsWith('ayat 1–4'));
surah.value='101';surah.fire('change');
assert.equal(session.value,'','Changing target to another surah must detach an incompatible session');
assert.ok(sessionHint.textContent.includes('dilepas'));
// Custom titles are preserved when selecting another session.
title.value='Rekaman pribadi saya';session.value='same-prefix-aaaa-one';session.fire('change');
assert.equal(title.value,'Rekaman pribadi saya');
assert.equal(to.value,'11');
assert.throws(()=>run(`validateRecordingSession({session:'j29',surah:101,from:1,to:1},30)`),/sesi|Sesi/);
assert.throws(()=>run(`validateRecordingSession({session:'same-prefix-aaaa-one',surah:102,from:1,to:1},30)`),/rentang|Rentang/);
run('hifzJuz=29');const unitHtml=run('audioTargetFields("")');
assert.ok(unitHtml.includes('j29'));assert.ok(!unitHtml.includes('value="j28"'));
assert.ok(!unitHtml.includes('Al-Qari'));
assert.ok(run(`recordingSessionText({juz:30,session:'deleted'})`).includes('tidak ditemukan'));
assert.ok(run(`recordingSessionText({juz:30,session:'same-prefix-aaaa-two'})`).includes('At-Takatsur'));
console.log('Quran form regressions passed: bounded verse selects, dynamic surah/from changes, descriptive and unique session labels, same-juz filtering, history shortcut, target sync/detach, custom title and missing-session display.');
