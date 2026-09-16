---
name: setting-up-a-daily-brief
description: Use when someone wants a daily brief — a researched summary of what happened in their industry, delivered on a schedule before their day starts. Interviews them about their work first, then writes their research contract, builds their template, and wires the schedule for Claude Code or Claude Desktop. Also use when an existing brief needs tuning, or has stopped arriving.
---

# Setting Up a Daily Brief

Builds someone a brief that researches their field overnight, verifies every claim against a
primary source, and is waiting before they start work.

<EXTREMELY-IMPORTANT>
**You do not know what this person does. Ask them.**

Do not pre-fill their industry, their competitors, their regulator, their sources or their
sections from anything you already know — not from the web, not from their company name, not from
another client's setup, not from context elsewhere in this workspace.

A brief built on guesses reads as generic, and generic is the one thing that makes someone stop
opening it. Their own words are better than anything you would infer. **Ask first. Build second.**

If the person says "just set it up, you know my industry" — you still ask. Ask fewer questions,
but ask. Three answers in their words beat twenty assumptions.
</EXTREMELY-IMPORTANT>

## What this builds

```
schedule fires -> research -> verify against primary sources -> write -> deliver
```

| File | Holds |
|---|---|
| `interview.md` | Their answers, in their words. The evidence behind everything else |
| `brief-prompt.md` | Their research contract: beat, watchlist, sections, verification rules |
| `template.html` | Masthead and styling, with a `__CONTENT__` slot |
| `run-brief.sh` | Scheduler entry point (Claude Code route) |
| `send_brief.py` | Email delivery, credential from the OS keychain |
| `recipients.txt` | Who gets it; first address is the sender |
| `seen.jsonl` | Append-only ledger; what stops it repeating itself |

## Step 1 — Interview them

**This is the step that decides whether the brief is any good.** Everything downstream is
plumbing.

Ask conversationally, **one question at a time**, and wait for each answer. Do not present the
whole list at once — people answer a list tersely and ramble helpfully at a single question, and
the specifics you need are in the rambling.

Work through `references/interview.md`. Write their answers into `interview.md` in the instance
folder, **in their own words**. Their phrasing goes into the contract nearly verbatim.

If they only have five minutes, ask these three:

1. **What do you need to know before you walk into a meeting?**
2. **Name the companies, regulators and people you watch.** Write down every name. This is the
   single biggest quality lever — a named company returns signal, an industry name returns noise.
3. **What is definitely not useful?**

Do not move on until you can state their beat back to them and they agree.

## Step 2 — Confirm what you heard

Before building, say back to them in five or six lines: their beat, their watchlist, their
sections in order, what is excluded, when it arrives and where.

Ask them to correct it. They will, and the correction is usually the most valuable thing in the
whole session.

## Step 3 — Choose the route

| | Claude Code (local) | Claude Desktop / Cowork (cloud) |
|---|---|---|
| Runs when their machine is off | No — needs a wake schedule and power | **Yes** |
| Can read local files | **Yes** | **No** |
| Can use connectors (mail, calendar, drive) | Only what you wire | **Yes** |
| Can send email itself | **Yes**, via SMTP | No — drafts via connector, or they read it in Claude |

**The deciding question: does the brief need to write into a folder on their computer?** If yes,
it must run locally. If it needs their work inbox, it must run in the cloud. If neither, start
with Cowork — it is less to maintain and nothing to keep awake.

Mechanics: `references/route-claude-code.md`, `references/route-cowork.md`.

## Step 4 — Write their contract

Copy `references/brief-prompt.template.md` into the instance and fill every `{{PLACEHOLDER}}` from
`interview.md`. **If a placeholder has no answer in the interview, go back and ask** — do not
invent one.

These rules go in whatever the beat, and are not negotiable:

- **Read the ledger first.** Never resend a story already in `seen.jsonl`. Follow-ups only with
  genuine new development, and they must say what changed.
- **Fetch the primary source for every item and read it.** A search snippet is a lead, never a
  citation.
- **Tag every item `Verified` or `Unconfirmed`.** Anything failing the check is dropped, not
  hedged.
- **Resolve conflicts out loud.** Two sources disagree, fetch a third, say which figure you use
  and that others differ.
- **Fewer real items beats padding.** A thin section says so in one line.
- **Absolute dates.** Never "yesterday" — the file is read later.
- **Write it publishable**, assuming they forward it unedited.

## Step 5 — Build the template

Start from `references/template.base.html`. Set the three palette values and the masthead text.

**The model must never emit the template.** It writes a CSS-free fragment; the runner splices it.
A branded template runs to hundreds of KB once assets are embedded, and a model asked to reproduce
that will corrupt the masthead on the day nobody is looking.

**Only use brand assets you have been given.** No logo unless they hand you one, and never another
organisation's mark. Absent real assets, the typographic masthead in the base template is correct
and looks deliberate — ask for a logo later.

## Step 6 — Wire delivery

For email, `references/send_brief.template.py`. Adapt, do not rewrite.

- **Credential in the OS keychain, never a file.** macOS:
  `security add-generic-password -s <service> -a <address> -w`
- **Never type their password for them.** Give them the command; they paste it. A Gmail app
  password is 16 characters with no spaces, and people paste Google's spaced display form, which
  Gmail rejects — so verify shape, never value.
- **Get their address from them.** Not from a directory, roster or signature block.
- **Prove delivery without sending.** Authenticate, `RCPT TO` each recipient, read the `250`, then
  `RSET` before `DATA`.
- **Email last, never fatal.** The brief is saved before the send; a mail outage costs the email,
  never the morning.

## Step 7 — Verify, then hand over

- [ ] One real run, read end to end as its audience would
- [ ] Two source links clicked at random — do they say what the brief says?
- [ ] Rendered in light **and** dark, at phone width
- [ ] If emailed: one sent to yourself, opened **in the destination client**
- [ ] The scheduler's own environment, not your shell
- [ ] The ledger gained a line per item; the next run excludes them
- [ ] **They know how to edit the watchlist themselves** — it is the file they will want to change

## Step 8 — Tune after a week

Three things come up, every time:

**"It tells me things I already know."** Watchlist too broad, or their own sources already cover
it. Narrow to named companies; add what they read daily to the exclusions.

**"There is not enough in it."** Widen the window, or add adjacent markets. **Never relax the
verification rules to fill space** — a thin true brief beats a full shaky one, and the first wrong
figure in front of their board costs more than a month of thin briefs.

**"I only read one section."** Good. Cut the rest. A brief they open daily beats a complete one
they abandon.

## Gotchas

**A scheduler's environment is not a shell.** `launchd` runs with
`PATH=/usr/bin:/bin:/usr/sbin:/sbin` and no nvm. Resolve the binary at runtime, and **prove auth
inside the scheduler** with a throwaway job running `claude -p "Reply with exactly: AUTH_OK"`.

**launchd does not fire on a sleeping Mac.** Pair it with
`sudo pmset repeat wakeorpoweron <DAYS> 06:55:00`, which also powers on from a full shutdown.

**A just-woken machine has no network.** Wait for connectivity before generating.

**Pin the model** with `--model`, or the job inherits whatever default they later set.

**Gmail strips `data:` URI images and ignores `display:block` with `margin:0 auto`.** Images
vanish and the masthead falls left. Email: CID attachments, centred with a table using
`align="center"`. Web: `data:` URIs are fine. Same design, two techniques.

**A cloud routine cannot read local files.** The most common false expectation in this setup.

**Name it distinctly.** If their setup already has an operations brief from their calendar and
inbox, this one needs a different name. Two routines called "Morning brief" confuse everyone.

## One instance per person

Everything in `references/` is generic. Each person gets their own instance folder holding their
interview, contract, template, ledger and recipients. **If you find yourself editing this skill to
fit somebody, that detail belongs in their instance instead.**
