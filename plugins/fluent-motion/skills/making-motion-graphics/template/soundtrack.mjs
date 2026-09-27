// node soundtrack.mjs → score.wav, an original score synthesised to the film's timeline (no samples, no licences).
// Cues are placed in MUSIC beats; M(c) converts a comp beat from comp.html so every hit lands on its cut.
// STYLE picks the groove: 'afrohouse' (warm, 118–124 BPM), 'amapiano' (log drum, 108–114 BPM), 'ambient' (no drums, corporate/calm).
import {writeFileSync} from 'node:fs';
import './timeline.js';
const {toMusic,MUSIC_BEATS,BPM}=globalThis;
const STYLE='afrohouse';
const SR=44100,B=60/BPM,DUR=MUSIC_BEATS*B+1.2,N=Math.ceil(SR*DUR),TAU=Math.PI*2,S16=B/4,SW=.12;   // SW: 16th swing
const L=new Float32Array(N),R=new Float32Array(N),PL=new Float32Array(N),PR=new Float32Array(N),WET=new Float32Array(N);
let seed=5;const noise=()=>((seed=(seed*16807)%2147483647)/2147483647)*2-1;
const hz=n=>440*2**((n-69)/12), T=b=>b*B, M=c=>toMusic(c);
// add(): one voice into the dry or sidechained ("pump") bus, with a reverb send
function add(t0,len,fn,g=1,pan=0,send=0,pump=false){const s0=Math.round(t0*SR),gl=g*Math.cos((pan+1)*Math.PI/4)*1.414,gr=g*Math.sin((pan+1)*Math.PI/4)*1.414;
  const [a,c]=pump?[PL,PR]:[L,R];for(let i=0;i<len*SR;i++){const j=s0+i;if(j<0||j>=N)continue;const v=fn(i/SR);a[j]+=v*gl;c[j]+=v*gr;WET[j]+=v*g*send}}
const hp=()=>{let lp=0;return (x,k=.25)=>{lp+=k*(x-lp);return x-lp}};

// ── Drums
const KICKS=[];
const kick=(t,g=.8)=>{KICKS.push(t);add(t,.45,x=>Math.tanh(1.4*Math.sin(TAU*(46*x+104*(1-Math.exp(-x*30))/30)))*Math.exp(-x*9.5)+(x<.004?noise()*.5*(1-x/.004):0),g)};
const clap=(t,g=.28)=>{const f=hp();add(t,.35,x=>{const e=[0,.009,.02].reduce((a,d)=>a+(x>=d?Math.exp(-(x-d)*(x-d<.015?140:18)):0),0);return f(noise(),.35)*e*.7},g,.05,.3)};
const ohat=(t,g=.13)=>{const f=hp();add(t,.22,x=>f(noise(),.6)*Math.exp(-x*16),g,.2,.08)};
const shaker=(t,g)=>{const f=hp();add(t,.06,x=>f(noise(),.7)*Math.exp(-x*70)*Math.min(1,x*900),g,-.3,.05)};
const conga=(t,f0,g=.16,pan=.35)=>add(t,.25,x=>Math.sin(TAU*(f0*x+f0*.6*(1-Math.exp(-x*40))/40))*Math.exp(-x*16)+(x<.003?noise()*.3:0),g,pan,.18);
const rim=(t,g=.1)=>add(t,.05,x=>Math.sin(TAU*1700*x)*Math.exp(-x*120),g,-.45,.2);
const logdrum=(t,n,g=.5,len=.45)=>add(t,len,x=>{const f=hz(n),ph=TAU*(f*x+f*1.2*(1-Math.exp(-x*38))/38);return Math.tanh(2.8*(Math.sin(ph)+.3*Math.sin(2*ph)))*Math.exp(-x*(4.5/len))*Math.min(1,x*600)},g,0,.05);

// ── Harmony: one chord per bar of 4 music beats. Default A minor: Am9 | Fmaj9 | Dm9 | Em7(add11). r = bass root (MIDI).
const CH=[{r:45,c:[57,60,64,67,71]},{r:41,c:[57,60,64,65,67]},{r:38,c:[57,60,62,65,69]},{r:40,c:[55,59,62,64,69]}];
const chordAt=b=>CH[Math.floor(b/4)%4];
const bass=(t,n,len,g=.34)=>add(t,len,x=>{const f=hz(n);return Math.tanh(1.5*(Math.sin(TAU*f*x)+.25*Math.sin(TAU*2*f*x)))*Math.min(1,x*200)*Math.min(1,(len-x)*40)},g,0,0,true);
// Warm pad: detuned saws through a two-pole lowpass; cut(x) is the cutoff in Hz over the note's life
function pad(t,notes,len,cut,g=.048){const st=notes.map(()=>[0,0]);
  add(t,len,x=>{let v=0;notes.forEach((n,i)=>{const f=hz(n);let s=0;for(const d of[-.004,0,.0045])s+=((x*f*(1+d)+i*.37)%1)*2-1;
    const k=1-Math.exp(-TAU*cut(x)/SR),q=st[i];q[0]+=k*(s-q[0]);q[1]+=k*(q[0]-q[1]);v+=q[1]});
    return v*Math.min(1,x/.08)*Math.min(1,(len-x)/.15)},g,0,.35,true)}
const mar=(t,n,g=.1,pan=0)=>add(t,.7,x=>{const f=hz(n);return (Math.sin(TAU*f*x)+.35*Math.sin(TAU*4*f*x)*Math.exp(-x*30))*Math.exp(-x*6)*Math.min(1,x*2000)},g,pan,.3);
const stab=(t,ns,g=.09,len=.45)=>pad(t,ns,len,x=>3200*Math.exp(-x*5)+300,g*1.8);

// ── FX: put a revCrash + impact on every scene cut, a riser before every reveal
const riser=(t,len,g=.28)=>{let lp=0;add(t,len,x=>{const k=x/len;lp+=(.01+.35*k*k)*(noise()-lp);return (lp*2.2+.25*Math.sin(TAU*(180+1400*k*k)*x))*k*k},g,0,.45)};
const down=(t,len=1,g=.22)=>{let lp=0;add(t,len,x=>{const k=x/len;lp+=(.4*(1-k)+.01)*(noise()-lp);return lp*(1-k)**2*2},g,0,.5)};
const impact=(t,g=.7)=>{add(t,2,x=>Math.sin(TAU*(30*x+50*(1-Math.exp(-x*5))/5))*Math.exp(-x*2),g,0,.15);down(t,1.4,g*.45)};
const crash=(t,g=.14)=>{const f=hp();add(t,2.2,x=>f(noise(),.5)*Math.exp(-x*2.2),g,.15,.5)};
const revCrash=(t,len=1,g=.12)=>{const f=hp();add(t-len,len,x=>f(noise(),.5)*(x/len)**3,g,-.15,.3)};
const tick=(t,g=.12)=>add(t,.04,x=>Math.sin(TAU*2600*x)*Math.exp(-x*150),g,.3,.4);

// ── Groove between two music beats, on one global 16th grid so cuts never land off-beat. Options thin it for quiet scenes.
function groove(from,to,{k=true,cl=true,hh=true,sh=true,cg=true,bs=true,pd=true,arp=false,cut=1400}={}){
  const drums=STYLE!=='ambient';
  for(let gi=Math.ceil(from*4-1e-6);gi<Math.round(to*4);gi++){const s=gi%16,ch=chordAt(gi/4),t=T(gi/4)+(gi%2?S16*SW:0);
    if(drums&&k&&s%4===0)kick(t);
    if(drums&&cl&&s%8===4)clap(t);
    if(drums&&hh&&s%4===2)ohat(t);
    if(drums&&sh)shaker(t,s%4===2?.05:s%2?.07:.035);
    if(STYLE==='afrohouse'){if(cg&&[3,6,10,11,14].includes(s))conga(t,[3,11].includes(s)?330:220,.16,s%2?.4:-.35);if(cg&&s===7)rim(t);
      if(bs&&[2,6,10,13,14].includes(s))bass(t,ch.r+(s===13?12:0)+(s===14?7:0),S16*(s===13?.9:1.7));}
    if(STYLE==='amapiano'&&bs&&[0,3,6,10,11,14].includes(s))logdrum(t,ch.r+[0,0,7,0,12,10][[0,3,6,10,11,14].indexOf(s)],.45,s===11?.25:.45);
    if(STYLE==='ambient'&&bs&&s===0)bass(t,ch.r,B*3.8,.22);
    if((arp||STYLE==='ambient')&&s%2===0)mar(t,ch.c[[0,2,4,1,3,2,4,3][(s/2)%8]]+12,.08,(s/2)%2?.3:-.3);}
  if(pd)for(let bb=Math.floor(from/4)*4;bb<to;bb+=4){const a=Math.max(bb,from),z=Math.min(bb+4,to);if(z-a>.05)pad(T(a),chordAt(bb).c,(z-a)*B+.05,()=>cut,.048)}
}

// ── Cue sheet: mirror comp.html's scenes. Write every time as M(comp beat).
// S1 kinetic words: a stab + kick per word, slam on the last
[0,1,2].forEach(i=>{stab(T(M(i)),CH[0].c.map(n=>n+[0,3,5][i]));kick(T(M(i)),.7);tick(T(M(i))+.01)});
riser(T(M(1.5)),T(M(3)-M(1.5)),.22);revCrash(T(M(3)),T(1));impact(T(M(3)),.8);stab(T(M(3)),CH[3].c,.1,.8);
// S2 reading scene: groove with the filter half open, marimba arp under the text
revCrash(T(M(4)),T(1));crash(T(M(4)),.12);groove(M(4),M(8),{arp:true,cut:1300});
[5.5,5.9].forEach((c,i)=>mar(T(M(c)),[81,84][i],.1));
// S3 the number: drums drop out, riser into the landing, then full groove
revCrash(T(M(8)),T(.8));groove(M(8),M(9.5),{k:false,cl:false,hh:false,bs:false,cg:false,cut:700});
riser(T(M(8.2)),T(M(9.5)-M(8.2)),.32);impact(T(M(9.5)),.85);crash(T(M(9.5)),.18);groove(M(9.5),M(12),{cut:2600});
// S4 end card: full groove, final hit on the last bar
revCrash(T(M(12)),T(1));impact(T(M(12)),.7);groove(M(12),M(15),{cut:3000,arp:true});
kick(T(M(15)));impact(T(M(15)),.6);crash(T(M(15)),.16);pad(T(M(15)),CH[0].c,2.2,x=>2600*Math.exp(-x*1.2)+300,.06);bass(T(M(15)),33,1.4,.3);

// ── Reverb, kick-keyed sidechain, master
function verb(x,off){const combs=[1557,1617,1491,1422,1277,1356].map(d=>({d:d+off,b:new Float32Array(d+off),i:0,lp:0}));
  const aps=[556,441,341].map(d=>({d:d+off,b:new Float32Array(d+off),i:0}));const y=new Float32Array(N);
  for(let n=0;n<N;n++){let s=0;const inp=x[n]*.2;
    for(const c of combs){const o=c.b[c.i];c.lp=o*.6+c.lp*.4;c.b[c.i]=inp+c.lp*.84;c.i=(c.i+1)%c.d;s+=o}
    for(const a of aps){const bo=a.b[a.i],v=-s+bo;a.b[a.i]=s+bo*.5;a.i=(a.i+1)%a.d;s=v}y[n]=s}return y}
const wl=verb(WET,0),wr=verb(WET,23);
const duck=new Float32Array(N).fill(1);
for(const t of KICKS){const s0=Math.round(t*SR);for(let i=0;i<.3*SR;i++){const j=s0+i;if(j<N)duck[j]=Math.min(duck[j],1-.7*Math.exp(-i/SR*14))}}
const OL=new Float32Array(N),OR=new Float32Array(N);let pk=0;
for(let n=0;n<N;n++){OL[n]=Math.tanh((L[n]+PL[n]*duck[n]+wl[n]*.4)*1.1);OR[n]=Math.tanh((R[n]+PR[n]*duck[n]+wr[n]*.4)*1.1);pk=Math.max(pk,Math.abs(OL[n]),Math.abs(OR[n]))}
const buf=Buffer.alloc(44+N*4);buf.write('RIFF',0);buf.writeUInt32LE(36+N*4,4);buf.write('WAVEfmt ',8);buf.writeUInt32LE(16,16);buf.writeUInt16LE(1,20);buf.writeUInt16LE(2,22);
buf.writeUInt32LE(SR,24);buf.writeUInt32LE(SR*4,28);buf.writeUInt16LE(4,32);buf.writeUInt16LE(16,34);buf.write('data',36);buf.writeUInt32LE(N*4,40);
for(let n=0;n<N;n++){const f=Math.min(1,(DUR-n/SR)/1)*.9/pk;buf.writeInt16LE(Math.round(OL[n]*f*32767),44+n*4);buf.writeInt16LE(Math.round(OR[n]*f*32767),46+n*4)}
writeFileSync(new URL('score.wav',import.meta.url),buf);
console.log(`score.wav ${DUR.toFixed(2)} s, ${STYLE} at ${BPM} BPM`);
