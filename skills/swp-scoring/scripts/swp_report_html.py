"""Render the SWP scoring result as a self-contained HTML report (no external assets)."""
from html import escape

CSS = """
:root{--bg:#fff;--fg:#1d2330;--mut:#5b6474;--line:#dde2ea;--head:#f3f5f9;--warn:#b3261e;--ok:#1b6e3a;--acc:#8a4b00;--chip:#fff4e5}
@media (prefers-color-scheme:dark){:root{--bg:#14171c;--fg:#e6e9ef;--mut:#9aa3b2;--line:#2c323c;--head:#1c2027;--warn:#ff8a80;--ok:#7dd3a0;--acc:#ffb74d;--chip:#2a2116}}
body{background:var(--bg);color:var(--fg);font:14px/1.5 system-ui,-apple-system,"Segoe UI","Noto Sans JP",sans-serif;margin:0;padding:24px 16px;max-width:1280px;margin-inline:auto}
h1{font-size:22px;margin:0 0 4px}h2{font-size:17px;margin:28px 0 8px}
p.mut,.mut{color:var(--mut)}
.wrap{overflow-x:auto;border:1px solid var(--line);border-radius:8px}
table{border-collapse:collapse;width:100%;font-size:13px}
th,td{border-bottom:1px solid var(--line);padding:6px 8px;text-align:left;vertical-align:top}
th{background:var(--head);position:sticky;top:0}
td.n{text-align:right;font-variant-numeric:tabular-nums}
.flag{color:var(--warn);font-weight:600}.chg{color:var(--acc);font-weight:600}.ok{color:var(--ok)}
.chip{background:var(--chip);border-radius:4px;padding:1px 6px;font-size:12px}
.kpi{display:flex;gap:12px;flex-wrap:wrap;margin:12px 0}
.kpi div{border:1px solid var(--line);border-radius:8px;padding:8px 14px}
.kpi b{display:block;font-size:20px}
"""


def _row(cells):
    return "<tr>" + "".join(cells) + "</tr>"


def _td(v, cls=""):
    return f'<td class="{cls}">{v}</td>' if cls else f"<td>{v}</td>"


def _issue_row(it):
    changed = it["swp"] != it["swpSkill"]
    swp_cls = "n chg" if changed else "n"
    flags = ", ".join(it["flags"])
    legal = '<span class="chip">+1 pháp lý</span>' if it.get("legal") else ""
    return _row([
        _td(escape(it["key"])), _td(escape(it["epic"])), _td(escape(it["title"])),
        _td(it["S"], "n"), _td(f'{it["C"]} → {it["cEff"]} {legal}' if it.get("legal") else it["C"], "n"),
        _td(it["swpSkill"], "n"), _td(it["swp"], swp_cls), _td(it["hours"], "n"),
        _td(escape(it.get("oqMode") or "—")), _td(escape(flags), "flag" if flags else ""),
    ])


def _sample_row(it):
    if it["reviewS"] or it["reviewC"]:
        c_eff = min(5, (it["reviewC"] or it["C"]) + (1 if it.get("legal") else 0))  # same basis as skill column
        decided = f'S{it["reviewS"] or it["S"]} × C{c_eff} → {it["swp"]}'
    else:
        decided = f'giữ {it["swp"]}'
    return _row([
        _td(escape(it["key"])), _td(escape(it["title"])), _td(escape(it["sampleReason"])),
        _td(f'S{it["S"]} × C{it["cEff"]} → {it["swpSkill"]}'), _td(decided, "chg" if it["swp"] != it["swpSkill"] else "ok"),
        _td(escape(it["reviewNote"] or "(chưa review)")),
    ])


def _epic_rows(data):
    rows = []
    for ep in data["epics"]:
        items = [i for i in data["issues"] if i["epic"] == ep["key"]]
        rows.append(_row([
            _td(escape(ep["key"])), _td(escape(ep["title"])), _td(len(items), "n"),
            _td(sum(i["swpSkill"] for i in items), "n"), _td(sum(i["swp"] for i in items), "n"),
            _td(sum(i["hours"] for i in items), "n"),
        ]))
    return "".join(rows)


def render_report(data):
    issues = data["issues"]
    samples = [i for i in issues if i["sampleReason"]]
    tot_skill = sum(i["swpSkill"] for i in issues)
    tot = sum(i["swp"] for i in issues)
    hours = sum(i["hours"] for i in issues)
    changed = sum(1 for i in issues if i["swp"] != i["swpSkill"])
    head = ("<tr><th>Issue</th><th>Epic</th><th>Tên</th><th>S</th><th>C</th><th>SWP skill</th>"
            "<th>SWP chốt</th><th>Giờ</th><th>OQ</th><th>Flag</th></tr>")
    return f"""<!doctype html><html lang="vi"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>SWP Report LAB-5</title><style>{CSS}</style></head><body>
<h1>Báo cáo chấm SWP — Product B backlog (LAB-5)</h1>
<p class="mut">Sinh bởi skill <code>skills/swp-scoring</code>. SWP = Fib(Scope × Complexity), +1 Complexity cho quy tắc pháp lý chưa xác minh.
Giờ = SWP × 4h × k (k = 1.25 nếu OQ ở STUB/BLOCK). Cột “SWP chốt” lấy từ <code>backlog/swp-review.json</code> (người review).</p>
<div class="kpi"><div>Issue<b>{len(issues)}</b></div><div>SWP skill<b>{tot_skill}</b></div><div>SWP chốt<b>{tot}</b></div>
<div>Giờ ước lượng<b>{hours}</b></div><div>Issue mẫu<b>{len(samples)}</b></div><div>Issue bị sửa điểm<b>{changed}</b></div></div>
<h2>1. Issue mẫu skill chọn để người review</h2>
<div class="wrap"><table><tr><th>Issue</th><th>Tên</th><th>Lý do chọn</th><th>Skill chấm</th><th>Chốt</th><th>Ghi chú review</th></tr>
{"".join(_sample_row(i) for i in samples)}</table></div>
<h2>2. Tổng theo epic</h2>
<div class="wrap"><table><tr><th>Epic</th><th>Tên</th><th>Số issue</th><th>SWP skill</th><th>SWP chốt</th><th>Giờ</th></tr>
{_epic_rows(data)}</table></div>
<h2>3. Toàn bộ issue</h2>
<div class="wrap"><table>{head}{"".join(_issue_row(i) for i in issues)}</table></div>
</body></html>"""
