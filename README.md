# Fluent AI Skills

Craft skills for working with AI — the methods we use every day at Fluent, generalised out of our own workflow so they run in yours.

Five skills:

- **building-your-own-agent** — turn a job you repeat into a folder that does it: the instructions, the steps and an example of the finished thing, so you stop explaining it every time. Works as a folder, or as project instructions if you only use a browser.
- **doing-big-tasks** — take a big task from brief to finished: understand it first, test assumptions against evidence, produce one plan, execute end to end, and verify with fresh eyes.
- **reviewing-ai-writing** — take out what makes writing read as machine-made, while keeping the writer sounding like themselves.
- **designing-visual-assets** — decide what an asset must communicate before composing it, then build and check it. Works with any brand, any editor, or none.
- **about-fluent** — who made these, and where to send feedback.

They are built on the open [Agent Skills](https://agentskills.io) standard, so the same folders run in Claude, ChatGPT and Codex, Cursor, Gemini CLI and other compatible tools.

## Install in Claude Code

```
/plugin marketplace add fluent-ke/fluent-plugins
/plugin install fluent-ai-skills@fluent
```

On claude.ai and Cowork: **Customize → Plugins**.

## Use them anywhere else

Each skill is a plain `SKILL.md` folder under [`skills/`](skills/). Copy the one you want into your tool's skills directory, or point your agent at this repo.

## Fluent 3D

A second plugin for 3D design and printing: set up CAD and slicer apps on any computer, model parts live in FreeCAD, OpenSCAD or Blender, and turn them into slicer projects ready to print. See [`plugins/fluent-3d`](plugins/fluent-3d/).

```
/plugin install fluent-3d@fluent
```

In Codex: `codex plugin marketplace add https://github.com/fluent-ke/fluent-plugins`, then `codex plugin add fluent-3d@fluent`.

## Feedback and more

These get better from real use. If one gets something wrong, or you want more like them, the `about-fluent` skill has the feedback form. More from Fluent: [fluent.ke](https://fluent.ke).

## Licence

[MIT](LICENSE).
