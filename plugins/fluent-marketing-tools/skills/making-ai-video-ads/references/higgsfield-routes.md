# Higgsfield: routes, costs and the trial

Tested on real jobs in November 2026. Plans and trials change: check the current terms on the account (`balance`, `show_plans_and_credits`) before relying on any line here.

## Three ways in

| Route | What it is | Notes |
|---|---|---|
| Connector (MCP) | Higgsfield connector added to Claude, ChatGPT or another MCP client | Has `media_upload`, `generate_video`, `get_cost`, `balance`, `cancel_trial_auto_renewal` |
| CLI | `npm i -g @higgsfield/cli`, then `higgsfield auth login` and `higgsfield workspace set <id>` | Refuses every request until a workspace is set. A `--prompt` value starting with `@` is read as a file path, so start prompts with a word |
| Official skills | `npx skills add higgsfield-ai/skills -g` | Drive the CLI. Install per user, not into a shared folder |

## Price before you run

- `get_cost: true` on the connector, or `higgsfield generate cost`, quotes a job without running it.
- Seedance 2.5, 30 seconds, quoted about 480 credits outside a trial (Nov 2026).
- A new free account starts with 10 credits and gets no daily top-up. A character sheet on Nano Banana Pro cost 2. GPT Image 2.6 was refused on the free plan (`job_minimum_basic_plan_required`) even though it returned a quote.

## The connector trial (Nov 2026)

Higgsfield offered a 72-hour free trial of its top models through the connector:

| Term | As found |
|---|---|
| Who gets it | New accounts. An older free account was never offered it |
| Card | Required. It auto-renews to a paid plan when the 72 hours end |
| Cancel | Straight after starting: say "cancel auto-renewal" to the connector, or use the website. The trial keeps running until its end time |
| Where it is free | Claude chat, Claude Cowork and ChatGPT, through the connector |
| Where it is refused | Claude Code (the connector says unlimited generations are not available there) and the CLI (`only_mcp_usage_on_trial_is_available`). No credits are charged on a refusal |
| Seedance 2.5 | 480p only, up to 30 seconds. 720p and 1080p are refused before submitting |
| Concurrency | One free job at a time. A second job approved while the first is queued never starts |
| Queue | About an hour per 30-second job; free jobs wait behind paid work |

**Use the `use_unlim: true` flag on every trial generation**, and tell the chat to stop if a job would cost credits instead.

## Driving a chat from your agent

When the free route is a chat surface:

1. In your agent: write the script and prompts, make and crop the references, upload them with `media_upload`, note the IDs.
2. Write one paste-ready prompt: the settings, the media IDs mapped to `@Image 1` and `@Image 2`, the film prompt unchanged, and "set use_unlim to true; if any generation would cost credits, stop and tell me".
3. In a chat with the Higgsfield connector on the same account: paste it, approve the tool calls, and wait for the job ID.
4. Back in your agent: `higgsfield generate wait <job-id>` (or the connector's `show_generations`) prints the result URL; download it and log it.
5. Submit the next format only after the first job finishes.

If the agent can drive a browser, it can do step 3 too. Approvals in the chat stay with the person.

## Other free routes

- Higgsfield runs weekly challenges with credit and cash prizes, and a creator partnership program with monthly credits.
- Extra accounts to repeat a trial break Higgsfield's terms. Leave them out.
