---
id: P2-B004
kind: gap
title: D06 shows a 5-rung ladder and different sleeve names than M11/14
phase: 2
type: DOC
status: backlog
priority: medium
size: XS
severity: S3
owner: agent
claimed_by: ""
depends_on: []
requirements: [R2.15, R2.13]
roadmap_todos: []
modules: [M11]
dashboards: [D06]
branch: p2/P2-B004-d06-ladder-rungs-sleeve-names
pr: ""
doc_sync: [docs/ui/dashboards/D06-risk.md]
doc_sync_status: n/a
found_in: docs/ui/dashboards/D06-risk.md 'Additions from the CryptoTrader review'
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P2-B004 · D06 shows a 5-rung ladder and different sleeve names than M11/14

## Goal / expected outcome

D06 matches the 6-rung ladder in 03 M11 / 14 §5 and the sleeve list in 14 §3.

## Context & references

- [D06 additions](../../../docs/ui/dashboards/D06-risk.md) · [03 M11 ladder](../../../docs/03-build-spec.md#m11-risk-manager--mt_risk-built-in-user-inputs-via-uitelegram-later-mcp) · [14 §3 allocation](../../../docs/14-strategy-evidence-and-validation.md#3-strategy-catalogue-evidence-ranked-templates) · [14 §5 ladder](../../../docs/14-strategy-evidence-and-validation.md#5-risk-engine-additions-m11)
- Affects P2-T018, P2-T042, P2-T049.

## Requirements

- **Steps to reproduce:** D06: 'Current rung (normal → reduced size → close-only → flat → kill)' and sleeves 'core / carry / momentum / experimental'.
- **Expected:** Six rungs: normal · half size/observe · hold · rules only (exits) · halt sleeve · kill; sleeves named from policy (14 §3 suggests trend, carry, hold-and-earn, memecoin, unlock/event, plus manual).
- **Actual:** Five differently named rungs; sleeve names don't match any other doc.
- **Suggested fix:** Edit D06 to the six rungs and 'sleeves from policy (example: 14 §3 list + manual)'. P2-T042 renders rungs and sleeves from the API, not hard-coded.
- **Impact:** S3: UI and engine would disagree on rung numbers (auto-downgrade uses rung ≥ 3).

## ToDo

- [ ] Decide the rule with the user (or record the decision taken in the linked task)
- [ ] Update the source doc(s) so they agree
- [ ] Update the affected task file(s) to match

## Verification

### Tests
- The affected task's tests encode the decided rule (named in that task).

### Scenarios
- Given rung 4 in the engine, when D06 renders, then it shows 'Rules only — exits, no entries'.

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

- `docs/ui/dashboards/D06-risk.md`: ladder + sleeves text.

## Branch & PR

- Branch: `p2/P2-B004-d06-ladder-rungs-sleeve-names`
- PR title: `P2-B004: align D06 ladder rungs and sleeve names`

## Progress log

- 2026-10-21 00:00 · planner · opened
