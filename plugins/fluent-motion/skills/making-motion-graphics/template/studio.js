// studio.js: the talking-head studio (references/studio.md). Loaded after edits.js and before comp.html's script; like edits.js it
// touches comp's globals only when a helper is called. Each effect needs the shot's mattes (segment.swift person) and its measurements
// (scripts/shot_check.py → shots/NAME.info.js, loaded after this file). Everything is pure in time.

// A shot's measurements and its clean-room plate; an alias shot (SHOTS.X.dir = another shot) uses that shot's.
const shotInfo=k=>globalThis.SHOTINFO?.[k]??globalThis.SHOTINFO?.[SHOTS[k]?.dir],cleanImg=k=>IMG[k+'_clean']??IMG[SHOTS[k]?.dir+'_clean'];
// The shot's measurements on the current frame: head top, head centre x, neck, shoulder line, subject left/right, room drift.
function head(k){const I=shotInfo(k);if(!I)return null;const f=I.f[clamp(shotIdx(k)-1,0,I.f.length-1)];
  return{top:f[0],cx:f[1],neck:f[2],sh:f[3],x0:f[4],x1:f[5],dx:f[6],dy:f[7],hh:f[2]-f[0],cy:(f[0]+f[2])/2,chest:[f[1],f[3]+(f[2]-f[0])*.6],moving:I.cam.moving}}
// The sandwich: the room, then whatever behind() draws, then the person on top, so graphics sit behind the speaker.
// s/x/y move room and person together (same transform as plate and subject); front() draws over everything.
function sandwich(k,behind,{s=1,x=0,y=0,room=true,front=null}={}){if(room)plate(k,s,x,y);if(behind)behind();subject(k,s,x,y);if(front)front()}
// Draw on the wall: follows the room's tracked drift, so a graphic stays put on the wall in a handheld shot.
function pinned(k,draw){const p=head(k);ctx.save();if(p&&p.moving)ctx.translate(p.dx,p.dy);draw();ctx.restore()}
// The room only, with the person removed: assets/NAME_clean.png from shot_check.py --clean (add it to SRC as NAME_clean).
const cleanRoom=(k,s=1,x=0,y=0)=>{const im=cleanImg(k);if(!im)return false;ctx.save();ctx.translate(W/2+x,H/2+y);ctx.scale(s,s);ctx.drawImage(im,-W/2,-H/2,W,H);ctx.restore();return true};
// A frosted glass card: the frame drawn so far, blurred and tinted inside a rounded rectangle, with a hairline edge.
function glass(x,y,w,h,{r=36,blur=28,tint='rgba(14,14,18,.55)',edge='rgba(255,255,255,.18)',alpha=1}={}){if(alpha<=0)return;const s=snap();
  ctx.save();ctx.globalAlpha=alpha;ctx.beginPath();ctx.roundRect(x,y,w,h,r);ctx.clip();ctx.filter=`blur(${blur}px)`;ctx.drawImage(s,0,0);ctx.filter='none';
  ctx.fillStyle=tint;ctx.fillRect(x,y,w,h);ctx.restore();ctx.save();ctx.globalAlpha=alpha;ctx.strokeStyle=edge;ctx.lineWidth=2;ctx.beginPath();ctx.roundRect(x+1,y+1,w-2,h-2,r);ctx.stroke();ctx.restore()}

// ═══ Walls: graphics on the wall behind the speaker (references/studio-walls.md)

// Shared bits for the group-A effects (SA = studio A).
const SA={
  // Chin line in frame px: head(k).neck reads mouth level on a seated, bearded speaker (and jumps with the hands), so take the lower of it
  // and a margin under the shoulder line. Anything drawn in front of the person stays below this.
  chin(k){const h=head(k);return h?Math.max(h.neck,h.sh+.2*(h.sh-h.top)):H*.55},
  // A rounded image card centred on (x,y), w wide, with a small drop shadow and a hairline edge; shade darkens it (depth cue).
  card(im,x,y,w,{sc=1,alpha=1,rot=0,r=18,shade=0}={}){if(!im||alpha<=0||sc<=0)return 0;const h=w*im.height/im.width;ctx.save();ctx.globalAlpha=alpha;
    ctx.translate(x,y);ctx.rotate(rot);ctx.scale(sc,sc);ctx.beginPath();ctx.roundRect(-w/2,-h/2,w,h,r);
    ctx.shadowColor='rgba(0,0,0,.4)';ctx.shadowBlur=24*sc;ctx.shadowOffsetY=9*sc;ctx.fillStyle='#000';ctx.fill();ctx.shadowColor='transparent';
    ctx.save();ctx.clip();ctx.drawImage(im,-w/2,-h/2,w,h);if(shade>0){ctx.fillStyle=`rgba(0,0,0,${shade})`;ctx.fillRect(-w/2,-h/2,w,h)}ctx.restore();
    ctx.strokeStyle='rgba(255,255,255,.22)';ctx.lineWidth=1.5/sc;ctx.stroke();ctx.restore();return h},
  out:z=>Number.isFinite(z)?1-IN(z-.5,.5,E.inOutCubic):1,   // fade-out factor for effects whose end beat z is optional
  dimRoom(a){if(a>0){ctx.fillStyle=`rgba(0,0,0,${a})`;ctx.fillRect(-200,-200,W+400,H+400)}},
  // Catmull-Rom through pts, n samples a segment: [[x,y,cumulativeLength,segmentIndex],…]
  smooth(P,n=18){const o=[];let L=0;for(let i=0;i<P.length-1;i++){const p0=P[Math.max(0,i-1)],p1=P[i],p2=P[i+1],p3=P[Math.min(P.length-1,i+2)];
    for(let j=i?1:0;j<=n;j++){const s=j/n,s2=s*s,s3=s2*s,f=(a,b,c,d)=>.5*(2*b+(-a+c)*s+(2*a-5*b+4*c-d)*s2+(-a+3*b-3*c+d)*s3),x=f(p0[0],p1[0],p2[0],p3[0]),y=f(p0[1],p1[1],p2[1],p3[1]);
      if(o.length){const q=o.at(-1);L+=Math.hypot(x-q[0],y-q[1])}o.push([x,y,L,i])}}return o},
  // Stroke a sampled path from length l0 to l1
  stroke(S,l0,l1){if(l1<=l0)return;ctx.beginPath();let on=false;for(const[x,y,l]of S){if(l<l0)continue;if(l>l1)break;on?ctx.lineTo(x,y):ctx.moveTo(x,y);on=true}
    const q=SA.at(S,l1);if(on)ctx.lineTo(q[0],q[1]);ctx.stroke()},
  at(S,l){const i=S.findIndex(p=>p[2]>=l);if(i<=0)return S[i<0?S.length-1:0];const[p,q]=[S[i-1],S[i]],u=(l-p[2])/((q[2]-p[2])||1);return[lerp(p[0],q[0],u),lerp(p[1],q[1],u)]}};

// orbit(k,a,z,{items,tilt,roll,period,rx,w,stagger,fly,phase}): IMG cards circle the speaker on a tilted ring round the chest, the far half
// behind the person and the near half in front (kept below the chin), scaled by depth; they swoop in one after another from a and out by z.
function orbit(k,a,z,{items,tilt=.85,roll=-.12,period=7,rx=470,w=220,stagger=.12,fly=.9,phase=-.4}={}){
  const h=head(k),n=items.length,[cx,cy]=h?h.chest:[W/2,H*.62],chin=SA.chin(k),fw=h?(h.sh-h.top)*.42:160,
    spin=TAU*(t-cS(a))/period,cr=Math.cos(roll),sr=Math.sin(roll),back=[],front=[];
  items.forEach((key,i)=>{const im=IMG[key];if(!im)return;const a0=a+i*stagger,z0=z-fly-(n-1-i)*stagger,ki=E.outExpo(PB(a0,a0+fly)),ko=inC(PB(z0,z0+fly));
    if(ki<=0||ko>=1)return;const th=phase+i*TAU/n+spin-(1-ki)*1.3+ko*1.5,rf=lerp(2.4,1,ki)+ko*1.8,ex=Math.cos(th)*rx*rf,ey=Math.sin(th)*rx*tilt*rf,d=Math.sin(th),
      s=lerp(.68,1.16,(d+1)/2),ch=w*im.height/im.width*s,x=cx+ex*cr-ey*sr;let y=cy+ex*sr+ey*cr;
    if(d>-.2&&Math.abs(x-cx)<fw+w*s/2)y=Math.max(y,chin+ch/2+16);   // near half and the hand-over: never across the face
    const c={im,x,y,d,s,al:clamp(ki*2.5)*(1-clamp(ko*2-.6)),rot:Math.cos(th)*.08};
    // crossing the ring's sides the card dissolves from behind the arm to in front of it instead of popping
    if(d<.15)back.push(c);if(d>-.15)front.push({...c,al:c.al*E.inOutCubic(clamp((d+.15)/.3))})});
  const dr=L=>L.sort((p,q)=>p.d-q.d).forEach(c=>SA.card(c.im,c.x,c.y,w,{sc:c.s,alpha:c.al,rot:c.rot,shade:Math.max(0,-c.d)*.3}));
  sandwich(k,()=>dr(back),{front:()=>dr(front)})}

// couchWall(k,a,z,{items,cols,gap,speed,stagger,rise,dim,r}): the wall behind the speaker becomes a feed of IMG cards in columns that rise
// from behind the person (centre column first), drift slowly upward and wrap, then sink away again by z. Behind the person, pinned to the wall.
function couchWall(k,a,z,{items,cols=3,gap=24,speed=34,stagger=.22,rise=1.1,dim=.38,r=20}={}){
  const cw=(W-gap*(cols+1))/cols,el=Math.max(0,t-cS(a)),kd=Math.min(IN(a,.8,E.outCubic),1-IN(z-.9,.9,E.inOutCubic)),
    order=[...Array(cols).keys()].sort((p,q)=>Math.abs(p-(cols-1)/2)-Math.abs(q-(cols-1)/2));
  sandwich(k,()=>pinned(k,()=>{SA.dimRoom(dim*kd);
    for(let c=0;c<cols;c++){const j=order.indexOf(c),ki=E.outExpo(PB(a+j*stagger,a+j*stagger+rise)),z0=z-rise*.8-(cols-1-j)*stagger,ko=inC(PB(z0,z0+rise*.8));
      if(ki<=0||ko>=1)continue;const list=items.filter((_,i)=>i%cols===c),L0=(list.length?list:items).map(key=>IMG[key]).filter(Boolean);if(!L0.length)continue;
      const hs=L0.map(im=>cw*im.height/im.width),Lc=hs.reduce((s,v)=>s+v+gap,0),rep=Math.ceil((H+600)/Lc),span=Lc*rep,hmax=Math.max(...hs),
        off=el*speed*(1+.18*((c*7)%3-1))-(c%2)*cw*.55,dy=((1-ki)+ko)*H*1.05,x=gap+c*(cw+gap)+cw/2;let cum=0;
      for(let q=0;q<rep;q++)L0.forEach((im,i)=>{const yy=((cum-off)%span+span)%span-hmax-gap+120;cum+=hs[i]+gap;   // wrap: cards leaving the top reappear behind the person
        if(yy+dy>H||yy+hs[i]+dy<-40)return;SA.card(im,x,yy+hs[i]/2+dy,cw,{r})})}}))}

// headlineWall(k,a,{cards,key,keyBeat,heroBeats,stagger,z}): the wall fills with vector cards (kind 'headline' | 'post' | 'search', each
// {kind,text,src?,handle?}) all making one claim; at keyBeat a yellow highlighter swipes the key word on every card; heroBeats [[beat,cardIndex],…]
// lift one card at a time to the front of the wall (still behind the person). Shows only the text passed in: no invented sources or numbers.
function headlineWall(k,a,{cards,key='',keyBeat=Infinity,heroBeats=[],stagger=.28,z=Infinity}={}){
  const h=head(k),hx=h?h.cx:W/2,ht=h?h.top:H*.3,SL=[[-250,-262,-.05],[290,-318,.04],[30,-96,-.02],[-310,80,.045],[360,40,-.035],[-330,318,-.025],[380,300,.03],[-40,-430,.02]],
    hb=[...heroBeats].sort((p,q)=>p[0]-q[0]),out=SA.out(z);
  const lay=cards.map((cd,i)=>{const L=SA.hlLay(cd),[dx,dy,rot]=SL[i%SL.length],x=clamp(hx+dx,L.w/2+20,W-L.w/2-20),y=Math.max(150+L.h/2,ht+dy),a0=a+i*stagger,
      u=hb.reduce((s,[bt,ix],j)=>ix===i?s+spring(bt,{z:.78,w:11})-(hb[j+1]?spring(hb[j+1][0],{z:.9,w:11}):0):s,0),
      S=Math.min(1.75,(W-110)/L.w,(ht-170)/L.h),tx=W/2,ty=(190+ht-14)/2,pop=spring(a0,{z:.62,w:13});
    return{L,i,u:clamp(u,0,1.1),x:lerp(x,tx,clamp(u)),y:lerp(y+Math.sin(t*1.3+i*2)*4,ty,clamp(u)),sc:lerp(lerp(.55,1,pop),S,u),rot:lerp(rot+(1-clamp(pop))*(i%2?.3:-.3),0,clamp(u)),
      al:clamp(PB(a0,a0+.2))*out,hi:E.inOutCubic(PB(keyBeat+i*.07,keyBeat+i*.07+.4))}});
  const lift=Math.max(0,...lay.map(c=>clamp(c.u)));
  sandwich(k,()=>pinned(k,()=>{SA.dimRoom(.22*Math.min(IN(a,.6),out));
    lay.filter(c=>c.u<.02).forEach(c=>SA.hlDraw(c,key));SA.dimRoom(.45*lift*out);
    lay.filter(c=>c.u>=.02).sort((p,q)=>p.u-q.u).forEach(c=>SA.hlDraw(c,key))}))}
// Layout of one headlineWall card: wrapped lines and size. Kinds differ in width, type and chrome.
SA.hlLay=cd=>{const kind=cd.kind||'headline',w={headline:440,post:420,search:460}[kind]||440,p=26,
    [w8,s,lh]=kind==='headline'?[800,40,46]:kind==='post'?[400,33,42]:[400,35,43],lines=wrap(cd.text,w8,s,w-p*2),
    top=kind==='post'?(cd.src||cd.handle?78:p):kind==='search'?(cd.src?62:p):(cd.src?60:p),foot=kind==='post'?56:p;
  return{cd,kind,w,p,w8,s,lh,lines,top,h:top+lines.length*lh+foot}};
// Draw one laid-out card at its place with its highlighter progress (multiply blend, so the ink stays dark over the yellow)
SA.hlDraw=(c,key)=>{const{L,x,y,sc,rot,al,hi}=c,{cd,kind,w,p,w8,s,lh,lines,top,h}=L;if(al<=0||sc<=0)return;
  ctx.save();ctx.globalAlpha=al;ctx.translate(x,y);ctx.rotate(rot);ctx.scale(sc,sc);ctx.translate(-w/2,-h/2);
  ctx.shadowColor='rgba(0,0,0,.35)';ctx.shadowBlur=26*sc;ctx.shadowOffsetY=10*sc;ctx.fillStyle=kind==='post'?'#FFFFFF':'#FBFAF6';ctx.beginPath();ctx.roundRect(0,0,w,h,16);ctx.fill();ctx.shadowColor='transparent';
  ctx.textBaseline='middle';ctx.textAlign='left';ctx.letterSpacing='0px';
  if(kind==='headline'&&cd.src){ctx.font=font(800,20);ctx.letterSpacing='2px';ctx.fillStyle=C.accent;ctx.fillText(cd.src.toUpperCase(),p,p+10);ctx.letterSpacing='0px';
    ctx.fillStyle='rgba(0,0,0,.12)';ctx.fillRect(p,p+28,w-p*2,2)}
  if(kind==='post'&&(cd.src||cd.handle)){ctx.fillStyle='#D9D4CB';ctx.beginPath();ctx.arc(p+24,p+24,24,0,TAU);ctx.fill();
    if(cd.src){ctx.font=font(800,26);ctx.fillStyle='#141414';ctx.fillText(cd.src,p+62,p+(cd.handle?12:24))}
    if(cd.handle){ctx.font=font(400,22);ctx.fillStyle='#7A766E';ctx.fillText(cd.handle,p+62,p+(cd.src?40:24))}}
  if(kind==='search'&&cd.src){ctx.fillStyle='#E4E1DA';ctx.beginPath();ctx.arc(p+12,p+12,12,0,TAU);ctx.fill();ctx.font=font(400,21);ctx.fillStyle='#4A6B4A';ctx.fillText(cd.src,p+32,p+13)}
  ctx.font=font(w8,s);const ink=kind==='search'?'#1F3FA6':'#141414';ctx.fillStyle=ink;
  lines.forEach((ln,i)=>ctx.fillText(ln,p,top+lh*(i+.5)));
  if(key&&hi>0){ctx.globalCompositeOperation='multiply';ctx.fillStyle='#FFDD33';const kl=key.toLowerCase(),all=lines.join(' ').toLowerCase();let st=0;
    const L0=lines.map(ln=>{const o=st;st+=ln.length+1;return o});   // char offset of each line, so a key that wraps onto the next line is marked on both
    for(let j=all.indexOf(kl);j>=0;j=all.indexOf(kl,j+kl.length))lines.forEach((ln,i)=>{const c0=Math.max(j,L0[i])-L0[i],c1=Math.min(j+kl.length,L0[i]+ln.length)-L0[i];if(c1<=c0)return;
      const x0=p+ctx.measureText(ln.slice(0,c0)).width-6,x1=p+ctx.measureText(ln.slice(0,c1)).width+6,yc=top+lh*(i+.5)+s*.04,hh=s*.56,xe=lerp(x0,x1,hi);
      ctx.beginPath();ctx.moveTo(x0+4,yc-hh);ctx.lineTo(xe+(hi<1?0:3),yc-hh+2);ctx.lineTo(xe,yc+hh);ctx.lineTo(x0,yc+hh-2);ctx.closePath();ctx.fill()});
    ctx.globalCompositeOperation='source-over'}
  if(kind==='search'){ctx.strokeStyle=ink;ctx.lineWidth=1.5;lines.forEach((ln,i)=>{const yy=top+lh*(i+.5)+s*.52;ctx.globalAlpha=al*.35;ctx.beginPath();ctx.moveTo(p,yy);ctx.lineTo(p+ctx.measureText(ln).width,yy);ctx.stroke()});ctx.globalAlpha=al}
  if(kind==='post'){const fy=h-p-6;ctx.strokeStyle='#8A857C';ctx.lineWidth=2.4;ctx.lineJoin='round';ctx.lineCap='round';
    ctx.beginPath();ctx.roundRect(p,fy-11,26,19,8);ctx.moveTo(p+7,fy+8);ctx.lineTo(p+4,fy+14);ctx.lineTo(p+13,fy+8);ctx.stroke();                  // reply
    const rx=p+96;ctx.beginPath();ctx.moveTo(rx,fy+2);ctx.lineTo(rx,fy-8);ctx.lineTo(rx+20,fy-8);ctx.moveTo(rx+15,fy-13);ctx.lineTo(rx+20,fy-8);ctx.lineTo(rx+15,fy-3);
    ctx.moveTo(rx+26,fy-4);ctx.lineTo(rx+26,fy+6);ctx.lineTo(rx+6,fy+6);ctx.moveTo(rx+11,fy+1);ctx.lineTo(rx+6,fy+6);ctx.lineTo(rx+11,fy+11);ctx.stroke();   // repost
    const hx=p+196;ctx.beginPath();ctx.moveTo(hx,fy+11);ctx.bezierCurveTo(hx-22,fy-2,hx-12,fy-16,hx,fy-6);ctx.bezierCurveTo(hx+12,fy-16,hx+22,fy-2,hx,fy+11);ctx.stroke()}   // like
  ctx.restore()};

// chartGrow(k,a,{points,kickAt,x,y,w,h,label,kickFrom,tag,axis,dim,panel,z}): a line chart of the author's points draws itself on the wall
// behind the speaker (the early, flat part with its small wobbles), then at kickAt the last segments kick up in C.accent with a glow and a fill
// while the room dims. No numbers appear unless passed: tag (text at the peak) and axis (labels under the points) are optional.
function chartGrow(k,a,{points,kickAt,x=60,y=280,w=W-120,h=360,label=null,kickFrom=points.length-2,tag=null,axis=null,dim=.32,panel=true,z=Infinity}={}){
  const out=SA.out(z),ap=IN(a,.5,E.outCubic)*out,lo=Math.min(...points),hi=Math.max(...points),px=46,top=label?96:46,bot=axis?70:44,
    P=points.map((v,i)=>[x+px+(w-2*px)*i/(points.length-1),y+h-bot-(h-top-bot)*(v-lo)/((hi-lo)||1)]),S=SA.smooth(P),kf=kickFrom>0?(S.findLast(p=>p[3]===kickFrom-1)??S[0])[2]:0,Lt=S.at(-1)[2],
    l1=lerp(0,kf,E.inOutCubic(PB(a+.35,kickAt))),l2=lerp(kf,Lt,E.outExpo(PB(kickAt,kickAt+.6))),kk=IN(kickAt,.45,E.outCubic)*out;
  sandwich(k,()=>pinned(k,()=>{if(ap<=0)return;SA.dimRoom(dim*kk);
    if(panel){glass(x,y,w,h,{alpha:ap,tint:'rgba(12,12,16,.5)'})}
    ctx.save();ctx.globalAlpha=ap;ctx.strokeStyle='rgba(255,255,255,.1)';ctx.lineWidth=2;for(let g=0;g<4;g++){const gy=y+top+(h-top-bot)*g/3;ctx.beginPath();ctx.moveTo(x+px,gy);ctx.lineTo(x+w-px,gy);ctx.stroke()}
    if(label)word(label,x+px,y+52,800,fit(label,800,w-2*px,44),C.ink,{align:'left'});
    if(axis)axis.forEach((s,i)=>i<P.length&&word(String(s),P[i][0],y+h-34,400,26,C.soft,{alpha:ap}));
    ctx.lineCap='round';ctx.lineJoin='round';ctx.strokeStyle=C.ink;ctx.lineWidth=9;SA.stroke(S,0,l1);
    if(l2>kf){const tip=SA.at(S,l2);ctx.save();ctx.beginPath();ctx.moveTo(SA.at(S,kf)[0],y+h-bot);S.filter(p=>p[2]>=kf&&p[2]<=l2).forEach(p=>ctx.lineTo(p[0],p[1]));ctx.lineTo(tip[0],tip[1]);
      ctx.lineTo(tip[0],y+h-bot);ctx.closePath();const g=ctx.createLinearGradient(0,y+top,0,y+h-bot);g.addColorStop(0,`rgba(${rgbOf(C.accent)},${.42*kk})`);g.addColorStop(1,`rgba(${rgbOf(C.accent)},0)`);
      ctx.fillStyle=g;ctx.fill();ctx.restore();ctx.strokeStyle=C.accent;ctx.lineWidth=11;ctx.shadowColor=C.accent;ctx.shadowBlur=28;SA.stroke(S,kf,l2);ctx.shadowBlur=0}
    const tip=SA.at(S,l2>kf?l2:l1),hot=l2>kf,pul=hot?1+.25*Math.sin(Math.max(0,b-kickAt)*TAU*.9)*Math.exp(-Math.max(0,b-kickAt)*.6):1;
    if(l1>0){ctx.fillStyle=hot?C.accent:C.ink;ctx.shadowColor=hot?C.accent:'transparent';ctx.shadowBlur=hot?24:0;ctx.beginPath();ctx.arc(tip[0],tip[1],11*pul,0,TAU);ctx.fill();ctx.shadowBlur=0;
      ctx.fillStyle=C.bg;ctx.beginPath();ctx.arc(tip[0],tip[1],4.5,0,TAU);ctx.fill()}ctx.restore();
    if(tag){const u=IN(kickAt+.45,.5,E.outBack),pk=P.at(-1);ctx.font=font(800,34);ctx.letterSpacing='0px';const pw=ctx.measureText(tag).width+34*1.9;   // left of the peak, clear of the rising line
      pill(tag,Math.max(x+px+pw/2,pk[0]-34-pw/2),clamp(pk[1]+40,y+top,y+h-bot-40),34,C.accent,C.bg,{sc:u,alpha:out,w8:800})}}))}

// checklist(k,a,{items:[[text,inBeat,tickBeat],…],x,y,w,title,row,size,z}): a frosted glass card behind the speaker grows row by row; each row
// lands at its inBeat and its tick draws on at its tickBeat; once every row is ticked an "n of n" pill, a full progress bar and a soft glow finish it.
function checklist(k,a,{items,x=80,y=280,w=W-160,title=null,row=92,size=48,footer=true,z=Infinity}={}){
  const n=items.length,out=SA.out(z),done=Math.max(...items.map(r=>r[2])),pad=34,tH=title?74:0,
    rk=items.map(([,ib])=>clamp(spring(ib,{z:.8,w:13}),0,1.04)),fk=clamp(spring(done+.3,{z:.8,w:12}),0,1.04),
    ch=pad*2+tH+rk.reduce((s,v)=>s+v*row,0)+fk*86,ap=IN(a,.4,E.outCubic)*out,gl=IN(done+.3,.6,E.outCubic)*out;
  sandwich(k,()=>pinned(k,()=>{if(ap<=0)return;
    if(gl>0){ctx.save();ctx.beginPath();ctx.rect(-200,-200,W+400,H+400);ctx.roundRect(x,y,w,ch,36);ctx.clip('evenodd');ctx.shadowColor=`rgba(${rgbOf(C.accent)},${.55*gl})`;
      ctx.shadowBlur=70;ctx.fillStyle='#000';ctx.beginPath();ctx.roundRect(x,y,w,ch,36);ctx.fill();ctx.restore()}
    glass(x,y,w,ch,{alpha:ap,blur:30,tint:'rgba(14,14,18,.5)',edge:gl>0?`rgba(${rgbOf(C.accent)},${.18+.5*gl})`:'rgba(255,255,255,.2)'});
    ctx.save();ctx.globalAlpha=ap;ctx.beginPath();ctx.roundRect(x,y,w,ch,36);ctx.clip();
    if(title)word(title,x+pad+4,y+pad+26,800,fit(title,800,w-pad*2,40),C.soft,{align:'left',track:1});
    items.forEach(([txt,ib,tb],i)=>{const u=rk[i];if(u<=0)return;const ry=y+pad+tH+row*(i+.5),cx=x+pad+30,tk=PB(tb,tb+.35),f=clamp(spring(tb,{z:.55,w:16}),0,1.2),sz=fit(txt,700,w-pad*2-90,size);
      ctx.save();ctx.globalAlpha=ap*clamp(u*1.4);ctx.translate((1-clamp(u))*60,0);
      ctx.strokeStyle='rgba(255,255,255,.45)';ctx.lineWidth=3;ctx.beginPath();ctx.arc(cx,ry,22,0,TAU);ctx.stroke();
      if(f>0){ctx.fillStyle=C.accent;ctx.beginPath();ctx.arc(cx,ry,22*f,0,TAU);ctx.fill();
        ctx.strokeStyle=C.bg;ctx.lineWidth=5.5;ctx.lineCap='round';ctx.lineJoin='round';const T=[[cx-10,ry+1],[cx-3,ry+8],[cx+11,ry-8]],l=E.outCubic(tk)*2;
        ctx.beginPath();ctx.moveTo(...T[0]);ctx.lineTo(lerp(T[0][0],T[1][0],clamp(l)),lerp(T[0][1],T[1][1],clamp(l)));if(l>1)ctx.lineTo(lerp(T[1][0],T[2][0],l-1),lerp(T[1][1],T[2][1],l-1));if(l>0)ctx.stroke()}
      word(txt,cx+44,ry+2,700,sz,C.ink,{align:'left',alpha:lerp(.72,1,clamp(f))});ctx.restore()});
    if(fk>0){const fy=y+pad+tH+row*n+30,ticks=items.filter(r=>b>=r[2]).length,bx=x+pad+150,bw=w-pad*2-160;ctx.globalAlpha=ap*clamp(fk);
      if(footer)pill(`${ticks} of ${n}`,x+pad+66,fy+8,28,C.accent,C.bg,{sc:clamp(fk),w8:800});
      ctx.fillStyle='rgba(255,255,255,.14)';ctx.beginPath();ctx.roundRect(bx,fy,bw,14,7);ctx.fill();
      ctx.fillStyle=C.accent;ctx.shadowColor=C.accent;ctx.shadowBlur=18*gl;ctx.beginPath();ctx.roundRect(bx,fy,bw*E.outCubic(PB(done+.3,done+1.1)),14,7);ctx.fill()}
    ctx.restore()}))}

// glassType(k,a,z,{word,x,y,size,ref,disp,drift}): one word as thick clear glass letters standing on the wall: a blurred-text height map gives
// normals, a WebGL shader refracts the room through them with per-channel offsets (dispersion), adds a dark rim and a moving rim light, and a
// soft shadow falls on the wall. In over .5 beat from a, a slow drift, out over .5 beat to z. (x,y) is the word's centre.
function glassType(k,a,z,{word:wd='GLASS',x=W/2,y=330,size=250,ref=1,disp=.18,drift=28,w8=800}={}){
  const kin=IN(a,.55,E.outCubic),kout=IN(z-.5,.5,E.inOutCubic),al=kin*(1-kout),p=PB(a,z);
  sandwich(k,()=>pinned(k,()=>{if(al<=0)return;const M=SA.hmap(wd,size,w8),gx=Math.round(x+drift*(p-.5)-M.w/2),gy=Math.round(y-M.h/2+(1-kin)*30-kout*24),room=snap();
    ctx.save();ctx.globalAlpha=.42*al;ctx.filter=`blur(${size*.05}px)`;ctx.font=font(w8,size);ctx.letterSpacing='0px';ctx.textAlign='center';ctx.textBaseline='middle';
    ctx.fillStyle='#000';ctx.fillText(wd,gx+M.w/2+size*.035,gy+M.h/2+size*.075);ctx.restore();             // soft shadow on the wall
    const g=SA.glass3d(M,room,gx,gy,{k:ref*kin*(1-kout*.6),disp,al,ang:-2.3+1.1*p});ctx.drawImage(g,gx,gy)}))}
// Height map of a word, memoised: R = wide blur (body), G = sharp coverage, B = narrow blur (bevel), packed with 'lighter' over black.
SA.hm=new Map();
SA.hmap=(wd,size,w8)=>{const id=wd+'|'+size+'|'+w8;if(SA.hm.has(id))return SA.hm.get(id);const c=document.createElement('canvas'),g=c.getContext('2d');
  g.font=font(w8,size);g.letterSpacing='0px';const pd=Math.round(size*.3),w=Math.ceil(g.measureText(wd).width+pd*2),h=Math.ceil(size*1.25+pd*2);c.width=w;c.height=h;
  g.fillStyle='#000';g.fillRect(0,0,w,h);g.globalCompositeOperation='lighter';g.font=font(w8,size);g.letterSpacing='0px';g.textAlign='center';g.textBaseline='middle';
  for(const[col,bl]of[['#f00',size*.075],['#0f0',0],['#00f',size*.022]]){g.filter=bl?`blur(${bl}px)`:'none';g.fillStyle=col;g.fillText(wd,w/2,h/2+size*.04)}
  const M={c,w,h};SA.hm.set(id,M);return M};
// The refraction pass (WebGL, built once on first use): room crop + height map in, premultiplied glass layer out (a canvas the size of the map).
SA.gl=null;
SA.glass3d=(M,room,gx,gy,{k,disp,al,ang})=>{if(!SA.gl){const c=document.createElement('canvas'),g=c.getContext('webgl',{preserveDrawingBuffer:true,premultipliedAlpha:true}),pr=g.createProgram(),
    sh=(ty,src)=>{const s=g.createShader(ty);g.shaderSource(s,src);g.compileShader(s);if(!g.getShaderParameter(s,g.COMPILE_STATUS))console.error(g.getShaderInfoLog(s));g.attachShader(pr,s)};
    sh(g.VERTEX_SHADER,'attribute vec2 q;varying vec2 v;void main(){v=q*.5+.5;gl_Position=vec4(q,0,1);}');
    sh(g.FRAGMENT_SHADER,`precision highp float;varying vec2 v;uniform sampler2D R,Hm;uniform vec2 px,L;uniform float k,disp,al;
float hg(vec2 p){vec3 c=texture2D(Hm,p).rgb;return c.r*.5+smoothstep(0.,1.,c.b)*.5;}
void main(){vec3 c=texture2D(Hm,v).rgb;float m=c.g;if(m<.004){gl_FragColor=vec4(0.);return;}
 vec2 e=px*3.;vec2 gr=vec2(hg(v+vec2(e.x,0.))-hg(v-vec2(e.x,0.)),hg(v+vec2(0.,e.y))-hg(v-vec2(0.,e.y)));
 vec2 o=gr*105.*k*px+(c.r-.5)*vec2(16.,-12.)*k*px;
 vec3 col=vec3(texture2D(R,v+o*(1.+disp)).r,texture2D(R,v+o).g,texture2D(R,v+o*(1.-disp)).b);
 col=mix(col,col*vec3(.9,.95,.98),k);
 float lam=clamp(dot(-gr*7.,L),-1.,1.);col*=1.+.5*lam*k;
 float rim=1.-smoothstep(.2,.8,c.b);col*=1.-.75*rim*k;
 vec3 N=normalize(vec3(-gr*5.5,1.));float sp=pow(max(dot(N,normalize(vec3(L,.55))),0.),22.);
 float edge=smoothstep(.0,.35,length(gr));col+=vec3(1.,.98,.94)*(sp*1.1*edge+.1*edge)*k;
 float a=m*al;gl_FragColor=vec4(clamp(col,0.,1.)*a,a);}`);
    g.linkProgram(pr);g.useProgram(pr);g.bindBuffer(g.ARRAY_BUFFER,g.createBuffer());g.bufferData(g.ARRAY_BUFFER,new Float32Array([-1,-1,1,-1,-1,1,1,1]),g.STATIC_DRAW);
    const l=g.getAttribLocation(pr,'q');g.enableVertexAttribArray(l);g.vertexAttribPointer(l,2,g.FLOAT,false,0,0);g.pixelStorei(g.UNPACK_FLIP_Y_WEBGL,true);
    const T=[0,1].map(i=>{const tx=g.createTexture();g.activeTexture(g.TEXTURE0+i);g.bindTexture(g.TEXTURE_2D,tx);
      for(const[p,v]of[[g.TEXTURE_MIN_FILTER,g.LINEAR],[g.TEXTURE_MAG_FILTER,g.LINEAR],[g.TEXTURE_WRAP_S,g.CLAMP_TO_EDGE],[g.TEXTURE_WRAP_T,g.CLAMP_TO_EDGE]])g.texParameteri(g.TEXTURE_2D,p,v);return tx});
    const u=n=>g.getUniformLocation(pr,n);g.uniform1i(u('R'),0);g.uniform1i(u('Hm'),1);
    const rc=document.createElement('canvas');SA.gl={c,g,T,u,rc,rg:rc.getContext('2d'),hmFor:null}}
  const{c,g,T,u,rc,rg}=SA.gl;if(c.width!==M.w||c.height!==M.h){c.width=rc.width=M.w;c.height=rc.height=M.h}
  rg.clearRect(0,0,M.w,M.h);rg.drawImage(room,-gx,-gy);                                    // the room behind the word's box
  g.activeTexture(g.TEXTURE0);g.bindTexture(g.TEXTURE_2D,T[0]);g.texImage2D(g.TEXTURE_2D,0,g.RGBA,g.RGBA,g.UNSIGNED_BYTE,rc);
  g.activeTexture(g.TEXTURE1);g.bindTexture(g.TEXTURE_2D,T[1]);if(SA.gl.hmFor!==M){g.texImage2D(g.TEXTURE_2D,0,g.RGBA,g.RGBA,g.UNSIGNED_BYTE,M.c);SA.gl.hmFor=M}
  g.viewport(0,0,M.w,M.h);g.clearColor(0,0,0,0);g.clear(g.COLOR_BUFFER_BIT);
  g.uniform2f(u('px'),1/M.w,1/M.h);g.uniform2f(u('L'),Math.cos(ang),Math.sin(ang));g.uniform1f(u('k'),k);g.uniform1f(u('disp'),disp);g.uniform1f(u('al'),al);
  g.drawArrays(g.TRIANGLE_STRIP,0,4);return c};

// ═══ Screens: screens and layouts around the speaker (references/studio-screens.md)

// ── Shared helpers
// In/out envelope in seconds: 0→1 over i s from beat a, back to 0 over o s ending at beat z.
const sbIO=(a,z,i=.7,o=.6,e=E.inOutCubic)=>Math.min(e(clamp((t-cS(a))/i)),e(clamp((cS(z)-t)/o)));
// The shot's average head measurements (head(k) per frame jitters; layouts anchor to the average). hh = head height (neck − top; a fallback for old info files).
const SBR={};function sbRef(k){if(SBR[k])return SBR[k];const I=shotInfo(k);if(!I)return{top:H*.3,cx:W/2,sh:H*.52,hh:H*.18};
  const n=I.f.length,avg=i=>I.f.reduce((s,f)=>s+f[i],0)/n,top=avg(0),sh=avg(3),nk=avg(2)-top;return SBR[k]={top,cx:avg(1),sh,hh:nk>.6*(sh-top)?nk:(sh-top)*.8}}
// Named offscreen canvas of a given size (created once), and draw() run into it with ctx swapped (cleared first).
const SBC={};function sbCanvas(n,w,h){let c=SBC[n];if(!c)c=SBC[n]=document.createElement('canvas');if(c.width!==w||c.height!==h){c.width=w;c.height=h}return c}
function sbInto(c,draw){const keep=ctx;ctx=c.getContext('2d');ctx.setTransform(1,0,0,1,0,0);ctx.globalAlpha=1;ctx.filter='none';ctx.shadowBlur=0;
  ctx.globalCompositeOperation='source-over';ctx.clearRect(0,0,c.width,c.height);try{draw()}finally{ctx=keep}return c}
// A soft drop shadow under a rounded rect (drawn before the rect itself).
function sbShadow(x,y,w,h,r,{blur=70,dy=30,alpha=.45}={}){if(alpha<=0)return;ctx.save();ctx.shadowColor=`rgba(0,0,0,${alpha})`;ctx.shadowBlur=blur;ctx.shadowOffsetY=dy;
  ctx.fillStyle='#000';ctx.beginPath();ctx.roundRect(x,y,w,h,r);ctx.fill();ctx.restore()}
// Light and dark UI palettes; UIT is the one uiType/uiBubble use (uiWorld sets it while the author's draw runs).
const sbTheme=d=>d?{bg:'#17181C',bar:'#202127',ink:'#F4F1EA',mute:'#8C8C95',line:'rgba(255,255,255,.09)',bub:'#2B2C33',field:'#222329',back:'#0C0C0E'}
  :{bg:'#FBFAF7',bar:'#EFEDE8',ink:'#1A1A1A',mute:'#8D8A84',line:'rgba(0,0,0,.09)',bub:'#ECEAE4',field:'#F2F0EB',back:'#DDD9D1'};
let UIT=sbTheme(false);
// A blurred copy of draw() (plate, cover…), drawn sharp offscreen then blurred onto the frame, overscaled so the blur's soft edge falls
// outside the frame, over an opaque fill (render() never clears the canvas: a see-through edge would show the previous frame).
function sbBlur(draw,px,{alpha=1,under='#0c0c0e'}={}){if(alpha<=0)return;const c=sbInto(sbCanvas('blr',W,H),draw),o=1+6*px/W;ctx.save();ctx.setTransform(1,0,0,1,0,0);
  if(alpha>=1&&under){ctx.fillStyle=under;ctx.fillRect(0,0,W,H)}ctx.globalAlpha=alpha;if(px>.3)ctx.filter=`blur(${px}px)`;about(W/2,H/2,o,()=>ctx.drawImage(c,0,0));ctx.restore()}
// App window chrome: rounded panel with a title bar (three dots, optional centred title). Returns the content rect below the bar.
function sbWindow(x,y,w,h,{T=UIT,title='',r=34,bar=66,shadow=.4}={}){sbShadow(x,y,w,h,r,{alpha:shadow});ctx.save();ctx.beginPath();ctx.roundRect(x,y,w,h,r);ctx.clip();
  ctx.fillStyle=T.bg;ctx.fillRect(x,y,w,h);ctx.fillStyle=T.bar;ctx.fillRect(x,y,w,bar);ctx.fillStyle=T.line;ctx.fillRect(x,y+bar-2,w,2);
  ['#FF5F57','#FEBC2E','#28C840'].forEach((c,i)=>{ctx.fillStyle=c;ctx.beginPath();ctx.arc(x+38+i*30,y+bar/2,9,0,TAU);ctx.fill()});
  if(title){ctx.font=font(800,28);ctx.letterSpacing='0px';ctx.fillStyle=T.mute;ctx.textAlign='center';ctx.textBaseline='middle';ctx.fillText(title,x+w/2,y+bar/2+1)}
  ctx.restore();ctx.save();ctx.strokeStyle=T.line;ctx.lineWidth=2;ctx.beginPath();ctx.roundRect(x+1,y+1,w-2,h-2,r);ctx.stroke();ctx.restore();return{x,y:y+bar,w,h:h-bar}}
// Media into a rect, cover-cropped: an IMG key, an image/canvas, or a function (w,h) drawing at the rect's top-left.
function sbMedia(m,x,y,w,h){if(!m)return;if(typeof m==='function'){ctx.save();ctx.translate(x,y);m(w,h);ctx.restore();return}const im=typeof m==='string'?IMG[m]:m;if(!im)return;
  const s=Math.max(w/im.width,h/im.height),sw=w/s,sh=h/s;ctx.drawImage(im,(im.width-sw)/2,(im.height-sh)/2,sw,sh,x,y,w,h)}
// Rolling odometer number v (continuous; whole numbers rest still) at (x,y) left-aligned, plus a suffix.
function sbOdo(v,x,y,size,col,{suffix='',w8=800}={}){ctx.save();ctx.font=font(w8,size);ctx.letterSpacing='0px';ctx.textAlign='left';ctx.textBaseline='middle';ctx.fillStyle=col;
  const dw=ctx.measureText('0').width,n=Math.max(1,String(Math.floor(v+.001)).length),lh=size*1.1;
  ctx.beginPath();ctx.rect(x-4,y-lh/2,dw*n+8,lh);ctx.save();ctx.clip();
  for(let p=0;p<n;p++){const q=10**p,pos=Math.floor(v/q)+Math.max(0,(v%q)-(q-1)),d=Math.floor(pos)%10,f=pos-Math.floor(pos),dx=x+(n-1-p)*dw;
    ctx.fillText(String(d),dx,y-f*lh);ctx.fillText(String((d+1)%10),dx,y+(1-f)*lh)}ctx.restore();
  if(suffix)ctx.fillText(suffix,x+dw*n+size*.06,y);ctx.restore()}

// ── 1. uiWorld: an app screen drops over the top ~55% of the frame; the speaker (shot pushed down, scaled ~1.25×) stands in front of it.
// uiWorld(k,a,z,{draw,dark,title,s,top,h,overlap}): draw(p,r) paints the screen content inside r={x,y,w,h} (p = 0→1 across a…z).
function uiWorld(k,a,z,{draw=null,dark=false,title='',s=1.25,top=250,h=830,overlap=.42}={}){const e=sbIO(a,z,.9,.7);if(e<=0){plate(k);return}
  const T=sbTheme(dark),R=sbRef(k),wb=top+h,oyT=wb-overlap*R.hh*s-H/2-(R.top-H/2)*s,sc=lerp(1,s,e),oy=lerp(0,oyT,e),pTop=H/2-H/2*sc+oy;
  const drop=Math.min(spring(a+.1,{z:.72,w:10}),E.inOutCubic(clamp((cS(z)-t)/.55))),wy=top-(1-drop)*(wb+80);
  sbBlur(()=>plate(k,sc*1.12,0,oy*.4),26);ctx.save();ctx.fillStyle=`rgba(0,0,0,${.35*e})`;ctx.fillRect(0,0,W,H);ctx.restore();   // backdrop for the strip the push uncovers
  masked(()=>plate(k,sc,0,oy),c=>{c.beginPath();c.rect(0,pTop+30*e,W,H*2)},{feather:40*e+.01});
  ctx.save();const g=ctx.createLinearGradient(0,0,0,wb+160);g.addColorStop(0,`rgba(0,0,0,${.45*e})`);g.addColorStop(1,'rgba(0,0,0,0)');ctx.fillStyle=g;ctx.fillRect(0,0,W,wb+160);ctx.restore();
  if(drop>0){const r=sbWindow(60,wy,W-120,h,{T,title,shadow:.5});if(draw){const keep=UIT;UIT=T;ctx.save();ctx.beginPath();ctx.rect(r.x,r.y,r.w,r.h);ctx.clip();
    ctx.translate(0,wy-top);draw(PB(a,z),{x:r.x,y:top+66,w:r.w,h:r.h});ctx.restore();UIT=keep}}
  ctx.save();ctx.shadowColor=`rgba(0,0,0,${.4*e})`;ctx.shadowBlur=50;ctx.shadowOffsetY=18;subject(k,sc,0,oy);ctx.restore()}
// Typing text with a caret, from beat a at cps characters a second (left-aligned at x, centred on y); returns the typed width. Use inside uiWorld/phone screens.
function uiType(text,x,y,a,cps=16,{size=42,col=UIT.ink,w8=400,caret=true}={}){const el=t-cS(a);if(el<0)return 0;const n=Math.min(text.length,Math.floor(el*cps)),s=text.slice(0,n);
  ctx.save();ctx.font=font(w8,size);ctx.letterSpacing='0px';ctx.textAlign='left';ctx.textBaseline='middle';ctx.fillStyle=col;ctx.fillText(s,x,y);const wd=ctx.measureText(s).width;
  const typing=n<text.length,on=typing||Math.floor((el-text.length/cps)*2.2)%2===0;   // solid while typing, blinks after
  if(caret&&on){ctx.fillStyle=C.accent;ctx.fillRect(x+wd+5,y-size*.56,Math.max(3,size*.075),size*1.12)}ctx.restore();return wd}
// Chat bubble popping in at beat a (springs from its tail corner). me:true = right side (x is its right edge), accent; else x is its left edge. y = top. Returns its height.
function uiBubble(text,x,y,a,{me=false,size=38,maxW=560,bg=null,fg=null}={}){const lines=wrap(text,400,size,maxW-size*1.5),lh=size*1.28;ctx.save();ctx.font=font(400,size);ctx.letterSpacing='0px';
  const tw=Math.max(...lines.map(l=>ctx.measureText(l).width)),w=tw+size*1.5,h=lines.length*lh+size*.95,bx=me?x-w:x,k=spring(a,{z:.6,w:13});
  if(k>0){const ax=me?x:x,ay=y+h,r=size*.75;ctx.globalAlpha=clamp(k*3);ctx.translate(ax,ay);ctx.scale(k,k);ctx.translate(-ax,-ay);
    ctx.beginPath();ctx.roundRect(bx,y,w,h,me?[r,r,r*.22,r]:[r,r,r,r*.22]);ctx.fillStyle=bg??(me?C.accent:UIT.bub);ctx.fill();
    ctx.fillStyle=fg??(me?'#fff':UIT.ink);ctx.textAlign='left';ctx.textBaseline='middle';lines.forEach((l,i)=>ctx.fillText(l,bx+size*.75,y+size*.475+lh*(i+.5)))}
  ctx.restore();return h}

// ── 2. frameBreak: the video shrinks into a floating post card over a blurred, darkened room; head and shoulders rise above the card's
// top edge and the arms reach past its sides; the card grows back to full frame by z.
// frameBreak(k,a,z,{s,x,y,cw,bottom,cut,handle,dim,r}): s = picture scale in the card, x/y = its shift (x>0 frees room for the handle), cw = card width, bottom = card's
// bottom edge, cut = where the card's top cuts the body (share of head height below the shoulder line).
function frameBreak(k,a,z,{s=.68,x=50,y=-10,cw=null,bottom=1480,cut=.12,handle=null,dim=.55,r=34}={}){cw??=Math.round(W*.72*s);const e=sbIO(a,z,.7,.7);if(e<=0){plate(k);return}
  const R=sbRef(k),top=H/2+(R.sh-H/2)*s+y+R.hh*s*cut,X=(W-cw)/2,sc=lerp(1,s,e),ox=lerp(0,x,e),oy=lerp(0,y,e),
    cx=lerp(0,X,e),cy=lerp(0,top,e),cwd=lerp(W,cw,e),ch=lerp(H,bottom-top,e),rr=lerp(0,r,e),ui=clamp((e-.55)/.45);
  sbBlur(()=>plate(k,1.1),30*e);ctx.save();ctx.fillStyle=`rgba(8,8,10,${dim*e})`;ctx.fillRect(0,0,W,H);ctx.restore();
  sbShadow(cx,cy,cwd,ch,rr,{alpha:.55*e,blur:80,dy:36});
  if(ui>0){ctx.save();ctx.globalAlpha=ui;const hy=top-44;   // handle row above the card: avatar, handle, more-dots
    ctx.fillStyle=C.accent;ctx.beginPath();ctx.arc(X+24,hy,24,0,TAU);ctx.fill();ctx.fillStyle='#fff';ctx.beginPath();ctx.arc(X+24,hy,18,0,TAU);ctx.fill();
    ctx.fillStyle='#9a958c';ctx.beginPath();ctx.arc(X+24,hy-4,7,0,TAU);ctx.fill();ctx.beginPath();ctx.arc(X+24,hy+14,11,Math.PI,TAU);ctx.fill();
    ctx.font=font(800,28);ctx.letterSpacing='0px';ctx.textAlign='left';ctx.textBaseline='middle';ctx.fillStyle='#fff';if(handle)ctx.fillText(handle,X+58,hy+1);
    for(let i=0;i<3;i++){ctx.beginPath();ctx.arc(X+cw-12-i*14,hy,4.5,0,TAU);ctx.fill()}
    const ay=bottom+48;ctx.strokeStyle='#fff';ctx.lineWidth=4;ctx.lineJoin='round';ctx.lineCap='round';   // action row under the card: like, comment, share, save
    ctx.beginPath();const hx=X+22;ctx.moveTo(hx,ay+14);ctx.bezierCurveTo(hx-26,ay-4,hx-14,ay-22,hx,ay-9);ctx.bezierCurveTo(hx+14,ay-22,hx+26,ay-4,hx,ay+14);ctx.stroke();
    ctx.beginPath();ctx.arc(X+86,ay-2,15,.6,TAU-.1);ctx.lineTo(X+103,ay+14);ctx.closePath();ctx.stroke();
    ctx.beginPath();ctx.moveTo(X+132,ay-14);ctx.lineTo(X+164,ay-14);ctx.lineTo(X+146,ay+14);ctx.closePath();ctx.stroke();
    ctx.beginPath();ctx.moveTo(X+cw-34,ay-16);ctx.lineTo(X+cw-10,ay-16);ctx.lineTo(X+cw-10,ay+16);ctx.lineTo(X+cw-22,ay+6);ctx.lineTo(X+cw-34,ay+16);ctx.closePath();ctx.stroke();ctx.restore()}
  ctx.save();ctx.beginPath();ctx.roundRect(cx,cy,cwd,ch,rr);ctx.clip();plate(k,sc,ox,oy);ctx.restore();
  if(e>0){ctx.save();ctx.strokeStyle=`rgba(255,255,255,${.9*e})`;ctx.lineWidth=6;ctx.beginPath();ctx.roundRect(cx+3,cy+3,cwd-6,ch-6,Math.max(0,rr-3));ctx.stroke();ctx.restore()}   // white post edge
  ctx.save();ctx.beginPath();ctx.rect(0,0,W,cy+ch);ctx.roundRect(cx,cy,cwd,ch,rr);ctx.clip('evenodd');   // the person's shadow only where they leave the card
  ctx.shadowColor=`rgba(0,0,0,${.5*e})`;ctx.shadowBlur=40;ctx.shadowOffsetY=16;subject(k,sc,ox,oy);ctx.restore();
  ctx.save();ctx.beginPath();ctx.rect(0,0,W,cy+ch);ctx.clip();subject(k,sc,ox,oy);ctx.restore();   // unclipped above the card and past its sides
  if(ui>0){ctx.save();ctx.globalAlpha=ui*.6;ctx.strokeStyle='rgba(255,255,255,.35)';ctx.lineWidth=2;ctx.beginPath();ctx.moveTo(cx+rr,cy+ch-1);ctx.lineTo(cx+cwd-rr,cy+ch-1);ctx.stroke();ctx.restore()}}

// ── 3. phoneMockup: a drawn phone (metal frame with thickness, bezel, notch, glass sheen) flies in beside the speaker in perspective and
// floats; its screen shows screen(p,w,h) drawn offscreen at screen size; taps=[[beat,x,y]] (x,y as 0–1 of the screen) show a touch and ripple.
// phoneMockup(k,a,z,{screen,side,taps,behind,w,h,x,y,tilt}): behind:true puts the phone between the room and the person.
function phoneMockup(k,a,z,{screen=null,side='right',taps=[],behind=false,w=360,h=760,x=null,y=null,tilt=16}={}){
  const out=clamp((t-(cS(z)-.55))/.55);if(b<a||out>=1){plate(k);return}
  const dir=side==='left'?-1:1,inK=spring(a,{z:.78,w:8.5}),sw=spring(a+.06,{z:.45,w:9}),o3=out*out*out,deg=Math.PI/180,
    cx=(x??(dir>0?W-70-w/2:70+w/2))+dir*((1-inK)*W*.8+o3*W*.8),cy=(y??H*.53)+Math.sin(t*1.7)*12+(1-inK)*140,
    th=(-dir*tilt+(1-sw)*-dir*58+o3*-dir*50+Math.sin(t*1.15)*2.5)*deg,ph=(Math.sin(t*.9+1)*3+(1-inK)*10)*deg,ps=(dir*(1-inK)*-8+Math.sin(t*.8)*1.2)*deg,F=1900,D=24,ins=20;
  const P=(px,py,pz)=>{const x1=px*Math.cos(th)-pz*Math.sin(th),z1=px*Math.sin(th)+pz*Math.cos(th),y2=py*Math.cos(ph)-z1*Math.sin(ph),z2=py*Math.sin(ph)+z1*Math.cos(ph),
    x3=x1*Math.cos(ps)-y2*Math.sin(ps),y3=x1*Math.sin(ps)+y2*Math.cos(ps),q=F/(F+z2);return[cx+x3*q,cy+y3*q]};
  const corners=pz=>[P(-w/2,-h/2,pz),P(w/2,-h/2,pz),P(w/2,h/2,pz),P(-w/2,h/2,pz)];
  const sw2=w-ins*2,sh2=h-ins*2,scr=sbInto(sbCanvas('phS',sw2,sh2),()=>{ctx.fillStyle='#FBFAF7';ctx.fillRect(0,0,sw2,sh2);if(screen)screen(PB(a,z),sw2,sh2);
    for(const[tb,tx,ty]of taps){const px=tx*sw2,py=ty*sh2,kd=PB(tb-.15,tb),ko=PB(tb+.1,tb+.55),kr=PB(tb,tb+.8);   // touch dot, then a ripple
      if(kd>0&&ko<1){ctx.fillStyle=`rgba(40,40,40,${.28*(1-ko)})`;ctx.beginPath();ctx.arc(px,py,30*E.outCubic(kd),0,TAU);ctx.fill();
        ctx.strokeStyle=`rgba(255,255,255,${.9*(1-ko)})`;ctx.lineWidth=3;ctx.stroke()}
      if(kr>0&&kr<1){ctx.strokeStyle=`rgba(255,90,54,${.8*(1-kr)})`;ctx.lineWidth=5;ctx.beginPath();ctx.arc(px,py,30+80*E.outExpo(kr),0,TAU);ctx.stroke()}}});
  const R0=58,face=sbInto(sbCanvas('phF',w,h),()=>{const m=ctx.createLinearGradient(0,0,w,h);m.addColorStop(0,'#E9EAEE');m.addColorStop(.45,'#9A9CA3');m.addColorStop(.7,'#D5D7DC');m.addColorStop(1,'#7A7C83');
    ctx.fillStyle=m;ctx.beginPath();ctx.roundRect(0,0,w,h,R0);ctx.fill();ctx.strokeStyle='rgba(255,255,255,.75)';ctx.lineWidth=2;ctx.beginPath();ctx.roundRect(1.5,1.5,w-3,h-3,R0-1);ctx.stroke();
    ctx.fillStyle='#050506';ctx.beginPath();ctx.roundRect(7,7,w-14,h-14,R0-6);ctx.fill();
    ctx.save();ctx.beginPath();ctx.roundRect(ins,ins,sw2,sh2,R0-ins+6);ctx.clip();ctx.drawImage(scr,ins,ins);
    const g=ctx.createLinearGradient(0,0,w,h*.7),q=clamp(.42-th*.9,.1,.9);g.addColorStop(0,'rgba(255,255,255,0)');g.addColorStop(Math.max(0,q-.14),'rgba(255,255,255,0)');
    g.addColorStop(q,'rgba(255,255,255,.16)');g.addColorStop(Math.min(1,q+.14),'rgba(255,255,255,0)');g.addColorStop(1,'rgba(255,255,255,0)');ctx.fillStyle=g;ctx.fillRect(0,0,w,h);ctx.restore();
    ctx.fillStyle='#050506';ctx.beginPath();ctx.roundRect(w/2-58,ins+16,116,34,17);ctx.fill();ctx.fillStyle='#1b2030';ctx.beginPath();ctx.arc(w/2+36,ins+33,7,0,TAU);ctx.fill()});
  const body=sbInto(sbCanvas('phB',w,h),()=>{const m=ctx.createLinearGradient(0,0,w,0);m.addColorStop(0,'#5E6066');m.addColorStop(.5,'#B9BBC1');m.addColorStop(1,'#55575D');
    ctx.fillStyle=m;ctx.beginPath();ctx.roundRect(0,0,w,h,R0);ctx.fill()});
  const draw=()=>{const C0=corners(0);ctx.save();ctx.filter='blur(34px)';ctx.fillStyle='rgba(0,0,0,.42)';ctx.translate(-dir*34,60);path(ctx,C0);ctx.fill();ctx.restore();   // soft cast shadow
    for(let i=0;i<=6;i++){const pz=D*(1-i/6);ctx.save();ctx.globalAlpha=1;quad(body,corners(pz),4);ctx.restore()}   // the metal edge: stacked silhouettes back to front
    ctx.save();ctx.fillStyle='rgba(0,0,0,.18)';path(ctx,corners(D*.15));ctx.restore();quad(face,C0,8)};
  if(behind)sandwich(k,draw);else{plate(k);draw()}}

// ── 4. pullBack: the video shrinks into a card inside a light app window (title bar, sidebar); a checklist of steps ticks off one by one,
// a timeline strip shows 'clips' (the current frame, cropped and tinted 5 ways) under a moving playhead, and a counter rolls up; back to full frame by z.
// pullBack(k,a,z,{steps,title,label}): steps = up to 6 short strings, ticked evenly between a+1.4 and z-1.4 beats.
function pullBack(k,a,z,{steps=['Step 1','Step 2','Step 3','Step 4'],title='Project',label='Done',listLabel='Checklist',timeLabel='Timeline'}={}){const e=sbIO(a,z,.8,.7);if(e<=0){plate(k);return}
  const T=sbTheme(false),wx=60,wy=330,ww=W-120,wh=1190,n=steps.length,ui=clamp((t-cS(a)-.45)/.4),tk=steps.map((_,i)=>a+1.4+i*Math.max(.5,(z-a-2.8)/Math.max(1,n-1)));
  ctx.save();const g=ctx.createLinearGradient(0,0,0,H);g.addColorStop(0,'#E4E0D8');g.addColorStop(1,'#CFCAC0');ctx.fillStyle=g;ctx.fillRect(0,0,W,H);ctx.restore();
  sbWindow(wx,wy,ww,wh,{T,title,shadow:.28});
  ctx.save();ctx.beginPath();ctx.roundRect(wx,wy,ww,wh,34);ctx.clip();ctx.fillStyle='#F3F1EC';ctx.fillRect(wx,wy+66,92,wh-66);ctx.fillStyle=T.line;ctx.fillRect(wx+92,wy+66,2,wh-66);   // sidebar with icon slots
  for(let i=0;i<6;i++){ctx.fillStyle=i===1?C.accent:'#DEDBD4';ctx.beginPath();ctx.roundRect(wx+25,wy+100+i*86,42,42,12);ctx.fill()}ctx.restore();
  const cX=190,cY=wy+100,cH=640,cW=cH*W/H,lx=cX+cW+46,rw=wx+ww-40-lx,fade=(d)=>clamp((t-cS(a)-.45-d)/.35);
  ctx.save();ctx.textBaseline='middle';ctx.textAlign='left';ctx.letterSpacing='2px';ctx.font=font(800,24);ctx.fillStyle=T.mute;ctx.globalAlpha=fade(0);if(listLabel)ctx.fillText(listLabel.toUpperCase(),lx,cY+18);ctx.restore();
  steps.forEach((s,i)=>{const yy=cY+82+i*86,al=fade(.1+i*.08);if(al<=0)return;const kk=spring(tk[i],{z:.5,w:16}),kc=PB(tk[i],tk[i]+.35),ks=PB(tk[i]+.15,tk[i]+.55);
    ctx.save();ctx.globalAlpha=al;ctx.translate((1-E.outCubic(al))*30,0);ctx.lineWidth=3;ctx.strokeStyle='#C9C5BC';ctx.beginPath();ctx.roundRect(lx,yy-21,42,42,11);ctx.stroke();
    if(kk>0){ctx.save();ctx.translate(lx+21,yy);ctx.scale(kk,kk);ctx.fillStyle=C.accent;ctx.beginPath();ctx.roundRect(-21,-21,42,42,11);ctx.fill();ctx.restore()}
    if(kc>0){ctx.strokeStyle='#fff';ctx.lineWidth=5;ctx.lineCap='round';ctx.lineJoin='round';ctx.setLineDash([60,60]);ctx.lineDashOffset=60*(1-kc);
      ctx.beginPath();ctx.moveTo(lx+11,yy+1);ctx.lineTo(lx+18,yy+9);ctx.lineTo(lx+32,yy-9);ctx.stroke();ctx.setLineDash([])}
    ctx.font=font(800,36);ctx.letterSpacing='-.5px';ctx.textAlign='left';ctx.textBaseline='middle';ctx.fillStyle=ks>0?`rgba(26,26,26,${lerp(1,.45,ks)})`:T.ink;
    const tw=ctx.measureText(s).width;ctx.fillText(s,lx+64,yy+2);if(ks>0){ctx.fillStyle='rgba(26,26,26,.5)';ctx.fillRect(lx+64,yy+1,tw*E.outCubic(ks),3)}ctx.restore()});
  {const ty=cY+82+n*86+10,al=label?fade(.4):0;if(al>0){ctx.save();ctx.globalAlpha=al;ctx.fillStyle=T.field;ctx.beginPath();ctx.roundRect(lx,ty,rw,150,22);ctx.fill();   // the counter tile
    ctx.font=font(800,22);ctx.letterSpacing='2px';ctx.fillStyle=T.mute;ctx.textAlign='left';ctx.textBaseline='middle';ctx.fillText(label.toUpperCase(),lx+28,ty+34);
    const rv=i=>Math.round(100*i/n),v=tk.reduce((s,c,i)=>s+(rv(i+1)-rv(i))*E.outCubic(PB(c,c+.6)),0);sbOdo(v,lx+26,ty+98,76,T.ink,{suffix:'%'});
    ctx.fillStyle='#E2DFD8';ctx.fillRect(lx+28,ty+136,rw-56,6);ctx.fillStyle=C.accent;ctx.fillRect(lx+28,ty+136,(rw-56)*v/100,6);ctx.restore()}}
  const im=FR['f'+k],ty=cY+cH+70,x0=cX,x1=wx+ww-40,crops=[[540,1000,1080],[490,760,520],[600,1700,560],[820,420,600],[500,1250,820]],
    filt=['none','grayscale(1)','saturate(1.5)','sepia(.55)','contrast(1.25) brightness(.92)'],tint=['rgba(255,90,54,.16)',null,'rgba(30,80,150,.18)',null,'rgba(0,0,0,.15)'],
    wid=[.2,.17,.24,.16,.23],ph=lerp(x0,x1,E.inOutCubic(PB(a+.8,z-1)));
  ctx.save();ctx.globalAlpha=fade(.2);ctx.font=font(800,24);ctx.letterSpacing='2px';ctx.fillStyle=T.mute;ctx.textAlign='left';ctx.textBaseline='middle';if(timeLabel)ctx.fillText(timeLabel.toUpperCase(),x0,ty);
  ctx.fillStyle='#CFCBC3';for(let i=0;i<=40;i++)ctx.fillRect(x0+(x1-x0)*i/40,ty+34,2,i%5?10:20);ctx.restore();
  let cx=x0;const gap=8,cw0=(x1-x0)-gap*4,clipY=ty+70,clipH=150;crops.forEach(([fx,fy,fw],i)=>{const cw=cw0*wid[i],kk=spring(a+.7+i*.12,{z:.7,w:14});
    if(kk>0&&im){ctx.save();ctx.translate(cx+cw/2,clipY+clipH/2);ctx.scale(kk,kk);ctx.translate(-cw/2,-clipH/2);ctx.beginPath();ctx.roundRect(0,0,cw,clipH,14);ctx.clip();
      const sw=Math.min(fw,1080),sh=sw*clipH/cw;ctx.filter=filt[i];ctx.drawImage(im,clamp(fx-sw/2,0,1080-sw),clamp(fy-sh/2,0,1920-sh),sw,sh,0,0,cw,clipH);ctx.filter='none';
      if(tint[i]){ctx.fillStyle=tint[i];ctx.fillRect(0,0,cw,clipH)}const on=ph>=cx&&ph<cx+cw;ctx.lineWidth=on?6:2;ctx.strokeStyle=on?C.accent:'rgba(0,0,0,.12)';
      ctx.beginPath();ctx.roundRect(0,0,cw,clipH,14);ctx.stroke();ctx.restore()}cx+=cw+gap});
  {const al=fade(.35);if(al>0){ctx.save();ctx.globalAlpha=al;const r=rng(9),wy2=clipY+clipH+60;ctx.fillStyle='#BDB8AE';   // an audio track under the clips
    for(let x=x0;x<x1;x+=9){const v=(.25+.75*r())*(.55+.45*Math.sin(x*.02));ctx.fillRect(x,wy2-v*34,5,v*68)}
    ctx.fillStyle=C.accent;ctx.fillRect(ph-2,ty+26,4,wy2+44-ty-26);ctx.beginPath();ctx.arc(ph,ty+26,11,0,TAU);ctx.fill();ctx.restore()}}
  const X=lerp(0,cX,e),Y=lerp(0,cY,e),Wd=lerp(W,cW,e),Hd=lerp(H,cH,e),rr=lerp(0,26,e);sbShadow(X,Y,Wd,Hd,rr,{alpha:.3*e,blur:50,dy:20});
  ctx.save();ctx.beginPath();ctx.roundRect(X,Y,Wd,Hd,rr);ctx.clip();plate(k,Hd/H,X+Wd/2-W/2,Y+Hd/2-H/2);ctx.restore()}

// ── 5. greenScreen: the speaker is cut out and shrinks to the bottom of the frame (bottom-anchored, ~55%); behind, the frame becomes the
// author's media as a big rounded card on a plain wallpaper, with an optional credit pill. Eases in at a and back to the plain shot by z.
// greenScreen(k,a,z,{media,wallpaper,credit,s,clean}): media = IMG key, image/canvas, or (w,h)=>draw; clean = IMG key of the empty room (default k+'_clean').
function greenScreen(k,a,z,{media=null,wallpaper='#ECE8E1',credit=null,s=.55,clean=null}={}){const e=sbIO(a,z,.8,.7);if(e<=0){plate(k);return}
  const R=sbRef(k),sc=lerp(1,s,e),oy=H/2*(1-sc),hT=H+(R.top-H)*s,cardB=hT+R.hh*s*.75,cX=80,cY=268,cW=W-160,cH=cardB-cY;
  ctx.save();ctx.fillStyle=wallpaper;ctx.fillRect(0,0,W,H);const g=ctx.createRadialGradient(W/2,H*.4,0,W/2,H*.4,H*.8);g.addColorStop(0,'rgba(255,255,255,.35)');g.addColorStop(1,'rgba(0,0,0,.10)');
  ctx.fillStyle=g;ctx.fillRect(0,0,W,H);ctx.restore();
  const room=(clean?IMG[clean]:cleanImg(k));sbBlur(()=>room?cover(room,1+.06*e):plate(k,1+.06*e),22*e,{alpha:1-e});
  const kc=Math.min(spring(a+.2,{z:.78,w:10}),E.inOutCubic(clamp((cS(z)-t)/.55)));
  if(kc>0){ctx.save();ctx.globalAlpha=clamp(kc*2);ctx.translate(W/2,cY+cH/2+(1-kc)*120);ctx.scale(lerp(.9,1,kc),lerp(.9,1,kc));ctx.translate(-W/2,-(cY+cH/2));
    sbShadow(cX,cY,cW,cH,40,{alpha:.35,blur:70,dy:30});ctx.save();ctx.beginPath();ctx.roundRect(cX,cY,cW,cH,40);ctx.clip();ctx.fillStyle='#fff';ctx.fillRect(cX,cY,cW,cH);
    sbMedia(media,cX,cY,cW,cH);ctx.restore();ctx.strokeStyle='rgba(255,255,255,.5)';ctx.lineWidth=2;ctx.beginPath();ctx.roundRect(cX+1,cY+1,cW-2,cH-2,39);ctx.stroke();
    if(credit){const kp=spring(a+.7,{z:.6,w:14});if(kp>0){ctx.font=font(800,26);ctx.letterSpacing='0px';const tw=ctx.measureText(credit).width,px=cX+28,py=cY+28,pw=tw+44,phh=52;
      ctx.save();ctx.translate(px,py+phh/2);ctx.scale(kp,kp);ctx.fillStyle='rgba(12,12,14,.72)';ctx.beginPath();ctx.roundRect(0,-phh/2,pw,phh,phh/2);ctx.fill();
      ctx.fillStyle='#fff';ctx.textAlign='left';ctx.textBaseline='middle';ctx.fillText(credit,22,1);ctx.restore()}}ctx.restore()}
  ctx.save();ctx.shadowColor=`rgba(0,0,0,${.35*e})`;ctx.shadowBlur=40;ctx.shadowOffsetY=-6;subject(k,sc,0,oy);ctx.restore()}

// ── 6. coverStory: the shot becomes a magazine cover: a hairline border draws on, the picture pushes in 3%, a tall condensed masthead rises
// BEHIND the head (the head overlaps its lower part), cover labels pop in at the sides, and an italic cover line lands on punchBeat.
// coverStory(k,a,z,{masthead,lines,coverLine,punchBeat,col,ink,issue}): lines = up to 4 labels, each 'text' or ['KICKER','text'].
function coverStory(k,a,z,{masthead='STUDIO',lines=[],coverLine='',punchBeat=null,col=C.accent,ink='#FFFFFF',issue=null}={}){const e=sbIO(a,z,.5,.6);if(e<=0){plate(k);return}
  const R=sbRef(k),s=1+.03*Math.min(E.inOutCubic(PB(a,z)),e),hT=H/2+(R.top-H/2)*s,eo=E.inOutCubic(clamp((cS(z)-t)/.6)),pb=punchBeat??lerp(a,z,.55);
  const M=masthead.toUpperCase(),ch=[...M],cond=.74,trk=.07;ctx.save();ctx.font=font(800,100);ctx.letterSpacing='0px';
  const cw=ch.map(c=>ctx.measureText(c).width/100),capR=ctx.measureText('H').actualBoundingBoxAscent/100;ctx.restore();
  let size=880/(cond*(cw.reduce((p,q)=>p+q,0)+trk*(ch.length-1)));size=Math.min(size,(hT-300)/(.72*capR));
  const capH=capR*size,base=hT+.28*capH,capT=base-capH,tot=size*(cw.reduce((p,q)=>p+q,0)+trk*(ch.length-1));
  sandwich(k,()=>{ctx.save();ctx.beginPath();ctx.rect(0,capT-30,W,capH+40);ctx.clip();ctx.translate(W/2,base);ctx.scale(cond,1);
    ctx.font=font(800,size);ctx.letterSpacing='0px';ctx.textAlign='left';ctx.textBaseline='alphabetic';ctx.fillStyle=col;let x=-tot/2;
    ch.forEach((c,i)=>{const kk=Math.min(E.outExpo(PB(a+.2+i*.05,a+.9+i*.05)),eo);if(kk>0)ctx.fillText(c,x,(1-kk)*capH*1.2);x+=size*(cw[i]+trk)});ctx.restore()},{s});
  const L=2*(960+1320),kb=E.inOutCubic(PB(a,a+1.3))*e;if(kb>0){ctx.save();ctx.strokeStyle=ink;ctx.lineWidth=2.5;ctx.shadowColor='rgba(0,0,0,.4)';ctx.shadowBlur=6;
    ctx.setLineDash([L*kb,L]);ctx.beginPath();ctx.moveTo(540,250);ctx.lineTo(1020,250);ctx.lineTo(1020,1570);ctx.lineTo(60,1570);ctx.lineTo(60,250);ctx.closePath();ctx.stroke();ctx.restore()}
  const sh=(f)=>{ctx.shadowColor='rgba(0,0,0,.75)';ctx.shadowBlur=22;f();ctx.shadowBlur=0};
  if(issue){const ki=clamp((t-cS(a)-.3)/.4)*e;if(ki>0){ctx.save();ctx.globalAlpha=ki;ctx.font=font(800,24);ctx.letterSpacing='4px';ctx.fillStyle=ink;ctx.textBaseline='middle';
    ctx.textAlign='left';sh(()=>ctx.fillText(issue.toUpperCase(),84,286));ctx.restore()}}
  const slots=[[0,base+120],[1,base+170],[0,base+330],[1,base+380]];lines.slice(0,4).forEach((ln,i)=>{const[kick,txt]=Array.isArray(ln)?ln:[null,ln],[side,yy]=slots[i],
    kk=Math.min(spring(a+1+i*.4,{z:.62,w:13}),eo);if(kk<=0)return;const x=side?1000:80,al=side?'right':'left';ctx.save();ctx.globalAlpha=clamp(kk*2);
    ctx.translate((side?1:-1)*(1-Math.min(1,kk))*60,0);ctx.textAlign=al;ctx.textBaseline='alphabetic';let y2=yy;
    if(kick){ctx.font=font(800,24);ctx.letterSpacing='3px';ctx.fillStyle=col;sh(()=>ctx.fillText(kick.toUpperCase(),x,y2));y2+=48}
    ctx.font=font(800,42);ctx.letterSpacing='-1px';ctx.fillStyle=ink;wrap(txt,800,42,230).forEach(l=>{sh(()=>ctx.fillText(l,x,y2));y2+=46});ctx.restore()});
  if(coverLine){const kl=PB(pb,pb+.35),ko=eo;if(kl>0&&ko>0){const sz=fit(coverLine,800,840,104),yy=1440,sc=lerp(1.6,1,E.outExpo(kl));halo(yy,clamp(kl*3)*ko*.8);
    ctx.save();ctx.globalAlpha=clamp(kl*4)*ko;ctx.translate(W/2,yy);ctx.scale(sc,sc);ctx.transform(1,0,-.2,1,0,0);ctx.font=font(800,sz);ctx.letterSpacing='-2px';ctx.textAlign='center';
    ctx.textBaseline='middle';ctx.fillStyle=ink;sh(()=>ctx.fillText(coverLine,0,0));const uw=ctx.measureText(coverLine).width*E.outCubic(PB(pb+.2,pb+.7));
    ctx.fillStyle=col;ctx.fillRect(-uw/2,sz*.62,uw,8);ctx.restore()}}}

// ═══ Looks: camera and stylised looks (references/studio-looks.md)

const SC={cv:{}};
SC.c=n=>SC.cv[n]??=(()=>{const c=mk();return[c,c.getContext('2d')]})();   // own scratch canvases (never fx/layer, which subject/sticker use)
SC.at=(tt,f)=>{const keep=t;t=tt;try{return f()}finally{t=keep}};          // run f() as if the film were at time tt (restores t)
// Steady head measurements: the matte's per-frame neck reading jumps, so the head height is the shot's median and the rest are
// averaged over ±r shot frames. at = film time in seconds (default now). Returns {cx,cy,top,hh,sh,chest:[x,y]}.
SC.hh={};
SC.head=(k,{r=5,at}={})=>{const I=shotInfo(k);if(!I)return{cx:W/2,cy:H*.35,top:H*.25,hh:H*.17,sh:H*.5,chest:[W/2,H*.6]};
  const F=I.f,hh=SC.hh[k]??=(()=>{const v=F.map(f=>f[2]-f[0]).sort((p,q)=>p-q);return v[v.length>>1]})(),
    i=at==null?shotIdx(k)-1:SC.at(at,()=>shotIdx(k)-1);let cx=0,top=0,sh=0,n=0;
  for(let j=Math.max(0,i-r);j<=Math.min(F.length-1,i+r);j++){cx+=F[j][1];top+=F[j][0];sh+=F[j][3];n++}cx/=n;top/=n;sh/=n;
  return{cx,top,hh,sh,cy:top+hh/2,chest:[cx,sh+hh*.6]}};

// ── 1. Digital zoom on the face. faceZoom(k, keys, {max=1.6, draw, blur=1}) → current scale
// keys = [[beat,'creep'|'snap'|'out',scale],…]: creep eases toward scale (default +0.12) until the next key; snap lands in 5 frames with a
// zoom blur; out whips back (default to 1) in 7 frames with motion blur. Aimed at the face, kept inside the frame, never above max.
function faceZoom(k,keys,{max=1.6,draw=()=>plate(k),blur=1}={}){
  const T=keys.map(([c,kind,v])=>[cS(c),kind,v]);
  const sAt=x=>{let v=1;for(let i=0;i<T.length;i++){const[a,kind,amt]=T[i];if(x<a)return v;const nx=T[i+1]?.[0]??Infinity,v0=v,
      tg=clamp(amt??(kind==='out'?1:kind==='snap'?1.35:v0+.12),1,max),
      d=kind==='snap'?5/FPS:kind==='out'?7/FPS:Math.max(.4,Math.min(nx-a,4)),ez=kind==='snap'?E.outExpo:kind==='out'?E.inOutCubic:(q=>.5-.5*Math.cos(Math.PI*q)),
      f=x2=>lerp(v0,tg,ez(clamp((x2-a)/d)));if(x<nx)return f(x);v=f(nx)}return v};
  const s=sAt(t),h=SC.head(k,{r:6}),hw=W/2/s,hh2=H/2/s,fx=clamp(h.cx,hw,W-hw),fy=clamp(h.cy+H*.1/s,hh2,H-hh2);   // face a little above centre
  ctx.save();ctx.translate(W/2,H/2);ctx.scale(s,s);ctx.translate(-fx,-fy);draw();ctx.restore();
  const v=Math.abs(s-sAt(t-1/FPS)),amt=Math.min(.45,v*1.6)*blur;            // blur follows the zoom's speed: snaps and whips smear, creeps stay sharp
  if(amt>.01)zoomBlur(W/2+(h.cx-fx)*s,H/2+(h.cy-fy)*s,amt,14);return s}

// ── 2. Zoom-through cut. zoomThroughCut(k, cutBeat, {into, len=9, depth=3.2, col}) → true while active
// Post edit, called in BOTH scenes around the cut, always with the OUTGOING shot k: before the cut the frame dives into a dark point on the
// speaker (default the shirt, head(k).chest at the cut) as a radial blur builds and a dark portal swells; after it the incoming frame opens
// out of the same point through the portal, zooming down from depth to 1 as the blur clears. len = frames each side.
function zoomThroughCut(k,cut,{into,len=9,depth=3.2,col='#07070a'}={}){const tc=cS(cut),f=(t-tc)*FPS;if(f<-len||f>=len)return false;
  const[x,y]=into??SC.head(k,{at:tc-.5/FPS}).chest,before=f<0,p=before?1+f/len:f/len,R=Math.hypot(W,H),rgb=rgbOf(col);
  if(before){const q=p*p*p,z=1+(depth-1)*q;post(s=>about(x,y,z,()=>ctx.drawImage(s,0,0)));zoomBlur(x,y,.5*p*p,14);
    const r=lerp(30,R*1.15,q),g=ctx.createRadialGradient(x,y,0,x,y,r);g.addColorStop(0,`rgba(${rgb},${clamp(p*2)})`);
    g.addColorStop(.45,`rgba(${rgb},${clamp(p*1.6)})`);g.addColorStop(1,`rgba(${rgb},0)`);
    ctx.save();ctx.setTransform(1,0,0,1,0,0);ctx.fillStyle=g;ctx.fillRect(0,0,W,H);ctx.restore()}
  else{const e=E.outCubic(p),z=depth-(depth-1)*e,r=R*1.15*p**1.4+24;
    post(s=>{ctx.fillStyle=col;ctx.fillRect(0,0,W,H);masked(()=>about(x,y,z,()=>ctx.drawImage(s,0,0)),c=>{c.beginPath();c.arc(x,y,r,0,TAU)},{feather:30+r*.08})});
    zoomBlur(x,y,.5*(1-p)**2,14)}
  return true}

// ── 3. Paper cut-out collage. paperCut(k, a, z, {words, palette, seed=4, sheets=4, y=H*.8, size=150, tear=1}) → true while active
// From beat a torn paper sheets slide over the room, the speaker becomes a white-edged paper cut-out that steps at 12 fps (the footage keeps
// its 30 fps frames: each 12 fps step gets a new seeded nudge and tilt, so the cut-out reads as stop-motion), the words slam down as ransom-note
// letters; at z the collage tears in two and the halves pull apart over `tear` beats to reveal the plain shot. Draws plate(k) outside a…z+tear.
SC.PAL=['#EBDDC2','#F2B544','#E4572E','#2E5266','#9CC5A1','#D9D0C1'];
SC.paperTex=null;
SC.paper=()=>SC.paperTex??=(()=>{const c=document.createElement('canvas');c.width=c.height=384;const g=c.getContext('2d'),r=rng(91),d=g.createImageData(384,384);
  for(let i=0;i<d.data.length;i+=4){const v=200+r()*55;d.data[i]=d.data[i+1]=d.data[i+2]=v;d.data[i+3]=255}g.putImageData(d,0,0);
  g.filter='blur(1.2px)';g.drawImage(c,0,0);g.filter='none';g.lineCap='round';   // soft mottling, then a few fibres
  for(let i=0;i<260;i++){const x=r()*384,y=r()*384,a=r()*TAU,l=6+r()*18;g.strokeStyle=r()<.5?'rgba(255,255,255,.5)':'rgba(120,110,95,.25)';g.lineWidth=.6+r()*.8;
    g.beginPath();g.moveTo(x,y);g.quadraticCurveTo(x+Math.cos(a+.6)*l*.5,y+Math.sin(a+.6)*l*.5,x+Math.cos(a)*l,y+Math.sin(a)*l);g.stroke()}return c})();
// A torn line from (x0,y0) to (x1,y1): seeded jagged points (fine tooth + slow wander), amp in px
SC.tornLine=(x0,y0,x1,y1,seed,amp=10,step=12)=>{const r=rng(seed),L=Math.hypot(x1-x0,y1-y0),n=Math.max(2,Math.round(L/step)),nx=-(y1-y0)/L,ny=(x1-x0)/L,
  p1=r()*TAU,p2=r()*TAU,P=[];for(let i=0;i<=n;i++){const q=i/n,o=(i&&i<n)?amp*(.55*(r()-.5)*2+.3*Math.sin(q*9+p1)+.25*Math.sin(q*23+p2)):0;
    P.push([lerp(x0,x1,q)+nx*o,lerp(y0,y1,q)+ny*o])}return P};
// A paper sheet w×h centred on 0,0 with torn long edges: [white core outline, coloured face outline]
SC.sheet=(w,h,seed)=>{const top=c=>SC.tornLine(-w/2,-h/2+c,w/2,-h/2+c,seed+c,9),bot=c=>SC.tornLine(w/2,h/2-c,-w/2,h/2-c,seed*3+c,9);
  return[[...top(-7),...bot(-7)],[...top(0),...bot(0)]]};
SC.fillPaper=(g,P,col,tex=.55)=>{path(g,P);g.fillStyle=col;g.fill();g.save();path(g,P);g.clip();g.globalCompositeOperation='multiply';g.globalAlpha=tex;
  g.fillStyle=g.createPattern(SC.paper(),'repeat');g.fillRect(-W*2,-H*2,W*4,H*4);g.restore()};
const PC_FONTS=[[800,'Brand'],[400,'Brand'],['bold','Georgia, serif'],['italic bold','"Times New Roman", serif'],['normal','Impact, sans-serif'],['bold','"Courier New", monospace'],['900','"American Typewriter", serif']];
function paperCut(k,a,z,{words='',palette=SC.PAL,seed=4,sheets=4,y=H*.7,size=150,tear=1,letterCase='mixed'}={}){
  if(b<a||b>=z+tear){plate(k);return false}
  const[cg,g]=SC.c('paper'),[cl,gl]=SC.c('ransom'),r=rng(seed),h=SC.head(k);
  for(const c of[g,gl]){c.setTransform(1,0,0,1,0,0);c.globalAlpha=1;c.filter='none';c.clearRect(0,0,W,H)}
  // sheets (canvas cg): overlapping torn bands, alternating sides, slight tilts; together they cover the frame
  const n=clamp(sheets,3,5);for(let i=0;i<n;i++){const ki=E.outBack(PB(a+i*.16,a+i*.16+.6)),dir=i%2?1:-1,rot=(r()-.5)*.13,hb=H/n*1.55,cy=(i+.5)*H/n+(r()-.5)*40,
      [core,face]=SC.sheet(W*1.7,hb,seed*31+i*7);if(ki<=0)continue;
    g.save();g.translate(W/2+dir*W*1.8*(1-ki),cy);g.rotate(rot+dir*.12*(1-ki));g.shadowColor='rgba(0,0,0,.35)';g.shadowBlur=26;g.shadowOffsetY=10;
    path(g,core);g.fillStyle='#FBF8F1';g.fill();g.shadowColor='transparent';SC.fillPaper(g,face,palette[i%palette.length]);g.restore()}
  // ransom-note words (canvas cl): one paper tile per letter, slammed down one after another
  if(words){const L=[];let line=[],lw=0;const lr=rng(seed*13+5),S=size,maxW=W*.88;
    const mkL=ch=>{const[fw,ff]=PC_FONTS[Math.floor(lr()*PC_FONTS.length)],sz=S*(.82+lr()*.36),up=lr()<.75,c=letterCase==='as-is'?ch:letterCase==='upper'||(letterCase==='mixed'&&up)?ch.toUpperCase():ch.toLowerCase();
      gl.font=`${fw} ${sz}px ${ff}`;gl.letterSpacing='0px';const m=gl.measureText(c).width,dark=lr()<.4,
      bg=dark?['#151515','#2E5266','#B8322A'][Math.floor(lr()*3)]:['#FFFFFF','#F4EBD6','#F2B544','#E9E2D2','#9CC5A1'][Math.floor(lr()*5)];
      return{c,fw,ff,sz,w:m+sz*.28,h:sz*1.08,bg,ink:dark?(lr()<.7?'#F4F1EA':'#F2B544'):(lr()<.75?'#111':'#C0392B'),rot:(lr()-.5)*.28,dy:(lr()-.5)*S*.14,jit:lr()}};
    for(const wd of words.split(/\s+/).filter(Boolean)){const ls=[...wd].map(mkL),ww=ls.reduce((s2,q)=>s2+q.w*.98,0);
      if(line.length&&lw+S*.32+ww>maxW){L.push([line,lw]);line=[];lw=0}if(line.length){line.push(null);lw+=S*.32}line.push(...ls);lw+=ww}
    if(line.length)L.push([line,lw]);const big=Math.max(...L.map(([,v])=>v)),fs=Math.min(1,maxW/big),LH=S*1.3*fs;let idx=0;
    L.forEach(([ln,wid],li)=>{let x=W/2-wid*fs/2;const yy=y+(li-(L.length-1)/2)*LH;
      for(const q of ln){if(!q){x+=S*.32*fs;continue}const a0=a+.75+idx++*.075,kq=PB(a0,a0+.22);
        if(kq>0){const sc=fs*lerp(2.3,1,E.outBack(kq)),cx=x+q.w*fs*.49;gl.save();gl.globalAlpha=clamp(kq*4);gl.translate(cx,yy+q.dy*fs);gl.rotate(q.rot+(1-E.outCubic(kq))*.5*(q.jit-.5));gl.scale(sc,sc);
          gl.shadowColor='rgba(0,0,0,.4)';gl.shadowBlur=10;gl.shadowOffsetY=5;const hw=q.w/2,hh=q.h/2,j=(q.jit-.5)*6;
          path(gl,[[-hw+j,-hh],[hw,-hh-j*.6],[hw-j*.4,hh],[-hw,hh+j*.5]]);gl.fillStyle=q.bg;gl.fill();gl.shadowColor='transparent';
          gl.font=`${q.fw} ${q.sz}px ${q.ff}`;gl.textAlign='center';gl.textBaseline='middle';gl.fillStyle=q.ink;gl.fillText(q.c,0,q.sz*.04);gl.restore()}
        x+=q.w*fs*.98}})}
  // the tear from z: a jagged line top to bottom; each half swings about its bottom corner (so the rip opens from the top) and slides away.
  // Paper only: the speaker stays on top and turns back from cut-out to footage as the paper goes.
  const q=PB(z,z+tear),tl=SC.tornLine(W*.53,-60,W*.47,H+60,seed*977,22,16),tw=SC.tornLine(W*.53,-60,W*.47,H+60,seed*977+1,22,16),
    ang=.42*q**1.6,dx=W*.95*q**2.2,
    torn=(im,core)=>{if(q<=0){ctx.drawImage(im,0,0);return}for(const s of[-1,1]){const ex=s<0?-W:2*W,ox=s<0?0:W,
        edge=[[ex,-60],...tl,[ex,H+60]],cp=[[ex,-60],...tw.map(([u,v],i)=>[u-s*(5+(i%3)*2),v]),[ex,H+60]];
      ctx.save();ctx.translate(ox+s*dx,H);ctx.rotate(s*ang);ctx.translate(-ox,-H);
      if(core){ctx.shadowColor='rgba(0,0,0,.45)';ctx.shadowBlur=40;path(ctx,cp);ctx.fillStyle='#FBF8F1';ctx.fill();ctx.shadowColor='transparent'}
      path(ctx,edge);ctx.clip();ctx.drawImage(im,0,0);ctx.restore()}};
  plate(k);ctx.save();ctx.setTransform(1,0,0,1,0,0);torn(cg,true);
  // the speaker as a paper cut-out: white edge grows in, then a seeded nudge and tilt per 12 fps step
  const st=Math.floor(t*12),w=rng(st*7919+seed),on=IN(a,.4,E.outCubic)*(1-E.inOutCubic(PB(z,z+tear*.6))),px=h.cx,py=h.sh+h.hh;
  if(on>.001){ctx.save();ctx.translate(px,py);ctx.rotate((w()-.5)*.022*on);ctx.translate(-px+(w()-.5)*7*on,-py+(w()-.5)*7*on);
    ctx.shadowColor=`rgba(0,0,0,${.4*on})`;ctx.shadowBlur=30;ctx.shadowOffsetY=14;sticker(k,{stroke:15*on});ctx.restore()}
  else subject(k);
  torn(cl,false);ctx.restore();return true}

// ── 4. Chalk outline and doodles that boil. doodleBoil(k, a, z, {doodles, col, seed=7, width=14, gap=12, out=.7}) → true while active
// From beat a a chalk line traces round the speaker (from the matte, swept on in 0.8 beat) and redraws every 2 frames with a seeded jitter;
// doodles = [[kind, beat, dx, dy, scale],…] draw on along their path from their beat, at dx,dy head-heights from the head centre (fixed
// where the head was at that beat), scale in head-heights. kinds: star arrow underline circle rays sparkle spiral heart. Rubs out from z.
SC.DOODLE={star:()=>[[...Array(6)].map((_,i)=>{const an=-Math.PI/2+i*TAU*2/5;return[.5*Math.cos(an),.5*Math.sin(an)]})],
  arrow:()=>{const P=[...Array(24)].map((_,i)=>{const q=i/23;return[lerp(-.5,.42,q),.25-.5*q+.18*Math.sin(q*Math.PI)]});return[P,[[.2,-.22],[.42,-.25],[.36,-.03]]]},
  underline:()=>[[...Array(24)].map((_,i)=>{const q=i/23;return[lerp(-.5,.5,q),.03*Math.sin(q*TAU*1.2)+.04*q]}),[...Array(16)].map((_,i)=>{const q=i/15;return[lerp(.38,-.42,q),.1+.02*Math.sin(q*7)]})],
  circle:()=>[[...Array(48)].map((_,i)=>{const an=-1.9+i/47*TAU*1.12,rr=1+.06*Math.sin(an*2.3);return[.5*rr*Math.cos(an),.47*rr*Math.sin(an)]})],
  rays:()=>[...Array(7)].map((_,i)=>{const an=Math.PI*(-1.08+i/6*1.16),c=Math.cos(an),s=Math.sin(an),o=.4+.04*(i%2);return[[o*c,o*s],[(o+.12)*c,(o+.12)*s]]}),
  sparkle:()=>[[[0,-.5],[.07,-.07],[.5,0],[.07,.07],[0,.5],[-.07,.07],[-.5,0],[-.07,-.07],[0,-.5]]],
  spiral:()=>[[...Array(60)].map((_,i)=>{const q=i/59,an=q*TAU*2.4;return[.5*q*Math.cos(an),.5*q*Math.sin(an)]})],
  heart:()=>[[...Array(48)].map((_,i)=>{const u=i/47*TAU,s=Math.sin(u);return[16*s*s*s/34,-(13*Math.cos(u)-5*Math.cos(2*u)-2*Math.cos(3*u)-Math.cos(4*u))/34-.05]})]};
SC.chalkTex=null;
SC.chalk=()=>SC.chalkTex??=(()=>{const c=document.createElement('canvas');c.width=c.height=256;const g=c.getContext('2d'),r=rng(29),d=g.createImageData(256,256);
  for(let i=0;i<d.data.length;i+=4){const v=r();d.data[i]=d.data[i+1]=d.data[i+2]=255;d.data[i+3]=v<.12?0:v<.24?110:190+v*65}g.putImageData(d,0,0);return c})();
function doodleBoil(k,a,z,{doodles=[],col='#F4F1EA',seed=7,width=14,gap=12,out=.7}={}){plate(k);if(b<a||b>=z+out)return false;
  const mm=FR['m'+k],[cc,g]=SC.c('chalk'),[cr,gr]=SC.c('ring'),st=Math.floor(fi()/2),r=rng(st*131+seed),h=SC.head(k,{r:6});
  g.setTransform(1,0,0,1,0,0);g.globalCompositeOperation='source-over';g.globalAlpha=1;g.filter='none';g.clearRect(0,0,W,H);
  // outline: matte grown by gap+width minus matte grown by gap = a ring round the body, re-jittered every 2 frames
  if(mm){gr.setTransform(1,0,0,1,0,0);gr.globalCompositeOperation='source-over';gr.clearRect(0,0,W,H);const wd=width*(.8+.45*r()),N=16;
    for(let i=0;i<N;i++)gr.drawImage(mm,Math.cos(i/N*TAU)*(gap+wd),Math.sin(i/N*TAU)*(gap+wd),W,H);
    gr.globalCompositeOperation='destination-out';for(let i=0;i<N;i++)gr.drawImage(mm,Math.cos(i/N*TAU)*gap,Math.sin(i/N*TAU)*gap,W,H);
    gr.globalCompositeOperation='source-in';gr.fillStyle=col;gr.fillRect(0,0,W,H);gr.globalCompositeOperation='source-over';
    const sw=E.inOutCubic(PB(a,a+.8)),ox=h.cx,oy=(h.top+H)/2,js=1+(r()-.5)*.012;
    if(sw>0){g.save();g.beginPath();g.moveTo(ox,oy);g.arc(ox,oy,H*1.5,-Math.PI/2,-Math.PI/2+TAU*sw+.001);g.closePath();g.clip();
      g.translate(ox+(r()-.5)*7,oy+(r()-.5)*7);g.scale(js,js);g.translate(-ox,-oy);g.drawImage(cr,0,0);g.restore()}}
  // doodles, drawn on along their path, boiling with a smooth per-step warp
  g.lineCap='round';g.lineJoin='round';g.strokeStyle=col;
  doodles.forEach(([kind,c0,dx=0,dy=0,sc=1],di)=>{const q=PB(c0,c0+.6);if(q<=0||!SC.DOODLE[kind])return;const H0=SC.head(k,{r:6,at:cS(c0)}),S=sc*H0.hh,
      x0=H0.cx+dx*H0.hh,y0=H0.cy+dy*H0.hh,R=rng(st*977+di*61+seed),p1=R()*TAU,p2=R()*TAU,A=2.6,tx=(R()-.5)*5,ty=(R()-.5)*5,
      P=SC.DOODLE[kind]().map(s=>s.map(([u,v])=>[x0+u*S+tx+A*Math.sin(v*9+p1),y0+v*S+ty+A*Math.sin(u*9+p2)])),
      len=P.map(s=>s.reduce((acc,p,i)=>i?acc+Math.hypot(p[0]-s[i-1][0],p[1]-s[i-1][1]):0,0)),tot=len.reduce((x,y)=>x+y,0);
    let left=E.outCubic(q)*tot;const lw=clamp(S*.028,5,11);
    for(const[pi,s]of P.entries()){if(left<=0)break;g.beginPath();g.moveTo(...s[0]);let acc=0;
      for(let i=1;i<s.length;i++){const sl=Math.hypot(s[i][0]-s[i-1][0],s[i][1]-s[i-1][1]);if(acc+sl>=left){const f=(left-acc)/sl;g.lineTo(lerp(s[i-1][0],s[i][0],f),lerp(s[i-1][1],s[i][1],f));acc+=sl;break}
        g.lineTo(...s[i]);acc+=sl}left-=len[pi];g.globalAlpha=.55;g.lineWidth=lw*1.5;g.stroke();g.globalAlpha=1;g.lineWidth=lw*.8;g.stroke()}});
  g.globalAlpha=1;
  // chalk grain (re-seeded every step), then the rub-out: eraser zigzags plus a fading haze of dust
  g.globalCompositeOperation='destination-in';g.save();g.translate(-r()*256,-r()*256);g.fillStyle=g.createPattern(SC.chalk(),'repeat');g.fillRect(0,0,W+256,H+256);g.restore();
  const ro=PB(z,z+out);if(ro>0){g.globalCompositeOperation='destination-out';g.lineWidth=220;g.strokeStyle='#000';g.beginPath();const rows=9,tot=rows*W,go=E.inOutCubic(ro)*tot*1.05;
    let done=0,X=-60,Y=H*.08;g.moveTo(X,Y);for(let i=0;i<rows&&done<go;i++){const nx=i%2?-60:W+60,ny=Y+H*.105,sl=Math.hypot(nx-X,ny-Y),f=Math.min(1,(go-done)/sl);
      X=lerp(X,nx,f);Y=lerp(Y,ny,f);g.lineTo(X,Y);done+=sl}g.stroke()}
  g.globalCompositeOperation='source-over';
  ctx.save();ctx.setTransform(1,0,0,1,0,0);if(ro>0){ctx.globalAlpha=.35*Math.sin(Math.PI*ro);ctx.filter='blur(14px)';ctx.drawImage(cc,0,0);ctx.filter='none'}
  ctx.globalAlpha=1-ro*.5;ctx.shadowColor='rgba(0,0,0,.65)';ctx.shadowBlur=10;ctx.drawImage(cc,0,0);ctx.restore();return true}

// ── 5. Dolly zoom. vertigo(k, a, z, {amt=1.33, force=false, ramp, blur=2.5, dim=.22}) → false when it refuses (draws the plain shot)
// The speaker holds still at the same size while the room behind (the clean plate, cleanRoom(k)) stretches to amt about the head over
// ramp beats (default 40% of a…z, at most 2), holds, then springs back from z. Refuses on a plain room or SHOTINFO coverage < 0.8 unless
// force:true, because the stretched room shows the plate's filled-in hole round the person.
function vertigo(k,a,z,{amt=1.33,force=false,ramp,blur=2.5,dim=.22}={}){const I=shotInfo(k);
  if(!cleanImg(k)||!I||(!force&&(I.bg.plain||I.bg.coverage<.8))){plate(k);return false}
  const rp=ramp??Math.min(2,(z-a)*.4),v=b<z?E.inOutCubic(PB(a,a+rp)):1-spring(z,{z:.62,w:10}),s=Math.max(1,1+(amt-1)*v);
  if(b<a||s<1.001){plate(k);return true}
  const h=SC.head(k,{r:6,at:cS(a)});ctx.save();if(blur)ctx.filter=`blur(${blur*(s-1)/(amt-1||1)}px)`;about(h.cx,h.cy,s,()=>cleanRoom(k));ctx.restore();
  const d=dim*(s-1)/(amt-1||1);if(d>0){const g=ctx.createRadialGradient(h.cx,h.cy+h.hh,h.hh*.8,h.cx,h.cy+h.hh,H*.75);g.addColorStop(0,'rgba(0,0,0,0)');   // the room darkens as it falls away
    g.addColorStop(1,`rgba(0,0,0,${d})`);ctx.save();ctx.fillStyle=g;ctx.fillRect(0,0,W,H);ctx.restore()}
  subject(k);return true}

// Every effect takes (k, a, z, opts). checklist, headlineWall and chartGrow can also end at a z given inside opts.
for(const n of['checklist','headlineWall','chartGrow']){const f=globalThis[n];globalThis[n]=(k,a,z,o)=>typeof z==='number'?f(k,a,{...(o||{}),z}):f(k,a,z)}
