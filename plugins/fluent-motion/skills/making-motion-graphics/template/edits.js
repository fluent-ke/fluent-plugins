// edits.js: the edit kit (recipes in references/edits.md). Loaded before comp.html's script, so a comp can call montage() at its top
// level; the helpers use comp's globals (W, H, FPS, B, b, m, t, ctx, C, E, clamp, lerp, rng, PB, IN, springs, IMG, SHOTS, FR, snap,
// about, quad, masked, zoomBlur, plate, subject) only when called. Every edit is pure in time: it reads t/b and the frame drawn so far, never anything left by an earlier frame.
// Three kinds: wrappers (camera) take a draw function; post edits (punch, shake, flash, leak, grade, letterbox, glitch, tilt3d) act on
// the frame drawn so far, so call them after the scene's drawing; transitions are listed once in TRANS in comp.html.

const cS=c=>toMusic(c)*B;                                   // comp beat → seconds
const fr=c=>(t-cS(c))*FPS;                                  // frames since comp beat c (negative before it)
const inC=k=>k*k*k;                                         // ease-in cubic (comp's E has no inCubic)
function post(draw){const s=snap();ctx.save();ctx.setTransform(1,0,0,1,0,0);ctx.filter='none';ctx.globalAlpha=1;draw(s);ctx.restore()}
function cover(im,s=1,ox=0,oy=0){if(!im)return;const k=Math.max(W/im.width,H/im.height)*s,w=im.width*k,h=im.height*k;ctx.drawImage(im,(W-w)/2+ox,(H-h)/2+oy,w,h)}

// ── Camera: shot sizes and a keyed move. keys = [[beat, size, focusX, focusY, rot], …]; size is a scale or a name.
// Springs between keys (so a new key bends the move under way); the focus point is kept inside the frame; float adds a hand-held drift.
const SIZES={wide:1,medium:1.35,close:1.8,insert:2.6};
function camera(keys,draw,{float=0,z=.85,w=9}={}){
  const K=keys.map(([a,sz,fx=W/2,fy=H/2,r=0])=>[a,typeof sz==='string'?SIZES[sz]:sz,fx,fy,r]),sp=i=>springs(K.map(k=>[k[0],k[i]]),{z,w});
  const s=Math.max(1,sp(1)),hw=W/2/s,hh=H/2/s,fx=clamp(sp(2),hw,W-hw),fy=clamp(sp(3),hh,H-hh);
  const n=(a,p,c,q)=>Math.sin(t*a+p)*.6+Math.sin(t*c+q)*.4,ox=float*n(1.3,.4,2.9,1.7)*6,oy=float*n(1.1,2.2,2.3,.3)*6,g=1+float*.012;
  ctx.save();ctx.translate(W/2+ox,H/2+oy);ctx.rotate(sp(4)+float*n(.9,1,1.7,2)*.004);ctx.scale(s*g,s*g);ctx.translate(-fx,-fy);draw();ctx.restore()}

// ── Post edits on the frame drawn so far
// Punch-in: a hard cut to a tighter frame between beats a and z (a jump-cut reframe). Scaling ≥ 1 about any point never shows an edge.
function punch(a,z,{to=1.15,x=W/2,y=H/2}={}){if(b<a||b>=z)return;post(s=>about(x,y,to,()=>ctx.drawImage(s,0,0)))}
// Shake on an impact: an instant offset decaying over len frames, amp as a share of the width, rot in degrees.
function shake(a,{amp=.03,len=10,rot=1.5,hz=12}={}){const f=fr(a);if(f<0||f>len)return;const d=Math.exp(-f/len*4),ph=f/FPS*hz*TAU;
  post(s=>{ctx.translate(W/2+Math.sin(ph)*amp*W*d,H/2+Math.cos(ph*1.3)*amp*W*.6*d);ctx.rotate(Math.sin(ph*.7)*rot*d*Math.PI/180);ctx.scale(1+amp*2.2,1+amp*2.2);ctx.drawImage(s,-W/2,-H/2)})}
// Flash frame: up frames to near-white, then down frames back. Never more than 3 flashes a second (photosensitivity).
function flash(a,{col='#ebebeb',up=2,down=10,max=1}={}){const f=fr(a)+up;if(f<0||f>up+down)return;
  ctx.save();ctx.setTransform(1,0,0,1,0,0);ctx.globalAlpha=max*(f<up?f/up:1-(f-up)/down);ctx.fillStyle=col;ctx.fillRect(0,0,W,H);ctx.restore()}
// Light leak: warm light drifting across in screen blend for len frames. Once a film.
function leak(a,{len=24,hues=['255,150,60','255,90,40','255,220,150'],seed=7}={}){const f=fr(a);if(f<0||f>len)return;const k=f/len,env=Math.sin(Math.PI*k),r=rng(seed);
  ctx.save();ctx.setTransform(1,0,0,1,0,0);ctx.globalCompositeOperation='screen';
  hues.forEach(h=>{const x=W*(r()*1.4-.2+k*(r()-.3)),y=H*(r()*1.2-.1),R=W*(.5+r()*.6),g=ctx.createRadialGradient(x,y,0,x,y,R);
    g.addColorStop(0,`rgba(${h},${.55*env})`);g.addColorStop(1,`rgba(${h},0)`);ctx.fillStyle=g;ctx.fillRect(0,0,W,H)});ctx.restore()}
// Colour grade for a look: contrast, saturation, brightness, then a tint into the highlights (soft-light) and the shadows (screen).
const LOOKS={'teal-orange':{con:1.08,sat:1.1,hi:'#ffb070',lo:'#0a3a44',amt:.25},'warm-film':{con:1.04,sat:.95,hi:'#ffd9a0',lo:'#2a1a10',amt:.22},
  'cool-night':{con:1.1,sat:.9,hi:'#a0c0ff',lo:'#0a1030',amt:.25},bleach:{con:1.2,sat:.55},mono:{con:1.15,sat:0},punchy:{con:1.12,sat:1.25}};
function grade(look,{amt=1}={}){const g=typeof look==='string'?LOOKS[look]:look;if(!g||amt<=0)return;
  post(s=>{ctx.filter=`contrast(${lerp(1,g.con||1,amt)}) saturate(${lerp(1,g.sat??1,amt)}) brightness(${lerp(1,g.bri||1,amt)})`;ctx.drawImage(s,0,0);ctx.filter='none';
    if(g.hi){ctx.globalCompositeOperation='soft-light';ctx.globalAlpha=(g.amt||.2)*amt;ctx.fillStyle=g.hi;ctx.fillRect(0,0,W,H)}
    if(g.lo){ctx.globalCompositeOperation='screen';ctx.globalAlpha=(g.amt||.2)*.5*amt;ctx.fillStyle=g.lo;ctx.fillRect(0,0,W,H)}})}
// Letterbox bars for a cinematic stretch from beat a to beat z, h as a share of the height for each bar.
function letterbox(a,z,{h=.11,col='#000'}={}){const k=Math.min(IN(a,.5,E.outCubic),1-IN(z-.5,.5,E.outCubic));if(k<=0)return;
  ctx.save();ctx.setTransform(1,0,0,1,0,0);ctx.fillStyle=col;ctx.fillRect(0,0,W,H*h*k);ctx.fillRect(0,H-H*h*k,W,H*h*k);ctx.restore()}
// Glitch burst: len frames of displaced slices and a red/blue split. Two a film at most.
function glitch(a,{len=3,seed=3,amt=1}={}){const f=Math.floor(fr(a));if(f<0||f>=len)return;const r=rng(seed+f*17);
  post(s=>{let y=0;while(y<H){const h=H*(.02+r()*.12),dx=(r()-.5)*W*.25*amt*(r()<.6?1:0);ctx.drawImage(s,0,y,W,h,dx,y,W,h);y+=h}
    const d=ctx.getImageData(0,0,W,H),o=new Uint8ClampedArray(d.data),sh=Math.round(14*amt)*4;
    for(let i=0;i<o.length;i+=4){d.data[i]=o[Math.min(o.length-4,i+sh)];d.data[i+2]=o[Math.max(0,i-sh)+2]}ctx.putImageData(d,0,0)})}
// 3D tilt: the frame swings about its vertical axis by deg degrees from beat a (in over len beats) and back at beat z.
function tilt3d(a,z,{deg=12,len=.6,bg=C.bg}={}){const k=Math.min(IN(a,len,E.outCubic),1-IN(z-len,len,E.inOutCubic));if(k<=0)return;
  const th=deg*k*Math.PI/180,p=W*2.2,P=[[0,0],[W,0],[W,H],[0,H]].map(([x,y])=>{const X=(x-W/2)*Math.cos(th),Z=(x-W/2)*Math.sin(th),s=p/(p+Z)*.94;return[W/2+X*s,H/2+(y-H/2)*s]});
  post(s=>{ctx.fillStyle=bg;ctx.fillRect(0,0,W,H);quad(s,P,10)})}

// ── Footage time: speed ramps and freeze frames live on the shot (SHOTS.X.ramp / SHOTS.X.freeze, read by shotT in comp.html).
// A frozen subject as an outlined sticker: the matte drawn 16 times around the subject in col, then the subject on top.
function sticker(k,{stroke=14,col='#ffffff',sc=1,x=0,y=0}={}){const im=FR['f'+k],mm=FR['m'+k];if(!im||!mm||sc<=0)return;
  lctx.setTransform(1,0,0,1,0,0);lctx.globalCompositeOperation='source-over';lctx.clearRect(0,0,W,H);
  for(let i=0;i<16;i++)lctx.drawImage(mm,Math.cos(i/16*TAU)*stroke,Math.sin(i/16*TAU)*stroke,W,H);
  lctx.globalCompositeOperation='source-in';lctx.fillStyle=col;lctx.fillRect(0,0,W,H);lctx.globalCompositeOperation='source-over';
  fctx.setTransform(1,0,0,1,0,0);fctx.clearRect(0,0,W,H);fctx.drawImage(im,0,0,W,H);fctx.globalCompositeOperation='destination-in';fctx.drawImage(mm,0,0,W,H);fctx.globalCompositeOperation='source-over';
  lctx.drawImage(fx,0,0);ctx.save();ctx.translate(W/2+x,H/2+y);ctx.scale(sc,sc);ctx.drawImage(layer,-W/2,-H/2);ctx.restore()}
// The whole freeze beat: the frame holds (set SHOTS.X.freeze=[[a,len]]), the room dims, the subject pops as a sticker, a label lands.
function freezeCard(k,a,len,{label=null,size=96,y=H*.24,dim=.45,stroke=14,col='#ffffff'}={}){if(b<a||b>=a+len)return;plate(k);
  ctx.save();ctx.fillStyle=`rgba(0,0,0,${dim*IN(a,.25)})`;ctx.fillRect(0,0,W,H);ctx.restore();
  sticker(k,{stroke,col,sc:lerp(1,1.06,springs([[a,0],[a+.05,1]],{z:.55,w:16}))});if(label)words([[label,C.accent]],W/2,y,800,Math.min(size,fit(label,800,W*.84,size)),a+.15,.12)}

// ── Layout edits
// Split screen: n panels (functions that draw a full frame), stacked ('v') or side by side ('h'), sliding in one after another from beat a.
function split(draws,a,{dir='v',gap=10,stagger=.25,col=C.bg}={}){const n=draws.length;ctx.save();ctx.fillStyle=col;ctx.fillRect(0,0,W,H);
  draws.forEach((d,i)=>{const k=IN(a+i*stagger,.5,E.outExpo);if(k<=0)return;const pw=dir==='v'?W:(W-gap*(n-1))/n,ph=dir==='v'?(H-gap*(n-1))/n:H,
      px=dir==='v'?0:i*(pw+gap),py=dir==='v'?i*(ph+gap):0,off=(1-k)*(i%2?1:-1)*(dir==='v'?W:H);
    ctx.save();ctx.beginPath();ctx.rect(px,py,pw,ph);ctx.clip();ctx.translate(px+pw/2-W/2+(dir==='v'?off:0),py+ph/2-H/2+(dir==='v'?0:off));d();ctx.restore()});ctx.restore()}
// A wall of images or frames: items are IMG keys or draw functions, tiles pop in one per stagger beats from beat a.
function grid(items,a,{cols=3,gap=12,stagger=.25,r=18,col=C.bg}={}){const rows=Math.ceil(items.length/cols),tw=(W-gap*(cols+1))/cols,th=(H-gap*(rows+1))/rows;
  ctx.save();ctx.fillStyle=col;ctx.fillRect(0,0,W,H);items.forEach((it,i)=>{const k=springs([[a+i*stagger,0],[a+i*stagger+.01,1]],{z:.7,w:14});if(k<=0)return;
    const x=gap+(i%cols)*(tw+gap),y=gap+Math.floor(i/cols)*(th+gap);ctx.save();ctx.translate(x+tw/2,y+th/2);ctx.scale(k,k);ctx.beginPath();ctx.roundRect(-tw/2,-th/2,tw,th,r);ctx.clip();
    ctx.translate(-W/2,-H/2);const s=Math.max(tw/W,th/H);about(W/2,H/2,s,()=>typeof it==='function'?it():cover(IMG[it]));ctx.restore()});ctx.restore()}
// 2.5D photo: IMG[key] and its matte IMG[key+'_m'] (from segment.swift); the subject moves more than the room, so depth appears.
function parallax(key,a,z,{push=.08,lift=50,blur=2}={}){const im=IMG[key],mm=IMG[key+'_m'];if(!im)return;const k=E.inOutCubic(PB(a,z));
  ctx.save();if(blur)ctx.filter=`blur(${blur*k}px)`;cover(im,1+push*k);ctx.restore();if(!mm)return;
  fctx.setTransform(1,0,0,1,0,0);fctx.clearRect(0,0,W,H);const keep=ctx;ctx=fctx;cover(im,1+push*1.9*k,0,-lift*k);fctx.globalCompositeOperation='destination-in';cover(mm,1+push*1.9*k,0,-lift*k);
  fctx.globalCompositeOperation='source-over';ctx=keep;ctx.drawImage(fx,0,0)}

// ── Montage: shots (SHOTS names, optionally with an in-point in frames: 'LEAP:30') or photos (IMG keys) cut on a beat pattern from
// beat a ('2 1 1 .5 .5 2' = beats per cut; the list repeats when the pattern is longer). Each cut gets its own copy of the shot, starting
// on its cut, so a shot can appear several times. Edits per cut: cut, punch (a reframe 1.14× halfway through), zoom (a fast radial
// settle into the shot), flash, shake; never the same twice running. Call montage() at the comp's top level, draw with MT.draw();
// MT.cuts lists the cut beats: copy the ones that get a hit into soundtrack.mjs.
function montage(list,a,pattern,{edits=['cut','punch','zoom'],push=.05}={}){const lens=pattern.trim().split(/\s+/).map(Number),cuts=[],keys=[];let at=a;
  const ed=[];lens.forEach((l,i)=>{cuts.push(at);const[it,from]=list[i%list.length].split(':');let key=it;
    if(SHOTS[it]){key=`${it}@${i}`;SHOTS[key]={...SHOTS[it],at,dir:SHOTS[it].dir||it,from:+(from||0)}}keys.push(key);
    let e=edits[i%edits.length];if(i&&e===ed[i-1])e=edits[(i+1)%edits.length];ed.push(e);at+=l});
  return{cuts,end:at,draw(){const i=cuts.findLastIndex(c=>b>=c);if(i<0||b>=at)return;const it=keys[i],c=cuts[i],k=PB(c,c+lens[i]);
    if(SHOTS[it])plate(it,1+push*k);else cover(IMG[it],1+push*k);const e=ed[i];
    if(e==='punch'&&k>.45)post(s=>about(W/2,H*.45,1.14,()=>ctx.drawImage(s,0,0)));
    if(e==='flash')flash(c,{down:8,max:.85});if(e==='shake')shake(c,{amp:.025});
    if(e==='zoom'){const f=fr(c);if(f>=0&&f<8)post(s=>{const z=1+.5*(1-f/8)**2;about(W/2,H/2,z,()=>ctx.drawImage(s,0,0));zoomBlur(W/2,H/2,.3*(1-f/8))})}}}}

// ── Transitions: TRANS in comp.html lists [cutBeat, kind, {opts}]. render() calls trans() after the scene is drawn.
// Before the cut the live frame is the outgoing scene; after it, the incoming one. iris and slice also need the outgoing scene's last
// frame, which frameAt() renders off-screen. kinds: cut, whip, flood, iris, slice, zoom, flash, glitch.
const TW={whip:5,flood:9,iris:12,slice:12,zoom:10,flash:10,glitch:3};   // frames each side of the cut (iris and slice: after only)
let held,hctx,inc;
async function frameAt(c){held??=mk();hctx??=held.getContext('2d');const keep=[t,m,b,ctx];b=c;m=toMusic(c);t=m*B;ctx=hctx;await preload();ctx.setTransform(1,0,0,1,0,0);ctx.clearRect(0,0,W,H);scene();ctx.setTransform(1,0,0,1,0,0);if(typeof look==='function')look();
  [t,m,b,ctx]=keep;await preload();return held}
async function trans(){if(typeof TRANS==='undefined')return;for(const[c,kind,o={}]of TRANS){const tc=cS(c),f=(t-tc)*FPS,w=o.len??TW[kind];
  if(kind==='cut'||Math.abs(f)>w)continue;const before=f<0,p=before?1+f/w:f/w,dir=o.dir??1;   // p: 0→1 into the cut, then 0→1 out of it
  if(kind==='whip')post(s=>{const x=before?dir*W*.5*inC(p):-dir*W*.5*(1-E.outCubic(p)),sp=before?p:1-p;
    for(let i=0;i<8;i++){ctx.globalAlpha=i?.35/i:1;const xx=x-dir*i*sp*W*.025;for(const o2 of[-W,0,W])ctx.drawImage(s,xx+o2,0)}});
  if(kind==='flood'){const R=Math.hypot(W,H),[x,y]=before?(o.from??[W/2,H/2]):(o.to??o.from??[W/2,H/2]),r=before?R*inC(p):R*(1-E.outCubic(p));
    ctx.save();ctx.setTransform(1,0,0,1,0,0);ctx.fillStyle=o.col??C.accent;ctx.beginPath();ctx.arc(x,y,r,0,TAU);ctx.fill();ctx.restore()}
  if(kind==='zoom'){const[x,y]=o.at??[W/2,H/2],z=before?1+1.5*inC(p):2.5-1.5*E.outCubic(p),bl=.35*(before?p:1-p);
    post(s=>about(x,y,z,()=>ctx.drawImage(s,0,0)));zoomBlur(x,y,bl)}
  if(kind==='flash'&&!before)flash(c,{up:0,down:w});
  if(kind==='flash'&&before&&f>-2)flash(c,{up:2,down:0});
  if(kind==='glitch')glitch(toComp((tc-w/FPS)/B),{len:w*2,seed:o.seed??5});
  if((kind==='iris'||kind==='slice')&&!before){inc??=mk();const ic=inc.getContext('2d');ic.clearRect(0,0,W,H);ic.drawImage(ctx.canvas,0,0);const B2=inc,A=await frameAt(c-.001);ctx.save();ctx.setTransform(1,0,0,1,0,0);ctx.drawImage(A,0,0);
    if(kind==='iris'){const[x,y]=o.at??[W/2,H/2],r=Math.hypot(W,H)*E.inOutCubic(p);ctx.beginPath();ctx.arc(x,y,r,0,TAU);ctx.clip();ctx.drawImage(B2,0,0)}
    else{const n=o.n??5,bh=H/n;for(let i=0;i<n;i++){const q=E.outExpo(clamp(p*1.6-i*.12));ctx.save();ctx.beginPath();ctx.rect(0,i*bh,W,bh+1);ctx.clip();
      ctx.drawImage(B2,(i%2?1:-1)*W*(1-q),0);ctx.restore()}}ctx.restore()}}}

// ── Guardrails, checked once the comp has loaded (render.mjs prints them): no transition kind twice running, at most 3 of a kind
// per 30 s, at most 2 glitches. Flash rate is the author's to keep under 3 a second.
addEventListener('DOMContentLoaded',()=>{if(typeof TRANS==='undefined')return;const T=[...TRANS].sort((x,y)=>x[0]-y[0]);
  T.forEach(([c,k],i)=>{if(i&&k!=='cut'&&k===T[i-1][1])console.warn(`⚠ transition ${k} twice running (beats ${T[i-1][0]} and ${c}): vary it`);
    const near=T.filter(([c2,k2])=>k2===k&&k!=='cut'&&Math.abs(cS(c2)-cS(c))<=15).length;if(near>3)console.warn(`⚠ ${near} ${k} transitions within 30 s around beat ${c}: at most 3`)});
  if(T.filter(([,k])=>k==='glitch').length>2)console.warn('⚠ more than 2 glitch transitions: glitch wears out fast')});
