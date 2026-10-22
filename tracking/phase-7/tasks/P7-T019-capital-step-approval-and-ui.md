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
depends_on: [P7-T018, P7-T016, P7-T020, P7-T025, P2-T035]
requirements: [R7.05, R7.08, R7.15]
roadmap_todos: [T7.21, T7.06, T7.26]
modules: [M11, M15]
dashboards: [D06, D03, D01]
tools: [git, uv, pnpm, node>=20]
mcp: []
env: []
services: [postgres, nats, mt-api, telegram bot api]
branch: p7/P7-T019-capital-step-approval-and-ui
pr: ""
doc_sync: [docs/02-v1-architecture.md, docs/ui/dashboards/D06-risk.md, docs/ui/dashboards/D03-strategies.md, docs/ui/mobile-and-telegram.md, docs/roadmap/phase-7-prove-and-go-live.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-22
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
review_result: ""
---

# P7-T019 · Capital-step proposals, C3 approval and D03/D06 step views

## Goal / expected outcome

When a sleeve is step-eligible, a proposal appears in D01 Needs-you and Telegram; approving it runs the C3 flow (approve + TOTP + 15-min cool-down), re-runs preflight and the gate check, then raises the bot's allocation by the step (+25% of current) and logs it.

## Context & references

- Roadmap: [R7.05, R7.08 · ToDo T7.21, T7.06](../../../docs/roadmap/phase-7-prove-and-go-live.md)
- Spec: [14 §7](../../../docs/14-strategy-evidence-and-validation.md#7-phase-capital-steps--kill-criteria-refines-04-phase-7) · [16 §2.5](../../../docs/16-configuration-and-safety-model.md#25-capital-steps-per-sleevebot) · [16 §2.3](../../../docs/16-configuration-and-safety-model.md#23-decisions-approvals-and-hitl) (C3 cool-down 15 min) · [07 §6](../../../docs/07-security-notes.md#6-application-controls) (raising a limit = C3) · [02 §7.2](../../../docs/02-v1-architecture.md#72-commands-rest-write) (C3 flow) · [mob §3](../../../docs/ui/mobile-and-telegram.md#3-telegram-bot) (C3 confirmations) · [D06](../../../docs/ui/dashboards/D06-risk.md) · [D03](../../../docs/ui/dashboards/D03-strategies.md)
- Related: P7-T018, P7-T011 (preflight), P7-T014 (gate report), P7-T061 (you approving), P7-T067 (composes the D06 Live tab) · cross-phase P2-T035 (Telegram C3 TOTP prompt, `depends_on`)

## Requirements

- Commands (02 §7.2 catalogue): `risk.capital.fund` (first funding at the bot's starting allocation, default A$2,000, **C3**, used by P7-T057) and `risk.capital_step.approve` (**C3**). Proposals are system events (`risk.event` type `capital_step_proposed`), not commands; declining = dismissing the card (recorded, no change); reducing an allocation is `risk.policy.update` (tightening, C1, immediate).
- On approve after cool-down: re-check eligibility, preflight (incl. AUSTRAC < 90 days), latest gate report pass ≤ 7 days; then apply a `risk.policy.update` loosening of the bot's allocation via the existing change-control service.
- Proposal expires after 7 days if not approved; a new dirty week cancels it. Once you start the C3 flow, the approval + TOTP must complete within the C3 approval TTL (default 10 min, 16 §2.3) or nothing applies.
- UI: `CapitalStepCard` (used by the D06 Live tab and D03 Go-live, composed in P7-T067) shows starting allocation, current allocation and step, clean-week streak (0–4) with the current week's checklist, next step amount, unsigned-review warnings, step-down history; D01 Needs-you card; phone ≤ 3 taps to reach the C3 confirmation.
- Funding the venue is a separate manual action; the system shows the required top-up amount but never moves money.

## ToDo

- [ ] Commands + server-side C3 classification.
- [ ] Integration with change-control (`risk.policy.update` diff).
- [ ] `CapitalStepCard` + history table; D01 Needs-you card; Telegram C3 message template.
- [ ] Tests (incl. Playwright matrix); docs.

## Verification

### Tests
- Integration: approve without TOTP → rejected; with TOTP → applies only after cool-down; dirty week during cool-down → cancelled.
- Integration: preflight failing at apply time (registry stale) → not applied, alert raised.
- Playwright: D06 sleeve card at all §6.8 viewports; axe clean.

### Scenarios
- Given an eligible micro-live bot at its A$2,000 starting allocation, when you approve, then after the 15-min cool-down its allocation becomes A$2,500 and the WORM log shows the approval chain.
- Given you reduce capital (tighten), then it applies immediately without C3.
- Given a proposal is 8 days old, then it expires; the clean streak stands and a fresh proposal is created next Monday.

### Stress / failure injection
- Telegram down during approval: C3 cannot complete (fail closed); web shows 'C3 channel unavailable'. Duplicate approve messages are idempotent.

## Acceptance criteria

- [ ] Capital increases only via C3 with re-checks at apply time.
- [ ] `CapitalStepCard` and the Needs-you card live (D06/D03 composition in P7-T067) and on phone.
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

- `docs/02-v1-architecture.md` §7.2: confirm `risk.capital.fund` / `risk.capital_step.approve` (C3) as built.
- `docs/ui/dashboards/D06-risk.md` and `D03-strategies.md`: sleeve capital-step views.
- `docs/ui/mobile-and-telegram.md` §3: capital-step C3 message.
- `docs/roadmap/phase-7-prove-and-go-live.md`: tick T7.21, T7.06 when this item is done.

## Branch & PR

- Branch: `p7/P7-T019-capital-step-approval-and-ui`
- PR title: `P7-T019: Capital-step proposals, C3 approval and D03/D06 step views`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P7-T019` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (+25% of current from the per-bot starting allocation (default A$2,000, 16 §2.5); commands per the 02 §7.2 catalogue; R7.15 share; dep P2-T035)
