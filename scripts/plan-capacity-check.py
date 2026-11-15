"""Check the sprint plan against owner capacity and dependencies; report estimate vs actual.

Capacity is in *estimate hours*: 6 focus h/day x 10 days, divided by the Sprint 1 actual/estimate
ratio of finished work (so a sprint is not planned on optimistic hours). Sprint 2 load includes the
re-estimated remaining hours of Sprint 1 carry-over.

Usage: python scripts/plan-capacity-check.py backlog/backlog-scored.json --md reports/plan-capacity-check.md
"""
import argparse
import json

CAP_ACTUAL = {"TL": 30, "BE1": 60, "BE2": 60, "BE3": 60, "FE1": 60, "QA1": 60, "BrSE": 20}


def units(it):
    """Work units of an issue: its sub-issues, or the issue itself."""
    if it["subIssues"]:
        return [dict(s, key=f"{it['key']}.{n}") for n, s in enumerate(it["subIssues"], 1)]
    st = it["status"]
    return [{"key": it["key"], "owner": it["owner"], "hours": it["hours"], "status": st,
             "actual": it.get("actual"), "remaining": it.get("remaining")}]


def unit_status(u, parent):
    return u.get("status") or ("Done" if parent["status"] == "Done" else "Todo")


def timesheet(data):
    rows, done_est, done_act = [], 0, 0
    for it in (i for i in data["issues"] if i.get("sprint") == 1):
        for u in units(it):
            st = unit_status(u, it)
            act = u.get("actual") or 0
            rem = u.get("remaining", 0 if st == "Done" else u["hours"])
            rem = u["hours"] if rem is None else rem
            if st == "Done":
                done_est, done_act = done_est + u["hours"], done_act + act
            rows.append((u["key"], u["owner"], st, u["hours"], act, rem))
    return rows, done_est, done_act


def load_by_owner(data, sprint, carry):
    load = {o: 0 for o in CAP_ACTUAL}
    for it in (i for i in data["issues"] if i.get("sprint") == sprint):
        for u in units(it):
            load[u["owner"]] += u["hours"]
    for owner, _, rem in carry:
        load[owner] += rem
    return load


def dep_problems(data):
    by = {i["key"]: i for i in data["issues"]}
    out = []
    for it in data["issues"]:
        sp = it.get("sprint")
        for d in it.get("deps", []):
            dsp = by[d].get("sprint")
            if sp and (dsp is None or dsp > sp):
                out.append(f"{it['key']} (Sprint {sp}) phụ thuộc {d} (Sprint {dsp or '—'})")
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("scored")
    ap.add_argument("--md", required=True)
    a = ap.parse_args()
    with open(a.scored, encoding="utf-8") as fh:
        data = json.load(fh)
    rows, done_est, done_act = timesheet(data)
    ratio = done_act / done_est
    cap = {o: round(c / ratio) for o, c in CAP_ACTUAL.items()}
    carry = [(o, k, rem) for k, o, st, _, _, rem in rows if st != "Done" and rem]
    md = ["### Giờ ước lượng và giờ thực tế Sprint 1 (theo đơn vị việc)", "",
          "| Việc | Phụ trách | Trạng thái | Ước lượng | Thực tế | Còn lại (ước lại) |", "|---|---|---|---:|---:|---:|"]
    for k, o, st, est, act, rem in rows:
        md.append(f"| {k} | {o} | {st} | {est} | {act} | {rem} |")
    tot = [sum(r[i] for r in rows) for i in (3, 4, 5)]
    md.append(f"| **Tổng** | | | **{tot[0]}** | **{tot[1]}** | **{tot[2]}** |")
    md += ["", f"Việc đã Done: ước {done_est}h, thực tế {done_act}h → hệ số thực tế/ước = **{ratio:.2f}**. "
           f"Năng lực tính theo giờ ước = năng lực thực ÷ {ratio:.2f}.", "",
           "### Tải theo người (giờ ước) so với năng lực", "",
           "| Sprint | " + " | ".join(CAP_ACTUAL) + " | Tổng |", "|---|" + "---:|" * (len(CAP_ACTUAL) + 1)]
    act_by = {o: 0 for o in CAP_ACTUAL}
    for k, o, *_ , act, _rem in [(r[0], r[1], r[2], r[3], r[4], r[5]) for r in rows]:
        act_by[o] += act
    md.append("| Năng lực thực (giờ) | " + " | ".join(str(c) for c in CAP_ACTUAL.values()) + f" | {sum(CAP_ACTUAL.values())} |")
    md.append("| Sprint 1 thực tế đã ghi | " + " | ".join(str(act_by[o]) for o in CAP_ACTUAL) + f" | {sum(act_by.values())} |")
    md.append("| Năng lực theo giờ ước | " + " | ".join(str(c) for c in cap.values()) + f" | {sum(cap.values())} |")
    for sp, cr in ((1, []), (2, carry), (3, [])):
        ld = load_by_owner(data, sp, cr)
        label = f"Sprint {sp}" + (" (gồm phần còn lại chuyển tiếp)" if cr else "")
        cells = [f"{ld[o]} ({ld[o] * 100 // cap[o]}%)" for o in CAP_ACTUAL]
        md.append(f"| {label} | " + " | ".join(cells) + f" | {sum(ld.values())} |")
    probs = dep_problems(data)
    md += ["", "### Phụ thuộc", "", "Không có issue nào xếp trước việc nó phụ thuộc." if not probs else
           "Vi phạm phụ thuộc:\n" + "\n".join(f"- {p}" for p in probs)]
    with open(a.md, "w", encoding="utf-8") as fh:
        fh.write("\n".join(md) + "\n")
    print(f"ratio={ratio:.2f} cap={cap} deps_problems={len(probs)}")


if __name__ == "__main__":
    main()
