---
id: P8-T029
kind: task
title: Phase 8 exit demo
phase: 8
type: VERIFY
status: backlog
priority: critical
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P8-T017, P8-T019, P8-T020, P8-T021, P8-T022, P8-T023, P8-T024, P8-T025, P8-T026, P8-T027, P8-T028]
requirements: [R8.01, R8.02, R8.03, R8.04, R8.05, R8.06, R8.07]
roadmap_todos: []
modules: [M20, M11, M17]
dashboards: [D17, D06, D05]
branch: p8/P8-T029-phase-exit-demo
pr: ""
doc_sync: [docs/roadmap/phase-8-mcp.md, docs/roadmap/README.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P8-T029 · Phase 8 exit demo

## Goal / expected outcome

The roadmap §6 demo runs live and every exit criterion in PHASE.md is ticked with evidence. From Claude: "how are my strategies doing, tighten BTC max position to X, and close half my EURUSD" → the tighten applies instantly, the close waits for your Telegram approval, and both appear in D17 and `audit.command`.

## Context & references

- Roadmap: [§6 Exit criteria](../../../docs/roadmap/phase-8-mcp.md#6-exit-criteria-demo) · all of [R8.01–R8.07](../../../docs/roadmap/phase-8-mcp.md#3-requirements)
- PHASE.md exit-criteria checklist (tracking/phase-8/PHASE.md)
- Evidence items: P8-T020 (auth), T021/T022 (bypass, C3), T023 (tool list), T024 (injection), T025 (audit), T026 (scenarios), T027 (stress), T028 (RUN).

## Requirements

- Demo on paper/practice accounts (or micro-live only if P7 already allows it and you choose to).
- Step 1: Claude reads strategy status (C0, read tools).
- Step 2: `risk_policy_update` tightening BTC max position to X → `applied` immediately; D06 Changes shows who = mcp.
- Step 3: `position_reduce(EURUSD, 0.5)` → `pending_approval`; Telegram MCP card; you approve; M11 passes; fill on the practice account.
- Step 4: D17 shows the session with all calls; `audit.command` has both writes with `source = mcp`; `audit.verify` green.
- Step 5: confirm each PHASE.md exit box with a link to its evidence (CI runs, reports, reviews).

## ToDo

- [ ] Prepare paper positions (EURUSD long, BTC policy at a known value).
- [ ] Run the demo with you; screen-record D17 and Telegram (no secrets on screen).
- [ ] Tick PHASE.md exit criteria with evidence links.
- [ ] Doc sync.

## Verification

### Tests
- Re-run the bypass (P8-T021), C3 (P8-T022) and tool-list (P8-T023) suites on the demo build; all green.

### Scenarios
- Given the demo prompt, when Claude acts, then tighten = instant, close = waits for Telegram, both in D17 + `audit.command`.
- Given you reject the close card instead, then nothing trades and the audit shows `rejected` (run once as a negative check).

### Stress / failure injection
- n/a: covered by P8-T027; the demo re-runs the security suites only.

## Acceptance criteria

- [ ] Demo passes end to end with recordings/links
- [ ] All PHASE.md exit criteria ticked with evidence
- [ ] No open S1/S2 P8 bugs
- [ ] CI green (lint, types, tests, `pit` check)

## Exceptions & edge cases

- EURUSD market closed (weekend): use a 24/7 crypto pair on testnet for the close step and re-run EURUSD on the next session.

## Cardinal rules (do NOT)

- Do NOT fake any step with mocks; this is the real stack.
- Do NOT show tokens or keys in the recording.
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order goes through M11, whatever its source.
- Do NOT make loosening risk, autonomous mode, mandates or kill-switch OFF anything less than C3 (Telegram + TOTP + cool-down); protective exits never wait for approval.
- Do NOT use live money before the P7 gates; keys stay trade-only, IP-locked, withdrawals disabled.
- Do NOT update or delete WORM rows; corrections are new rows (15 §2).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code (including the MCP SDK).
- Do NOT commit secrets or paste them into chats/issues (including into the Claude conversation); secrets live in the sops/age file (07 §2).

## Doc sync on completion

- `docs/roadmap/phase-8-mcp.md`: tick the remaining boxes and note the demo date.
- `docs/roadmap/README.md`: phase status text if it carries one (generated blocks are rebuilt by `./kanban build`).

## Branch & PR

- Branch: `p8/P8-T029-phase-exit-demo`
- PR title: `P8-T029: Phase 8 exit demo`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P8-T029` run

## Progress log

- 2026-10-21 00:00 · planner · created
