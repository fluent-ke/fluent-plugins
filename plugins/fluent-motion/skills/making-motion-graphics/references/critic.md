# Blind critic

The agent that built a film reads its own stills with its intentions in mind and sees what it meant to draw. A **blind critic** is a fresh agent that sees only what a viewer would, plus the brief: it catches the cramped card, the dead beat and the default look that the builder explains away. Run it once after the stills pass, before the full render.

## Dispatch

Start a subagent (the Agent or Task tool; in an app without one, a fresh chat) and give it these files and nothing else: not the conversation, not comp.html, not your notes on what each scene is meant to do.

- the brief: goal, audience, format, length, and the one action the film asks for
- the look: the reference video's sheet from `study_reference.sh`, or the four look lines
- out/stills-sheet.png (one still per scene and each text's settled state)
- out/beats-sheet.png (one frame per music beat; tell the critic that `m` labels are evenly spaced music beats and `b` labels are comp beats, whose spacing widens wherever a scene is stretched to hold, by design)
- the fact list, so it can check the words on screen
- the stills sheets of the brand's last two films (their out/stills-sheet.png, from sibling folders), labelled as earlier films, so it can judge sameness (when an earlier film has no sheet, its row from ../film-log.tsv instead; skip for a brand's first film)
- the brand's ../taste.md, so it knows what the client liked and disliked
- for a film with a voice, the verbatim transcript, so it can check every caption against what was said

Paste this as its prompt:

```
You are a senior motion designer reviewing a draft social film from its contact sheets. You did not make it.
Judge only what is on the sheets against the brief and the look.

Score each scene 1-10 (3 = template, 5 = competent student work, 8 = agency work, 10 = award-winning) on:
- hierarchy: one idea, and the eye knows where to go first
- legibility: every text readable at phone size, inside the safe area (on 1080x1920: top 250 px, bottom 350 px and
  sides 60–100 px clear), held long enough to read
- look: matches the reference or the four look lines; flag the default look (centred text on a gradient, everything
  fading in, a logo at the end) wherever it appears
- motion: kinetic scenes move on their hits; holds are still but alive
- rhythm: scene lengths vary, there is a rest and a burst; not a metronome of equal cards
- brand: marks sharp and in proportion, colours from the palette, one accent
- truth: every word on screen matches the fact list
Then score the whole film 1-10 on wow (would someone send it to a friend?) and on sameness against the earlier films'
sheets (10 = clearly a different film; 3 = the same film with new words). Skip sameness when there are no earlier films.

List the five fixes that would most improve the film, most important first, each tied to a scene and a beat (m or b
number from the tile labels) and specific enough to act on ("S3: the label under the number sits on the bright part
of the glow; move it 80 px down or add a halo"). At least one fix must raise the wow. Mark any scene that looks like
a template CRITICAL. Say which scene is weakest and why.
```

## Acting on it

Apply every fix you agree with; for any you reject, say why in one line when delivering. Re-render the stills and both sheets. The film passes when no score is below 5 and sameness is 6 or more (or, for a brand's first film, when no score is below 5). When it does not, send the new sheets to a **second, fresh** critic together with the first critic's fix list, and add to its prompt: "First mark each earlier fix FIXED, PARTLY or STILL PRESENT, then score again." The critic cannot hear the score or feel timing: `--draft`, `audio_check.py` and `rhythm.py` still carry those.
