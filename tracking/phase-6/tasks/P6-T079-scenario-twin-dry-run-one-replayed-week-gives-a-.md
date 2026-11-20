---
id: P6-T079
kind: task
title: Scenario-twin dry run: one replayed week gives a report per bot within max_shock
phase: 6
type: VERIFY
status: backlog
priority: high
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P6-T075, P6-T076]
requirements: [R6.33]
roadmap_todos: [T6.76]
modules: [M14, mt-engine]
dashboards: [D14]
tools: [git, cargo, docker]
mcp: []
env: []
services: [nats, supabase-postgres, llm-local]
branch: p6/P6-T079-scenario-twin-dry-run-one-replayed-week-gives-a-
pr: ""
doc_sync: [docs/roadmap/phase-6-ai-models-treasury.md]
doc_sync_status: n/a
found_in: ""
created: 2026-11-20
updated: 2026-11-20
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
review_result: ""
---

# P6-T079 · Scenario-twin dry run: one replayed week gives a report per bot within max_shock

## Goal / expected outcome

One full week of recorded data is replayed through the scenario twin with the week's scenarios: every active paper bot gets a report, every injected shock is inside `crowdsim.max_shock`, and the baseline replay tracks the real paper run.

## Context & references

- Roadmap: [R6.33](../../../docs/roadmap/phase-6-ai-models-treasury.md#3-requirements) · ToDo T6.76
- Canonical: [18 §2.4](../../../docs/18-platform-and-deployment.md#24-scenario--crowd-simulator-m14-a-go-live-tool) · [16 §2.14b](../../../docs/16-configuration-and-safety-model.md#214b-scenario--crowd-simulator-m14)
- Depends on (this phase): P6-T075 (twin), P6-T076 (containers and settings)

## Requirements

- Use the latest complete paper week (or a recorded fixture week if no paper bots run yet).
- The week's pick (default 3 scenarios) runs on `local-advisor`; the twin runs baseline + one replay per scenario.
- Checks: one report row per active bot per scenario; every applied shock ≤ `crowdsim.max_shock`; baseline within the P2 backtest↔paper parity tolerance; all rows `synthetic = true`.

## ToDo

- [ ] Run the dry run (`sim.crowdsim.run` for the week, then the twin).
- [ ] Check the four conditions with a committed query script.
- [ ] Record commands, wall time and results in the progress log.

## Verification

### Tests
- The committed query script's own unit test on fixture rows (pass and fail cases).

### Scenarios
- Given the latest paper week with N active bots and 3 scenarios, when the dry run finishes, then 3N report rows exist, each shock within the caps, and the baseline matches the real paper run.

### Stress / failure injection
- n/a: a single dry run; load is covered in P6-T075.

## Acceptance criteria

- [ ] A report for every bot for every scenario of the week.
- [ ] Every injected shock inside `crowdsim.max_shock`.
- [ ] Evidence (commands, timings, row counts) in the progress log.

## Exceptions & edge cases

- No paper bots yet: use the fixture week and two template bots; repeat with real bots in P6-T080's first week.

## Cardinal rules (do NOT)

- Do NOT point the twin at real paper or live accounts.
- Do NOT edit report rows to pass a check; re-run instead (rows are insert-only).
- Do NOT commit secrets or paste them into chats/issues/PRs; secrets live only in the sops/age file (07 §2).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral/broker IDs in vendored code.

## Doc sync on completion

- `docs/roadmap/phase-6-ai-models-treasury.md`: tick T6.76 (and note this task ID) once all items covering it are done.

## Branch & PR

- Branch: `p6/P6-T079-scenario-twin-dry-run-one-replayed-week-gives-a-`
- PR title: `P6-T079: Scenario-twin dry run: one replayed week gives a report per bot within max_shock`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P6-T079` run

## Progress log

- 2026-11-20 01:11 · cloud:vm:be04b6ae61f8 · created
- 2026-11-20 00:00 · aligner · Rust-max per 17 §H (new task for the scenario & crowd simulator workstream, 18 §2.4)
