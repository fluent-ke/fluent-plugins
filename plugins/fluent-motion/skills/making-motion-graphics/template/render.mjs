// node render.mjs                         → out/video-only.mp4 (then ./mix.sh adds the audio)
// node render.mjs stills 0.5 3 b8.5      → stills/0.5s.png, stills/3s.png, stills/b8.5.png (seconds, or bN = comp beat N)
// node render.mjs --query "day=TODAY" --out video-only-today.mp4   → a variant; comp.html reads it from Q
// node render.mjs --draft                 → half size with score.wav muxed in, to check timing against the music (out/draft.mp4)
// Options: --workers N (default: performance cores, max 6)   --png (lossless frame capture, slower)
// render(t) is pure, so the film is split into N ranges rendered by N browser pages at once, each encoded to its own chunk,
// then the chunks are joined without re-encoding. Frames are captured as JPEG q0.95 (4–5× cheaper than PNG deflate).
import {chromium} from 'playwright';
import {spawn, execFileSync} from 'node:child_process';
import {createServer} from 'node:http';
import {readFile, mkdir, writeFile, rm} from 'node:fs/promises';
import {extname} from 'node:path';
import os from 'node:os';
const dir=new URL('.', import.meta.url).pathname, args=process.argv.slice(2);
const opt=k=>{const i=args.indexOf(k);return i<0?null:args.splice(i,2)[1]};
const flag=k=>{const i=args.indexOf(k);return i<0?false:(args.splice(i,1),true)};
const draft=flag('--draft'), png=flag('--png');
const query=opt('--query'), out=opt('--out')||(draft?'draft.mp4':'video-only.mp4');
let perf=4;try{perf=+execFileSync('sysctl',['-n','hw.perflevel0.physicalcpu']).toString()||4}catch{perf=Math.max(2,os.cpus().length>>1)}
const WORKERS=Math.max(1,+(opt('--workers')||Math.min(6,perf)));
const types={'.html':'text/html','.js':'text/javascript','.css':'text/css','.jpg':'image/jpeg','.png':'image/png','.webp':'image/webp','.svg':'image/svg+xml','.ttf':'font/ttf','.otf':'font/otf','.woff2':'font/woff2','.woff':'font/woff'};
const srv=createServer(async(q,r)=>{const p=decodeURIComponent(q.url.split('?')[0].slice(1));
  try{const b=await readFile(dir+p);r.writeHead(200,{'content-type':types[extname(p).toLowerCase()]||'application/octet-stream','cache-control':'max-age=3600'});r.end(b)}catch{r.writeHead(404);r.end()}}).listen(0);
const url=`http://localhost:${srv.address().port}/comp.html${query?'?'+query:''}`;
const browser=await chromium.launch();
async function open(){const page=await browser.newPage();
  page.on('pageerror',e=>{console.error('comp.html error:',e.message);process.exitCode=1});
  await page.goto(url);if(!await page.evaluate(()=>window.ready)) throw new Error('assets failed to load');
  const cfg=await page.evaluate(()=>window.CONFIG);await page.setViewportSize({width:cfg.W,height:cfg.H});return [page,cfg]}
const grab=(page,t,fmt)=>page.evaluate(async([t,fmt,draft])=>{await render(t);const c=document.getElementById('c');
  let src=c;if(draft){src=window.__half||(window.__half=Object.assign(document.createElement('canvas'),{width:c.width>>1,height:c.height>>1}));
    src.getContext('2d').drawImage(c,0,0,src.width,src.height)}
  return src.toDataURL(fmt==='png'?'image/png':'image/jpeg',.95).split(',')[1]},[t,fmt,draft]);
// Encode settings shared by every chunk (identical flags are what lets the concat skip re-encoding).
// Colour: convert to BT.709 limited range explicitly and tag it, so Instagram/TikTok don't shift the hues.
const encode=(file,fps)=>['-y','-loglevel','error','-f','image2pipe','-framerate',String(fps),'-c:v',png?'png':'mjpeg','-i','-',
  '-vf','scale=out_color_matrix=bt709:out_range=tv,format=yuv420p','-c:v','libx264','-preset',draft?'veryfast':'slow','-crf',draft?'23':'16',
  '-profile:v','high','-colorspace','bt709','-color_primaries','bt709','-color_trc','bt709','-color_range','tv','-movflags','+faststart',file];

const [page0,{W,H,FPS,DUR}]=await open();
if(args[0]==='stills'){
  await rm(dir+'stills',{recursive:true,force:true});await mkdir(dir+'stills',{recursive:true});
  for(const a of args.slice(1)){
    const sec=a.startsWith('b')?await page0.evaluate(c=>toMusic(c)*60/BPM,+a.slice(1)):+a;
    if(!Number.isFinite(sec)||sec<0||sec>DUR) throw new Error(`still "${a}" is outside the film (0–${DUR.toFixed(2)} s). Pass seconds, or bN for comp beat N, one per argument.`);
    await writeFile(`${dir}stills/${a.startsWith('b')?a:a+'s'}.png`,Buffer.from(await grab(page0,sec,'png'),'base64'));}
  console.log(`stills → ${dir}stills/ (film is ${DUR.toFixed(2)} s)`);
}else{
  const t0=Date.now(),N=Math.round(DUR*FPS),K=Math.min(WORKERS,Math.ceil(N/30)),per=Math.ceil(N/K),tmp=dir+'out/.chunks/';
  await rm(tmp,{recursive:true,force:true});await mkdir(tmp,{recursive:true});
  const pages=[page0,...await Promise.all(Array.from({length:K-1},()=>open().then(([p])=>p)))];
  let done=0;
  await Promise.all(pages.map(async(page,k)=>{const a=k*per,z=Math.min(N,a+per);if(a>=z)return;
    const ff=spawn('ffmpeg',encode(`${tmp}${String(k).padStart(2,'0')}.mp4`,FPS),{stdio:['pipe','inherit','inherit']});
    let next=grab(page,a/FPS,png?'png':'jpg');                       // capture frame f+1 while frame f is written
    for(let f=a;f<z;f++){const b64=await next;if(f+1<z)next=grab(page,(f+1)/FPS,png?'png':'jpg');
      if(!ff.stdin.write(Buffer.from(b64,'base64'))) await new Promise(r=>ff.stdin.once('drain',r));
      if(++done%120===0) console.log(`frame ${done}/${N}`)}
    ff.stdin.end();await new Promise((r,j)=>ff.on('close',c=>c?j(new Error('ffmpeg chunk '+k+' failed')):r()))}));
  await writeFile(tmp+'list.txt',pages.map((_,k)=>`file '${String(k).padStart(2,'0')}.mp4'`).join('\n'));
  execFileSync('ffmpeg',['-y','-loglevel','error','-f','concat','-safe','0','-i',tmp+'list.txt','-c','copy','-movflags','+faststart',dir+'out/'+out]);
  if(draft){const {existsSync}=await import('node:fs');if(existsSync(dir+'score.wav')){   // a draft is for checking timing against the score: give it the sound
    execFileSync('ffmpeg',['-y','-loglevel','error','-i',dir+'out/'+out,'-i',dir+'score.wav','-map','0:v','-map','1:a','-c:v','copy','-c:a','aac','-b:a','160k','-shortest',tmp+'d.mp4']);
    execFileSync('mv',[tmp+'d.mp4',dir+'out/'+out])}}
  await rm(tmp,{recursive:true,force:true});
  console.log(`→ out/${out} (${N} frames, ${DUR.toFixed(2)} s) in ${((Date.now()-t0)/1000).toFixed(1)} s with ${K} workers${draft?' (draft, half size)':''}`);
}
await browser.close(); srv.close();
