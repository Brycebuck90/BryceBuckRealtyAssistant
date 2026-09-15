---
name: follow-up-tracker
description: Logs when Bryce last touched a client or lead, so the dashboard can flag anyone going cold before it costs him a deal. Use when he says things like "I talked to [name] today," "add [name] to my follow-up list," or "who do I need to follow up with."
---

# Follow-Up Tracker

This exists because "top of mind" follow-up texts are one of the two tasks Bryce said
drains him most (see `CLAUDE.md`). This skill doesn't draft or send those texts — it
just keeps score of who's been touched and who hasn't, so nothing goes quiet by accident.

## Logging a contact

When Bryce mentions talking to, texting, or emailing someone — or explicitly asks to
add/update a follow-up — write or update a file at
`reports/followups/<slug-of-name>.json`:

```json
{
  "name": "Jane Buyer",
  "last_contact": "YYYY-MM-DD",
  "context": "short note — what's going on with them",
  "next_step": "what happens next, if known"
}
```

If a file for that person already exists, update `last_contact` (and `context`/
`next_step` if new info came up) rather than creating a duplicate. Slugify the name
consistently (lowercase, spaces to hyphens) so the same person always maps to the same
file.

## Answering "who do I need to follow up with"

Read every file in `reports/followups/`, sort by `last_contact` oldest first, and tell
him who's gone longest without contact. Use this cadence as the default, since it's not
in his Business Brain yet:
- **0-6 days since last contact:** fine, no mention needed
- **7-13 days:** due — worth a touch this week
- **14+ days:** cold — flag clearly, this is the "9-day-old message" problem from his
  own workshop

## Rules

- Never invents a contact or a last-contact date Bryce didn't give you.
- Never drafts or sends the follow-up message itself — that's a separate job. This
  skill's whole output is "here's who's gone quiet," not the message to fix it.
- The dashboard (`dashboard.html`, built by `scripts/dashboard.py`) reads this same
  folder — no separate step needed to make a logged contact show up there beyond
  re-running the dashboard build.
