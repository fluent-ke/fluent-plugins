# Where an agent lives, tool by tool

Verified August 2026. **Check rather than trust** — none of this is standardised, every row is one vendor's convention, and they move. Rows marked *tested* were run directly; the rest come from vendor documentation.

## The short version

| Tool | Reads on its own | The person does |
|---|---|---|
| **Claude Code** | `CLAUDE.md` in the folder you start in, and every folder above it. **Not `AGENTS.md`** — *tested* | Opens it in the folder |
| **Cowork** | The `CLAUDE.md` in the folder you point it at. Separately, it has its own folder-instructions field in the interface — the two are different things, and the file is the one that travels | Points Cowork at the folder |
| **ChatGPT desktop** | `AGENTS.md` in an attached folder, loaded at the start — *tested on the ChatGPT tab, August 2026.* OpenAI's docs attribute this to Codex mode and the project's primary folder, so confirm it on the version in front of you | Attaches the folder; a project is built around it |
| **Codex** | `AGENTS.override.md`, then `AGENTS.md`, merged from the project root down | Attaches the folder as the project's primary folder |
| **Cursor** | `AGENTS.md` | Opens the folder |
| **Copilot** | `AGENTS.md` on its main surfaces — the coding agent and VS Code | Opens the folder |
| **Gemini CLI** | `GEMINI.md` is the documented default. Whether `AGENTS.md` is read without configuring `context.fileName` is genuinely unclear — **test it before relying on it** | Opens the folder |
| **A browser** | Nothing from a folder — there is no folder | Pastes the instructions into a project, uploads the files |

## Which home to recommend

Where the person can choose, a **folder beats a project**, every time:

| | Folder | Project, in a browser |
|---|---|---|
| The output | The agent writes the file itself | It replies, and they save it by hand |
| History | Keeps its own, and can read last month's | Whatever they remember to keep |
| Example and template | Sit in the folder, always there | Uploaded, and re-uploaded when they change |
| Starting it | Open the folder, say "run it" | Open the project, paste the material |

So the order of preference is: a desktop app with the folder attached, then Claude Code, then a browser project. **Recommend it, never require it.** Build the thing that works where they are today, then say in one sentence what moving would give them. Someone who has never automated anything should not have to install software before they have seen it work once.

## Attaching a folder

- **ChatGPT desktop** — add the folder to the app; it creates a project around that folder and reads `AGENTS.md` from it at the start of a session. Labels move between versions, so look for the folder or project control rather than reciting a menu path
- **Cowork** — point it at the folder; it reads the `CLAUDE.md` inside
- **Claude Code** — open it in the folder

If they attach a folder that holds several agents, they get none of them. One job, one folder, attach that one.

## Why two instruction files

No single filename is read by everything. `AGENTS.md` is the open convention across most tools; `CLAUDE.md` is what Claude Code and Cowork read. Claude Code does not read `AGENTS.md` — tested, twice, in a clean folder.

So the job is written once in `AGENTS.md`, and `CLAUDE.md` is a two-line bridge:

```
@AGENTS.md

Read AGENTS.md in this folder and follow it before anything else.
```

Both lines earn their place. The import is what actually pulls the file in where imports are supported. The sentence is the fallback for everywhere else — but it only works where the agent can read files, so it does nothing in a browser.

**Write those lines into `CLAUDE.md` as plain text.** Tested: the same import inside a fenced code block does not load — the file is read as an example rather than an instruction, and the agent starts with nothing.

## Instructions load; the rest is fetched

The instruction file is in context from the start of the session. Everything it points at — `workflows/`, `examples/`, `templates/` — is opened only when the job runs.

That is the property the whole design rests on. The folder can hold as much detail as the job needs, as long as the detail sits in files the instruction file names rather than in the instruction file itself. Keep it short and let it point.

## One folder per agent, and open that folder

The tool reads the folder you point it at. Someone with `agents/weekly-report/` and `agents/inbox-triage/` who opens `agents/` reliably gets neither — tested.

- One job, one folder, named after the job
- Suggest somewhere ordinary — the home folder or Documents — and let them choose. It is their machine
- Inside Drive, Dropbox or OneDrive is fine, and is how most people will back it up. If the folder will hold a client's real figures, say that out loud before putting it in a synced drive
- Windows is no different; nothing in the folder is OS-specific
- If a `CLAUDE.md` already exists where they want this, add to it rather than overwriting, and say that you did

## In a browser

There is no folder to attach on claude.ai or in ChatGPT on the web. Both offer a project, which holds instructions plus uploaded files.

- Flatten the instructions into one block for the Instructions field — procedure and rules inline, since there is no file tree to point at
- Upload the example and the template, and **name them explicitly in the instructions** so the model reaches for the right one rather than whatever the project surfaces
- Keep the block tight. On claude.ai, instructions and uploads draw on the same project capacity, shown as a percentage on the project page
- Rewrite the trigger, the output destination and the run log for a place with no filesystem — the main skill has the three replacements

**Where the instructions go.** Menu names drift, so check what is on their screen rather than reciting this:

- **claude.ai** — Projects in the sidebar, create one, name it after the job, then the project's Instructions field. Files are added to the same project
- **ChatGPT** — Projects, new project, Add instructions, then upload the files to the project

Walk them through it in their own window rather than handing over a list. This is the step where a non-technical person stops, and it is the only unfamiliar thing in the whole build.

## Skills are a different thing

A skill and an agent folder are not the same, and confusing them costs portability.

On claude.ai, Cowork and ChatGPT, a skill is installed against the **account**, not found inside a folder. Claude Code is the exception — it does read a project's own `.claude/skills/`, tested. So a skills folder inside an agent works on exactly one surface.

Build the agent out of instructions and workflow files. Do not make it depend on a skill, because the skill will not travel with the folder.

## Running it on a schedule

Each surface has its own mechanism, and all of them need whatever the job reads to be connected first:

- **Cowork scheduled tasks** — the right home for most of the people this skill is for
- **Claude Code scheduled tasks**
- A project page on claude.ai shows a **Scheduled** section for recurring tasks — observed August 2026
- ChatGPT has tasks; Codex has scheduled runs

**One trap.** Claude Code's cloud *routines* run in a fresh remote session from a cloned repository, not from the folder on the person's machine. A folder agent that lives in Documents is not there when the routine runs. Use a scheduler that runs where the folder is, or put the folder in a repository the routine clones.

Build the agent and confirm it works by hand first. Scheduling something that has never produced a correct output on demand just produces wrong output unattended.
