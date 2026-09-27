# Install Fluent Motion

**For people:** open Claude Code or Codex on the computer you make videos on, and paste:

> Install the Fluent Motion plugin by following https://github.com/fluent-ke/fluent-plugins/blob/main/plugins/fluent-motion/INSTALL.md

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
claude plugin install fluent-motion@fluent
claude plugin update fluent-motion@fluent
```

Every command is safe to re-run: on a machine that already has the plugin, this sequence updates it. One install covers the terminal, the desktop app and the IDE extensions.

Done when `claude plugin list` shows `fluent-motion@fluent` with `Status: ✔ enabled`.

Without a terminal, in the desktop app: **+** next to the prompt box, **Plugins**, **Add marketplace**, enter `fluent-ke/fluent-plugins`, then install **Fluent Motion**.

## Codex

```bash
codex plugin marketplace add https://github.com/fluent-ke/fluent-plugins
codex plugin marketplace upgrade fluent
codex plugin add fluent-motion@fluent
```

Every command is safe to re-run: on a machine that already has the plugin, this sequence updates it. One install covers the CLI, the desktop app and the IDE extension.

Done when `codex plugin list` shows `fluent-motion@fluent  installed, enabled`.

## Claude chat and Cowork

Install from **Customize → Plugins**, adding the marketplace from the repository `fluent-ke/fluent-plugins`. Tell the user what to expect: code there runs in a sandbox, so the skill can storyboard and write the film's code, but rendering needs Chromium and ffmpeg on a real computer. For finished MP4s, they install in Claude Code or Codex.

## Other agents

Copy the skill folder into the folder the agent loads skills from (see its documentation):

```bash
git clone --depth 1 https://github.com/fluent-ke/fluent-plugins.git
cp -R fluent-plugins/plugins/fluent-motion/skills/* <agent skills folder>/
```

An agent with no skills support can read `plugins/fluent-motion/skills/making-motion-graphics/SKILL.md` from that clone and follow it directly.

## 2. First film

Skills load when a session starts, so the user opens a new session. Then they give it material and a goal, for example:

> Make a 20-second vertical hype video for our launch from the poster in this folder.

That starts the `making-motion-graphics` skill. The first render installs Playwright and Chromium into the film's folder; it needs Node 18+, ffmpeg and Python 3 with Pillow (`pip install pillow`). On macOS: `brew install node ffmpeg`. On Windows: `winget install OpenJS.NodeJS Gyan.FFmpeg`, and run the scripts from Git Bash or WSL.

## Update or remove

- **Update:** run the install commands for your agent again.
- **Remove:** `claude plugin uninstall fluent-motion@fluent` or `codex plugin remove fluent-motion@fluent`.
