---
id: P3-T025
kind: task
title: Per-FY per-activity regime setting with dual investor and trader reporting
phase: 3
type: BUILD
status: backlog
priority: critical
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P3-T023, P3-T024, P3-T038]
requirements: [R3.07]
roadmap_todos: [T3.24]
modules: [M18]
dashboards: [D15]
tools: [git, uv]
mcp: []
env: []
services: [postgres, mt-api]
branch: p3/P3-T025-regime-setting-dual-reporting
pr: ""
doc_sync: [docs/roadmap/phase-3-journal-and-tax.md]
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

# P3-T025 · Per-FY per-activity regime setting with dual investor and trader reporting

## Goal / expected outcome

The tax regime is an effective-dated setting per FY and activity (`investment`/`trading` tag, asset class) with values investor / trader-in-business / revenue-instrument / `both`; until the agent decides, every FY computation is produced **both ways** (investor vs trader-in-business) side by side, which is exit criterion 2.

## Context & references

- Roadmap: [R3.07, T3.24](../../../docs/roadmap/phase-3-journal-and-tax.md) · exit criterion 2
- [09 key findings: carrying on a business](../../../docs/09-journal-and-tax.md#️-key-findings-that-shape-the-design) · D15 regime toggle [D15](../../../docs/ui/dashboards/D15-tax.md) · command `tax.regime.set` (C1, after an agent answer) in [02 §7.2](../../../docs/02-v1-architecture.md#72-commands-rest-write)
- Answer comes from P3-T001; P7 entry needs it ([P7 T7.01](../../../docs/roadmap/phase-7-prove-and-go-live.md))

## Requirements

- `journal.regime_setting` (WORM): FY, activity scope (tag, asset class), regime, `decided_by` (agent answer ref | default), effective_from, reason.
- Default for every FY/activity = `both` (dual computation).
- Trader-in-business computation: all trading gains/losses (incl. crypto and shares in `trading`-tagged accounts) are ordinary income/loss; no CGT discount; `investment`-tagged accounts stay capital (argument per 09 goal 7).
- `tax.regime.set` (C1) requires a linked `TAX_QUESTION` answer id recorded with `task.answer` (C1, P3-T038) unless setting back to `both`; audited.
- Summary output: two columns (Investor, Trader) with the delta, each with rule version + FX source; D15 badge shows `both` / chosen regime.

## ToDo

- [ ] Implement `rules/au_2026/regime.py` (dual runner over the same inputs)
- [ ] `tax.regime.set` command handler + validation against TAX_QUESTION answers
- [ ] Report model with paired columns; tests; docs

## Verification

### Tests

- Golden: same FY fixture → investor net capital gain vs trader ordinary income match hand-computed figures.
- Unit: `tax.regime.set` without an answer id → rejected (problem+json).
- Unit: investment-tagged lots remain capital under trader regime.

### Scenarios

- Given no agent answer, when D15 Summary opens, then both columns show with the badge `both`.
- Given the agent answers "trader for trading accounts from FY2026-27", when you set it, then that FY shows Trader as primary and Investor as an informational comparison, and the change is in `audit.command`.

### Stress / failure injection

- n/a: doubles computation time of P3-T023 (budget stays < 2 min per FY)

## Acceptance criteria

- [ ] Dual computation for every FY by default
- [ ] Regime changes audited and linked to an agent answer
- [ ] Exit criterion 2 data available via `/tax/summary?fy=`
- [ ] CI green (lint, types, tests, `pit` check; `tax-golden` once P3-T045 lands)

## Exceptions & edge cases

- Mid-FY regime change → split by effective date with a warning (agent to confirm).
- Locked FY (`tax.fy.lock`, C3) → regime change refused with 423 until a C3 unlock (P3-T055).

## Cardinal rules (do NOT)

- Do NOT pick a regime by default other than `both`.
- Do NOT let the UI alone enforce the answer link; the server validates.
- Do NOT commit secrets or paste them into chats/issues; secrets live only in the sops/age file ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Do NOT UPDATE or DELETE `journal.*` (WORM) rows; corrections are new rows referencing the superseded row ([15 §2](../../../docs/15-bots-hitl-and-worm-audit.md#2-worm-records-write-once-read-many)).
- Do NOT use floats for money, quantities, FX rates or tax; `Decimal` in Python and `numeric` in Postgres only ([02 §5.2](../../../docs/02-v1-architecture.md#52-key-conventions)).
- Do NOT present output as tax advice; every tax surface carries "Not tax advice. Confirm with a registered tax agent."
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order goes through M11.
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.

## Doc sync on completion

- `docs/roadmap/phase-3-journal-and-tax.md`: tick T3.24 once every item mapped to it is done.

## Branch & PR

- Branch: `p3/P3-T025-regime-setting-dual-reporting`
- PR title: `P3-T025: Per-FY per-activity regime setting with dual investor and trader reporting`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P3-T025` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (answer link via `task.answer` C1 (P3-T038 added to depends_on); locked FY via P3-T055; tools/services filled)
