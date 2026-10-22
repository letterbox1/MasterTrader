---
id: P2-T166
kind: task
title: E2E scenario: create three ways → backtest → validate → paper
phase: 2
type: VERIFY
status: backlog
priority: critical
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P2-T143, P2-T144, P2-T146, P2-T114, P2-T007, P2-T021, P2-T017, P2-T036]
requirements: [R2.06, R2.40, R2.42, R2.45, R2.50]
roadmap_todos: [T2.32, T2.27]
modules: [M0, M7, M15]
dashboards: [D03, D04, D05]
tools: [pnpm, uv, playwright]
mcp: []
env: []
services: [nats, postgres, mlflow]
branch: p2/P2-T166-e2e-strategy-lifecycle-scenario
pr: ""
doc_sync: [docs/02-v1-architecture.md, docs/roadmap/phase-2-strategies-risk-lab.md]
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

# P2-T166 · E2E scenario: create three ways → backtest → validate → paper

## Goal / expected outcome

A Playwright + API end-to-end scenario of flow F7 through the UI: a strategy created from a template, one from code and one by 'describe it' are each backtested with measured costs, validated with every harness section shown, and the passing one is started on paper behind M11 — covering exit criteria 1 and the lab side of 2.

## Context & references

- Roadmap: [exit criteria 1–2](../../../docs/roadmap/phase-2-strategies-risk-lab.md#6-exit-criteria-demo) · [02 F7](../../../docs/02-v1-architecture.md#8-end-to-end-flows)
- Prerequisites (`depends_on`): lifecycle + gate profile (P2-T007), paper engine (P2-T021), M11 RiskGate (P2-T017), bots (P2-T036)
- Decisions: a strategy is promoted through gates; a bot is switched between `paper`/`hitl`/`autonomous` ([17 §B](../../../docs/17-decisions-register.md#b-cross-doc-conflicts-one-canonical-answer)); `lab.leakage.waive` is C2 (17 §D)

## Requirements

- Three strategies created via the three builder tabs; each reaches `backtested` via a truth run with a measured cost snapshot (snapshot id visible).
- Validation report shows every harness section (list in P2-T114); failing ones show reasons; a passing fixture reaches `validated` (gate-checked and audited in `audit.command`).
- Setting the mode ceiling to `paper` and starting a paper bot succeeds only for the validated one; the others are refused with the failing gate.
- Orders from the paper strategy appear in D05 with M11 decisions; nothing bypasses M11.
- Scenario runs nightly against the compose test profile with recorded LLM responses.

## ToDo

- [ ] Write `apps/web/e2e/lifecycle.spec.ts` + API fixtures
- [ ] Seed data snapshot + cost snapshot for the test profile
- [ ] Run and record evidence

## Verification

### Tests
- The E2E spec (nightly) + manual run with screenshots for the exit demo.

### Scenarios
- Given a generated strategy that fails leakage review, when the user waives one item with a reason (C2), then the waiver appears in Gates and in the audit log.
- Given paper start attempted on a `backtested` (not validated) strategy without the override, then it is refused (D03 rule).

### Stress / failure injection
- Run the scenario while 5 other lab jobs are queued: jobs complete within caps; UI remains responsive.

## Acceptance criteria

- [ ] Exit criterion 1 demonstrated end to end
- [ ] Lab side of exit criterion 2 demonstrated (paper behind M11)
- [ ] Nightly E2E green

## Exceptions & edge cases

- Gateway unavailable during the nightly run: describe-it step uses recorded responses; live variant only in the demo.

## Cardinal rules (do NOT)

- Do NOT stub M11 or the cost snapshot in the E2E; use the real services in the test profile.
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order goes through M11.
- Do NOT skip, weaken or delete a test to get green.

## Doc sync on completion

- `docs/02-v1-architecture.md` F7: confirm flow as implemented.
- `docs/roadmap/phase-2-strategies-risk-lab.md`: tick T2.32, T2.27 once every task mapped to it (part A and part B) is done.

## Branch & PR

- Branch: `p2/P2-T166-e2e-strategy-lifecycle-scenario`
- PR title: `P2-T166: E2E scenario: create three ways → backtest → validate → paper`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P2-T166` run · Playwright viewport matrix + axe green

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (paper start via mode ceiling + paper bot, waiver C2, lifecycle/engine/bot deps)
