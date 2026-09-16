# Fluent Plugins

Public plugins from [Fluent](https://fluent.ke): the methods we use every day, generalised so they run in your setup. Every skill is a plain `SKILL.md` folder on the open [Agent Skills](https://agentskills.io) standard, so the same folders run in Claude, ChatGPT and Codex, Cursor, Gemini CLI and other compatible tools.

## The plugins

| Plugin | What it gives you | Folder |
|---|---|---|
| **Fluent AI Skills** | Build your own agent for a job you repeat, finish big tasks end to end, write without AI slop, design with intent, and turn long documents into audio briefings | [`plugins/fluent-ai-skills`](plugins/fluent-ai-skills/) |
| **Daily Brief** | A researched brief on your industry, checked against primary sources and waiting before your day starts. It interviews you first | [`plugins/daily-brief`](plugins/daily-brief/) |
| **Fluent Marketing Tools** | Operating procedures for Pencil design files and for Meta ads built through the Ads MCP | [`plugins/fluent-marketing-tools`](plugins/fluent-marketing-tools/) |
| **Fluent 3D** | Set up CAD and slicer apps, model parts live in FreeCAD, and slice them ready to print | [`plugins/fluent-3d`](plugins/fluent-3d/) |

## Install

In Claude Code, add the marketplace once, then install the plugins you want:

```
/plugin marketplace add fluent-ke/fluent-plugins
/plugin install fluent-ai-skills@fluent
/plugin install daily-brief@fluent
/plugin install fluent-marketing-tools@fluent
/plugin install fluent-3d@fluent
```

In the Claude desktop app, claude.ai and Cowork: **Customize → Plugins**, add the marketplace `fluent-ke/fluent-plugins`, then install from the list.

In Codex:

```
codex plugin marketplace add https://github.com/fluent-ke/fluent-plugins
codex plugin add fluent-ai-skills@fluent
```

## Updates

Plugins update from this repository. In Claude Code, `/plugin marketplace update fluent` then `/plugin update <plugin>@fluent`; the desktop app and Cowork pick up new versions on their own.

## Use the skills anywhere else

Copy a skill folder from `plugins/<plugin>/skills/` into your tool's skills directory, or point your agent at this repo.

## Feedback and more

These get better from real use. If one gets something wrong, or you want more like them, the `about-fluent` skill in Fluent AI Skills has the feedback form. More from Fluent: [fluent.ke](https://fluent.ke).

## Licence

[MIT](LICENSE).
