---
name: making-ai-video-ads
description: Use when someone wants a video ad, promo or explainer made with AI video generation (Higgsfield, Seedance, Kling, Veo), especially one with a talking presenter or avatar; when they want to get the most out of a Higgsfield trial or credits; or when generated takes need finishing into captioned, branded ads for every social placement.
license: MIT
metadata:
  author: fluent
  version: "0.1"
---

# Making AI Video Ads

## What this is for

A 30-second ad with a consistent presenter who says real lines, finished in every size a feed needs, in a day and mostly for free.

**The take is footage, not the ad.** The video model makes the picture and the voice. The words, the presenter's look, the review, the edit and the music are yours, and they decide whether it reads as an ad or as an AI demo. Budget the model's time for one or two takes and spend your own on everything around them.

Works from any agent with a terminal. Higgsfield is the worked route; the method holds for any model that takes reference images and dialogue.

## The shape

1. Words
2. Presenter
3. Film prompt
4. Generate
5. Review the take
6. Edit
7. Music
8. Hand over

Keep a **generation log** from step 4 on: one row per attempt with time, surface, model and settings, job ID, result and credits charged. Refusals go in it too. It is how you learn which route is free, and the evidence when a charge appears.

## 1. Words

Every line comes from the advertiser's own live material: their website today, not last quarter's deck. Positioning drifts, and an ad that repeats a retired line is worse than no ad. No invented claims, figures or client names.

- **Five or six lines, about 65 words**, spoken unhurried in about 26 seconds. The payoff line goes last.
- **Leave the last 3 to 4 seconds silent.** The end card goes there, and generated video tends to add speech in any spare time.
- **The end card carries the headline and the call to action**, not the payoff line again.

Done when you have a table of time, line and picture, and every line points to where it came from.

## 2. Presenter

One consistent face across every shot is what makes an avatar ad work.

1. **Make a character sheet in one image call:** front, three-quarter, profile and two or three close-up expressions of the same person, plain background, no text. Prompt template: `references/film-prompt.md`.
2. **Get the person's pick on the look now** (hair, clothes, style). Changing it after a video take costs another take.
3. **Crop references locally.** Sheets overlap, and a leg behind a face crop turns into an extra limb on screen. Crop one tight face and one full-body strip:
   `ffmpeg -i sheet.png -vf "crop=W:H:X:Y" ref-face.png`
4. **Upload once and note the IDs** (Higgsfield `media_upload`). The IDs work from any surface on the same account, so one upload serves every take.

Done when the face and full-body references are uploaded and their IDs are written in the log.

## 3. Film prompt

Generate the whole ad in one pass when the model allows it (Seedance 2.5 omni-reference takes up to 30 seconds). One pass holds the face steadier across cuts than stitched clips, and the model times the dialogue to the picture.

The template, the stage format and the bans list are in `references/film-prompt.md`. The parts that decide whether it works: dialogue in `{ }`, sound in `< >`, each stage ending on an end state, and a bans list naming the failures you have seen (subtitles, logos, readable screens, a second speaker).

Write the vertical as its own take with "Vertical 9:16 framing. Keep [presenter] in the centre third." Cropping a wide take to vertical loses the presenter at the edges.

## 4. Generate

**Price every job before you run it.** Quote first (Higgsfield `get_cost`, or `higgsfield generate cost`), then run. A 30-second clip can cost hundreds of credits outside a trial.

Which surface generates for free, what each one refuses, the trial's resolution and queue limits and the cancel step are in `references/higgsfield-routes.md`. Read it before the first generation; it is dated, so check the terms still hold.

The pattern that works when the free route is a chat surface: plan, write and upload in your agent, then paste one prompt that names the media IDs into a chat with the Higgsfield connector. Only the generation happens in the chat.

Done when each take is downloaded beside the project, its job ID is in the log, and the balance shows what you expected.

## 5. Review the take

Look and listen before you edit.

- **Contact sheet:** `ffmpeg -i take.mp4 -vf "fps=1/2.5,scale=180:-1,tile=6x2" -frames:v 1 sheet.png`
- **Transcript:** `scripts/caption_timings.py` transcribes the take, times every scripted line and reports any speech after the last line.

Check every take for each of these:

| Check | If it fails |
|---|---|
| Every line word for word | Re-roll |
| Same face, hair and clothes in every shot | Re-roll |
| Only the presenter speaks | Re-roll |
| Speech or sounds after the last line | Cut before it in the edit |
| Garbled text on a screen or page | Defocus that shot in the edit (`soften`) |
| Soft picture (trial resolution) | Upscale and sharpen in the edit |
| Lighting off the brief | Note it; re-roll only if it breaks the brand |

Re-roll for the presenter and the words. Fix everything else in the edit, which is free and takes minutes.

## 6. Edit

`scripts/build_ad.py` turns takes into finished ads: Lanczos upscale with a light sharpen, captions on a soft fade, a defocus on flagged shots, a cut before tail speech, a fade through dark into an end card, loudness at -14 LUFS, and every format in one run. Needs Python 3, Pillow and ffmpeg.

1. Copy `assets/ad.example.json` beside the takes and fill in the lines, takes, font, colours and end card. The fields are documented in `references/edit-config.md`.
2. Run `python3 scripts/caption_timings.py ad.json TAKE` for each take. It writes the caption times and suggests the cut.
3. Add `soften` spans for any garbled shots, and a `crop` for any format cut from another take.
4. Run `python3 scripts/build_ad.py ad.json`.
5. Make a contact sheet of every output and check three things: captions inside the frame, the crop keeps the head, the end card is clean.

| Placement | Size |
|---|---|
| Reels, stories, TikTok, WhatsApp status | 9:16, 1080x1920 |
| Instagram and Facebook feed | 4:5, 1080x1350 |
| X, LinkedIn, YouTube | 16:9, 1920x1080 |

Name each file for where it goes, so nobody has to look it up.

## 7. Music

Use a licensed track from a free library, chosen to fit the film, and record its licence beside the edit. How to choose, the libraries whose terms allow ads, and the licence note template are in `references/music.md`.

The build always writes both versions: `no-music/` and `with-music/`. Keep both. The person may prefer one, and the no-music version is what you re-score from if a platform flags the track.

## 8. Hand over

- Both versions in every format, with the music source and licence note.
- What is not fixed, such as the trial's resolution ceiling, said in one line.
- Label it as AI-generated when posting. Meta, TikTok and YouTube all have a label for it.
- Publishing is the person's call. Hand over the files and stop.

## Common mistakes

| What happens | What it actually is |
|---|---|
| Lines written from memory of the brand | Old positioning. Read the live site first |
| Avatar generated straight into video | No locked face, so it drifts between shots. Sheet first |
| Whole character sheet used as the reference | Overlapping figures become extra limbs. Crop it |
| Video job run without a quote | A surprise bill. Quote, then run |
| Second job submitted while the first is queued on a trial | It silently does not start. One at a time |
| Re-rolling for a garbled screen or an extra "Mm" | Paying an hour for an edit fix |
| Vertical made by cropping the wide take | The presenter falls off the edges. Generate it |
| One version handed over | No way to compare, nothing to fall back on |

---

Stuck, or want to send feedback on this skill? Read the `about-fluent` skill if Fluent AI Skills is installed, or visit fluent.ke.
