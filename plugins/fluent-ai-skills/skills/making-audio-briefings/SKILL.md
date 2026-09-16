---
name: making-audio-briefings
description: Use when someone wants to listen instead of read — an audio version of a report, contract review, board pack, proposal, meeting recap, research summary, PDF or long agent output — or says "read this to me", "make this listenable", "that's a lot", or asks for a spoken overview.
license: MIT
metadata:
  author: fluent
  version: "0.4"
---

# Making Audio Briefings

A briefing someone can take in on a walk or a drive: what the material is, what matters in it, and what they have to decide. The speech is made by the computer's own speech engine, so the text goes to no audio service and needs no API key or install.

It runs where the agent can run commands on a **Mac or Windows computer**: Claude Code, Codex, or a desktop agent working on local files. A browser chat or cloud sandbox has no speech engine. There, say so in one line and offer a written summary.

## 1. Read the whole source

Read all of it, including appendices, schedules and data notes, before writing a word. When the source is your own work from this session, use the finished version.

**Done when** every section of the source has been read.

## 2. Write the spoken text

Write the way a trusted colleague briefs someone the morning after, in the person's own voice notes or style guide when they have one.

**For a document**, in this order:

1. what it is, who it is from, and why it matters to the listener
2. the headline, in one sentence
3. the substance, in the order the reader would meet it
4. what is weak, missing, risky or unconfirmed
5. what the listener has to decide, and by when

**For work you just did**: the situation, the path you took, why that path over the alternatives, what came out, and where you are unsure. Name the substance of each change; a count ("added three items") tells the listener nothing.

Writing for the ear:

- short sentences; a clause the listener cannot re-read has to land the first time
- each point with its meaning: "the liability cap is one month's fees, well below the usual twelve"
- money, dates and units spelled out: "twelve thousand dollars", "the thirtieth of September"
- abbreviations expanded: "Q and A", "for example"
- plain paragraphs only; headings, bullets and tables become sentences
- open questions and decisions last, framed as "what I need from you"

Length follows the material: about a minute for a letter or a quiet day's work, three to seven minutes for a long report. Speech runs at about 180 words a minute.

Personal data, credentials and anything the person has marked confidential stay out of the spoken text, as they would stay out of a summary sent by email.

**Done when** every decision and risk in the source appears in the text, and the text contains no markdown.

## 3. Make the audio

Write the text to a file with a single-quoted heredoc, so quotes and apostrophes survive, then run the script that ships in this skill's folder:

```bash
cat > briefing.txt << 'EOF_TEXT'
[the spoken text]
EOF_TEXT
python3 "<this skill's folder>/scripts/say_it.py" --text-file briefing.txt --name "YYYY-MM-DD - subject - briefing" --out-dir "<folder>"
```

On Windows use `python` in place of `python3`.

- **Folder:** beside the document or work it briefs. When there is no obvious home, an `audio/` folder in the working directory.
- **Result:** `.m4a` on a Mac (small, plays on a phone), `.wav` on Windows. It opens in the default player; `--no-open` saves without playing.
- **Voice:** the computer's system voice, which gives the best quality available. The person changes it in System Settings, Accessibility, Spoken Content on a Mac, or Settings, Time and Language, Speech on Windows. `--voice NAME` picks another installed voice for one run. On a Mac, Siri voices work only as the system voice.

Delete `briefing.txt` once the audio exists.

**Done when** the script prints the saved file with its length, and that length is within a minute of your estimate.

## 4. Hand over

Say where the file is and how long it runs. If that folder syncs to the person's phone (iCloud Drive, OneDrive, Google Drive), it is on their phone too.

## When to offer it

Offer in one line, "Want this as audio?", after delivering a long report, review, recap or research summary, when the session runs on the person's own computer.

---

Stuck, or want to send feedback on this skill? Read the `about-fluent` skill.
