#!/usr/bin/env python3
"""Builds dashboard.html from the JSON reports in reports/.

Read-only viewer. Doesn't touch email, doesn't send or delete anything —
it just turns saved skill output into one clean local webpage, ordered
around running an efficient day: email triage, follow-ups going cold,
goal progress, then comp/deal runs.

Run it any time with: python3 scripts/dashboard.py
Or just ask Claude to "update my dashboard."
"""
import json
import html
from pathlib import Path
from datetime import datetime, date

ROOT = Path(__file__).resolve().parent.parent
REPORTS = ROOT / "reports"
OUTPUT = ROOT / "dashboard.html"


def load_reports(subfolder):
    folder = REPORTS / subfolder
    if not folder.exists():
        return []
    records = []
    for path in sorted(folder.glob("*.json")):
        try:
            records.append(json.loads(path.read_text()))
        except (json.JSONDecodeError, OSError):
            continue
    return records


def money(n):
    if n is None:
        return "-"
    return f"${n:,.0f}"


def esc(s):
    return html.escape(str(s)) if s is not None else ""


# ---------------------------------------------------------------- email ----

def build_email_section():
    reports = load_reports("email")
    if not reports:
        return """
    <section class="block">
      <div class="block-head"><h2>Email Triage</h2></div>
      <p class="empty">No sweep run yet. Say "audit my email" and it'll show up here.</p>
    </section>"""

    reports.sort(key=lambda r: r.get("date", ""), reverse=True)
    latest = reports[0]
    date_str = esc(latest.get("date", ""))
    days = latest.get("days_covered", 7)

    money_items = latest.get("money", [])
    worth_items = latest.get("worth_your_time", [])
    noise_count = latest.get("noise_count", 0)

    oldest_flag = ""
    if money_items:
        oldest = max((m.get("days_ago") or 0) for m in money_items)
        if oldest >= 3:
            oldest_flag = f'<p class="callout">Oldest money item has been sitting {oldest} day(s). That\'s the one to hit first.</p>'

    money_rows = ""
    for m in money_items:
        money_rows += f"""
        <div class="item item-money">
          <div class="item-top">
            <strong>{esc(m.get('from'))}</strong>
            <span class="age">{esc(m.get('days_ago'))}d ago</span>
          </div>
          <div class="item-subject">{esc(m.get('subject'))}</div>
          <div class="item-why">{esc(m.get('why'))}</div>
          {f'<div class="item-draft">Draft ready: {esc(m.get("draft_path"))}</div>' if m.get('draft_path') else ''}
        </div>"""

    worth_rows = ""
    for w in worth_items:
        worth_rows += f"""
        <div class="item">
          <div class="item-top">
            <strong>{esc(w.get('from'))}</strong>
            <span class="age">{esc(w.get('days_ago'))}d ago</span>
          </div>
          <div class="item-subject">{esc(w.get('subject'))}</div>
        </div>"""

    return f"""
    <section class="block">
      <div class="block-head">
        <h2>Email Triage</h2>
        <span class="date">{date_str} · last {days} days</span>
      </div>
      {oldest_flag}
      {f'<h3 class="subhead">Money ({len(money_items)})</h3>{money_rows}' if money_items else '<p class="empty-inline">Nothing money-shaped in this sweep.</p>'}
      {f'<h3 class="subhead">Worth your time ({len(worth_items)})</h3>{worth_rows}' if worth_items else ''}
      <p class="noise-count">{noise_count} noise item(s) filtered out.</p>
    </section>"""


# ------------------------------------------------------------ follow-ups ----

def build_followups_section():
    contacts = load_reports("followups")
    if not contacts:
        return """
    <section class="block">
      <div class="block-head"><h2>Follow-Ups</h2></div>
      <p class="empty">No contacts logged yet. Say "I talked to [name] today" and they'll show up here.</p>
    </section>"""

    today = date.today()
    enriched = []
    for c in contacts:
        try:
            last = datetime.fromisoformat(c.get("last_contact", "")).date()
            days_since = (today - last).days
        except ValueError:
            days_since = None
        enriched.append((days_since, c))

    enriched.sort(key=lambda pair: (pair[0] is None, -(pair[0] or 0)), reverse=True)
    enriched.sort(key=lambda pair: (pair[0] is None, pair[0] or 0), reverse=True)

    rows = ""
    for days_since, c in enriched:
        if days_since is None:
            status, cls = "unknown", "status-fine"
        elif days_since >= 14:
            status, cls = "cold", "status-cold"
        elif days_since >= 7:
            status, cls = "due", "status-due"
        else:
            status, cls = "fine", "status-fine"

        days_label = f"{days_since}d" if days_since is not None else "-"
        rows += f"""
        <div class="item">
          <div class="item-top">
            <strong>{esc(c.get('name'))}</strong>
            <span class="status-chip {cls}">{status} · {days_label}</span>
          </div>
          {f'<div class="item-why">{esc(c.get("context"))}</div>' if c.get('context') else ''}
          {f'<div class="item-draft">Next: {esc(c.get("next_step"))}</div>' if c.get('next_step') else ''}
        </div>"""

    return f"""
    <section class="block">
      <div class="block-head"><h2>Follow-Ups</h2></div>
      {rows}
    </section>"""


# ---------------------------------------------------------------- goals ----

def build_goal_section():
    path = REPORTS / "goals" / "progress.json"
    if not path.exists():
        return """
    <section class="block">
      <div class="block-head"><h2>90-Day Goal</h2></div>
      <p class="empty">Not tracking a goal yet. Say "log a closed deal" and it'll set one up from your Business Brain.</p>
    </section>"""

    try:
        g = json.loads(path.read_text())
    except (json.JSONDecodeError, OSError):
        return ""

    target_deals = g.get("target_deals", 0) or 1
    target_gci = g.get("target_gci", 0) or 1
    deals = g.get("deals_closed", 0)
    gci = g.get("gci_earned", 0)

    deals_pct = min(100, round(100 * deals / target_deals))
    gci_pct = min(100, round(100 * gci / target_gci))

    days_left = ""
    try:
        start = datetime.fromisoformat(g.get("period_start", "")).date()
        end_day = (start - date.today()).days + g.get("period_days", 90)
        days_left = f"{max(0, (start.toordinal() + g.get('period_days', 90)) - date.today().toordinal())} days left"
    except (ValueError, TypeError):
        days_left = ""

    return f"""
    <section class="block">
      <div class="block-head">
        <h2>90-Day Goal</h2>
        <span class="date">{esc(days_left)}</span>
      </div>
      <div class="goal-row">
        <div class="goal-label">Deals: {deals} of {target_deals}</div>
        <div class="progress-bar"><div class="progress-fill" style="width:{deals_pct}%"></div></div>
      </div>
      <div class="goal-row">
        <div class="goal-label">GCI: {money(gci)} of {money(target_gci)}</div>
        <div class="progress-bar"><div class="progress-fill" style="width:{gci_pct}%"></div></div>
      </div>
    </section>"""


# ----------------------------------------------------------------- comps ----

def comp_card(r):
    subject = esc(r.get("subject", "Unknown property"))
    details = esc(r.get("subject_details", ""))
    kind = r.get("type", "valuation")
    badge = "Deal Analysis" if kind == "deal" else "Valuation"

    if kind == "deal" and r.get("verdict"):
        headline = esc(r["verdict"])
        headline_class = "verdict-good" if "good" in r["verdict"].lower() else "verdict-pass"
    else:
        lo, hi = r.get("range_low"), r.get("range_high")
        headline = f"{money(lo)} - {money(hi)}"
        headline_class = "verdict-range"

    ts = r.get("timestamp", "")
    try:
        date_str = datetime.fromisoformat(ts).strftime("%b %d, %Y")
    except ValueError:
        date_str = ts

    return f"""
    <div class="comp-card">
      <div class="card-head">
        <span class="badge">{badge}</span>
        <span class="date">{esc(date_str)}</span>
      </div>
      <h3>{subject}</h3>
      {f'<p class="details">{details}</p>' if details else ''}
      <p class="headline {headline_class}">{headline}</p>
    </div>"""


def build_comps_section():
    reports = load_reports("comps")
    reports.sort(key=lambda r: r.get("timestamp", ""), reverse=True)
    if not reports:
        return """
    <section class="block block-secondary">
      <div class="block-head"><h2>Recent Comp &amp; Deal Runs</h2></div>
      <p class="empty">No comp runs saved yet.</p>
    </section>"""

    cards = "".join(comp_card(r) for r in reports[:6])
    return f"""
    <section class="block block-secondary">
      <div class="block-head"><h2>Recent Comp &amp; Deal Runs</h2></div>
      <div class="comp-grid">{cards}</div>
    </section>"""


# ------------------------------------------------------------------ page ----

def build():
    sections = (
        build_email_section()
        + build_followups_section()
        + build_goal_section()
        + build_comps_section()
    )

    page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Bryce Buck Realty — Dashboard</title>
<style>
  :root {{
    color-scheme: light dark;
    --bg: #f7f6f3;
    --card-bg: #ffffff;
    --text: #1c1c1c;
    --muted: #6b6b6b;
    --border: #e5e2db;
    --accent: #1f4d3d;
    --accent-bg: #e8f0ec;
    --warn-bg: #fdf3e0;
    --warn-text: #7a5a00;
    --cold-bg: #fbe4e0;
    --cold-text: #a13a24;
    --due-bg: #fdf3e0;
    --due-text: #8a6100;
    --fine-bg: #e8f0ec;
    --fine-text: #1f4d3d;
  }}
  @media (prefers-color-scheme: dark) {{
    :root {{
      --bg: #15171a;
      --card-bg: #1e2124;
      --text: #ececec;
      --muted: #9a9a9a;
      --border: #2c2f33;
      --accent: #7fd9b9;
      --accent-bg: #1c332a;
      --warn-bg: #332a12;
      --warn-text: #e0c069;
      --cold-bg: #3a2018;
      --cold-text: #f0a58c;
      --due-bg: #332a12;
      --due-text: #e0c069;
      --fine-bg: #1c332a;
      --fine-text: #7fd9b9;
    }}
  }}
  * {{ box-sizing: border-box; }}
  body {{
    margin: 0;
    padding: 32px 20px 60px;
    background: var(--bg);
    color: var(--text);
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
  }}
  .wrap {{ max-width: 900px; margin: 0 auto; }}
  h1 {{ font-size: 1.6rem; margin: 0 0 4px; }}
  .subtitle {{ color: var(--muted); margin: 0 0 32px; font-size: 0.95rem; }}
  .block {{
    background: var(--card-bg);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 20px 24px;
    margin-bottom: 20px;
  }}
  .block-secondary {{ opacity: 0.92; }}
  .block-head {{
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    margin-bottom: 10px;
    flex-wrap: wrap;
    gap: 4px;
  }}
  .block-head h2 {{ font-size: 1.15rem; margin: 0; }}
  .subhead {{ font-size: 0.9rem; color: var(--muted); margin: 16px 0 8px; text-transform: uppercase; letter-spacing: 0.03em; }}
  .date {{ color: var(--muted); font-size: 0.85rem; }}
  .badge {{
    background: var(--accent-bg);
    color: var(--accent);
    font-size: 0.75rem;
    font-weight: 600;
    padding: 3px 10px;
    border-radius: 999px;
    text-transform: uppercase;
    letter-spacing: 0.03em;
  }}
  .callout {{
    background: var(--warn-bg);
    color: var(--warn-text);
    border-radius: 8px;
    padding: 10px 16px;
    font-size: 0.88rem;
    margin: 8px 0 16px;
  }}
  .item {{
    border-top: 1px solid var(--border);
    padding: 10px 0;
  }}
  .item:first-of-type {{ border-top: none; }}
  .item-top {{ display: flex; justify-content: space-between; align-items: center; gap: 8px; }}
  .item-subject {{ font-size: 0.92rem; margin-top: 2px; }}
  .item-why {{ font-size: 0.85rem; color: var(--muted); margin-top: 4px; }}
  .item-draft {{ font-size: 0.8rem; color: var(--accent); margin-top: 4px; }}
  .age {{ font-size: 0.8rem; color: var(--muted); white-space: nowrap; }}
  .status-chip {{
    font-size: 0.75rem;
    font-weight: 600;
    padding: 2px 10px;
    border-radius: 999px;
    text-transform: uppercase;
    white-space: nowrap;
  }}
  .status-cold {{ background: var(--cold-bg); color: var(--cold-text); }}
  .status-due {{ background: var(--due-bg); color: var(--due-text); }}
  .status-fine {{ background: var(--fine-bg); color: var(--fine-text); }}
  .noise-count {{ font-size: 0.8rem; color: var(--muted); margin: 12px 0 0; }}
  .empty {{ color: var(--muted); padding: 8px 0; }}
  .empty-inline {{ color: var(--muted); font-size: 0.9rem; margin: 8px 0; }}
  .goal-row {{ margin: 14px 0; }}
  .goal-label {{ font-size: 0.92rem; margin-bottom: 6px; font-weight: 600; }}
  .progress-bar {{
    background: var(--border);
    border-radius: 999px;
    height: 10px;
    overflow: hidden;
  }}
  .progress-fill {{
    background: var(--accent);
    height: 100%;
    border-radius: 999px;
  }}
  .comp-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
    gap: 12px;
  }}
  .comp-card {{
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 14px 16px;
  }}
  .comp-card h3 {{ font-size: 0.95rem; margin: 4px 0; }}
  .comp-card .details {{ color: var(--muted); font-size: 0.82rem; margin: 0 0 8px; }}
  .headline {{ font-size: 1.1rem; font-weight: 700; margin: 4px 0 0; }}
  .verdict-range {{ color: var(--accent); }}
  .verdict-good {{ color: #1a7a3c; }}
  .verdict-pass {{ color: #b3391a; }}
</style>
</head>
<body>
  <div class="wrap">
    <h1>Your Dashboard</h1>
    <p class="subtitle">Read-only. Nothing here was sent or changed — just what the skills have already worked out for you.</p>
    {sections}
  </div>
</body>
</html>"""

    OUTPUT.write_text(page)
    print(f"Wrote {OUTPUT}")


if __name__ == "__main__":
    build()
