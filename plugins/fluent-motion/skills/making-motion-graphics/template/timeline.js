// Shared by comp.html and soundtrack.mjs. The music runs at a steady BPM in "music beats";
// the animation is authored in "comp beats". Each segment says how many music beats one comp beat lasts,
// so reading scenes can hold longer while kinetic scenes stay on the grid.
// [comp start, comp end, music beats per comp beat]. Keep every segment boundary landing on a whole music beat.
globalThis.BPM=120;                 // the score's tempo; comp.html and soundtrack.mjs both read it
globalThis.SEG=[[0,4,1],[4,8,2],[8,12,1.5],[12,16,1.5]];
globalThis.toMusic=c=>{let m=0;for(const[a,z,f]of SEG){if(c<=a)break;m+=(Math.min(c,z)-a)*f}return m};
globalThis.toComp=m=>{let acc=0;for(const[a,z,f]of SEG){const len=(z-a)*f;if(m<=acc+len)return a+(m-acc)/f;acc+=len}return SEG.at(-1)[1]};
globalThis.MUSIC_BEATS=toMusic(SEG.at(-1)[1]);
