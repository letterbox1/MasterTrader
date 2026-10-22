---
id: P2-B015
kind: gap
title: "Postgres-down behaviour differs: 02 §9.3 keeps the engine trading, 16 §3.1 fires the dead-man on a missing DB heartbeat"
phase: 2
type: DOC
status: backlog
priority: medium
size: XS
severity: S3
owner: agent
claimed_by: ""
depends_on: []
requirements: [R2.18, R2.56]
roadmap_todos: []
modules: [M11, M12]
dashboards: []
tools: []
mcp: []
env: []
services: []
branch: p2/P2-B015-postgres-down-vs-db-heartbeat
pr: ""
doc_sync: [docs/02-v1-architecture.md, docs/16-configuration-and-safety-model.md]
doc_sync_status: n/a
found_in: docs/02-v1-architecture.md §9.3 vs docs/16-configuration-and-safety-model.md §3.1
created: 2026-10-22
updated: 2026-10-22
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
review_result: ""
---

# P2-B015 · Postgres-down behaviour differs: 02 §9.3 keeps the engine trading, 16 §3.1 fires the dead-man on a missing DB heartbeat

## Goal / expected outcome

One documented behaviour when Postgres is unreachable: either the engine keeps trading on the bounded JetStream buffer (02 §9.3) or the layer-1 watchdog treats the DB heartbeat like any other component (16 §3.1).

## Context & references

- [02 §9.3 Postgres down row](../../../docs/02-v1-architecture.md#93-degraded-modes): "Engine continues in memory with risk limits; WORM writes buffer in NATS JetStream … above 80% of the buffer new entries stop".
- [16 §3.1 layer 1](../../../docs/16-configuration-and-safety-model.md#31-three-layer-dead-mans-switch): watches "Feeds, risk service, DB, NATS heartbeats"; missing 5 s → cancel, 10 s → `on_system_failure`.
- Affects P2-T032, P2-T054, P2-T059.

## Requirements

- **Steps to reproduce:** Read the two rows above for a 30 s Postgres outage.
- **Expected:** one behaviour (e.g. the engine continues on the buffer and the DB is not a layer-1 trigger, or the DB heartbeat triggers the dead-man only once the buffer bound is reached).
- **Actual:** 02 says trading continues; 16 says orders are cancelled at 5 s and `on_system_failure` applies at 10 s.
- **Suggested fix:** Decide and align 16 §3.1 and 02 §9.3. Until then the tasks implement 16 §3.1 (the reference doc, fail-flat) with the watched-component list as a setting, and test both paths in P2-T059.
- **Impact:** S3: drills and degraded-mode tests can't assert one expected outcome.

## ToDo

- [ ] Decide the wording with the user (or apply the suggested fix if it follows 16/17)
- [ ] Update the source doc(s) so they agree
- [ ] Update the affected task file(s) to match

## Verification

### Tests
- The affected tasks' tests encode the agreed behaviour.

### Scenarios
- Given the fixed docs, when a reader follows either section, then both describe the same behaviour.

### Stress / failure injection
- n/a: documentation gap

## Acceptance criteria

- [ ] Docs agree in one place, cross-linked from the others
- [ ] Affected tasks reference the decision

## Exceptions & edge cases

- Until resolved, the affected tasks follow 16/17 (the reference docs) as stated under Suggested fix.

## Cardinal rules (do NOT)

- Do NOT close without the doc fix merged and the dependent task(s) updated to match.
- Do NOT "fix" by silently picking a number in code; the decision is recorded in the docs and in policy.

## Doc sync on completion

- The doc(s) in `doc_sync`: aligned wording.

## Branch & PR

- Branch: `p2/P2-B015-postgres-down-vs-db-heartbeat`
- PR title: `P2-B015: align docs`

## Progress log

- 2026-10-22 00:00 · aligner · opened during task alignment (docs/16–17 wave): doc contradiction found while aligning tasks
