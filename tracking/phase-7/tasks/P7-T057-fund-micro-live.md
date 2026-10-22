---
id: P7-T057
kind: task
title: Fund the starting allocation (default A$2,000) after the gate report passes
phase: 7
type: USER
status: backlog
priority: critical
size: XS
severity: ""
owner: user
claimed_by: ""
depends_on: [P7-T001, P7-T011, P7-T014, P7-T044, P7-T045, P7-T046, P7-T047, P7-T053, P7-T056, P7-T069]
requirements: [R7.05, R7.01]
roadmap_todos: [T7.04]
modules: [M11]
dashboards: [D06, D03, D05]
tools: []
mcp: []
env: []
services: [venue live sub-account, your bank]
branch: p7/P7-T057-fund-micro-live
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

# P7-T057 · Fund the starting allocation (default A$2,000) after the gate report passes

## Goal / expected outcome

You set the first bot's **starting live allocation** in its strategy settings (default A$2,000; suggested micro-live range A$2–5k), transfer that amount into its live sub-account (one P1 sleeve, `hitl` mode) only after preflight, the gate report and the stress replay are in, and confirm the funding so the bot's capital state becomes `micro_live`.

## Context & references

- Roadmap: [R7.05, R7.01 · ToDo T7.04](../../../docs/roadmap/phase-7-prove-and-go-live.md)
- Spec: [14 §7](../../../docs/14-strategy-evidence-and-validation.md#7-phase-capital-steps--kill-criteria-refines-04-phase-7) (micro-live starting allocation per bot) · [16 §2.5](../../../docs/16-configuration-and-safety-model.md#25-capital-steps-per-sleevebot) (default A$2,000, set per bot when it goes live; [17 §E](../../../docs/17-decisions-register.md#e-ratification-2026-10-22)) · [14 §3](../../../docs/14-strategy-evidence-and-validation.md#3-strategy-catalogue-evidence-ranked-templates) (trend A$2–5k minimum) · [07 §3](../../../docs/07-security-notes.md#3-broker--exchange-keys) (transfers are manual, outside the system) · Roadmap exit criterion 1
- Related: P7-T011, P7-T014, P7-T046, P7-T047 (live key audit, T7.65), P7-T069 (stress replay, T7.66), P7-T067 (D03 Go-live, D06 Live), P7-T059

## Requirements

- Preconditions shown in D06/D03 before you transfer: preflight all green (incl. egress `ok`); latest gate report `pass` ≤ 7 days with the stress-replay results attached; registry re-check < 90 days for this venue; live key audit `pass`.
- Amount: the bot's starting allocation (default A$2,000, suggested A$2–5k), set in its strategy settings (D03 Go-live); the funding confirmation is a C3 loosening from 0.
- Mode: every bot starts live in `hitl` (R7.08); autonomous only later via P7-T058 (C3).
- Confirmation: `risk.capital.fund {bot, amount, venue_subaccount}` (C3) after the deposit is visible in recon.

## ToDo

- [ ] In D03 → bot → Go-live, set the starting allocation (default A$2,000); then in D06 → Live → 'Fund the starting allocation' confirm all preconditions are green (screenshot).
- [ ] Transfer the amount from your bank to the venue sub-account yourself.
- [ ] Wait for recon to show the balance; then confirm funding via C3 (Telegram approve + TOTP).
- [ ] Start the bot in HITL mode (C2) from D03.
- [ ] Note the start date in the progress log (starts P7-T059 and the yearly review schedule from P7-T042).

## Verification

### Tests
- n/a (user action); preflight and C3 enforced by P7-T011/T019.

### Scenarios
- Given preflight is red, then the 'Fund' action is disabled and lists what is missing.

### Stress / failure injection
- n/a: one-off action.

## Acceptance criteria

- [ ] Sub-account funded with the bot's starting allocation; capital state `micro_live`; bot running in `hitl`.
- [ ] WORM records show gate report id and preflight snapshot.

## Exceptions & edge cases

- Deposit delayed/held (Travel Rule checks): wait; do not confirm funding before recon shows it.

## Cardinal rules (do NOT)

- Do NOT fund before the gate report, the stress replay and preflight pass.
- Do NOT fund more than the bot's starting allocation set in its strategy settings.
- Do NOT use keys that are not trade-only, IP-locked and withdrawal-disabled; no live money before the P7 gates pass.
- Do NOT let loosening risk, autonomous mode or a capital step apply without C3 (Telegram + TOTP + cool-down); protective exits never wait for approval.
- Do NOT weaken a gate, threshold or window to "get live sooner" (roadmap §1, Out).

## Doc sync on completion

- `docs/14-strategy-evidence-and-validation.md` §7: note micro-live start date for the first sleeve.
- `docs/roadmap/phase-7-prove-and-go-live.md`: tick T7.04 when this item is done.

## Branch & PR

- Branch: `p7/P7-T057-fund-micro-live`
- PR title: `P7-T057: Fund the starting allocation (default A$2,000) after the gate report passes`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P7-T057` run · evidence (redacted, no secrets) linked in the progress log

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (starting allocation per bot default A$2,000 (16 §2.5, 17 §E); stress replay (P7-T069) and live key audit before funding)
