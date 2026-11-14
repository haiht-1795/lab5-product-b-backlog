"""Create labels, epic/issue/sub-issue GitHub issues from backlog-scored.json, link sub-issues,
and close Done items. Idempotent: keys already in backlog/github-map.json are skipped.

Usage: python scripts/github-issues-sync.py
"""
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gh_cli import REPO, load_json, rest, save_json  # noqa: E402

SCORED = "backlog/backlog-scored.json"
MAP = "backlog/github-map.json"
LABELS = {
    "type:epic": "5319e7", "type:task": "0e8a16", "type:sub-task": "c2e0c6", "type:design": "fbca04",
    "type:clarify": "d93f0b", "constraint:duty-2024": "b60205", "constraint:touch-duty-2024": "e99695",
    "oq:CFG": "bfdadc", "oq:STUB": "f9d0c4", "oq:BLOCK": "b60205", "needs-design": "fef2c0",
}
COMMON_DOD = ("Code review xong · unit test xanh trên CI · đúng tiêu chí trên · không hard-code đề xuất "
              "vendor ở chỗ có ⏳ OQ (làm theo CFG/STUB/BLOCK) · cập nhật trạng thái trên Project.")


def ensure_labels():
    existing = {l["name"] for l in rest("GET", f"repos/{REPO}/labels?per_page=100")}
    for name, color in LABELS.items():
        if name not in existing:
            rest("POST", f"repos/{REPO}/labels", {"name": name, "color": color})


def issue_labels(it):
    labels = ["type:" + ("task" if it.get("type", "build") == "build" else it["type"])]
    if it["epic"] == "E08":
        labels.append("constraint:duty-2024")
    elif it.get("constraintTouch"):
        labels.append("constraint:touch-duty-2024")
    if it.get("oqMode"):
        labels.append("oq:" + it["oqMode"])
    if it.get("needsDesign"):
        labels.append("needs-design")
    return labels


def epic_body(ep, items):
    swp, hrs = sum(i["swp"] for i in items), sum(i["hours"] for i in items)
    lines = [f"**Feature LAB-1/LAB-4:** {ep['feature']}", f"**Spec LAB-4:** {ep['spec']}",
             f"**Tổng:** {len(items)} issue · {swp} SWP · {hrs} giờ (SWP/giờ nằm ở từng issue con)"]
    if ep.get("constraint"):
        lines.append("\n> ⚠ Epic tách riêng cho ràng buộc đặc thù Product B: giới hạn giờ lái xe tải từ 4/2024 "
                     "(改善基準告示). Mọi ngưỡng là tham số có version, chờ xác minh pháp lý (OPS-LAW-01).")
    return "\n".join(lines)


def task_body(it, epic_no):
    oq = f"{it['oq']} → dev làm theo **{it['oqMode']}**" if it.get("oq") else "—"
    est = (f"Scope {it['S']} × Complexity {it['cEff']}{' (+1 pháp lý)' if it.get('legal') else ''} → "
           f"SWP skill **{it['swpSkill']}**, chốt **{it['swp']}** · **{it['hours']} giờ** (k={it['k']})")
    lines = [f"**Epic:** #{epic_no}", f"**Spec LAB-4:** {it['spec']}", f"**⏳ OQ:** {oq}",
             f"**Ước lượng:** {est}", f"**Phụ trách (giả định):** {it['owner']}"]
    if it.get("reviewNote"):
        lines.append(f"**Review SWP:** {it['reviewNote']}")
    if it["epic"] == "E08" or it.get("constraintTouch"):
        lines.append("**Ràng buộc đặc thù:** giới hạn giờ lái 2024 — xem task-breakdown.md §3")
    lines += ["", "### Định nghĩa xong", f"- {it['dod']}", f"- {COMMON_DOD}"]
    return "\n".join(lines)


def create(key, title, body, labels, gmap):
    if key in gmap:
        return gmap[key]
    res = rest("POST", f"repos/{REPO}/issues", {"title": title, "body": body, "labels": labels})
    gmap[key] = {"number": res["number"], "id": res["id"], "node_id": res["node_id"]}
    save_json(MAP, gmap)
    time.sleep(1.2)  # stay under content-creation secondary rate limit
    return gmap[key]


def link(parent, child, gmap_links, link_key):
    if link_key in gmap_links:
        return
    try:
        rest("POST", f"repos/{REPO}/issues/{parent['number']}/sub_issues", {"sub_issue_id": child["id"]})
    except RuntimeError as exc:
        if "already" not in str(exc).lower() and "duplicate" not in str(exc).lower():
            raise
    gmap_links.append(link_key)


def main():
    data = load_json(SCORED)
    gmap = load_json(MAP, {})
    links = gmap.setdefault("_links", [])
    ensure_labels()
    for ep in data["epics"]:
        items = [i for i in data["issues"] if i["epic"] == ep["key"]]
        create(ep["key"], f"[{ep['key']}] {ep['title']}", epic_body(ep, items),
               ["type:epic"] + (["constraint:duty-2024"] if ep.get("constraint") else []), gmap)
    for it in data["issues"]:
        epic = gmap[it["epic"]]
        node = create(it["key"], f"[{it['key']}] {it['title']}", task_body(it, epic["number"]), issue_labels(it), gmap)
        link(epic, node, links, f"{it['epic']}>{it['key']}")
        for n, sub in enumerate(it["subIssues"], 1):
            skey = f"{it['key']}.{n}"
            sbody = (f"**Issue cha:** #{node['number']}\n**Ước lượng:** {sub['hours']} giờ "
                     f"({int(sub['share'] * 100)}% của {it['hours']} giờ; SWP tính ở issue cha)\n"
                     f"**Phụ trách (giả định):** {sub['owner']}")
            labels = ["type:sub-task"] + (["constraint:duty-2024"] if it["epic"] == "E08" else [])
            snode = create(skey, f"[{skey}] {sub['title']}", sbody, labels, gmap)
            link(node, snode, links, f"{it['key']}>{skey}")
    save_json(MAP, gmap)
    print("issues in map:", len([k for k in gmap if not k.startswith("_")]))


if __name__ == "__main__":
    main()
