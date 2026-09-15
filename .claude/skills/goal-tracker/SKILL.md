---
name: goal-tracker
description: Tracks progress toward Bryce's 90-day goal (6 deals / $30K GCI) from his Business Brain. Use when he says things like "log a closed deal," "update my goal progress," or "how am I tracking toward my 90-day goal."
---

# Goal Tracker

Read `CLAUDE.md` → **"What I'm building toward"** for the current target. Right now
that's 6 deals and $30,000 GCI in 90 days — but always read it fresh rather than
hardcoding the number, since goals get updated as quarters turn over.

## The progress file

One file, `reports/goals/progress.json`:

```json
{
  "period_start": "YYYY-MM-DD",
  "period_days": 90,
  "target_deals": 6,
  "target_gci": 30000,
  "deals_closed": 0,
  "gci_earned": 0,
  "log": [
    {"date": "YYYY-MM-DD", "description": "123 Main St closing", "gci": 8500}
  ]
}
```

If it doesn't exist yet, create it from what's in CLAUDE.md, with `period_start` set to
today and everything else at zero.

## Logging a deal

When Bryce says something like "log a closed deal, $8,500 GCI on 123 Main," append an
entry to `log`, increment `deals_closed` by 1, and add the GCI to `gci_earned`. Confirm
back to him in one line what got logged and where he now stands (e.g. "3 of 6 deals,
$18,200 of $30,000 — 25 days left in the sprint").

## Answering progress questions

Read the file, compare against the target and against how many days are left in the
period (`period_start` + `period_days`), and give a straight read — on pace, behind, or
ahead. No filler.

## Rules

- Never invents a closed deal or a GCI number Bryce didn't give you.
- If the 90-day window has expired, say so and ask if he wants to start a new period
  rather than silently rolling it over.
- The dashboard (`dashboard.html`) reads this same file to show a running progress bar
  — re-run `python3 scripts/dashboard.py` after logging to see it update there.
