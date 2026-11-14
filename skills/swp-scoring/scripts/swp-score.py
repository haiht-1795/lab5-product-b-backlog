"""Score a backlog JSON with SWP (Scope x Complexity -> Fibonacci), convert to hours,
flag granularity problems, pick review samples, and write scored JSON + HTML report.

Usage: swp-score.py backlog.json [swp-review.json] --out scored.json --html report.html
"""
import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from swp_report_html import render_report  # noqa: E402

HOURS_PER_SWP = 4
STUB_FACTOR = 1.25
SUB_MAX_HOURS = 16
ISSUE_MAX_HOURS_WITHOUT_SUB = 24


def fib_swp(product):
    """Map Scope x Complexity product to Fibonacci SWP."""
    for limit, swp in ((2, 1), (4, 2), (6, 3), (10, 5), (12, 8), (16, 13)):
        if product <= limit:
            return swp
    return 21


def score(s, c, legal):
    c_eff = min(5, c + (1 if legal else 0))
    return c_eff, fib_swp(s * c_eff)


def hours_for(swp, oq_mode):
    k = STUB_FACTOR if oq_mode in ("STUB", "BLOCK") else 1.0
    return int(round(swp * HOURS_PER_SWP * k)), k


def split_hours(total, subs):
    """Distribute parent hours over sub-issues by share; last one takes the remainder."""
    out, used = [], 0
    for i, sub in enumerate(subs):
        h = total - used if i == len(subs) - 1 else int(round(total * sub[1]))
        used += h
        out.append({"title": sub[0], "share": sub[1], "owner": sub[2],
                    "status": sub[3] if len(sub) > 3 else None, "hours": h})
    return out


def flags_for(it, swp, hours, subs):
    f = []
    if swp >= 21:
        f.append("SPLIT")
    if hours > ISSUE_MAX_HOURS_WITHOUT_SUB and not subs:
        f.append("NEED-SUB")
    if any(s["hours"] > SUB_MAX_HOURS for s in subs):
        f.append("SUB-BIG")
    if it.get("oqMode") == "BLOCK" and it.get("type") not in ("clarify", "design") and it.get("sprint"):
        f.append("BLOCK-SPRINT")
    if it.get("needsDesign") and it.get("sprint"):
        f.append("DESIGN-SPRINT")
    return f


def pick_samples(issues):
    """Return {key: reason} following the 4 sampling rules in SKILL.md."""
    picked = {}
    for it in issues:
        if it["flags"]:
            picked[it["key"]] = "R1 flag: " + ",".join(it["flags"])
        elif it.get("legal") and it["swpSkill"] >= 8:
            picked[it["key"]] = "R2 ràng buộc pháp lý, SWP ≥ 8"
        elif abs(it["S"] - it["C"]) >= 2:
            picked[it["key"]] = "R3 chấm lệch |S−C| ≥ 2"
    by_epic = {}
    for it in issues:
        by_epic.setdefault(it["epic"], []).append(it)
    for epic, items in by_epic.items():
        if any(i["key"] in picked for i in items):
            continue
        top = max(items, key=lambda i: (i["swpSkill"], i["key"]))
        picked[top["key"]] = "R4 SWP lớn nhất của epic (đối chứng)"
    return picked


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("backlog")
    ap.add_argument("review", nargs="?")
    ap.add_argument("--out", required=True)
    ap.add_argument("--html", required=True)
    a = ap.parse_args()

    with open(a.backlog, encoding="utf-8") as fh:
        data = json.load(fh)
    review, frozen_samples = {}, {}
    if a.review and os.path.exists(a.review):
        with open(a.review, encoding="utf-8") as fh:
            rv_file = json.load(fh)
        review = rv_file.get("decisions", {})
        # Samples chosen in the first (pre-review) run are frozen so the audit trail survives fixes.
        frozen_samples = rv_file.get("samplesFirstRun", {})

    for it in data["issues"]:
        c_eff, swp_skill = score(it["S"], it["C"], it.get("legal"))
        it["cEff"], it["swpSkill"] = c_eff, swp_skill
        rv = review.get(it["key"], {})
        if "S" in rv or "C" in rv:
            _, swp_final = score(rv.get("S", it["S"]), rv.get("C", it["C"]), it.get("legal"))
        else:
            swp_final = swp_skill
        it["swp"] = swp_final
        it["reviewNote"] = rv.get("note", "")
        it["reviewS"], it["reviewC"] = rv.get("S"), rv.get("C")
        it["hours"], it["k"] = hours_for(swp_final, it.get("oqMode", ""))
        it["subIssues"] = split_hours(it["hours"], it.get("subs", []))
        it["flags"] = flags_for(it, swp_final, it["hours"], it["subIssues"])

    samples = frozen_samples or pick_samples(data["issues"])
    for it in data["issues"]:
        it["sampleReason"] = samples.get(it["key"], "")

    with open(a.out, "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=1)
    os.makedirs(os.path.dirname(a.html) or ".", exist_ok=True)
    with open(a.html, "w", encoding="utf-8") as fh:
        fh.write(render_report(data))

    total = sum(i["swp"] for i in data["issues"])
    hrs = sum(i["hours"] for i in data["issues"])
    flagged = [i["key"] for i in data["issues"] if i["flags"]]
    print(f"issues={len(data['issues'])} swp={total} hours={hrs} samples={len(samples)} flagged={flagged}")


if __name__ == "__main__":
    main()
