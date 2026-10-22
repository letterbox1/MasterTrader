---
id: P8-T001
kind: task
title: Decide whether to build MCP (decision gate)
phase: 8
type: USER
status: backlog
priority: critical
size: XS
severity: ""
owner: user
claimed_by: ""
depends_on: []
requirements: []
roadmap_todos: [T8.01]
modules: [M20]
dashboards: [D16]
tools: []
mcp: []
env: []
services: []
branch: p8/P8-T001-decision-gate
pr: ""
doc_sync: [docs/roadmap/phase-8-mcp.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-22
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
review_result: ""
---

# P8-T001 · Decide whether to build MCP (decision gate)

## Goal / expected outcome

You make and record a go / no-go decision on Phase 8 after **at least 4 weeks (28 days) of daily use** of the web UI and Telegram. *Go* lets every other P8 item proceed; *no-go* cancels the phase cleanly. Nothing in Phase 8 is built before this decision.

## Context & references

- Roadmap: [§2 Entry criteria](../../../docs/roadmap/phase-8-mcp.md#2-entry-criteria) · ToDo [T8.01](../../../docs/roadmap/phase-8-mcp.md#4-todo-sets)
- Plan: [04 Phase 8](../../../docs/04-plan-of-action.md) ("only if you want it") · [03 §1 Deferred row](../../../docs/03-build-spec.md)
- Evidence source: [D16 System → Audit](../../../docs/ui/dashboards/D16-system.md) (`/audit/log` filtered by source = web / telegram)
- Cross-phase: Phase 8 is **hard-gated** ([17 §E](../../../docs/17-decisions-register.md#e-ratification-2026-10-22)): it opens only after its prerequisite phases exit (`opens_after: [6]`) and this decision; the roadmap flow also expects daily use after P7.
- What you'd get: [16 §2.12](../../../docs/16-configuration-and-safety-model.md#212-mcp-phase-8) (scopes, never-exposed list, limits) and [16 §2.3](../../../docs/16-configuration-and-safety-model.md#23-decisions-approvals-and-hitl) (every MCP order needs your approval card; MCP can never approve).
- Unblocks: P8-T002 and, through it, every other P8 item.

## Requirements

- Evidence: activity (at least one login or command) on each of the last 28 days in D16 Audit, source `web` or `telegram`. A missed day or two is your call; note it.
- Decision outcomes (pick one): `go-full` (all six tool groups), `go-read-only` (read & analyse, agents, curation only; trade/strategies/risk tool tasks P8-T010–T012 are cancelled with reason and the exit demo is amended), or `no-go`.
- The decision, its date and the evidence summary are written in this file's Progress log. Nothing is pasted into chat that contains tokens or account data.

## ToDo

- [ ] Open D16 → Audit, filter source = `web`, date range = last 28 days; count the days with activity. Repeat for `telegram`.
- [ ] Write down 3–5 concrete things you would ask Claude that are slow in the UI/Telegram today (e.g. "compare my sleeves' drawdowns this month").
- [ ] Decide `go-full`, `go-read-only` or `no-go`.
- [ ] Append to the Progress log: `- YYYY-MM-DD HH:MM · user · decision: <outcome>; active days web=<n> telegram=<n>; reasons: …`.
- [ ] If `no-go`: ask the agent to run `./kanban cancel <id> "decision gate: no-go"` for every other P8 item.
- [ ] If `go-read-only`: ask the agent to cancel P8-T010, P8-T011, P8-T012 with reason and to amend the exit demo in PHASE.md to the read-only subset.
- [ ] Run `./kanban done P8-T001`.

## Verification

### Tests
- n/a: human decision; the evidence is the D16 audit filter result recorded in the Progress log.

### Scenarios
- Given 28 active days and a `go-full` decision, when this item is marked done, then P8-T002 moves to `ready` at the next triage.
- Given only 15 active days, when you review, then you wait and re-check later; the item stays open.
- Given `no-go`, when the other items are cancelled, then the phase can close with no open S1/S2 bugs (the gaps are cancelled too).

### Stress / failure injection
- n/a: decision item, no runtime behaviour.

## Acceptance criteria

- [ ] Decision, date and evidence (active-day counts) recorded in the Progress log
- [ ] Downstream item statuses match the decision (cancelled / amended / untouched)

## Exceptions & edge cases

- P6 not done: the phase isn't open anyway; you can still record usage evidence early.
- Holidays or illness: count the 28 days excluding them and say so.
- Live trading not yet started (P7): MCP can still be built and tested against paper/practice accounts only.

## Cardinal rules (do NOT)

- Do NOT let the agent start P8 BUILD work before this item is done.
- Do NOT decide on behalf of the user; only the user records this decision.
- Do NOT commit secrets or paste them into chats/issues (including the Claude conversation); secrets live in the sops/age file (07 §2).
- Do NOT use live money before the P7 gates; keys stay trade-only, IP-locked, withdrawals disabled.

## Doc sync on completion

- `docs/roadmap/phase-8-mcp.md`: tick T8.01 and add `(decision: <outcome>, date)`; if `no-go`, mark the remaining ToDos `(deferred: decision gate no-go)`.

## Branch & PR

- Branch: `p8/P8-T001-decision-gate`
- PR title: `P8-T001: Decide whether to build MCP (decision gate)`
- PR checklist: no PR needed (decision only) · Progress log entry written · `./kanban done P8-T001` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (hard gate per 17 §E and what MCP would allow per 16 §2.3/§2.12; tools/env/services fields)
