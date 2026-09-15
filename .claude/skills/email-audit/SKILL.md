---
name: email-audit
description: The 7-Day Sweep. Reads Bryce's inbox (read-only), sorts it into money / worth-your-time / noise using his Business Brain, and drafts replies for anything real. Use when Bryce says things like "audit my email," "run the sweep," or "what did I miss."
---

# Email Audit — The 7-Day Sweep

Read `CLAUDE.md` first, always — specifically **"What a real opportunity looks like for
me this quarter"**. That section is the whole filter. It's what turns a generic inbox
scan into one that knows a live deal from a newsletter.

## What this does

1. Run `python3 scripts/inbox.py` (add `--days N` if Bryce asked for a different window;
   default is 7). If it returns `"ok": false`, stop and tell him plainly what's wrong —
   usually missing `.env` credentials (Lesson 3 not done on this machine yet) or a login
   failure. Don't guess around it.
2. Sort every message into exactly one of three buckets:
   - **Money** — matches "what a real opportunity looks like" in CLAUDE.md: a live buyer
     or seller question, a past client mentioning a move, an investor asking about
     off-market, anything that smells like a deal.
   - **Worth your time** — not a deal, but a real person who deserves a reply (a referral
     source, a vendor, a genuine question).
   - **Noise** — newsletters, marketing, automated notifications, spam.
3. For every **money** item, draft a reply in Bryce's voice (see CLAUDE.md → "How I
   sound") and save it as a `.txt` file in `drafts/`, named
   `YYYY-MM-DD-<sender-slug>-<short-subject-slug>.txt`. **Never send it.** It sits there
   for Bryce to read, edit, and send himself.
4. Save a summary of the run to `reports/email/YYYY-MM-DD.json` (see shape below) so
   `dashboard.html` can show it. After saving, mention he can run
   `python3 scripts/dashboard.py` (or ask to "update my dashboard") to see it there.

## Report shape

```json
{
  "date": "YYYY-MM-DD",
  "days_covered": 7,
  "money": [
    {"from": "Jane Buyer <jane@example.com>", "subject": "...", "days_ago": 2,
     "why": "one line on why this is a real opportunity", "draft_path": "drafts/..."}
  ],
  "worth_your_time": [
    {"from": "...", "subject": "...", "days_ago": 0, "why": "one line"}
  ],
  "noise_count": 0
}
```

## Rules

- Read-only, always. Never send, delete, move, archive, or mark as read unless Bryce has
  explicitly turned `MARK_AS_READ` on in `.env` — that's `inbox.py`'s call to make, not
  this skill's.
- Never open or describe attachment contents — the filename is the only signal, per
  `PERMISSIONS.md`.
- If the oldest **money** item is more than a few days old, say so plainly when you hand
  back results — that's the number that makes this useful (see `lesson-4-the-sweep.md`
  for why that moment matters).
- If the inbox is genuinely clean, say that plainly too. Don't manufacture urgency to
  make the sweep feel more useful than it was.
