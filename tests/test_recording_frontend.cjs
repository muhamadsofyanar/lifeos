const assert=require('node:assert/strict'),fs=require('node:fs'),vm=require('node:vm');
const nodes=new Map();const node=s=>{if(!nodes.has(s))nodes.set(s,{innerHTML:'',textContent:'',open:false,dataset:{juz:'29'},showModal(){this.open=true},close(){this.open=false},classList:{add(){},remove(){}}});return nodes.get(s)};
let stopped=0,uploadCount=0;
class Recorder{static isTypeSupported(t){return t==='audio/mp4'}constructor(stream,opts){this.mimeType=opts.mimeType;this.state='inactive'}start(){this.state='recording'}stop(){this.state='inactive';this.ondataavailable?.({data:new Blob([new Uint8Array([0,0,0,16,102,116,121,112,77,52,65,32,0,0,0,0])],{type:this.mimeType})});this.onstop?.()}}
const ctx=vm.createContext({console,structuredClone,crypto:require('node:crypto').webcrypto,Date,URL,Blob,MediaRecorder:Recorder,isSecureContext:true,navigator:{mediaDevices:{getUserMedia:async()=>({getTracks:()=>[{stop(){stopped++}}]})}},document:{querySelector:node,addEventListener(){}},setInterval:()=>1,setTimeout:()=>1,clearInterval(){},clearTimeout(){},confirm:()=>true,FormData:class{},fetch:async(path,request)=>{assert.equal(path,'/api/recordings');assert.equal(request.method,'POST');assert.ok(request.body instanceof Blob);assert.equal(JSON.parse(decodeURIComponent(request.headers['X-Recording-Metadata'])).juz,29);uploadCount++;return {ok:true,json:async()=>({id:'id',created:true})}}});
for(const f of ['app','features','hifz','wellbeing','recordings'])vm.runInContext(fs.readFileSync(`static/${f}.js`,'utf8'),ctx);
vm.runInContext(`data=normalizeClient(Object.fromEntries(['inbox','tasks','projects','notes','events','sessions','reviews','areas','goals'].map(k=>[k,[]])));csrf='token';hifzJuz=29;render=()=>{};recordingMetadata=()=>({title:'Test',date:'2026-11-01',juz:29,target:'Al-Mulk 1–2',duration:1});api=async()=>({recordings:[]});`,ctx);
(async()=>{
 vm.runInContext('recordingDialog()',ctx);
 await vm.runInContext('beginRecording()',ctx);
 assert.equal(vm.runInContext('recordingActive()',ctx),true);
 vm.runInContext('finishRecording()',ctx);
 assert.equal(stopped,1,'Mic track must stop after recording');
 assert.equal(vm.runInContext('rec.blob.size>0',ctx),true);
 assert.ok(node('#audio-preview').innerHTML.includes('draft-player'));
 await vm.runInContext('saveRecording()',ctx);
 assert.equal(uploadCount,1);assert.equal(vm.runInContext('rec.blob',ctx),null);assert.equal(vm.runInContext('rec.dialog',ctx),false);
 // Permission denied: error is understandable and UI returns to an idle state.
 vm.runInContext("recordingDialog();navigator.mediaDevices.getUserMedia=async()=>{throw {name:'NotAllowedError'}}",ctx);
 await vm.runInContext('beginRecording()',ctx);
 assert.equal(vm.runInContext('recordingActive()',ctx),false);assert.ok(node('#rec-message').textContent.includes('Izin mikrofon ditolak'));
 // Upload failure keeps the draft and offers retry/download instead of losing audio.
 vm.runInContext("rec.blob=new Blob(['draft audio'],{type:'audio/webm'});fetch=async()=>({ok:false,json:async()=>({error:'Gagal menyimpan'})})",ctx);
 await vm.runInContext('saveRecording()',ctx);
 assert.equal(vm.runInContext('rec.blob.size',ctx),11);assert.ok(node('#rec-message').textContent.includes('tetap tersedia'));
 vm.runInContext('releaseRecording(true)',ctx);
 console.log('Recorder simulation passed: format selection, stop mic, preview, upload, denial and failed-upload draft preservation.');
})().catch(e=>{console.error(e);process.exitCode=1});
