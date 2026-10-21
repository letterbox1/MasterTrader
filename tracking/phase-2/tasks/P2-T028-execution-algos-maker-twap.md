---
id: P2-T028
kind: task
title: Execution methods: maker-first, TWAP slicing and fixed exit plan
phase: 2
type: BUILD
status: backlog
priority: high
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P2-T021]
requirements: [R2.33]
roadmap_todos: [T2.25]
modules: [M12]
dashboards: []
branch: p2/P2-T028-execution-algos-maker-twap
pr: ""
doc_sync: [docs/14-strategy-evidence-and-validation.md, docs/roadmap/phase-2-strategies-risk-lab.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P2-T028 · Execution methods: maker-first, TWAP slicing and fixed exit plan

## Goal / expected outcome

Nautilus exec algorithms provide maker-first (post-only with timeout, then taker) and TWAP/slicing for orders larger than ~1% of 1-minute volume, and every entry carries an exit plan fixed and logged at entry.

## Context & references

- Roadmap: [R2.33](../../../docs/roadmap/phase-2-strategies-risk-lab.md) · ToDo T2.25
- Spec: [14 §4 execution + stops/exits](../../../docs/14-strategy-evidence-and-validation.md#4-trading-methods-enforced-in-code-defaults-user-editable-in-d06)
- Related: P2-T029 TCA consumes slices; P2-T017 gate checks each child order.

## Requirements

- `MakerFirst` ExecAlgorithm: post-only at best bid/ask, reprice up to N times, timeout (default 30 s, policy), then escalate to taker within collar; never beyond the decision deadline.
- `TWAP` ExecAlgorithm: triggers when order qty > 1% of trailing 1-min volume (from `md.*.bar.1m`), slices evenly over horizon H with jitter; each child passes M11.
- Exit plan (`stop`, `target`, `time_stop`, `trail`) required on every entry intent; stored immutable in `audit.order`; changes only via `position.set_brackets` (C2) and logged as new rows.
- Memecoin rule: never average down (adds to a losing position rejected).

## ToDo

- [ ] Exec algorithms in `packages/mt_engine/algos/`
- [ ] Exit plan model + validation in OrderIntent
- [ ] Sim tests on recorded books
- [ ] Update the docs listed under *Doc sync on completion* and tick the roadmap ToDo box(es) once every task mapped to them is done

## Verification

### Tests
- Sim tests: maker-first fills as maker when book trades through; escalates after timeout; respects deadline.
- Sim: TWAP slices count/size for a 5% of 1-min volume order.
- Unit: entry without exit plan rejected.

### Scenarios
- Given a post-only order not filled in 30 s, when timeout hits, then it is cancelled and replaced by a taker order within the collar, both linked in audit.
- Given the decision deadline passes mid-slice, when the next child is due, then remaining slices are dropped.

### Stress / failure injection
- Replay a volatile hour (e.g. a 2024-08 crash window from Parquet): algos never exceed collar, never act after deadline.

## Acceptance criteria

- [ ] Maker-first and TWAP implemented with sim tests
- [ ] Exit plan mandatory and immutable
- [ ] Child orders each go through M11
- [ ] CI green: ruff, mypy, pytest (and the `mt_risk` golden suite, `pit` check, viewport matrix where relevant)

## Exceptions & edge cases

- Venue lacks post-only: maker-first degrades to limit-at-touch with timeout; recorded.
- Thin volume data stale: TWAP threshold uses last good value; DQ stale → hold.

## Cardinal rules (do NOT)

- Do NOT let a child order skip the gate.
- Do NOT widen stops after entry without C2.
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order goes through M11, whatever its source.
- Do NOT commit secrets or paste them into chats/issues/logs; secrets live in the sops/age file (07 §2).
- Do NOT skip, weaken or delete a test to get green; risk-manager golden tests are mandatory for merge.

## Doc sync on completion

- `docs/14-strategy-evidence-and-validation.md` §4: algorithm defaults as built.
- `docs/roadmap/phase-2-strategies-risk-lab.md`: tick T2.25 when all tasks mapped to it are done.

## Branch & PR

- Branch: `p2/P2-T028-execution-algos-maker-twap`
- PR title: `P2-T028: Execution methods: maker-first, TWAP slicing and fixed exit plan`
- PR checklist: tests added and green · docs synced · task file ticked · no secrets (gitleaks) · `./kanban done P2-T028` run

## Progress log

- 2026-10-21 00:00 · planner · created
