#!/usr/bin/env python3
"""Email the day's brief. Generic template - see setting-up-a-daily-brief.

Reads the SMTP app password from the macOS Keychain, never from a file, so no
credential lives in the synced vault. Builds the newsletter with the Claude
Community lockup as CID attachments, because Gmail strips data: URI images.

Usage: send_brief.py <brief-dir> "<Long Date>"
Config: recipients.txt (one address per line, # comments allowed)
Keychain: security add-generic-password -s CHANGEME-brief-smtp -a <address> -w
"""
import os, re, ssl, sys, smtplib, subprocess
from email.message import EmailMessage
from email.utils import make_msgid, formatdate

HERE = os.path.dirname(os.path.abspath(__file__))
SERVICE = "CHANGEME-brief-smtp"   # one keychain service per instance
SMTP_HOST, SMTP_PORT = "smtp.gmail.com", 465

# --- per-instance configuration -------------------------------------------------
ORG        = "CHANGEME ORG"
BRIEF_NAME = "CHANGEME Brief"
TAGLINE    = "CHANGEME one-line footer"
ACCENT, GROUND, INK = "#1F4D5C", "#FBFAF8", "#1A1A1A"
# --------------------------------------------------------------------------------


def keychain_password(account):
    r = subprocess.run(
        ["security", "find-generic-password", "-s", SERVICE, "-a", account, "-w"],
        capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit(
            "No Keychain entry for service '%s' account '%s'.\n"
            "Create one with:\n"
            "  security add-generic-password -s %s -a %s -w"
            % (SERVICE, account, SERVICE, account))
    return r.stdout.strip()


def recipients():
    path = os.path.join(HERE, "recipients.txt")
    if not os.path.exists(path):
        raise SystemExit("recipients.txt missing - add one address per line.")
    out = []
    for line in open(path, encoding="utf-8"):
        line = line.split("#", 1)[0].strip()
        if line:
            out.append(line)
    if not out:
        raise SystemExit("recipients.txt has no addresses.")
    return out


def build_html(fragment, date_long, cids=None):
    """Email-safe wrapper. Inline styles on structural elements; Gmail drops much of a
    <style> block and ignores CSS variables entirely. Centring uses a table with
    align="center" because Gmail ignores display:block + margin:0 auto on children."""
    accent, ground, ink = ACCENT, GROUND, INK
    frag = fragment.replace(
        '<div class="tip">',
        '<div style="background:rgba(26,26,26,.04);border-left:3px solid %s;'
        'padding:18px 20px;margin:0 0 20px">' % accent)
    return f"""<!DOCTYPE html><html><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>
  body{{margin:0;padding:0;background:{ground}}}
  .wrap{{max-width:640px;margin:0 auto;background:{ground};color:{ink};
        font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Arial,sans-serif;
        font-size:16px;line-height:1.62}}
  h2{{font-size:12px;letter-spacing:.2em;text-transform:uppercase;color:{accent};margin:34px 0 2px}}
  .hr{{height:2px;background:{accent};opacity:.3;border:0;margin:0 0 20px}}
  .item{{padding-bottom:22px;margin-bottom:24px;border-bottom:1px solid rgba(26,26,26,.13)}}
  .item h3{{font-size:18px;line-height:1.35;margin:0 0 8px}}
  .meta{{font-size:13px;color:rgba(26,26,26,.6);margin:0 0 10px}}
  .tag{{display:inline-block;font-size:11px;letter-spacing:.09em;text-transform:uppercase;
       font-weight:700;color:{accent};border:1px solid {accent};border-radius:3px;padding:1px 6px;
       margin-right:8px}}
  a{{color:{accent}}}
  .src{{font-size:13px;word-break:break-word}}
  .standfirst{{font-size:17px;color:rgba(26,26,26,.66);padding-bottom:22px;
              border-bottom:1px solid rgba(26,26,26,.13)}}
  pre{{background:rgba(26,26,26,.05);padding:12px 14px;overflow-x:auto;font-size:13px}}
  .quiet{{color:rgba(26,26,26,.6);font-style:italic}}
</style></head>
<body style="margin:0;padding:0;background:{ground}">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"
       style="background:{accent};border-collapse:collapse">
 <tr><td align="center" style="padding:32px 20px 26px;
     font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Arial,sans-serif">
   <div style="color:#fff;font-size:11px;letter-spacing:.24em;text-transform:uppercase;
               opacity:.8">{ORG}</div>
   <div style="color:#fff;font-size:25px;font-weight:600;padding-top:8px">{BRIEF_NAME}</div>
   <div style="color:#fff;font-size:13px;opacity:.88;padding-top:5px">{date_long}</div>
 </td></tr>
</table>
<div class="wrap" style="padding:0 20px 10px">
{frag}
</div>
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"
       style="background:{accent};border-collapse:collapse;margin-top:36px">
 <tr><td align="center" style="padding:26px 20px;color:#fff;font-size:13px;line-height:1.6;
     font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Arial,sans-serif">
   {TAGLINE}<br>
   <span style="font-size:12px;opacity:.82">Every item was checked against its primary
   source before publication.</span>
 </td></tr>
</table>
</body></html>"""


def main():
    if len(sys.argv) < 3:
        raise SystemExit("usage: send_brief.py <brief-dir> \"<Long Date>\"")
    outdir, date_long = sys.argv[1], sys.argv[2]

    frag_path = os.path.join(outdir, "content.html")
    if not os.path.exists(frag_path):
        raise SystemExit("no content.html in %s" % outdir)
    fragment = open(frag_path, encoding="utf-8").read()

    rcpts = recipients()
    sender = rcpts[0]
    password = keychain_password(sender)


    msg = EmailMessage()
    msg["Subject"] = "%s - %s" % (BRIEF_NAME, date_long)
    msg["From"] = sender
    msg["To"] = ", ".join(rcpts)
    msg["Date"] = formatdate(localtime=True)

    plain = re.sub(r"<[^>]+>", "", fragment)
    plain = re.sub(r"\n{3,}", "\n\n", plain).strip()
    msg.set_content("%s - %s\n\n%s" % (BRIEF_NAME, date_long, plain))
    msg.add_alternative(build_html(fragment, date_long), subtype="html")


    full = os.path.join(outdir, "brief.html")
    if os.path.exists(full):
        with open(full, "rb") as fh:
            msg.add_attachment(fh.read(), maintype="text", subtype="html",
                               filename="brief-%s.html" % os.path.basename(outdir))

    ctx = ssl.create_default_context()
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT, context=ctx, timeout=60) as s:
        s.login(sender, password)
        s.send_message(msg)
    print("emailed %s to %s" % (os.path.basename(outdir), ", ".join(rcpts)))


if __name__ == "__main__":
    main()
