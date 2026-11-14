"""Put every epic/issue/sub-issue into the GitHub Project and write field values:
Status, Iteration, SWP (reviewed), Giờ ước lượng, Phụ trách (giả định), Cấp, Ràng buộc đặc thù.
Also closes Done issues and makes the project public. Reads backlog-scored.json + github-map.json.

Usage: python scripts/github-project-sync.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gh_cli import OWNER, PROJECT_NUMBER, REPO, graphql, load_json, rest, save_json  # noqa: E402
from project_field_setup import ensure_fields  # noqa: E402

SCORED, MAP = "backlog/backlog-scored.json", "backlog/github-map.json"
BATCH = 6


def project_id():
    q = "query($o:String!,$n:Int!){user(login:$o){projectV2(number:$n){id}}}"
    return graphql(q, {"o": OWNER, "n": PROJECT_NUMBER})["user"]["projectV2"]["id"]


def add_items(pid, gmap):
    items = gmap.setdefault("_items", {})
    todo = [(k, v["node_id"]) for k, v in gmap.items() if not k.startswith("_") and k not in items]
    add_batch = 5  # addProjectV2ItemById is heavy; large batches trigger server errors
    for i in range(0, len(todo), add_batch):
        chunk = todo[i:i + add_batch]
        body = "".join(f'a{n}:addProjectV2ItemById(input:{{projectId:"{pid}",contentId:"{cid}"}}){{item{{id}}}} '
                       for n, (_, cid) in enumerate(chunk))
        res = graphql("mutation{" + body + "}")
        for n, (key, _) in enumerate(chunk):
            items[key] = res[f"a{n}"]["item"]["id"]
        save_json(MAP, gmap)
    return items


def rows(data):
    """Yield (key, values) where values maps field name -> python value."""
    constraint = lambda it: ("Giờ lái 2024" if it["epic"] == "E08"
                             else "Liên quan giờ lái 2024" if it.get("constraintTouch") else "Không")
    for ep in data["epics"]:
        its = [i for i in data["issues"] if i["epic"] == ep["key"]]
        st = [i["status"] for i in its]
        status = "Done" if all(s == "Done" for s in st) else ("Todo" if all(s == "Todo" for s in st) else "In Progress")
        yield ep["key"], {"Status": status, "Cấp": "Epic", "SWP": sum(i["swp"] for i in its),
                          "Giờ ước lượng": sum(i["hours"] for i in its),
                          "Ràng buộc đặc thù": "Giờ lái 2024" if ep.get("constraint") else "Không"}
    for it in data["issues"]:
        base = {"Iteration": it.get("sprint"), "Ràng buộc đặc thù": constraint(it)}
        yield it["key"], {**base, "Status": it["status"], "Cấp": "Issue", "SWP": it["swp"],
                          "Giờ ước lượng": it["hours"], "Phụ trách (giả định)": it["owner"]}
        for n, sub in enumerate(it["subIssues"], 1):
            sst = sub["status"] or ("Done" if it["status"] == "Done" else "Todo")
            yield f"{it['key']}.{n}", {**base, "Status": sst, "Cấp": "Sub-issue",
                                      "Giờ ước lượng": sub["hours"], "Phụ trách (giả định)": sub["owner"]}


def value_literal(field, val):
    if field["type"] == "NUMBER":
        return f"{{number:{val}}}"
    if field["type"] == "ITERATION":
        return f'{{iterationId:"{field["iterations"][str(val)]}"}}'
    return f'{{singleSelectOptionId:"{field["options"][val]}"}}'


def write_values(pid, fields, items, data):
    muts = []
    for key, vals in rows(data):
        for fname, val in vals.items():
            if val in (None, ""):
                continue
            f = fields[fname]
            muts.append(f'updateProjectV2ItemFieldValue(input:{{projectId:"{pid}",itemId:"{items[key]}",'
                        f'fieldId:"{f["id"]}",value:{value_literal(f, val)}}}){{projectV2Item{{id}}}}')
    for i in range(0, len(muts), BATCH):
        graphql("mutation{" + " ".join(f"m{n}:{m}" for n, m in enumerate(muts[i:i + BATCH])) + "}")
    return len(muts)


def close_done(data, gmap):
    for key, vals in rows(data):
        if vals["Status"] == "Done":
            rest("PATCH", f"repos/{REPO}/issues/{gmap[key]['number']}", {"state": "closed", "state_reason": "completed"})


def main():
    data, gmap = load_json(SCORED), load_json(MAP)
    pid = project_id()
    fields = ensure_fields(pid, data)
    items = add_items(pid, gmap)
    print("field values written:", write_values(pid, fields, items, data))
    close_done(data, gmap)
    readme = ("Backlog LAB-5 Product B (Yuki Cold Logistics) break từ thiết kế LAB-4. Cấp Epic → Issue → Sub-issue. "
              "SWP chỉ ghi ở cấp Issue (đã review); Epic = tổng; Sub-issue chỉ có giờ. Khi cộng SWP/giờ hãy lọc Cấp = Issue. "
              "Ràng buộc đặc thù 'Giờ lái 2024' = 改善基準告示 (epic E08). Repo: https://github.com/" + REPO)
    graphql("mutation($p:ID!,$r:String!){updateProjectV2(input:{projectId:$p,public:true,"
            "shortDescription:\"LAB-5 · Product B backlog · SWP + giờ · Sprint 1 giả lập\",readme:$r}){projectV2{id}}}",
            {"p": pid, "r": readme})
    print("done")


if __name__ == "__main__":
    main()
