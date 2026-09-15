---
name: comp-analyzer
description: Takes comps and deal numbers Bryce already pulled and does the math — property value from closed comps, and investment deal analysis against his 15% ROI / $30K profit bar. Use when Bryce says things like "run these comps," "analyze this deal," or pastes in comp/deal numbers.
---

# Comp & Deal Analyzer

Read `CLAUDE.md` first, always. This skill exists because running comps and analyzing
deals by hand is the task that drains Bryce most — the job here is to do the math fast
and hand back a clean answer, not to replace his judgment on the deal itself.

**This skill never pulls data on its own.** Bryce feeds it comps or deal numbers he
already gathered from the MLS. If he hasn't given enough to work with, ask for what's
missing — don't guess at numbers.

---

## Mode 1: Just valuing a property (comps only)

Ask for (if not already given): the subject property, and for each comp — address,
close price, close date, and square footage (bed/bath/lot if he has it).

Do the math:
- Price per square foot for each comp
- Average and median close price across the comps
- Average and median $/sqft, applied to the subject's square footage
- Flag anything that looks like an outlier (a comp far outside the range of the others)
  rather than silently averaging it in

Bryce's comp window, in order: **6 months first. If that's not enough data, go to 12
months. If 12 months still isn't enough, go to 24 months** — that last step only
happens in worst-case scenarios where the immediate area just isn't turning over.

Hand back a value **range**, not a single number — that's how Bryce actually uses this
with clients. Keep the output short: the range, the math behind it, and anything he
should double check (e.g. "only 2 comps under 6 months, one 11-month comp included to
hit 3"). If none of the comps he gave you fall inside 12 months, flag it plainly and
say he's effectively in the 24-month worst-case tier — that's a signal to double check
nothing more recent closed before taking a number to a client.

## Mode 2: Investment deal analysis

Ask for whatever's missing from: current value (or purchase price), after repair value
(ARV) — from Mode 1 if he hasn't already run comps — estimated repair costs, taxes,
holding costs (utilities, insurance, etc.), and all closing costs (both sides if he has
them).

Do the math:
- Total investment = purchase price + repair costs + holding costs + closing costs
- Profit = ARV − total investment
- ROI = profit / total investment

Bryce's bar: **a good deal clears at least 15% ROI OR $30,000 in profit** (either one is
enough — it doesn't have to hit both).

Give a clear verdict up top — **"Good deal"** or **"Pass"** — with the numbers that got
it there, so he can see the math, not just trust the label. If it's close, say so
("just under the bar at 13% ROI / $27K profit") instead of a flat pass/fail.

---

## Tone

Direct, no-BS, straight to the numbers — this is a working tool, not a report. No filler,
no hedging language. Match how Bryce talks (see `CLAUDE.md` → How I sound).

## Rules

- Never presents a verdict as final — it's Bryce's call, this just does the arithmetic
  and applies his own stated bar.
- Never invents comps or numbers he didn't provide.
- Nothing here drafts anything client-facing — that's a different job. This skill's
  output is for Bryce, to make the decision, not to send.

## Saving the result (for the dashboard)

Once a run is complete (not a partial/in-progress one still waiting on missing info),
save it as a JSON file in `reports/comps/`, named `YYYY-MM-DD-<short-slug-of-address>.json`.
This is what `dashboard.html` reads to show Bryce his results in one place instead of
scrolling chat history — after saving, mention he can run `python3 scripts/dashboard.py`
(or just ask to "update my dashboard") to see it there.

Shape of the file:

```json
{
  "id": "YYYY-MM-DD-short-slug",
  "timestamp": "YYYY-MM-DDTHH:MM:SS",
  "type": "valuation",           // or "deal"
  "subject": "full subject address",
  "subject_details": "SF, condition, bed/bath — whatever's known",
  "range_low": 0,                 // valuation mode
  "range_high": 0,                // valuation mode
  "verdict": null,                // deal mode: "Good deal" or "Pass", else null
  "recommended_list_price": "129,900-132,900",  // optional, valuation mode
  "comps": [
    {"address": "", "closed": "YYYY-MM-DD", "sold_price": 0, "sqft": 0, "price_per_sqft": 0.0, "days_on_market": 0}
  ],
  "flags": ["anything Bryce should double check"],
  "notes": "short free-text takeaway"
}
```

For deal mode, it's fine to omit `range_low`/`range_high`/`comps` if the deal came in as
raw numbers rather than through Mode 1 — just fill in `verdict` and whatever inputs went
into the math in `notes`.
