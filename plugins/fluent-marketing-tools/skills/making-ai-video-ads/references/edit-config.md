# ad.json

The one file `build_ad.py` and `caption_timings.py` read. For a story ad, `assemble_story.py` writes `lines` and each take's `file`, `times` and `cut` into it (see `story-ads.md`). Paths are relative to `ad.json`. Start from `assets/ad.example.json`.

| Field | What it holds |
|---|---|
| `lines` | The scripted lines in order, exactly as spoken. Each becomes one caption |
| `font` | A `.ttf` or `.otf` for captions and the end card. Without it, Pillow's default font is used |
| `colors.ground` | End card background, caption shadow and fade. Hex |
| `colors.text` | Caption and end card text. Hex |
| `colors.line` | The call-to-action outline. Hex |
| `end_card.logo` | Logo image for a dark ground (PNG with transparency) |
| `end_card.headline` | One line, the advertiser's own words |
| `end_card.cta` | The call to action, in an outlined pill |
| `end_card.seconds` | How long the card holds. Default 3.5 |
| `takes.KEY.file` | A generated take |
| `takes.KEY.times` | `[start, end]` per line. Written by `caption_timings.py` |
| `takes.KEY.cut` | Where the film ends and the end card begins. Suggested by `caption_timings.py`; set it before any extra speech |
| `takes.KEY.soften` | `[[start, end], ...]` spans to defocus, for garbled screens or pages. Blurs the whole frame; for a region beside a face, use `blur` in `story.json` |
| `formats[].name` | Output file name, e.g. `brand-ad-ig-fb-4x5` |
| `formats[].take` | Which take it is cut from |
| `formats[].size` | `[width, height]` |
| `formats[].crop` | `[w, h, x, y]` in source pixels, for a format cut from another take (4:5 from 9:16) |
| `formats[].cap_px`, `cap_width`, `cap_bottom` | Caption overrides. Defaults suit each size, keeping vertical captions above the platform's buttons |
| `music.file` | The licensed track. Leave `music` out for a no-music build only |
| `music.level_db` | Track level before ducking. About -13 for a track mastered near -14 LUFS |
| `music.start_at` | Where in the track to start. Default 0 |
| `music.break_before_last_line` | `true` fades the music out just before the payoff line |
| `music.return_at` | Seconds into the track for the phrase that returns on the end card |
| `music.return_boost_db` | Lift for that return. Default 3 |
| `out_dir`, `work_dir` | Default `exports` and `build` |

Output: `exports/no-music/NAME.mp4` always, and `exports/with-music/NAME.mp4` when `music` is set. `--only no-music` or `--only with-music` builds one; naming formats after `ad.json` builds only those.
