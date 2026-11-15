"""Markdown table builders used by render-doc-tables.py. Every number comes from
backlog-scored.json / lab1-estimate.json so the docs cannot drift from the Project."""

FOCUS_HOURS_PER_DAY = 6  # same capacity basis as sprint planning (PREMISE A-01)
LAB1_HOURS_PER_MD = 8


def _epic_issues(data, ek):
    return [i for i in data["issues"] if i["epic"] == ek]


def epic_map(data):
    rows = ["| Spec (mã/file LAB-4, dòng PREMISE) | Epic trên Project | Ghi chú |", "|---|---|---|"]
    for ep in data["epics"]:
        note = ("⚠ Ràng buộc đặc thù: giới hạn giờ lái xe tải 2024 (改善基準告示) — tách epic riêng"
                if ep.get("constraint") else f"Feature {ep['feature']}")
        rows.append(f"| {ep['spec']} | #{{{ep['key']}}} — {ep['title']} | {note} |")
    return "\n".join(rows)


def spec_to_issue(data):
    rows = ["| Spec | Epic | Issue / sub-issue | Phần spec chưa thành issue và vì sao |", "|---|---|---|---|"]
    for ep in data["epics"]:
        its = _epic_issues(data, ep["key"])
        cells = "<br>".join(f"#{{{i['key']}}} {i['spec']}" + (f" ({len(i['subIssues'])} sub)" if i["subIssues"] else "")
                            for i in its)
        rows.append(f"| {ep['spec']} | #{{{ep['key']}}} | {cells} | {ep['notIssued']} |")
    return "\n".join(rows)


def epic_totals(data):
    rows = ["| Epic | Số issue | Số sub-issue | Tổng SWP | Tổng giờ | Ghi chú |", "|---|---:|---:|---:|---:|---|"]
    t = [0, 0, 0, 0]
    for ep in data["epics"]:
        its = _epic_issues(data, ep["key"])
        n, ns = len(its), sum(len(i["subIssues"]) for i in its)
        swp, hrs = sum(i["swp"] for i in its), sum(i["hours"] for i in its)
        legal = sum(1 for i in its if i.get("legal"))
        stub = sum(1 for i in its if i.get("oqMode") in ("STUB", "BLOCK"))
        nd = sum(1 for i in its if i.get("needsDesign") or i.get("type") == "design")
        bits = [f"{legal} issue +1 pháp lý" if legal else "", f"{stub} STUB/BLOCK (k=1.25)" if stub else "",
                f"{nd} chờ spec/thiết kế" if nd else ""]
        rows.append(f"| #{{{ep['key']}}} {ep['title']} | {n} | {ns} | {swp} | {hrs} | {'; '.join(b for b in bits if b) or '—'} |")
        t = [t[0] + n, t[1] + ns, t[2] + swp, t[3] + hrs]
    rows.append(f"| **Tổng** | **{t[0]}** | **{t[1]}** | **{t[2]}** | **{t[3]}** | |")
    return "\n".join(rows)


def lab1_compare(data, lab1):
    cover = {}
    for i in data["issues"]:
        for f in i["lab1"].split(","):
            cover.setdefault(f, set()).add(i["epic"])
    rows = ["| Phần (epic) | LAB-1 (MD) | LAB-5 (giờ → MD @6h) | Chênh | Vì sao |", "|---|---:|---:|---:|---|"]
    tot1 = tot5 = 0
    for ep in data["epics"]:
        md1 = sum(lab1["features"][f] / len(es) for f, es in cover.items() if ep["key"] in es and f != "PLATFORM")
        if ep["key"] == "E01":
            md1 += lab1["platformSetupMd"]
        hrs = sum(i["hours"] for i in _epic_issues(data, ep["key"]))
        md5 = hrs / FOCUS_HOURS_PER_DAY
        tot1, tot5 = tot1 + md1, tot5 + md5
        rows.append(f"| {ep['key']} {ep['title']} | {md1:.1f} | {hrs} → {md5:.1f} | {(md5 - md1) / md1 * 100:+.0f}% | {ep['lab1Why']} |")
    rows.append(f"| **Tổng build (FE+BE+UT)** | **{tot1:.0f}** | **{tot5:.0f}** | **{(tot5 - tot1) / tot1 * 100:+.0f}%** | "
                "Xem giải thích dưới bảng |")
    return "\n".join(rows)


def samples(data):
    rows = ["| Issue | Lý do skill chọn | Skill chấm (Scope × Complexity → SWP) | Bạn chốt | Lý do |", "|---|---|---|---|---|"]
    for i in data["issues"]:
        if not i["sampleReason"]:
            continue
        legal = " (+1 pháp lý)" if i.get("legal") else ""
        c_eff = min(5, (i["reviewC"] or i["C"]) + (1 if i.get("legal") else 0))  # same basis as skill column
        decided = (f"**S{i['reviewS'] or i['S']} × C{c_eff}{legal} → {i['swp']}**"
                   if i["swp"] != i["swpSkill"] else f"Giữ {i['swp']}")
        rows.append(f"| #{{{i['key']}}} {i['title']} | {i['sampleReason']} | S{i['S']} × C{i['cEff']}{legal} → {i['swpSkill']} "
                    f"| {decided} | {i['reviewNote']} |")
    return "\n".join(rows)


def timesheet(it):
    """(actual, remaining) of an issue: own values or the sum over its sub-issues."""
    subs = it["subIssues"]
    if subs:
        done = it["status"] == "Done"
        act = sum(s.get("actual", 0) for s in subs)
        rem = sum(s.get("remaining", 0 if (done or s.get("status") == "Done") else s["hours"]) for s in subs)
        return act, rem
    return it.get("actual", 0), it.get("remaining", 0 if it["status"] == "Done" else it["hours"])


def status_sprint(data, sprint=1):
    order = ["Done", "In Review", "In Progress", "Blocked", "Todo"]
    rows = ["| Trạng thái | Số issue | Tổng SWP | Giờ ước | Giờ thực tế | Còn lại (ước lại) | Ghi chú |",
            "|---|---:|---:|---:|---:|---:|---|"]
    its = [i for i in data["issues"] if i.get("sprint") == sprint]
    tot = [0, 0]
    for st in order:
        group = [i for i in its if i["status"] == st]
        if not group:
            continue
        ts = [timesheet(i) for i in group]
        act, rem = sum(t[0] for t in ts), sum(t[1] for t in ts)
        tot = [tot[0] + act, tot[1] + rem]
        keys = ", ".join(f"#{{{i['key']}}}" for i in group)
        rows.append(f"| {st} | {len(group)} | {sum(i['swp'] for i in group)} | {sum(i['hours'] for i in group)} "
                    f"| {act} | {rem} | {keys} |")
    rows.append(f"| **Cam kết** | **{len(its)}** | **{sum(i['swp'] for i in its)}** | **{sum(i['hours'] for i in its)}** "
                f"| **{tot[0]}** | **{tot[1]}** | |")
    return "\n".join(rows)
