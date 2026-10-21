---
id: P5-T064
kind: task
title: Phase 5 exit demo
phase: 5
type: VERIFY
status: backlog
priority: critical
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P5-T001, P5-T002, P5-T004, P5-T005, P5-T006, P5-T007, P5-T008, P5-T051, P5-T052, P5-T053, P5-T054, P5-T055, P5-T056, P5-T057, P5-T058, P5-T059, P5-T060, P5-T061, P5-T062, P5-T063]
requirements: [R5.01, R5.02, R5.03, R5.04, R5.05, R5.06, R5.07, R5.10, R5.11, R5.12, R5.13, R5.14, R5.15, R5.16, R5.17, R5.18, R5.20, R5.21, R5.22, R5.23, R5.N1, R5.N2]
roadmap_todos: []
modules: [M4, M19, M22, M18]
dashboards: [D12, D13, D18]
branch: p5/P5-T064-phase-5-exit-demo
pr: ""
doc_sync: [docs/roadmap/phase-5-airdrops-wallets-curation.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P5-T064 · Phase 5 exit demo

## Goal / expected outcome

A recorded demo walks every exit criterion: (1) a weekly digest of vetted airdrops/launches with EV, steps and verified links; (2) a testnet auto-claim with simulation proof, mandate and journal links, and a scam rejected with reasons; (3) the drainer suite passing and D18 showing every registered wallet reconciled to the journal — plus a check that all tasks are done/cancelled and no S1/S2 bugs are open.

## Context & references

- Roadmap: [§6 exit criteria](../../../docs/roadmap/phase-5-airdrops-wallets-curation.md) · entry criteria for P6 (signer, cost gate, wallet view)
- Evidence from P5-T052 (drainer), P5-T056 (testnet claim), P5-T059 (recon week), P5-T060 (scam rejected), P5-T063 (digests)

## Requirements

- Demo script `docs/demos/phase-5.md` (or progress-log section) listing each criterion, the command/screen used and the evidence link.
- Criterion 1: show the latest weekly digest in Telegram and the D13 preview; every link verified.
- Criterion 2: D12 history for the testnet claim (mandate, simulation diff, tx, journal) and a rejected scam with reasons.
- Criterion 3: CI run of the drainer suite (green) and D18 with recon status green for every registered wallet.
- Plus: kill drill evidence, network isolation result, policy matrix, chaos outcome table, SoK report.

## ToDo

- [ ] Collect evidence links from the dependent items.
- [ ] Run the demo end to end with you (≈ 45 min); record it.
- [ ] Tick the exit-criteria boxes in `tracking/phase-5/PHASE.md`.
- [ ] Confirm all P5 tasks done/cancelled and no open S1/S2 bugs; `./kanban validate --phase 5`.

## Verification

### Tests
- Each exit criterion demonstrated live with evidence links.

### Scenarios
- Given any criterion fails during the demo, then a bug item is filed (S1/S2) and the demo is rerun after the fix.

### Stress / failure injection
- n/a: demonstration (stress covered by P5-T062)

## Acceptance criteria

- [ ] Exit criterion 1 demonstrated
- [ ] Exit criterion 2 demonstrated
- [ ] Exit criterion 3 demonstrated
- [ ] All tasks done/cancelled; no open S1/S2 bugs
- [ ] PHASE.md exit boxes ticked

## Exceptions & edge cases

- A RUN item still within its window (none expected) is recorded as started, not blocking, per the planning brief.

## Cardinal rules (do NOT)

- Do NOT demo on mainnet funds beyond the funded floats; do NOT bypass any check to make the demo work.
- Do NOT apply loosening (new mandate, higher caps, autonomous claims) without C3 (Telegram approve + TOTP + cool-down); protective actions (revoke, sweep, kill) never wait for approval.
- Do NOT move value outside the configured caps/floats; exchange keys stay read-only or trade-only, IP-locked, withdrawals disabled; no live trading before the P7 gates.
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.

## Doc sync on completion

- `tracking/phase-5/PHASE.md`: exit-criteria boxes ticked (the generated roadmap blocks update via `./kanban build`).
- `docs/roadmap/phase-5-airdrops-wallets-curation.md`: tick the related exit criterion when this lands (with the other tasks sharing that ToDo).

## Branch & PR

- Branch: `p5/P5-T064-phase-5-exit-demo`
- PR title: `P5-T064: Phase 5 exit demo`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P5-T064` run

## Progress log

- 2026-10-21 00:00 · planner · created
