"""Compute Sprint burndown (SWP + hours) from the daily log and render a static SVG chart
plus a Markdown table. SWP burns only when an Issue is Done; hours burn per finished
issue-without-subs or sub-issue.

Usage: python scripts/burndown-chart-svg.py backlog/backlog-scored.json backlog/sprint-1-daily-log.json \
          --svg reports/burndown-sprint-1.svg --md reports/burndown-sprint-1-table.md
"""
import argparse
import json

W, H, PAD_L, PAD_R, PAD_T, PAD_B = 760, 360, 56, 150, 40, 56
SURFACE, INK, INK2, GRID, ACTUAL = "#fcfcfb", "#0b0b0b", "#52514e", "#e4e3df", "#2a78d6"


def compute(scored, log):
    sprint = log["sprint"]
    issues = [i for i in scored["issues"] if i.get("sprint") == sprint]
    swp_of = {i["key"]: i["swp"] for i in issues}
    hours_of = {}
    for i in issues:
        if i["subIssues"]:
            for n, s in enumerate(i["subIssues"], 1):
                hours_of[f"{i['key']}.{n}"] = s["hours"]
        else:
            hours_of[i["key"]] = i["hours"]
    swp, hrs = sum(swp_of.values()), sum(hours_of.values())
    n = len(log["days"])
    rows = []
    for d, day in enumerate(log["days"]):
        swp -= sum(swp_of.get(k, 0) for k in day["done"])
        hrs -= sum(hours_of.get(k, 0) for k in day["done"])
        ideal = round(sum(swp_of.values()) * (n - 1 - d) / (n - 1), 1)
        rows.append({"date": day["date"], "ideal": ideal, "swp": swp, "hours": hrs,
                     "done": day["done"], "note": day["note"]})
    return sum(swp_of.values()), sum(hours_of.values()), rows


def svg(total, rows):
    pw, ph = W - PAD_L - PAD_R, H - PAD_T - PAD_B
    x = lambda i: PAD_L + pw * i / (len(rows) - 1)
    y = lambda v: PAD_T + ph * (1 - v / total)
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
           f'font-family="system-ui,Segoe UI,sans-serif" role="img" aria-label="Burndown Sprint 1 theo SWP">',
           f'<rect width="{W}" height="{H}" fill="{SURFACE}"/>',
           f'<text x="{PAD_L}" y="24" font-size="15" font-weight="600" fill="{INK}">Burndown Sprint 1 (16–27/11/2026) — SWP còn lại</text>']
    for v in range(0, total + 1, 10):
        out.append(f'<line x1="{PAD_L}" x2="{PAD_L + pw}" y1="{y(v):.1f}" y2="{y(v):.1f}" stroke="{GRID}" stroke-width="1"/>')
        out.append(f'<text x="{PAD_L - 8}" y="{y(v) + 4:.1f}" font-size="11" text-anchor="end" fill="{INK2}">{v}</text>')
    for i, r in enumerate(rows):
        out.append(f'<text x="{x(i):.1f}" y="{H - PAD_B + 18}" font-size="11" text-anchor="middle" fill="{INK2}">{r["date"][5:]}</text>')
    ideal = " ".join(f"{x(i):.1f},{y(r['ideal']):.1f}" for i, r in enumerate(rows))
    actual = " ".join(f"{x(i):.1f},{y(r['swp']):.1f}" for i, r in enumerate(rows))
    out.append(f'<polyline points="{ideal}" fill="none" stroke="{INK2}" stroke-width="2" stroke-dasharray="6 5"/>')
    out.append(f'<polyline points="{actual}" fill="none" stroke="{ACTUAL}" stroke-width="2" stroke-linejoin="round"/>')
    for i, r in enumerate(rows):
        out.append(f'<circle cx="{x(i):.1f}" cy="{y(r["swp"]):.1f}" r="4" fill="{ACTUAL}" stroke="{SURFACE}" stroke-width="2">'
                   f'<title>{r["date"]}: còn {r["swp"]} SWP, {r["hours"]} giờ</title></circle>')
    last = rows[-1]
    lx = PAD_L + pw + 10
    out.append(f'<text x="{lx}" y="{y(last["swp"]) + 4:.1f}" font-size="12" fill="{INK}">Thực tế: còn {last["swp"]} SWP</text>')
    out.append(f'<text x="{lx}" y="{y(0) + 4:.1f}" font-size="12" fill="{INK2}">Lý tưởng: 0</text>')
    out.append(f'<text x="{PAD_L}" y="{H - 12}" font-size="11" fill="{INK2}">SWP chỉ giảm khi issue Done '
               f'(issue In Review/In Progress chưa tính). Trục ngang: ngày làm việc.</text>')
    out.append("</svg>")
    return "\n".join(out)


def table(total, hours, rows):
    lines = ["| Ngày | SWP lý tưởng | SWP còn lại | Giờ còn lại | Hoàn thành trong ngày | Ghi chú |",
             "|---|---:|---:|---:|---|---|"]
    for r in rows:
        lines.append(f"| {r['date']} | {r['ideal']} | {r['swp']} | {r['hours']} | {', '.join(r['done']) or '—'} | {r['note'] or ''} |")
    lines.append(f"\nCam kết: {total} SWP / {hours} giờ.")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("scored")
    ap.add_argument("log")
    ap.add_argument("--svg", required=True)
    ap.add_argument("--md", required=True)
    a = ap.parse_args()
    with open(a.scored, encoding="utf-8") as fh:
        scored = json.load(fh)
    with open(a.log, encoding="utf-8") as fh:
        log = json.load(fh)
    total, hours, rows = compute(scored, log)
    with open(a.svg, "w", encoding="utf-8") as fh:
        fh.write(svg(total, rows))
    with open(a.md, "w", encoding="utf-8") as fh:
        fh.write(table(total, hours, rows))
    print(f"total={total} hours={hours} end_swp={rows[-1]['swp']} end_hours={rows[-1]['hours']}")


if __name__ == "__main__":
    main()
