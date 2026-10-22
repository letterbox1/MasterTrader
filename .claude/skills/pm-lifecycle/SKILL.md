---
name: pm-lifecycle
description: Overview and router for the CeraNova PM project-management lifecycle (kanban per phase, project board, typed tasks, delegation, gap reconciliation, doc sync). Use when the user asks to "set up project management", "manage this project", "what's next", or anything about the kanban, roadmap, phases, tasks or gaps, and you need to pick the right pm-* skill.
compatibility: Any Agent Skills-compatible agent (Claude Code, Codex, Gemini CLI, Cursor, OpenCode and others) working in a git repository with python3 >= 3.9; uses the ./kanban CLI from CeraNova PM.
metadata:
  author: CeraNova
  product: CeraNova PM
  version: "1.4.2"
---

# CeraNova PM lifecycle (router)

The lifecycle, with the skill for each stage:

| # | Stage | Skill | Output |
|---|---|---|---|
| 0 | Install / initialise the kit in this repo | **pm-bootstrap** | `tracking/`, hooks, config, merged CLAUDE.md/AGENTS.md, first board |
| any | Something isn't working, or "what's next?" | **pm-doctor** (`./kanban doctor [--fix]`) | Setup repaired; ordered list of next lifecycle steps |
| 1 | Understand the project: code, existing docs, the human's brief | **pm-intake** | GOAL, SPEC, ARCHITECTURE docs filled in; first gap list |
| 2 | Vet docs the human hands you (other specs, research) | **pm-doc-ingest** | Review doc; merged specs; decisions needed |
| 2 | Get outside facts: tools, repos, vendors, licences, prices, regulation | **pm-research** | `docs/research/<topic>.md` with dated sources; decisions fed |
| 2–3 | Contract a product area in detail: UI screens/design system, API, data, pipeline | **pm-scope** | `docs/<area>/` unit docs with acceptance criteria and data contracts |
| 3 | Phase the work | **pm-roadmap** | `docs/roadmap/` phase docs with R/T IDs; phases in `tracking/` |
| 4 | Plan each phase into task files | **pm-plan** (+ **pm-delegate** for one agent per phase) | `tracking/phase-N/{PHASE.md,tasks/,bugs/}`; boards built |
| 5 | Reconcile gaps and decisions with the human | **pm-reconcile** | Decisions register + configuration doc; doc alignment; task alignment; gaps closed |
| 6 | Execute tasks | **pm-execute** (+ **pm-delegate** for parallel phases) | Code/content + tests; items done with evidence |
| 6 | Independently verify an item before done | **pm-review** | Pass/fail verdict with findings (`./kanban reviewed`) |
| any | New bugs, requests, CI or review failures; stale or blocked items | **pm-triage** | Deduplicated, classified items; groomed board |
| 7 | Keep docs true as the work changes | **pm-doc-sync** | DOC_SYNC queue cleared; phase completion recorded in docs |
| 8 | Report, resume, hand off | **pm-status** | Progress summary, board link, handoff |

## Always-on rules

- **Item files are the source of truth** (`tracking/phase-N/tasks|bugs/*.md`). Boards (`KANBAN.md`, `kanban.html`, `BOARD.md`) are generated: never edit them.
- **Hooks:**
  - Agent session hooks: resume brief at session start, board rebuild after edits, doc-sync prompt at end of turn. Installed for Claude Code, Codex, Gemini CLI, Cursor and OpenCode (`./kanban agents`). Without them, run `./kanban resume` at the start and `./kanban build` after editing items.
  - git hooks: pre-commit validate + rebuild, pre-push gate, post-merge/checkout resume.
- **`owner: user` items are the human's:** accounts, credentials, money, approvals, decisions. Prepare them; never do them.
- **Bulk edits** to item files (planning or alignment waves): `./kanban pause` first; `./kanban pause --off && ./kanban build` after.
- **Before a session ends:** checkpoint in-progress items, commit, push. Progress must survive crashes and cloud↔local moves.
- If `tracking/kanban.config.json` doesn't exist, start with **pm-bootstrap**.
- **`./kanban doctor` always tells you the next step** (it's also in every session-start brief as "Lifecycle next").
- **Question checkpoints with the human:** after intake (one batch of questions with proposed answers), after the roadmap (confirm phases, `USER` register and fixed dates), whenever S1/S2 gaps exist (**pm-reconcile**), and before anything needing their money, accounts or approval. Ask only about real design choices and facts only they have: configurable values get defaults (they change them in settings later) and unverified facts become research tasks; neither goes to the human for review.

## Where things are

- **Guides:** `docs/pm/LIFECYCLE.md`, `docs/pm/SKILLS.md`, `docs/pm/CUSTOMIZING.md`, `docs/pm/MERGING.md`.
- **Data:** `tracking/README.md`, `tracking/SCHEMA.md`, `tracking/briefs/*.md`.
- **Templates:** `docs/pm/templates/`.
- **CLI:** `./kanban --help`.
