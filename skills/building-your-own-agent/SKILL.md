---
name: building-your-own-agent
description: Use when someone wants AI to take over a job they repeat — a weekly report, a monthly update, the same analysis or the same write-up every time — or says "make this repeatable", "set it up so it just does this", "I do this every week and I'm tired of explaining it". Also when a job was just finished well and should never have to be explained again, when someone asks for a CLAUDE.md, an AGENTS.md, or project instructions, or when they want an assistant for one specific job rather than a general chat.
license: MIT
metadata:
  author: fluent
  version: "0.1"
---

# Building Your Own Agent

## What this is for

Someone does the same job every week and explains it from scratch to an AI every week. The explaining costs more than the job.

An agent ends that. Not a personality, not a clever prompt — **a job, the steps, an example of the finished thing, and permission to get on with it**, written down where the tool picks it up on its own.

**The folder is the agent.** Each tool wraps it in its own thing: Claude Code and Cowork read the folder you point them at; the ChatGPT desktop app builds a project around it. The wrapper changes, the folder does not. In a browser there is no folder, so the same content goes into a project's instructions — see *In a browser*.

The person you are helping is usually not technical. They do not need to know what a model is or what an MCP server is. It is a few text files. Do not teach the machinery.

## The shape

1. Find the specimen
2. Check the job is ready
3. Write it
4. Run it once
5. Hand it over

## 1. Find the specimen

The failure this skill exists to prevent is writing an agent out of your imagination while the person's real work sits untouched.

**Never build from a description when a specimen exists.** Look, in this order:

| What they have | What you do |
|---|---|
| **They just did the job with you, in this conversation** | Build from the conversation. It is already in your context — you do not need a transcript |
| **They are about to do it** | Offer to keep a running note in `notes/run-log.md` as you go, then build from that. Worth it for a long job, overkill for a short one |
| **Past work on their machine or in their drive** | Read several. What repeats is the template; what changes is the input |
| **None of it** | Then, and only then, the five questions |

### From a job you just did

The corrections are the gold. Every "no, shorter", "biggest one first", "we never include those", "we call these Cost Reviews" is a rule the person did not know they had and would never say in an interview. Collect all of them.

Then, in order of value:

1. **The corrections** → the rules
2. **The steps that actually happened** — including ones nobody would think to mention
3. **The output they accepted** → save that artefact as the example. Do not re-derive a template from memory when the approved thing exists
4. **The inputs, and where they came from**
5. **Dead ends** → a short "don't bother with" note

**Separate the instance from the procedure, and say the split to them before you write a file.** A run is one month's numbers, one client's name. An agent that bakes those in looks right on the day it is built and is wrong the second time.

Say it in the conversation: *"I'm treating the Q3 figures as this month's input and the three-section structure as the rule. Right?"* Writing the split into the instructions instead is not the same thing — a wrong split then ships silently, inside a file they will not read.

### From work they already have

Read several, not one:

- What they always follow → `templates/`
- What is constant versus what changes → constants are rules, variables are inputs
- The most recent accepted one → `examples/`

**Check the evidence before you enshrine it.** Past work carries past mistakes — arithmetic that does not add up, a paragraph copy-pasted for three weeks. Copy the format, not the errors, and tell them what you found.

Files show outputs, never process, so this door ends with two questions: where does the raw material come from, and what would make one of these wrong?

**If the example carries a real client's name or figures, ask before saving it, or swap the identifying details.** It is the format you need, not the client. This matters most for the people this skill helps most — consultants and agencies holding several clients' material, often in a synced drive.

### When there is no example at all

Do not invent one. A made-up example teaches a made-up voice, and once it sits in `examples/` nobody replaces it.

Ship without one, put a line in the instructions — *"No example yet. The first output the person accepts gets saved here"* — and tell them that is the step left. If you must show a shape, put it in `templates/` as a skeleton with placeholders, never in `examples/` as a finished specimen.

### The five questions

Only when there is no run and no files:

1. What is the job, in one sentence — and how often does it come round?
2. Walk me through the last time you did it. What did you start with, what did you end with?
3. **Send me the last one you did.** Not "a good one" — people who work by hand have last month's file, not a thing they would call exemplary
4. What would have made that one wrong?
5. Where does the material come from, and where does the finished thing go?

Then play the job back in their words, ask "is that it?", and write.

### The output has the parts they named, in their order

Whatever the door, the finished thing's parts come from **their example, or the words they used** — nothing else. They said four things, it has four things, in that order, under their names for them.

If the job genuinely needs a part they did not name, add it and say so in one line: *"I added a subject line — say if you'd rather it didn't."* A greeting, a sign-off, a summary paragraph and a duplicate list are four parts they did not ask for, and each is a small future argument with the output.

## 2. Check the job is ready

| Condition | Fails when |
|---|---|
| **Same shape every time** | Every instance is a fresh judgement call |
| **Reachable material** | It lives behind a login the agent does not have |
| **You can point at a good one** | Nothing has ever been written down and nothing can be shown |
| **Checkable in a minute** | Verifying costs as much as doing it |
| **Cheap to be wrong** | It sends, pays or publishes with no human in between |

The last one is a gate, not a veto. That job still becomes an agent — one that **stops at the draft**. Say so as soon as it applies: it changes the trigger you write in step 3 and the test run in step 4.

**"Not yet" beats "no".** Name the condition that failed and what would fix it: *"Four of the five hold. What's missing is one you've already done — dig out last month's, drop it in, and this works."*

## 3. Write it

```
cost-reviews/
├── AGENTS.md          the agent: the job, the trigger, the rules, the map
├── CLAUDE.md          two lines, so Claude reads the same file
├── workflows/
│   └── cost-review.md      the numbered procedure
├── examples/
│   └── good-one.md         the finished thing they accepted
├── templates/
├── input/             where material arrives
└── output/            where finished work lands
```

**`AGENTS.md` and `CLAUDE.md` are the only two that must exist.** Everything else earns its place from the job. Write those two first, so five minutes gets a working agent.

**The filenames are not a style choice.** Those two names are what the tools open by themselves. `instructions.md` or `how-to.md` is a file the person attaches by hand every time, which is the thing they asked you to end. Which tool reads which, and the exact two-line bridge for `CLAUDE.md`: `references/platform-homes.md`.

**Write the bridge into the file as plain lines, never inside a code fence.** Tested: an import inside a fence is treated as an example and does not load, so the agent silently gets nothing.

`AGENTS.md` carries: what the agent is for, the trigger, where the procedure lives, the rules, and what access it needs. Keep the procedure in `workflows/` — the instruction file loads every session, the rest is opened only when the job runs.

A complete agent built from a real job: `references/example-agent.md`.

### The trigger

The one sentence that ends the explaining. Put it in every agent, in the person's own terms:

> When a file lands in `input/`, or I say "run it", do the job. Don't ask questions first. Ask only if the input is missing or unreadable.

**For a job that sends, pays or publishes, write the gated form instead:**

> When a file lands in `input/`, or I say "run it", do the job **and stop at the draft**. Show me the result. Never send, pay or publish unless I ask for it in that run.

Without a trigger, the agent interviews the person every time and the promise quietly dies. With the wrong one, it does something irreversible on their behalf.

## In a browser

On claude.ai or ChatGPT on the web there is no folder. The same content goes into a project, and **three things must be rewritten, not just flattened**:

| Folder version | Browser version |
|---|---|
| "When a file lands in `input/`" | "When I paste the numbers, or say run it" |
| Writes to `output/2026-W31-report.md` | "Reply with the finished report — I'll save it" |
| Appends to `output/log.md` | "Keep the running log as a project file I update", or drop it |

Then put the procedure and rules inline in the instructions field, since there is no file tree to point at, and **name the example and template explicitly** so the model reaches for the right one. Produce those two as documents they can save and upload — never write "upload the example" as though it already exists.

**Do not read portability as "avoid every platform feature".** That reasoning ends in a prompt the person re-pastes forever. What travels is the instructions; use the best home the tool offers.

**A tool not in the reference table** — a chat app with no folders and no projects — gets the same treatment: instructions pasted at the top of a new chat, and one saved copy they keep.

## 4. Run it once

Do the job with the agent you just built, on their real input, and show them the result. It takes one run and it is the only proof the thing works. Everything before it is a folder of assertions.

It is also where you find out the evidence was wrong. Watch the arithmetic.

**If the job sends, pays or publishes, the test run stops at the draft.** Never let the proof run be the thing that goes out.

## 5. Hand it over

Give them the steps for **the tool they already use**. Literal steps, not the concept — for someone who has never opened a terminal, "open a terminal in the folder" is where they stop. Never make installing something a precondition for having anything that works.

**Then, if they are browser-only, tell them once what a desktop app would add.** A folder beats a project for the same agent: it writes the output itself instead of handing it back for them to save, it keeps its own history, the example and template sit beside it, and nothing gets pasted. One sentence with the gain, and leave the choice with them — `references/platform-homes.md` has what each tool allows and how a folder is attached. Say it once. If they are happy in the browser, that agent still works.

Then give them the smoke test, because the first thing anyone wants to know is whether it read the file at all:

> Start it and ask: *"what job are you set up for?"* If it can't tell you, the instructions aren't loading.

## Make the second run land where the first one did

For a folder agent. One that files differently each time stops being trusted on run three. Put these in the workflow as filled-in values, never as advice:

- **An exact output name**, with a worked instance: `output/2026/2026-W31-report.md`
- **Where it goes** — shaped by the job. Recurring output gets a year folder; processing what arrives gets `input/new/` and `input/done/` so nothing runs twice; research gets `sources/`
- **A one-line run log**, same fields every time, so it can be read back
- **What to do if the file already exists** — decided in the file, not at run time

## Access to the material

An agent cannot connect itself to Gmail or Drive. Those are account-level, set up by the person.

**Name the access, verify it, never assume it.** Write into the instructions what the agent needs and what to do without it — stop and say so, rather than half-doing the job. Then offer the manual path, which works everywhere and needs no permissions: export or download into `input/`. For a monthly job that is often the right answer, not the fallback. Ask which they want; do not silently pick.

## Leave it able to grow

End the instructions with a standing line: when the job changes or a variant appears, add another file to `workflows/` rather than starting over. That is what keeps an agent alive instead of frozen at the moment it was built.

## Common mistakes

Every one of these came from watching agents build these without this skill.

| What happens | What it actually is |
|---|---|
| Hands over a prompt to re-paste each time | Instructions with no home. Six manual steps forever |
| Names the file `instructions.md` or `how-to.md` | A file nothing loads. The name is the mechanism |
| Buries it in a hidden config folder | Not something the person owns, sees, or can hand to anyone |
| Invents the format from their description | The specimen was in the room and you did not ask for it |
| Invents an example when none exists | A made-up specimen teaches a made-up voice, and never gets replaced |
| Adds sections nobody asked for | A greeting, a sign-off, a duplicate list. Bloat from imagination |
| Quietly reshapes what they described | Their four sections became three. Keep their shape, or name the change |
| Bakes in this month's numbers or this client's name | Right on day one, wrong on run two |
| Records the instance-versus-rule split in the file instead of saying it | Documentation is not confirmation. A wrong split ships silently |
| Refuses a tool's own feature "for portability" | Lowest common denominator. The instructions travel; the mechanism need not |
| Ships a browser agent that writes to `input/` and `output/` | Folders that do not exist. Rewrite the trigger, the destination and the log |
| Copies the format and the errors with it | Past work carries past mistakes. Check the arithmetic first |
| Writes into the person's home directory unasked | Ask where it goes. It is their machine |

## Red flags — stop

- You are about to write the agent without having seen one finished example of the work
- The job can send, pay or publish, and the trigger you wrote does not stop at the draft
- You are about to do a live test run of a job that sends, pays or publishes
- You are saving a named client's real figures somewhere without asking
- You are handing over something you never ran

---

Stuck, or want to send feedback on this skill? Read the `about-fluent` skill.
