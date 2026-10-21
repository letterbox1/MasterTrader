---
id: P2-B007
kind: gap
title: "Client order ID derivation is ambiguous: signal-derived vs restart epoch"
phase: 2
type: DOC
status: backlog
priority: medium
size: XS
severity: S3
owner: agent
claimed_by: ""
depends_on: []
requirements: [R2.32]
roadmap_todos: []
modules: [M12]
dashboards: []
branch: p2/P2-B007-client-order-id-derivation
pr: ""
doc_sync: [docs/03-build-spec.md, docs/07-security-notes.md]
doc_sync_status: n/a
found_in: docs/03-build-spec.md M12; docs/07-security-notes.md §6
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P2-B007 · Client order ID derivation is ambiguous: signal-derived vs restart epoch

## Goal / expected outcome

One ID scheme that both prevents duplicates across restarts and keeps the epoch for traceability.

## Context & references

- [03 M12 'IDs include a restart epoch'](../../../docs/03-build-spec.md#m12-execution--mt_engine) · [07 §6 'derived from the signal ID'](../../../docs/07-security-notes.md#6-application-controls)
- Affects P2-T027, P2-T055.

## Requirements

- **Steps to reproduce:** If the epoch is part of the ID, the same signal after a restart produces a new ID, so the venue's duplicate-ID protection no longer stops a resubmit.
- **Expected:** Deterministic intent-derived ID + a persisted intent ledger checked before submit; epoch carried as a prefix/tag for engine-generated orders and traceability.
- **Actual:** Two docs describe different, partly conflicting schemes.
- **Suggested fix:** Document the scheme implemented in P2-T027 (ID = env+epoch prefix + hash(intent_id, leg), resubmit blocked by `ops.intent_ledger` across epochs).
- **Impact:** S3: risk of duplicate orders after restarts if implemented literally from 03 M12.

## ToDo

- [ ] Decide the rule with the user (or record the decision taken in the linked task)
- [ ] Update the source doc(s) so they agree
- [ ] Update the affected task file(s) to match

## Verification

### Tests
- The affected task's tests encode the decided rule (named in that task).

### Scenarios
- Given a crash after submit, when restarted, then no second order is sent for the same intent.

### Stress / failure injection
- n/a: documentation/specification gap

## Acceptance criteria

- [ ] Docs agree in one place, cross-linked from the others
- [ ] Affected tasks reference the decision

## Exceptions & edge cases

- Until resolved, the affected task implements the conservative option stated under Suggested fix.

## Cardinal rules (do NOT)

- Do NOT close without the doc fix merged and the dependent task(s) updated to match.
- Do NOT "fix" by silently picking a number in code; the decision is recorded in the doc and in the risk policy (user input).
- Do NOT edit WORM records to "fix" data; append a correction instead.

## Doc sync on completion

- `docs/03-build-spec.md` M12 and `docs/07-security-notes.md` §6: one scheme.

## Branch & PR

- Branch: `p2/P2-B007-client-order-id-derivation`
- PR title: `P2-B007: define client order ID and intent ledger scheme`

## Progress log

- 2026-10-21 00:00 · planner · opened
