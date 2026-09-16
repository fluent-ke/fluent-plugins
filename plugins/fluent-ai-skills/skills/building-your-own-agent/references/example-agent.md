# A worked example

A consultant produces monthly cost reviews for about four clients. One had just been made in the conversation, and three corrections came out of it: biggest category first, one paragraph with no guessing at causes, and the deliverable is called a Cost Review.

Here is the whole agent that came out of that. Nothing was invented — every rule below is one of those corrections, and the example file is the document they had already approved.

```
cost-reviews/
├── AGENTS.md
├── CLAUDE.md
├── workflows/cost-review.md
├── examples/meridian-health-2026-07-cost-review.md
├── templates/cost-review-template.md
├── input/
└── output/
    ├── 2026/
    └── log.md
```

## AGENTS.md

```markdown
# Cost Reviews

## What this is for

You produce monthly Cost Reviews — a client's messy expense spreadsheet turned into a
short summary of what they spent, by category. About four clients a month. Each
spreadsheet is a fresh input; the shape of the output never changes.

## Trigger

When a spreadsheet lands in `input/`, or the person says "run it", produce the Cost
Review. Do not ask questions first. Ask only if the input is missing, unreadable, or
has no clear category breakdown.

## How to do it

Follow `workflows/cost-review.md`.
Match `examples/meridian-health-2026-07-cost-review.md` — that is a real approved one.
The empty shape is `templates/cost-review-template.md`.

## Rules

- Call it a Cost Review. Not a Spend Analysis, not an Expense Summary.
- Biggest category first, always — in the table and in how you talk about the numbers.
- One paragraph of commentary. Say what the numbers show. Never state or imply a cause:
  no "likely due to", no "this suggests", no explaining why a number is what it is.
- The shape is locked: summary line, table by category, one paragraph. Nothing else,
  unless a client asks — and then it is a new file in `workflows/`, not a quiet edit here.

## Where it lands

`output/{yyyy}/{client-slug}-{yyyy-mm}-cost-review.md` — for example
`output/2026/meridian-health-2026-07-cost-review.md`.
Then one line in `output/log.md`, same four fields every time: date run, client, input file, output file.
If that file already exists, stop and ask before overwriting.

## What you need

No account access. The person puts the spreadsheet in `input/` by hand each time. If a
client ever sends data another way, ask before assuming access to it.

## This can grow

When a client wants a different shape, add a file to `workflows/` for that variant
rather than changing this one underneath everyone else.
```

## CLAUDE.md

```
@AGENTS.md

Read AGENTS.md in this folder and follow it before anything else.
```

## What to notice

**The rules are corrections, not preferences.** Each one exists because someone said "no" once. That is why they are specific enough to follow and short enough to read.

**The example is the approved artefact**, saved as it was. The template was made by stripping that file down to placeholders — not written from imagination.

**The client's name and figures appear in exactly two places**: the example, and one log line. `AGENTS.md`, the workflow and the template have none, so the next three clients need no edits.

**The trigger is one sentence** and it is why the person never explains the job again.

**Nothing here mentions a model, a tool or a platform.** Point Claude Code, Cowork or the ChatGPT desktop app at this folder and it works the same.

## The same agent in a browser

She has no folder, so it goes into a project's instructions. Three things change — everything else is the same words:

| In the folder | In the project |
|---|---|
| "When a spreadsheet lands in `input/`, or the person says run it" | "When I paste a client's expenses, or say run it" |
| "Save as `output/2026/{client-slug}-{yyyy-mm}-cost-review.md`" | "Reply with the finished Cost Review — I'll save it" |
| "Append one line to `output/log.md`" | Dropped. There is nothing to append to |

The rules, the trigger's do-not-ask clause and the growing line carry over untouched. The procedure goes inline in the instructions rather than in `workflows/`, because there is no file to point at.

The example and the template still matter — produce them as two documents she can save and upload to the project, and name them in the instructions so the model reaches for the right one. Do not tell her to upload files that do not exist yet.
