const assert=require('node:assert/strict'),fs=require('node:fs'),vm=require('node:vm');
const nodes=new Map();
function node(key){
 if(!nodes.has(key))nodes.set(key,{innerHTML:'',textContent:'',open:false,values:{},
  showModal(){this.open=true},close(){this.open=false},
  insertAdjacentHTML(_where,html){this.innerHTML+=html},
  querySelector(){return null},querySelectorAll(){return []},addEventListener(){},
  classList:{add(){},remove(){}}});
 return nodes.get(key);
}
class FormDataFixture{
 constructor(form){this.values=form.values}
 [Symbol.iterator](){return Object.entries(this.values)[Symbol.iterator]()}
}
const ctx=vm.createContext({console,Date,structuredClone,crypto:require('node:crypto').webcrypto,
 document:{querySelector:node,addEventListener(){}},FormData:FormDataFixture,
 confirm:()=>true,setInterval(){},setTimeout(){},clearInterval(){},clearTimeout(){},URL,Blob});
for(const name of ['app','features','hifz','wellbeing','recordings','consolidated'])vm.runInContext(fs.readFileSync(`static/${name}.js`,'utf8'),ctx);
const run=code=>vm.runInContext(code,ctx);
run(`data=normalizeClient(Object.fromEntries(['inbox','tasks','projects','notes','events','sessions','reviews','areas','goals'].map(k=>[k,[]])));persist=async()=>{};render=()=>{};let savedForm,savedHtml;showForm=(title,html,save)=>{savedForm=save;savedHtml=html};attachDraft=()=>{};`);

(async()=>{
 run(`data.projects=[{id:'p" data-injected="yes',title:'Imported'}]`);
 const options=run("options('projects','')");
 assert.ok(options.includes('value="p&quot; data-injected=&quot;yes"'));
 assert.ok(!options.includes('value="p" data-injected='));

 run('qlog()');
 await run(`savedForm({date:today(),minutes:'20',surah:'101',from:'1',to:'11',status:'self',teacher:'',mode:'Murajaah saja',note:'',updateProgress:'on'})`);
 assert.equal(run('data.quran.length'),11);
 const logId=run('data.quranSessions[0].id');
 run(`qlog(${JSON.stringify(logId)})`);
 assert.ok(run('savedHtml').includes('koreksi hanya mengubah riwayat'));
 await run(`savedForm({date:today(),minutes:'25',surah:'101',from:'1',to:'11',status:'strengthen',teacher:'',mode:'Murajaah saja',note:''})`);
 assert.equal(run('data.quran[0].status'),'self','History-only correction must preserve current progress');
 assert.equal(run('data.quranSessions[0].minutes'),25);
 await run(`savedForm({date:today(),minutes:'25',surah:'102',from:'1',to:'8',status:'teacher',teacher:'Penyimak',mode:'Setoran ke guru',note:'',updateProgress:'on'})`);
 assert.equal(run("data.quran.filter(q=>q.surah===102&&q.status==='teacher').length"),8);
 assert.equal(run("data.quran.filter(q=>q.surah===101).length"),11,'Changing session target must not silently delete prior progress');

 run('hifzJuz=1;hLog()');
 await run(`savedForm({date:today(),minutes:'25',unit:'1:2:1',load:'S2',status:'self',connection:'not_checked',teacher:'',note:'',updateProgress:'on'})`);
 assert.equal(run('data.quranUnitSessions[0].units.join(",")'),'1:2:1,1:3:1');
 assert.equal(run('data.quranUnits.length'),2);
 assert.equal(run('data.quranUnitSessions[0].connection'),'not_checked');
 assert.ok(run('hLogs(1)').includes('Belum diperiksa'));
 assert.ok(!run('hLogs(1)').includes('undefined'));
 const unitLogId=run('data.quranUnitSessions[0].id');
 run(`hLogEdit(${JSON.stringify(unitLogId)})`);
 assert.throws(()=>run(`savedForm({date:today(),minutes:'25',unit:'1:2:1',load:'S2',status:'self',connection:'teacher',teacher:'',note:''})`),/penyimak/);
 assert.throws(()=>run(`savedForm({date:today(),minutes:'25',unit:'1:21:1',load:'S2',status:'self',connection:'self',teacher:'',note:''})`),/dua halaman/);
 assert.throws(()=>run(`savedForm({date:today(),minutes:'25',unit:'1:2:1',load:'N',status:'self',connection:'not_checked',teacher:'',note:''})`),/Potongan kecil/);
 await run(`savedForm({date:today(),minutes:'30',unit:'1:2:1',load:'S2',status:'strengthen',connection:'teacher',teacher:'Penyimak sambungan',note:''})`);
 assert.equal(run('data.quranUnitSessions.length'),1);
 assert.equal(run('data.quranUnitSessions[0].connection'),'teacher');
 assert.equal(run('data.quranUnits[0].status'),'self','History edit must not implicitly overwrite progress');

 // Execute the actual task editor submit handler, including its completion paths.
 async function submitTask(id,values){
  run(`editor('task',${JSON.stringify(id)})`);
  const form=node('#editor');form.values={title:'Task',status:'todo',priority:'normal',estimate:'25',repeat:'none',...values};
  await form.onsubmit({preventDefault(){},target:form});
 }
 await submitTask('',{status:'done',repeat:'daily'});
 assert.equal(run('data.tasks.length'),2);
 assert.equal(run('summaryData(today(),today()).completed'),1);
 assert.equal(run("data.tasks.find(t=>t.status==='todo').completedDay"),null);
 const taskId=run("data.tasks.find(t=>t.status==='done').id");
 await submitTask(taskId,{status:'todo',repeat:'daily'});
 assert.equal(run('summaryData(today(),today()).completed'),0);
 await submitTask(taskId,{status:'done',repeat:'daily'});
 assert.equal(run('summaryData(today(),today()).completed'),1);
 assert.equal(run('data.tasks.length'),2,'Reopening/completing must not duplicate recurring copy');

 // Planner Inbox reference and measurement source must remain distinct.
 run(`data.inbox=[{id:'inbox-one',title:'Original idea'}];draft={id:'p1',source:'inbox-one',measurementSource:'Service log',idea:'Improve service',outcome:'Faster service',metric:'Response time',unit:'hours',baseline:'48',target:'24',period:'weekly',process:'Review delays',frequency:'weekly',capacity:60,minutes:25,steps:'Inspect log',estimates:'25'};planStep=5;collectPlan=()=>{};`);
 await run("savePlan('apply')");
 assert.equal(run('data.inbox.length'),0);
 assert.equal(run('data.goals[0].source'),'Service log');
 assert.equal(run('data.plans[0].source'),'inbox-one');
 assert.equal(run('data.goals[0].measurementVersion'),1);
 assert.throws(()=>run(`requireMeasurement({metric:'Response time'})`),/Lengkapi/);

 run(`data.quranSessions=Array.from({length:25},(_,i)=>({id:'page'+i,date:today(),minutes:20,surah:101,from:1,to:1,status:'practiced',note:'',created:i}));hHistoryLimit=20`);
 assert.equal((run('hLogs(30)').match(/class="panel session-card"/g)||[]).length,20);
 assert.ok(run('hLogs(30)').includes('Tampilkan 20 sesi berikutnya'));
 await run("hifzAction('h-log-more','')");
 assert.equal((run('hLogs(30)').match(/class="panel session-card"/g)||[]).length,25);
 assert.ok(!run('hLogs(30)').includes('<p>Sudah dilatih · </p>'));
 const progressCount=run('data.quran.length');
 await run("hifzAction('h-log-delete','verse:page0')");
 assert.equal(run('data.quranSessions.length'),24);
 assert.equal(run('data.quran.length'),progressCount);
 assert.equal(run("localDate(new Date(2026,10,1))"),'2026-11-01');
 console.log('Repair regressions passed: escaped IDs, session corrections/explicit progress, S2 units/connection/teacher/partial load, editor completion/reopening/recurrence, planner source separation, history pagination/deletion and local dates.');
})().catch(error=>{console.error(error);process.exitCode=1});
