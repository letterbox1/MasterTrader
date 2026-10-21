---
id: P7-T057
kind: task
title: Fund micro-live (A$2–5k) after the gate report passes
phase: 7
type: USER
status: backlog
priority: critical
size: XS
severity: ""
owner: user
claimed_by: ""
depends_on: [P7-T001, P7-T011, P7-T014, P7-T044, P7-T045, P7-T046, P7-T047, P7-T053, P7-T056]
requirements: [R7.05, R7.01]
roadmap_todos: [T7.04]
modules: [M11]
dashboards: [D06, D03, D05]
branch: p7/P7-T057-fund-micro-live
pr: ""
doc_sync: [docs/14-strategy-evidence-and-validation.md, docs/roadmap/phase-7-prove-and-go-live.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P7-T057 · Fund micro-live (A$2–5k) after the gate report passes

## Goal / expected outcome

You transfer A$2–5k into the first live sub-account (one P1 sleeve, HITL mode) only after preflight and the gate report pass, and confirm the funding in the system so the sleeve's capital state becomes `micro_live`.

## Context & references

- Roadmap: [R7.05, R7.01 · ToDo T7.04](../../../docs/roadmap/phase-7-prove-and-go-live.md)
- Spec: [14 §7](../../../docs/14-strategy-evidence-and-validation.md#7-phase-capital-steps--kill-criteria-refines-04-phase-7) (micro-live A$2–5k) · [14 §3](../../../docs/14-strategy-evidence-and-validation.md#3-strategy-catalogue-evidence-ranked-templates) (trend A$2–5k minimum) · [07 §3](../../../docs/07-security-notes.md#3-broker--exchange-keys) (transfers are manual, outside the system) · Roadmap exit criterion 1
- Related: P7-T011, P7-T014, P7-T046, P7-T047, P7-T059

## Requirements

- Preconditions shown in D06 before you transfer: preflight all green; latest gate report `pass` ≤ 7 days; registry re-check < 90 days for this venue.
- Amount: A$2,000–5,000; sleeve capital limit set to the funded amount (tightening is C1; first funding from 0 is a C3 loosening).
- Mode: HITL first (approve mode); autonomous only later via P7-T058.
- Confirmation: `risk.capital.fund {sleeve, amount, venue_subaccount}` (C3) after the deposit is visible in recon.

## ToDo

- [ ] Open D06 → sleeve → 'Fund micro-live'; confirm all preconditions are green (screenshot).
- [ ] Transfer the amount from your bank to the venue sub-account yourself.
- [ ] Wait for recon to show the balance; then confirm funding via C3 (Telegram approve + TOTP).
- [ ] Start the bot in HITL mode (C2) from D03.
- [ ] Note the start date in the progress log (starts P7-T059 and P7-T062).

## Verification

### Tests
- n/a (user action); preflight and C3 enforced by P7-T011/T019.

### Scenarios
- Given preflight is red, then the 'Fund' action is disabled and lists what is missing.

### Stress / failure injection
- n/a: one-off action.

## Acceptance criteria

- [ ] Sub-account funded with A$2–5k; capital state `micro_live`; bot running in HITL.
- [ ] WORM records show gate report id and preflight snapshot.

## Exceptions & edge cases

- Deposit delayed/held (Travel Rule checks): wait; do not confirm funding before recon shows it.

## Cardinal rules (do NOT)

- Do NOT fund before the gate report and preflight pass.
- Do NOT fund more than A$5,000 at this stage.
- Do NOT use keys that are not trade-only, IP-locked and withdrawal-disabled; no live money before the P7 gates pass.
- Do NOT let loosening risk, autonomous mode or a capital step apply without C3 (Telegram + TOTP + cool-down); protective exits never wait for approval.
- Do NOT weaken a gate, threshold or window to "get live sooner" (roadmap §1, Out).

## Doc sync on completion

- `docs/14-strategy-evidence-and-validation.md` §7: note micro-live start date for the first sleeve.
- `docs/roadmap/phase-7-prove-and-go-live.md`: tick T7.04 when this item is done.

## Branch & PR

- Branch: `p7/P7-T057-fund-micro-live`
- PR title: `P7-T057: Fund micro-live (A$2–5k) after the gate report passes`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P7-T057` run · evidence (redacted, no secrets) linked in the progress log

## Progress log

- 2026-10-21 00:00 · planner · created
