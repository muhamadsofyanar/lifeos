const assert=require('node:assert/strict'),fs=require('node:fs'),vm=require('node:vm');
const nodes=new Map();function node(s){if(!nodes.has(s))nodes.set(s,{innerHTML:'',textContent:'',open:false,values:{},showModal(){this.open=true},close(){this.open=false},querySelector(){return {textContent:''}},querySelectorAll(){return []},addEventListener(){},insertAdjacentHTML(_p,h){this.innerHTML+=h},classList:{add(){},remove(){}}});return nodes.get(s)}
class FormDataFixture{constructor(form){this.values=form.values}[Symbol.iterator](){return Object.entries(this.values)[Symbol.iterator]()}}
const ctx=vm.createContext({console,Date,structuredClone,crypto:require('node:crypto').webcrypto,document:{querySelector:node,addEventListener(){}},FormData:FormDataFixture,confirm:()=>true,setInterval(){},setTimeout(){},clearInterval(){},clearTimeout(){},URL,Blob});
for(const f of ['app','features','hifz','wellbeing','recordings','consolidated','transfer','academy'])vm.runInContext(fs.readFileSync('static/'+f+'.js','utf8'),ctx);
const run=s=>vm.runInContext(s,ctx);
run(`data=normalizeClient(Object.fromEntries(['inbox','tasks','projects','notes','events','sessions','reviews','areas','goals'].map(k=>[k,[]])));revision=1;persist=async()=>{};render=()=>{};attachDraft=()=>{};let savedForm;showForm=(title,html,save)=>{savedForm=save};`);
(async()=>{
 assert.equal(run('ACADEMY_LESSONS.length'),9);
 for(const lesson of run('ACADEMY_LESSONS')){
  assert.ok(lesson.sources.length>0,lesson.id);
  assert.equal(typeof lesson.question,'string');
  assert.equal(lesson.options.length,3);
  assert.ok(lesson.answer>=0&&lesson.answer<3);
  const html=run(`academyLessonHtml(${JSON.stringify(lesson.id)})`);
  assert.ok(html.includes('Sumber'));
  assert.ok(html.includes('Latihan'));
 }
 run(`page='Belajar LifeOS'`);assert.ok(run('content()').includes('Belajar → coba → tinjau'));
 run("academyExercise('smart')");
 assert.throws(()=>run("savedForm({answer:'0',evidence:'Saya sudah paham'})"),/jawaban|Jawaban/);
 await run("savedForm({answer:String(ACADEMY_LESSONS.find(l=>l.id==='smart').answer),evidence:'Saya memeriksa ruang lingkup, ukuran, bukti kapasitas dan tenggat tujuan saya.'})");
 assert.equal(run("Object.keys(academyProgress().results).length"),1);
 assert.equal(run('data.tasks.length'),0,'Learning must not silently create workload');
 await run("academyCreateLearning('smart')");
 await run("academyCreateLearning('smart')");
 assert.equal(run('data.learning.length'),1);
 assert.equal(run('data.learning[0].nextReview'),'');
 assert.equal(run('data.practiceLogs.length'),0);
 assert.equal(run('data.tasks.length'),0);
 assert.equal(run("assessSmart({due:'2026-02-30'}).checks.T"),false);
 const incomplete=run(`assessSmart({outcome:'Menuntaskan layanan',scope:'Klien izinhukum',metric:'Pekerjaan selesai',unit:'pekerjaan',baseline:'Belum diketahui',target:'Seluruh daftar',source:'Daftar klien',period:'Periode belum ditetapkan',capacity:'',why:'Menjaga layanan',due:''})`);
 assert.equal(incomplete.ready,false);
 assert.equal(incomplete.checks.M,false);
 assert.equal(incomplete.checks.A,false);
 assert.equal(incomplete.checks.T,false);
 assert.equal(run("assessSmart({baseline:'tidak diketahui'}).checks.M"),false);
 assert.ok(incomplete.missing.length>0);
 const draft={outcome:'IZINHUKUM — Menuntaskan daftar layanan',scope:'Daftar yang disepakati',metric:'Pekerjaan yang selesai',unit:'pekerjaan',baseline:'8',target:'8',source:'Daftar layanan',period:'Periode uji',capacity:'Kapasitas dua penanggung jawab dikonfirmasi dari jadwal mereka.',why:'Memenuhi kesepakatan layanan',due:'2026-12-01',area:''};
 ctx.draftFixture=draft;
 assert.equal(run('assessSmart(draftFixture).ready'),true);
 run('smartDraft=structuredClone(draftFixture);smartDraft.goalId=""');
 await run('applySmartGoal()');
 assert.equal(run('data.goals.length'),1);
 assert.equal(run('data.goals[0].baseline'),'8');
 assert.equal(run('data.goals[0].due'),'2026-12-01');
 assert.equal(run('data.tasks.length'),0);
 assert.equal(run('data.goals[0].smartReview.required'),true,'Completeness must not certify feasibility');
 await run('applySmartGoal()');assert.equal(run('data.goals.length'),1,'Repeated apply must update the same explicitly chosen goal');
 run('smartDraft.baseline="Belum diketahui";smartDraft.due=""');
 await run('applySmartGoal()');
 assert.equal(run('data.goals[0].smartReview.status'),'draft');
 assert.equal(run('data.goals[0].due'),'');
 assert.equal(run('data.goals[0].baseline'),'Belum diketahui');
 run('startSmartClinic(data.goals[0].id)');
 assert.equal(run('smartDraft.goalId'),run('data.goals[0].id'));
 assert.ok(node('#modal').innerHTML.includes('Langkah 1 / 5'));
 run('smartDraft.outcome="Draft belum selesai";smartStep=2');
 await run('saveSmartDraft()');
 run('smartDraft=null;startSmartClinic()');
 assert.equal(run('smartDraft.outcome'),'Draft belum selesai');
 assert.equal(run('smartStep'),2);
 const beforeWizard=run('JSON.stringify(data.goals)');
 run('startSmartClinic(data.goals[0].id)');
 const steps=[{outcome:'IZINHUKUM — Tujuan diperjelas',scope:'Cakupan yang disepakati'},
              {metric:'Pekerjaan selesai',unit:'pekerjaan',baseline:'8',target:'8',source:'Daftar layanan',period:'Periode uji'},
              {capacity:'Sumber daya dan kapasitas sudah diperiksa bersama penanggung jawab.'},
              {why:'Memenuhi kesepakatan layanan',area:''},
              {due:'2026-12-01'}];
 for(let i=0;i<steps.length;i++){
  const form=node('#smart-form');form.values=steps[i];
  form.onsubmit({preventDefault(){}});
 }
 assert.equal(run('smartStep'),4);
 assert.ok(node('#modal').innerHTML.includes('Terapkan perumusan'));
 assert.equal(run('JSON.stringify(data.goals)'),beforeWizard,'Wizard preview must not change stored Goal');
 run("startSmartClinic('',false,true)");
 assert.equal(run('smartDraft.goalId'),'');
 assert.equal(run('smartDraft.outcome'),'');
 assert.equal(run('smartStep'),0);
 console.log('Academy regressions passed: nine source-linked lessons, checks/exercises, no automatic workload, SMART unknowns, explicit goal apply/idempotence, draft save/resume and non-certification.');
})().catch(e=>{console.error(e);process.exitCode=1});
