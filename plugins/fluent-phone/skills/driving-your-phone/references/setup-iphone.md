# Setup: iPhone from a Mac (mirroir)

[mirroir](https://github.com/jfarcand/mirroir-mcp) drives the iPhone through Apple's iPhone Mirroring window. It runs on macOS only, because iPhone Mirroring exists only there.

## What the devices need

From [Apple's iPhone Mirroring requirements](https://support.apple.com/en-us/120421):

- A Mac with Apple silicon or a T2 chip, on macOS 15 Sequoia or later.
- An iPhone on iOS 18 or later, with a passcode, **locked** and near the Mac.
- Both signed in to the same Apple Account, with two-factor authentication on.
- Bluetooth and Wi-Fi on for both. The Mac is not sharing its internet connection, using AirPlay or using Sidecar.
- Not available in the European Union.

Open iPhone Mirroring once by hand and confirm the phone's screen appears before going further.

## Install and register

```
npx -y mirroir-mcp install
```

or with Homebrew: `brew tap jfarcand/tap && brew install mirroir-mcp`. Then register it with your agent:

- Claude Code: `claude mcp add --transport stdio mirroir -- npx -y mirroir-mcp`
- Codex: `codex mcp add mirroir -- npx -y mirroir-mcp`

Run `npx -y mirroir-mcp doctor`; each line that fails names its fix. The person grants Screen Recording and Accessibility to the app that runs the server, in System Settings → Privacy & Security. Tell them which pane and which app; they click it.

## Permissions

With no config, mirroir exposes only read-only tools. Actions are switched on in `~/.mirroir-mcp/permissions.json`. A starting point for someone who wants the agent to read, tap, type and scroll, with money apps closed:

```json
{
  "allow": ["tap", "type_text", "press_key", "launch_app", "press_home", "press_back", "swipe", "scroll_to", "save_note"],
  "deny": [],
  "blockedApps": ["Wallet", "Settings", "M-PESA", "MySafaricom", "Airtel Money"]
}
```

Add every bank and crypto app on the phone to `blockedApps`, by the name under its icon. mirroir then refuses to launch them or tap their named icon on the Home Screen or in Spotlight. Icons with no name under them are not checked (the Dock, folders, the App Library, the App Switcher), so the consent rules in SKILL.md stay the real guard. The full schema, including per-app allow lists, is in mirroir's [permissions doc](https://github.com/jfarcand/mirroir-mcp/blob/main/docs/permissions.md). Allow `long_press`, `drag`, `double_tap` or `run_steps` only when a task needs them.

## Running

- The Mac stays awake and unlocked; the iPhone stays locked. Picking the phone up and unlocking it ends the mirroring session.
- An error that names something the person must do (unlock the Mac, approve a prompt, lock the iPhone) means stop, tell them, and retry once after they say it is done.
- `npx -y mirroir-mcp skill` prints mirroir's own manual for the full tool list.
