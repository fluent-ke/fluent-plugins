# Setting up the tools

Guide the person through these on their own computer, one step at a time, and confirm each worked before the next. App labels change between versions: describe what to look for, and if a screen differs from this, follow what's in front of them.

Do them in this order: **Google Drive first, then Obsidian, then the AI.** Each later step records the folder's location, so moving the folder afterwards means redoing them.

---

## 1. Sync the folder with Google Drive for desktop

Why: the workspace lives on their computer, where the AI and Obsidian can open it, and Drive keeps a copy in the cloud and on their other computers. A lost laptop costs nothing.

1. Install **Google Drive for desktop** from Google's download page and sign in with the account they want the workspace in.
2. In its settings, set **My Drive** to **Mirror files**, not **Stream files**. Mirror keeps a real copy of every file on the computer. With Stream, files are only fetched when opened, and AI tools and Obsidian can find a folder half-empty. If disk space is too tight for Mirror, keep Stream and mark the workspace folder **available offline**.
3. Move the workspace folder into My Drive, for example `My Drive/Workspaces/<Business Name>`. Where it ends up:
   - **Mac:** `~/Library/CloudStorage/GoogleDrive-<their email>/My Drive/` (also shown in Finder's sidebar under Google Drive)
   - **Windows:** with Stream, a drive letter (usually `G:`) that holds `My Drive`; with Mirror, the folder chosen during setup (it shows the location in Drive's settings). Open File Explorer and look for Google Drive in the left sidebar
4. Check: open drive.google.com in a browser and confirm the folder and a few files are there.

Notes:
- Don't put the same workspace in two sync services (Drive and Dropbox, Drive and OneDrive). They fight and make conflict copies.
- If they already use another sync service they trust, that works too; the point is one folder, synced automatically.
- Several people editing the same workspace at the same time can create conflict copies. For a team, agree who works where, or give each person their own workspace.

## 2. Install Obsidian and open the vault

Why: Obsidian is a free reader and editor for the workspace's Markdown files, with links between notes and a search across everything. The files stay theirs; the AI reads the same files directly.

1. Download Obsidian from obsidian.md (Mac, Windows, Linux, iPhone, Android) and install it.
2. On the first screen choose **Open folder as vault** (not "Create new vault") and pick the workspace folder inside Google Drive.
3. If Obsidian asks whether to trust the folder, allow it.
4. Show them three things, nothing more: the file tree on the left, search, and that typing `[[` links to another note.
5. For a second workspace, use the vault switcher (bottom left, or **Open another vault**) and open the other folder. Each vault is separate.

Notes:
- **Obsidian Sync is not needed**: Google Drive already syncs the folder. Using both on one folder causes conflicts.
- On a phone, Google Drive and Obsidian don't share folders easily. Treat the phone as optional; the computer is the main surface.
- Obsidian's community plugins are optional. Start without them.

## 3. Point their AI at the folder

The aim is the same everywhere: the AI reads the workspace's instructions at the start, and works and saves inside the folder. Pick the route that matches what they use. Where they have a choice, a desktop app or Claude Code with the folder attached beats a browser project, because the AI can read and write the files itself.

### Claude app with Cowork

Cowork lives inside the Claude desktop app. Point a Cowork task at the workspace folder; it reads the `CLAUDE.md` in that folder and the folders above it. If the app offers a folder-instructions field, leave it short ("Follow CLAUDE.md in this folder"); the file is what travels with the folder.

### Claude Code

Open it in the workspace folder (`cd` into the folder, then `claude`, or pick the folder in the desktop app's Code tab). It reads `CLAUDE.md` there and in the project or area folder it's working in.

### Claude Preferences

In Claude's settings, under the profile's personal preferences, add a short line so every chat knows the workspace exists:

> My work lives in one folder, "<Workspace Name>", organised with PARA (1. Projects, 2. Areas, 3. Resources, 4. Archive). When a chat can reach that folder, read CLAUDE.md first, keep files in the right project or area, and track real work with the tracking-work skill.

Preferences apply to every chat, so keep anything business-specific out of them; that belongs in `CLAUDE.md`.

### The tracking-work skill in Claude

Zip the `tracking-work` folder (the folder itself, with `SKILL.md` inside; a zip of the bare file is rejected) and upload it where Claude's settings manage skills, then switch it on. From then on it works in every chat and every Cowork task. Check by starting a chat in the workspace and saying "let's start a task": it should create a `task.md`.

### Claude Projects (browser, no folder access)

A Project can't see the folder, so it gets a copy:

1. Create a Project named after the workspace.
2. Paste the root `CLAUDE.md` into the Project's instructions.
3. Upload the project and area home notes and any key resources to the Project's files.
4. Tell the person the trade-off plainly: the Project only knows what was uploaded, and replies they want to keep must be saved into the folder by hand. Update the uploads when the files change.

### ChatGPT

- **ChatGPT desktop with a folder attached:** attach the workspace folder; it reads `AGENTS.md` from it at the start. Confirm on their version by asking "what does AGENTS.md in this folder say?".
- **Custom instructions** (settings, personalisation): add the same short line as the Claude Preferences above, with `AGENTS.md` in place of `CLAUDE.md`.
- **A ChatGPT project:** like a Claude Project. Paste `AGENTS.md` and the tracking rules into the project's instructions and upload the key files.
- **Tracking:** where ChatGPT can't load skills, the tracking rules and template go into the root `AGENTS.md`, and this goes into custom instructions:
  > For any real piece of work, keep one file `<Task Name> - task.md` in the project or area's `tasks/<task-name>/` folder: live state at the top (Objective, Intent, Decisions, Next Steps), a dated session log at the bottom, newest first. Read it before starting, update it as we go, and write a Resume line when we stop. The full rules are in AGENTS.md.
- **Limits to say out loud:** a ChatGPT project, like a Claude Project, can't save into the folder, so anything worth keeping is saved by hand. Whether the desktop app can write back to an attached folder depends on the version; test it by asking it to create a small note.

### Codex, Cursor, Copilot and other agents

Most read `AGENTS.md` from the folder they're opened in. Open the workspace folder and check it answered from the file.

### Check it worked

Whatever the route, open a fresh chat in the workspace and ask: *"What is this workspace, and what's in progress?"* A right answer, with no help, means the setup works. A vague one means the instructions aren't loading: fix that before finishing.
