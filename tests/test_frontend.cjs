const assert=require('node:assert/strict');const fs=require('node:fs');const vm=require('node:vm');
const nodes=new Map();function node(sel){if(!nodes.has(sel))nodes.set(sel,{innerHTML:'',open:false,showModal(){this.open=true},close(){this.open=false},textContent:'',classList:{add(){},remove(){}}});return nodes.get(sel)}
const ctx=vm.createContext({console,structuredClone,crypto:require('node:crypto').webcrypto,Date,setInterval(){},setTimeout(){},document:{querySelector:node,addEventListener(){}},confirm:()=>true,FormData:class{},fetch:()=>{throw Error('Unexpected network')},URL,Blob});
vm.runInContext(fs.readFileSync('static/app.js','utf8')+'\n'+fs.readFileSync('static/features.js','utf8')+'\n'+fs.readFileSync('static/hifz.js','utf8')+'\n'+fs.readFileSync('static/wellbeing.js','utf8'),ctx);
vm.runInContext(`
data=normalizeClient(Object.fromEntries(['inbox','tasks','projects','notes','events','sessions','reviews','areas','goals','quran','quranSessions','plans','preferences'].map(k=>[k,[]])));
`,ctx);
assert.equal(vm.runInContext('SURAHS.reduce((n,s)=>n+s.count,0)',ctx),564);
assert.equal(vm.runInContext('qnext().surah+":"+qnext().ayah',ctx),'101:1');
vm.runInContext("upsertVerse(101,1,'self');upsertVerse(101,2,'strengthen')",ctx);
assert.equal(vm.runInContext('qnext().ayah',ctx),2);
vm.runInContext("upsertVerse(101,1,'strengthen')",ctx);
assert.equal(vm.runInContext('data.quran.length',ctx),2);
assert.equal(vm.runInContext("normalizeClient({tasks:[{id:'old'}]}).tasks[0].id",ctx),'old');
for(const p of ['Panduan','Belajar & Praktik','Today','Sullamul Hifz','Idea Planner','Inbox','Tasks','Projects','Notes','Calendar','Focus','Review','Analytics','Areas & Goals','Settings']){
 const html=vm.runInContext(`page=${JSON.stringify(p)};content()`,ctx);assert.equal(typeof html,'string',p);assert.ok(html.length>20,p);
}
assert.equal(vm.runInContext("planTasks({steps:'Satu\\nDua',estimates:'15,30'}).reduce((n,t)=>n+t.estimate,0)",ctx),45);
vm.runInContext("data.tasks=[{id:'repeat',status:'todo',repeat:'daily',due:'2026-11-01'}];complete(data.tasks[0]);complete(data.tasks[0]);complete(data.tasks[0])",ctx);
assert.equal(vm.runInContext('data.tasks.length',ctx),2,'Reopening must not duplicate next recurring task');
assert.ok(vm.runInContext("btn('Save','plan-save').includes('type=\"button\"')",ctx));
assert.equal(vm.runInContext('new Set(HIFZ_ORDER).size',ctx),30);
for(const [j,count] of [[30,564],[29,100],[28,60],[27,40],[26,20],[1,21],[25,20]])assert.equal(vm.runInContext(`juzUnits(${j}).length`,ctx),count);
for(let j=1;j<=30;j++){vm.runInContext(`hifzJuz=${j};quranContent()`,ctx)}
console.log('Frontend checks passed: 15 pages, 30 juz, 564 verses, original 79-verse rubu, progress, legacy normalization, estimates, recurrence, form button behavior.');
(async()=>{
 vm.runInContext(`persist=async()=>{};draft={id:'plan-test',idea:'Uji pemasaran',outcome:'Pelanggan bertambah',metric:'Pertanyaan dan transaksi',process:'Tinjau dan follow-up',frequency:'Pekanan',capacity:60,minutes:25,steps:'Catat kondisi awal\\nUji penawaran',estimates:'20,25'};planStep=5;collectPlan=()=>{};`,ctx);
 await vm.runInContext("savePlan('apply')",ctx);
 assert.equal(vm.runInContext('data.plans[0].applied',ctx),true);
 assert.equal(vm.runInContext('data.goals.length',ctx),1);
 assert.equal(vm.runInContext('data.projects.length',ctx),1);
 assert.equal(vm.runInContext('data.notes.length',ctx),1);
 assert.equal(vm.runInContext("data.tasks.filter(t=>t.project===data.projects[0].id).length",ctx),2);
 await vm.runInContext("savePlan('apply')",ctx);
 assert.equal(vm.runInContext('data.projects.length',ctx),1,'Repeated apply must not create duplicate project');
 console.log('Planner apply integration passed: goal/project/note/tasks linked, duplicate apply rejected.');
})().catch(e=>{console.error(e);process.exitCode=1});
assert.equal(vm.runInContext('RUBU.map(([a,b])=>SURAHS.filter(s=>s.number>=a&&s.number<=b).reduce((n,s)=>n+s.count,0)).join(",")',ctx),'79,67,67,75,64,55,71,86');
vm.runInContext(`data.dayPlans=[{id:today(),date:today(),work:20,rest:540,contemplation:15,quran:25,fixed:100,buffer:30}];data.tasks.push({id:'capacity',title:'A',bigDate:today(),status:'todo',estimate:90})`,ctx);
assert.ok(vm.runInContext('dayBalance().includes("melebihi kapasitas")',ctx));
console.log('Daily capacity warning and eight rubu boundaries passed.');
