# Install Fluent CAD

**For people:** open Claude Code or Codex on the computer you design on, and paste:

> Install the Fluent CAD plugin by following https://github.com/fluent-ke/fluent-plugins/blob/main/plugins/fluent-cad/INSTALL.md

**For agents:** the steps below install the plugin, prove it installed, and hand over to setup. Tell the user what each command does before running it. The commands download from GitHub and write to the agent's settings folder in the user's home, so a sandbox may need the user's approval for network access or for writing outside the project.

## 1. Find your path

| You are running in | Go to |
|---|---|
| Claude Code: terminal, desktop app, VS Code or JetBrains | [Claude Code](#claude-code) |
| Codex: CLI, desktop app or IDE extension | [Codex](#codex) |
| Claude chat (web or desktop) or Cowork | [Claude chat and Cowork](#claude-chat-and-cowork) |
| Another agent that loads `SKILL.md` folders | [Other agents](#other-agents) |

When the user works in both Claude Code and Codex, install in both. `claude --version` and `codex --version` show which command-line tools are present.

## Claude Code

```bash
claude plugin marketplace add fluent-ke/fluent-plugins
claude plugin marketplace update fluent
claude plugin install fluent-cad@fluent
claude plugin update fluent-cad@fluent
```

Every command is safe to re-run: on a machine that already has the plugin, this sequence updates it. One install covers the terminal, the desktop app and the IDE extensions.

Done when `claude plugin list` shows `fluent-cad@fluent` with `Status: ✔ enabled`.

Without a terminal, in the desktop app: **+** next to the prompt box, **Plugins**, **Add marketplace**, enter `fluent-ke/fluent-plugins`, then install **Fluent CAD**.

## Codex

```bash
codex plugin marketplace add https://github.com/fluent-ke/fluent-plugins
codex plugin marketplace upgrade fluent
codex plugin add fluent-cad@fluent
```

Every command is safe to re-run: on a machine that already has the plugin, this sequence updates it. One install covers the CLI, the desktop app and the IDE extension.

Done when `codex plugin list` shows `fluent-cad@fluent  installed, enabled`.

## Claude chat and Cowork

Install from **Customize → Plugins**, adding the marketplace from the repository `fluent-ke/fluent-plugins`. Tell the user what to expect: code there runs in a sandbox rather than on their computer, so the skills give advice, model scripts and step-by-step guidance, but can't install apps, check the computer or drive CAD apps. For the full setup, they install in Claude Code or Codex on the computer they design on. Claude Desktop's own connectors (Blender, Fusion, SketchUp, ArchiCAD) still work there: `setting-up-cad-apps` explains each.

## Other agents

Copy the five skill folders into the folder the agent loads skills from (see its documentation):

```bash
git clone --depth 1 https://github.com/fluent-ke/fluent-plugins.git
cp -R fluent-plugins/plugins/fluent-cad/skills/* <agent skills folder>/
```

An agent with no skills support can read `plugins/fluent-cad/skills/setting-up-cad-apps/SKILL.md` from that clone and follow it directly.

## 2. Hand over to setup

Skills load when a session starts, so the user opens a new session. Then they say:

> Set up this computer for my work. I'm a *what you do* and I use *your apps*.

That starts the `setting-up-cad-apps` skill. [GUIDE.md](GUIDE.md) covers everything after that.

## Update or remove

- **Update:** run the install commands for your agent again.
- **Remove:** `claude plugin uninstall fluent-cad@fluent` or `codex plugin remove fluent-cad@fluent`.
