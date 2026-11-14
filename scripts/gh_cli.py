"""Thin wrappers around the `gh` CLI (REST + GraphQL) with retry on secondary rate limits."""
import json
import subprocess
import time

REPO = "haiht-1795/lab5-product-b-backlog"
OWNER = "haiht-1795"
PROJECT_NUMBER = 1


def _run(args, payload=None, retries=4):
    for attempt in range(retries):
        proc = subprocess.run(["gh"] + args, input=payload, capture_output=True, text=True, encoding="utf-8")
        if proc.returncode == 0:
            return json.loads(proc.stdout) if proc.stdout.strip() else {}
        err = proc.stderr
        transient = ("rate limit", "abuse", "502", "504", "something went wrong", "timeout")
        if any(t in err.lower() for t in transient):
            time.sleep(20 * (attempt + 1))
            continue
        raise RuntimeError(f"gh {' '.join(args[:3])} failed: {err.strip()}")
    raise RuntimeError("gh: retries exhausted")


def rest(method, path, body=None):
    args = ["api", "-X", method, path]
    if body is None:
        return _run(args)
    return _run(args + ["--input", "-"], json.dumps(body, ensure_ascii=False))


def graphql(query, variables=None):
    body = {"query": query, "variables": variables or {}}
    res = _run(["api", "graphql", "--input", "-"], json.dumps(body, ensure_ascii=False))
    if res.get("errors"):
        raise RuntimeError(json.dumps(res["errors"], ensure_ascii=False)[:800])
    return res["data"]


def load_json(path, default=None):
    try:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    except FileNotFoundError:
        return default


def save_json(path, data):
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=1)
