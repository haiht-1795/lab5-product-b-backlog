"""Create / normalise the custom fields of the GitHub Project and return a lookup:
{field name: {"id", "type", "options": {name: id}, "iterations": {sprint no: id}}}."""
from gh_cli import graphql

STATUS = ["Todo", "In Progress", "In Review", "Blocked", "Done"]
STATUS_COLORS = {"Todo": "GRAY", "In Progress": "YELLOW", "In Review": "BLUE", "Blocked": "RED", "Done": "GREEN"}
LEVELS = ["Epic", "Issue", "Sub-issue"]
CONSTRAINTS = ["Giờ lái 2024", "Liên quan giờ lái 2024", "Không"]

FIELDS_Q = """query($p:ID!){node(id:$p){... on ProjectV2{fields(first:50){nodes{
 ... on ProjectV2FieldCommon{id name dataType}
 ... on ProjectV2SingleSelectField{options{id name}}
 ... on ProjectV2IterationField{configuration{iterations{id title} completedIterations{id title}}}}}}}}"""


def epic_label(ep):
    """Option name of the 'Epic' single-select field (groupable, unlike the built-in Parent issue)."""
    title = ep["title"] if len(ep["title"]) <= 45 else ep["title"][:44] + "…"
    return f"{ep['key']} {title}"


def _fields(pid):
    return {f["name"]: f for f in graphql(FIELDS_Q, {"p": pid})["node"]["fields"]["nodes"] if f}


def _opts(names, colors=None):
    return "[" + ",".join(f'{{name:"{n}",color:{(colors or {}).get(n, "GRAY")},description:""}}' for n in names) + "]"


def _create(pid, name, dtype, options=None):
    extra = f",singleSelectOptions:{_opts(options)}" if options else ""
    graphql(f'mutation{{createProjectV2Field(input:{{projectId:"{pid}",dataType:{dtype},name:"{name}"{extra}}})'
            "{projectV2Field{... on ProjectV2FieldCommon{id}}}}")


def ensure_fields(pid, data):
    f = _fields(pid)
    status = f["Status"]
    if [o["name"] for o in status["options"]] != STATUS:
        graphql(f'mutation{{updateProjectV2Field(input:{{fieldId:"{status["id"]}",'
                f'singleSelectOptions:{_opts(STATUS, STATUS_COLORS)}}}){{projectV2Field{{... on ProjectV2FieldCommon{{id}}}}}}}}')
    wanted = {"SWP": ("NUMBER", None), "Giờ ước lượng": ("NUMBER", None),
              "Phụ trách (giả định)": ("SINGLE_SELECT", data["meta"]["owners"]),
              "Cấp": ("SINGLE_SELECT", LEVELS), "Ràng buộc đặc thù": ("SINGLE_SELECT", CONSTRAINTS),
              "Epic": ("SINGLE_SELECT", [epic_label(e) for e in data["epics"]])}
    for name, (dtype, options) in wanted.items():
        if name not in f:
            _create(pid, name, dtype, options)
    out = {}
    for name, fd in _fields(pid).items():
        entry = {"id": fd["id"], "type": fd.get("dataType")}
        if "options" in fd:
            entry["options"] = {o["name"]: o["id"] for o in fd["options"]}
        if fd.get("dataType") == "ITERATION":
            its = fd["configuration"]["iterations"] + fd["configuration"]["completedIterations"]
            entry["iterations"] = {t["title"].split()[-1]: t["id"] for t in its}
        out[name] = entry
    return out
