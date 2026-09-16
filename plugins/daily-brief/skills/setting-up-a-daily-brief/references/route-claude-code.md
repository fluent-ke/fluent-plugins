# Route: Claude Code (local schedule)

Pick this when the brief must write into a local or synced folder — a vault, a repo, a second
brain. A cloud routine cannot reach any of those.

## Cost of this route

The machine must be on, or wakeable, and have power. That is the only real limitation, and it is
worth stating to the person plainly rather than discovering it together on day three.

## macOS

**1. Runner.** `run-brief.sh` in the instance folder. It must:

- `cd "$(dirname "$0")"` — a scheduler gives you no working directory
- Resolve the `claude` binary at runtime, with a fallback glob. `launchd` runs with
  `PATH=/usr/bin:/bin:/usr/sbin:/sbin`; an nvm-installed binary is not on it
- Pin the model with `--model`, so the job does not inherit the person's own default
- Wait for real connectivity before generating — a just-woken machine has no Wi-Fi yet
- Skip if today's brief already exists, so a second run cannot overwrite one being read
- Retry generation once if the first attempt leaves files incomplete
- Splice the fragment into the template, then copy to `latest.*`
- Email **last**, and never fatally

**2. Schedule.** A `launchd` agent in `~/Library/LaunchAgents/`, with `StartCalendarInterval` set
to the hour and minute. Omit `Weekday` for every day; include it for weekdays only. Load with
`launchctl load`, then confirm with `launchctl print gui/$(id -u)/<label>`.

**3. Wake.** `sudo pmset repeat wakeorpoweron MTWRFSU 06:55:00`, five minutes before the fire time.
Without it, `launchd` defers on a sleeping Mac and the brief arrives when the lid opens. Verify
with `pmset -g sched`.

**4. Prove auth in the scheduler's own environment.** Do not assume. Load a throwaway agent that
runs `claude -p "Reply with exactly: AUTH_OK"`, kickstart it, read the output file, then remove it.
If this fails you have found the problem now instead of at 07:00.

**5. Test the real job** with `launchctl kickstart -k gui/$(id -u)/<label>` and read both log paths.

## Windows

Task Scheduler, with "Wake the computer to run this task" enabled and "Run whether user is logged
on or not" for an unattended box. Same script logic in PowerShell. Credential goes in Credential
Manager rather than Keychain.

## Linux

`systemd` timer with `Persistent=true`, or cron on an always-on host. A server that never sleeps
removes the wake problem entirely, which is why a VPS is the better home when one is available.
