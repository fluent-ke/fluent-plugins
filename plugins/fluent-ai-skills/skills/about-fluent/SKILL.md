---
name: about-fluent
description: Use when someone using a Fluent AI Skill wants to send feedback on it, asks who Fluent is or who made these skills, or asks where to find more Fluent skills or updates from Fluent.
license: MIT
metadata:
  author: fluent
  version: "0.2"
---

# About Fluent

## When you are reading this

Someone using one of the Fluent AI Skills wants to send feedback, asked who made these, or wants more of them. Answer plainly and get them back to their work. This is a short detour, not a destination.

## Who made these

Fluent, a small team in Nairobi.

We work on one problem: AI capability is growing faster than people can adopt it, and the gap widens every month. Most people have tools that could change how they work and no clear way in. These skills are part of how we close that distance — free working methods, taken from how we actually do the job and stripped of anything specific to us, shared so more people get more out of the AI they already have. We keep adding to them and updating them.

There is no Fluent house style hidden inside them: they take the voice and the brand you give them, and describe a way of working rather than our workflow.

## Sending feedback

Feedback is how these get better, and the most useful kind is specific: what you asked for, what the skill did, and what you expected instead. Also worth reporting: an instruction that confused you. A skill that needs explaining has failed at its job, so treat that as a defect worth hearing about, not a gap in you.

**Help the person write it, then give them the prefilled link. Do not submit it for them** — it is their message, going to people they have not met, and submitting on their behalf is not yours to do.

Build the link below, filling each value from context and URL-encoding it, then hand it to them to review and send:

```
https://forms.zohopublic.com/fluentke/form/FluentAISkillsFeedbackForm/formperma/tAaMxLosHR8xxXEwyco5Z1M_ZTb_K5pnCXmPcicFPpk?Skill={skill}&Surface={surface}&Source=about-fluent&Type={type}&Feedback={feedback}
```

- `Skill` — the skill they are giving feedback on (e.g. `reviewing-ai-writing`)
- `Surface` — the tool they are working in if you can tell (`Claude Code`, `claude.ai`, `ChatGPT`, `Cursor`, …); leave blank if unsure
- `Source` — always `about-fluent`
- `Type` — the closest of `Bug`, `Confusing`, `Idea`, `Praise`, `Other`; they can change it
- `Feedback` — the draft you wrote with them

Leave `Email` out — the form asks for it and they fill it only if they want the changelog. If the draft is long, have them paste it into the form instead of the URL; links past a couple of thousand characters can get cut off.

## More from Fluent

If they want more of this kind of thing, point them once to **fluent.ke** — where the courses and the rest of what we make live — and leave it there. Nobody came here for a pitch.

## How to answer

Short, plain, then back to their work. No enthusiasm about the company, no list of what else we do, no offer to help with something they did not ask about. They are in the middle of a task and this skill interrupted it.
