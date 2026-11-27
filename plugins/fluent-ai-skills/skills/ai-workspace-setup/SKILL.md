---
name: ai-workspace-setup
description: Use when someone wants their business files set up so AI can actually work in them — a messy folder, a Google Drive full of documents, context scattered across chats — or says "organise my files", "set up PARA", "set up a second brain", "make an Obsidian vault", "I want Claude (or ChatGPT) to know my business", "my AI keeps forgetting what we did", or "I want my work tracked". Also when they need to sync a work folder with Google Drive, point Claude or ChatGPT at one folder, or keep separate workspaces (two businesses, business and personal) apart.
license: MIT
metadata:
  author: fluent
  version: "0.1"
---

# AI Workspace Setup

## What this is for

An AI is only as useful as the context it can reach. Most business owners have that context, but it is spread across a downloads folder, three Drive accounts, WhatsApp exports and old chats, so every session starts from zero and they explain their business again.

This skill turns that mess into a **workspace**: one folder, organised with PARA, opened in Obsidian, synced by Google Drive, with instructions that make the AI work inside it and a tracking skill that makes it remember. It is the setup we run every day at Fluent, generalised for anyone.

The person does not need to code. Do the work for them; explain each piece in one or two plain sentences as you reach it, never as a lecture up front.

## The pieces, in plain words

- **PARA** is four folders that everything fits into, sorted by how active it is:
  - `1. Projects`: work with a finish line ("Launch the wholesale price list", "Hire a sales rep").
  - `2. Areas`: responsibilities that never end ("Sales", "Finance", "Marketing", "Operations").
  - `3. Resources`: reference you reuse (templates, price lists, brand files, contacts, research).
  - `4. Archive`: anything finished or no longer active. Nothing is deleted; it moves here.
  The test for any file: *is it something I'm finishing, something I keep running, something I look things up in, or something I'm done with?*
- **A vault** is just a folder that Obsidian opens. Nothing is locked in: the files stay ordinary Markdown documents the person owns, readable by any AI or editor. Obsidian adds a small hidden `.obsidian` folder for its own settings.
- **The instruction file** (`AGENTS.md`, plus a two-line `CLAUDE.md`) sits in the folder and tells the AI who the person is, how the workspace is laid out and how to work. Each project and area can have its own, so the AI picks up local context when it works there.
- **The tracking skill** gives every real piece of work one `task.md` file holding its current state and a log of each session. It is how the AI remembers between chats.

## The shape

1. Understand the person and their mess
2. Propose the PARA map, then reorganise
3. Write the instruction files
4. Generate their tracking-work skill
5. Install Obsidian and open the vault
6. Sync the folder with Google Drive
7. Point their AI at the folder
8. Repeat for each separate workspace
9. Do one real task with them, tracked

Steps 5 to 7 need the person's own computer and accounts. Guide them click by click and confirm each one worked before moving on. Everything else you do yourself.

## 1. Understand the person and their mess

Ask, conversationally and few at a time: what the business does, who else works in it, what their week looks like, which AI they use (Claude app, Claude Code, Cowork, ChatGPT, a browser only), and where their files live today.

Then look at the folder yourself. Get the shape before the detail: how many files, what kinds, the obvious clusters (clients, money, marketing, admin), duplicates, and anything sensitive (ID scans, passwords, bank statements). **If there is a text file of passwords or keys, say so and recommend a password manager; never copy it into the new structure as-is.**

If they work in more than one world that should not mix (two businesses, a business and a household, a client they work inside), note it now. That is step 8.

## 2. Propose the PARA map, then reorganise

Show the proposed structure before moving anything: the projects and areas you found, named in their words, and where each existing folder goes. A short table of *current folder → new home* is enough. Get a yes, then move.

The layout every workspace uses:

```
<Workspace Name>/
├── AGENTS.md                ← who they are, how the workspace works
├── CLAUDE.md                ← two-line bridge to AGENTS.md
├── .claude/skills/tracking-work/SKILL.md
├── 1. Projects/<Project Name>/
│   ├── <Project Name>.md    ← home note: what it is, status, key links
│   ├── AGENTS.md            ← project-specific context (optional at first)
│   ├── tasks/<task-name>/<Task Name> - task.md
│   └── resources/           ← meetings/, docs/, anything the project uses
├── 2. Areas/<Area Name>/    ← same shape as a project
├── 3. Resources/
└── 4. Archive/
```

Rules for the move:

- **Move, never delete.** Keep a move log (`4. Archive/reorganisation-log.md`: old path → new path) so any move can be undone.
- When unsure where something goes, put it in `_to-sort/` at the root and list it for the person. Don't guess at their business.
- Old, finished or dead material goes to `4. Archive/` with its folder intact.
- Keep file names readable and unique; rename `Document (3) final FINAL.docx` only when the person agrees.
- Start small: three to six areas and only the projects that are live. A structure they recognise beats a complete one.

## 3. Write the instruction files

Write a root `AGENTS.md` from what you learned: what the business is, who is involved, how the person likes to work and be spoken to, the PARA layout, and the working rules (use the tracking skill for any real task, keep files in the right project or area, ask before deleting or sending anything outside). Keep it under a page; it loads into every session, so every line should change what the AI does.

Write `CLAUDE.md` beside it as two plain lines, not inside a code block:

```
@AGENTS.md

Read AGENTS.md in this folder and follow it before anything else.
```

Claude Code and Cowork read `CLAUDE.md`; most other tools read `AGENTS.md`. The bridge means the instructions are written once.

Add a project's or area's own `AGENTS.md` only when it has context worth carrying (a client's background, a recurring process). Empty files are noise.

## 4. Generate their tracking-work skill

Write `.claude/skills/tracking-work/SKILL.md` into the workspace from the template in `references/tracking-work-skill.md`, tailored to them: their status words, their project and area names in the example. Then create their first real `task.md` with them so they see it work. The worked example in that reference shows a full task file mid-flight.

Explain it in one line: *every real piece of work gets one file that says where it stands, so any chat, tomorrow or next month, picks up exactly where the last one stopped.*

If their AI cannot load skills (a browser-only ChatGPT, for example), put the tracking rules and template into the instructions instead (step 7). Same method, different home.

## 5 to 7. Obsidian, Google Drive and the AI

Click-by-click guidance for installing Obsidian, syncing with Google Drive for desktop, and setting up Claude (app, Projects, Preferences, Cowork, Claude Code) or ChatGPT to work inside the folder is in `references/tools-setup.md`. Read it before guiding them. Labels in these apps change between versions; describe what to look for rather than reciting menu paths, and check with the person that each step landed.

The order matters: put the folder where Google Drive syncs it **first**, then open it in Obsidian, then attach it to the AI. Moving a vault after Obsidian and the AI know its path means redoing both.

## 8. One workspace per world

If the person has separate worlds, give each its own workspace: its own folder, its own PARA, its own `AGENTS.md`, its own tracking skill, its own Obsidian vault. Explain why: an AI opened in one workspace sees only that workspace, so a client's details never leak into a personal note, and each AI session gets only the context that belongs to it.

- Never nest one workspace inside another; place them side by side (for example `My Drive/Workspaces/<Business>` and `My Drive/Workspaces/Personal`).
- Obsidian switches between vaults from its vault menu; each opens on its own.
- Something genuinely shared (a brand kit, a price list) lives in one workspace's `3. Resources/`; the other points to it rather than copying it.

## 9. Do one real task with them, tracked

Finish by doing one small real job from their week inside the new workspace, with a `task.md`, so they see the whole loop: open the folder, ask, the AI finds the context, does the work, records it. Then close a session and open a fresh one to show it picks up where it stopped. That moment is what makes the setup stick.

## When it's done

They have: one PARA folder with their files in it and nothing lost; `AGENTS.md` and `CLAUDE.md` written; a tracking-work skill and at least one real `task.md`; Obsidian open on the folder; Google Drive syncing it; their AI set to work inside it; and a separate workspace for each world that should not mix.

Check before saying done: open the folder in their AI fresh and ask "what is this workspace and what's in progress?". If the answer is right without help, the setup works.

## Don'ts

- Don't delete anything. Archive it.
- Don't build the full system on day one. A few areas, the live projects, one tracked task.
- Don't lecture on methodology. One sentence per idea, at the moment it's needed.
- Don't put secrets (passwords, API keys, card numbers) into instruction files or synced notes.
- Don't merge separate worlds into one workspace to save setup time.
