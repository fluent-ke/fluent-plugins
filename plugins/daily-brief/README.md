# Daily Brief

A daily brief that researches your field overnight, verifies every claim against a primary source,
and is waiting before your day starts.

Built by [Fluent](https://fluent.ke).

## What it does

It **interviews you first.** It does not assume it knows your industry, your competitors or your
regulator — those come from you, and the brief is only as good as that conversation.

Then it writes your research contract, builds your template, and wires the schedule.

```
schedule fires -> research -> verify against primary sources -> write -> deliver
```

## Install

In Claude Code:

```
/plugin marketplace add fluent-ke/fluent-plugins
/plugin install daily-brief@fluent
```

In the Claude desktop app or Cowork: **Customize → Plugins**, add the marketplace `fluent-ke/fluent-plugins`, then install **Daily Brief**.

Then:

```
/setup-brief
```

Answer the questions. It builds the rest.

## Commands

| Command | What it does |
|---|---|
| `/setup-brief` | Interviews you, then builds and schedules your brief |
| `/brief-now` | Runs today's brief immediately, without waiting for the schedule |
| `/tune-brief` | Adjusts the watchlist, sections or exclusions after you have read a few |

## Without Claude Code

`setup-prompt.md` is a standalone prompt for Claude Desktop, Cowork or claude.ai. Paste it into a
chat and it runs the same interview with no plugin required.

## Where it runs

| | Claude Code | Claude Desktop / Cowork |
|---|---|---|
| Runs when your machine is off | No — needs a wake schedule and power | **Yes** |
| Can read local files | **Yes** | **No** |
| Can use your connectors | Only what you wire | **Yes** |
| Can email the brief itself | **Yes** | No — drafts, or you read it in Claude |

Start with Cowork unless the brief must write into a folder on your computer.

## What it will not do

- **Send anything.** It writes files and drafts. Sending stays with you.
- **Publish an unverified claim.** Anything it cannot check against a primary source is dropped,
  not hedged.
- **Pad a quiet day.** A thin section says so.

## Verification

Every item is checked against the source page, not a search result, before it is published. Items
are tagged `Verified` or `Unconfirmed`. Where sources disagree, the brief fetches a third and says
in the copy which figure it used and that others differ.

That discipline is the product. A brief you cannot trust in front of your board is worse than no
brief.
