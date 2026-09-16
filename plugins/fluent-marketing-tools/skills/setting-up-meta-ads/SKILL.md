---
name: setting-up-meta-ads
description: Use when building or editing Meta (Facebook/Instagram) ads through the Ads MCP — a campaign, ad set, dynamic-creative ad, conversion tracking, or UTM parameters — or when a create call is rejected over an optimization goal, promoted object, call-to-action, or budget-type change, a create returns a retryable INTERNAL error, an image cannot be uploaded because local-file upload is unavailable, a publish is blocked by error #1870194 over location targeting, a warning says the account is near its spending limit, or a dynamic-creative ad won't delete.
license: MIT
metadata:
  author: fluent
  version: "0.1"
---

# Setting Up Meta Ads

## Overview

The Ads MCP builds real campaigns on live money. Build everything **paused**, preview it,
and hand the client the activation — never call `ads_activate_entity` yourself. The order is
campaign → ad set → ad, and the traps are mostly things that **cannot be undone after
creation**, so getting them right the first time is the whole game.

**Ad copy is the brand's voice.** Write headlines, primary text and descriptions from the brand's own
voice guide, and when the `reviewing-ai-writing` skill is installed, run it over them before they go
into a creative.

## Set-at-creation, immutable forever

These cannot be edited later. A wrong one means delete-and-rebuild, so decide before you call.

| Field | Lives on | If wrong |
|---|---|---|
| **Budget type** (daily vs lifetime) | campaign | `Budget type change not allowed`. Pick **lifetime** when the client wants an exact total across the flight — daily × days overspends. |
| **Objective** | campaign | Gates which optimization goals are legal. Read `valid_optimization_goals` from the create response; don't guess. |
| **Dynamic creative** | ad set | A DCO ad set holds **exactly one ad**, and that ad **cannot be deleted or edited**. |

Because the campaign holds the immutable budget, **keep it and rebuild below it.** To change
a dynamic-creative ad you delete its **ad set** (Meta refuses to delete the ad directly:
`Dynamic Creative Ad deletion is not allowed`), then recreate ad set + ad. The campaign, and
its budget, survive untouched.

**The rebuild, in order — there is no delete tool on this MCP.** Deleting is
`ads_update_entity` with `{"status": "DELETED"}` on the ad set. **Create the replacement ad set
and ad first, then delete the old one.** Reversing it leaves a campaign with nothing under it if
a create then fails, and the old ad set is a working fallback until the new one exists. Say
which ad set the client should activate, because the deleted one still shows in Ads Manager.

**A create can fail with `INTERNAL` / `is_retryable: true`.** Before retrying, list the
children of the target parent — a retry landing on top of a partial success puts **two ads in a
DCO ad set**, which the format forbids and which you then have to unpick. Read first, retry second.

## Building the dynamic-creative ad (the undocumented part)

`ads_create_creative` only makes single-image / single-video / catalog creatives, and the
tool docs imply that's all there is. **It isn't.** `ads_create_ad` accepts an inline
`asset_feed_spec`, and that is the only way to build a 5×5×5×3 dynamic creative through the
MCP. Do not conclude it needs Ads Manager — that conclusion is wrong.

Passing an `asset_feed_spec` **auto-flags the ad set as dynamic creative** — you never set
`is_dynamic_creative` yourself, and the one-ad / no-delete rules above kick in from that moment.

```json
{
  "object_story_spec": { "page_id": "<PAGE_ID>" },
  "self_ai_disclosure": "OPT_IN",
  "url_tags": "utm_source={{site_source_name}}&utm_medium=paid_social&utm_campaign=<slug>&utm_content={{ad.name}}&utm_term={{placement}}",
  "asset_feed_spec": {
    "ad_formats": ["SINGLE_IMAGE"],
    "images": [{ "hash": "..." }],
    "bodies": [{ "text": "primary text" }],
    "titles": [{ "text": "headline" }],
    "descriptions": [{ "text": "description" }],
    "call_to_action_types": ["SIGN_UP", "LEARN_MORE", "SEE_DETAILS"],
    "link_urls": [{ "website_url": "https://www.example.com" }]
  }
}
```

- `self_ai_disclosure: "OPT_IN"` whenever the imagery was AI-generated (e.g. from Pencil). It's
  the honest declaration and Meta may show an "AI info" label — so match it across campaigns
  you intend to compare, or one carries the label and the other doesn't.

## Getting images in: they need a public URL

`ads_creative_upload_media` takes a **public URL** or a local file, and **local-file upload is
disabled on some ad accounts** — it fails with *"Local file upload is not available for ad
account …"*. A file that exists only on someone's own computer or in a synced folder is not
reachable. Establish this **before** promising an ad, because it is the step most likely to stall.

Routes, in the order worth offering:

1. **The client uploads in Ads Manager**, then read the hashes back with `ads_get_ad_images`.
   Reaching the media library means starting an ad they do not want — that draft is never
   published, so the API never sees it and your ad set stays empty and clean. Tell them to
   discard it.
2. **A throwaway public repo or bucket**, if the client agrees to the file being public briefly.
   Meta fetches once at upload.
3. **Reuse a published post's CDN URL** — a poster or video already on the Page has a public
   `fbcdn` URL that `ads_creative_upload_*` fetches directly. Only works if the published asset
   is still accurate; a repriced or re-dated poster is not.

**Check which file actually arrived.** A hand-upload puts the client's choice in, not yours:
verify the names in `ads_get_ad_images` against the ones you asked for. A poster variant
carrying an organic CTA ("Link in caption", "Comment X to join") contradicts the ad unit's own
button and reads as a recycled organic post — the **clean** variant is the one a paid ad wants.

## The conversion does not have to fire on the ad's destination

A third-party destination the pixel cannot reach — a hosted form, a checkout on someone else's
domain — does **not** force you down to a Traffic objective. What matters is where the
**conversion** fires, not where the click lands. If the flow ends on a page the client owns and
the pixel is on (a post-payment or thank-you page), a Sales objective optimising on that event
is legitimate.

Check it rather than assuming, before choosing the objective:

- `ads_get_datasets`, then `ads_get_dataset_stats` with `aggregation: "host"` — this is the
  question "which domains has this pixel ever heard from?", and it answers in one call.
- `ads_get_customconversions` — a custom conversion's `pixel_rule` names the exact URL substring
  it fires on, and `last_fired_time` says whether it is real.
- Then `{"custom_conversion_id": "<id>"}` as the ad set's `promoted_object`, with
  `OFFSITE_CONVERSIONS`. A custom conversion is sharper than `custom_event_type` — it can mean
  *paid*, where a generic `Lead` means *submitted a form*.

**Then say the dependency out loud:** the flow has to actually redirect to that page. If it does
not, the campaign optimises on an event that never arrives, and nothing in the ad build reveals it.

## Website URL and URL parameters are two fields

`link_urls[].website_url` is the clean destination (`https://www.example.com`). The UTMs go in
**`url_tags`** — Meta's separate "URL parameters" field. Baking UTMs into the URL works but
leaves the parameters field empty and breaks tracking the moment someone edits the URL. Keep
them apart.

`{{ad.name}}`, `{{site_source_name}}`, `{{placement}}` resolve at delivery. **`{{ad.name}}`
freezes at publish** — so name every ad meaningfully (after its creative, e.g.
`sq-kenyan-a`) **before** publishing, or `utm_content` reports a stale name forever.

## Tracking is separate and not automatic

Without it the campaign reports clicks but **zero conversions**, so it can't be compared to a
conversions campaign — set it or the whole test is unreadable. It lives on the **ad**, and
unlike creative fields it's **editable in place** via `ads_update_entity` (no rebuild):

```json
{ "tracking_specs": [{ "action.type": ["offsite_conversion"], "fb_pixel": ["<PIXEL_ID>"] }],
  "conversion_domain": "example.com" }
```

Do **not** put the pixel in the ad set's `promoted_object` under a Traffic objective —
`Promoted Object Invalid`. `promoted_object` is required for conversions objectives, rejected
for Traffic.

## Errors are the real documentation

Two enums are narrower than any doc, and only the rejection reveals the true list:

- **Optimization goal** is gated by objective — trust `valid_optimization_goals` from the
  campaign response.
- **CTA type** is gated again under Traffic + dynamic creative. `SIGN_UP`, `LEARN_MORE`,
  `SEE_DETAILS` pass; `BOOK_NOW`, `GET_DETAILS`, `REGISTER_NOW`, `GET_STARTED` are rejected
  with `Not Supported CallToAction Type For Objective`. When one is refused, the error lists
  every valid value — read it and pick from it rather than guessing again.

### #1870194 — "location targeting option that has been removed"

Ads Manager can refuse to publish an MCP-built ad set with *"Your audience contains a location
targeting option that has been removed (people living in, people travelling in or people
recently in a location)"*. The API never raises it: `ads_get_errors` returns `[]` throughout,
so it appears only when the client hits Publish.

**Set `geo_locations.location_types` explicitly on the ad set** — `["home", "recent"]`, the
surviving pair. Passing it at creation costs nothing and is what preceded a clean publish on the
one account where this was worked through.

**Do not verify it from the read-back.** `targeting` comes back as *effective* targeting, and it
keeps listing `frequently_in` — the retired value — no matter what you write, at create and
update alike, with Advantage+ audience on or off. An ad set that reads `["frequently_in", "home",
"recent"]` published successfully and went ACTIVE. Reading that field to judge whether the fix
landed produces a confident wrong answer twice over; the publish attempt is the only real test.

## What you cannot fix from here — tell the client

- **Instagram identity — and `[]` does NOT mean Facebook-only.** `ads_get_ig_accounts` returning
  `[]` means the app cannot *enumerate* IG accounts on the ad account (it needs `instagram_basic`).
  It says nothing about delivery. A creative carrying only `page_id` still runs Instagram
  placements off the **Page-backed Instagram identity** — the Page's own connected account — with
  nothing linked and no UI step. Measured on a live ad account in August 2026: `[]` from
  the tool while Instagram carried **2 of 3 impressions and the only click**. What an explicit
  `instagram_user_id` buys is the handle and keeping engagement on the account, not access to the
  placement. Say that, not "it may run Facebook-only".
- **Per-image attribution in the client's own analytics is impossible with one DCO ad.** All
  images share one destination URL, so GA/Plausible sees one source. Per-image data exists
  **only inside Meta** — read it with `ads_get_ad_entities`, `level: ad`,
  `breakdowns: ["image_asset"]`. If they need per-image splits in their own analytics, that's
  a different structure: separate ads, one image and one `utm_content` each.
- **Sub-two-day flights never leave Meta's learning phase.** Any "winner" is directional, not
  significant. Say so rather than letting a noisy number read as a result.
- **The account spending limit.** Ads Manager warns *"You'll reach your account spending limit
  soon"* on the publish screen. It is an **account-level** cap, invisible from the campaign you
  built and unaffected by a small daily budget, and it stops delivery across every campaign when
  hit. Billing job, theirs, and worth raising before activation rather than after delivery dies.
- **A conversion goal with too few events.** Optimisation wants roughly 50 events a week to leave
  learning. Do the arithmetic on their budget and flight and say the number plainly, rather than
  letting a conversions objective imply an accuracy the spend cannot buy.

**Before crying "leak": a campaign can read `ACTIVE` and spend nothing.** Campaigns whose
`stop_time` has passed, and campaigns whose ad sets are paused, both keep an `ACTIVE`
`effective_status`. Check `stop_time` and last-3-days spend before telling anyone money is
draining on a dead event.

## Before you hand it back

1. `ads_get_ad_preview` (`MOBILE_FEED_STANDARD` and `INSTAGRAM_STANDARD`) — return the
   `preview_url` to the client as a link.
2. Re-read entities and confirm status is `PAUSED` everywhere. Editing a budget **force-pauses**
   the campaign — expected, not a bug.
3. State plainly what's left for the client: activation, and the Instagram account.

## Red flags — stop

- About to call `ads_activate_entity` — that's the client's to do, not yours.
- Concluding a dynamic creative "can't be built via MCP" — it can, via inline `asset_feed_spec`.
- Pixel going into a Traffic ad set's `promoted_object`.
- UTMs baked into `website_url` instead of `url_tags`.
- Publishing before the ad is named for its creative.
- Reporting the ad built but never setting `tracking_specs`.
- Dropping to a Traffic objective because the destination has no pixel, without first checking
  where the flow *ends*.
- Retrying a failed create without reading the parent's children first.
- Judging a targeting fix from the `targeting` read-back instead of a publish attempt.
- Promising an ad before establishing that the images can actually reach Meta.
- Calling placement coverage from any identity- or account-listing tool. Only a
  `publisher_platform` breakdown (`ads_get_ad_entities`, `level: ad`) on an entity that has
  actually delivered answers "where is this running?" — one call, and it ends the question.

---

Stuck, or want to send feedback on this skill? Read the `about-fluent` skill if Fluent AI Skills is installed, or visit fluent.ke.
