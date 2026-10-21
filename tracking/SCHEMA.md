# Tracking Schema

Every kanban in this repo (the nine phase boards and the root board) is **generated** from the same kind of file: one Markdown file per work item with a small front-matter header. `./kanban validate` enforces this schema. `./kanban build` turns the files into the boards.

**Single source of truth:** the item files under `tracking/phase-N/tasks/` and `tracking/phase-N/bugs/`, plus `tracking/phase-N/PHASE.md`.

**Generated (never edit by hand):**
- `tracking/phase-N/BOARD.md`;
- `KANBAN.md`, `kanban.html`;
- `tracking/DOC_SYNC.md`;
- the marked blocks in `docs/roadmap/README.md`.

## 1. Layout

```
tracking/
├── README.md              how to use it (humans and agents)
├── SCHEMA.md              this file
├── SESSIONS.md            append-only session log (written by the SessionStart hook / `./kanban session`)
├── DOC_SYNC.md            generated: completed items whose docs still need updating
├── templates/             task.md · bug.md · phase.md
└── phase-N/
    ├── PHASE.md           phase metadata + exit-criteria checklist (hand-edited)
    ├── BOARD.md           generated phase kanban with progress bar
    ├── tasks/P<N>-T<nnn>-<slug>.md
    └── bugs/P<N>-B<nnn>-<slug>.md
```

## 2. Item front matter

The front matter is a restricted YAML subset: one `key: value` per line. Values are plain text, `""`, or inline lists `[a, b]`. No nesting, no multi-line values.

```yaml
---
id: P2-T014                     # P<phase>-T<nnn> for tasks, P<phase>-B<nnn> for bugs/gaps
kind: task                      # task | bug | gap | chore
title: Risk policy model and versioned store
phase: 2
type: BUILD                     # USER | BUILD | OPS | VERIFY | RUN | DOC
status: backlog                 # backlog | ready | in_progress | review | blocked | done | cancelled
priority: high                  # critical | high | medium | low
size: M                         # XS=1 S=2 M=3 L=5 XL=8 (weights for progress)
severity: ""                    # bugs only: S1 (critical) | S2 (major) | S3 (minor) | S4 (trivial)
owner: agent                    # user | agent | unassigned
claimed_by: ""                  # set by `./kanban start` (env:host:session)
depends_on: [P2-T010, P0-T022]  # item IDs (any phase)
requirements: [R2.11]           # roadmap requirement IDs
roadmap_todos: [T2.22]          # roadmap ToDo IDs
modules: [M11]
dashboards: [D06]
branch: p2/P2-T014-risk-policy-store
pr: ""
doc_sync: [docs/03-build-spec.md, docs/roadmap/phase-2-strategies-risk-lab.md]
doc_sync_status: n/a            # n/a | pending | done (set automatically on completion)
found_in: ""                    # bugs: item ID or area where it was found
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""              # "auto:deps …" is managed by triage
checkpoint: ""                  # one-line "where I am" for resume
---
```

**Rules:**
- `id` is unique across the repo and matches the filename prefix; `phase` matches the folder.
- Every `depends_on` ID must exist, and dependencies can't form a cycle.
- `requirements` and `roadmap_todos` must exist in the phase's roadmap document (warning if not).
- `owner: user` for `type: USER` items (things only the human can do).
- `branch` follows `p<N>/<ID>-<slug>`; one branch and one PR per task, unless a task says otherwise.

## 3. Item body (required headings, in this order)

| Heading | Content |
|---|---|
| `# <ID> · <title>` | Title line |
| `## Goal / expected outcome` | What exists or is true when this is done |
| `## Context & references` | Links to roadmap requirements, spec sections, dashboards, flows, other tasks |
| `## Requirements` | What it must do (functional + non-functional), each traceable |
| `## ToDo` | `- [ ]` checklist of concrete steps (code, config, tests, docs) |
| `## Verification` | `### Tests`, `### Scenarios`, `### Stress / failure injection` (write "n/a: reason" where one doesn't apply) |
| `## Acceptance criteria` | `- [ ]` checklist; all ticked before `done` |
| `## Exceptions & edge cases` | Known exceptions, degraded behaviour, what must not break |
| `## Cardinal rules (do NOT)` | Hard prohibitions for whoever implements it |
| `## Doc sync on completion` | Which docs change when this lands, and how |
| `## Branch & PR` | Branch name, PR title, PR checklist |
| `## Progress log` | Append-only `- YYYY-MM-DD HH:MM · who · note` lines (resume trail) |

**Bugs and gaps** use the same headings. Their `## Requirements` section holds **steps to reproduce / expected / actual**.

## 4. Status flow and automatic triage

```
backlog ──(deps done & phase open)──▶ ready ──start──▶ in_progress ──review──▶ review ──done──▶ done
   ▲                                    │                   │                     │
   └──(a dependency re-opened)──────────┘                   └──── block ──▶ blocked ◀┘   (cancel ▶ cancelled)
```

**Triage runs on every build, every hook and every CLI command:**
- `backlog` → `ready` when all `depends_on` items are `done`/`cancelled` and the phase is open.
- `ready` → `backlog` if a dependency is re-opened.
- `blocked` with `blocked_reason: auto:deps …` → `ready` once its dependencies are done.
- `done` with a non-empty `doc_sync` and `doc_sync_status: n/a` → `pending` (listed in `tracking/DOC_SYNC.md`).
- **Stale:** `in_progress` items not updated for 7 days are flagged on the boards.
- **Phase status:** `not_started` / `in_progress` / `done`. **Done** = every task `done`/`cancelled`, no open S1/S2 bug, and every exit-criteria box in `PHASE.md` ticked. When a phase completes, `PHASE.md` gets `status: done`, `completed:` and `doc_sync_status: pending`.
- **Phase opening:** a phase is open when every phase in its `opens_after` list is done, or when `PHASE.md` says `force_open: true`.

**Done gate:** `./kanban done` refuses unless every `## ToDo` and `## Acceptance criteria` box is ticked and the progress log has a verification note.

## 5. Progress

Weights by size: XS = 1, S = 2, M = 3, L = 5, XL = 8. Cancelled items are excluded.

| Status | Credit |
|---|---|
| `done` | 100% |
| `review` | 90% |
| `in_progress` | 10% + 70% × the share of ticked ToDo boxes |
| anything else | 0% |

The phase bar shows done / review / in progress as separate segments. Bugs are counted separately, and open S1/S2 bugs block phase completion.
