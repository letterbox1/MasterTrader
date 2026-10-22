#!/usr/bin/env python3
"""Project kanban (CeraNova PM): per-phase boards + a unified project board, generated from tracking/ item files.

Source of truth: tracking/phase-N/{PHASE.md,tasks/*.md,bugs/*.md}. See tracking/SCHEMA.md.
Project settings: tracking/kanban.config.json (all optional). Stdlib only (Python >= 3.9), so it runs the
same in cloud sessions, local shells, git hooks and CI, for any project type.
"""
from __future__ import annotations

import argparse
import shutil
import datetime as dt
import hashlib
import json
import os
import re
import socket
import subprocess
import sys
from pathlib import Path

ROOT = Path(os.environ.get("KANBAN_ROOT") or Path(__file__).resolve().parents[2]).resolve()
TRACK = ROOT / "tracking"
STATE = TRACK / ".state"
CONFIG_FILE = TRACK / "kanban.config.json"
DEFAULT_CONFIG = {
    "project": "",                                   # display name; defaults to the repo folder name
    "roadmap_dir": "docs/roadmap",                   # where phase-N-<slug>.md roadmap docs live
    "roadmap_index": "docs/roadmap/README.md",       # gets <!-- kanban:... --> status blocks if present
    "types": ["USER", "BUILD", "OPS", "VERIFY", "RUN", "DOC", "RESEARCH"],
    "sizes": {"XS": 1, "S": 2, "M": 3, "L": 5, "XL": 8},
    "required_headings": [
        "## Goal / expected outcome", "## Context & references", "## Requirements", "## ToDo",
        "## Verification", "## Acceptance criteria", "## Exceptions & edge cases",
        "## Cardinal rules (do NOT)", "## Doc sync on completion", "## Branch & PR", "## Progress log",
    ],
    "stale_days": 7,
    "brand": {"accent": "", "accent2": "", "logo": "", "attribution": True, "fonts": True},  # board accents, project logo, credit, embedded fonts
    "project_type": "",                              # set by `init` from `./kanban detect`; drives pm-research agendas
    "foundation_docs": ["GOAL.md", "SPEC.md"],       # pm-intake is suggested until these exist without pm:fill markers
    # Requirements every task of a type needs, merged with each item's own tools/mcp/env/services ("*" = all types),
    # e.g. {"*": {"tools": ["git"]}, "BUILD": {"tools": ["node", "pnpm"]}, "OPS": {"env": ["CLOUD_TOKEN"]}}
    "requires_defaults": {},
    "env_files": [".env", ".env.local"],
    "require_review": False,                         # true: `done` needs a passing `./kanban reviewed` (pm-review) first             # preflight also accepts env var NAMES defined here (values never read out)
}


def load_config() -> dict:
    cfg = json.loads(json.dumps(DEFAULT_CONFIG))
    if CONFIG_FILE.exists():
        try:
            cfg.update(json.loads(CONFIG_FILE.read_text()))
        except json.JSONDecodeError as e:
            sys.exit(f"invalid {CONFIG_FILE}: {e}")
    return cfg


CFG = load_config()
KIT_NAME = "CeraNova PM"
KIT_URL = "https://ceranovaai.com"
PROJECT = CFG.get("project") or ROOT.name
ROADMAP = ROOT / CFG["roadmap_dir"]

STATUSES = ["backlog", "ready", "in_progress", "review", "blocked", "done", "cancelled"]
OPEN_STATUSES = {"backlog", "ready", "in_progress", "review", "blocked"}
CLOSED = {"done", "cancelled"}
KINDS = ["task", "bug", "gap", "chore"]
TYPES = list(CFG["types"])
PRIORITIES = ["critical", "high", "medium", "low"]
SIZES = dict(CFG["sizes"])
SEVERITIES = ["", "S1", "S2", "S3", "S4"]
OWNERS = ["user", "agent", "unassigned"]
DOC_SYNC = ["n/a", "pending", "done"]
HEADINGS = list(CFG["required_headings"])
ID_RE = re.compile(r"^P(\d+)-([TB])(\d{3,})$")
STALE_DAYS = int(CFG["stale_days"])
COLUMNS = ["backlog", "ready", "in_progress", "review", "blocked", "done"]
COLUMN_TITLES = {"backlog": "Backlog", "ready": "Ready", "in_progress": "In progress", "review": "Review",
                 "blocked": "Blocked", "done": "Done", "cancelled": "Cancelled"}


# ---------------------------------------------------------------- helpers

def now() -> dt.datetime:
    return dt.datetime.now(dt.timezone.utc)


def today() -> str:
    return now().strftime("%Y-%m-%d")


def stamp() -> str:
    return now().strftime("%Y-%m-%d %H:%M")


def env_label() -> str:
    cloud = any(os.environ.get(k) for k in ("CLAUDE_CODE_REMOTE", "CLAUDE_CODE_REMOTE_SDK_URL", "CLAUDE_CODE_CONTAINER_ID"))
    sess = os.environ.get("CLAUDE_CODE_SESSION_ID") or os.environ.get("KANBAN_SESSION") or "manual"
    return f"{'cloud' if cloud else 'local'}:{socket.gethostname()[:20]}:{sess[-12:]}"


def rel(p: Path) -> str:
    return p.resolve().relative_to(ROOT).as_posix()


def parse_value(v: str):
    v = v.strip()
    if v in ('""', "''", "", "null", "~"):
        return ""
    if v.startswith("[") and v.endswith("]"):
        inner = v[1:-1].strip()
        return [x.strip().strip("\"'") for x in inner.split(",") if x.strip()] if inner else []
    if len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'":
        return v[1:-1]
    if v in ("true", "false"):
        return v == "true"
    return v


def fmt_value(v) -> str:
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, list):
        return "[" + ", ".join(str(x) for x in v) + "]"
    s = str(v)
    if s == "":
        return '""'
    if any(c in s for c in ":#[]") or s != s.strip():
        return '"' + s.replace('"', "'") + '"'
    return s


def split_doc(text: str):
    if not text.startswith("---"):
        raise ValueError("missing front matter")
    end = text.find("\n---", 3)
    if end < 0:
        raise ValueError("unterminated front matter")
    fm = text[4:end]
    body = text[end + 4:].lstrip("\n")
    meta = {}
    for line in fm.splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if ":" not in line:
            raise ValueError(f"bad front matter line: {line!r}")
        k, v = line.split(":", 1)
        v = re.sub(r"\s+#.*$", "", v) if not v.strip().startswith(('"', "'")) else v
        meta[k.strip()] = parse_value(v)
    return meta, body


def write_meta(path: Path, updates: dict):
    text = path.read_text()
    end = text.find("\n---", 3)
    fm_lines = text[4:end].splitlines()
    done = set()
    for i, line in enumerate(fm_lines):
        k = line.split(":", 1)[0].strip()
        if k in updates:
            fm_lines[i] = f"{k}: {fmt_value(updates[k])}"
            done.add(k)
    for k, v in updates.items():
        if k not in done:
            fm_lines.append(f"{k}: {fmt_value(v)}")
    path.write_text("---\n" + "\n".join(fm_lines) + text[end:])


def append_log(path: Path, note: str, who: str | None = None):
    text = path.read_text().rstrip("\n")
    who = who or env_label()
    line = f"- {stamp()} · {who} · {note}"
    if "## Progress log" not in text:
        text += "\n\n## Progress log\n"
    path.write_text(text + "\n" + line + "\n")


def section(body: str, heading: str) -> str:
    i = body.find(heading + "\n")
    if i < 0:
        return ""
    rest = body[i + len(heading) + 1:]
    m = re.search(r"^## ", rest, re.M)
    return rest[: m.start()] if m else rest


def checklist(body: str, heading: str):
    s = section(body, heading)
    done = len(re.findall(r"^\s*- \[[xX]\]", s, re.M))
    todo = len(re.findall(r"^\s*- \[ \]", s, re.M))
    return done, done + todo


# ---------------------------------------------------------------- model

class Item:
    def __init__(self, path: Path):
        self.path = path
        self.meta, self.body = split_doc(path.read_text())

    def __getitem__(self, k):
        return self.meta.get(k, "")

    @property
    def id(self):
        return self.meta.get("id", "")

    @property
    def weight(self):
        return SIZES.get(str(self["size"]), 3)

    def todo(self):
        return checklist(self.body, "## ToDo")

    def acceptance(self):
        return checklist(self.body, "## Acceptance criteria")

    def credit(self):
        st = self["status"]
        if st == "done":
            return 1.0
        if st == "review":
            return 0.9
        if st == "in_progress":
            d, t = self.todo()
            return 0.1 + 0.7 * (d / t if t else 0)
        return 0.0

    def stale(self):
        if self["status"] != "in_progress" or not self["updated"]:
            return False
        try:
            u = dt.date.fromisoformat(str(self["updated"])[:10])
        except ValueError:
            return False
        return (now().date() - u).days > STALE_DAYS

    def last_log(self, n=1):
        s = section(self.body, "## Progress log")
        lines = [l for l in s.splitlines() if l.startswith("- ")]
        return lines[-n:]

    def is_open_bug(self):
        return self["kind"] in ("bug", "gap") and self["status"] not in CLOSED


class Phase:
    def __init__(self, n: int):
        self.n = n
        self.dir = TRACK / f"phase-{n}"
        self.file = self.dir / "PHASE.md"
        if self.file.exists():
            self.meta, self.body = split_doc(self.file.read_text())
        else:
            self.meta, self.body = {"phase": str(n), "title": f"Phase {n}", "status": "not_started", "opens_after": []}, ""
        self.items: list[Item] = []

    @property
    def title(self):
        return self.meta.get("title", f"Phase {self.n}")

    def tasks(self):
        return [i for i in self.items if i["kind"] in ("task", "chore")]

    def bugs(self):
        return [i for i in self.items if i["kind"] in ("bug", "gap")]

    def exit_criteria(self):
        return checklist(self.body, "## Exit criteria")

    def progress(self):
        items = [i for i in self.tasks() if i["status"] != "cancelled"]
        total = sum(i.weight for i in items) or 0
        if not total:
            return {"pct": 0.0, "done": 0.0, "review": 0.0, "inprog": 0.0, "weight": 0}
        seg = {"done": 0.0, "review": 0.0, "inprog": 0.0}
        for i in items:
            c = i.credit() * i.weight
            key = {"done": "done", "review": "review"}.get(i["status"], "inprog")
            seg[key] += c
        return {"pct": 100 * sum(seg.values()) / total, "done": 100 * seg["done"] / total,
                "review": 100 * seg["review"] / total, "inprog": 100 * seg["inprog"] / total, "weight": total}

    def counts(self):
        c = {s: 0 for s in STATUSES}
        for i in self.tasks():
            c[i["status"]] = c.get(i["status"], 0) + 1
        return c

    def open_bugs(self):
        c = {"S1": 0, "S2": 0, "S3": 0, "S4": 0, "": 0}
        for b in self.bugs():
            if b.is_open_bug():
                c[b["severity"] if b["severity"] in c else ""] += 1
        return c


def phase_numbers() -> list[int]:
    if not TRACK.exists():
        return []
    return sorted(int(m.group(1)) for d in TRACK.iterdir()
                  if d.is_dir() and (m := re.fullmatch(r"phase-(\d+)", d.name)))


def roadmap_doc(n: int, ph: "Phase | None" = None) -> "Path | None":
    if ph is not None and ph.meta.get("roadmap"):
        p = ROOT / str(ph.meta["roadmap"])
        if p.exists():
            return p
    return next(iter(sorted(ROADMAP.glob(f"phase-{n}-*.md"))), None)


def load():
    phases = {n: Phase(n) for n in phase_numbers()}
    items = {}
    errors = []
    for n, ph in phases.items():
        for sub in ("tasks", "bugs"):
            d = ph.dir / sub
            if not d.exists():
                continue
            for p in sorted(d.glob("*.md")):
                try:
                    it = Item(p)
                except ValueError as e:
                    errors.append(f"{rel(p)}: {e}")
                    continue
                ph.items.append(it)
                if it.id in items:
                    errors.append(f"{rel(p)}: duplicate id {it.id} (also {rel(items[it.id].path)})")
                items[it.id] = it
    return phases, items, errors


def phase_done(ph: Phase, phases) -> bool:
    tasks = ph.tasks()
    if not tasks:
        return False
    if any(t["status"] not in CLOSED for t in tasks):
        return False
    ob = ph.open_bugs()
    if ob["S1"] or ob["S2"]:
        return False
    d, t = ph.exit_criteria()
    return t > 0 and d == t


def phase_open(ph: Phase, phases) -> bool:
    if ph.meta.get("force_open") is True:
        return True
    after = ph.meta.get("opens_after") or []
    return all(int(a) in phases and phases[int(a)].meta.get("status") == "done" for a in after if str(a).isdigit())


# ---------------------------------------------------------------- roadmap ids

def roadmap_ids(n: int, ph: "Phase | None" = None):
    doc = roadmap_doc(n, ph)
    if not doc:
        return set(), set()
    s = doc.read_text()
    reqs = set(re.findall(r"^\| (R\d+\.N?\d+) \|", s, re.M))
    todos = set(re.findall(r"\*\*(T\d+\.\d+)\*\*", s))
    return reqs, todos


# ---------------------------------------------------------------- validate

def validate(phases, items, load_errors):
    errors, warns = list(load_errors), []
    ids = set(items)
    for n, ph in phases.items():
        if not ph.file.exists():
            warns.append(f"tracking/phase-{n}/PHASE.md missing")
        reqs, todos = roadmap_ids(n, ph)
        for it in ph.items:
            where = rel(it.path)
            m = ID_RE.match(it.id)
            if not m:
                errors.append(f"{where}: bad id {it.id!r}")
                continue
            if int(m.group(1)) != n or str(it["phase"]) != str(n):
                errors.append(f"{where}: id/phase/folder mismatch")
            if not it.path.name.startswith(it.id + "-"):
                errors.append(f"{where}: filename must start with '{it.id}-'")
            if (m.group(2) == "T") != (it.path.parent.name == "tasks"):
                errors.append(f"{where}: T-ids live in tasks/, B-ids in bugs/")
            for k, allowed in (("kind", KINDS), ("type", TYPES), ("status", STATUSES), ("priority", PRIORITIES),
                               ("owner", OWNERS), ("doc_sync_status", DOC_SYNC), ("severity", SEVERITIES)):
                if it[k] not in allowed:
                    errors.append(f"{where}: {k}={it[k]!r} not in {allowed}")
            if it["size"] not in SIZES:
                errors.append(f"{where}: size={it['size']!r} not in {list(SIZES)}")
            if it["kind"] in ("bug", "gap") and not it["severity"]:
                errors.append(f"{where}: bugs/gaps need a severity")
            for d in it["depends_on"] or []:
                if d not in ids:
                    errors.append(f"{where}: depends_on {d} does not exist")
                if d == it.id:
                    errors.append(f"{where}: depends on itself")
            for h in HEADINGS:
                if h not in it.body:
                    errors.append(f"{where}: missing heading '{h}'")
            if it["type"] == "USER" and it["owner"] != "user":
                warns.append(f"{where}: type USER should have owner: user")
            if it["status"] == "done":
                for name, (d, t) in (("ToDo", it.todo()), ("Acceptance criteria", it.acceptance())):
                    if d != t:
                        errors.append(f"{where}: done but {t - d} unticked {name} box(es)")
                if not it["completed"]:
                    errors.append(f"{where}: done without 'completed' date")
            if it["kind"] == "task" and it.todo()[1] == 0:
                warns.append(f"{where}: no ToDo checklist items")
            if it["kind"] == "task" and it.acceptance()[1] == 0:
                warns.append(f"{where}: no acceptance criteria")
            for r in it["requirements"] or []:
                if reqs and r not in reqs and r.startswith(f"R{n}."):
                    warns.append(f"{where}: requirement {r} not found in roadmap phase {n}")
            for t in it["roadmap_todos"] or []:
                if todos and t not in todos and t.startswith(f"T{n}."):
                    warns.append(f"{where}: roadmap ToDo {t} not found in roadmap phase {n}")
            if it["review_result"] not in ("", "pass", "fail"):
                errors.append(f"{where}: review_result={it['review_result']!r} not in ['', 'pass', 'fail']")
            for f in REQ_FIELDS:
                v = it.meta.get(f, [])
                if v not in ("", None) and not isinstance(v, list):
                    errors.append(f"{where}: {f} must be a list like [a, b]")
            for e in (it["env"] if isinstance(it["env"], list) else []):
                if "=" in e or not ENV_NAME_RE.match(e):
                    errors.append(f"{where}: env lists variable NAMES only ({e.split('=')[0][:40]!r} has a value or bad name); "
                                  "never put values in item files")
            if it["branch"] and not str(it["branch"]).startswith(f"p{n}/{it.id}"):
                warns.append(f"{where}: branch should start with p{n}/{it.id}")
    # cycles
    graph = {k: list(v["depends_on"] or []) for k, v in items.items()}
    color = {}

    def dfs(u, stack):
        color[u] = 1
        for v in graph.get(u, []):
            if v not in graph:
                continue
            if color.get(v) == 1:
                errors.append("dependency cycle: " + " → ".join(stack + [u, v]))
            elif not color.get(v):
                dfs(v, stack + [u])
        color[u] = 2

    for k in graph:
        if not color.get(k):
            dfs(k, [])
    return errors, warns


# ---------------------------------------------------------------- requirements & preflight

REQ_FIELDS = ("tools", "mcp", "env", "services")
ENV_NAME_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")


def effective_requires(it: "Item") -> dict:
    """What a task needs to be worked: its own tools/mcp/env/services plus `requires_defaults` for its type."""
    d = CFG.get("requires_defaults") or {}
    out = {}
    for f in REQ_FIELDS:
        vals = list((d.get("*") or {}).get(f, [])) + list((d.get(str(it["type"])) or {}).get(f, []))
        vals += list(it[f]) if isinstance(it[f], list) else []
        out[f] = list(dict.fromkeys(str(v).strip() for v in vals if str(v).strip()))
    return out


def _tool_name(spec: str) -> str:
    return re.split(r"[<>=@\s]", spec, maxsplit=1)[0]


_MCP_CACHE = None


def mcp_configured() -> set:
    """Names of MCP servers configured for any agent, project or user level (names only)."""
    global _MCP_CACHE
    if _MCP_CACHE is not None:
        return _MCP_CACHE
    names, home = set(), Path.home()
    for f, key in ((ROOT / ".mcp.json", "mcpServers"), (ROOT / ".claude" / "settings.json", "mcpServers"),
                   (ROOT / ".cursor" / "mcp.json", "mcpServers"), (ROOT / ".gemini" / "settings.json", "mcpServers"),
                   (ROOT / ".vscode" / "mcp.json", "servers"), (ROOT / "opencode.json", "mcp"),
                   (home / ".claude.json", "mcpServers"), (home / ".cursor" / "mcp.json", "mcpServers"),
                   (home / ".gemini" / "settings.json", "mcpServers"),
                   (home / ".config" / "opencode" / "opencode.json", "mcp")):
        try:
            names |= set((json.loads(f.read_text()).get(key) or {}).keys())
        except (OSError, ValueError, AttributeError):
            pass
    for f in (ROOT / ".codex" / "config.toml", home / ".codex" / "config.toml"):
        try:
            names |= set(re.findall(r"^\[mcp_servers\.([^\]]+)\]", f.read_text(), re.M))
        except OSError:
            pass
    _MCP_CACHE = {n.strip('"') for n in names}
    return _MCP_CACHE


def env_names_available() -> set:
    names = set(os.environ)
    for rp in CFG.get("env_files") or []:
        try:
            names |= set(re.findall(r"^\s*(?:export\s+)?([A-Za-z_][A-Za-z0-9_]*)\s*=", (ROOT / rp).read_text(), re.M))
        except OSError:
            pass
    return names


def preflight(it: "Item") -> list:
    """[(field, name, status)] with status ok | missing (blocks start) | not-found (MCP may be user-level or a
    hosted connector) | confirm (services can't be checked automatically)."""
    req = effective_requires(it)
    rows = []
    for t in req["tools"]:
        rows.append(("tool", t, "ok" if shutil.which(_tool_name(t)) else "missing"))
    if req["mcp"]:
        have = mcp_configured()
        rows += [("mcp", m, "ok" if m in have else "not-found") for m in req["mcp"]]
    if req["env"]:
        have = env_names_available()
        rows += [("env", e, "ok" if e in have else "missing") for e in req["env"]]
    rows += [("service", sv, "confirm") for sv in req["services"]]
    return rows


def preflight_missing(it: "Item") -> list:
    return [f"{f} {n}" for f, n, st in preflight(it) if st == "missing"]


def format_preflight(it: "Item", rows=None) -> str:
    rows = preflight(it) if rows is None else rows
    if not rows:
        return f"{it.id}: no tools, MCP servers, env vars or services listed"
    mark = {"ok": "ok     ", "missing": "MISSING", "not-found": "check  ", "confirm": "confirm"}
    out = [f"{it.id} preflight ({it['title']}):"]
    out += [f"  {mark[st]} {f:7} {n}" + {"not-found": "  (not in any MCP config here; fine if it's a user-level or hosted connector)",
                                           "confirm": "  (check it's reachable)"}.get(st, "") for f, n, st in rows]
    return "\n".join(out)


def cmd_preflight(a):
    phases, items, _ = load()
    if a.id:
        sel = [get(items, x) for x in a.id]
    else:
        sel = [i for i in next_items(phases, items, phase=a.phase) if i["owner"] != "user"] if a.ready else \
              [i for i in items.values() if i["status"] not in CLOSED and (a.phase is None or str(i["phase"]) == str(a.phase))]
    bad = 0
    for it in sorted(sel, key=lambda i: i.id):
        rows = preflight(it)
        if a.id or any(st != "ok" for _, _, st in rows):
            print(format_preflight(it, rows))
        bad += any(st == "missing" for _, _, st in rows)
    if not a.id:
        print(f"{len(sel)} item(s) checked, {bad} missing a tool or env var on this machine.")
    sys.exit(1 if bad else 0)


# ---------------------------------------------------------------- triage

def deps_done(it: Item, items) -> bool:
    return all(items[d]["status"] in CLOSED for d in (it["depends_on"] or []) if d in items)


def triage(phases, items, quiet=True):
    changes = []
    # phase status first (depends on items only)
    for n, ph in phases.items():
        if not ph.file.exists():
            continue
        st = ph.meta.get("status", "not_started")
        tasks = ph.tasks()
        new = st
        if phase_done(ph, phases):
            new = "done"
        elif any(t["status"] not in ("backlog", "ready") for t in tasks):
            new = "in_progress"
        elif st == "done":
            new = "in_progress"
        upd = {}
        if new != st:
            upd["status"] = new
            if new == "in_progress" and not ph.meta.get("started"):
                upd["started"] = today()
            if new == "done":
                upd["completed"] = today()
                upd["doc_sync_status"] = "pending"
            changes.append(f"phase {n}: {st} → {new}")
        if upd:
            upd["updated"] = today()
            write_meta(ph.file, upd)
            ph.meta.update(upd)
    for it in items.values():
        ph = phases[int(it["phase"])]
        st, upd = it["status"], {}
        ok = deps_done(it, items)
        if st == "backlog" and ok and phase_open(ph, phases):
            upd["status"] = "ready"
        elif st == "ready" and (not ok or not phase_open(ph, phases)):
            upd["status"] = "backlog"
        elif st == "blocked" and str(it["blocked_reason"]).startswith("auto:deps") and ok:
            upd.update(status="ready", blocked_reason="")
        if st == "done" and (it["doc_sync"] or []) and it["doc_sync_status"] == "n/a":
            upd["doc_sync_status"] = "pending"
        if upd:
            upd["updated"] = today()
            write_meta(it.path, upd)
            changes.append(f"{it.id}: " + ", ".join(f"{k}={v}" for k, v in upd.items() if k != "updated"))
            it.meta.update(upd)
    if changes and not quiet:
        print("triage:\n  " + "\n  ".join(changes))
    return changes


# ---------------------------------------------------------------- render: markdown boards

def bar(p: Phase | None = None, seg=None, width=24) -> str:
    seg = seg or p.progress()
    d = round(seg["done"] / 100 * width)
    r = round(seg["review"] / 100 * width)
    i = round(seg["inprog"] / 100 * width)
    i = max(0, min(i, width - d - r))
    return "█" * d + "▓" * r + "▒" * i + "░" * (width - d - r - i)


def overall(phases):
    tot = sum(p.progress()["weight"] for p in phases.values())
    if not tot:
        return {"pct": 0, "done": 0, "review": 0, "inprog": 0, "weight": 0}
    agg = {k: sum(p.progress()[k] * p.progress()["weight"] for p in phases.values()) / tot
           for k in ("pct", "done", "review", "inprog")}
    agg["weight"] = tot
    return agg


def md_link(it: Item, base: Path) -> str:
    return f"[{it.id}]({os.path.relpath(it.path, base)})"


def esc(s) -> str:
    return str(s).replace("|", "\\|")


def render_board(ph: Phase, items, phases) -> str:
    base = ph.dir
    pr = ph.progress()
    c = ph.counts()
    ob = ph.open_bugs()
    ed, et = ph.exit_criteria()
    road = roadmap_doc(ph.n, ph)
    out = [f"# Phase {ph.n} · {ph.title}: Kanban", "",
           "> Generated by `./kanban build`. Do not edit; change the item files in `tasks/` and `bugs/`, or `PHASE.md`.", "",
           f"**Status:** `{ph.meta.get('status', 'not_started')}` · **Open:** {'yes' if phase_open(ph, phases) else 'no (waiting on ' + ', '.join('P' + str(a) for a in ph.meta.get('opens_after') or []) + ')'}",
           "",
           f"`{bar(ph)}` **{pr['pct']:.0f}%**  (█ done {pr['done']:.0f}% · ▓ review {pr['review']:.0f}% · ▒ in progress {pr['inprog']:.0f}%)",
           "",
           "| Backlog | Ready | In progress | Review | Blocked | Done | Cancelled | Open bugs S1/S2/S3/S4 | Exit criteria |",
           "|---|---|---|---|---|---|---|---|---|",
           f"| {c['backlog']} | {c['ready']} | {c['in_progress']} | {c['review']} | {c['blocked']} | {c['done']} | {c['cancelled']} | {ob['S1']}/{ob['S2']}/{ob['S3']}/{ob['S4']} | {ed}/{et} |",
           "",
           f"Roadmap: [{road.name if road else 'n/a'}]({os.path.relpath(road, base) if road else '#'}) · Phase plan: [PHASE.md](PHASE.md) · Root board: [KANBAN.md]({os.path.relpath(ROOT / 'KANBAN.md', base)})",
           ""]
    tasks = sorted(ph.tasks(), key=lambda i: i.id)
    for col in ["in_progress", "review", "blocked", "ready", "backlog", "done", "cancelled"]:
        rows = [t for t in tasks if t["status"] == col]
        if not rows and col == "cancelled":
            continue
        out += [f"## {COLUMN_TITLES[col]} ({len(rows)})", ""]
        if not rows:
            out += ["_None._", ""]
            continue
        if col in ("in_progress", "review"):
            out += ["| ID | Title | Type | Owner | ToDo | Checkpoint | Claimed by |", "|---|---|---|---|---|---|---|"]
            for t in rows:
                d, tt = t.todo()
                flag = " ⚠️ stale" if t.stale() else ""
                out.append(f"| {md_link(t, base)} | {esc(t['title'])}{flag} | {t['type']} | {t['owner']} | {d}/{tt} | {esc(t['checkpoint'])} | {esc(t['claimed_by'])} |")
        elif col == "blocked":
            out += ["| ID | Title | Type | Reason |", "|---|---|---|---|"]
            for t in rows:
                out.append(f"| {md_link(t, base)} | {esc(t['title'])} | {t['type']} | {esc(t['blocked_reason'])} |")
        elif col in ("done", "cancelled"):
            out += ["| ID | Title | Type | Completed | Doc sync |", "|---|---|---|---|---|"]
            for t in rows:
                out.append(f"| {md_link(t, base)} | {esc(t['title'])} | {t['type']} | {t['completed']} | {t['doc_sync_status']} |")
        else:
            out += ["| ID | Title | Type | Priority | Size | Owner | Waiting on |", "|---|---|---|---|---|---|---|"]
            for t in rows:
                waiting = [d for d in (t["depends_on"] or []) if d in items and items[d]["status"] not in CLOSED]
                out.append(f"| {md_link(t, base)} | {esc(t['title'])} | {t['type']} | {t['priority']} | {t['size']} | {t['owner']} | {', '.join(waiting) or '—'} |")
        out.append("")
    bugs = sorted(ph.bugs(), key=lambda i: (i["status"] in CLOSED, i["severity"], i.id))
    out += [f"## Bugs & gaps ({sum(1 for b in bugs if b.is_open_bug())} open / {len(bugs)} total)", ""]
    if bugs:
        out += ["| ID | Severity | Title | Status | Found in |", "|---|---|---|---|---|"]
        for b in bugs:
            out.append(f"| {md_link(b, base)} | {b['severity']} | {esc(b['title'])} | {b['status']} | {esc(b['found_in'])} |")
    else:
        out.append("_None._")
    out.append("")
    return "\n".join(out)


def render_root(phases, items) -> str:
    ov = overall(phases)
    allt = [i for i in items.values() if i["kind"] in ("task", "chore")]
    mark = "tools/kanban/brand/ceranova-mark-128.png"
    sig = ([f'<sub><img src="{mark}" width="16" height="16" alt=""> Managed with [{KIT_NAME}]({KIT_URL})</sub>', ""]
           if (ROOT / mark).exists() and (CFG.get("brand") or {}).get("attribution", True) else [])
    out = [f"# {PROJECT} · Project Kanban", "", *sig,
           "> Generated by `./kanban build` from `tracking/`. Do not edit. **Open [`kanban.html`](kanban.html)** for the interactive board (`./kanban open`), or read the per-phase boards below.", "",
           f"**Overall:** `{bar(seg=ov, width=30)}` **{ov['pct']:.0f}%** · {len(allt)} tasks · "
           f"{sum(1 for i in allt if i['status'] == 'done')} done · {sum(1 for i in allt if i['status'] == 'in_progress')} in progress · "
           f"{sum(1 for i in allt if i['status'] == 'blocked')} blocked · {sum(1 for i in items.values() if i.is_open_bug())} open bugs/gaps", "",
           f"_Updated {stamp()} UTC._", "",
           "## Phases", "",
           "| Phase | Status | Progress | Tasks (done/total) | In progress | Blocked | Open bugs S1/S2 | Exit criteria | Board |",
           "|---|---|---|---|---|---|---|---|---|"]
    for n, ph in phases.items():
        pr, c, ob = ph.progress(), ph.counts(), ph.open_bugs()
        tot = sum(v for k, v in c.items() if k != "cancelled")
        ed, et = ph.exit_criteria()
        out.append(f"| **P{n}** {esc(ph.title)} | `{ph.meta.get('status', 'not_started')}` | `{bar(ph, width=16)}` {pr['pct']:.0f}% | "
                   f"{c['done']}/{tot} | {c['in_progress']} | {c['blocked']} | {ob['S1']}/{ob['S2']} | {ed}/{et} | [BOARD](tracking/phase-{n}/BOARD.md) |")
    out.append("")

    def lst(title, rows, fmt):
        out.extend([f"## {title} ({len(rows)})", ""])
        out.extend([fmt(r) for r in rows] or ["_None._"])
        out.append("")

    lk = lambda i: f"[{i.id}]({rel(i.path)})"
    lst("In progress", sorted([i for i in items.values() if i["status"] == "in_progress"], key=lambda i: i.id),
        lambda i: f"- {lk(i)} {i['title']} · {i.todo()[0]}/{i.todo()[1]} · _{i['checkpoint'] or 'no checkpoint'}_{' · ⚠️ stale' if i.stale() else ''}")
    lst("Blocked", sorted([i for i in items.values() if i["status"] == "blocked"], key=lambda i: i.id),
        lambda i: f"- {lk(i)} {i['title']} · {i['blocked_reason']}")
    lst("Next up (ready, top 12)", next_items(phases, items)[:12],
        lambda i: f"- {lk(i)} `{i['type']}` {i['title']} · {i['priority']}")
    lst("Open S1/S2 bugs", sorted([i for i in items.values() if i.is_open_bug() and i["severity"] in ("S1", "S2")], key=lambda i: i.id),
        lambda i: f"- {lk(i)} **{i['severity']}** {i['title']}")
    pend = docsync_pending(phases, items)
    lst("Doc sync pending", pend, lambda x: f"- {x}")
    out += ["## How this works", "",
            "- Item files: `tracking/phase-N/tasks/*.md` and `bugs/*.md` ([schema](tracking/SCHEMA.md), [guide](tracking/README.md)).",
            "- Agents follow [AGENTS.md](AGENTS.md); hooks in `.claude/settings.json` and `tools/kanban/githooks/` re-triage and rebuild these boards.",
            "- Roadmap: [docs/roadmap/](docs/roadmap/README.md).", ""]
    return "\n".join(out)


def docsync_pending(phases, items):
    rows = []
    for i in sorted(items.values(), key=lambda i: i.id):
        if i["doc_sync_status"] == "pending":
            rows.append(f"[{i.id}]({rel(i.path)}) {i['title']} → " + ", ".join(f"`{d}`" for d in (i["doc_sync"] or [])))
    for n, ph in phases.items():
        if ph.meta.get("doc_sync_status") == "pending":
            rows.append(f"Phase {n} completed → mark done in `docs/roadmap/README.md`, `docs/04-plan-of-action.md`, `SPEC.md` phases table (`./kanban docsync P{n} --done`)")
    return rows


def render_docsync(phases, items) -> str:
    rows = docsync_pending(phases, items)
    return "\n".join(["# Doc sync queue", "",
                      "> Generated. Items completed whose listed docs must be updated to match the code. "
                      "Update the docs, then run `./kanban docsync <ID> --done`.", ""] +
                     ([f"- [ ] {r}" for r in rows] or ["_Nothing pending._"]) + [""])


def next_items(phases, items, phase=None, owner=None):
    prio = {p: i for i, p in enumerate(PRIORITIES)}
    dependents = {}
    for i in items.values():
        for d in i["depends_on"] or []:
            dependents[d] = dependents.get(d, 0) + 1
    rows = [i for i in items.values() if i["status"] == "ready"
            and (phase is None or str(i["phase"]) == str(phase)) and (owner is None or i["owner"] == owner)]
    return sorted(rows, key=lambda i: (int(i["phase"]), prio.get(i["priority"], 9), -dependents.get(i.id, 0), i.id))


# ---------------------------------------------------------------- render: html

def html_data(phases, items):
    ph_rows = []
    for n, ph in phases.items():
        ed, et = ph.exit_criteria()
        road = roadmap_doc(n, ph)
        ph_rows.append({"n": n, "title": ph.title, "status": ph.meta.get("status", "not_started"),
                        "open": phase_open(ph, phases), "progress": ph.progress(), "counts": ph.counts(),
                        "bugs": ph.open_bugs(), "exit": [ed, et], "roadmap": rel(road) if road else "",
                        "board": f"tracking/phase-{n}/BOARD.md", "body": ph.body})
    its = []
    for i in sorted(items.values(), key=lambda i: i.id):
        d, t = i.todo()
        ad, at = i.acceptance()
        waiting = [x for x in (i["depends_on"] or []) if x in items and items[x]["status"] not in CLOSED]
        its.append({k: i[k] for k in ("id", "kind", "title", "phase", "type", "status", "priority", "size", "severity",
                                      "owner", "claimed_by", "depends_on", "requirements", "roadmap_todos", "modules",
                                      "dashboards", "branch", "pr", "doc_sync", "doc_sync_status", "found_in", "created",
                                      "updated", "started", "completed", "blocked_reason", "checkpoint")}
                   | {"todo": [d, t], "acc": [ad, at], "waiting": waiting, "stale": i.stale(), "path": rel(i.path),
                      "requires": effective_requires(i),
                      "body": i.body, "last": (i.last_log() or [""])[0]})
    sessions = []
    sf = TRACK / "SESSIONS.md"
    if sf.exists():
        sessions = [l for l in sf.read_text().splitlines() if l.startswith("- ")][-15:]
    return {"generated": stamp() + " UTC", "overall": overall(phases), "phases": ph_rows, "items": its,
            "docsync": docsync_pending(phases, items), "sessions": sessions}


SKIP_DIRS = {".git", "node_modules", ".venv", "venv", "__pycache__", "dist", "build", "target", ".next",
             "tracking", ".claude", ".agents", ".github", "vendor", "third_party", ".idea", ".vscode"}
KIT_FILES = {"kanban", "KANBAN.md", "kanban.html", "CLAUDE.md", "AGENTS.md", "GEMINI.md", "README.md",
             "LICENSE", ".gitignore", ".gitattributes", "install.sh", "install.py"}
EXT_GROUPS = {
    "code": {".py", ".js", ".ts", ".tsx", ".jsx", ".go", ".rs", ".java", ".kt", ".swift", ".c", ".cc", ".cpp", ".h",
             ".cs", ".rb", ".php", ".scala", ".dart", ".vue", ".svelte", ".lua", ".ex", ".exs", ".sql"},
    "video": {".mp4", ".mov", ".mxf", ".mkv", ".prproj", ".fcpxml", ".drp", ".aep", ".edl", ".r3d", ".braw", ".otio"},
    "audio": {".wav", ".aif", ".aiff", ".flac", ".mp3", ".als", ".ptx", ".rpp", ".flp", ".logicx", ".omf", ".aaf", ".sesx"},
    "data": {".ipynb", ".parquet", ".h5", ".hdf5", ".pkl", ".onnx", ".safetensors", ".pt", ".ckpt", ".feather", ".arrow"},
    "paper": {".tex", ".bib", ".cls", ".bst"},
    "prose": {".md", ".mdx", ".rst", ".adoc", ".txt"},
    "design": {".fig", ".sketch", ".xd", ".psd", ".ai", ".afdesign", ".afphoto", ".penpot", ".indd"},
}
MANIFESTS = {"package.json", "pyproject.toml", "requirements.txt", "setup.py", "Cargo.toml", "go.mod", "pom.xml",
             "build.gradle", "build.gradle.kts", "Gemfile", "composer.json", "pubspec.yaml", "mix.exs", "Package.swift"}
DOC_SITES = {"mkdocs.yml", "docusaurus.config.js", "docusaurus.config.ts", "book.toml", "_config.yml", "antora.yml"}
GAME_MARKERS = {"project.godot", "ProjectVersion.txt"}


def detect_project_type() -> tuple:
    """Best-effort project type from repo contents: (type, [signals]). Config `project_type` overrides it elsewhere."""
    counts = {k: 0 for k in EXT_GROUPS}
    names, meaningful, scanned = set(), 0, 0
    for dirpath, dirnames, filenames in os.walk(ROOT):
        rel_dir = Path(dirpath).relative_to(ROOT)
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS and not (rel_dir == Path("docs") and d == "pm")
                       and not (rel_dir == Path("tools") and d == "kanban")]
        for fn in filenames:
            scanned += 1
            if scanned > 20000:
                break
            names.add(fn)
            if fn in KIT_FILES and rel_dir == Path("."):
                continue
            meaningful += 1
            ext = os.path.splitext(fn)[1].lower()
            for k, exts in EXT_GROUPS.items():
                if ext in exts:
                    counts[k] += 1
            if fn.endswith(".uproject") or fn.endswith(".unity"):
                names.add("UNREAL_OR_UNITY")
    signals, kinds = [], []
    if meaningful < 5:
        return "greenfield", [f"only {meaningful} project file(s) besides the kit"]
    if names & GAME_MARKERS or "UNREAL_OR_UNITY" in names:
        kinds.append("game"); signals.append("game engine project files")
    if counts["video"] >= 3:
        kinds.append("media-video"); signals.append(f"{counts['video']} video/edit files")
    if counts["audio"] >= 3:
        kinds.append("media-audio"); signals.append(f"{counts['audio']} audio/session files")
    if counts["data"] >= 2 or "dvc.yaml" in names:
        kinds.append("data-ml"); signals.append(f"{counts['data']} notebook/model/data files")
    code = counts["code"] >= 10 or bool(names & MANIFESTS)
    if code and not kinds:
        kinds.append("software"); signals.append(f"{counts['code']} code files" + (", manifests: " + ", ".join(sorted(names & MANIFESTS)) if names & MANIFESTS else ""))
    elif code:
        signals.append(f"also {counts['code']} code files")
    if counts["paper"] >= 1 and not code:
        kinds.append("research"); signals.append(f"{counts['paper']} LaTeX/BibTeX files")
    if counts["design"] >= 2 and not code:
        kinds.append("design"); signals.append(f"{counts['design']} design files")
    if not kinds and (counts["prose"] >= 10 or names & DOC_SITES):
        kinds.append("docs"); signals.append(f"{counts['prose']} prose files" + (" + docs site config" if names & DOC_SITES else ""))
    if not kinds:
        return ("greenfield" if meaningful < 15 else "mixed"), signals or [f"{meaningful} files, no strong signal"]
    return (kinds[0] if len(kinds) == 1 else "mixed"), signals + ([f"types: {', '.join(kinds)}"] if len(kinds) > 1 else [])


def project_type() -> str:
    return CFG.get("project_type") or detect_project_type()[0]


LOGO_CANDIDATES = ["brand/logo.svg", "brand/mark.svg", "brand/logo.png", "logo.svg", "logo.png", "assets/logo.svg",
                   "assets/logo.png", "public/logo.svg", "public/logo.png", "static/logo.svg", "static/logo.png",
                   "docs/logo.svg", "docs/logo.png", ".github/logo.svg", ".github/logo.png", "icon.svg",
                   "public/favicon.svg", "assets/icon.png"]


def _data_uri(p: Path) -> str:
    import base64
    mime = {".svg": "image/svg+xml", ".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".webp": "image/webp"}.get(p.suffix.lower())
    if not mime or not p.exists() or p.stat().st_size > 300_000:
        return ""
    return f"data:{mime};base64," + base64.b64encode(p.read_bytes()).decode()


def project_logo() -> str:
    brand = CFG.get("brand") or {}
    if brand.get("logo") is False:
        return ""
    paths = [brand["logo"]] if brand.get("logo") else LOGO_CANDIDATES
    for rp in paths:
        uri = _data_uri(ROOT / rp)
        if uri:
            return uri
    return ""


BRAND_DIR = Path(__file__).resolve().parent / "brand"
FONT_FACES = [("Bebas Neue", "BebasNeue-Regular.woff2", "400", "normal"), ("DM Sans", "DMSans-Variable.woff2", "300 700", "normal"),
              ("Space Mono", "SpaceMono-Regular.woff2", "400", "normal")]


def kit_mark() -> str:
    for name in ("ceranova-mark.svg", "ceranova-mark-128.png", "ceranova-mark.png"):
        uri = _data_uri(BRAND_DIR / name)
        if uri:
            return uri
    return ""


def kit_fonts_css() -> str:
    """The CeraNova PM fonts (SIL OFL, see tools/kanban/brand/fonts/) embedded, so the board works offline."""
    import base64
    out = []
    for family, fn, weight, style in FONT_FACES:
        f = BRAND_DIR / "fonts" / fn
        if f.exists():
            out.append(f"@font-face{{font-family:\"{family}\";src:url(data:font/woff2;base64,{base64.b64encode(f.read_bytes()).decode()}) "
                       f"format(\"woff2\");font-weight:{weight};font-style:{style};font-display:swap}}")
    return "".join(out)


def render_html(phases, items) -> str:
    tpl = (Path(__file__).parent / "board_template.html").read_text()
    data = json.dumps(html_data(phases, items), ensure_ascii=False).replace("</", "<\\/")
    brand = CFG.get("brand") or {}
    css = ""
    if brand.get("accent"):  # optional override of the CeraNova red (primary accent)
        css += f":root,:root[data-theme]{{--red:{brand['accent']};--red-light:{brand['accent']};--accent:{brand['accent']};}}"
    if brand.get("accent2"):  # optional override of the CeraNova gold (secondary accent)
        css += f":root,:root[data-theme]{{--gold:{brand['accent2']};--gold-light:{brand['accent2']};--brand:{brand['accent2']};}}"
    name = PROJECT.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    logo = project_logo()
    logo_html = f'<img class="plogo" src="{logo}" alt="">' if logo else f'<span class="plogo txt">{(name[:1] or "P").upper()}</span>'
    mark = kit_mark()
    kitmark_html = f'<img class="mark" src="{mark}" alt="CeraNova">' if mark else '<span class="markdot"></span>'
    favicon = f'<link rel="icon" href="{mark}">' if mark else ""
    mark_html = f'<img class="kitmark" src="{mark}" alt="">' if mark else '<span class="kitdot"></span>'
    credit = (f'<a class="credit" href="{KIT_URL}" target="_blank" rel="noopener">{mark_html}<span>Powered by <b>{KIT_NAME}</b></span></a>'
              if brand.get("attribution", True) else "")
    fonts = kit_fonts_css() if brand.get("fonts", True) else ""
    return (tpl.replace("/*__DATA__*/null", data).replace("__PROJECT__", name).replace("__LOGO__", logo_html)
               .replace("__KITMARK__", kitmark_html).replace("__FAVICON__", favicon).replace("/*__FONTS__*/", fonts)
               .replace("__CREDIT__", credit).replace("__KIT_NAME__", KIT_NAME).replace("/*__BRAND__*/", css))


# ---------------------------------------------------------------- roadmap blocks

def replace_block(text: str, name: str, content: str) -> str:
    start, end = f"<!-- kanban:{name}:start -->", f"<!-- kanban:{name}:end -->"
    if start not in text:
        return text
    a = text.index(start) + len(start)
    b = text.index(end)
    return text[:a] + "\n" + content.strip("\n") + "\n" + text[b:]


def roadmap_blocks(phases):
    readme = ROOT / CFG["roadmap_index"]
    if not readme.exists():
        return
    s = readme.read_text()
    # phase status
    rows = ["| Phase | Status | Progress | Tasks done/total | Board |", "|---|---|---|---|---|"]
    for n, ph in phases.items():
        c = ph.counts()
        tot = sum(v for k, v in c.items() if k != "cancelled")
        pr = ph.progress()
        rows.append(f"| P{n} {ph.title} | `{ph.meta.get('status', 'not_started')}` | `{bar(ph, width=16)}` {pr['pct']:.0f}% | {c['done']}/{tot} | [BOARD](../../tracking/phase-{n}/BOARD.md) |")
    s = replace_block(s, "phase-status", "\n".join(rows))
    # counts + user register from roadmap docs
    types = ["USER", "BUILD", "OPS", "VERIFY", "RUN"]
    crow, reg, tot = [], [], {t: 0 for t in types}
    for f in sorted(ROADMAP.glob("phase-*.md"), key=lambda f: int(re.match(r"phase-(\d+)", f.name).group(1)) if re.match(r"phase-(\d+)-", f.name) else 10**6):
        mm = re.match(r"phase-(\d+)-", f.name)
        if not mm:
            continue
        txt = f.read_text()
        n = mm.group(1)
        first = (txt.splitlines() or [""])[0].lstrip("# ").strip()
        title = first.split("·", 1)[1].strip() if "·" in first else first
        c = {t: len(re.findall(rf"\*\*T\d+\.\d+\*\* `{t}`", txt)) for t in types}
        nreq = len(set(re.findall(r"^\| (R\d+\.N?\d+) ", txt, re.M)))
        for t in types:
            tot[t] += c[t]
        crow.append(f"| [P{n} {title}]({f.name}) | {nreq} | " + " | ".join(str(c[t]) for t in types) + f" | {sum(c.values())} |")
        for m in re.finditer(r"^- \[[ xX]\] \*\*(T\d+\.\d+)\*\* `USER` (.*)$", txt, re.M):
            tid, body = m.groups()
            act, sep, ref = body.rpartition(" → ")
            if not sep:
                act, ref = body, ""
            reg.append(f"| {tid} | P{n} | {act.strip()} | {ref.strip() or '—'} |")
    counts = ("| Phase | Requirements | `USER` | `BUILD` | `OPS` | `VERIFY` | `RUN` | ToDos |\n|---|---|---|---|---|---|---|---|\n"
              + "\n".join(crow) + "\n| **Total** | | " + " | ".join(f"**{tot[t]}**" for t in types) + f" | **{sum(tot.values())}** |")
    s = replace_block(s, "roadmap-counts", counts)
    s = replace_block(s, "user-register", "| ID | Phase | Action | Feeds / blocks |\n|---|---|---|---|\n" + "\n".join(reg))
    if s != readme.read_text():
        readme.write_text(s)


# ---------------------------------------------------------------- build

def build(quiet=True, force=False):
    phases, items, errs = load()
    if (STATE / "paused").exists() and not force:  # bulk edits in progress: no triage/rewrites until `pause --off`
        if not quiet:
            print("kanban paused: skipped triage/build (run `./kanban pause --off && ./kanban build`)")
        return phases, items, errs
    triage(phases, items, quiet=quiet)
    written = []
    for n, ph in phases.items():
        if ph.file.exists() or ph.items:
            p = ph.dir / "BOARD.md"
            write_if_changed(p, render_board(ph, items, phases), written)
    write_if_changed(ROOT / "KANBAN.md", render_root(phases, items), written)
    write_if_changed(ROOT / "kanban.html", render_html(phases, items), written)
    write_if_changed(TRACK / "DOC_SYNC.md", render_docsync(phases, items), written)
    roadmap_blocks(phases)
    save_fingerprint()
    if not quiet:
        print(f"built {len(written)} file(s): " + ", ".join(written) if written else "boards up to date")
    return phases, items, errs


def strip_volatile(s: str) -> str:
    return re.sub(r"(_Updated |\"generated\": \")[^_\"]*", "", s)


def write_if_changed(p: Path, content: str, written: list):
    if p.exists() and strip_volatile(p.read_text()) == strip_volatile(content):
        return
    p.write_text(content)
    written.append(rel(p))


def fingerprint() -> str:
    acc = []
    for p in sorted(TRACK.rglob("*.md")):
        if p.name in ("BOARD.md", "DOC_SYNC.md"):
            continue
        st = p.stat()
        acc.append(f"{p}:{st.st_mtime_ns}:{st.st_size}")
    tpl = Path(__file__).parent / "board_template.html"
    acc.append(f"{tpl.stat().st_mtime_ns}" if tpl.exists() else "")
    return hashlib.sha256("\n".join(acc).encode()).hexdigest()


def save_fingerprint():
    STATE.mkdir(parents=True, exist_ok=True)
    (STATE / "fingerprint").write_text(fingerprint())


def changed_since_build() -> bool:
    f = STATE / "fingerprint"
    return not f.exists() or f.read_text() != fingerprint()


# ---------------------------------------------------------------- commands

def get(items, iid) -> Item:
    if iid not in items:
        sys.exit(f"unknown item {iid}")
    return items[iid]


def set_status(it: Item, status: str, note: str, extra: dict | None = None):
    upd = {"status": status, "updated": today()} | (extra or {})
    write_meta(it.path, upd)
    it.meta.update(upd)
    append_log(it.path, note)


def cmd_start(a):
    phases, items, _ = load()
    it = get(items, a.id)
    if it["status"] not in ("ready", "blocked", "backlog", "review", "in_progress") and not a.force:
        sys.exit(f"{a.id} is {it['status']}; use --force to restart")
    if not deps_done(it, items) and not a.force:
        waiting = [d for d in it["depends_on"] if items[d]["status"] not in CLOSED]
        sys.exit(f"{a.id} waits on {', '.join(waiting)} (use --force to override)")
    rows = preflight(it)
    missing = [f"{f} {n}" for f, n, st in rows if st == "missing"]
    if missing and not a.force:
        print(format_preflight(it, rows))
        sys.exit(f"{a.id} needs {', '.join(missing)} on this machine. Install or provide them and retry; or block it "
                 f"(`./kanban block {a.id} --reason \"needs {missing[0]}\"`) and raise a USER task for the human "
                 f"(`./kanban new --phase {it['phase']} --type USER --title \"Provide {missing[0]}\"`). --force starts anyway.")
    extra = {"claimed_by": env_label(), "blocked_reason": ""}
    if not it["started"]:
        extra["started"] = today()
    set_status(it, "in_progress", "started" + (f" ({a.note})" if a.note else ""), extra)
    print(f"{a.id} → in_progress. Branch: {it['branch']}")
    if rows:
        print(format_preflight(it, rows))
    if a.git and it["branch"]:
        r = subprocess.run(["git", "switch", it["branch"]], cwd=ROOT, capture_output=True, text=True)
        if r.returncode:
            subprocess.run(["git", "switch", "-c", it["branch"]], cwd=ROOT, check=False)
    build()


def cmd_checkpoint(a):
    _, items, _ = load()
    it = get(items, a.id)
    write_meta(it.path, {"checkpoint": a.note[:160], "updated": today()})
    append_log(it.path, "checkpoint: " + a.note)
    print(f"{a.id} checkpoint saved")
    build()


def cmd_tick(a):
    _, items, _ = load()
    it = get(items, a.id)
    text = it.path.read_text()
    boxes = [m for m in re.finditer(r"^(\s*)- \[ \] (.*)$", text, re.M)]
    target = None
    if a.which.isdigit():
        idx = int(a.which) - 1
        if 0 <= idx < len(boxes):
            target = boxes[idx]
    else:
        target = next((m for m in boxes if a.which.lower() in m.group(2).lower()), None)
    if not target:
        sys.exit("no matching unticked box")
    text = text[:target.start()] + target.group(1) + "- [x] " + target.group(2) + text[target.end():]
    it.path.write_text(text)
    write_meta(it.path, {"updated": today()})
    print(f"ticked: {target.group(2)}")
    build()


def cmd_review(a):
    _, items, _ = load()
    it = get(items, a.id)
    extra = {"pr": a.pr} if a.pr else {}
    set_status(it, "review", "ready for review" + (f": {a.pr}" if a.pr else ""), extra)
    print(f"{a.id} → review")
    build()


def cmd_reviewed(a):
    """Record an independent review verdict (pm-review). A fail sends the item back to in_progress with the findings."""
    _, items, _ = load()
    it = get(items, a.id)
    who = env_label()
    if it["claimed_by"] and it["claimed_by"] == who:
        print(f"note: {a.id} was built in this same session; a review by a separate agent or session is stronger.")
    if a.result == "pass":
        write_meta(it.path, {"review_result": "pass", "updated": today()})
        append_log(it.path, f"review pass: {a.note}")
        print(f"{a.id}: review passed")
    else:
        set_status(it, "in_progress", f"review fail: {a.note}",
                   {"review_result": "fail", "checkpoint": f"review failed: {a.note}"[:200]})
        print(f"{a.id}: review failed → in_progress (findings in the progress log and checkpoint)")
    build()


def cmd_done(a):
    phases, items, _ = load()
    it = get(items, a.id)
    d, t = it.todo()
    ad, at = it.acceptance()
    problems = []
    if d != t:
        problems.append(f"{t - d} unticked ToDo box(es)")
    if ad != at:
        problems.append(f"{at - ad} unticked acceptance box(es)")
    log = section(it.body, "## Progress log").lower()
    if not a.evidence and "verified:" not in log:
        problems.append("no verification evidence (pass --evidence \"what was run and the result\")")
    if not deps_done(it, items):
        problems.append("dependencies not done")
    if CFG.get("require_review") and it["review_result"] != "pass" and it["kind"] == "task":
        problems.append("no passing review (run the pm-review skill: `./kanban reviewed <ID> --pass|--fail`)")
    if problems and not a.force:
        sys.exit(f"{a.id} can't be done: " + "; ".join(problems))
    if a.evidence:
        append_log(it.path, "verified: " + a.evidence)
    extra = {"completed": today(), "checkpoint": ""}
    if it["doc_sync"]:
        extra["doc_sync_status"] = "pending"
    set_status(it, "done", "done" + (" (forced: " + "; ".join(problems) + ")" if problems else ""), extra)
    print(f"{a.id} → done" + ("; doc sync pending for " + ", ".join(it["doc_sync"]) if it["doc_sync"] else ""))
    build(quiet=False)


def cmd_block(a):
    _, items, _ = load()
    it = get(items, a.id)
    set_status(it, "blocked", "blocked: " + a.reason, {"blocked_reason": a.reason})
    print(f"{a.id} → blocked")
    build()


def cmd_unblock(a):
    phases, items, _ = load()
    it = get(items, a.id)
    st = "in_progress" if it["started"] and not a.ready else ("ready" if deps_done(it, items) else "backlog")
    set_status(it, st, "unblocked", {"blocked_reason": ""})
    print(f"{a.id} → {st}")
    build()


def cmd_cancel(a):
    _, items, _ = load()
    it = get(items, a.id)
    set_status(it, "cancelled", "cancelled: " + a.reason, {"completed": today()})
    print(f"{a.id} → cancelled")
    build()


def cmd_reopen(a):
    _, items, _ = load()
    it = get(items, a.id)
    set_status(it, "ready", "reopened: " + a.reason, {"completed": "", "doc_sync_status": "n/a"})
    print(f"{a.id} → ready")
    build()


def slugify(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")[:48]


def cmd_new(a):
    phases, items, _ = load()
    kind = a.kind
    letter = "B" if kind in ("bug", "gap") else "T"
    if a.phase not in phases:
        sys.exit(f"phase {a.phase} doesn't exist; create it with `./kanban phase-add --title \"…\"`")
    ph = phases[a.phase]
    nums = [int(ID_RE.match(i.id).group(3)) for i in ph.items if ID_RE.match(i.id) and ID_RE.match(i.id).group(2) == letter]
    iid = f"P{a.phase}-{letter}{(max(nums) + 1 if nums else 1):03d}"
    tpl = (TRACK / "templates" / ("bug.md" if letter == "B" else "task.md")).read_text()
    tpl = tpl.replace("P0-B000" if letter == "B" else "P0-T000", iid)
    slug = slugify(a.title)
    tpl = re.sub(r"p0/" + iid + r"-short-slug", f"p{a.phase}/{iid}-{slug}", tpl)
    tpl = tpl.replace("Short imperative title", a.title).replace("Short description of the defect or gap", a.title)
    tpl = re.sub(r"^- \d{4}-\d{2}-\d{2} \d{2}:\d{2} · planner · created$", f"- {stamp()} · {env_label()} · created", tpl, flags=re.M)
    tpl = re.sub(r"^- \d{4}-\d{2}-\d{2} \d{2}:\d{2} · reporter · opened$", f"- {stamp()} · {env_label()} · opened", tpl, flags=re.M)
    d = ph.dir / ("bugs" if letter == "B" else "tasks")
    d.mkdir(parents=True, exist_ok=True)
    path = d / f"{iid}-{slug}.md"
    path.write_text(tpl)
    upd = {"phase": a.phase, "kind": kind, "type": a.type, "created": today(), "updated": today(),
           "priority": a.priority, "owner": "user" if a.type == "USER" else "agent"}
    if letter == "B":
        upd.update(severity=a.severity, found_in=a.found_in or "")
    if a.depends:
        upd["depends_on"] = a.depends.split(",")
    write_meta(path, upd)
    print(rel(path))
    build()


def cmd_docsync(a):
    phases, items, _ = load()
    if re.fullmatch(r"P\d", a.id):
        ph = phases[int(a.id[1])]
        write_meta(ph.file, {"doc_sync_status": "done" if a.done else "pending", "updated": today()})
    else:
        it = get(items, a.id)
        write_meta(it.path, {"doc_sync_status": "done" if a.done else "pending", "updated": today()})
        append_log(it.path, "doc sync " + ("done" if a.done else "re-opened") + (f": {a.note}" if a.note else ""))
    print(f"{a.id} doc sync → {'done' if a.done else 'pending'}")
    build()


def cmd_validate(a):
    phases, items, errs = load()
    errors, warns = validate(phases, items, errs)
    if a.phase is not None:
        pre = (f"tracking/phase-{a.phase}/",)
        errors = [e for e in errors if e.startswith(pre) or "cycle" in e]
        warns = [w for w in warns if w.startswith(pre)]
    for w in warns if not a.quiet else []:
        print("warn: " + w)
    for e in errors:
        print("ERROR: " + e)
    print(f"{len(items)} items · {len(errors)} error(s) · {len(warns)} warning(s)")
    sys.exit(1 if errors else 0)


def cmd_build(a):
    _, _, errs = build(quiet=False, force=True)
    for e in errs:
        print("ERROR: " + e)
    if a.check:
        r = subprocess.run(["git", "status", "--porcelain", "--", "KANBAN.md", "kanban.html", "tracking", CFG["roadmap_index"]],
                           cwd=ROOT, capture_output=True, text=True)
        if r.stdout.strip():
            print("generated files are out of date:\n" + r.stdout)
            sys.exit(1)


def cmd_list(a):
    _, items, _ = load()
    for i in sorted(items.values(), key=lambda i: i.id):
        if a.phase is not None and str(i["phase"]) != str(a.phase):
            continue
        if a.status and i["status"] != a.status:
            continue
        if a.type and i["type"] != a.type:
            continue
        if a.kind and i["kind"] != a.kind and not (a.kind == "gap" and i["kind"] == "bug" and a.include_bugs):
            continue
        if a.severity and i["severity"] != a.severity:
            continue
        if a.grep and not all(w in (i["title"] + "\n" + i.body).lower() for w in a.grep.lower().split()):
            continue
        d, t = i.todo()
        print(f"{i.id:9} {i['status']:12} {i['type']:6} {i['priority']:8} {d:>2}/{t:<2} {i['title']}")


def cmd_show(a):
    _, items, _ = load()
    print(get(items, a.id).path.read_text())


def cmd_next(a):
    phases, items, _ = load()
    rows = next_items(phases, items, a.phase, a.owner)[: a.n]
    for i in rows:
        print(f"{i.id:9} {i['type']:6} {i['priority']:8} {i['title']}  ({rel(i.path)})")
    if not rows:
        print("nothing ready" + (f" in phase {a.phase}" if a.phase is not None else ""))


def brief(phases, items) -> str:
    out = [f"## {PROJECT} kanban: resume brief ({env_label()})", ""]
    ov = overall(phases)
    out.append(f"Overall {ov['pct']:.0f}% · " + " · ".join(
        f"P{n} {p.progress()['pct']:.0f}% ({p.meta.get('status', '?')})" for n, p in phases.items()))
    inprog = [i for i in items.values() if i["status"] in ("in_progress", "review")]
    out.append("")
    out.append("**In progress / review (resume these first):**" if inprog else "**Nothing in progress.**")
    for i in sorted(inprog, key=lambda i: i.id):
        d, t = i.todo()
        out.append(f"- {i.id} [{i['status']}] {i['title']} · ToDo {d}/{t} · branch `{i['branch']}` · claimed by {i['claimed_by'] or '—'}")
        out.append(f"  checkpoint: {i['checkpoint'] or '—'}")
        for l in i.last_log(2):
            out.append(f"  log: {l[2:]}")
    blocked = [i for i in items.values() if i["status"] == "blocked"]
    if blocked:
        out.append("**Blocked:** " + "; ".join(f"{i.id} ({i['blocked_reason']})" for i in blocked))
    pend = docsync_pending(phases, items)
    if pend:
        out.append("**Doc sync pending:** " + "; ".join(re.sub(r"\]\([^)]*\)", "]", p) for p in pend))
    nxt = next_items(phases, items)[:5]
    if nxt:
        out.append("**Next ready:** " + "; ".join(f"{i.id} {i['title']}" for i in nxt))
    bugs = [i for i in items.values() if i.is_open_bug() and i["severity"] in ("S1", "S2")]
    if bugs:
        bugs = sorted(bugs, key=lambda i: (i["severity"], i.id))
        shown = "; ".join(f"{i.id} {i['title']}" for i in bugs[:6])
        out.append(f"**Open S1/S2 bugs ({len(bugs)}):** {shown}" + (f"; … +{len(bugs) - 6} more (see KANBAN.md)" if len(bugs) > 6 else ""))
    steps = lifecycle_steps(phases, items)
    out.append("**Lifecycle next:** " + " → ".join(f"{k} ({w})" for k, w in steps[:3]))
    out += ["", "Protocol: AGENTS.md. Claim with `./kanban start <ID>`, checkpoint with `./kanban checkpoint <ID> \"…\"`, "
                "finish with `./kanban done <ID> --evidence \"…\"`, file bugs with `./kanban new --kind bug …`."]
    return "\n".join(out)


def cmd_resume(a):
    phases, items, _ = build()
    print(brief(phases, items))


def log_session(event: str, note: str = ""):
    f = TRACK / "SESSIONS.md"
    if not f.exists():
        f.write_text("# Session log\n\nAppend-only. One line per session start/end/handoff, so work can resume across cloud and local.\n\n")
    br = subprocess.run(["git", "rev-parse", "--abbrev-ref", "HEAD"], cwd=ROOT, capture_output=True, text=True).stdout.strip()
    _, items, _ = load()
    active = ",".join(sorted(i.id for i in items.values() if i["status"] == "in_progress")) or "—"
    with f.open("a") as fh:
        fh.write(f"- {stamp()} · {event} · {env_label()} · branch {br or '?'} · active {active}" + (f" · {note}" if note else "") + "\n")


def cmd_session(a):
    log_session(a.event, a.note or "")
    print("logged")


def cmd_pause(a):
    STATE.mkdir(parents=True, exist_ok=True)
    f = STATE / "paused"
    if a.off:
        f.unlink(missing_ok=True)
        print("kanban hooks resumed")
    else:
        f.write_text(stamp())
        print("kanban hooks paused (run `./kanban pause --off` to resume)")


def ensure_git_hooks():
    """Point git at tools/kanban/githooks if it isn't already (fresh clones, new cloud containers)."""
    r = subprocess.run(["git", "config", "--get", "core.hooksPath"], cwd=ROOT, capture_output=True, text=True)
    if r.returncode == 0 or not (ROOT / ".git").exists():
        return False
    subprocess.run(["git", "config", "core.hooksPath", "tools/kanban/githooks"], cwd=ROOT, check=False)
    return True


def cmd_install_hooks(a):
    subprocess.run(["git", "config", "core.hooksPath", "tools/kanban/githooks"], cwd=ROOT, check=True)
    for p in (Path(__file__).parent / "githooks").iterdir():
        p.chmod(0o755)
    print("git hooks installed (core.hooksPath = tools/kanban/githooks)")


def cmd_open(a):
    build()
    path = ROOT / "kanban.html"
    print(path)
    for opener in (["xdg-open"], ["open"], ["cmd", "/c", "start", ""]):
        try:
            subprocess.Popen(opener + [str(path)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return
        except (FileNotFoundError, OSError):
            continue


def cmd_serve(a):
    build()
    import functools
    import http.server
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(ROOT))
    print(f"serving http://127.0.0.1:{a.port}/kanban.html  (Ctrl-C to stop)")
    http.server.ThreadingHTTPServer(("127.0.0.1", a.port), handler).serve_forever()


# ---------------------------------------------------------------- project setup (CeraNova PM)

def create_phase(n: int, title: str, opens_after: list, roadmap_rel: str = "") -> Path:
    d = TRACK / f"phase-{n}"
    (d / "tasks").mkdir(parents=True, exist_ok=True)
    (d / "bugs").mkdir(exist_ok=True)
    f = d / "PHASE.md"
    if f.exists():
        return f
    tpl = (TRACK / "templates" / "phase.md").read_text()
    tpl = re.sub(r"^# Phase \d+ · .*$", f"# Phase {n} · {title}", tpl, count=1, flags=re.M)
    f.write_text(tpl)
    write_meta(f, {"phase": n, "title": title, "roadmap": roadmap_rel, "opens_after": opens_after,
                   "status": "not_started", "updated": today()})
    return f


def create_roadmap_doc(n: int, title: str) -> str:
    rel_path = f"{CFG['roadmap_dir']}/phase-{n}-{slugify(title)}.md"
    dst = ROOT / rel_path
    src = ROOT / "docs" / "pm" / "templates" / "roadmap" / "phase.md"
    if not dst.exists() and src.exists():
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_text(src.read_text().replace("{{N}}", str(n)).replace("{{PHASE_TITLE}}", title)
                       .replace("{{PROJECT}}", PROJECT))
    idx = ROOT / CFG["roadmap_index"]
    idx_src = ROOT / "docs" / "pm" / "templates" / "roadmap" / "README.md"
    if not idx.exists() and idx_src.exists():
        idx.parent.mkdir(parents=True, exist_ok=True)
        idx.write_text(idx_src.read_text().replace("{{PROJECT}}", PROJECT))
    return rel_path if dst.exists() else ""


def cmd_detect(a):
    t, signals = detect_project_type()
    cfg_t = CFG.get("project_type")
    print(f"detected: {t}" + (f"   (config says: {cfg_t})" if cfg_t and cfg_t != t else ""))
    for sg in signals:
        print(f"  - {sg}")
    print("research agendas: pm-research skill, references/research-agendas.md (section for this type)")


def cmd_init(a):
    TRACK.mkdir(exist_ok=True)
    if not CONFIG_FILE.exists() or a.force:
        cfg = {k: v for k, v in DEFAULT_CONFIG.items() if k in ("project", "roadmap_dir", "roadmap_index", "types", "stale_days")}
        cfg["project"] = a.project or ROOT.name
        cfg["project_type"] = a.type or detect_project_type()[0]
        CONFIG_FILE.write_text(json.dumps(cfg, indent=2) + "\n")
        CFG.update(cfg)
        global PROJECT
        PROJECT = cfg["project"]
        print(f"wrote {rel(CONFIG_FILE)}")
    titles = [t.strip() for t in (a.phases or "").split(",") if t.strip()]
    existing = phase_numbers()
    start = (max(existing) + 1) if existing else 0
    for i, t in enumerate(titles):
        n = start + i
        road = create_roadmap_doc(n, t) if a.roadmap else ""
        create_phase(n, t, [n - 1] if n > 0 else [], road)
        print(f"created phase {n}: {t}" + (f" (roadmap {road})" if road else ""))
    if ensure_git_hooks():
        print("git hooks enabled (core.hooksPath = tools/kanban/githooks)")
    build(quiet=False, force=True)


def cmd_phase_add(a):
    existing = phase_numbers()
    n = a.number if a.number is not None else ((max(existing) + 1) if existing else 0)
    after = [int(x) for x in a.opens_after.split(",")] if a.opens_after else ([n - 1] if n > 0 else [])
    road = create_roadmap_doc(n, a.title) if a.roadmap else ""
    create_phase(n, a.title, after, road)
    print(f"phase {n}: {a.title} (opens after {after or 'nothing'})")
    build(force=True)


def _hook_cmd(root_expr: str, event: str, agent: str = "") -> str:
    return f'python3 "{root_expr}/tools/kanban/kanban.py" hook {event}' + (f" --agent {agent}" if agent else "")


GIT_ROOT = "$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
CLAUDE_HOOKS = {
    "SessionStart": [{"hooks": [{"type": "command", "command": _hook_cmd("$CLAUDE_PROJECT_DIR", "session-start"), "timeout": 30}]}],
    "PostToolUse": [{"matcher": "Write|Edit|MultiEdit|Bash|NotebookEdit",
                     "hooks": [{"type": "command", "command": _hook_cmd("$CLAUDE_PROJECT_DIR", "post-tool"), "timeout": 30}]}],
    "Stop": [{"hooks": [{"type": "command", "command": _hook_cmd("$CLAUDE_PROJECT_DIR", "stop"), "timeout": 30}]}],
}
# Session hooks per coding agent. Same three behaviours everywhere (resume brief at start, board rebuild after
# edits, doc-sync follow-up at end of turn); only the config file and the output format differ (`hook --agent`).
AGENT_HOOKS = {
    "claude": {"dir": ".claude", "file": ".claude/settings.json", "style": "groups", "events": CLAUDE_HOOKS},
    "codex": {"dir": ".codex", "file": ".codex/hooks.json", "style": "groups", "events": {
        "SessionStart": [{"matcher": "startup|resume", "hooks": [{"type": "command", "command": _hook_cmd(GIT_ROOT, "session-start", "codex"), "timeout": 30}]}],
        "PostToolUse": [{"hooks": [{"type": "command", "command": _hook_cmd(GIT_ROOT, "post-tool", "codex"), "timeout": 30}]}],
        "Stop": [{"hooks": [{"type": "command", "command": _hook_cmd(GIT_ROOT, "stop", "codex"), "timeout": 30}]}]}},
    "gemini": {"dir": ".gemini", "file": ".gemini/settings.json", "style": "groups", "events": {
        "SessionStart": [{"hooks": [{"type": "command", "name": "ceranova-pm-resume", "command": _hook_cmd("$GEMINI_PROJECT_DIR", "session-start", "gemini"), "timeout": 30000}]}],
        "AfterTool": [{"matcher": "write_file|replace|edit|run_shell_command",
                       "hooks": [{"type": "command", "name": "ceranova-pm-build", "command": _hook_cmd("$GEMINI_PROJECT_DIR", "post-tool", "gemini"), "timeout": 30000}]}],
        "AfterAgent": [{"hooks": [{"type": "command", "name": "ceranova-pm-docsync", "command": _hook_cmd("$GEMINI_PROJECT_DIR", "stop", "gemini"), "timeout": 30000}]}]}},
    "cursor": {"dir": ".cursor", "file": ".cursor/hooks.json", "style": "flat", "events": {
        "sessionStart": [{"command": _hook_cmd(GIT_ROOT, "session-start", "cursor")}],
        "afterFileEdit": [{"command": _hook_cmd(GIT_ROOT, "post-tool", "cursor")}],
        "stop": [{"command": _hook_cmd(GIT_ROOT, "stop", "cursor")}]}},
    "opencode": {"dir": ".opencode", "file": ".opencode/plugins/ceranova-pm.js", "style": "plugin",
                 "source": "tools/kanban/adapters/opencode-plugin.js"},
}
AGENT_NAMES = list(AGENT_HOOKS)
BLOCK_RE = re.compile(r"<!-- pm-kit:start.*?<!-- pm-kit:end -->\n?", re.S)
BLOCKS_DIR = ROOT / "docs" / "pm" / "templates" / "agent-blocks"


def find_doc(name: str) -> "Path | None":
    """A foundation doc by name, at the root or anywhere under docs/ (case-insensitive, ignoring templates)."""
    stem = name.lower()[:-3] if name.lower().endswith(".md") else name.lower()
    cands = [ROOT / name] + (sorted((ROOT / "docs").rglob("*.md")) if (ROOT / "docs").exists() else [])
    for p in cands:
        if p.exists() and "templates" not in p.parts and stem in p.name.lower():
            return p
    return None


def has_fill_markers(p: "Path | None") -> bool:
    return bool(p and p.exists() and "<!-- pm:fill" in p.read_text())


def lifecycle_steps(phases, items) -> list:
    """Ordered (skill, reason) list: where the project is in the CeraNova PM lifecycle and what to do next."""
    steps = []
    if not CONFIG_FILE.exists() and not phases:
        return [("pm-bootstrap", "CeraNova PM isn't initialised in this repo")]
    found = {n: find_doc(n) for n in CFG.get("foundation_docs", ["GOAL.md", "SPEC.md"])}
    missing = [n for n, p in found.items() if not p]
    unfilled = [rel(p) for p in found.values() if has_fill_markers(p)]
    if missing or unfilled:
        steps.append(("pm-intake", "foundation docs " + ", ".join(
            ([f"missing: {', '.join(missing)}"] if missing else []) + ([f"unfinished: {', '.join(unfilled)}"] if unfilled else []))))
    if not phases:
        steps.append(("pm-roadmap", "no phases yet"))
    else:
        docs = {n: roadmap_doc(n, ph) for n, ph in phases.items()}
        no_doc = [f"P{n}" for n, d in docs.items() if not d]
        unfilled_rm = [f"P{n}" for n, d in docs.items() if has_fill_markers(d)]
        if no_doc or unfilled_rm:
            steps.append(("pm-roadmap", "roadmap " + ", ".join(
                ([f"missing for {', '.join(no_doc)}"] if no_doc else []) + ([f"unfinished for {', '.join(unfilled_rm)}"] if unfilled_rm else []))))
        unplanned = [f"P{n}" for n, ph in phases.items() if not ph.tasks() and ph.meta.get("status") != "done"]
        if unplanned:
            steps.append(("pm-delegate" if len(unplanned) > 1 else "pm-plan", f"phases without tasks: {', '.join(unplanned)}"))
    blocking = sorted(i.id for i in items.values() if i.is_open_bug() and i["severity"] in ("S1", "S2"))
    if blocking:
        steps.append(("pm-reconcile", f"{len(blocking)} open S1/S2 gap(s)/bug(s): {', '.join(blocking[:6])}" + (" …" if len(blocking) > 6 else "")))
    pend = docsync_pending(phases, items)
    if pend:
        steps.append(("pm-doc-sync", f"{len(pend)} doc sync item(s) pending"))
    to_review = sorted(i.id for i in items.values() if i["status"] == "review" and i["review_result"] != "pass")
    if to_review:
        steps.append(("pm-review", f"{len(to_review)} item(s) waiting for an independent review: {', '.join(to_review[:6])}"))
    inprog = sorted(i.id for i in items.values() if i["status"] in ("in_progress", "review") and i.id not in to_review)
    if inprog:
        steps.append(("pm-execute", f"resume in-flight: {', '.join(inprog[:6])}"))
    stale = sorted(i.id for i in items.values() if i.stale())
    if stale:
        steps.append(("pm-triage", f"{len(stale)} in-progress item(s) untouched for over {STALE_DAYS} days: {', '.join(stale[:6])}"))
    ready = next_items(phases, items)
    ready_agent = [i for i in ready if i["owner"] != "user"]
    ready_user = [i for i in ready if i["owner"] == "user"]
    lacking = [(i, preflight_missing(i)) for i in ready_agent[:12]]
    lacking = [(i, m) for i, m in lacking if m]
    runnable = [i for i in ready_agent if i not in {x for x, _ in lacking}]
    if runnable:
        steps.append(("pm-execute", f"{len(ready_agent)} task(s) ready, next: {runnable[0].id} {runnable[0]['title']}"))
    if lacking:
        steps.append(("ask the human", f"{len(lacking)} ready task(s) need tools/keys missing here: " +
                      "; ".join(f"{i.id} ({', '.join(m)})" for i, m in lacking[:4])))
    if ready_user:
        steps.append(("ask the human", f"{len(ready_user)} USER item(s) waiting on them, next: {ready_user[0].id} {ready_user[0]['title']}"))
    if not steps:
        steps.append(("pm-status", "nothing pending: report status"))
    return steps


def merge_block(name: str) -> bool:
    src = BLOCKS_DIR / name
    if not src.exists():
        return False
    block = src.read_text()
    dst = ROOT / name
    cur = dst.read_text() if dst.exists() else ""
    new = BLOCK_RE.sub(lambda _: block, cur, count=1) if BLOCK_RE.search(cur) else (cur.rstrip("\n") + "\n\n" + block if cur else block)
    if new != cur:
        dst.write_text(new)
        return True
    return False


def agent_hooks_installed(agent: str) -> bool:
    spec = AGENT_HOOKS[agent]
    f = ROOT / spec["file"]
    if not f.exists():
        return False
    if spec["style"] == "plugin":
        return "kanban.py" in f.read_text()
    try:
        hooks = json.loads(f.read_text()).get("hooks", {})
    except json.JSONDecodeError:
        return False
    for event in spec["events"]:
        entries = hooks.get(event, [])
        cmds = [h.get("command", "") for e in entries for h in (e.get("hooks", []) if spec["style"] == "groups" else [e])]
        if not any("tools/kanban/kanban.py" in c for c in cmds):
            return False
    return True


def merge_agent_hooks(agent: str) -> bool:
    """Add the kanban hooks to an agent's config next to whatever is already there. True if the file changed."""
    spec = AGENT_HOOKS[agent]
    f = ROOT / spec["file"]
    f.parent.mkdir(parents=True, exist_ok=True)
    if spec["style"] == "plugin":
        body = (Path(__file__).resolve().parent / "adapters" / Path(spec["source"]).name).read_text()
        if f.exists() and f.read_text() == body:
            return False
        f.write_text(body)
        return True
    cur = json.loads(f.read_text()) if f.exists() and f.read_text().strip() else {}
    if spec["style"] == "flat":
        cur.setdefault("version", 1)
    hooks = cur.setdefault("hooks", {})
    changed = False
    for event, entries in spec["events"].items():
        existing = hooks.setdefault(event, [])
        cmds = [h.get("command", "") for e in existing for h in (e.get("hooks", []) if spec["style"] == "groups" else [e])]
        if not any("tools/kanban/kanban.py" in c for c in cmds):
            existing.extend(json.loads(json.dumps(entries)))
            changed = True
    if changed:
        f.write_text(json.dumps(cur, indent=2) + "\n")
    return changed


def merge_claude_hooks() -> bool:
    return merge_agent_hooks("claude")


def agents_present() -> list:
    """Agents this repo is set up for: Claude Code always, others when their config folder exists."""
    return ["claude"] + [a for a in AGENT_NAMES[1:] if (ROOT / AGENT_HOOKS[a]["dir"]).exists()]


def cmd_agents(a):
    want = AGENT_NAMES if a.add == "all" else [x.strip() for x in (a.add or "").split(",") if x.strip()]
    bad = [x for x in want if x not in AGENT_HOOKS]
    if bad:
        sys.exit(f"unknown agent(s): {', '.join(bad)} (choose from {', '.join(AGENT_NAMES)} or all)")
    for ag in want:
        print(f"{ag}: {'hooks added to' if merge_agent_hooks(ag) else 'already set up in'} {AGENT_HOOKS[ag]['file']}")
    present = agents_present()
    print("Session hooks by agent (git hooks and AGENTS.md cover every agent regardless):")
    for ag in AGENT_NAMES:
        state = "installed" if agent_hooks_installed(ag) else ("MISSING (folder exists)" if ag in present else "not set up")
        print(f"  {ag:9} {state:24} {AGENT_HOOKS[ag]['file']}")
    if any(ag in present and not agent_hooks_installed(ag) for ag in AGENT_NAMES):
        print("Run `./kanban agents --add <name>` or `./kanban doctor --fix` to add the missing ones.")


def _fix_gitignore():
    gi = ROOT / ".gitignore"
    cur = gi.read_text() if gi.exists() else ""
    gi.write_text(cur + ("" if not cur or cur.endswith("\n") else "\n") + "tracking/.state/\n")


def _fix_config():
    TRACK.mkdir(exist_ok=True)
    CONFIG_FILE.write_text(json.dumps({"project": PROJECT, "roadmap_dir": CFG["roadmap_dir"],
                                       "roadmap_index": CFG["roadmap_index"]}, indent=2) + "\n")


SKILL_DIRS = (".claude/skills", ".agents/skills")


def _unmirrored_skills() -> list:
    """Skills (any SKILL.md folder, incl. ones agents wrote for this project) present in one agent dir but not the other."""
    dirs = [ROOT / d for d in SKILL_DIRS if (ROOT / d).exists()]
    names = {d: {p.parent.name for p in d.glob("*/SKILL.md")} for d in dirs}
    return sorted({n for d in dirs for n in names[d] if any(n not in names[o] for o in dirs if o != d)})


def _fix_skills():
    """Mirror skills between agent skill dirs (.claude/skills <-> .agents/skills) so every agent sees the same set:
    pm-* from whichever dir has the kit's copy, other skills where missing."""
    dirs = [ROOT / d for d in SKILL_DIRS]
    src = next((d for d in dirs if (d / "pm-lifecycle" / "SKILL.md").exists()), None)
    if not src:
        return False
    for d in dirs:
        if d != src:
            for sk in src.glob("pm-*"):
                shutil.copytree(sk, d / sk.name, dirs_exist_ok=True)
    for d in dirs:
        for sk in (p.parent for p in d.glob("*/SKILL.md")):
            for o in dirs:
                if o != d and not (o / sk.name / "SKILL.md").exists():
                    shutil.copytree(sk, o / sk.name, dirs_exist_ok=True)
    return True


def cmd_doctor(a):
    problems = []

    def check(cond, good, bad, fix=None):
        if cond:
            print("  ok    " + good)
            return True
        if a.fix and fix:
            try:
                if fix() is not False:
                    print("  FIXED " + bad)
                    return True
            except Exception as e:  # report and carry on
                bad += f" (auto-fix failed: {e})"
        problems.append(bad)
        print("  FIX   " + bad)
        return False

    print(f"CeraNova PM doctor: {PROJECT} ({ROOT})" + ("  [--fix]" if a.fix else ""))
    print("Setup:")
    check(sys.version_info >= (3, 9), f"python {sys.version.split()[0]}", "python >= 3.9 required")
    is_git = check((ROOT / ".git").exists(), "git repository", "not a git repository (run `git init`)")
    hp = subprocess.run(["git", "config", "--get", "core.hooksPath"], cwd=ROOT, capture_output=True, text=True).stdout.strip() if is_git else ""
    if hp and hp != "tools/kanban/githooks":
        check(False, "", f"project uses core.hooksPath={hp}: add `python3 tools/kanban/kanban.py git-hook <name> \"$@\"` "
                         "to its pre-commit/pre-push/post-merge/post-checkout (docs/pm/MERGING.md)")
    elif is_git:
        check(hp == "tools/kanban/githooks", "git hooks enabled", "git hooks not enabled", fix=ensure_git_hooks)
    for exe in ["kanban", "tools/kanban/kanban.py", *[f"tools/kanban/githooks/{h}" for h in ("pre-commit", "pre-push", "post-merge", "post-checkout")]]:
        p = ROOT / exe
        if p.exists():
            check(os.access(p, os.X_OK), f"{exe} executable", f"{exe} not executable", fix=lambda p=p: p.chmod(0o755))
    for ag in agents_present():
        check(agent_hooks_installed(ag), f"{ag} session hooks configured ({AGENT_HOOKS[ag]['file']})",
              f"{AGENT_HOOKS[ag]['file']} lacks the kanban hooks", fix=lambda ag=ag: merge_agent_hooks(ag) or True)
    for f in ("CLAUDE.md", "AGENTS.md"):
        p = ROOT / f
        check(p.exists() and "pm-kit:start" in p.read_text(), f"{f} has the CeraNova PM block",
              f"{f} missing the CeraNova PM block", fix=lambda f=f: merge_block(f) or False)
    gi = ROOT / ".gitignore"
    check(gi.exists() and "tracking/.state/" in gi.read_text(), ".gitignore covers tracking/.state/",
          ".gitignore lacks tracking/.state/", fix=_fix_gitignore)
    check(CONFIG_FILE.exists(), f"{rel(CONFIG_FILE)} present", "no tracking/kanban.config.json", fix=_fix_config)
    for t in ("task.md", "bug.md", "phase.md"):
        check((TRACK / "templates" / t).exists(), f"template {t}", f"tracking/templates/{t} missing (re-run install.sh --update)")
    phases, items, errs = load()
    errors, warns = validate(phases, items, errs)
    check(not errors, f"{len(items)} item(s) in {len(phases)} phase(s) validate",
          f"{len(errors)} validation error(s): " + "; ".join(errors[:5]))
    if (STATE / "paused").exists():
        print("  note  hooks are paused (bulk edit in progress?). If nothing is mid-edit: `./kanban pause --off && ./kanban build`")
    if a.fix and not errors:
        build(force=True)
        phases, items, errs = load()
    t, _sig = detect_project_type()
    print(f"Project type: {CFG.get('project_type') or t}" + ("" if CFG.get("project_type") else " (detected; set `project_type` in the config to pin it)"))
    skill_dirs = [d for d in SKILL_DIRS if (ROOT / d / "pm-lifecycle" / "SKILL.md").exists()]
    check(bool(skill_dirs), "skills installed in " + ", ".join(skill_dirs), "pm-* skills not found in .claude/skills or .agents/skills",
          fix=_fix_skills)
    for d in SKILL_DIRS:
        if skill_dirs and d not in skill_dirs and (ROOT / d.split("/")[0]).exists():
            if a.fix and _fix_skills():
                print(f"  FIXED pm-* skills mirrored into {d}/")
            else:
                print(f"  note  {d}/ exists but has no pm-* skills; `./kanban doctor --fix` copies them there")
    if skill_dirs and len([d for d in SKILL_DIRS if (ROOT / d).exists()]) > 1:
        loose = _unmirrored_skills()
        if loose and a.fix and _fix_skills():
            print(f"  FIXED skills mirrored between {' and '.join(SKILL_DIRS)}: {', '.join(loose)}")
        elif loose:
            print(f"  note  skills only in one agent dir: {', '.join(loose)}; `./kanban doctor --fix` mirrors them")
    print("Lifecycle (next steps, in order):")
    for i, (skill, why) in enumerate(lifecycle_steps(phases, items), 1):
        print(f"  {i}. {skill}: {why}")
    if problems:
        print(f"{len(problems)} setup problem(s) left." +
              ("" if a.fix else " Run `./kanban doctor --fix` for the safe ones; the pm-doctor skill covers the rest."))
    sys.exit(1 if problems else 0)


# ---------------------------------------------------------------- git hooks (any tool, any model)

def generated_paths() -> list[str]:
    return ["KANBAN.md", "kanban.html", "tracking", CFG["roadmap_index"]]


def cmd_git_hook(a):
    """Called by the shims in tools/kanban/githooks/. Chains the project's own .git/hooks/<name> first."""
    legacy = ROOT / ".git" / "hooks" / a.name
    if legacy.exists() and os.access(legacy, os.X_OK):
        r = subprocess.run([str(legacy), *a.args], cwd=ROOT)
        if r.returncode:
            sys.exit(r.returncode)
    if (STATE / "paused").exists():
        return
    git = lambda *x: subprocess.run(["git", *x], cwd=ROOT, capture_output=True, text=True).stdout
    if a.name == "pre-commit":
        staged = git("diff", "--cached", "--name-only").split()
        watch = ("tracking/", "tools/kanban/", CFG["roadmap_dir"].rstrip("/") + "/")
        if not any(p.startswith(watch) for p in staged):
            return
        phases, items, errs = load()
        errors, _ = validate(phases, items, errs)
        if errors:
            print("kanban: validation failed, commit blocked:\n  " + "\n  ".join(errors[:20]))
            sys.exit(1)
        build(force=True)
        subprocess.run(["git", "add", "--", *[p for p in generated_paths() if (ROOT / p).exists()]], cwd=ROOT)
    elif a.name == "pre-push":
        phases, items, errs = load()
        errors, _ = validate(phases, items, errs)
        if errors:
            print("kanban: validation failed, push blocked. Run ./kanban validate")
            sys.exit(1)
        build(force=True)
        dirty = [l for l in git("status", "--porcelain", "--", *generated_paths()).splitlines() if "SESSIONS.md" not in l]
        if dirty:
            print("kanban: boards were out of date and have been rebuilt. Commit them, then push again:\n"
                  "  git add -A " + " ".join(generated_paths()) + " && git commit -m 'kanban: rebuild boards'")
            sys.exit(1)
        pend = docsync_pending(*load()[:2])
        if pend:
            print(f"kanban: note: {len(pend)} item(s) still need doc sync (tracking/DOC_SYNC.md).")
    elif a.name in ("post-merge", "post-checkout"):
        if a.name == "post-checkout" and (len(a.args) < 3 or a.args[2] != "1"):
            return
        phases, items, _ = build(force=True)
        print(brief(phases, items))


# ---------------------------------------------------------------- hooks

def read_hook_input() -> dict:
    """The agent's JSON event on stdin. Never blocks: some callers leave stdin open without writing to it."""
    try:
        if sys.stdin is None or sys.stdin.isatty():
            return {}
        if os.name != "nt":
            import select
            if not select.select([sys.stdin], [], [], 2)[0]:
                return {}
        raw = sys.stdin.read()
        return json.loads(raw) if raw.strip() else {}
    except (json.JSONDecodeError, OSError):
        return {}


def hook_output(agent: str, event: str, context: str, followup: str) -> str:
    """Format a hook result for the calling agent. `context` is text for the model at session start; `followup`
    asks the agent to keep going at end of turn (doc sync)."""
    context, followup = context.strip(), followup.strip()
    if agent in ("", "claude", "codex"):  # plain stdout = context; {"decision":"block"} continues the turn
        return followup and json.dumps({"decision": "block", "reason": followup}) or context
    if agent == "gemini":  # stdout must be JSON only
        if followup:
            return json.dumps({"decision": "block", "reason": followup})
        if context:
            return json.dumps({"hookSpecificOutput": {"hookEventName": "SessionStart", "additionalContext": context}})
        return "{}"
    if agent == "cursor":
        if followup:
            return json.dumps({"followup_message": followup})
        return json.dumps({"additional_context": context} if context else {})
    return json.dumps({"context": context, "followup": followup})  # opencode plugin / anything else


def _hook_run(event: str, data: dict) -> tuple:
    """The hook behaviour shared by every agent: returns (context, followup)."""
    if event == "session-start" and (ROOT / ".pm-kit-source").exists():
        return "", ""  # the kit's own source repo: nothing to resume
    if event == "session-start" and not CONFIG_FILE.exists() and not phase_numbers():
        return ("CeraNova PM is installed but not initialised in this repo (no tracking/kanban.config.json). "
                "Run the pm-bootstrap skill (or `./kanban init --project \"<name>\"`) before other project work."), ""
    if event == "session-start":
        ensure_git_hooks()
        log_session("session-start", data.get("source", "") or data.get("agent", ""))
        phases, items, _ = build()
        return brief(phases, items), ""
    if event == "post-tool":
        if changed_since_build():
            build()
        return "", ""
    phases, items, _ = build() if changed_since_build() else load()
    pending = [i.id for i in items.values() if i["doc_sync_status"] == "pending"] + \
              [f"P{n}" for n, p in phases.items() if p.meta.get("doc_sync_status") == "pending"]
    STATE.mkdir(parents=True, exist_ok=True)
    nf = STATE / "docsync-notified.json"
    notified = set(json.loads(nf.read_text())) if nf.exists() else set()
    new = [p for p in pending if p not in notified]
    if not new or data.get("stop_hook_active") or int(data.get("loop_count") or 0) > 0:
        return "", ""
    nf.write_text(json.dumps(sorted(notified | set(new))))
    return "", ("Kanban doc-sync: these completed items changed behaviour that the docs describe: "
                + ", ".join(new) + ". Update the docs listed in each item's `doc_sync` field (spec, roadmap, "
                "architecture, UI docs as relevant), then run `./kanban docsync <ID> --done` for each, "
                "rebuild with `./kanban build`, and commit + push the tracking files. See tracking/DOC_SYNC.md.")


def cmd_hook(a):
    """Entry point for every agent's session hooks (Claude Code, Codex, Gemini CLI, Cursor, OpenCode)."""
    import contextlib
    import io
    data = read_hook_input()
    if (STATE / "paused").exists():  # e.g. while planners write items in bulk; `./kanban pause --off` re-enables
        if a.agent in ("gemini", "cursor", "opencode"):
            print("{}")
        sys.exit(0)
    context = followup = ""
    noise = io.StringIO()
    try:
        with contextlib.redirect_stdout(noise):  # agents that parse stdout as JSON must see nothing else
            context, followup = _hook_run(a.event, data)
    except Exception as e:  # hooks must never break the session
        print(f"kanban hook ({a.event}) error: {e}", file=sys.stderr)
    stray = noise.getvalue().strip()
    if stray:
        print(stray, file=sys.stderr)
    out = hook_output(a.agent, a.event, context, followup)
    if out:
        print(out)
    sys.exit(0)


# ---------------------------------------------------------------- main

def main():
    p = argparse.ArgumentParser(prog="kanban", description=f"{PROJECT} kanban CLI (CeraNova PM; see tracking/README.md)")
    sp = p.add_subparsers(dest="cmd", required=True)

    s = sp.add_parser("validate", help="check every item against tracking/SCHEMA.md")
    s.add_argument("--phase", type=int)
    s.add_argument("--quiet", action="store_true", help="errors only")
    s.set_defaults(f=cmd_validate)
    s = sp.add_parser("build", help="triage + regenerate boards, KANBAN.md, kanban.html, DOC_SYNC.md, roadmap blocks")
    s.add_argument("--check", action="store_true", help="fail if generated files differ from git (CI)")
    s.set_defaults(f=cmd_build)
    s = sp.add_parser("triage", help="alias of build")
    s.add_argument("--check", action="store_true")
    s.set_defaults(f=cmd_build)
    s = sp.add_parser("list")
    s.add_argument("--phase", type=int)
    s.add_argument("--status")
    s.add_argument("--type")
    s.add_argument("--kind", choices=KINDS)
    s.add_argument("--include-bugs", action="store_true", help="with --kind gap: also list bugs")
    s.add_argument("--severity", choices=SEVERITIES[1:])
    s.add_argument("--grep", help="words that must all appear in the title or body (find duplicates)")
    s.set_defaults(f=cmd_list)
    s = sp.add_parser("show")
    s.add_argument("id")
    s.set_defaults(f=cmd_show)
    s = sp.add_parser("next", help="ready items, most important first")
    s.add_argument("--phase", type=int)
    s.add_argument("--owner", choices=OWNERS)
    s.add_argument("-n", type=int, default=10)
    s.set_defaults(f=cmd_next)
    s = sp.add_parser("start", help="claim an item (→ in_progress)")
    s.add_argument("id")
    s.add_argument("--note")
    s.add_argument("--git", action="store_true", help="switch to (or create) the item's branch")
    s.add_argument("--force", action="store_true")
    s.set_defaults(f=cmd_start)
    s = sp.add_parser("preflight", help="check the tools, MCP servers, env vars and services items need on this machine")
    s.add_argument("id", nargs="*")
    s.add_argument("--phase", type=int)
    s.add_argument("--ready", action="store_true", help="only ready agent items")
    s.set_defaults(f=cmd_preflight)
    s = sp.add_parser("checkpoint", help="save a resume note")
    s.add_argument("id")
    s.add_argument("note")
    s.set_defaults(f=cmd_checkpoint)
    s = sp.add_parser("tick", help="tick a checklist box by number (1-based) or text")
    s.add_argument("id")
    s.add_argument("which")
    s.set_defaults(f=cmd_tick)
    s = sp.add_parser("review")
    s.add_argument("id")
    s.add_argument("--pr")
    s.set_defaults(f=cmd_review)
    s = sp.add_parser("reviewed", help="record an independent review verdict (pm-review)")
    s.add_argument("id")
    g = s.add_mutually_exclusive_group(required=True)
    g.add_argument("--pass", dest="result", action="store_const", const="pass")
    g.add_argument("--fail", dest="result", action="store_const", const="fail")
    s.add_argument("--note", required=True, help="what was checked and found")
    s.set_defaults(f=cmd_reviewed)
    s = sp.add_parser("done", help="complete an item (checklists + evidence required)")
    s.add_argument("id")
    s.add_argument("--evidence")
    s.add_argument("--force", action="store_true")
    s.set_defaults(f=cmd_done)
    s = sp.add_parser("block")
    s.add_argument("id")
    s.add_argument("--reason", required=True)
    s.set_defaults(f=cmd_block)
    s = sp.add_parser("unblock")
    s.add_argument("id")
    s.add_argument("--ready", action="store_true")
    s.set_defaults(f=cmd_unblock)
    s = sp.add_parser("cancel")
    s.add_argument("id")
    s.add_argument("--reason", required=True)
    s.set_defaults(f=cmd_cancel)
    s = sp.add_parser("reopen")
    s.add_argument("id")
    s.add_argument("--reason", required=True)
    s.set_defaults(f=cmd_reopen)
    s = sp.add_parser("new", help="create a task/bug/gap/chore from the template")
    s.add_argument("--phase", type=int, required=True)
    s.add_argument("--title", required=True)
    s.add_argument("--kind", choices=KINDS, default="task")
    s.add_argument("--type", choices=TYPES, default="BUILD")
    s.add_argument("--priority", choices=PRIORITIES, default="medium")
    s.add_argument("--severity", choices=SEVERITIES[1:], default="S3")
    s.add_argument("--found-in")
    s.add_argument("--depends", help="comma-separated item IDs")
    s.set_defaults(f=cmd_new)
    s = sp.add_parser("docsync", help="mark an item's (or phase P<N>'s) doc sync done/pending")
    s.add_argument("id")
    s.add_argument("--done", action="store_true")
    s.add_argument("--note")
    s.set_defaults(f=cmd_docsync)
    s = sp.add_parser("resume", help="print the resume brief (what's in flight, checkpoints, next)")
    s.set_defaults(f=cmd_resume)
    s = sp.add_parser("session", help="append to tracking/SESSIONS.md")
    s.add_argument("event", choices=["session-start", "handoff", "session-end"])
    s.add_argument("--note")
    s.set_defaults(f=cmd_session)
    s = sp.add_parser("hook", help="entry point for agent session hooks (Claude Code, Codex, Gemini CLI, Cursor, OpenCode)")
    s.add_argument("event", choices=["session-start", "post-tool", "stop"])
    s.add_argument("--agent", default="", choices=["", *AGENT_NAMES], help="output format for this agent (default: Claude Code)")
    s.set_defaults(f=cmd_hook)
    s = sp.add_parser("agents", help="show or add session hooks for coding agents")
    s.add_argument("--add", help=f"comma-separated: {', '.join(AGENT_NAMES)}, or all")
    s.set_defaults(f=cmd_agents)
    s = sp.add_parser("pause", help="pause/resume the Claude Code hooks (bulk edits)")
    s.add_argument("--off", action="store_true")
    s.set_defaults(f=cmd_pause)
    s = sp.add_parser("init", help="set up tracking/ for this project (config + phases)")
    s.add_argument("--project", help="display name (default: repo folder name)")
    s.add_argument("--phases", help='comma-separated phase titles, e.g. "Foundations,Core features,Launch"')
    s.add_argument("--roadmap", action="store_true", help="also create roadmap phase docs from docs/pm/templates")
    s.add_argument("--force", action="store_true", help="rewrite tracking/kanban.config.json")
    s.add_argument("--type", help="project type (default: detected; see `./kanban detect`)")
    s.set_defaults(f=cmd_init)
    s = sp.add_parser("detect", help="detect the project type (drives research agendas)")
    s.set_defaults(f=cmd_detect)
    s = sp.add_parser("phase-add", help="add a phase")
    s.add_argument("--title", required=True)
    s.add_argument("--number", type=int)
    s.add_argument("--opens-after", help="comma-separated phase numbers (default: the previous phase)")
    s.add_argument("--roadmap", action="store_true", help="also create its roadmap doc from the template")
    s.set_defaults(f=cmd_phase_add)
    s = sp.add_parser("doctor", help="check the CeraNova PM setup and say which lifecycle skill comes next")
    s.add_argument("--fix", action="store_true", help="repair what is safe to repair (hooks, blocks, settings, config, permissions, boards)")
    s.set_defaults(f=cmd_doctor)
    s = sp.add_parser("git-hook", help="entry point for the git hook shims")
    s.add_argument("name", choices=["pre-commit", "pre-push", "post-merge", "post-checkout"])
    s.add_argument("args", nargs="*")
    s.set_defaults(f=cmd_git_hook)
    s = sp.add_parser("install-hooks", help="use tools/kanban/githooks for git")
    s.set_defaults(f=cmd_install_hooks)
    s = sp.add_parser("open", help="build and open kanban.html")
    s.set_defaults(f=cmd_open)
    s = sp.add_parser("serve", help="build and serve kanban.html on localhost")
    s.add_argument("--port", type=int, default=8765)
    s.set_defaults(f=cmd_serve)
    a = p.parse_args()
    a.f(a)


if __name__ == "__main__":
    main()
