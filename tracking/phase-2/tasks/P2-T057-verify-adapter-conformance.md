---
id: P2-T057
kind: task
title: Adapter conformance on practice/testnet accounts
phase: 2
type: VERIFY
status: backlog
priority: high
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P2-T023, P2-T024, P2-T025, P2-T026, P2-T027]
requirements: [R2.30]
roadmap_todos: [T2.25]
modules: [M12]
dashboards: []
tools: [uv]
mcp: []
env: []
services: []
branch: p2/P2-T057-verify-adapter-conformance
pr: ""
doc_sync: [docs/03-build-spec.md, docs/roadmap/phase-2-strategies-risk-lab.md]
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

# P2-T057 · Adapter conformance on practice/testnet accounts

## Goal / expected outcome

One shared conformance suite runs keyless against the sandbox venue, mock servers and recorded cassettes for Binance testnet, Alpaca paper, OANDA practice and IG demo, proving submit/modify/cancel/fill/brackets/resting stops/reports/reconnect behave identically through the engine. The same suite runs against the real practice/testnet endpoints with your keys in P2-T071.

## Context & references

- Roadmap: [R2.30](../../../docs/roadmap/phase-2-strategies-risk-lab.md) · ToDo T2.25
- Spec: [03 M12](../../../docs/03-build-spec.md#m12-execution--mt_engine)
- Build first, keys last ([17 §E](../../../docs/17-decisions-register.md#e-ratification-2026-10-22)): no keys here; live run in P2-T071.
- Related: P2-T023–T027, P2-T073 (resting venue stops, cancel-after timers).

## Requirements

- Cases: market, limit (rest + cancel), modify price/qty, stop, bracket, partial fill, reject (insufficient margin, bad tick size), reconnect mid-order, status/fill/position reports for reconciliation.
- Runs per PR with cassettes and nightly against mock servers/emulators; the suite takes a `--live` flag used only by P2-T071 on the host runner.
- Output matrix venue × case pass/fail stored as artefact.

## ToDo

- [ ] `tests/conformance/` parametrised by venue
- [ ] Nightly runner on the host (not GitHub-hosted)
- [ ] Matrix report
- [ ] Record results (numbers, run IDs, screenshots) in the progress log and tick the roadmap ToDo box

## Verification

### Tests
- The suite.

### Scenarios
- Given the OANDA stream drops during a pending limit, when it reconnects, then the fill that happened meanwhile is recovered via reports.

### Stress / failure injection
- Nightly reconnect storm against mock servers: 10 forced disconnects in 5 min per venue; no lost fills.

## Acceptance criteria

- [ ] All cases pass on all four venues (or documented venue limitation)
- [ ] Nightly job green 3 nights running

## Exceptions & edge cases

- Venue doesn't support a case (e.g. modify on IG working orders): documented as N/A with reason.

## Cardinal rules (do NOT)

- Do NOT run conformance with live (real-money) credentials.
- Do NOT store venue keys in CI secrets of a hosted runner.
- Do NOT commit secrets or paste them into chats/issues/logs; secrets live in the sops/age file (07 §2).
- Do NOT skip, weaken or delete a test to get green; risk-manager golden tests are mandatory for merge.
- Keys are trade-only, IP-locked, withdrawals disabled. No live money before the P7 gates; this phase is paper/testnet/practice only.

## Doc sync on completion

- `docs/03-build-spec.md` M12: venue capability matrix.
- `docs/roadmap/phase-2-strategies-risk-lab.md`: tick T2.25 when all tasks mapped to it are done.

## Branch & PR

- Branch: `p2/P2-T057-verify-adapter-conformance`
- PR title: `P2-T057: Adapter conformance on practice/testnet accounts`
- PR checklist: tests added and green · docs synced · task file ticked · no secrets (gitleaks) · `./kanban done P2-T057` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (keyless conformance (cassettes, mock servers); live run moved to P2-T071; resting stops case)
