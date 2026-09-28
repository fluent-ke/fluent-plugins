// node soundtrack.mjs → score.wav, an original score synthesised to the film's timeline (no samples, no licences).
// Cues are placed in MUSIC beats; M(c) converts a comp beat from comp.html so every hit lands on its cut.
// STYLE picks the groove: 'afrohouse' (warm, 118–124 BPM), 'amapiano' (log drum, 108–114 BPM), 'benga' (Kenyan: plucked guitars in
// interlocking 16ths, a walking bass, house kick; 118–128 BPM, major key), 'drill' (Nairobi drill: half-time drums, triplet hat rolls,
// sliding 808s, a buzzy nyatiti-like lyre riff, brass stabs; minor key, 118–144 BPM), 'ambient' (no drums, corporate/calm; 80–100 BPM).
// Every film gets its own music: this script logs STYLE/KEY/BPM to ../score-log.tsv and warns when the brand's recent films used the same style.
// KEY transposes the whole score in semitones (-5…+6), so even a style used before sounds new.
import {writeFileSync,readFileSync,existsSync} from 'node:fs';
import './timeline.js';
const {toMusic,MUSIC_BEATS,BPM}=globalThis;
const STYLE='afrohouse';
const KEY=0;
const SR=44100,B=60/BPM,DUR=MUSIC_BEATS*B+1.2,N=Math.ceil(SR*DUR),TAU=Math.PI*2,S16=B/4,SW=STYLE==='drill'?0:.12;   // SW: 16th swing (drill stays straight)
const L=new Float32Array(N),R=new Float32Array(N),PL=new Float32Array(N),PR=new Float32Array(N),WET=new Float32Array(N);
let seed=5;const noise=()=>((seed=(seed*16807)%2147483647)/2147483647)*2-1;
const hz=n=>440*2**((n+KEY-69)/12), T=b=>b*B, M=c=>toMusic(c);   // KEY transposes every pitched voice
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
const CH=STYLE==='drill'
  ? [{r:28,c:[52,55,59,62,67]},{r:24,c:[52,55,59,60,64]},{r:21,c:[52,57,60,64,69]},{r:23,c:[51,54,57,59,63]}]   // Em | Cmaj7 | Am | B7: dark, with a pull
  : STYLE==='benga'
  ? [{r:38,c:[62,66,69,73,76]},{r:35,c:[59,62,66,69,74]},{r:31,c:[59,62,67,71,74]},{r:33,c:[57,61,64,67,71]}]   // D | Bm | G | A: benga is bright and major
  : [{r:45,c:[57,60,64,67,71]},{r:41,c:[57,60,64,65,67]},{r:38,c:[57,60,62,65,69]},{r:40,c:[55,59,62,64,69]}];
const chordAt=b=>CH[Math.floor(b/4)%4];
const bass=(t,n,len,g=.34)=>add(t,len,x=>{const f=hz(n);return Math.tanh(1.5*(Math.sin(TAU*f*x)+.25*Math.sin(TAU*2*f*x)))*Math.min(1,x*200)*Math.min(1,(len-x)*40)},g,0,0,true);
// Warm pad: detuned saws through a two-pole lowpass; cut(x) is the cutoff in Hz over the note's life
function pad(t,notes,len,cut,g=.048){const st=notes.map(()=>[0,0]);
  add(t,len,x=>{let v=0;notes.forEach((n,i)=>{const f=hz(n);let s=0;for(const d of[-.004,0,.0045])s+=((x*f*(1+d)+i*.37)%1)*2-1;
    const k=1-Math.exp(-TAU*cut(x)/SR),q=st[i];q[0]+=k*(s-q[0]);q[1]+=k*(q[0]-q[1]);v+=q[1]});
    return v*Math.min(1,x/.08)*Math.min(1,(len-x)/.15)},g,0,.35,true)}
const mar=(t,n,g=.1,pan=0)=>add(t,.7,x=>{const f=hz(n);return (Math.sin(TAU*f*x)+.35*Math.sin(TAU*4*f*x)*Math.exp(-x*30))*Math.exp(-x*6)*Math.min(1,x*2000)},g,pan,.3);
const stab=(t,ns,g=.09,len=.45)=>pad(t,ns,len,x=>3200*Math.exp(-x*5)+300,g*1.8);
// Plucked string (Karplus-Strong): a burst of filtered noise in a delay line tuned to the note, damped a little each pass.
// bright 0..1 = pick brightness; mute = short palm-muted decay. Good for benga/soukous guitars, kora-like and lyre-like lines.
function pluck(t,n,g=.12,pan=0,{bright=.7,mute=false,len=null}={}){
  const f=hz(n),P=Math.max(2,Math.round(SR/f)),buf=new Float32Array(P);let lp=0;
  for(let i=0;i<P;i++){lp+=bright*(noise()-lp);buf[i]=lp}
  const damp=mute?.955:.996,L2=len??(mute?.22:1.1);let i=0,body=0;
  add(t,L2,x=>{const j=i%P,v=buf[j];buf[j]=(v+buf[(j+1)%P])*.5*damp;i++;body+=.18*(v-body);return (v*.8+body*.6)*Math.min(1,(L2-x)*25)},g,pan,.22,true)}
const snare=(t,g=.14)=>{const f=hp();add(t,.2,x=>(f(noise(),.45)*.8+.35*Math.sin(TAU*190*x)*Math.exp(-x*30))*Math.exp(-x*22),g,-.05,.25)};
const chh=(t,g=.045,pan=.25)=>{const f=hp();add(t,.05,x=>f(noise(),.75)*Math.exp(-x*90),g,pan,.05)};
const ARP=[0,2,1,2,0,2,1,2,0,2,1,2,0,1,2,1];                                   // benga rhythm guitar: 16th arpeggio over the triad
const LEAD=new Map([[0,4],[2,3],[3,4],[4,5],[6,4],[7,3],[8,2],[10,3],[11,4],[12,3],[14,2],[15,1],   // lead: two bars of chord-tone
  [16,4],[18,5],[19,6],[20,5],[22,4],[24,3],[26,4],[27,3],[28,2],[30,1],[31,0]]);                 // indices, chattering 16ths
// Drill kit and voices. 808: a saturated sine that slides in from the previous note. Lyre: Karplus-Strong with a resonator buzz.
function e808(t,n,len,g=.5,from=null){const f1=hz(n),f0=from!=null?hz(from):f1;let ph=0;
  add(t,len,x=>{const f=f0+(f1-f0)*Math.min(1,x/.09);ph+=TAU*f/SR;return Math.tanh(2.2*Math.sin(ph))*Math.exp(-x*(1.3/len))*Math.min(1,(len-x)*30)+(x<.006?(1-x/.006)*.6:0)},g)}
const dkick=(t,g=.55)=>{KICKS.push(t);add(t,.18,x=>Math.tanh(2*Math.sin(TAU*(60*x+160*(1-Math.exp(-x*45))/45)))*Math.exp(-x*22),g)};
const dsnare=(t,g=.3)=>{const f=hp();add(t,.28,x=>f(noise(),.5)*.9*Math.exp(-x*16)+.5*Math.sin(TAU*(210-60*x)*x)*Math.exp(-x*28),g,.02,.35)};
const dhat=(t,g=.06,pan=.2)=>{const f=hp();add(t,.035,x=>f(noise(),.8)*Math.exp(-x*140),g,pan,.04)};
function lyre(t,n,g=.13,pan=.4,len=.9){const f=hz(n),P=Math.max(2,Math.round(SR/f)),buf=new Float32Array(P);let lp=0;
  for(let i=0;i<P;i++){lp+=.8*(noise()-lp);buf[i]=lp}let i=0,body=0;
  add(t,len,x=>{const j=i%P,v=buf[j];buf[j]=(v+buf[(j+1)%P])*.5*.9965;i++;body+=.2*(v-body);return (v*.8+body*.5+Math.tanh(v*6)*.25*Math.exp(-x*5))*Math.min(1,(len-x)*20)},g,pan,.3,true)}
const brass=(t,ns,g=.1,len=.7)=>pad(t,ns,len,x=>4200*Math.exp(-x*6)+500,g*1.7);
const EMP=[40,43,45,47,50,52,55,57,59,62,64,67,69,71,74,76];   // E minor pentatonic
const RIFF=new Map([[0,9],[2,10],[3,9],[4,7],[6,8],[7,9],[8,6],[10,7],[11,6],[12,4],[14,6],[15,7],[16,9],[18,11],[19,10],[20,9],[22,8],[23,9],[24,11],[26,12],[27,11],[28,10],[30,9],[31,8]]);
const BASS808=[[0,0],[6,0],[10,7,1],[14,12,1]];   // [16th, semitones over the root + 24, slides in?]

// ── FX: put a revCrash + impact on every scene cut, a riser before every reveal
const riser=(t,len,g=.28)=>{let lp=0;add(t,len,x=>{const k=x/len;lp+=(.01+.35*k*k)*(noise()-lp);return (lp*2.2+.25*Math.sin(TAU*(180+1400*k*k)*x))*k*k},g,0,.45)};
const down=(t,len=1,g=.22)=>{let lp=0;add(t,len,x=>{const k=x/len;lp+=(.4*(1-k)+.01)*(noise()-lp);return lp*(1-k)**2*2},g,0,.5)};
const impact=(t,g=.7)=>{add(t,2,x=>Math.sin(TAU*(30*x+50*(1-Math.exp(-x*5))/5))*Math.exp(-x*2),g,0,.15);down(t,1.4,g*.45)};
const crash=(t,g=.14)=>{const f=hp();add(t,2.2,x=>f(noise(),.5)*Math.exp(-x*2.2),g,.15,.5)};
const revCrash=(t,len=1,g=.12)=>{const f=hp();add(t-len,len,x=>f(noise(),.5)*(x/len)**3,g,-.15,.3)};
const tick=(t,g=.12)=>add(t,.04,x=>Math.sin(TAU*2600*x)*Math.exp(-x*150),g,.3,.4);

// ── Groove between two music beats, on one global 16th grid so cuts never land off-beat. Options thin it for quiet scenes.
function groove(from,to,{k=true,cl=true,hh=true,sh=true,cg=true,bs=true,pd=true,arp=false,cut=1400}={}){
  const drums=STYLE!=='ambient'&&STYLE!=='drill';
  for(let gi=Math.ceil(from*4-1e-6);gi<Math.round(to*4);gi++){const s=gi%16,ch=chordAt(gi/4),t=T(gi/4)+(gi%2?S16*SW:0);
    if(drums&&k&&s%4===0)kick(t);
    if(drums&&cl&&s%8===4)clap(t);
    if(drums&&hh&&s%4===2)ohat(t);
    if(drums&&sh)shaker(t,s%4===2?.05:s%2?.07:.035);
    if(STYLE==='afrohouse'){if(cg&&[3,6,10,11,14].includes(s))conga(t,[3,11].includes(s)?330:220,.16,s%2?.4:-.35);if(cg&&s===7)rim(t);
      if(bs&&[2,6,10,13,14].includes(s))bass(t,ch.r+(s===13?12:0)+(s===14?7:0),S16*(s===13?.9:1.7));}
    if(STYLE==='amapiano'&&bs&&[0,3,6,10,11,14].includes(s))logdrum(t,ch.r+[0,0,7,0,12,10][[0,3,6,10,11,14].indexOf(s)],.45,s===11?.25:.45);
    if(STYLE==='ambient'&&bs&&s===0)bass(t,ch.r,B*3.8,.22);
    if(STYLE==='benga'){const tri=ch.c.slice(0,3).map(n=>n<60?n+12:n);
      if(drums&&cl&&s%8===4)snare(t);if(drums&&hh&&s%2===1)chh(t);
      if(bs&&s%2===0){const nxt=chordAt(gi/4+4).r;bass(t,ch.r+12+[0,7,12,7,0,7,10,nxt-ch.r+(nxt<ch.r?12:0)-1][s/2],S16*1.8,.21)}   // walking eighths
      if(cg)pluck(t,tri[ARP[s]]+(s>=12?12:0),.11,-.45,{bright:.55,mute:true});
      if(arp&&LEAD.has(gi%32)){const c5=ch.c.map(n=>n+12);pluck(t,c5[LEAD.get(gi%32)%5]+(LEAD.get(gi%32)>4?12:0),.14,.45,{bright:.85,len:.5})}}
    if(STYLE==='drill'){const bar=Math.floor(gi/16);
      if(k&&(([0,7,11].includes(s)&&!(bar%2&&s===11))||(bar%2&&s===13)))dkick(t,s?.45:.55);
      if(cl&&s===8)dsnare(t);
      if(hh){if(bar%2&&s>=12)for(let r=0;r<3;r++)dhat(t+r*S16/3,.045+.01*r,.25);else if(s%2===0)dhat(t,s%4===0?.065:.05)}
      if(bs){const h=BASS808.find(([st])=>st===s);if(h){const p=BASS808[(BASS808.indexOf(h)+3)%4];e808(t,ch.r+24+h[1],S16*(s===0?6:s===14?2.2:4),.5,h[2]?ch.r+24+p[1]:null)}}
      if((cg||arp)&&RIFF.has(gi%32))lyre(t,EMP[RIFF.get(gi%32)],arp?.13:.1,.4,.8)}
    if(((arp&&STYLE!=='benga'&&STYLE!=='drill')||STYLE==='ambient')&&s%2===0)mar(t,ch.c[[0,2,4,1,3,2,4,3][(s/2)%8]]+12,.08,(s/2)%2?.3:-.3);}
  if(pd)for(let bb=Math.floor(from/4)*4;bb<to;bb+=4){const a=Math.max(bb,from),z=Math.min(bb+4,to);if(z-a>.05)pad(T(a),chordAt(bb).c,(z-a)*B+.05,()=>cut,.048)}
}

// ── Cue sheet: mirror comp.html's scenes. Write every time as M(comp beat).
// The hits below use kick() and impact() whatever the STYLE: for ambient, drop the kick() calls and soften the impacts.
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
console.log(`score.wav ${DUR.toFixed(2)} s, ${STYLE}, key ${KEY>=0?'+':''}${KEY}, ${BPM} BPM`);
// Score log: one line per film in the folder that holds the brand's films. Every film gets its own music.
{const log=new URL('../score-log.tsv',import.meta.url),film=new URL('.',import.meta.url).pathname.split('/').filter(Boolean).pop();
  const rows=(existsSync(log)?readFileSync(log,'utf8').trim().split('\n'):[]).filter(r=>r&&!r.startsWith('film\t')).map(r=>r.split('\t'));
  const others=rows.filter(r=>r[0]!==film),recent=others.slice(-2);
  if(recent.some(r=>r[1]===STYLE))console.log(`⚠ ${STYLE} was used by ${recent.filter(r=>r[1]===STYLE).map(r=>r[0]).join(', ')}: this brand's recent films need different music. Pick another STYLE (or at least a new KEY and tempo).`);
  const line=[film,STYLE,KEY,BPM,new Date().toISOString().slice(0,10)];
  writeFileSync(log,['film\tstyle\tkey\tbpm\tdate',...others.map(r=>r.join('\t')),line.join('\t')].join('\n')+'\n')}
