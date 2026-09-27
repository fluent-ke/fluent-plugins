// node render.mjs                         → out/video-only.mp4 (then ./mix.sh adds the audio)
// node render.mjs stills 0.5 3 b8.5      → stills/0.5s.png, stills/3s.png, stills/b8.5.png (seconds, or bN = comp beat N)
// node render.mjs --query "day=TODAY" --out video-only-today.mp4   → a variant; comp.html reads it from Q
import {chromium} from 'playwright';
import {spawn} from 'node:child_process';
import {createServer} from 'node:http';
import {readFile, mkdir, writeFile} from 'node:fs/promises';
import {extname} from 'node:path';
const dir=new URL('.', import.meta.url).pathname, args=process.argv.slice(2);
const opt=k=>{const i=args.indexOf(k);return i<0?null:args.splice(i,2)[1]};
const query=opt('--query'), out=opt('--out')||'video-only.mp4';
const types={'.html':'text/html','.js':'text/javascript','.css':'text/css','.jpg':'image/jpeg','.png':'image/png','.webp':'image/webp','.svg':'image/svg+xml','.ttf':'font/ttf','.otf':'font/otf','.woff2':'font/woff2','.woff':'font/woff'};
// Strip the query string before touching the disk: variants pass ?key=value to comp.html
const srv=createServer(async(q,r)=>{const p=decodeURIComponent(q.url.split('?')[0].slice(1));
  try{const b=await readFile(dir+p);r.writeHead(200,{'content-type':types[extname(p).toLowerCase()]||'application/octet-stream'});r.end(b)}catch{r.writeHead(404);r.end()}}).listen(0);
const browser=await chromium.launch();
const page=await browser.newPage();
page.on('pageerror',e=>{console.error('comp.html error:',e.message);process.exitCode=1});
await page.goto(`http://localhost:${srv.address().port}/comp.html${query?'?'+query:''}`);
if(!await page.evaluate(()=>window.ready)) throw new Error('assets failed to load');
const {W,H,FPS,DUR}=await page.evaluate(()=>window.CONFIG);
await page.setViewportSize({width:W,height:H});
const grab=t=>page.evaluate(async t=>{await render(t);return document.getElementById('c').toDataURL('image/png').split(',')[1]},t);
if(args[0]==='stills'){
  const {rm}=await import('node:fs/promises');await rm(dir+'stills',{recursive:true,force:true});await mkdir(dir+'stills',{recursive:true});
  for(const a of args.slice(1)){
    const sec=a.startsWith('b')?await page.evaluate(c=>toMusic(c)*60/BPM,+a.slice(1)):+a;
    if(!Number.isFinite(sec)||sec<0||sec>DUR) throw new Error(`still "${a}" is outside the film (0–${DUR.toFixed(2)} s). Pass seconds, or bN for comp beat N, one per argument.`);
    await writeFile(`${dir}stills/${a.startsWith('b')?a:a+'s'}.png`,Buffer.from(await grab(sec),'base64'));}
  console.log(`stills → ${dir}stills/ (film is ${DUR.toFixed(2)} s)`);
}else{
  await mkdir(dir+'out',{recursive:true});
  const N=Math.round(DUR*FPS);
  const ff=spawn('ffmpeg',['-y','-loglevel','error','-f','image2pipe','-framerate',String(FPS),'-c:v','png','-i','-',
    '-c:v','libx264','-preset','slow','-crf','16','-pix_fmt','yuv420p',dir+'out/'+out],{stdio:['pipe','inherit','inherit']});
  for(let f=0;f<N;f++){
    if(!ff.stdin.write(Buffer.from(await grab(f/FPS),'base64'))) await new Promise(r=>ff.stdin.once('drain',r));
    if(f%60===0) console.log(`frame ${f}/${N}`);
  }
  ff.stdin.end(); await new Promise(r=>ff.on('close',r));
  console.log(`→ out/${out} (${N} frames, ${DUR.toFixed(2)} s)`);
}
await browser.close(); srv.close();
