---
id: P7-T061
kind: task
title: Approve each capital step after 4 clean weeks (C3)
phase: 7
type: USER
status: backlog
priority: high
size: XS
severity: ""
owner: user
claimed_by: ""
depends_on: [P7-T019, P7-T059]
requirements: [R7.05]
roadmap_todos: [T7.06]
modules: [M11]
dashboards: [D06, D01]
tools: []
mcp: []
env: []
services: [telegram, TOTP app, your bank]
branch: p7/P7-T061-approve-capital-steps
pr: ""
doc_sync: [docs/14-strategy-evidence-and-validation.md, docs/roadmap/phase-7-prove-and-go-live.md]
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

# P7-T061 · Approve each capital step after 4 clean weeks (C3)

## Goal / expected outcome

When a sleeve shows 'step eligible' after 4 clean weeks, you approve (C3) or decline the step (+25% of the current allocation, up to the sleeve target cap), and top up the venue sub-account manually by the shown amount.

## Context & references

- Roadmap: [R7.05 · ToDo T7.06](../../../docs/roadmap/phase-7-prove-and-go-live.md)
- Spec: [14 §7](../../../docs/14-strategy-evidence-and-validation.md#7-phase-capital-steps--kill-criteria-refines-04-phase-7) (+25% of the current allocation after 4 consecutive clean weeks, up to the sleeve target cap, e.g. A$10–25k) · [16 §2.5](../../../docs/16-configuration-and-safety-model.md#25-capital-steps-per-sleevebot) · [07 §6](../../../docs/07-security-notes.md#6-application-controls) (raising a limit = C3)
- Related: P7-T019, P7-T059, P7-T046 (registry re-check before each funding)

## Requirements

- Approve only if the proposal shows all checks green at apply time (preflight, registry < 90 days, gate report ≤ 7 days).
- Top-up is manual from your bank/vault; confirm via recon before the bot uses the new capital.
- Declining is fine; record the reason.

## ToDo

- [ ] Open the Needs-you card or Telegram proposal.
- [ ] Check the evidence summary; approve via C3 (approve + TOTP) or decline.
- [ ] Transfer the top-up; confirm recon shows it.
- [ ] Record the decision and amount in the progress log.

## Verification

### Tests
- n/a (user action).

### Scenarios
- Given a step is approved but the top-up hasn't arrived, then the sleeve limit is raised but sizing uses actual venue balance (never more).

### Stress / failure injection
- n/a.

## Acceptance criteria

- [ ] Each eligible step during the phase is approved or declined with a record.
- [ ] No capital increase without C3.

## Exceptions & edge cases

- Phase exits before any step becomes eligible: this item is done as 'no eligible step yet', and step approvals continue as standing operations ([roadmap README §10](../../../docs/roadmap/README.md#10-standing-operations-recurring-outside-the-phases)).

## Cardinal rules (do NOT)

- Do NOT top up more than the approved step.
- Do NOT approve a step while any kill/decay warning is active (a warning already steps the allocation back one step, 16 §2.5).
- Do NOT let loosening risk, autonomous mode or a capital step apply without C3 (Telegram + TOTP + cool-down); protective exits never wait for approval.
- Do NOT use keys that are not trade-only, IP-locked and withdrawal-disabled; no live money before the P7 gates pass.

## Doc sync on completion

- `docs/14-strategy-evidence-and-validation.md` §7: none unless a rule changed.
- `docs/roadmap/phase-7-prove-and-go-live.md`: tick T7.06 when this item is done.

## Branch & PR

- Branch: `p7/P7-T061-approve-capital-steps`
- PR title: `P7-T061: Approve each capital step after 4 clean weeks (C3)`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P7-T061` run · evidence (redacted, no secrets) linked in the progress log

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (+25% of current up to the sleeve cap per 16 §2.5)
