#!/usr/bin/env python3
"""
inbox.py — read-only inbox reader for The 80/20 Starter.

Fetches the last N days of mail over IMAP and prints it as JSON.

HARD GUARANTEES (do not remove — these are the promise we make out loud):
  * NEVER deletes, moves, flags, or sends anything. No such code exists here.
    These are not switches that are turned off — the capability is absent.
  * NEVER opens attachments. Filenames are reported; contents are never read.
  * Nothing is stored. Output goes to stdout and dies with the process.

YOUR CHOICE (see PERMISSIONS.md):
  * Marking as read is OFF by default — we use BODY.PEEK so your inbox looks
    untouched. If you'd rather it marked what it read, that's your call:
    set MARK_AS_READ=true in .env, or pass --mark-read.

Standard library only. Nothing to install.

Usage:
    python3 scripts/inbox.py               # last 7 days, nothing marked read
    python3 scripts/inbox.py --days 14
    python3 scripts/inbox.py --check       # test the connection only
    python3 scripts/inbox.py --mark-read   # opt in to marking mail as read
"""

import argparse
import email
import email.utils
import imaplib
import json
import os
import re
import sys
from datetime import datetime, timedelta
from email.header import decode_header, make_header

# IMAP hosts by provider. One code path, every provider.
IMAP_HOSTS = {
    "gmail.com": "imap.gmail.com",
    "googlemail.com": "imap.gmail.com",
    "yahoo.com": "imap.mail.yahoo.com",
    "ymail.com": "imap.mail.yahoo.com",
    "aol.com": "imap.aol.com",
    "outlook.com": "outlook.office365.com",
    "hotmail.com": "outlook.office365.com",
    "live.com": "outlook.office365.com",
    "msn.com": "outlook.office365.com",
    "icloud.com": "imap.mail.me.com",
    "me.com": "imap.mail.me.com",
}

MAX_BODY_CHARS = 2000   # plenty to judge an email by; keeps the payload sane
MAX_MESSAGES = 400      # safety cap for very busy inboxes


def load_env(path=".env"):
    """Minimal .env reader — no dependency, no surprises."""
    if not os.path.exists(path):
        return
    with open(path, "r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, val = line.split("=", 1)
            os.environ.setdefault(key.strip(), val.strip().strip('"').strip("'"))


def resolve_host(address, override):
    if override:
        return override
    domain = address.split("@")[-1].lower()
    if domain in IMAP_HOSTS:
        return IMAP_HOSTS[domain]
    # Work/brokerage domains are very often Google Workspace or Microsoft 365.
    return None


def decode_field(raw):
    if not raw:
        return ""
    try:
        return str(make_header(decode_header(raw)))
    except Exception:
        return str(raw)


def extract_body(msg):
    """Plain text only. Attachments are never opened — only named."""
    body = ""
    attachments = []

    if msg.is_multipart():
        for part in msg.walk():
            disposition = str(part.get("Content-Disposition") or "")
            filename = part.get_filename()

            if filename or "attachment" in disposition.lower():
                # NEVER read the payload. The name is a signal; the contents are theirs.
                attachments.append(decode_field(filename) or "(unnamed attachment)")
                continue

            if part.get_content_type() == "text/plain" and not body:
                try:
                    payload = part.get_payload(decode=True) or b""
                    body = payload.decode(part.get_content_charset() or "utf-8", "replace")
                except Exception:
                    body = ""
    else:
        try:
            payload = msg.get_payload(decode=True) or b""
            body = payload.decode(msg.get_content_charset() or "utf-8", "replace")
        except Exception:
            body = ""

    body = re.sub(r"\r\n", "\n", body)
    body = re.sub(r"\n{3,}", "\n\n", body)
    body = re.sub(r"[ \t]{2,}", " ", body).strip()

    truncated = len(body) > MAX_BODY_CHARS
    return body[:MAX_BODY_CHARS], truncated, attachments


def connect(address, password, host):
    conn = imaplib.IMAP4_SSL(host)
    conn.login(address, password)
    return conn


def fetch(conn, days, mark_read=False):
    # Default: readonly=True + BODY.PEEK, so the server never sets the \Seen flag.
    # If the user opted in to mark_read, we open the mailbox writable and drop the
    # .PEEK — that is the ONLY thing this flag changes. Nothing else becomes possible:
    # there is still no delete, move, flag, or send anywhere in this file.
    conn.select("INBOX", readonly=not mark_read)

    since = (datetime.now() - timedelta(days=days)).strftime("%d-%b-%Y")
    status, data = conn.search(None, "SINCE", since)
    if status != "OK":
        return [], 0

    ids = data[0].split()
    total = len(ids)
    if total > MAX_MESSAGES:
        ids = ids[-MAX_MESSAGES:]

    # BODY.PEEK[] reads without setting the \Seen flag — the whole reason nobody's
    # inbox gets "marked read" by running this. BODY[] is the opt-in alternative.
    fetch_spec = "(BODY[])" if mark_read else "(BODY.PEEK[])"

    messages = []
    for msg_id in ids:
        status, payload = conn.fetch(msg_id, fetch_spec)
        if status != "OK" or not payload or not isinstance(payload[0], tuple):
            continue

        msg = email.message_from_bytes(payload[0][1])
        body, truncated, attachments = extract_body(msg)

        date_raw = msg.get("Date", "")
        try:
            parsed = email.utils.parsedate_to_datetime(date_raw)
            date_iso = parsed.isoformat()
            days_ago = (datetime.now(parsed.tzinfo) - parsed).days
        except Exception:
            date_iso, days_ago = date_raw, None

        messages.append({
            "from": decode_field(msg.get("From", "")),
            "to": decode_field(msg.get("To", "")),
            "subject": decode_field(msg.get("Subject", "")),
            "date": date_iso,
            "days_ago": days_ago,
            "message_id": msg.get("Message-ID", ""),
            "body": body,
            "body_truncated": truncated,
            "attachments": attachments,
        })

    return messages, total


def main():
    parser = argparse.ArgumentParser(description="Read-only inbox reader.")
    parser.add_argument("--days", type=int, default=7, help="How far back to look (default 7)")
    parser.add_argument("--check", action="store_true", help="Test the connection and exit")
    parser.add_argument("--mark-read", action="store_true",
                        help="Opt in to marking mail as read (default: leaves it untouched)")
    args = parser.parse_args()

    load_env()
    mark_read = args.mark_read or os.environ.get("MARK_AS_READ", "").lower() in ("1", "true", "yes")
    address = os.environ.get("EMAIL_ADDRESS", "").strip()
    password = os.environ.get("EMAIL_APP_PASSWORD", "").strip()
    host = resolve_host(address, os.environ.get("IMAP_HOST", "").strip())

    if not address or not password:
        print(json.dumps({
            "ok": False,
            "error": "missing_credentials",
            "message": "EMAIL_ADDRESS and EMAIL_APP_PASSWORD are not set. Copy .env.example to .env and fill it in (Lesson 3).",
        }, indent=2))
        sys.exit(1)

    if not host:
        print(json.dumps({
            "ok": False,
            "error": "unknown_provider",
            "message": "Couldn't guess the mail server for '%s'. Add IMAP_HOST to .env — for a work address it's usually imap.gmail.com (Google Workspace) or outlook.office365.com (Microsoft 365)." % address,
        }, indent=2))
        sys.exit(1)

    try:
        conn = connect(address, password, host)
    except imaplib.IMAP4.error as exc:
        print(json.dumps({
            "ok": False,
            "error": "login_failed",
            "host": host,
            "message": "The mail server rejected the login: %s. Almost always this is a regular password instead of an app password, or 2-factor isn't on yet. If it's a brokerage account, the admin may block app passwords — point it at an email you control instead." % exc,
        }, indent=2))
        sys.exit(1)
    except Exception as exc:
        print(json.dumps({
            "ok": False, "error": "connection_failed", "host": host, "message": str(exc),
        }, indent=2))
        sys.exit(1)

    try:
        if args.check:
            print(json.dumps({
                "ok": True, "checked": True, "account": address, "host": host,
                "message": "Connected. Read-only. Nothing was changed.",
            }, indent=2))
            return

        messages, total = fetch(conn, args.days, mark_read)
        print(json.dumps({
            "ok": True,
            "account": address,
            "host": host,
            "days": args.days,
            "found": total,
            "returned": len(messages),
            "capped": total > MAX_MESSAGES,
            "marked_as_read": mark_read,
            "notice": (
                "Your mail was marked as read — you turned that on. Set MARK_AS_READ=false "
                "in .env to go back to leaving it untouched."
                if mark_read else
                "Nothing was marked as read. Your inbox looks exactly like it did before. "
                "If you'd rather it marked what it read, that's your call — see PERMISSIONS.md."
            ),
            "never_does": ["send", "delete", "move", "archive", "open attachments"],
            "messages": messages,
        }, indent=2))
    finally:
        try:
            conn.close()
        except Exception:
            pass
        conn.logout()


if __name__ == "__main__":
    main()
