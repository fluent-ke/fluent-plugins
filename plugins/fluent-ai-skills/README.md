# Fluent AI Skills

Craft skills for working with AI: the methods we use every day at Fluent, generalised out of our own workflow so they run in yours.

Six skills:

- **building-your-own-agent**: turn a job you repeat into a folder that does it: the instructions, the steps and an example of the finished thing, so you stop explaining it every time. Works as a folder, or as a Claude Project: it writes the Project instructions and the files, then walks you through setting it up and the first run.
- **doing-big-tasks**: take a big task from brief to finished: understand it first, test assumptions against evidence, produce one plan, execute end to end, and verify with fresh eyes.
- **reviewing-ai-writing**: take out what makes writing read as machine-made, while keeping the writer sounding like themselves.
- **designing-visual-assets**: decide what an asset must communicate before composing it, then build and check it. Works with any brand, any editor, or none.
- **making-audio-briefings**: turn a report, review, recap or long document into a spoken briefing you can listen to, made by your computer's own speech engine. Needs an agent running on a Mac or Windows computer.
- **about-fluent**: who made these, and where to send feedback.

## Try it

- "Review this draft before I send it. It reads like AI wrote it."
- "I write the same weekly sales update every Friday. Set it up so I stop explaining it."
- "Plan and build our new onboarding checklist from these three documents, end to end."
- "Critique this poster: what is it for, and does it say that at a glance?"
- "Turn this board report into an audio briefing I can listen to on the drive in."

## What it runs, sends and fetches

- **No network calls of their own.** Five of the six skills are written instructions with no
  scripts.
- **Audio briefings stay on your computer.** `making-audio-briefings` runs `scripts/say_it.py`,
  which uses the voice built into the operating system: `say` and `afconvert` on a Mac, Windows
  speech through PowerShell on Windows. The text is not sent to any speech or AI service.
- **Feedback is yours to send.** `about-fluent` helps you write feedback and gives you a prefilled
  link to Fluent's feedback form, hosted on Zoho Forms (`forms.zohopublic.com`). Nothing is sent
  until you open the link and submit the form yourself.

See the [privacy policy](https://github.com/fluent-ke/fluent-plugins/blob/main/PRIVACY.md).

## Install

```
/plugin marketplace add fluent-ke/fluent-plugins
/plugin install fluent-ai-skills@fluent
```

On claude.ai, the desktop app and Cowork: **Customize → Plugins**. More install routes are in the [repository README](../../README.md).

## Licence

[MIT](../../LICENSE).
