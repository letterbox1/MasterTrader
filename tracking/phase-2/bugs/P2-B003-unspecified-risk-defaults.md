---
id: P2-B003
kind: gap
title: "Risk defaults left unspecified: dead-man N, collar %, decision deadlines, cost-blowout and downgrade thresholds"
phase: 2
type: DOC
status: backlog
priority: high
size: XS
severity: S3
owner: agent
claimed_by: ""
depends_on: []
requirements: [R2.14, R2.16, R2.18, R2.53]
roadmap_todos: []
modules: [M11]
dashboards: []
branch: p2/P2-B003-unspecified-risk-defaults
pr: ""
doc_sync: [docs/14-strategy-evidence-and-validation.md, docs/03-build-spec.md, docs/15-bots-hitl-and-worm-audit.md]
doc_sync_status: n/a
found_in: docs/03-build-spec.md M11/M16; docs/14 §5; docs/15 §1.2
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P2-B003 · Risk defaults left unspecified: dead-man N, collar %, decision deadlines, cost-blowout and downgrade thresholds

## Goal / expected outcome

Every threshold the risk manager needs has a documented default (user-editable in policy), so goldens and drills have numbers.

## Context & references

- [03 M11](../../../docs/03-build-spec.md#m11-risk-manager--mt_risk-built-in-user-inputs-via-uitelegram-later-mcp) · [03 M16](../../../docs/03-build-spec.md#m16-live-cost--data-quality-monitor--mt_monitor-always-on-autonomous) · [14 §5](../../../docs/14-strategy-evidence-and-validation.md#5-risk-engine-additions-m11) · [15 §1.2](../../../docs/15-bots-hitl-and-worm-audit.md#1-trading-bots)
- Affects P2-T012, P2-T017, P2-T031, P2-T032, P2-T037, P2-T048.

## Requirements

- **Steps to reproduce:** Search the docs for defaults of: dead-man 'N seconds' and heartbeat interval; price collar 'within X%'; decision deadline 'per sleeve'; spread 'N× normal'; automatic kill on 'cost blow-out'; auto-downgrade on 'N consecutive losses'; '1× until approved' (approved how?).
- **Expected:** A default per item (e.g. heartbeat 1 s, dead-man 10 s, collar 2% crypto / 0.5% FX, decision deadline 2 s fast / 60 s slow sleeves, spread 3× normal, kill on cost ratio > 3× (pause at 1.5×), N consecutive losses 5, leverage raise = C3).
- **Actual:** Only placeholders (N, X) or 'per sleeve' without numbers.
- **Suggested fix:** Adopt the example defaults above as proposals in 14 §5; you confirm or change them in P2-T048; code ships them only as policy defaults.
- **Impact:** S3: tasks can be built but tests/drills need agreed numbers.

## ToDo

- [ ] Decide the rule with the user (or record the decision taken in the linked task)
- [ ] Update the source doc(s) so they agree
- [ ] Update the affected task file(s) to match

## Verification

### Tests
- The affected task's tests encode the decided rule (named in that task).

### Scenarios
- Given the defaults are documented, when goldens are written (P2-T051), then each threshold has boundary cases.

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

- `docs/14-strategy-evidence-and-validation.md` §5: add the defaults table rows.

## Branch & PR

- Branch: `p2/P2-B003-unspecified-risk-defaults`
- PR title: `P2-B003: document missing risk default thresholds`

## Progress log

- 2026-10-21 00:00 · planner · opened
