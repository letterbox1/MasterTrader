---
id: P7-T054
kind: task
title: Phone test: ≤ 3-tap flows, PWA installed, C3 on phone
phase: 7
type: VERIFY
status: backlog
priority: high
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P7-T039, P7-T040]
requirements: [R7.12]
roadmap_todos: [T7.25]
modules: [M15]
dashboards: [D01, D05, D06]
branch: p7/P7-T054-verify-phone-flows-and-pwa
pr: ""
doc_sync: [docs/ui/mobile-and-telegram.md, docs/roadmap/phase-7-prove-and-go-live.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P7-T054 · Phone test: ≤ 3-tap flows, PWA installed, C3 on phone

## Goal / expected outcome

On your actual phone with the PWA installed, every phone flow in mob §2 completes in ≤ 3 taps from a cold open, `/kill` halts within 1 s of confirm, and every C3 change (incl. capital step and autonomous promotion) completes end to end without a desktop.

## Context & references

- Roadmap: [R7.12 · ToDo T7.25](../../../docs/roadmap/phase-7-prove-and-go-live.md)
- Spec: [mob §2](../../../docs/ui/mobile-and-telegram.md#2-phone-flows-must-be--3-taps-from-a-cold-open) · [mob §4](../../../docs/ui/mobile-and-telegram.md#4-acceptance-criteria) (kill < 1 s; C3 on phone; viewports) · [DESIGN.md §6.8](../../../DESIGN.md#68-test-matrix-every-screen-must-pass) · Roadmap R7.12 'Verified by: phone test'
- Related: P7-T039, P7-T040, P7-T041 (optional)

## Requirements

- Flows: HALT; approve an order; check safety; see P&L; close a position; complete a task; read the morning brief; plus approve capital step (C3) and promote bot (C3).
- Measured tap counts recorded per flow (Playwright on the matrix + a manual run on your phone).
- Viewport matrix incl. 280×653 and 568×320 green for the touched screens.

## ToDo

- [ ] Install the PWA on your phone (Android/iOS).
- [ ] Run each flow from a cold open; record taps and time.
- [ ] Run `/kill` timing check (engine metric).
- [ ] Run the Playwright tap-count suite in CI.
- [ ] File bugs for any flow > 3 taps.

## Verification

### Tests
- Playwright tap-count suite; axe checks; kill latency metric.

### Scenarios
- Given the phone is locked, when an approval notification arrives, then unlock → tap notification → hold-to-confirm completes the approval (≤ 3 taps after unlock).

### Stress / failure injection
- Run the approve flow on throttled 3G (Playwright network profile): still within TTL and ≤ 3 taps.

## Acceptance criteria

- [ ] All flows ≤ 3 taps; kill < 1 s; C3 flows complete on phone.
- [ ] Evidence recorded (redacted screenshots).

## Exceptions & edge cases

- iOS PWA push limitations: Telegram remains the primary channel; record which channel was used.

## Cardinal rules (do NOT)

- Do NOT count TOTP digit entry as extra 'taps' to game the metric — record it explicitly as the TOTP step.
- Do NOT let loosening risk, autonomous mode or a capital step apply without C3 (Telegram + TOTP + cool-down); protective exits never wait for approval.
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.

## Doc sync on completion

- `docs/ui/mobile-and-telegram.md` §4: measured results.
- `docs/roadmap/phase-7-prove-and-go-live.md`: tick T7.25 when this item is done.

## Branch & PR

- Branch: `p7/P7-T054-verify-phone-flows-and-pwa`
- PR title: `P7-T054: Phone test: ≤ 3-tap flows, PWA installed, C3 on phone`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P7-T054` run · evidence (redacted, no secrets) linked in the progress log

## Progress log

- 2026-10-21 00:00 · planner · created
