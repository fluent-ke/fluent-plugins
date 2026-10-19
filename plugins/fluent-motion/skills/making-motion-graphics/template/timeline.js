// Shared by comp.html and soundtrack.mjs. The music runs at a steady BPM in "music beats";
// the animation is authored in "comp beats". Each segment says how many music beats one comp beat lasts,
// so reading scenes can hold longer while kinetic scenes stay on the grid.
// [comp start, comp end, music beats per comp beat]. Keep every segment boundary landing on a whole music beat.
globalThis.BPM=120;                 // the score's tempo; comp.html and soundtrack.mjs both read it
// Film length (s) = MUSIC_BEATS × 60 / BPM (the template's default is 24 music beats = 12 s); score.wav adds a 1.2 s tail.
globalThis.SEG=[[0,4,1],[4,8,2],[8,12,1.5],[12,16,1.5]];
globalThis.toMusic=c=>{let m=0;for(const[a,z,f]of SEG){if(c<=a)break;m+=(Math.min(c,z)-a)*f}return m};
globalThis.toComp=m=>{let acc=0;for(const[a,z,f]of SEG){const len=(z-a)*f;if(m<=acc+len)return a+(m-acc)/f;acc+=len}return SEG.at(-1)[1]};
globalThis.MUSIC_BEATS=toMusic(SEG.at(-1)[1]);
// The film card: what this film is, so the brand's next film can be different (one row per film in ../film-log.tsv, updated on every
// run). It must differ from each of the brand's last two films on at least 4 of the 6 fields shape…ending, and share at most half its
// transitions (plain cuts aside) with the last one. shape continuous and talking-head relax qc.sh's rhythm gate. soundtrack.mjs logs it to ../film-log.tsv
// and warns when it repeats the brand's last two films. Vocabulary (free text is fine; keep it short and consistent):
//   shape    promo | product | explainer | montage | sting | data | loop | brand | talking-head | continuous | essay | before-after | cold-open | split
//   opening  hook-word | mid-action | question | number | object | silence | cold-open
//   signature the one move that recurs: slam-echo, flood, morph, whip, iris, ramp, punch, type-as-scene …
//   camera   locked | push | orbit | dolly-through | scale-dive | handheld
//   text     the text treatment: centred-slam | left-stack | giant-crop | caption | serif-editorial | mono
//   ending   lockup-cta | loop | hold | cut-to-black | callback
//   transitions every transition kind used, e.g. ['cut','flood','whip']
globalThis.FILM={shape:'promo',opening:'hook-word',signature:'slam-echo',camera:'locked',text:'centred-slam',ending:'lockup-cta',transitions:['cut','swipe']};
