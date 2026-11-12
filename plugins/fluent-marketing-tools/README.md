# Fluent Marketing Tools

Operating procedures for the tools behind marketing production, written from real campaigns: the failure modes, the undocumented routes and the checks that settle whether something actually worked.

Three skills:

- **designing-in-pencil**: create and edit Pencil (`.pen`) slide decks, posters and social creative through the Pencil MCP or the `pen` CLI, with a guard that makes a wrong-document write impossible, a scaffolder for new files (optionally seeded from your brand file), and the gotchas that cost real time.
- **making-ai-video-ads**: make a 30-second presenter ad with AI video (worked route: Higgsfield and Seedance 2.5): real lines, a consistent avatar, the free and refused generation routes, a review checklist, and two scripts that time the captions from the audio and build the finished ad in 16:9, 9:16 and 4:5 with an end card and licensed music, always with a no-music version beside it.
- **setting-up-meta-ads**: build Facebook and Instagram campaigns, ad sets and dynamic-creative ads through the Meta Ads MCP: everything paused, the settings that cannot be changed after creation, image upload routes, conversion tracking, UTM parameters, and what to hand back to the account owner.

Each needs the tool's own MCP server connected in your agent; the video skill's scripts also need Python 3, Pillow, ffmpeg and Whisper. None of them activates an ad or publishes anything: that stays with you.

## Install

```
/plugin marketplace add fluent-ke/fluent-plugins
/plugin install fluent-marketing-tools@fluent
```

On claude.ai, the desktop app and Cowork: **Customize → Plugins**.

Ad copy reads best with `reviewing-ai-writing` from Fluent AI Skills installed alongside.

## Licence

[MIT](../../LICENSE).
