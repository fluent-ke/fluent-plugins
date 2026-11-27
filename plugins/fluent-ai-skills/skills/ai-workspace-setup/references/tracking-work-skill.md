# The tracking-work skill: template and worked example

This skill is installed **in the person's AI**, not in the workspace folder, so it works in every chat and every workspace (step 4 of the main skill says how for each tool). It works untouched; tailor only the status words (`To Do | Doing | Waiting | Done`) if they already use others, changing them in both places they appear.

Leave the `description:` line as it is. That line is what makes the AI use the skill without being reminded; shortening it is how a tracking skill quietly stops working.

---

## Template

````markdown
---
name: tracking-work
description: Use when starting, continuing, handing off or finishing any real piece of work in this workspace — a multi-step job, anything spanning more than one sitting, a change across several files, setting up a new project or area, or anything that produces something someone will reuse. Also when the person says "let's continue", "where were we", "pick this up", "hand off" or "we're done with this".
---

# Tracking Work

Every real piece of work gets **one file**, `<Task Name> - task.md`, in its own folder inside the workspace you're working in: `<project or area>/tasks/<task-name>/`. Anything the task produces (drafts, data, notes) goes in that same folder. If you're not in a workspace folder, ask which one the work belongs to.

The AI has no memory between chats. This file is the memory. A fresh chat, tomorrow or next month, reads it once and knows what is being done, what happened and what's next.

The file has two halves with opposite rules:

- **Live state (top):** what is true right now. Rewrite it in place when things change.
- **Session log (bottom):** what happened, newest first. Add to it; never edit old entries.

## Starting

1. Find the task's file (search the `tasks/` folders by name), or create it from the template below if it's new. If you don't know which project or area it belongs to, ask.
2. On a new task, fill **Intent** before any work: what it's for, what done looks like, what's out of scope. If the person hasn't said, ask.
3. Add a dated session entry at the top of the log **before doing the work**, so the session is on record even if the chat dies.
4. Say in two lines where the task stands and what's next.

## While working

After each milestone or change of direction, update the live state and the current session entry. Don't wait for the end.

**Rewrite the live state; never stack updates on it.** If you're about to write "UPDATE 2" near the top, stop: change the section so it reads true now, and put the history in the session log.

## Handing off

When the person stops ("let's pick this up later", "hand off"):

1. Bring the live state up to date and tick finished steps `[x]`.
2. Finish the session entry with **State** and **Resume**.
3. Give the person one line they can paste into a new chat to carry on.

## Finishing

When the whole task is done: set `Status: Done`, add a **Task Complete** block at the very bottom, and move the task folder into `tasks/completed/`.

## The test

Would someone opening this cold know what was being done, what happened and what's next, without asking? Every line should help them. Decisions carry their reason. Dead ends are written down as plainly as wins.

## Template

```
---
Status: Doing    # To Do | Doing | Waiting | Done
Project: <project or area>
---

# <Task Name>

## Objective
<one line: what finishing looks like>

## Intent
**For:** <why this matters, what changes when it's done>
**Done looks like:** <2-4 checkable points>
**Out of scope:** <what this is not doing>

## Decisions
- <decision>: <why>

## Working / Open
- Working: <what's confirmed good>
- Open: <what's broken or unresolved>

## Open Questions
- <unknown not yet decided>

## Next Steps
- [ ] <next action>

---

# Session Log

## Session 1: YYYY-MM-DD HH:MM
**Goal:** <what this session aimed at>
**Did:** <what was done and what actually happened>
**State:** <where it stands>
**Resume:** <the exact next thing to pick up>
```
````

---

## Worked example: the setup itself

The first task in every new workspace is its own setup. Here it is halfway through, for a bakery owner, Amina, at `2. Areas/AI Setup/tasks/ai-workspace-setup/AI Workspace Setup - task.md`:

```markdown
---
Status: Doing
Project: AI Setup
---

# AI Workspace Setup

## Objective
Amina's business files organised so Claude can work in them and remember between chats.

## Intent
**For:** her files are spread over a Downloads folder, two Drive accounts and WhatsApp, and she re-explains the bakery in every chat.
**Done looks like:**
- Every file in PARA, nothing deleted, every move logged
- Instruction files at the root and in each project and area
- Tracking skill installed in Claude; Drive syncing; Obsidian open on the folder
- A fresh chat can say what the business is and what's in progress
**Out of scope:** her personal files (a separate workspace later), the online shop rebuild.

## Decisions
- Claude only, so `CLAUDE.md` files and no `AGENTS.md`: she doesn't use other AI tools.
- Areas: Sales, Production, Finance, Marketing, AI Setup. Projects: Wholesale Price List, Second Oven. She named them.
- Supplier invoices go to `3. Resources/Suppliers/`, not Finance: she looks prices up there more than she manages them.

## Working / Open
- Working: 412 files moved, log in `move-log.md` in this folder; 23 left in `_to-sort/`. Root and area `CLAUDE.md` files written.
- Open: Google Drive is on Stream; needs switching to Mirror before Obsidian.

## Open Questions
- Do the 2023 wedding-cake orders go to Archive or to a Weddings area?

## Next Steps
- [ ] Amina: switch Google Drive to Mirror files
- [ ] Open the folder in Obsidian
- [ ] Upload the tracking-work skill in Claude's settings
- [ ] Fresh-chat test, then close this task

---

# Session Log

## Session 2: 2026-03-12 10:15
**Goal:** reorganise into PARA and write the instruction files.
**Did:** got her yes on the map; moved 412 files (`move-log.md`); wrote root `CLAUDE.md` and one per area and project. Found a passwords note and left it out; she's moving it to a password manager.
**State:** structure done; tools not set up yet.
**Resume:** switch Drive to Mirror, then Obsidian.

## Session 1: 2026-03-10 16:40
**Goal:** understand the business and map the mess.
**Did:** interviewed Amina (bakery, 4 staff, sells retail and to three cafés); surveyed 435 files across Downloads and Drive; drafted the PARA map.
**State:** map ready to show her.
**Resume:** show the map, get a yes, start moving.
```

What this shows the person:

- If the chat dies, the next one reads this file and carries on from "switch Drive to Mirror". Nobody re-explains anything.
- The **Decisions** carry their reasons, so nobody later moves supplier invoices back into Finance.
- The first Next Step names Amina, so it's plain what's waiting on her and what's on the AI.
- What the task produced (`move-log.md`) sits in its folder.
