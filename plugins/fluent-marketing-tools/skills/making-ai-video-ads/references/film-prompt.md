# Prompts: character sheet and film

Both templates come from an ad that worked on the first take: a 30-second, six-line avatar ad, with Seedance 2.5 omni-reference on Higgsfield, every line word for word and the same face in every shot.

## Character sheet (image model)

Use an image model that holds one identity across panels (Nano Banana Pro or GPT Image on Higgsfield). One call, landscape 16:9 or 3:2:

```
A character reference sheet for an animated presenter named [NAME]. [STYLE: e.g. premium 3D animated
feature-film look: soft subsurface skin, realistic fabric and hair, expressive eyes, natural gestures].
[WHO: age range, heritage, skin tone, build, presence].
[LOOK: hair, earrings, clothes, one accent detail such as a small coloured pin on the left lapel].
Panels, all the same person: full body front, full body three-quarter, full body profile,
head-and-shoulders smiling, listening, speaking. Plain warm-grey background, even soft light.
No text, no labels, no logos, no watermarks.
```

One accent detail (a pin, a scarf colour) gives the video model something to keep consistent and you something to check.

## Film (Seedance 2.5, mode omni_reference)

Settings: duration up to 30, resolution as the route allows, aspect ratio 16:9 or 9:16, `generate_audio` on, the face and full-body crops as image references.

```
[Generation Goal] A 30-second [STYLE] commercial for [BRAND], [what it does]. [NAME] speaks to camera
and moves through [N] settings, ending at [final picture].

[References] [NAME] corresponds to @Image 1 (face) and @Image 2 (full body). Use only [NAME]'s face, hair,
skin and clothing: [list]. Do not use the image backgrounds, and ignore any partial figures in the images.

[Style] [Look and light, e.g. low-key evening light, warm tungsten lamps, near-black shadows, city
lights through windows]. [Who else appears, e.g. every character is Black African (Kenyan)].
Calm, assured performance; nothing exaggerated.

[Voice] [NAME] speaks clear [accent] English, warm and unhurried, mid-low pitch. Only [NAME] speaks.

[Prohibitions] Pure video. No subtitles, no on-screen text, no logos or brand names anywhere, no
legible text on screens or papers, no background music. No lip movement when [NAME] is not speaking.
No other character talks. No cheering, no applause, no exaggerated smiles.

[0-6s] [Shot: setting, framing, lens, camera move]. [Action]. [NAME] says: {line one} <sound>.
End state: [where they are, what they are doing].

[6-13s] Cut to [shot]. [NAME] says while walking: {line two} End state: [...].

[13-21s] Cut to [cutaways]. [NAME]'s voice continues over these shots: {line three} End state: [...].

[21-27s] Cut back to [shot], push in to a medium close-up as [NAME] says straight to camera:
{payoff line} One small nod on the last word. End state: [NAME] holds eye contact.

[27-30s] Hold on [NAME], still and calm, room tone only. No speech.

[Maintain consistency] The same [NAME] in every shot: face, hair, clothes, [accent detail].
Each other person keeps their own face and clothes; no clones.
```

For the vertical take, add one line at the top: `Vertical 9:16 framing. Keep [NAME] in the centre third of the frame.`

## What the model does anyway

Seen on real takes; plan the edit for them instead of fighting them in the prompt:

- **Speech after the last line.** An echo of the payoff or an "Mm" in the silent hold. The edit cuts before it, and the hold gives it room to land outside the ad.
- **Readable nonsense on screens.** "No legible text" lowers it but does not remove it. The edit defocuses that shot.
- **Brighter than asked.** Low-key light drifts toward even office light. Say it twice (Style and the stage) if it matters.
- **Accent detail moves.** A pin on the left lapel may sit on the right. Only re-roll if someone would notice.
