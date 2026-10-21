---
id: P2-T160
kind: task
title: Verify a seeded look-ahead bug is caught by analysers and leakage review
phase: 2
type: VERIFY
status: backlog
priority: critical
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P2-T112, P2-T113, P2-T114]
requirements: [R2.43]
roadmap_todos: [T2.64]
modules: [M7]
dashboards: [D04]
branch: p2/P2-T160-verify-seeded-lookahead-bug
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

# P2-T160 · Verify a seeded look-ahead bug is caught by analysers and leakage review

## Goal / expected outcome

Evidence that a strategy with a deliberately planted look-ahead bug is blocked twice over: the look-ahead analyser fails it and the LLM leakage review marks look-ahead 'present' quoting the exact line, so the strategy cannot reach `validated`.

## Context & references

- Roadmap: [R2.43](../../../docs/roadmap/phase-2-strategies-risk-lab.md#3-requirements) · ToDo T2.64
- [14 §6 gate 1](../../../docs/14-strategy-evidence-and-validation.md#6-validation-harness-extends-03-8) · [03 §8 item 3](../../../docs/03-build-spec.md#8-promotion-gates-per-strategy-configurable)

## Requirements

- Seed three variants into a copy of the EMA template: (a) `close.shift(-1)` in the signal, (b) using the forming (unclosed) higher-timeframe bar, (c) normalising with full-sample mean/std.
- Each variant: look-ahead or repaint analyser fails (a, b) and the leakage review flags the matching checklist item with a verified quote (a, b, c — c is 'full-sample fitting').
- Lifecycle refuses `validated` for all three; the clean template passes both.
- Run against the live gateway once (manually, recorded) and in CI with recorded responses.

## ToDo

- [ ] Add seeded fixtures under `tests/fixtures/strategies/seeded_lookahead_*`
- [ ] Run suite; capture reports
- [ ] Assert lifecycle refusal via part A's promote path
- [ ] Record evidence in the progress log

## Verification

### Tests
- Integration (CI, recorded LLM): three seeded variants fail, clean passes.
- Manual: one live-gateway run with spend logged.

### Scenarios
- Given variant (c), when only analysers run, then they may pass — the leakage review must catch it, proving the two layers are complementary.
- Given the gateway is down, then the leakage section is pending and the strategy stays blocked.

### Stress / failure injection
- n/a: correctness check; failure injection of the gateway covered in P2-T167.

## Acceptance criteria

- [ ] All three seeded bugs blocked
- [ ] Clean template passes
- [ ] Evidence (report links) in the progress log

## Exceptions & edge cases

- Model non-determinism: the live run is evidence only; CI uses recorded responses.

## Cardinal rules (do NOT)

- Do NOT tune the checklist prompt on the seeded fixtures until it passes; fix generally and keep the fixtures as a held-out check.
- Do NOT skip, weaken or delete a test to get green.

## Doc sync on completion

- `docs/14-strategy-evidence-and-validation.md` §6: seeded-bug evidence summary.
- `docs/roadmap/phase-2-strategies-risk-lab.md`: tick T2.64 once every task mapped to it (part A and part B) is done.

## Branch & PR

- Branch: `p2/P2-T160-verify-seeded-lookahead-bug`
- PR title: `P2-T160: Verify a seeded look-ahead bug is caught by analysers and leakage review`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P2-T160` run

## Progress log

- 2026-10-21 00:00 · planner · created
