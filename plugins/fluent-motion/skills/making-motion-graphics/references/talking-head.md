# Talking-head films

A person speaks to camera (an interview, a founder story, a testimonial) and the film is cut from what they say: jump cuts and punch-ins, captions, a key word tucked behind their head, cutaways and footage effects on the big lines, a quiet score underneath. **The voice is the timeline**: it plays in real time, so nothing is stretched and every cue sits on a measured word onset.

## 1. Probe the take

`ffprobe -show_entries stream=r_frame_rate:stream_side_data=rotation …`. Phones and many cameras store portrait footage as landscape with a rotation flag; ffmpeg rotates it on decode, so a "1920×1080" file can be a 1080×1920 shot. Pick the film's `FPS` so it divides the source rate (100 or 50 → 25, 120 or 60 → 30, 24 → 24): frames then decimate evenly. 100 → 30 gives a 3-3-4 cadence that judders. Use the same number in three places: `cut_interview.py --fps`, `CONFIG.FPS` in comp.html (the template says 30; a mismatch plays the picture fast or slow against the voice), and `qc.sh … <FPS>`.

## 2. Transcribe, then verify

`cut_interview.py … --whisper small` writes `words.json`. Treat it as a draft:

- **Word times drift** by up to 0.6 s, worst on the first word after a pause. Page and cue times come from `onsets.txt` (measured), never from whisper alone.
- **Names get misheard** ("Acme" as "Ack me", "her house"). Take brand names from the client, never from the transcript.
- **Verify the lines that matter** (the hook, the brand line, anything you will set big) with a second, independent read: the same clip alone with `--beam_size 5 --condition_on_previous_text False`, and a larger model (`medium`). Clip-level reads beat whole-file reads, which drag context across lines. Where reads disagree, settle that clip; do not take a majority vote.
- Caption what is said, verbatim. When a phrase reads oddly but is what they said, caption it as said and put the emphasis on another phrase.

## 3. Cut

From the project folder, first `python3 $K/scripts/cut_interview.py take.mp4 --fps 25 --whisper small`: it prints the take's words in source time (and keeps them in `src/words-source.json`). Then cut for real with `--from`:

- **The hook is the first frame.** Start on the strongest line, not on "So, I believe that…" or a breath. Whisper's source times put you within a word; to cut cleanly between two words that run together, read the level in 10 ms steps around that point and cut in the dip. Re-runs reuse the cached transcript.
- Pauses over `--gap` (0.55 s) are shortened to `--keep` (0.3 s). Edit `edl.json` and re-run to keep a pause that carries rhythm: a list ("from your bedroom, from a café, from your mother's garage") or the beat before the turn.
- Every cut is a jump cut. `cut_interview.py` prints them in edited time (`cuts.txt`): put a camera key (below) on each one, not a dissolve.

In comp.html: `CONFIG.FPS` as above, `CUTS=[]` (the template's swipes would paint bands across the interview), `SHOTS={TALK:{at:0,n:<frames>,mask:true}}`. In `timeline.js`: one uniform segment, `SEG=[[0,N,1]]`, with N music beats covering the edit plus the end card. Never stretch a segment: it would break lip-sync. Frames load only while the shot plays, so an end card that runs past the last frame must not draw `plate('TALK')`: give it its own background.

## 4. Camera

The shot is locked off; the edit moves the camera. Per line, snap to a new scale about the face, overshoot a little and push in slowly:

```js
const FACE=[495,800],CAM=[[0,1.22],[2.36,1.0],[4.78,1.36],[60,1]];        // [line start s, scale]; the face point stays put
function cam(){let i=CAM.findIndex(([a])=>a>t)-1;if(i<0)i=0;const[a,s]=CAM[i],z=CAM[i+1][0];return s*(1+.03*TP(a,z))*(1+.045*Math.exp(-(t-a)*16))}
const talk=(s=cam(),f=null)=>{if(f)ctx.filter=f;about(...FACE,s,()=>plate('TALK'));ctx.filter='none'};
const talkSub=(s=cam())=>about(...FACE,s,()=>subject('TALK'));
```

Alternate wide (1.0) and tight (1.25–1.5) between lines, with a key on every jump cut from `cuts.txt`. Keep a scale low where cards or chat sit above the head.

## 5. Text behind the head

Mattes: `swift $K/scripts/segment.swift person shots/TALK masks/TALK`, then `python3 $K/scripts/asset_tools.py heads masks/TALK head.js` (the head's top and centre per frame) and load `<script src="head.js"></script>` next to captions.js. `HEAD[shotIdx('TALK')-1]` is the frame playing now: `[top, centreX]` in source pixels. Place the word like this:

1. **Keep the camera still under the word.** The word lives in screen space; if a camera key lands while it is up, the head jumps under a still word. Put the punch-in on the word's own onset, or no key until it leaves.
2. **Average the head top** over the frames the word is up (`HEAD.slice(f0,f1)`), so the word does not bob, and convert it to the screen: `top = FACE[1]+(avg-FACE[1])*s`.
3. **Measure the letters' bottom, not the font's.** Set the font and `ctx.textBaseline='middle'` *before* `measureText`, and measure a flat-bottomed capital (`'I'` or `'H'`): `actualBoundingBoxDescent` of a whole word includes tails (Q, g, y, p, j) that hang below the line and would push the word up. With Poppins Bold the flat bottom is about `0.24 × size` below `y`.
4. **Tuck 30–80 px.** Set `y = top + tuck - bottom` so only that sliver of the letters goes behind the hair. Draw `talk()`, then the word, then `talkSub()`, and check a still: a word sunk too deep loses a whole letter ("FA_TER"), one too high just floats.

The same matte darkens the world around them on a line like "alone": `talk(s,'brightness(.2) saturate(.3)')`, a navy wash, then `talkSub(s)` at full exposure.

## 6. Captions

Write `pages.txt` by hand, 2–4 words a page, each page starting on a measured onset, the key phrase in `*stars*`:

```
0.04 | most founders
0.58 | don't *quit*
26.75 | That's why we built a *Acme.*
```

`python3 $K/scripts/captions.py pages.txt words.json captions.js --join acme=ack+me --snap onsets.txt` (`--snap` moves each later word onto its measured onset), load `<script src="captions.js"></script>` before the main script in comp.html, and call `caps()` last in each scene. `caps()` grows a brand-colour box behind the words said so far, because plain white text with a shadow disappears over a light shirt or a bright sky. Captions sit low (y ≈ 0.73 H) and inside x 60–960.

## 7. Cutaways on the big lines

- **Safe area for everything, not only captions.** Cards, chips, labels and chat bubbles stay inside x 60–960 and below y 250; the top bar and right-hand buttons of TikTok and Reels cover the rest.
- **UI cards** illustrate the problem lines (a build stuck at 99 %, a message delivered and unanswered, "build failed", a deadline "not set"): one card per line in the same slot above the head, popping in on a spring with a slight tilt. Four in a row starts to read as a template, so break the run with a cutaway.
- **Landscape photos** in a 9:16 film: full bleed only when the upscale stays under about 1.6×. Otherwise use a split screen: the photo panel on top (1080 × ~780), the speaker below (`plate('TALK',1,0,560)` drops the frame so the face sits at about y 1350), and captions on the seam.
- **Footage effects** ([footage-effects.md](footage-effects.md)) work on stills of the place: a masked frame build behind the speaker on a list, crowd masking on "somebody at the next table", a stadium reveal from an empty room to a full one, a logo match cut on the brand line, a hyperlapse merge on "faster", a warp portal into the end card on the call to action. Each must say the line, not argue with it: an empty room under "next to other founders" works against the pitch.

## 8. Score and mix

A score under a voice stays low and simple: pads and a soft pulse under the problem, the beat and a lift (minor to relative major) on the turn line, a breath before the call to action. `lofi` is built for this ([score.md](score.md)). Write cues in seconds at onsets: one-shots (`kick(t)`, `impact(t)`, `riser(t,len)`) take seconds; `groove(from,to)` takes music beats, so call `groove(a/B,z/B)`.

`./mix-voice.sh <name>`: the voice is cleaned and compressed, the score ducked under it, the whole mix normalised to -14 LUFS / -1 dBTP. It prints how far the voice sits above the music per 4 s window. Keep every window at 10 dB or more (`MUSIC=0.15 ./mix-voice.sh …` lowers the bed from its 0.22 default). Phone speakers lose speech below that.

## 9. Review

Give the blind critic ([critic.md](critic.md)) the verbatim transcript as well as the brief, so it can check every caption against what was said.
