# Bambu printer safety gate

*Contributed by Samwel Tinega from his project work.*

Applies whenever a task touches a real, physical Bambu Lab printer over the
local network via `bambu-printer-mcp` or `bambu-cli` — not to designing or
slicing, which stay local and are always safe to do. Mistakes at the printer
cost filament, time, or damage the machine.

## The pipeline

Every print originates from a reviewed, sliced file — never raw G-code and
never an in-session auto-slice the user hasn't seen:

1. **Design** — FreeCAD, OpenSCAD, Fusion, or another CAD app produces the
   model (STEP/STL).
2. **Slice** — Bambu Studio (or the matching slicer) turns the model into a
   `.gcode.3mf`, with the correct printer profile, nozzle, bed type, and
   AMS/filament mapping selected by the user.
3. **Review** — the user (or the agent, read-only) inspects the `.gcode.3mf`
   metadata before it goes anywhere near the printer: plate count, estimated
   time/filament use, per-slot AMS mapping, calibration flags.
4. **Send** — only after review and explicit approval does a file reach the
   printer.

Do not shortcut this by asking the MCP server to auto-slice an STL directly
onto the printer unless the user explicitly asks for that specific shortcut
*and* still reviews the resulting plan before printing.

## Default: read-only

Unless the current turn contains explicit user approval for a specific
physical action, only use these categories of calls:

- Printer/job status, temperatures, progress, layer count
- AMS/filament inventory (`get_printer_filaments`, AMS resource reads)
- HMS / error-state resource reads
- Camera snapshot, **only if** the user has said camera access is enabled
- Listing files already on the printer (no download/delete)
- Inspecting a local `.gcode.3mf`'s metadata (plate objects, slice settings)

Never call, suggest, or chain into a write action as a side effect of a read
request.

## Requires explicit approval, every time

Each of the following needs the user's explicit go-ahead **in the current
conversation** — a past approval for one job does not carry over to the next:

- Uploading or starting a print (`print_3mf`, file upload + start)
- Queueing, pausing, resuming, or cancelling a job
- Setting nozzle/bed temperature, heating, or any G-code dispatch
- Moving axes, homing, or calibration routines
- AMS filament drying (`set_ams_drying`) or AMS RFID/config changes
- Deleting files from the printer's storage
- Any raw G-code, regardless of how trivial it looks

When asking for approval, state plainly: the printer model, the file being
sent, the AMS/filament mapping, and what the action will physically do (e.g.
"this heats the nozzle to 220°C and starts printing plate 1 of
cowl_v3.gcode.3mf using AMS slots 0-2"). Do not batch multiple physical
actions into one approval — get one confirmation per action.

## Pre-flight checks before any write action

Before requesting approval for a print, verify and report:

- **Printer model** matches the sliced file's target profile
- **Nozzle diameter** matches what's physically installed
- **Bed type** matches what's physically on the printer
- **Material/AMS mapping** — each slot in the 3MF resolves to a real,
  currently-loaded spool (check `get_printer_filaments`); flag any
  `unresolved` or `none`-confidence match rather than assuming it's fine
- **Sliced-file metadata** — plate count, estimated time, filament grams —
  looks sane for what the user asked for

If any check fails or is ambiguous, stop and surface it — do not proceed on a
best-effort guess.

## Secrets

Printer serial number, LAN access code/token, and any credentials live only
in a local ACL-restricted `.env` used by `bambu-printer-mcp`, or in the OS
credential manager. Never:

- Print, log, or echo the serial number or access code/token in chat, tool
  output, reports, screenshots, commit messages, or any file under version
  control
- Write them into a skill file, a report, or memory
- Pass them as CLI arguments (they show up in process listings/shell
  history) — prefer env vars sourced from the `.env` file

When a printer status response includes the serial number (it does, by
default, in `get_printer_status`), redact it before displaying, saving to a
file, or summarizing — including inside any nested JSON-encoded string
fields in the response, not just top-level keys.

**Key-name-based redaction is not enough.** Status calls can embed a
JSON-encoded string inside a `text` field that a naive object-walker skips
over, and raw CLI commands can print the access code and serial as plain
table columns with no JSON structure at all — either leaks a real secret
into tool output before being caught. The fix that holds:

- **Never run the raw CLI directly when its output might reach chat/logs.**
  Wrap it in a script that loads the known secret values from `.env` inside
  the script and does a literal string-replace on the captured output
  before returning anything, so the redaction happens before the text exists
  in context, not after.
- For MCP JSON responses, redact by **both** key name (`serial`, `token`,
  `access.?code`, `password`) **and** literal value match against the known
  secrets from `.env`, recursing into any string field that parses as JSON.
  Do this in a script that writes only the redacted result to a file that is
  then read — never read or print a raw response file directly.
- After writing a redacted summary, delete any raw/intermediate file that
  held the unredacted response.
- Treat every new printer-control command as a potential leak vector before
  running it, not just ones already known to print secrets.

If a secret does leak into chat/tool output despite this, say so immediately
and plainly, and recommend changing the printer's LAN access code so the leaked
value stops working, following Bambu Lab's current instructions for that printer
model (on many models the code changes when LAN Only Mode is switched off and on
from the touchscreen; confirm the new code differs before relying on it).

## Network

The printer must stay LAN-only. Never propose port-forwarding, tunneling, or
any configuration that exposes it to the public internet.
