---
name: driving-your-phone
description: Use when a task needs the person's own phone, iPhone or Android — reading or replying to a DM, watching a reel or video someone sent, reading a voice memo's transcript, liking, following or posting from an app, or anything only the phone app can do — and when phone control misbehaves, such as typing that reports success but shows nothing, an app search that never opens the app, a feed that scrolls past items, or a tap on a toggle that undoes it.
license: MIT
metadata:
  author: fluent
  version: "0.1"
---

# Driving Your Phone

An agent can work the person's real phone: read the screen, tap, type and swipe, with their accounts and their money on it. Every action is real and most are visible to other people, so the work is small checked steps and a clear line on what needs a yes.

## 1. Pick the route

| Phone | Computer | Route |
|---|---|---|
| iPhone | Mac | **mirroir** MCP through Apple's iPhone Mirroring. Setup: [references/setup-iphone.md](references/setup-iphone.md) |
| Android | Windows, macOS or Linux | **mobile-mcp** over adb, by USB or Wi-Fi. Setup: [references/setup-android.md](references/setup-android.md) |
| iPhone | Windows or Linux | No route this skill supports: iPhone screen control needs a Mac. Say so, then offer the app's web version (WhatsApp Web, instagram.com) or talk the person through doing it on the phone |

Skip setup when the tools are already connected. The route is ready when one read of the screen comes back with the text that is actually on the phone.

## 2. Work in checked steps

1. **Look**: read the screen as text with tap points before acting. Take coordinates from that reading, never from your estimate of a screenshot.
2. **Expect**: name the change the action should cause.
3. **Act once**, then read again. The tool's "success" only means the input was sent; the screen says whether it worked. If nothing changed, read again and choose differently instead of repeating the action.
4. **Narrate**: one line to the person before each move on their phone, one line on what the screen showed after. Never run a long series in silence.
5. **Learn**: before working in an app, read the notes saved for it; when something will hold next time (where a control hides, a route that works), save one line. On mirroir that is `get_notes` / `save_note`; on mobile-mcp keep them in `phone-notes.md` in the working folder, one heading per app.

The work is done when the screen shows the result the person asked for, read back from the phone itself.

## 3. Consent

Reading is free. Anything that leaves the phone or changes it waits for a yes:

- **Send, post, comment, delete, buy, change a setting**: show the exact text and who it goes to, then wait for a yes, every time.
- **Likes and follows in bulk**: one yes can cover a batch the person asked for ("like all his posts"). State the count first, since each one notifies the other person.
- **Install, uninstall, clear an app's data, open a link**: only when the person asked for that exact action.

Money apps stay closed: M-PESA, MySafaricom, Airtel Money, bank apps, Wallet or Google Wallet, crypto exchanges. On iPhone, block them in mirroir's config ([setup](references/setup-iphone.md)); on Android nothing blocks them, so stay out of them. When the phone shows a PIN pad, an M-PESA prompt, a password sheet or a one-time code, stop and hand the phone to the person: PINs, passwords and codes are theirs to type.

## 4. Field-tested fixes

These cost real sessions to find. Check the screen before trusting one; apps change.

- **Typing says it worked but nothing appears** (mirroir): the iPhone Mirroring window is behind another window. Bring it forward with `osascript -e 'tell application "iPhone Mirroring" to activate'`, tap the field, then type. The "Spotlight takes typing only once" error is the same fault.
- **The app search never opens the app** (iPhone): the app is not on the first Home Screen page. Swipe left past the last page to the App Library, tap the category group that holds it, then tap the app. mirroir's app block does not cover the App Library, so take this route only to apps the person may use. On Android, `mobile_list_apps` gives the package name for `mobile_launch_app`.
- **A feed scrolls further than the swipe**: drags carry inertia, so a 200-point drag can move a feed 400 to 600 points. When working item by item (liking each post, reading each message), match each item to the one before by its date or caption. When the chain breaks, scroll back to the last item you handled and come forward again.
- **A toggle can undo itself**: before tapping a like, follow or save, check its state in a cropped screenshot, since a red heart or a filled icon means it is already on. Confirm the tap by the count changing by one.
- **Copying on the phone does not reach the computer**: Universal Clipboard can silently fail. Read the text on screen instead, or send the file to the computer and work on it there.
- **Two accounts with almost the same name**: compare the handle letter by letter, the post count and the "Followed by" line before acting, and ask when two still look plausible.
- **Rate limits**: bulk likes, follows or messages can trigger an action block. Work at a steady pace and stop at the first warning.

App-by-app routes (Voice Memos transcripts, Instagram DMs and reels, Notes): [references/apps.md](references/apps.md).
