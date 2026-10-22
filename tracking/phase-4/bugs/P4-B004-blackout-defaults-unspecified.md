---
id: P4-B004
kind: gap
title: Calendar blackout defaults (window, scope, action) are unspecified
phase: 4
type: DOC
status: done
priority: high
size: XS
severity: S3
owner: agent
claimed_by: ""
depends_on: []
requirements: [R4.10]
roadmap_todos: []
modules: [M5, M11]
dashboards: [D06]
branch: p4/P4-B004-blackout-defaults-unspecified
pr: ""
doc_sync: [docs/14-strategy-evidence-and-validation.md, docs/ui/dashboards/D06-risk.md, docs/03-build-spec.md]
doc_sync_status: done
found_in: docs/03-build-spec.md M5 and M11; docs/ui/dashboards/D06-risk.md (Blackouts node); docs/14 §5 defaults
created: 2026-10-21
updated: 2026-10-22
started: ""
completed: 2026-10-22
blocked_reason: ""
checkpoint: ""
---

# P4-B004 · Calendar blackout defaults (window, scope, action) are unspecified

## Goal / expected outcome

The risk-policy defaults include a concrete blackout rule set so P4-T038/T052 test against documented values, not a planner's proposal.

## Context & references

- Found in: [03 M5](../../../docs/03-build-spec.md#m5-calendars--mt_datacalendar) ('event within N minutes', 'pause scalpers around NFP') · [03 M11](../../../docs/03-build-spec.md#m11-risk-manager--mt_risk-built-in-user-inputs-via-uitelegram-later-mcp) · [D06](../../../docs/ui/dashboards/D06-risk.md)
- Related: P4-T038 (proposes 15 min before/after, high importance, block new entries for scalper/intraday tags), P4-T052.

## Requirements

- **Steps to reproduce:** look for N, importance threshold, affected strategies and action in 03/14/D06 — none given.
- **Expected:** documented defaults: importance ≥ high; macro releases + CB decisions; `pre_min = 15`, `post_min = 15`; scope = strategies tagged scalper/intraday on instruments mapped to the event's currency/country; action = block new entries (exits allowed); stale-calendar fail-safe.
- **Actual:** no defaults; behaviour on open positions unspecified.
- **Impact:** S3 — exit criterion 2 is testable only with assumed values.
- **Suggested fix:** add the defaults to 14 §5 defaults table and D06 Blackouts node (user can change; loosening is C3).

## ToDo

- [x] Decision recorded: blackout defaults in 16 §2.8 (17 §C)
- [x] Docs carry it: 16 §2.8 (15 min before to 15 min after high-importance events; bots marked `event_sensitive`, scalping/intraday by default; block new entries; exits and protective orders continue; configurable per bot and event type), 03 M5 'Default blackout', 14 §5 defaults row (D06 keeps a Blackouts policy node; its first-install defaults list doesn't repeat the values, a minor doc follow-up)
- [x] Implementation owned by P4-T038 (rule evaluator + M11 hook + seeded default) and P4-T052 (NFP blackout test)

## Verification

### Tests
- Doc review: the corrected section is consistent with the linked sources (links resolve).

### Scenarios
- Given the user prefers ±30 min, then they tighten via D06 (C1) and the test parameters follow the policy.

### Stress / failure injection
- n/a: documentation gap.

## Acceptance criteria

- [x] Blackout defaults documented (checked in 16 §2.8, 03 M5, 14 §5, 2026-10-22)
- [x] Root cause noted: 03 M5 said 'event within N minutes' without defaults

## Exceptions & edge cases

- Protective exits are never blocked (global rule).

## Cardinal rules (do NOT)

- Do NOT close without updating every listed doc.
- Do NOT edit WORM records to 'fix' data; append a correction instead.

## Doc sync on completion

- `docs/14-strategy-evidence-and-validation.md`: §5 defaults: blackout row
- `docs/ui/dashboards/D06-risk.md`: Blackouts node fields
- `docs/03-build-spec.md`: M5: default rule

## Branch & PR

- Branch: `p4/P4-B004-blackout-defaults-unspecified`
- PR title: `P4-B004: fix calendar blackout defaults (window, scope, action) are unspecified`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P4-B004` run

## Progress log

- 2026-10-21 00:00 · planner · opened
- 2026-10-22 00:00 · aligner · resolved by 17 §C (P4-B004 → 16 §2.8); docs checked: 16 §2.8, 03 M5 default blackout, 14 §5 calendar blackout row; implementation owned by P4-T038, P4-T052, P4-T045; root cause: M5 left N and scope unspecified
- 2026-10-22 02:04 · cloud:vm:be04b6ae61f8 · verified: decided in docs/17 §C (P4-B004 -> 16 §2.8); docs updated: 16 §2.8, 03 M5 default blackout, 14 §5 calendar blackout row; implementation owned by P4-T038, P4-T052, P4-T045
- 2026-10-22 02:04 · cloud:vm:be04b6ae61f8 · done
- 2026-10-22 02:04 · cloud:vm:be04b6ae61f8 · doc sync done: docs updated in the alignment wave
