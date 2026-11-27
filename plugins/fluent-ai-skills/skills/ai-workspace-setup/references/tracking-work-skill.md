# The tracking-work skill: template and worked example

Write the template below into the person's workspace at `.claude/skills/tracking-work/SKILL.md`. It works untouched; tailor only two things:

1. **The status words** (`To Do | Doing | Waiting | Done`) if they already use others. Change them in both places they appear.
2. **The folder names** in the paths, if their PARA folders are named differently.

Leave the `description:` line as it is. That line is what makes the AI use the skill without being reminded; shortening it is how a tracking skill quietly stops working.

---

## Template

````markdown
---
name: tracking-work
description: Use when starting, continuing, handing off or finishing any real piece of work in this workspace — a multi-step job, anything spanning more than one sitting, a change across several files, setting up a new project or area, or anything that produces something someone will reuse. Also when the person says "let's continue", "where were we", "pick this up", "hand off" or "we're done with this".
---

# Tracking Work

Every real piece of work gets **one file**, `<Task Name> - task.md`, in its own folder: `<project or area>/tasks/<task-name>/`. Anything the task produces (drafts, data, notes) goes in that same folder.

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

## Worked example

A bakery owner, Amina, set up her workspace. Her areas are Sales, Production, Finance and Marketing. Here is a real task two sessions in, at `2. Areas/Sales/tasks/wholesale-price-list/Wholesale Price List - task.md`:

```markdown
---
Status: Waiting
Project: Sales
---

# Wholesale Price List

## Objective
A one-page wholesale price list Amina can send to cafés and supermarkets.

## Intent
**For:** three cafés asked for wholesale prices last month and she quoted each one differently from memory. One list means consistent prices and a faster yes.
**Done looks like:**
- Every product at a wholesale price with at least 35% margin at current flour and butter costs
- Minimum order and delivery terms stated
- A PDF on her letterhead, ready to send
**Out of scope:** retail prices, the online shop, a supermarket listing deal.

## Decisions
- Price per dozen, not per piece: the cafés all order by the dozen.
- Free delivery above 5,000 KES only: below that, delivery cost wipes out the margin (worked out from last month's fuel receipts in `resources/`).

## Working / Open
- Working: costs per item calculated in `costing.xlsx` in this folder; draft list written.
- Open: sourdough margin is only 22%. Amina wants to check the new flour supplier's price before deciding.

## Open Questions
- Raise the sourdough price, or drop it from the wholesale list?

## Next Steps
- [ ] Amina: get the new supplier's flour quote (she's calling Thursday)
- [ ] Recalculate sourdough with the new flour price
- [ ] Put the list on her letterhead and export the PDF

---

# Session Log

## Session 2: 2026-03-12 10:15
**Goal:** turn the costings into a draft list.
**Did:** applied a 35% margin to every item; wrote the draft (`draft-price-list.md`); set delivery terms from the fuel receipts. Sourdough came out at 22%.
**State:** draft done except sourdough; waiting on Amina's flour quote.
**Resume:** when the flour quote is in, recalculate sourdough in `costing.xlsx`, then build the PDF.

## Session 1: 2026-03-10 16:40
**Goal:** work out what each product actually costs.
**Did:** pulled ingredient prices from the last three supplier invoices in `3. Resources/Suppliers/`; built `costing.xlsx`. Butter had gone up 18% since her last pricing.
**State:** costs known for all 11 products.
**Resume:** apply margins and draft the list.
```

What this shows the person:

- A fresh chat, opened next week with "let's finish the price list", reads this file and starts on the sourdough recalculation. Nobody re-explains anything.
- The **Decisions** carry their reasons, so nobody later "fixes" free delivery back to every order.
- **Waiting** plus the first Next Step makes it plain the task is on Amina, not the AI.
- Everything the task produced (`costing.xlsx`, `draft-price-list.md`) sits in its folder.
