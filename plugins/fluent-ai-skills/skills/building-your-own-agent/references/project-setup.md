# Setting up the agent as a Project

For the *As a Claude Project* branch of the main skill. The person is non-technical and this is the one unfamiliar step in the whole build, so walk them through it on their own screen, one step at a time, and wait for "done" before the next. Menu labels drift between versions: name what to look for ("the Instructions box on the Project page"), and ask what they see when it does not match.

## The instructions block

Hand it over as one fenced block they can copy in one go. Fill every heading from the specimen and their corrections; drop a heading only if the job truly has nothing for it.

```
JOB
You are the Weekly Cost Review helper for [business]. You turn [input] into [output], about [how often].

TRIGGER
When I paste or attach [the material], or say "run it", do the job straight away. Do not ask questions first. Ask only if the material is missing or unreadable.
[For anything that sends, pays or publishes, add: Stop at the draft. Show it to me. Never send, pay or publish.]

STEPS
1. ...
2. ...

OUTPUT
[Their parts, in their order, under their names.] Reply with the finished thing; I will save it.
After it, add a short list headed "Please check" with anything you assumed or were unsure about.

RULES
- [each correction they made, one line each]
- Use only what I give you and the files in this Project. If something is missing, say what, rather than guess.

FILES
- "good-example": a finished one I approved. Match its shape and tone.
- "price-list": [what it is]. Use it for [what].
[If none yet: No example yet. The first answer I accept gets saved here as good-example.]

When the job changes or a new variant appears, tell me, and write the new instructions in full for me to paste.
```

The "Please check" line is there because the person, not the agent, owns what goes out: it makes every run end with the parts they should verify.

## Setup steps

### claude.ai, and the Claude desktop app's chat

1. Open **Projects** in the left sidebar. On a phone browser, open the menu first.
2. Click **New project**. Name it after the job. The description is optional.
3. On the Project page, find **Instructions** and open it (it may read *Set project instructions*, or show a pencil). Paste the whole block. Save.
4. Under **Files**, add each file the instructions name: the plus button, then upload from the device, or add it as text and paste. Give each file the exact name the instructions use.
5. Start a chat from the message box on the Project page. Chats started from the main page are outside the Project and know none of it.

### Claude phone app

Projects show in the app, but creating one or editing instructions can be missing depending on the version. If a step is not there, open claude.ai in the phone's browser for the setup, then use the Project from the app.

### ChatGPT

Projects in the sidebar, **New project**, name it, then the project's settings for **Instructions**, and add the files to the project. Start the chat inside the project.

## Smoke test

In a new chat inside the Project, send: *What job are you set up for?* It should answer with the job, the trigger and the files by name. If it answers generally, the instructions did not save, or the chat was started outside the Project.

## First run

1. In a new chat inside the Project, they paste or attach one real input (with private details covered, if it is a shared or free account) and send it with nothing else. The trigger means no question should come back.
2. Then they send the check, in the same chat:

   ```
   Let me check your answer. Tell me:
   1. Which parts came from my input or the Project files, and which did you assume?
   2. What is the most likely mistake in your answer, and how can I check it quickly?
   3. Which numbers, names or dates should I check against the original?
   Then show me the corrected version if you find a problem.
   ```

3. They check one figure or fact themselves, by hand or against the original. That check is the habit to leave them with.

## The fix loop

Every fix goes into the instructions, or the agent repeats the mistake in the next chat. In the Project chat, or back with you:

```
Here is what was wrong or missing: [their words].
Rewrite the Project instructions so you get this right every time. Show me the lines you changed, then the full new instructions in one block I can copy. I will paste them into the Project myself.
```

They open the Project's Instructions, replace the old block with the new one, save, and test again in a new chat. When an answer comes out right, they save it as a file called `good-example` in the Project, replacing any older one.

## Done when

The Project exists under the job's name, the smoke test names the job, one real input has produced an answer they checked, and they know the fix loop: new block, paste over, new chat.
