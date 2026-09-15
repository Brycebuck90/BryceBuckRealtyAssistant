#!/usr/bin/env python3
"""Builds dashboard.html from the JSON reports in reports/.

Read-only viewer. Doesn't touch email, doesn't send or delete anything —
it just turns saved skill output into one clean local webpage.

Run it any time with: python3 scripts/dashboard.py
Or just ask Claude to "update my dashboard."
"""
import json
import html
from pathlib import Path
from datetime import datetime

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
    records.sort(key=lambda r: r.get("timestamp", ""), reverse=True)
    return records


def money(n):
    if n is None:
        return "-"
    return f"${n:,.0f}"


def comp_card(r):
    subject = html.escape(r.get("subject", "Unknown property"))
    details = html.escape(r.get("subject_details", ""))
    kind = r.get("type", "valuation")
    badge = "Deal Analysis" if kind == "deal" else "Valuation"

    if kind == "deal" and r.get("verdict"):
        headline = html.escape(r["verdict"])
        headline_class = "verdict-good" if "good" in r["verdict"].lower() else "verdict-pass"
    else:
        lo, hi = r.get("range_low"), r.get("range_high")
        headline = f"{money(lo)} - {money(hi)}"
        headline_class = "verdict-range"

    comps_rows = ""
    for c in r.get("comps", []):
        comps_rows += f"""
        <tr>
          <td>{html.escape(c.get('address', ''))}</td>
          <td>{html.escape(c.get('closed', ''))}</td>
          <td>{money(c.get('sold_price'))}</td>
          <td>{c.get('sqft', '-')}</td>
          <td>${c.get('price_per_sqft', 0):,.2f}</td>
          <td>{c.get('days_on_market', '-')}</td>
        </tr>"""

    comps_table = ""
    if comps_rows:
        comps_table = f"""
        <div class="table-scroll">
        <table class="comps-table">
          <thead>
            <tr><th>Comp</th><th>Closed</th><th>Sold Price</th><th>SF</th><th>$/SF</th><th>DOM</th></tr>
          </thead>
          <tbody>{comps_rows}</tbody>
        </table>
        </div>"""

    flags_html = ""
    flags = r.get("flags") or []
    if flags:
        items = "".join(f"<li>{html.escape(f)}</li>" for f in flags)
        flags_html = f'<ul class="flags">{items}</ul>'

    notes = r.get("notes", "")
    notes_html = f'<p class="notes">{html.escape(notes)}</p>' if notes else ""

    rec_price = r.get("recommended_list_price")
    rec_html = f'<p class="rec-price">Recommended list: <strong>${html.escape(str(rec_price))}</strong></p>' if rec_price else ""

    ts = r.get("timestamp", "")
    try:
        date_str = datetime.fromisoformat(ts).strftime("%b %d, %Y")
    except ValueError:
        date_str = ts

    return f"""
    <article class="card">
      <div class="card-head">
        <span class="badge">{badge}</span>
        <span class="date">{html.escape(date_str)}</span>
      </div>
      <h2>{subject}</h2>
      {f'<p class="details">{details}</p>' if details else ''}
      <p class="headline {headline_class}">{headline}</p>
      {rec_html}
      {notes_html}
      {flags_html}
      {comps_table}
    </article>"""


def build():
    comp_reports = load_reports("comps")
    cards_html = "".join(comp_card(r) for r in comp_reports)
    if not cards_html:
        cards_html = '<p class="empty">No comp runs saved yet. Run the comp-analyzer skill and it\'ll show up here.</p>'

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
  .card {{
    background: var(--card-bg);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 20px 24px;
    margin-bottom: 20px;
  }}
  .card-head {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 10px;
  }}
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
  .date {{ color: var(--muted); font-size: 0.85rem; }}
  h2 {{ font-size: 1.15rem; margin: 0 0 4px; }}
  .details {{ color: var(--muted); margin: 0 0 12px; font-size: 0.9rem; }}
  .headline {{ font-size: 1.4rem; font-weight: 700; margin: 8px 0; }}
  .verdict-range {{ color: var(--accent); }}
  .verdict-good {{ color: #1a7a3c; }}
  .verdict-pass {{ color: #b3391a; }}
  .rec-price {{ margin: 4px 0 12px; font-size: 0.92rem; }}
  .notes {{ font-size: 0.9rem; color: var(--muted); margin: 8px 0; }}
  .flags {{
    background: var(--warn-bg);
    color: var(--warn-text);
    border-radius: 8px;
    padding: 12px 16px 12px 32px;
    font-size: 0.85rem;
    margin: 12px 0;
  }}
  .flags li {{ margin-bottom: 6px; }}
  .flags li:last-child {{ margin-bottom: 0; }}
  .table-scroll {{
    overflow-x: auto;
    margin-top: 12px;
  }}
  .comps-table {{
    width: 100%;
    border-collapse: collapse;
    font-size: 0.85rem;
  }}
  .comps-table th, .comps-table td {{
    text-align: left;
    padding: 6px 10px;
    border-bottom: 1px solid var(--border);
    white-space: nowrap;
  }}
  .comps-table th {{ color: var(--muted); font-weight: 600; }}
  .empty {{ color: var(--muted); text-align: center; padding: 40px 0; }}
</style>
</head>
<body>
  <div class="wrap">
    <h1>Your Dashboard</h1>
    <p class="subtitle">Read-only. Nothing here was sent or changed — just what the skills have already worked out for you.</p>
    {cards_html}
  </div>
</body>
</html>"""

    OUTPUT.write_text(page)
    print(f"Wrote {OUTPUT} ({len(comp_reports)} comp report(s))")


if __name__ == "__main__":
    build()
