---
name: ai-workspace-setup
description: Use when someone wants their business files set up so AI can actually work in them — a messy folder, a Google Drive full of documents, context scattered across chats — or says "organise my files", "set up PARA", "set up a second brain", "make an Obsidian vault", "I want Claude (or ChatGPT) to know my business", "my AI keeps forgetting what we did", or "I want my work tracked". Also when they need to sync a work folder with Google Drive, point Claude or ChatGPT at one folder, or keep separate workspaces (two businesses, business and personal) apart.
license: MIT
metadata:
  author: fluent
  version: "0.2"
---

# AI Workspace Setup

## What this is for

An AI is only as useful as the context it can reach. Most business owners have that context, but it is spread across a downloads folder, three Drive accounts, WhatsApp exports and old chats, so every session starts from zero and they explain their business again.

This skill turns that mess into a **workspace**: one folder, organised with PARA, opened in Obsidian, synced by Google Drive, with instructions that make the AI work inside it and a tracking skill that makes it remember. It is the setup we run every day at Fluent, generalised for anyone.

The person does not need to code. Do the work for them; explain each piece in one or two plain sentences as you reach it, never as a lecture up front.

## The pieces, in plain words

- **PARA** is four folders that everything fits into, sorted by how active it is:
  - `1. Projects`: work with a finish line ("Launch the wholesale price list", "Hire a sales rep").
  - `2. Areas`: responsibilities that never end ("Sales", "Finance", "Marketing", "AI Setup").
  - `3. Resources`: reference you reuse (templates, price lists, brand files, contacts, research).
  - `4. Archive`: anything finished or no longer active. Nothing is deleted; it moves here.
  The test for any file: *is it something I'm finishing, something I keep running, something I look things up in, or something I'm done with?*
- **A vault** is just a folder that Obsidian opens. Nothing is locked in: the files stay ordinary Markdown documents the person owns, readable by any AI or editor. Obsidian adds a small hidden `.obsidian` folder for its own settings.
- **The instruction file** sits in the folder and tells the AI who the person is, how the workspace is laid out and how to work. There is one at the root and one in every project and area, so the AI picks up local context wherever it works. Claude reads `CLAUDE.md`; ChatGPT and most other tools read `AGENTS.md`.
- **The tracking skill** gives every real piece of work one `task.md` file holding its current state and a log of each session. It is how the AI remembers between chats. It is installed in the AI itself, not the folder, so it works in every chat and every workspace.

## The shape

1. Understand the person, and open the setup as their first task
2. Propose the PARA map, then reorganise
3. Write the instruction files
4. Install the tracking-work skill in their AI
5. Sync the folder with Google Drive
6. Install Obsidian and open the vault
7. Point their AI at the folder
8. Repeat for each separate workspace
9. Close the setup task, and prove it remembers

Steps 4 to 7 need the person's own computer and accounts. Guide them click by click and confirm each one worked before moving on. Everything else you do yourself.

## 1. Understand the person, and open the setup as their first task

Ask, conversationally and few at a time: what the business does, who else works in it, what their week looks like, which AI they use (Claude, Claude Code, ChatGPT, a browser only), and where their files live today.

Then look at the folder yourself. Get the shape before the detail: how many files, what kinds, the obvious clusters (clients, money, marketing, admin), duplicates, and anything sensitive (ID scans, passwords, bank statements). **If there is a text file of passwords or keys, say so and recommend a password manager; never copy it into the new structure as-is.**

**The setup itself is the first tracked task.** Create the area `2. Areas/AI Setup/` straight away and open `2. Areas/AI Setup/tasks/ai-workspace-setup/AI Workspace Setup - task.md` using the template in `references/tracking-work-skill.md`, which also shows this exact task filled in. Record each step in it as you go. The person sees tracking work on something real from the first minute, and if the chat dies halfway, the next one picks up from the file. The AI Setup area stays as the home for everything about how they work with AI from then on: new skills, instruction changes, tools they try.

If they work in more than one world that should not mix (two businesses, a business and a household, a client they work inside), note it now. That is step 8.

## 2. Propose the PARA map, then reorganise

Show the proposed structure before moving anything: the projects and areas you found, named in their words, and where each existing folder goes. A short table of *current folder → new home* is enough. Get a yes, then move.

The layout every workspace uses:

```
<Workspace Name>/
├── CLAUDE.md                ← who they are, how the workspace works
├── 1. Projects/<Project Name>/
│   ├── <Project Name>.md    ← home note: what it is, status, key links
│   ├── CLAUDE.md            ← what an AI needs to know to work here
│   ├── tasks/<task-name>/<Task Name> - task.md
│   │        └── completed/
│   └── resources/           ← meetings/, docs/, anything the project uses
├── 2. Areas/
│   ├── AI Setup/            ← same shape; holds the setup task
│   └── <Area Name>/         ← same shape as a project
├── 3. Resources/
└── 4. Archive/
```

Rules for the move:

- **Move, never delete.** Keep a move log in the setup task's folder (old path → new path) so any move can be undone.
- When unsure where something goes, put it in `_to-sort/` at the root and list it for the person. Don't guess at their business.
- Old, finished or dead material goes to `4. Archive/` with its folder intact.
- Keep file names readable and unique; rename `Document (3) final FINAL.docx` only when the person agrees.
- Start small: three to six areas plus AI Setup, and only the projects that are live. A structure they recognise beats a complete one.

## 3. Write the instruction files

**Which file depends on their AI:**

- **Claude only** (the Claude app with Cowork, Claude Code): write `CLAUDE.md` only. No `AGENTS.md`.
- **ChatGPT, Codex, Cursor or other agents only:** write `AGENTS.md` only.
- **Both:** write the content in `AGENTS.md`, and make each `CLAUDE.md` a two-line bridge, written as plain lines and not inside a code block:
  ```
  @AGENTS.md

  Read AGENTS.md in this folder and follow it before anything else.
  ```

**The root file:** what the business is, who is involved, how the person likes to work and be spoken to, the PARA layout, and the working rules (track any real task with the tracking-work skill, keep files in the right project or area, ask before deleting anything or sending anything outside). Keep it under a page; it loads into every session, so every line should change what the AI does.

**Every project and area gets its own file too**, next to its home note. AI tools read the instruction file in the folder they're working in and in every folder above it, so a project's file adds local context on top of the root's. Keep each one short: what this project or area is, who's involved, the decisions and facts an AI needs to work here, where things live. A few lines at setup is fine; it grows as work happens. Don't repeat the root file in it.

## 4. Install the tracking-work skill in their AI

The tracking skill is installed **in the AI, not in the workspace folder**, so it works in every chat, every Cowork task and every workspace they have, without being copied around.

Write the skill from the template in `references/tracking-work-skill.md`, tailored only where they already use different status words. Then install it:

- **Claude (app, Cowork):** package the `tracking-work` folder as a zip (the folder itself, with `SKILL.md` inside, not the file on its own) and have them upload it in Claude's settings where skills are managed. Then turn it on.
- **Claude Code:** put it in their personal skills folder, `~/.claude/skills/tracking-work/SKILL.md`, so it loads in every project.
- **ChatGPT or a tool without skills:** add the tracking rules and template to the root instruction file and to their custom instructions instead. Same method, different home.

Explain it in one line: *every real piece of work gets one file that says where it stands, so any chat, tomorrow or next month, picks up exactly where the last one stopped.* The setup task they are watching fill up is the example.

## 5 to 7. Google Drive, Obsidian and the AI

Click-by-click guidance for syncing with Google Drive for desktop, installing Obsidian, and setting Claude or ChatGPT to work inside the folder is in `references/tools-setup.md`. Read it before guiding them. Labels in these apps change between versions; describe what to look for rather than reciting menu paths, and check with the person that each step landed.

The order matters: put the folder where Google Drive syncs it **first**, then open it in Obsidian, then attach it to the AI. Moving a vault after Obsidian and the AI know its path means redoing both.

## 8. One workspace per world

If the person has separate worlds, give each its own workspace: its own folder, its own PARA, its own instruction files, its own Obsidian vault. The tracking skill is already in their AI, so it works in all of them. Explain why they are separate: an AI working in one workspace sees only that workspace, so a client's details never leak into a personal note, and each session gets only the context that belongs to it.

- Never nest one workspace inside another; place them side by side (for example `My Drive/Workspaces/<Business>` and `My Drive/Workspaces/Personal`).
- Obsidian switches between vaults from its vault menu; each opens on its own.
- Something genuinely shared (a brand kit, a price list) lives in one workspace's `3. Resources/`; the other points to it rather than copying it.
- Each workspace gets its own AI Setup area only if they'll work on AI there; otherwise the first one's is enough.

## 9. Close the setup task, and prove it remembers

Before closing, open a **fresh** chat in the workspace and ask: *"What is this workspace, and what's in progress?"* It should describe the business and point to the AI Setup task without help. If the answer is vague, the instructions aren't loading: fix that first.

Then mark the setup task done (its Task Complete block, its folder moved into `tasks/completed/`), and suggest one small real job from their week as the next task, so the second tracked task is theirs.

## When it's done

They have: one PARA folder with their files in it and nothing lost; a root instruction file and one in every project and area; an AI Setup area with the completed setup task; the tracking-work skill installed in their AI; Obsidian open on the folder; Google Drive syncing it; their AI set to work inside it; and a separate workspace for each world that should not mix.

## Don'ts

- Don't delete anything. Archive it.
- Don't build the full system on day one. A few areas, the live projects, one tracked task.
- Don't lecture on methodology. One sentence per idea, at the moment it's needed.
- Don't put secrets (passwords, API keys, card numbers) into instruction files or synced notes.
- Don't merge separate worlds into one workspace to save setup time.
- Don't write `AGENTS.md` for someone who only uses Claude. One file they understand beats two they don't.
