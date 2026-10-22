---
id: P1-T072
kind: task
title: Egress fault test: wrong IP or country blocks new orders and alerts
phase: 1
type: VERIFY
status: backlog
priority: high
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P1-T071, P1-T045]
requirements: [R1.16]
roadmap_todos: [T1.65]
modules: [M16, M17]
dashboards: [D16]
tools: [git, uv, docker]
mcp: []
env: []
services: [nats, postgres, ntfy]
branch: p1/P1-T072-verify-egress-fault-test
pr: ""
doc_sync: [docs/roadmap/phase-1-data-and-monitoring.md, docs/02-v1-architecture.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-22
updated: 2026-10-22
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
review_result: ""
---

# P1-T072 · Egress fault test: wrong IP or country blocks new orders and alerts

## Goal / expected outcome

On the running stack, a wrong egress IP and a wrong egress country each flip `egress.status` to a blocking state within two check intervals, raise a critical alert through the one fan-out, turn the D16 egress tile red, and make the pre-trade gate contract reject new orders while exits pass. The report is stored as R1.16 evidence.

## Context & references

- Roadmap: requirement [R1.16](../../../docs/roadmap/phase-1-data-and-monitoring.md#3-requirements) · ToDo [T1.65](../../../docs/roadmap/phase-1-data-and-monitoring.md#4-todo-sets)
- Design: [16 §3.2](../../../docs/16-configuration-and-safety-model.md#32-network-egress-and-ip-locked-keys) · degraded modes [02 §9.3](../../../docs/02-v1-architecture.md#93-degraded-modes) · alert list [07 §9](../../../docs/07-security-notes.md#9-monitoring--incident-response) ("egress IP/country mismatch or tunnel down")
- M11 is built in P2: the real order rejection is proven by P2's safety-state golden tests (R2.58, T2.71). Here the gate is the shared `mt_risk.safety.egress_allows(entry|exit)` contract function that P2 calls, tested against live `egress.status`
- Depends on (this phase): P1-T071 (check), P1-T045 (alert fan-out)

## Requirements

- E2E suite `tests/e2e/egress_fault.py` (`make e2e-egress`) against the dev stack, keyless: the probe's observers are pointed at a local fake that returns a chosen IP; GeoIP uses a fixture MMDB mapping that IP to a chosen country
- Cases: (1) IP not in `expected_ips`; (2) expected IP but country ≠ `residency_country`; (3) observers disagree; (4) observers unreachable; (5) `expected_ips` empty (`unconfigured`); (6) recovery to `ok`
- For each: assert `egress.status` and KV `egress`, time to state (≤ 2 intervals at a test interval of 5 s), `alert.critical.egress` delivered to the notifier with dedupe, D16 tile state (Playwright), and `egress_allows("entry") == False` / `egress_allows("exit") == True` for blocking states
- Also assert a stale KV value (older than 3 intervals) is treated as blocking by `egress_allows`
- Report with timings under `reports/verify/P1-T072/`

## ToDo

- [ ] Write the fake observer, fixture MMDB and the e2e suite
- [ ] Add the `egress_allows` contract tests (shared with P2)
- [ ] Run all six cases 10× and store the report
- [ ] Update the docs listed under Doc sync and tick the roadmap ToDo box

## Verification

### Tests

- E2E suite as described; runs nightly in CI against Compose

### Scenarios

- Given the observed IP changes to one not on the list, when two checks fail, then entries are refused by the gate, exits still pass, a critical alert reaches every enabled channel, and D16 shows red
- Given the country changes while the IP matches, when checked, then `country_mismatch` blocks entries the same way
- Given the fault clears, when the next check passes, then the status returns to `ok`, an info alert is sent, and entries are allowed again

### Stress / failure injection

- This task is the fault test; add a chaos run (random case every 30 s for 15 min): no missed detection, no stuck state, no alert storm (dedupe holds)

## Acceptance criteria

- [ ] All six cases pass 10/10 runs; blocking states reached within 2 intervals
- [ ] Entries blocked and exits allowed through the gate contract in every blocking state
- [ ] Report stored with timings

## Exceptions & edge cases

- Live tunnel/failover behaviour (broadband → 4G with the same exit-node IP) is P7's drill (T7.64), not this task
- The test never changes your real `expected_ips`; it runs with a test settings profile

## Cardinal rules (do NOT)

- Do NOT weaken the agreement or two-check rule to make a run pass
- Do NOT point the test at real venues or real keys; keyless only
- Do NOT use the egress result for tax residency
- Do NOT skip, weaken or delete a test (or widen a tolerance) to get CI green

## Doc sync on completion

- `docs/roadmap/phase-1-data-and-monitoring.md`: tick T1.65; note P1-T072 next to it.
- `docs/02-v1-architecture.md` §9.3: confirm the egress mismatch row matches the observed behaviour.

## Branch & PR

- Branch: `p1/P1-T072-verify-egress-fault-test`
- PR title: `P1-T072: Egress fault test: wrong IP or country blocks new orders and alerts`
- PR checklist: suite added · report stored · docs synced · task file ticked · `./kanban done P1-T072` run

## Progress log

- 2026-10-22 00:00 · aligner · created for T1.65 / R1.16 (docs/16–17 alignment)
