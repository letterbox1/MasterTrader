---
id: P7-T019
kind: task
title: Capital-step proposals, C3 approval and D03/D06 step views
phase: 7
type: BUILD
status: backlog
priority: critical
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P7-T018, P7-T016, P7-T020, P7-T025]
requirements: [R7.05, R7.08]
roadmap_todos: [T7.21, T7.06]
modules: [M11, M15]
dashboards: [D06, D03, D01]
branch: p7/P7-T019-capital-step-approval-and-ui
pr: ""
doc_sync: [docs/02-v1-architecture.md, docs/ui/dashboards/D06-risk.md, docs/ui/dashboards/D03-strategies.md, docs/ui/mobile-and-telegram.md, docs/roadmap/phase-7-prove-and-go-live.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P7-T019 · Capital-step proposals, C3 approval and D03/D06 step views

## Goal / expected outcome

When a sleeve is step-eligible, a proposal appears in D01 Needs-you and Telegram; approving it runs the C3 flow (approve + TOTP + 15-min cool-down), re-runs preflight and the gate check, then raises the sleeve capital limit by the step amount and logs it.

## Context & references

- Roadmap: [R7.05, R7.08 · ToDo T7.21, T7.06](../../../docs/roadmap/phase-7-prove-and-go-live.md)
- Spec: [14 §7](../../../docs/14-strategy-evidence-and-validation.md#7-phase-capital-steps--kill-criteria-refines-04-phase-7) · [07 §6](../../../docs/07-security-notes.md#6-application-controls) (raising a limit = C3) · [02 §7.2](../../../docs/02-v1-architecture.md#72-commands-rest-write) (C3 flow) · [mob §3](../../../docs/ui/mobile-and-telegram.md#3-telegram-bot) (C3 confirmations) · [D06](../../../docs/ui/dashboards/D06-risk.md) · [D03](../../../docs/ui/dashboards/D03-strategies.md)
- Related: P7-T018, P7-T011 (preflight), P7-T014 (gate report), P7-T061 (you approving)

## Requirements

- Commands: `risk.capital.fund` (first funding from 0 → micro_live, **C3**, used by P7-T057), `risk.capital_step.propose` (system), `risk.capital_step.approve` (**C3**), `risk.capital_step.reject` (C1), `risk.capital_step.reduce` (tightening, C1, immediate).
- On approve after cool-down: re-check eligibility, preflight (incl. AUSTRAC < 90 days), latest gate report pass ≤ 7 days; then apply a `risk.policy.update` loosening of the sleeve capital limit via the existing change-control service.
- Proposal expires after 7 days if not approved; a new dirty week cancels it.
- UI: D06 sleeve card shows state, clean-week streak (0–4), next step amount, history; D03 strategy Overview shows the same; D01 Needs-you card; phone ≤ 3 taps to reach the C3 confirmation.
- Funding the venue is a separate manual action; the system shows the required top-up amount but never moves money.

## ToDo

- [ ] Commands + server-side C3 classification.
- [ ] Integration with change-control (`risk.policy.update` diff).
- [ ] D06 sleeve card + history table; D03 Overview widget; D01 Needs-you card; Telegram C3 message template.
- [ ] Tests (incl. Playwright matrix); docs.

## Verification

### Tests
- Integration: approve without TOTP → rejected; with TOTP → applies only after cool-down; dirty week during cool-down → cancelled.
- Integration: preflight failing at apply time (registry stale) → not applied, alert raised.
- Playwright: D06 sleeve card at all §6.8 viewports; axe clean.

### Scenarios
- Given an eligible micro-live sleeve at A$4,000, when you approve, then after 15 min the sleeve limit becomes A$5,000 and the WORM log shows the approval chain.
- Given you reduce capital (tighten), then it applies immediately without C3.
- Given a proposal is 8 days old, then it expires; the clean streak stands and a fresh proposal is created next Monday.

### Stress / failure injection
- Telegram down during approval: C3 cannot complete (fail closed); web shows 'C3 channel unavailable'. Duplicate approve messages are idempotent.

## Acceptance criteria

- [ ] Capital increases only via C3 with re-checks at apply time.
- [ ] Step views live in D06/D03/D01 and on phone.
- [ ] Every step is in the WORM log with the gate report id and preflight snapshot.
- [ ] CI green.

## Exceptions & edge cases

- Hard ceiling lower than the step: step is capped at the ceiling and the UI says so.
- Two sleeves eligible the same week: separate proposals, separate C3 confirmations.

## Cardinal rules (do NOT)

- Do NOT move funds or call venue transfer endpoints; funding is manual.
- Do NOT batch several capital steps into one C3 confirmation.
- Do NOT let loosening risk, autonomous mode or a capital step apply without C3 (Telegram + TOTP + cool-down); protective exits never wait for approval.
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order goes through M11.
- Do NOT update or delete WORM rows; corrections are new rows with `supersedes_id` (15 §2).
- Do NOT use keys that are not trade-only, IP-locked and withdrawal-disabled; no live money before the P7 gates pass.
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.

## Doc sync on completion

- `docs/02-v1-architecture.md` §7.2: `risk.capital_step.*` commands (C3 for approve).
- `docs/ui/dashboards/D06-risk.md` and `D03-strategies.md`: sleeve capital-step views.
- `docs/ui/mobile-and-telegram.md` §3: capital-step C3 message.
- `docs/roadmap/phase-7-prove-and-go-live.md`: tick T7.21, T7.06 when this item is done.

## Branch & PR

- Branch: `p7/P7-T019-capital-step-approval-and-ui`
- PR title: `P7-T019: Capital-step proposals, C3 approval and D03/D06 step views`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P7-T019` run

## Progress log

- 2026-10-21 00:00 · planner · created
