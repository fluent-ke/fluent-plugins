# Music for the ad

A licensed track from a free library, chosen for this film, with its licence written down beside the edit.

## Libraries whose free terms cover ads

Read the licence page itself before you download; these are the terms as read in November 2026.

| Library | Free licence covers | Credit | Watch for |
|---|---|---|---|
| Mixkit (mixkit.co/free-stock-music) | Commercial use on web and social, including social posts, online ads and YouTube | Not required | No TV or radio broadcast, games, CDs or DVDs; no remixing into a music-only track; no registering it on a rights service. Licence text: mixkit.co/license/#musicFree |
| Pixabay Music (pixabay.com/music) | Commercial use, royalty free | Not required | Its terms flag promoting a product or service as a case that may need more; some tracks are registered with Content ID |
| YouTube Audio Library | Videos, with each track's own terms | Per track | Built for YouTube; check the track's terms for use elsewhere |
| Incompetech (Kevin MacLeod) | Commercial use under CC BY 4.0 | Required, in the caption | Credit line on every post |

Mixkit is the simplest for paid social: clear terms, no credit line, direct downloads.

## Choosing the track

1. **Name the mood in three words from the film**, such as "calm, hopeful, warm" or "fast, bright, confident".
2. **Shortlist five to ten tracks** from the library's mood and genre lists, by title and genre.
3. **Listen to the first 30 seconds of each**, since that is the part the ad uses. Prefer a track whose opening matches the opening shot and whose change (a lift, a new section) falls near the ad's turn.
4. **Reject anything that fights the voice:** busy melody in the speech range, vocals, or drums louder than the presenter.

If an audio-analysis tool is available, rank the shortlist against the mood words and check the opening's mood. Your ears still decide.

## Placing it

`build_ad.py` handles this from the `music` block in `ad.json`:

- Plays from `start_at` under the film, at `level_db` (about 8 dB under the voice), and ducks further whenever the presenter speaks.
- `break_before_last_line` fades the music out just before the payoff, so the line lands in near-silence.
- `return_at` brings back a phrase of the track (pick a strong first note) as the end card lands, then fades out at the end.

## Licence note

Save this as `SOURCE.md` next to the track:

```
Track: [title], by [artist]
File: [filename]
Source: [library page URL], audio [download URL]
Licence: [licence name], read [date] at [URL]
Terms as read: [allowed uses]; [credit needed or not]; not allowed: [list]
Why this track: [mood match, where its change falls]
How it is cut: [start, break, return]
```

If a platform claims the track, the licence note is what you dispute with, and the no-music version is what you re-score from.
