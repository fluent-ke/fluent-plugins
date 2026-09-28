# Voiceover and captions

## Choosing a voice

A voice that sounds read rather than spoken is the fastest way to make an ad feel cheap. Microsoft's Kenyan neural voices (`en-KE-AsiliaNeural`, `en-KE-ChilembaNeural`, free through `uvx --from edge-tts`) are standard voices with no speaking styles, so they cannot be directed; use them only for timing drafts. Audition before committing: no vendor publishes proof of Kenyan-accent quality.

| Option | Why | Terms (check on the day) |
|---|---|---|
| ElevenLabs v3, a Kenyan voice from the Voice Library | Most expressive; audio tags (`[excited]`, `[warmly]`), ellipses for pauses, CAPS for stress; Swahili supported; `/with-timestamps` returns character timings for captions | Paid plan for commercial use (free plan is non-commercial). Hosted MCP at `https://api.elevenlabs.io/v1/mcp` (OAuth) |
| Gemini TTS (through the `media-use` skill) | A style prompt directs persona, pace and emotion; Swahili supported | API key; check the free-tier data terms |
| OpenAI `gpt-4o-mini-tts` | Cheap, directed in plain language | API key; usage policy asks you to disclose the voice is AI |
| Chatterbox Multilingual (local, MIT) | Runs on Apple Silicon, Swahili, emotion control, can clone a voice from about 5 s of audio | Outputs carry an inaudible watermark |
| A real Kenyan voice artist | The benchmark the others are measured against | Signed consent before any cloning |

Avoid for client work, because the weights or outputs are non-commercial: XTTS-v2, F5-TTS, Spark-TTS, `facebook/mms-tts-swh`.

## Directing it so it sells

- Write for the ear: short lines, second person, one idea per line, the user's own words where they exist. Run the script through the brand's copy rules before generating anything.
- Generate **phrase by phrase**, three takes each, keep the best take of every line. Join with 150–300 ms gaps of room tone, never digital silence.
- Give each line a one-line delivery note (warm, amused, certain) and turn it into the vendor's control: tags, a style prompt, instructions.
- Slightly faster than natural (`atempo=1.04`) reads as confident in a 30 s ad; slower reads as a lecture.
- Place each phrase on the beat grid: start lines on a music beat (`M(c)` in seconds) so words and hits land together.

## Captions

1. **Word timings for a known script:** the vendor's timestamps (ElevenLabs `/with-timestamps`) shifted by each clip's offset; otherwise `stable-ts` (`model.align(audio, script)`, MIT); for Swahili the Montreal Forced Aligner Swahili model. When there is no script, transcribe first with `whisper` (MIT) or `whisper.cpp` using word timestamps.
2. **Pages:** group words into pages of 2–4 words (a page closes after about 600 ms or at punctuation). One page on screen at a time.
3. **Style:** each word pops in on its own start time (`words()` in comp.html takes the page's start beat and a per-word step), the active or key word in the accent colour, heavy weight, 80–110 px on a 1080-wide frame, a soft dark shadow or a local `halo()` behind it. Keep caption pages inside x 60–960 and y 250–1490 so the platform's buttons and caption bar do not cover them.
4. **Burn them in** through the comp, not a subtitle file: styling and timing then match the rest of the film.

## Mix

`[music][vo]sidechaincompress=threshold=0.05:ratio=8:attack=20:release=300` ducks the score under the voice, then the two-pass loudnorm in `mix.sh`. Check it with `audio_check.py`: the voice sections should read louder than the score-only sections, never flat.
