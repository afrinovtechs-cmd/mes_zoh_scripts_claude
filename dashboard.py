import pathlib, re, webbrowser
from datetime import date

COLORS = {"FAIL": "#ef4444", "WATCH": "#f59e0b", "PASS": "#22c55e"}

def _parse_verdicts() -> list:
    rows = []
    text = (pathlib.Path(__file__).parent / "verdicts.md").read_text()
    for line in text.splitlines():
        # Format: | Ticker | Company | Country | Moat | Mgmt | Price | Circle | **VERDICT** | Confidence |
        m = re.match(
            r'\|\s*(\S+)\s*\|([^|]+)\|[^|]+\|([^|]+)\|([^|]+)\|([^|]+)\|[^|]+\|\s*\*\*(PASS|FAIL|WATCH)\*\*',
            line
        )
        if m:
            rows.append({
                "ticker":  m.group(1),
                "company": m.group(2).strip(),
                "moat":    m.group(3).strip(),
                "mgmt":    m.group(4).strip(),
                "price":   m.group(5).strip(),
                "verdict": m.group(6),
            })
    return rows

def _card(r: dict) -> str:
    c = COLORS[r["verdict"]]
    reason = f"Moat: {r['moat']} | Mgmt: {r['mgmt']} | Price: {r['price']}"
    return (f'<div class="card"><div class="ticker">{r["ticker"]}</div>'
            f'<span class="pill" style="background:{c}">{r["verdict"]}</span>'
            f'<p class="reason">{reason}</p>'
            f'<a href="reports/{r["ticker"]}.md">Read full report →</a></div>')

def generate_and_open():
    rows = _parse_verdicts()
    groups: dict = {"FAIL": [], "WATCH": [], "PASS": []}
    for r in rows:
        groups[r["verdict"]].append(r)

    cols = ""
    for v in ["FAIL", "WATCH", "PASS"]:
        cards = "".join(_card(r) for r in groups[v])
        n = len(groups[v])
        cols += (f'<div class="col">'
                 f'<h3 style="color:{COLORS[v]};border-bottom:3px solid {COLORS[v]};padding-bottom:6px">'
                 f'{v} ({n})</h3>{cards}</div>')

    html = f"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">
<title>Buffett Audit {date.today()}</title>
<style>
  *{{box-sizing:border-box}}body{{font-family:-apple-system,sans-serif;background:#f1f5f9;padding:24px;margin:0}}
  h1{{color:#0f172a;margin-bottom:4px}}p.sub{{color:#64748b;margin:0 0 24px}}
  .cols{{display:flex;gap:16px;align-items:flex-start}}
  .col{{flex:1;background:#fff;border-radius:10px;padding:16px;box-shadow:0 1px 3px rgba(0,0,0,.1)}}
  h3{{margin:0 0 12px;font-size:1em;text-transform:uppercase;letter-spacing:.05em}}
  .card{{border:1px solid #e2e8f0;border-radius:8px;padding:12px;margin:8px 0}}
  .ticker{{font-size:1.6em;font-weight:700;color:#0f172a;line-height:1}}
  .pill{{display:inline-block;margin:6px 0;padding:3px 10px;border-radius:99px;color:#fff;font-size:.75em;font-weight:700}}
  .reason{{font-size:.78em;color:#475569;margin:6px 0 8px}}
  a{{font-size:.78em;color:#3b82f6;text-decoration:none}}a:hover{{text-decoration:underline}}
</style></head>
<body>
<h1>Buffett Audit</h1><p class="sub">Generated {date.today()} · {len(rows)} tickers</p>
<div class="cols">{cols}</div>
</body></html>"""

    out = pathlib.Path(__file__).parent / "dashboard.html"
    out.write_text(html)
    webbrowser.open(str(out))
    return str(out)
