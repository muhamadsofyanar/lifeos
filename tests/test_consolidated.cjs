const assert=require('node:assert/strict'),fs=require('node:fs'),vm=require('node:vm');
const nodes=new Map();function node(s){if(!nodes.has(s))nodes.set(s,{innerHTML:'',textContent:'',open:false,insertAdjacentHTML(_p,html){this.innerHTML+=html},showModal(){this.open=true},close(){this.open=false},classList:{add(){},remove(){}}});return nodes.get(s)}
const ctx=vm.createContext({console,Date,structuredClone,URL,Blob,crypto:require('node:crypto').webcrypto,document:{querySelector:node,addEventListener(){}},setInterval(){},setTimeout(){},clearInterval(){},clearTimeout(){},FormData:class{},confirm:()=>true,fetch:()=>{throw Error('Unexpected network')}});
for(const f of ['app','features','hifz','wellbeing','recordings','consolidated'])vm.runInContext(fs.readFileSync(`static/${f}.js`,'utf8'),ctx);
vm.runInContext(`data=normalizeClient(Object.fromEntries(['inbox','tasks','projects','notes','events','sessions','reviews','areas','goals'].map(k=>[k,[]])));persist=async()=>{};render=()=>{};`,ctx);
for(const p of ['Rutinitas','Catatan Waktu','Cari Semua','Calendar','Today','Review','Analytics','Focus','Notes','Settings'])assert.ok(vm.runInContext(`page=${JSON.stringify(p)};content().length>20`,ctx),p);
vm.runInContext(`data.routines=[{id:'weekday',title:'Latihan',days:[1,2,3,4,5],start:'2026-11-01',minutes:20},{id:'paused',title:'Jeda',days:[1],start:'2026-11-01',minutes:20,active:false},{id:'future',title:'Nanti',days:[1],start:'2026-12-01',minutes:20}];`,ctx);
assert.equal(vm.runInContext("dueRoutines('2026-11-02').length",ctx),1);
assert.equal(vm.runInContext("dueRoutines('2026-11-01').length",ctx),0);
vm.runInContext(`data.events=[{id:'one',date:'2026-11-02',time:'09:00',until:'10:00',title:'Belajar'}]`,ctx);
assert.equal(vm.runInContext("calendarConflicts({date:'2026-11-02',time:'09:30',until:'10:30'}).length",ctx),1);
assert.equal(vm.runInContext("calendarConflicts({date:'2026-11-02',time:'10:00',until:'11:00'}).length",ctx),0);
assert.equal(vm.runInContext("calendarConflicts({date:'2026-11-02',time:'09:30',until:'10:30'},'one').length",ctx),0);
assert.equal(vm.runInContext("suggestedPlan('saya ingin pelanggan izinhukum').steps.includes('Catat pertanyaan')",ctx),true);
assert.equal(vm.runInContext("suggestedPlan('hafalan quran').minutes",ctx),25);
vm.runInContext(`data.quranChecks=[{id:'old',juz:30,nextReview:today()},{id:'new',juz:30,nextReview:dateAdd(today(),7)},{id:'due',juz:29,nextReview:today()}]`,ctx);
assert.equal(vm.runInContext('murajaahDue().length',ctx),1);
// Exercise actual record handlers and persistence mutation boundaries with a captured form callback.
vm.runInContext(`let savedForm;showForm=(title,html,save)=>{savedForm=save};`,ctx);
(async()=>{
 vm.runInContext("routineRecord('weekday')",ctx);
 await vm.runInContext("savedForm({status:'done',note:'Latihan pertama'})",ctx);
 vm.runInContext("routineRecord('weekday')",ctx);
 await vm.runInContext("savedForm({status:'skip',note:'Sesuaikan beban'})",ctx);
 assert.equal(vm.runInContext('data.routineLogs.length',ctx),1);
 assert.equal(vm.runInContext('data.routineLogs[0].status',ctx),'skip');
 for(let i=0;i<4;i++){
  vm.runInContext(`data.sessions.push({id:'focus${i}',start:Date.now()-25*60000,end:null,day:today()})`,ctx);
  await vm.runInContext(`change(()=>{data.sessions.find(s=>s.id==='focus${i}').end=Date.now()})`,ctx);
 }
 assert.equal(vm.runInContext("data.preferences.find(p=>p.id==='focus-rounds').count",ctx),4);
 assert.equal(vm.runInContext('breakState().duration',ctx),15);
 await vm.runInContext("change(()=>data.notes.push({id:'note',title:'Unrelated'}))",ctx);
 assert.equal(vm.runInContext("data.preferences.find(p=>p.id==='focus-rounds').count",ctx),4);
 vm.runInContext("data.timeEntries=[{id:'manual',date:today(),minutes:30,title:'Koordinasi'}]",ctx);
 assert.equal(vm.runInContext('summaryData(today(),today()).manual',ctx),30);
 assert.ok(vm.runInContext('summaryData(today(),today()).focus>=100',ctx));
 vm.runInContext("data.goals.push({id:'g',title:'Pelanggan'});indicatorForm('g')",ctx);
 await vm.runInContext("savedForm({title:'Pertanyaan masuk',unit:'orang per pekan',baseline:'0',target:'Tentukan setelah uji'})",ctx);
 const indicatorId=vm.runInContext("data.goals.find(g=>g.id==='g').indicators[0].id",ctx);
 vm.runInContext(`indicatorRecord('g',${JSON.stringify(indicatorId)})`,ctx);
 await vm.runInContext("savedForm({date:today(),value:'3',note:'Catatan aktual'})",ctx);
 assert.equal(vm.runInContext("data.metricLogs.find(l=>l.goal==='g').value",ctx),3);
 assert.equal(vm.runInContext("data.metricLogs.find(l=>l.goal==='g').indicator",ctx),indicatorId);
 // Draft protection saves locally, restores, excludes passwords/files, and clears independently.
 const storage=new Map();ctx.localStorage={getItem:k=>storage.get(k)||null,setItem:(k,v)=>storage.set(k,v),removeItem:k=>storage.delete(k)};
 const els=[{name:'body',type:'textarea',value:'Jangan hilang'},{name:'password',type:'password',value:'secret'},{name:'file',type:'file',value:'private.wav'}];
 const form={querySelectorAll:()=>els,insertAdjacentHTML(){},querySelector:()=>({textContent:''}),addEventListener(type,fn){this.input=fn}};
 ctx.formFixture=form;vm.runInContext("attachDraft(formFixture,'draft-test')",ctx);form.input();
 const saved=[...storage.values()][0];assert.ok(saved.includes('Jangan hilang'));assert.ok(!saved.includes('secret'));assert.ok(!saved.includes('private.wav'));
 els[0].value='';vm.runInContext("attachDraft(formFixture,'draft-test')",ctx);assert.equal(els[0].value,'Jangan hilang');
 storage.set('lifeos:draft:v1:draft-test',JSON.stringify({updated:Date.now(),revision:1,values:{body:'Draft lama'}}));vm.runInContext('revision=2',ctx);els[0].value='Data server lebih baru';vm.runInContext("attachDraft(formFixture,'draft-test')",ctx);assert.equal(els[0].value,'Data server lebih baru');
 nodes.set('#modal form',form);await vm.runInContext("consolidatedAction('draft-restore','draft-test')",ctx);assert.equal(els[0].value,'Draft lama');
 vm.runInContext("clearDraft('draft-test')",ctx);assert.equal(storage.size,0);
 console.log('Consolidated checks passed: schedules, routine upsert, calendar overlap, goal suggestions, murajaah due, Pomodoro rounds, actual summaries and local draft recovery.');
})().catch(e=>{console.error(e);process.exitCode=1});
