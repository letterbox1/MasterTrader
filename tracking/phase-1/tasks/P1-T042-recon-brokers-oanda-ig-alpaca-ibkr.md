---
id: P1-T042
kind: task
title: Reconcile OANDA, IG, Alpaca and IBKR paper accounts
phase: 1
type: BUILD
status: backlog
priority: high
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P1-T041]
requirements: [R1.12]
roadmap_todos: [T1.29]
modules: [M16]
dashboards: [D07]
tools: [git, uv, docker]
mcp: []
env: []
services: [nats, postgres]
branch: p1/P1-T042-recon-brokers-oanda-ig-alpaca-ibkr
pr: ""
doc_sync: [docs/roadmap/phase-1-data-and-monitoring.md, docs/03-build-spec.md, docs/02-v1-architecture.md]
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

# P1-T042 · Reconcile OANDA, IG, Alpaca and IBKR paper accounts

## Goal / expected outcome

Recon adapters for the OANDA practice, IG demo, Alpaca paper and IBKR paper accounts plug into the framework, so every practice venue is reconciled clean (exit criterion 2).

## Context & references

- Roadmap: requirements [R1.12](../../../docs/roadmap/phase-1-data-and-monitoring.md#3-requirements) · ToDo [T1.29](../../../docs/roadmap/phase-1-data-and-monitoring.md#4-todo-sets)
- Spec: [03 M16](../../../docs/03-build-spec.md#m16-live-cost--data-quality-monitor--mt_monitor-always-on-autonomous) · [phase 1 §6 exit criteria](../../../docs/roadmap/phase-1-data-and-monitoring.md#6-exit-criteria-demo) item 2
- IBKR paper goes through the `ib-gateway` container (P1-T070, [17 §D](../../../docs/17-decisions-register.md#d-other-decisions) P1-B013), only when you use IBKR
- Build first, keys last: all four adapters are built and tested against recorded fixtures; the live run with your practice credentials is P1-T074
- Depends on (this phase): P1-T041

## Requirements

- OANDA: account summary, open positions, open trades (thin httpx, GET only)
- IG: accounts, positions (REST, GET only)
- Alpaca: account, positions (GET only)
- IBKR paper: via the `ib-gateway` container (P1-T070) with `ib_async` positions + account values in read-only API mode; when `ibkr.enabled: false` the adapter reports `disabled (not used)`
- Same cadence, tolerances, `audit.recon` rows and `recon.*` publishing as P1-T041 (16 §2.9 defaults)

## ToDo

- [ ] Implement four adapters behind the GET-only client
- [ ] Wire the IBKR adapter to the `ib-gateway` service name from P1-T070 (fixture-tested; no container work here)
- [ ] Write the tests listed under Verification
- [ ] Update the docs listed under Doc sync and tick the roadmap ToDo box(es)

## Verification

### Tests

- Unit: response parsing per broker fixture
- Integration: injected mismatch per broker → incident
- Security: write attempts blocked before network

### Scenarios

- Given IG demo session expires, when recon runs, then it re-logs in and continues
- Given IB Gateway is not running, when recon runs, then IBKR shows `unreachable` and other venues are unaffected

### Stress / failure injection

- n/a: low-frequency polling; failure handling covered by scenarios

## Acceptance criteria

- [ ] Every adapter reconciles clean against fixtures and raises an incident on an injected mismatch; IBKR disabled cleanly when not used; the live run is P1-T074
- [ ] CI green (ruff, mypy, pytest, `pit` bypass check, gitleaks)

## Exceptions & edge cases

- OANDA/IG/Alpaca/IBKR practice credentials are not scope-limited (normal credentials, no money at risk, [17 §D](../../../docs/17-decisions-register.md#d-other-decisions) P1-B008); the GET-only allow-list stays as a tested safeguard

## Cardinal rules (do NOT)

- Do NOT UPDATE or DELETE WORM rows (`audit.*`); resolutions and corrections are new rows with `supersedes_id` ([15 §2](../../../docs/15-bots-hitl-and-worm-audit.md#2-worm-records-write-once-read-many)).
- Do NOT use keys with withdrawal rights, or without an IP allow-list where the venue supports one; practice/testnet/paper only, no live money before the P7 gates.
- Do NOT place, modify or cancel orders from this code; P1 is read-only toward venues (orders arrive in P2 through M11).
- Do NOT commit secrets or paste them into chats, issues, logs or test fixtures; credentials come only from the sops/age secrets file (kept outside the repo) mounted on tmpfs ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Do NOT skip, weaken or delete a test (or widen a tolerance) to get CI green.
- Do NOT add an image without pinning it by digest, or vendored code that carries telemetry or referral IDs.

## Doc sync on completion

- `docs/roadmap/phase-1-data-and-monitoring.md`: tick T1.29 once every task traced to it in PHASE.md is done; note P1-T042 next to it.
- `docs/03-build-spec.md` §M16: venues covered by reconciliation
- `docs/02-v1-architecture.md` §3.2: IB Gateway container if added

## Branch & PR

- Branch: `p1/P1-T042-recon-brokers-oanda-ig-alpaca-ibkr`
- PR title: `P1-T042: Reconcile OANDA, IG, Alpaca and IBKR paper accounts`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P1-T042` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (ib-gateway via P1-T070 (P1-B013); normal practice credentials (P1-B008); keyless build, live run in P1-T074)
