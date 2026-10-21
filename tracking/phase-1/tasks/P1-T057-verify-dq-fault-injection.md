---
id: P1-T057
kind: task
title: Verify DQ end to end with fault injection
phase: 1
type: VERIFY
status: backlog
priority: critical
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P1-T031, P1-T032, P1-T033, P1-T034, P1-T035, P1-T036, P1-T045, P1-T048]
requirements: [R1.10, R1.N1]
roadmap_todos: [T1.61]
modules: [M16]
dashboards: [D07]
branch: p1/P1-T057-verify-dq-fault-injection
pr: ""
doc_sync: [docs/roadmap/phase-1-data-and-monitoring.md, docs/03-build-spec.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P1-T057 · Verify DQ end to end with fault injection

## Goal / expected outcome

On the running stack, killing a feed, injecting a bad tick, skewing the clock and dropping sequence IDs each produce the right `dq.status`, incident, D07 display and alert, with the stale path measured under 2 s.

## Context & references

- Roadmap: requirements [R1.10](../../../docs/roadmap/phase-1-data-and-monitoring.md#3-requirements), [R1.N1](../../../docs/roadmap/phase-1-data-and-monitoring.md#3-requirements) · ToDo [T1.61](../../../docs/roadmap/phase-1-data-and-monitoring.md#4-todo-sets)
- Roadmap T1.61 · SLO [02 §9.2](../../../docs/02-v1-architecture.md#92-observability--slos) · exit criterion 3 ([phase 1 §6 exit criteria](../../../docs/roadmap/phase-1-data-and-monitoring.md#6-exit-criteria-demo)) · harness from P1-T030
- Depends on (this phase): P1-T031, P1-T032, P1-T033, P1-T034, P1-T035, P1-T036, P1-T045, P1-T048

## Requirements

- Test plan `tests/e2e/dq_fault_injection.py` runnable against the dev stack (`make e2e-dq`)
- Cases: (1) kill a live crypto WS (container network cut) → `stale` < 2 s; (2) inject a bad tick via the harness proxy → flagged, bar unaffected; (3) skew exchange timestamps +1 s and fake chrony offset → skew incident + critical alert; (4) drop sequence IDs → gap incident and book `bad` until resync; (5) crossed book; (6) divergence offset
- For each: assert NATS status, `audit.dq_event` rows (open + resolve), D07 visible within 2 s of publish, alert on configured channels
- Report: detection times per case (p50/p99 over 20 runs for the kill case)

## ToDo

- [ ] Write the e2e suite and fault proxy (toxiproxy or a custom NATS-side injector)
- [ ] Run 20× for the kill case and record the distribution
- [ ] Store the report under `reports/verify/P1-T057/`
- [ ] Update the docs listed under Doc sync and tick the roadmap ToDo box(es)

## Verification

### Tests

- E2E suite as described; runs nightly in CI against compose

### Scenarios

- Given the feed is killed, when 2 s pass, then `dq.status` is `stale`, D07 shows it with the incident, and Telegram/email/ntfy received the alert
- Given the feed returns, when hysteresis passes, then the incident resolves (new row) and a resolution notice is sent

### Stress / failure injection

- Chaos: run the six cases in random order for 30 min; no missed detection, no stuck status

## Acceptance criteria

- [ ] Kill case p99 < 2 s over 20 runs; all six cases pass; report stored
- [ ] CI green (ruff, mypy, pytest, `pit` bypass check, gitleaks)

## Exceptions & edge cases

- Run during quiet hours too (Sunday crypto) to catch timeout tuning issues

## Cardinal rules (do NOT)

- Do NOT UPDATE or DELETE WORM rows (`audit.*`); resolutions and corrections are new rows with `supersedes_id` ([15 §2](../../../docs/15-bots-hitl-and-worm-audit.md#2-worm-records-write-once-read-many)).
- Do NOT skip, weaken or delete a test (or widen a tolerance) to get CI green.
- Do NOT commit secrets or paste them into chats, issues, logs or test fixtures; credentials come only from the sops/age secrets file mounted on tmpfs ([07 §2](../../../docs/07-security-notes.md#2-secrets)).

## Doc sync on completion

- `docs/roadmap/phase-1-data-and-monitoring.md`: tick T1.61 once every task traced to it in PHASE.md is done; note P1-T057 next to it.
- `docs/03-build-spec.md` §M16: link the fault-injection report

## Branch & PR

- Branch: `p1/P1-T057-verify-dq-fault-injection`
- PR title: `P1-T057: Verify DQ end to end with fault injection`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P1-T057` run

## Progress log

- 2026-10-21 00:00 · planner · created
