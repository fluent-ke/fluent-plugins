---
name: doing-big-tasks
description: Use for any task big enough that getting it wrong costs real time — a build, a migration, a research project, a launch, a report, a rewrite, anything multi-step or spanning several files or days. Also when work keeps stalling for approval, when an agent hands the thinking back, or when something was "finished" and turned out not to be.
license: MIT
metadata:
  author: fluent
  version: "0.2"
---

# Doing Big Tasks

## What this is for

Most work with an AI fails in one of two ways. It stops every few steps to ask what to do next, so the person ends up doing the thinking anyway. Or it runs ahead confidently on an assumption nobody checked, and the result has to be thrown away.

This skill is the method that avoids both: **do the thinking yourself, hand over one plan, then finish the job.**

Use it when the task is big enough that getting it wrong costs real time. For a quick answer, skip the plan — but never skip the thinking. Steps 1 and 2 run on everything.

## The shape

1. Know the task
2. Work it out yourself
3. Produce one plan
4. Get the plan critiqued cold
5. Execute it as a mandate
6. Verify with fresh eyes
7. Record what actually happened

---

## 1. Know the task

Understand what the task actually is before doing anything about it.

**Gather context from the person** — but ask one or two pointed questions only if it is genuinely unclear. A list of questions is the thinking handed back. Most of what you need is findable.

**Gather context from the surroundings.** Zoom out and in: the task, what it sits inside, what it touches, what depends on it. Then ask the question people skip:

**What already exists to do this?** Find it before building anything. If you are replacing something that works, say why. Most rebuilt things were rebuilt because nobody looked.

## 2. Work it out yourself

The goal is to get it *done*. Figure it out; do not hand it back. This is where the discipline lives.

**Name your assumptions and test them.** Three kinds: about the whole task, about each step, and about your own plan. Validate each against something real — the actual file, the actual data, a test, the source. Rebuild around the ones that fail. **Never carry an untested assumption as a fact.**

**Decide from evidence, not recall.** Assume you do not know. What you remember about a tool, a price, a limit or an API is a hypothesis — go and check. This matters most where you feel most confident: "it's just a small update" is the exact thought that precedes getting it wrong. A question about how some external thing behaves is a research task, not a memory lookup.

**Pick the best mechanism, not the first one.** For each step, define what it must *achieve*, then choose the best option out of all of them, weighed against the evidence. The first idea is a candidate, not an answer.

## 3. Produce one plan

Everything above resolves into a single plan. Not a decision served at a time, not a question every few minutes. One thing, written to be read and approved in one pass.

**The plan contains:**

- *(only if genuinely unclear)* the one or two questions you could not resolve yourself
- **The whole task as you understand it** — the big picture and the small, where it is going and why
- **What "done" looks like**, comprehensively, and what it achieves
- **The best way there, and the steps** — the mechanism chosen out of the options, broken into what will actually be executed
- **Ripples** — what else this affects, each stated as concrete follow-on work, not an observation
- **Compounding** — what becomes possible *because* this is done

**Ripples and compounding are work, not commentary.** State each as "because we did X, Y now has to change" and fold it into the execution list. A ripple you name but never action is a half-finished plan.

Write it to be scanned. Surface only the forks you genuinely cannot call — for everything else, make the call and say you made it.

### The bar — a plan is done when

1. It shows understanding of the **whole** task, big picture and small.
2. It defines **comprehensively** what done looks like.
3. It presents the **best** way there — assumptions surfaced and tested, alternatives weighed, plus the ripples and the compounding, both actioned.

Hit all three and the person can just say "go".

## 4. Get the plan critiqued cold

**Before the plan reaches the person, have it attacked.** What is weak, what is missing, what will not hold, which fork got dodged. Fold the critique in. What they see should already be stress-tested.

**The critic must have fresh context — not a copy of yours.** A reviewer that inherits your reasoning inherits your blind spots and will agree with you. See *Working in different environments* for how to get genuinely fresh eyes wherever you are running.

## 5. Execute it as a mandate

**Once approved, a plan is a mandate to complete.** Run it end to end. Do not stop to re-confirm each step — the person will interrupt if they need to. Serving decisions one at a time is the babysitting this whole method exists to end.

**But it is not a mandate to guess.** If a load-bearing fact is still unconfirmed and getting it wrong means doing the wrong work, that is a blocker. Stop and get it answered before executing that part. The mandate is to finish, not to barrel through an unknown.

**Re-plan on new input.** A new fact mid-stream can change everything or nothing. Re-run steps 1 and 2 against it — re-infer, re-check, re-think — rather than patching the plan's wording. If it materially changes things, update the plan and say what changed. If not, carry on. Do not ignore it, and do not restart from zero.

**Picking up someone else's plan?** If a plan already covers the work, do not re-plan from scratch. Say a plan exists and where it got to, then continue from there.

## 6. Verify with fresh eyes

**The one who did the work cannot check it.** They read their own intent into the result and see the thing they meant to build rather than the thing that is there.

So verification is a separate job, done against **the plan as the specification**, by someone or something with **fresh context**. It reads the actual end state — not the transcript of what was attempted — and answers: was every part done, and done the way it was meant to be? Then it reports the gaps.

Verification is always against the plan. Never against a memory of the plan.

## 7. Record what actually happened

Stamp the plan with a short note: what was done, that it was verified and how, and anything that changed along the way — a better mechanism found mid-execution, a judgement call, a step that shifted.

The plan is the record of intent. The stamp is the record of reality. Keeping both is what lets someone pick this up cold in three months.

---

## Working in different environments

The method never changes. Two things do: **where the plan lives**, and **how you reach fresh context**.

### Fresh context

Steps 4 and 6 need a reader who has not been in your head.

**A sub-agent and a new conversation are equivalent** — both start with only what you hand them. Use whichever your environment has.

**The failure is a fork.** A reviewer that inherits your conversation inherits the reasoning it was meant to check, and it will agree with you. If the only "fresh" reviewer available is a copy of your own context, say so and treat its verdict as weak.

### Where the plan lives

| Environment | The plan lives | Carried forward by |
|---|---|---|
| Files persist between sessions | A file that outlives the session | The file itself |
| Files are ephemeral, but the person keeps documents | Documents the person keeps and can re-attach | Those documents |
| Neither | This conversation only | The handoff, in full |

An ephemeral filesystem is not the same as no filesystem. If you can write files but they vanish with the session, write them anyway — then hand them over as documents rather than leaving them to be lost.

### The handoff

When work moves to a session that was not here — a new conversation, a colleague, tomorrow — what you hand over is **the orientation you already did, plus the plan**. Not a summary of them.

The point is that the next session does not start by working out what you already worked out. Re-orienting is the expensive part, and it is the part you have already paid for.

**A handoff is complete when the receiving session can start the work without asking a single question.** That is the test. Everything else is detail.

**It carries:**

- **What the task is**, and what done looks like
- **The orientation** — what you found out, where things are, what already exists
- **The assumptions you tested**, and what they turned out to be. Untested ones flagged as untested
- **The plan** — the steps, in order
- **The decisions already made, and why**, so they are not silently re-opened
- **What is still unresolved**, and who resolves it

Where the environment supports documents, most of that should *be* documents attached to the handoff, not prose retyped into a prompt. A prompt that says "see the plan document" plus the document beats a prompt that paraphrases it.

**Write it for someone who was not in the room.** "As we discussed" means nothing to a session that was not there. This is the failure mode of the whole pattern: a handoff that reads perfectly to its author and is unusable by its recipient. Before sending, read it as a stranger.

Compose it for the task in front of you. A three-step task needs a paragraph and a plan; a migration needs the orientation documents, the tested assumptions, and the constraint list. Do not pad the small one to look thorough, and do not compress the large one to look tidy.


## Common failures

| What happens | What it actually is |
|---|---|
| A list of questions comes back instead of a plan | The thinking handed back. Answer what you can find; ask only what you genuinely cannot resolve. |
| Each step pauses for approval | Serving decisions one at a time. Once the plan is approved, finish. |
| Confident work built on a wrong fact | An assumption carried as fact. Test the load-bearing ones before building on them. |
| "Done" that turns out not to be | Self-verification. The one who did the work cannot check it. |
| The critic agrees with everything | A forked reviewer, inheriting the author's reasoning. Give it fresh context. |
| The plan drifts from what was actually built | No stamp. Record what changed while executing. |
| A handoff the next session cannot use | Written for someone who was already in the room. Read it as a stranger before sending. |
| A handoff that paraphrases the plan | Attach the plan. A summary of the orientation makes the next session redo the orientation. |
| The next session starts by working out what you already knew | The handoff carried conclusions but not the orientation behind them. |
| A ripple named in the plan and never done | Ripples are work. Put them in the execution list. |

---

Stuck, or want to send feedback on this skill? Read the `about-fluent` skill.
