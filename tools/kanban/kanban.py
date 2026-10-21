#!/usr/bin/env python3
"""MasterTrader kanban: per-phase boards + unified root board, generated from tracking/ item files.

Source of truth: tracking/phase-N/{PHASE.md,tasks/*.md,bugs/*.md}. See tracking/SCHEMA.md.
Stdlib only, so it runs the same in cloud sessions, local shells, git hooks and CI.
"""
from __future__ import annotations

import argparse
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
ROADMAP = ROOT / "docs" / "roadmap"
PHASES = range(9)

STATUSES = ["backlog", "ready", "in_progress", "review", "blocked", "done", "cancelled"]
OPEN_STATUSES = {"backlog", "ready", "in_progress", "review", "blocked"}
CLOSED = {"done", "cancelled"}
KINDS = ["task", "bug", "gap", "chore"]
TYPES = ["USER", "BUILD", "OPS", "VERIFY", "RUN", "DOC"]
PRIORITIES = ["critical", "high", "medium", "low"]
SIZES = {"XS": 1, "S": 2, "M": 3, "L": 5, "XL": 8}
SEVERITIES = ["", "S1", "S2", "S3", "S4"]
OWNERS = ["user", "agent", "unassigned"]
DOC_SYNC = ["n/a", "pending", "done"]
HEADINGS = [
    "## Goal / expected outcome", "## Context & references", "## Requirements", "## ToDo",
    "## Verification", "## Acceptance criteria", "## Exceptions & edge cases",
    "## Cardinal rules (do NOT)", "## Doc sync on completion", "## Branch & PR", "## Progress log",
]
ID_RE = re.compile(r"^P([0-8])-([TB])(\d{3})$")
STALE_DAYS = 7
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


def load():
    phases = {n: Phase(n) for n in PHASES}
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
    return all(phases[int(a)].meta.get("status") == "done" for a in after if str(a).isdigit())


# ---------------------------------------------------------------- roadmap ids

def roadmap_ids(n: int):
    files = list(ROADMAP.glob(f"phase-{n}-*.md"))
    if not files:
        return set(), set()
    s = files[0].read_text()
    reqs = set(re.findall(r"^\| (R\d\.N?\d+) \|", s, re.M))
    todos = set(re.findall(r"\*\*(T\d\.\d+)\*\*", s))
    return reqs, todos


# ---------------------------------------------------------------- validate

def validate(phases, items, load_errors):
    errors, warns = list(load_errors), []
    ids = set(items)
    for n, ph in phases.items():
        if not ph.file.exists():
            warns.append(f"tracking/phase-{n}/PHASE.md missing")
        reqs, todos = roadmap_ids(n)
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
    road = next(iter(ROADMAP.glob(f"phase-{ph.n}-*.md")), None)
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
    out = ["# MasterTrader · Project Kanban", "",
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
        road = next(iter(ROADMAP.glob(f"phase-{n}-*.md")), None)
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
                      "body": i.body, "last": (i.last_log() or [""])[0]})
    sessions = []
    sf = TRACK / "SESSIONS.md"
    if sf.exists():
        sessions = [l for l in sf.read_text().splitlines() if l.startswith("- ")][-15:]
    return {"generated": stamp() + " UTC", "overall": overall(phases), "phases": ph_rows, "items": its,
            "docsync": docsync_pending(phases, items), "sessions": sessions}


def render_html(phases, items) -> str:
    tpl = (Path(__file__).parent / "board_template.html").read_text()
    data = json.dumps(html_data(phases, items), ensure_ascii=False).replace("</", "<\\/")
    return tpl.replace("/*__DATA__*/null", data)


# ---------------------------------------------------------------- roadmap blocks

def replace_block(text: str, name: str, content: str) -> str:
    start, end = f"<!-- kanban:{name}:start -->", f"<!-- kanban:{name}:end -->"
    if start not in text:
        return text
    a = text.index(start) + len(start)
    b = text.index(end)
    return text[:a] + "\n" + content.strip("\n") + "\n" + text[b:]


def roadmap_blocks(phases):
    readme = ROADMAP / "README.md"
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
    for f in sorted(ROADMAP.glob("phase-*.md")):
        txt = f.read_text()
        n = re.search(r"phase-(\d)", f.name).group(1)
        title = txt.splitlines()[0].split("·", 1)[1].strip()
        c = {t: len(re.findall(rf"\*\*T\d\.\d+\*\* `{t}`", txt)) for t in types}
        nreq = len(set(re.findall(r"^\| (R\d\.N?\d+) ", txt, re.M)))
        for t in types:
            tot[t] += c[t]
        crow.append(f"| [P{n} {title}]({f.name}) | {nreq} | " + " | ".join(str(c[t]) for t in types) + f" | {sum(c.values())} |")
        for m in re.finditer(r"^- \[[ xX]\] \*\*(T\d\.\d+)\*\* `USER` (.*)$", txt, re.M):
            tid, body = m.groups()
            act, _, ref = body.partition(" → ")
            reg.append(f"| {tid} | P{n} | {act.strip()} | {ref.strip() or '—'} |")
    counts = ("| Phase | Requirements | `USER` | `BUILD` | `OPS` | `VERIFY` | `RUN` | ToDos |\n|---|---|---|---|---|---|---|---|\n"
              + "\n".join(crow) + "\n| **Total** | | " + " | ".join(f"**{tot[t]}**" for t in types) + f" | **{sum(tot.values())}** |")
    s = replace_block(s, "roadmap-counts", counts)
    s = replace_block(s, "user-register", "| ID | Phase | Action | Feeds / blocks |\n|---|---|---|---|\n" + "\n".join(reg))
    if s != readme.read_text():
        readme.write_text(s)


# ---------------------------------------------------------------- build

def build(quiet=True):
    phases, items, errs = load()
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
    extra = {"claimed_by": env_label(), "blocked_reason": ""}
    if not it["started"]:
        extra["started"] = today()
    set_status(it, "in_progress", "started" + (f" ({a.note})" if a.note else ""), extra)
    print(f"{a.id} → in_progress. Branch: {it['branch']}")
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
    ph = phases[a.phase]
    nums = [int(ID_RE.match(i.id).group(3)) for i in ph.items if ID_RE.match(i.id) and ID_RE.match(i.id).group(2) == letter]
    iid = f"P{a.phase}-{letter}{(max(nums) + 1 if nums else 1):03d}"
    tpl = (TRACK / "templates" / ("bug.md" if letter == "B" else "task.md")).read_text()
    tpl = tpl.replace("P0-B000" if letter == "B" else "P0-T000", iid)
    slug = slugify(a.title)
    tpl = re.sub(r"p0/" + iid + r"-short-slug", f"p{a.phase}/{iid}-{slug}", tpl)
    tpl = tpl.replace("Short imperative title", a.title).replace("Short description of the defect or gap", a.title)
    tpl = tpl.replace("2026-10-21 00:00 · planner · created", f"{stamp()} · {env_label()} · created")
    tpl = tpl.replace("2026-10-21 00:00 · reporter · opened", f"{stamp()} · {env_label()} · opened")
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
    _, _, errs = build(quiet=False)
    for e in errs:
        print("ERROR: " + e)
    if a.check:
        r = subprocess.run(["git", "status", "--porcelain", "--", "KANBAN.md", "kanban.html", "tracking", "docs/roadmap/README.md"],
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
    out = [f"## MasterTrader kanban: resume brief ({env_label()})", ""]
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
        out.append("**Open S1/S2 bugs:** " + "; ".join(f"{i.id} {i['title']}" for i in bugs))
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


# ---------------------------------------------------------------- hooks

def read_hook_input() -> dict:
    try:
        raw = sys.stdin.read() if not sys.stdin.isatty() else ""
        return json.loads(raw) if raw.strip() else {}
    except (json.JSONDecodeError, OSError):
        return {}


def cmd_hook(a):
    data = read_hook_input()
    if (STATE / "paused").exists():  # e.g. while planners write items in bulk; `./kanban unpause` re-enables
        sys.exit(0)
    try:
        if a.event == "session-start":
            log_session("session-start", data.get("source", ""))
            phases, items, _ = build()
            print(brief(phases, items))
        elif a.event == "post-tool":
            if changed_since_build():
                build()
        elif a.event == "stop":
            phases, items, _ = build() if changed_since_build() else load()
            pending = [i.id for i in items.values() if i["doc_sync_status"] == "pending"] + \
                      [f"P{n}" for n, p in phases.items() if p.meta.get("doc_sync_status") == "pending"]
            STATE.mkdir(parents=True, exist_ok=True)
            nf = STATE / "docsync-notified.json"
            notified = set(json.loads(nf.read_text())) if nf.exists() else set()
            new = [p for p in pending if p not in notified]
            if new and not data.get("stop_hook_active"):
                nf.write_text(json.dumps(sorted(notified | set(new))))
                reason = ("Kanban doc-sync: these completed items changed behaviour that the docs describe: "
                          + ", ".join(new) + ". Update the docs listed in each item's `doc_sync` field (spec, roadmap, "
                          "architecture, UI docs as relevant), then run `./kanban docsync <ID> --done` for each, "
                          "rebuild with `./kanban build`, and commit + push the tracking files. See tracking/DOC_SYNC.md.")
                print(json.dumps({"decision": "block", "reason": reason}))
    except Exception as e:  # hooks must never break the session
        print(f"kanban hook ({a.event}) error: {e}", file=sys.stderr)
    sys.exit(0)


# ---------------------------------------------------------------- main

def main():
    p = argparse.ArgumentParser(prog="kanban", description="MasterTrader kanban CLI (see tracking/README.md)")
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
    s = sp.add_parser("hook", help="entry point for Claude Code / git hooks")
    s.add_argument("event", choices=["session-start", "post-tool", "stop"])
    s.set_defaults(f=cmd_hook)
    s = sp.add_parser("pause", help="pause/resume the Claude Code hooks (bulk edits)")
    s.add_argument("--off", action="store_true")
    s.set_defaults(f=cmd_pause)
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
