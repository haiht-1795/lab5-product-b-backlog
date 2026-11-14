"""Render doc-templates/*.md into the repo-root Markdown files.

- `{{TABLE:name}}` is replaced by a generated table (see doc_table_builders.py).
- `{{FILE:path}}` is replaced by the content of a generated file (e.g. burndown table).
- `#{I-0801}` / `#{E08}` is replaced by the real GitHub issue number from backlog/github-map.json.

Usage: python scripts/render-doc-tables.py
"""
import glob
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import doc_table_builders as tb  # noqa: E402
from gh_cli import load_json  # noqa: E402

TEMPLATES = "doc-templates"


def main():
    data = load_json("backlog/backlog-scored.json")
    lab1 = load_json("backlog/lab1-estimate.json")
    gmap = load_json("backlog/github-map.json", {})
    tables = {
        "epic-map": lambda: tb.epic_map(data),
        "spec-to-issue": lambda: tb.spec_to_issue(data),
        "epic-totals": lambda: tb.epic_totals(data),
        "lab1-compare": lambda: tb.lab1_compare(data, lab1),
        "samples": lambda: tb.samples(data),
        "status-sprint-1": lambda: tb.status_sprint(data, 1),
    }
    missing = set()

    def issue_ref(m):
        key = m.group(1)
        if key in gmap:
            return f"#{gmap[key]['number']}"
        missing.add(key)
        return f"`{key}`"

    for path in sorted(glob.glob(os.path.join(TEMPLATES, "*.md"))):
        with open(path, encoding="utf-8") as fh:
            text = fh.read()
        text = re.sub(r"\{\{TABLE:([\w-]+)\}\}", lambda m: tables[m.group(1)](), text)
        text = re.sub(r"\{\{FILE:([^}]+)\}\}", lambda m: open(m.group(1), encoding="utf-8").read(), text)
        text = re.sub(r"#\{([EI]-?[\d.]+|E\d\d)\}", issue_ref, text)
        # Bare keys coming from data (review notes, daily log) → issue numbers too.
        text = re.sub(r"(?<![\w`#{])(I-\d{4}(?:\.\d+)?)\b", issue_ref, text)
        out = os.path.basename(path)
        with open(out, "w", encoding="utf-8") as fh:
            fh.write(text)
        print("rendered", out)
    if missing:
        print("WARNING unresolved issue keys:", sorted(missing))


if __name__ == "__main__":
    main()
