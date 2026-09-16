# Route: Claude Desktop / Cowork (cloud schedule)

Pick this when the person will not keep a machine awake, or when the brief needs their connectors
— work email, calendar, drive. This is the right default for most executives.

## What you gain and lose

**Gain:** it runs whether or not their laptop is open, and it can reach connected accounts.

**Lose:** it **cannot read any folder on their computer.** A cloud task has no access to a local
second brain, vault or repo. Everything it needs must be uploaded into the project, connected as a
connector, or reachable on the public web.

That single line decides the route. Confirm which side of it the brief sits on before building.

## Setup

**1. A project.** Create it in Cowork from scratch, saved to the Claude account — not opened from a
local folder, or the schedule cannot use it.

**2. Project instructions.** State the role, the sources, the output format, and the prohibitions.
Keep the prohibitions explicit and absolute: draft only, never send, never delete, and name any
data class that must stay out.

**3. Context files.** Upload only what the brief needs: their profile, their format template, their
watchlist of named entities. Re-upload when they change — the project holds a copy, not a live link.

**4. Connectors.** Connect in Customize, then Connectors. In a regulated business, confirm their
policy permits connecting work accounts **before** doing it, and record who approved it.

**5. The scheduled task.** Scheduled, then New task, then Set up manually. Set the name, the prompt,
the frequency, and the approval mode. Select the project where offered.

**Set approval to "Ask before actions"** for anything that could send or modify. A brief should be
drafting only, but the setting is cheap insurance.

**6. Trial on demand first.** Run it manually for a week before switching to the schedule. Read
every output. Tune the prompt while it is cheap to do so.

## Delivery to an inbox

A cloud routine cannot run an SMTP script. Options, in order of preference:

1. **The person reads it in Claude.** Simplest. The scheduled task's output is waiting for them.
   For many people this is genuinely enough and needs no mail plumbing at all.
2. **A mail connector drafts it.** The routine writes a draft to their own mailbox, which they send
   or simply read. Keeps the send action with a human.
3. **A local companion job mails it.** Only if a machine is available — at which point ask whether
   the whole thing belongs on the Claude Code route instead.

Do not promise SMTP-style delivery from a cloud routine. It is the most common false expectation in
this setup.

## Timezone

Confirm the person's timezone explicitly and state the conversion back to them. Gulf Standard Time
is UTC+4, East Africa Time UTC+3, and a Sunday-to-Thursday working week is normal in the Gulf — so
"weekdays" must be defined, not assumed.

## Naming

If the person's kit already contains an operations brief built from their calendar and inbox, this
one needs a distinct name. Two routines both called "Morning brief" will be confused by the person,
by you, and by any agent reading their setup later.
