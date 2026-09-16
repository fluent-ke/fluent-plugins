# The setup prompt

For **Claude Desktop, Cowork, or claude.ai** — anywhere the plugin cannot be installed. Paste the
block below into a new chat. It does the same interview the plugin does.

Works on its own: it carries its own instructions and needs no plugin, no skill and no files.

---

```
I want you to set up a daily brief for me — a short, researched summary of what happened in my
industry, waiting for me each morning before I start work.

Before you build anything, interview me about my work.

Rules for the interview:
- Ask me ONE question at a time and wait for my answer. Do not show me a list.
- Do not fill in any answer for me. You do not know my industry, my competitors, my regulator or
  my sources until I tell you. If you think you know from my company name, ask anyway.
- If I am vague, ask a follow-up rather than guessing.

Cover these, in roughly this order:
1. What I actually do day to day, and what I am accountable for.
2. What I need to know before I walk into a meeting.
3. The companies, regulators, people and products I watch — ask "who else?" twice after my first
   answer, because the third batch of names is usually the important one.
4. Who regulates me, if anyone, and whether their decisions change my plans.
5. What is definitely NOT useful to me. Push for specifics: a size, a geography, a topic.
6. Which markets and currencies matter.
7. Anything commercially sensitive that must never appear, and any policy my organisation has
   about what can go into an AI tool.
8. The sources I already trust, and any I distrust.
9. How long the brief should be, and whether I want interpretation or only what happened.
10. What time, which timezone, and which days — ask, do not assume Monday to Friday.
11. Where it should arrive, and if by email, ask me for the address.

When you have enough, say back to me in five or six lines: my beat, my watchlist, my sections in
order, what is excluded, and when it arrives. Let me correct it before you build.

Then produce, as a single document I can save:

A) MY BRIEF CONTRACT — the instructions for generating the brief each day. It must include:
   - Read the ledger of what has already been sent, and never resend a story that is in it.
   - My watchlist, by name, to be searched explicitly.
   - My sections, in the order I chose, with the one I said I would keep placed first.
   - VERIFICATION, which is not optional: fetch the primary source page for every item and read
     it before publishing. A search snippet is a lead, never a citation. Check the claim, date,
     figure and name against the page fetched. Tag each item Verified or Unconfirmed. Drop
     anything that fails rather than hedging it. When two sources disagree, fetch a third and say
     in the copy which figure is used and that others differ.
   - Fewer real items beats padding. A thin section says so in one line.
   - Absolute dates, never "yesterday".
   - Lead with what happened, then what it means for me specifically.
   - My exclusions and my confidentiality constraints.

B) A SCHEDULED TASK I can create in Cowork, with the exact prompt to paste in, the frequency in
   my timezone, and a note to trial it on demand for a week before scheduling it.

C) A SHORT NOTE on how to tune it after a week: what to change if it tells me things I already
   know, if there is not enough in it, or if I only read one section.

Do not start researching or write a sample brief until I have confirmed the contract.
```

---

## Using it

1. Paste into a new chat and answer the questions.
2. Save the contract it produces — that is the file that matters. Everything else is plumbing.
3. Create the scheduled task in Cowork and **trial it on demand for a week**, reading every output
   and tuning before switching to the schedule.

## Handing it to someone

This block is safe to send by email or paste into a message. It has no dependencies and names no
client. The person who receives it gets the same interview whoever they are.
