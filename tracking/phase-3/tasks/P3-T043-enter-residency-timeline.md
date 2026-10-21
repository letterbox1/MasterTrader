---
id: P3-T043
kind: task
title: Enter your residency timeline
phase: 3
type: USER
status: backlog
priority: medium
size: XS
severity: ""
owner: user
claimed_by: ""
depends_on: [P3-T031, P3-T041]
requirements: [R3.09]
roadmap_todos: [T3.05]
modules: [M18]
dashboards: [D15]
branch: p3/P3-T043-enter-residency-timeline
pr: ""
doc_sync: [docs/roadmap/phase-3-journal-and-tax.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P3-T043 · Enter your residency timeline

## Goal / expected outcome

The residency timeline holds your Australian residency period (from your arrival or birth date to open-ended) and any planned moves as notes, so plugin selection, I1 modelling and the Egypt hard flag work from real data.

## Context & references

- Roadmap: [R3.09, T3.05](../../../docs/roadmap/phase-3-journal-and-tax.md) · D15 Residency tab [D15](../../../docs/ui/dashboards/D15-tax.md) · mechanism P3-T031

## Requirements

- In D15 → Residency → Add period: country AU, from (date you became an AU tax resident), to empty; evidence notes (encrypted) optional.
- Planned moves: **do not** enter future periods until dates are firm; record intentions as a TAX_QUESTION (DTA/tie-breaker) instead.
- Review the recomputation preview and confirm (C1).

## ToDo

- [ ] Add the AU period via D15 (or `tax.residency.add`)
- [ ] Check the jurisdiction badge shows AU_2026 for FY2026-27
- [ ] Log any planned move as a TAX_QUESTION

## Verification

### Tests

- Confirmation: `/tax/residency` returns the AU period; D15 badge AU.

### Scenarios

- Given only an AU period, when D15 opens, then no compliance flags show and AU_2026 is active.

### Stress / failure injection

- n/a

## Acceptance criteria

- [ ] AU period entered and confirmed
- [ ] Badge shows AU

## Exceptions & edge cases

- Entering an EG period activates the crypto hard flag immediately for that date range (P3-T033).

## Cardinal rules (do NOT)

- Do NOT enter passport numbers or addresses in evidence notes beyond what the agent needs.
- Do NOT commit secrets or paste them into chats/issues; secrets live only in the sops/age file ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Do NOT present output as tax advice; every tax surface carries "Not tax advice. Confirm with a registered tax agent."
- Loosening risk, autonomous mode and mandates are C3 (Telegram + TOTP + cool-down); protective exits never wait for approval.

## Doc sync on completion

- `docs/roadmap/phase-3-journal-and-tax.md`: tick T3.05 once every item mapped to it is done.

## Branch & PR

- Branch: `p3/P3-T043-enter-residency-timeline` (only if this action changes a config/seed file; otherwise no PR)
- PR title: `P3-T043: Enter your residency timeline`
- Checklist: steps done · outputs stored where stated (secrets only in the sops file) · confirmation recorded in the progress log · `./kanban done P3-T043` run

## Progress log

- 2026-10-21 00:00 · planner · created
