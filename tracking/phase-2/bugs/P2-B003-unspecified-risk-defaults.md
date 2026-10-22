---
id: P2-B003
kind: gap
title: "Risk defaults left unspecified: dead-man N, collar %, decision deadlines, cost-blowout and downgrade thresholds"
phase: 2
type: DOC
status: done
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
tools: []
mcp: []
env: []
services: []
branch: p2/P2-B003-unspecified-risk-defaults
pr: ""
doc_sync: [docs/14-strategy-evidence-and-validation.md, docs/03-build-spec.md, docs/15-bots-hitl-and-worm-audit.md]
doc_sync_status: done
found_in: docs/03-build-spec.md M11/M16; docs/14 §5; docs/15 §1.2
created: 2026-10-21
updated: 2026-10-22
started: ""
completed: 2026-10-22
blocked_reason: ""
checkpoint: ""
review_result: ""
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

- [x] Defaults recorded in 16 §2–§3 for every open number (dead-man 5 s/10 s, collar 2%/0.5%/1%, deadlines 1 s/10 s/5 min/1 h, spread 3×, cost blow-out 1.5× over 20 fills → pause the bot, 5 consecutive losses → downgrade, leverage raise C3)
- [x] Docs agree: 14 §5 and 03 M11 reference 16
- [x] Tasks updated: values are policy defaults with 16 links (P2-T012, P2-T017, P2-T032, P2-T034, P2-T037, P2-T048, P2-T070)

## Verification

### Tests
- The affected task's tests encode the decided rule (named in that task).

### Scenarios
- Given the defaults are documented, when goldens are written (P2-T051), then each threshold has boundary cases.

### Stress / failure injection
- n/a: documentation/specification gap

## Acceptance criteria

- [x] Docs agree in one place, cross-linked from the others (16 §2.1 (collar, API-error pause, cost blow-out), §2.2 (stale 2 s/60 s), §2.3 (decision deadlines, TTLs, mode levels), §2.6 (5 losing trades downgrade), §3.1 (dead-man 5 s/10 s); 14 §5 table; 03 M11)
- [x] Affected tasks reference the decision (P2-T012, P2-T017, P2-T032, P2-T034, P2-T037, P2-T048, P2-T070)

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
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (resolved by 17 §C (P2-B003); docs carry it (16 §2.1 (collar, API-error pause, cost blow-out), §2.2 (stale 2 s/60 s), §2.3 (decision deadlines, TTLs, mode levels), §2.6 (5 losing trades downgrade), §3.1 (dead-man 5 s/10 s); 14 §5 table; 03 M11); implementation owned by P2-T012, P2-T017, P2-T032, P2-T034, P2-T037, P2-T048, P2-T070)
- 2026-10-22 02:14 · cloud:vm:be04b6ae61f8 · verified: decided in docs/17 (17 §C (P2-B003)); docs updated: 16 §2.1 (collar, API-error pause, cost blow-out), §2.2 (stale 2 s/60 s), §2.3 (decision deadlines, TTLs, mode levels), §2.6 (5 losing trades downgrade), §3.1 (dead-man 5 s/10 s); 14 §5 table; 03 M11; implementation owned by P2-T012, P2-T017, P2-T032, P2-T034, P2-T037, P2-T048, P2-T070
- 2026-10-22 02:14 · cloud:vm:be04b6ae61f8 · done
- 2026-10-22 02:14 · cloud:vm:be04b6ae61f8 · doc sync done: docs updated in the alignment wave
