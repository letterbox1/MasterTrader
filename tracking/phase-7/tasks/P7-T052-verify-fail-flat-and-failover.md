---
id: P7-T052
kind: task
title: Automated fail-flat and 4G failover test
phase: 7
type: VERIFY
status: backlog
priority: critical
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P7-T033]
requirements: [R7.11]
roadmap_todos: [T7.41]
modules: [M11, M12]
dashboards: [D06, D16]
branch: p7/P7-T052-verify-fail-flat-and-failover
pr: ""
doc_sync: [docs/07-security-notes.md, docs/roadmap/phase-7-prove-and-go-live.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P7-T052 · Automated fail-flat and 4G failover test

## Goal / expected outcome

A scripted test with paper positions proves: a link loss shorter than N keeps trading, longer than N fails flat, UPS low-battery fails flat before shutdown, resting broker-side stops remain at the venue throughout, and egress IP is unchanged on 4G.

## Context & references

- Roadmap: [R7.11 · ToDo T7.41](../../../docs/roadmap/phase-7-prove-and-go-live.md)
- Spec: [07 §5](../../../docs/07-security-notes.md#5-network--host) · Roadmap R7.11 'Verified by: pull-the-plug drill' (this is the automated precursor)
- Related: P7-T033, P7-T030, P7-T009, P7-T053

## Requirements

- Cases: egress blocked 60 s (no flatten), 120 s (fail flat), NUT `LOWBATT` (fail flat + shutdown), 4G switch (egress IP same; venue calls succeed).
- After each: recon clean; resting stops present for remaining positions; timings recorded.

## ToDo

- [ ] Script `tools/drills/failflat_test.sh` (iptables egress block, NUT dummy driver).
- [ ] Run on the host with paper positions.
- [ ] Attach results.

## Verification

### Tests
- The script asserts each case's outcome via `mt_api` queries and venue REST.

### Scenarios
- Given a 120 s outage, then cancels and flatten are sent at N + 1 s and the venue confirms after reconnection.

### Stress / failure injection
- The test is the fault injection; repeat the 120 s case 3 times.

## Acceptance criteria

- [ ] All four cases pass and are recorded.

## Exceptions & edge cases

- Script must restore networking on exit (trap).

## Cardinal rules (do NOT)

- Do NOT run this with live positions.
- Do NOT use keys that are not trade-only, IP-locked and withdrawal-disabled; no live money before the P7 gates pass.
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.

## Doc sync on completion

- `docs/07-security-notes.md` §5: measured results.
- `docs/roadmap/phase-7-prove-and-go-live.md`: tick T7.41 when this item is done.

## Branch & PR

- Branch: `p7/P7-T052-verify-fail-flat-and-failover`
- PR title: `P7-T052: Automated fail-flat and 4G failover test`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P7-T052` run · evidence (redacted, no secrets) linked in the progress log

## Progress log

- 2026-10-21 00:00 · planner · created
