# Progress

## Lesson 1 — Setup
- [x] Complete

## Lesson 2 — Your Brain
- [x] Complete — `CLAUDE.md` filled in from Bryce's existing EA brief + follow-up interview

## Lesson 3 — Connect
- [ ] Not complete
- **Do this one on a local machine, not a cloud/web Claude Code session.**
  A web/remote session tried this once and the raw IMAP connection (port 993)
  got silently blocked by the sandbox's network policy — it hung, then failed,
  with no auth error at all. Nothing wrong with the credentials; the
  environment just can't make that kind of connection.
- Next step on a real machine: generate a fresh Gmail app password (revoke the
  one made during the failed attempt — it was never used and never committed),
  `cp .env.example .env`, fill in `EMAIL_ADDRESS` / `EMAIL_APP_PASSWORD` /
  `IMAP_HOST=imap.gmail.com` (custom domain `theelevategroup.com` runs on
  Google Workspace), then `python3 inbox.py --check`.

## Lesson 4 — The Sweep
- [ ] Not started (depends on Lesson 3)
