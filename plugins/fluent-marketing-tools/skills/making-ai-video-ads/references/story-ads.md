# Story ads: 60 to 90 seconds, narrated, in chapters

For a longer ad that tells a story with several characters, such as a before-and-after or a workplace scene, with a narrator over the picture. Tested on a 90-second, four-chapter ad in November 2026. Every step of SKILL.md still applies; this file covers what changes.

## What changes

| Step | 30-second presenter ad | Story ad |
|---|---|---|
| Words | Five or six lines spoken on camera | One narration script of about 150 to 200 words, in paragraphs, one paragraph per chapter or two |
| People | One presenter sheet | One cast sheet with every character, cropped per person |
| Picture | One take per format | Three or four silent chapters of about 20 seconds, generated for each aspect |
| Voice | Spoken in the take | One separate narration track, recorded once |
| Edit | `build_ad.py` | `assemble_story.py`, then `build_ad.py` |

## Words

- **Write the narration as paragraphs, one per beat:** problem, the familiar thing the viewer already knows, the turn, what the advertiser does, then the payoff. The script, its sources and a table of chapter, picture and paragraph go in one file.
- **The payoff line can be a short clip reused from an earlier ad,** such as a presenter saying the catchphrase on camera. Use the raw take, not the finished export, which has captions and music burned in, and keep about a second after the last word: the build fades into the end card over the last 0.9 seconds. Each aspect needs its own raw take. With only one aspect, close the other format on the end card or generate the payoff there too; a crop loses the presenter at the edges.

## Cast

1. **One image call makes the whole cast:** every character in a row, full body, with a head-and-shoulders close-up above each, plain background, no text or labels. Five people fit at 2k. One sheet keeps them in one style and one light.
2. **Crop each person out locally** into a face and a full-body reference. Group characters who only appear together, such as colleagues in the background, into one strip.
3. **Up to four image references per job** worked reliably: for example the leader's face and body, plus the team strip and one other person. Name in the prompt who each `@Image` is.

## Chapters

- **About 20 seconds each, written in stages** (`[0-5s] ... [5-14s] ...`), each stage ending on an end state, with the same Style, Prohibitions and Consistency blocks pasted into every chapter, word for word.
- **Silent on camera.** In Prohibitions: "No speech, no dialogue, no lip movement, no narration, no music: room tone and soft office sound only." The narration goes on in the edit, so no chapter needs a silent tail.
- **A match cut across chapters** (the same person doing the same thing twice, once with a person and once with AI) holds when both chapters share the same references, room and style block.
- **AI as a laptop screen, never a figure.** Ban robots, holograms and glowing AI figures. A screen reads as real work.
- **One job at a time on a trial.** A second job is refused with `rate_limit_reached` (429) and nothing is created. Submit the next chapter only once the previous one has finished. Four chapters in two formats is eight jobs: plan for eight to ten hours of queue.
- **Ask the chat to submit and stop,** for one approval per job: "Submit one video now, then stop: do not wait for it or poll it, just give me the job ID." Wait for the result from your own terminal (see higgsfield-routes.md).

## Narration

- **Clone the narrator's voice from audio you already have,** such as the presenter's lines from an earlier ad: cut 20 to 30 seconds of clean speech, upload it, and generate the narration with a text-to-speech model that takes it as a voice reference (Higgsfield Seed Audio, `audio_references`). The voice then matches the payoff clip. Clone only a voice whose owner agreed to it.
- **One job for the whole script,** with paragraphs separated by blank lines, so every pause and the tone stay consistent. Write the delivery note in your message to the chat, outside the quoted script: a chat surface may drop delivery notes from the prompt so they are not read aloud.
- **Check it with a transcript, then by ear.** Run Whisper with word timestamps over the narration. A line the transcript mishears, especially a short first word such as "At", gets a short regeneration of that paragraph alone. When two takes are both near misses, let the person listen and choose: speech-to-text mishears unclear onsets in both directions.
- **Whisper invents words on silence.** A silent chapter that transcribes as "I'll see you in the next one" or "Thank you" has no speech in it. Check its loudness before believing it.

## Edit

`scripts/assemble_story.py story.json` joins the chapters, lays each narration piece over its chapter with the room tone at -14 dB, softens flagged screen regions with a feathered blur, appends the closing clip with its own audio, and fills `ad.json` with the lines, caption times and cut for each format. Then `python3 scripts/build_ad.py ad.json` adds captions, the end card, music and every size, as for a 30-second ad. Skip `caption_timings.py`: the caption times are already written.

Every clip is fitted to the first chapter's frame, so a closing clip at another size joins cleanly, and a clip with no sound gets silence. The script warns when narration runs past the end of its chapter (it is cut there) and when a caption line straddles the edge of a narration piece (it is left out).

```json
{
  "ad": "ad.json",
  "voices": {
    "narration": {"file": "audio/narration.wav", "lines": ["First sentence.", "Second sentence."]}
  },
  "chapters": [
    {"takes": {"wide": "ch1-16x9.mp4", "tall": "ch1-9x16.mp4"}, "trim": [0, 18.5],
     "voice": [{"from": "narration", "start": 0.0, "end": 13.3, "at": 1.2}]},
    {"takes": {"wide": "ch2-16x9.mp4", "tall": "ch2-9x16.mp4"}, "trim": [0, 20],
     "voice": [{"from": "narration", "start": 14.0, "end": 25.3, "at": 2.0}],
     "blur": {"wide": [[14.9, 20.1, 0, 0, 470, 480]]}}
  ],
  "closer": {"takes": {"wide": "payoff-16x9.mp4", "tall": "payoff-9x16.mp4"}, "line": "The payoff line."}
}
```

| Field | What it holds |
|---|---|
| `ad` | The `build_ad.py` config to fill. Its end card, formats, font and music stay yours; `lines` and each take's `file`, `times` and `cut` are written |
| `voices.NAME.file` | A narration file. Several are allowed, such as the full read and a regenerated paragraph |
| `voices.NAME.lines` | Caption lines, timed by Whisper on first run and cached beside the file as `FILE.captions.json`. Check that file by ear once; corrections there are kept |
| `voices.NAME.captions` | Or give `[[start, end, text], ...]` directly, in the voice file's own time |
| `chapters[].takes` | The chapter file for each take key. Keys match `formats[].take` in `ad.json` |
| `chapters[].trim` | `[from, to]` seconds of the chapter to keep. Trim a long hold rather than stretch the narration |
| `chapters[].voice` | Pieces of narration: which voice, `start` and `end` in that file (leave out `end` for the rest of the file), and `at`, seconds into this chapter |
| `chapters[].blur.TAKE` | `[[from, to, x, y, w, h], ...]` in chapter seconds and pixels of the first chapter's frame, given per take. Softens a screen with fake text while a face beside it stays sharp. An optional seventh value sets the strength (default 6; about 12 hides small text such as a chat bubble). For a moving camera, split the shot into short spans with their own boxes |
| `closer` | An optional last clip with its own sound: `takes`, optional `trim`, its caption `line`, and `line_at` (seconds into the clip the caption appears, default 0.15). The caption holds to the end of the clip |
| `room_db`, `work_dir` | Chapter sound under the narration (default -14 dB) and the output folder (default `build`) |

- Find blur regions from one still per shot (`ffmpeg -ss T -i chapter.mp4 -frames:v 1 still.png`) and shot cuts from `ffmpeg -i chapter.mp4 -vf "select='gt(scene,0.25)',showinfo" -f null -`.
- `--standin` previews the timing with chapter 1 standing in for chapters not yet generated, so the edit is ready before the last chapter lands.
- `soften` in `ad.json` blurs the whole frame; use `blur` here when a person shares the shot.
- **Music for 90 seconds:** choose a track that runs at least the length of the ad from `start_at`, and set `return_at` to a phrase in that track that suits the end card; the example value fits only the 30-second example. Choose by listening across the whole length, not the first 30 seconds.

## Review the cut

- A contact sheet of the whole ad (`fps=1/4,tile=7x3`) shows a missing caption, a soft shot or a face that drifted between chapters at a glance.
- The finished 1080p file can be too large to send to a phone. Send a 720p preview for review (`-vf scale=1280:-2 -crf 24`) and keep the 1080p masters for posting.
