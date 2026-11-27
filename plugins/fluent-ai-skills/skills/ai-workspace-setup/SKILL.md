---
name: ai-workspace-setup
description: Use when someone wants their business files set up so AI can actually work in them — a messy folder, a Google Drive full of documents, context scattered across chats — or says "organise my files", "set up PARA", "set up a second brain", "make an Obsidian vault", "I want Claude (or ChatGPT) to know my business", "my AI keeps forgetting what we did", or "I want my work tracked". Also when they need to sync a work folder with Google Drive, point Claude or ChatGPT at one folder, or keep separate workspaces (two businesses, business and personal) apart.
license: MIT
metadata:
  author: fluent
  version: "0.4"
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
8. Make it portable: instructions, memory and Drive
9. Repeat for each separate workspace
10. Close the setup task, and prove it remembers

Steps 4 to 8 need the person's own computer and accounts. Guide them click by click and confirm each one worked before moving on. Everything else you do yourself.

## 1. Understand the person, and open the setup as their first task

Ask, conversationally and few at a time: what the business does, who else works in it, what their week looks like, which AI they use (Claude, Claude Code, ChatGPT, a browser only), and where their files live today.

If they've already told you enough and said "just do it", don't hold them up with questions: work from what they gave you, and write your assumptions into the setup task's Decisions so they can correct them later.

Then look at the folder yourself. Get the shape before the detail: how many files, what kinds, the obvious clusters (clients, money, marketing, admin), exact duplicates, personal files mixed in with business ones, and anything sensitive (ID scans, bank statements, passwords). Note any date in their notes that has already passed (a lease ending, a plan for "mid next year") as an Open Question in the setup task; stale facts in instruction files mislead every later chat.

**Passwords, PINs or keys in a plain file:** leave that file where it is, outside the workspace and anything that syncs. Don't copy its contents anywhere. Tell them plainly: move these into a password manager, change the ones that were sitting in plain text, then delete the file themselves.

**The setup itself is the first tracked task.** Create the area `2. Areas/AI Setup/` straight away and open `2. Areas/AI Setup/tasks/ai-workspace-setup/AI Workspace Setup - task.md` using the template in `references/tracking-work-skill.md`, which also shows this exact task filled in. Record each step in it as you go. The person sees tracking work on something real from the first minute, and if the chat dies halfway, the next one picks up from the file. The AI Setup area stays as the home for everything about how they work with AI from then on: new skills, instruction changes, tools they try.

If they work in more than one world that should not mix (two businesses, a business and a household, a client they work inside), note it now. That is step 9, and it shapes step 2.

## 2. Propose the PARA map, then reorganise

Show the proposed structure before moving anything: the projects and areas you found, named in their words, and where each existing folder goes. A short table of *current folder → new home* is enough. Get a yes, then move. If they already said "just do it", move, and put the table in the setup task so they can review it after.

If one messy folder holds two worlds (business and personal, say), split it now into **sibling workspaces** under one parent folder, each with its own PARA. The parent holds only the workspaces, no files and no instructions. See step 9.

The layout every workspace uses:

```
<Workspace Name>/
├── CLAUDE.md                ← who they are, how the workspace works
├── 1. Projects/<Project Name>/
│   ├── <Project Name>.md    ← home note: what it is, status, key links
│   ├── CLAUDE.md            ← what an AI needs to know to work here
│   ├── tasks/<task-name>/<Task Name> - task.md   (when the first task starts)
│   └── resources/           ← (when there's something to put in it)
├── 2. Areas/
│   ├── AI Setup/            ← same shape; holds the setup task
│   └── <Area Name>/         ← same shape as a project
├── 3. Resources/
└── 4. Archive/
```

Rules for the move:

- **Move, never delete.** Keep a move log in the setup task's folder (old path → new path) so any move can be undone.
- A file that belongs to two worlds goes where it's mostly used; note the call in the setup task.
- Folders left empty by the move can be removed.
- When unsure where something goes, put it in `_to-sort/` at the root and list it for the person. Don't guess at their business.
- Old, finished or dead material goes to `4. Archive/` with its folder intact.
- Keep file names readable and unique; rename `Document (3) final FINAL.docx` only when the person agrees.
- Start small: three to six areas plus AI Setup, and only the projects that are live. A structure they recognise beats a complete one. At setup, each project and area gets just its home note and instruction file; `tasks/` and `resources/` appear when there's something to put in them.

## 3. Write the instruction files

**Which file depends on their AI:**

- **Claude only** (the Claude app with Cowork, Claude Code): write `CLAUDE.md` only. No `AGENTS.md`.
- **ChatGPT, Codex, Cursor or other agents only:** write `AGENTS.md` only.
- **Both:** write the content in `AGENTS.md`, and make each `CLAUDE.md` a two-line bridge, written as plain lines and not inside a code block:
  ```
  @AGENTS.md

  Read AGENTS.md in this folder and follow it before anything else.
  ```

**The root file:** every workspace has one at its top. It explains the workspace: what the business (or this part of their life) is, who is involved, how the person likes to work and be spoken to, the PARA layout, and the working rules (track any real task with the tracking-work skill, keep files in the right project or area, ask before deleting anything or sending anything outside). Keep it under a page; it loads into every session, so every line should change what the AI does.

**Every project and area gets its own file too**, next to its home note. AI tools read the instruction file in the folder they're working in and in every folder above it, so a project's file adds local context on top of the root's. Keep each one short: what this project or area is, who's involved, the decisions and facts an AI needs to work here, where things live. A few lines at setup is fine; it grows as work happens. Don't repeat the root file in it.

## 4. Install the tracking-work skill in their AI

The tracking skill is installed **in the AI, not in the workspace folder**, so it works in every chat, every Cowork task and every workspace they have, without being copied around.

Write the skill from the template in `references/tracking-work-skill.md`, tailored only where they already use different status words. Save anything they need to install or paste themselves (the skill zip, a custom-instructions text) in the setup task's folder and point them to it. Then install it:

- **Claude (app, Cowork):** package the `tracking-work` folder as a zip (the folder itself, with `SKILL.md` inside, not the file on its own) and have them upload it in Claude's settings where skills are managed. Then turn it on.
- **Claude Code:** put it in their personal skills folder, `~/.claude/skills/tracking-work/SKILL.md`, so it loads in every project.
- **ChatGPT or a tool without skills:** put the tracking rules and template in the root `AGENTS.md`, and the short version from `references/tools-setup.md` in their custom instructions. Same method, different home.

Explain it in one line: *every real piece of work gets one file that says where it stands, so any chat, tomorrow or next month, picks up exactly where the last one stopped.* The setup task they are watching fill up is the example.

## 5 to 7. Google Drive, Obsidian and the AI

Click-by-click guidance for syncing with Google Drive for desktop, installing Obsidian, and setting Claude or ChatGPT to work inside the folder is in `references/tools-setup.md`. Read it before guiding them. Labels in these apps change between versions; describe what to look for rather than reciting menu paths, and check with the person that each step landed.

The order matters: put the folder where Google Drive syncs it **first**, then open it in Obsidian, then attach it to the AI. Moving a vault after Obsidian and the AI know its path means redoing both.

## 8. Make it portable: instructions, memory and Drive

The folder on a computer is where the AI is most powerful: it reads and writes the files itself. But the person will also talk to their AI on a phone, in a browser, or in a chat that isn't attached to the folder. Those chats should still know the setup and still reach the files. Three things make that work:

1. **A workspace brief.** Write `workspace-brief.md` in the setup task's folder, short enough to paste into a settings field:
   - who they are and what each workspace is, in a line each
   - where each workspace lives in Google Drive (`My Drive/Workspaces/<Name>`)
   - the PARA layout, and that the root `CLAUDE.md` or `AGENTS.md` is read first
   - how to work **with** the folder: read the root file, track real work in a `task.md`
   - how to work **without** it: search Google Drive for the workspace, read its root file, find a task by searching for its `- task.md` file; if the chat can't save to Drive, give the updated task file or document as text to save, or say it's best finished on the computer
   - which workspace never to mix with which
2. **Custom instructions and memory.** Have them paste the brief into Claude's Preferences or ChatGPT's custom instructions; this replaces the shorter line in `references/tools-setup.md`. Then have them save it to the AI's memory too, where it has one (ask the AI to remember the workspace setup, then check it appears in memory settings). Settings fields have length limits: if the brief doesn't fit, keep the "how to work" lines in the field and put the rest in memory.
3. **Google Drive connected to the AI.** Have them connect Google Drive in Claude's or ChatGPT's connectors, signed in to the same Google account that syncs the workspace. Then a chat anywhere can search and read the workspace files. Whether it can also create or edit files depends on the connector; test it with a small note and tell them what it can do.

Check it: on their phone or in a browser chat with no folder, ask *"What's in progress in my <Name> workspace?"* It should find the workspace in Drive and read the open tasks. Update the brief whenever a workspace is added or moved.

## 9. One workspace per world

If the person has separate worlds, give each its own workspace: its own folder, its own PARA, its own instruction files, its own Obsidian vault. Track the whole setup, all workspaces, in the one AI Setup task in the first workspace. The tracking skill is already in their AI, so it works in all of them. Explain why they are separate: an AI working in one workspace sees only that workspace, so a client's details never leak into a personal note, and each session gets only the context that belongs to it.

- Never nest one workspace inside another; place them side by side (for example `My Drive/Workspaces/<Business>` and `My Drive/Workspaces/Personal`).
- Obsidian switches between vaults from its vault menu; each opens on its own.
- The workspace brief names every workspace, and the fresh-chat test in step 10 runs in each one.
- Something genuinely shared (a brand kit, a price list) lives in one workspace's `3. Resources/`; the other points to it rather than copying it.
- Each workspace gets its own AI Setup area only if they'll work on AI there; otherwise the first one's is enough.

## 10. Close the setup task, and prove it remembers

Until the person has done their steps, leave the setup task at `Status: Waiting` with their steps first in Next Steps. Before closing, open a **fresh** chat in the workspace and ask: *"What is this workspace, and what's in progress?"* It should describe the business and point to the AI Setup task without help. If the answer is vague, the instructions aren't loading: fix that first.

Then mark the setup task done (its Task Complete block, its folder moved into `tasks/completed/`), and suggest one small real job from their week as the next task, so the second tracked task is theirs.

## When it's done

They have: one PARA folder with their files in it and nothing lost; a root instruction file and one in every project and area; an AI Setup area with the completed setup task; the tracking-work skill installed in their AI; Obsidian open on the folder; Google Drive syncing it; their AI set to work inside it; the workspace brief in their custom instructions and memory, with Drive connected so chats away from the computer still reach the files; and a separate workspace for each world that should not mix.

## Don'ts

- Don't delete anything yourself. Archive it. (Exact duplicates go to `4. Archive/` too; deleting is the person's call.)
- Don't build the full system on day one. A few areas, the live projects, one tracked task.
- Don't lecture on methodology. One sentence per idea, at the moment it's needed.
- Don't put secrets (passwords, API keys, card numbers) into instruction files or synced notes.
- Don't merge separate worlds into one workspace to save setup time.
- Don't write `AGENTS.md` for someone who only uses Claude. One file they understand beats two they don't.
