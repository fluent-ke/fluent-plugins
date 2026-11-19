# Fluent Phone

Your agent works your own phone the way you would: reads the screen, taps, types and scrolls, in small checked steps, with a yes from you before anything goes out.

One skill:

- **driving-your-phone**: picks the route for your phone and computer, sets it up, and works through apps with the fixes we found the hard way: typing that silently goes nowhere, apps the search cannot open, feeds that scroll past items, likes that undo themselves, and voice-memo transcripts read straight off the phone.

| Phone | Computer | Uses |
|---|---|---|
| iPhone | Mac (macOS 15 or later) | [mirroir](https://github.com/jfarcand/mirroir-mcp) through Apple's iPhone Mirroring |
| Android | Windows, macOS or Linux | [mobile-mcp](https://github.com/mobile-next/mobile-mcp) over adb, by USB or Wi-Fi |

iPhone screen control needs a Mac. From Windows or Linux the skill says so and offers the app's web version instead.

M-PESA, bank, wallet and crypto apps stay closed, and the agent never types a PIN, password or one-time code. Every message, post, comment and delete waits for your yes; a batch of likes or follows you asked for gets one yes, with the count stated first.

## Install

```
/plugin marketplace add fluent-ke/fluent-plugins
/plugin install fluent-phone@fluent
```

On claude.ai, the desktop app and Cowork: **Customize → Plugins**. The phone tools run on your own computer, so this plugin needs an agent that runs there, such as Claude Code or Codex.

## Licence

[MIT](../../LICENSE).
