---
id: P1-T071
kind: task
title: Build the egress IP and country check
phase: 1
type: BUILD
status: backlog
priority: high
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P1-T004, P1-T005, P0-T017, P0-T035, P0-T051]
requirements: [R1.16]
roadmap_todos: [T1.33]
modules: [M16, M17]
dashboards: [D16, D06]
tools: [git, uv, docker, pnpm, node>=20]
mcp: []
env: []
services: [nats, postgres]
branch: p1/P1-T071-egress-ip-country-check
pr: ""
doc_sync: [docs/roadmap/phase-1-data-and-monitoring.md, docs/02-v1-architecture.md, docs/ui/dashboards/D16-system.md]
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

# P1-T071 · Build the egress IP and country check

## Goal / expected outcome

Every minute (default, configurable) `monitor` confirms that exchange traffic leaves via the allow-listed egress IP and that the IP's country matches your configured residency, using a free GeoIP database; the result is published as `egress.status` (NATS + KV) for M11 (which blocks new orders on a mismatch from P2) and alerts on a mismatch. It's a safety check only, never a tax input.

## Context & references

- Roadmap: requirement [R1.16](../../../docs/roadmap/phase-1-data-and-monitoring.md#3-requirements) · ToDo [T1.33](../../../docs/roadmap/phase-1-data-and-monitoring.md#4-todo-sets)
- Design: [16 §3.2](../../../docs/16-configuration-and-safety-model.md#32-network-egress-and-ip-locked-keys) (one fixed AU egress IP; egress check every minute; free GeoIP DB e.g. DB-IP Lite (CC BY); mismatch blocks new orders + alerts; not a tax input) · [17 §A](../../../docs/17-decisions-register.md#a-s2-items-all-resolved) P7-B004
- Subjects: [02 §6](../../../docs/02-v1-architecture.md#6-messaging-nats) `egress.status` (monitor → risk, UI) · degraded modes [02 §9.3](../../../docs/02-v1-architecture.md#93-degraded-modes) ("Egress IP or country mismatch: new orders blocked; alert / red egress chip")
- UI: [D16 System](../../../docs/ui/dashboards/D16-system.md) Egress panel (IP, country vs residency, last check) · [D06 Risk](../../../docs/ui/dashboards/D06-risk.md) risk-state strip shows the egress check (P2)
- Consumers: P2 inline pre-trade safety checks (R2.58, T2.39) read `egress.status`; P7 points the expected IP at the static exit node (R7.14, T7.42)
- Keys IP allow-list: [07 §3](../../../docs/07-security-notes.md#3-broker--exchange-keys); until the P7 exit node exists, the expected IP is the one your testnet keys are allow-listed to (recorded in P1-T002)
- Cross-phase prerequisites: P0-T017 (settings + clock), P0-T035 (confirmation levels: changing the expected IP or residency is C3), P0-T051 (D16 Health page that hosts the Egress tile)
- Depends on (this phase): P1-T004 (streams/KV), P1-T005 (connector base: the check runs through the same egress path and quota hooks)

## Requirements

- Settings (all configurable defaults in `config/egress.yaml`, linked to [16 §3.2](../../../docs/16-configuration-and-safety-model.md#32-network-egress-and-ip-locked-keys)): `expected_ips` (list; empty → status `unconfigured`, a warning, never `ok`), `residency_country` (default `AU`), `interval_s` (default 60), `observers` (≥ 2 free "what is my IP" endpoints, e.g. `api.ipify.org`, `ifconfig.co/json`; agreement required), `geoip_db` path
- The probe uses the **same HTTP client, network and route** as venue traffic (the `core` egress allow-list; from P7 the exit-node tunnel) so it measures what the exchanges see
- GeoIP: DB-IP Lite country MMDB (CC BY 4.0) downloaded monthly by a Prefect flow, checksum-verified, attribution shown in D16; no paid GeoIP API
- Status: `ok | ip_mismatch | country_mismatch | observers_disagree | unreachable | unconfigured`, with observed IP (shown masked except to you in D16), country, expected, checked_at; published on `egress.status` and KV `egress` (history 1) on change and every interval
- Mismatch or `unreachable` for 2 consecutive checks (default) → `alert.critical.egress` on every channel; recovery → `alert.info.egress_ok`; `unconfigured` → `alert.warning.egress_unconfigured` once a day
- Changing `expected_ips` or `residency_country` is a `system.settings.update` that **loosens** a safety gate → C3 (break-glass CLI `mtctl approve` + TOTP until Telegram C3 lands in P2); setting them stricter is C1
- D16 Health: Egress tile (IP masked, country vs residency, last check, status chip; red on mismatch) via `/system/health` and WS `system`
- Metrics: `mt_egress_status{status}`, `mt_egress_check_seconds`; Grafana panel added to the system board

## ToDo

- [ ] Implement `mt_monitor.egress` (observers, agreement rule, GeoIP lookup, status machine) and the KV/NATS publisher
- [ ] Add the monthly DB-IP Lite download flow with checksum and attribution
- [ ] Add `config/egress.yaml` defaults and the C1/C3 classification hook for these settings
- [ ] Add the D16 Egress tile (component library v0, all data states)
- [ ] Add `egress.status` to the WS fan-out and the alert rules
- [ ] Write the tests listed under Verification (keyless; observers and GeoIP faked in CI)
- [ ] Update the docs listed under Doc sync and tick the roadmap ToDo box

## Verification

### Tests

- Unit: status machine for every outcome; observers disagree → `observers_disagree` (not `ok`); empty expected list → `unconfigured`; GeoIP lookup against a fixture MMDB
- Unit: settings classification: removing an IP or tightening residency = C1; adding an IP or changing residency = C3 (pending until approved)
- Integration: fake observers on the test network → KV `egress` and `egress.status` messages; alert published after 2 consecutive mismatches
- Component (Vitest): Egress tile renders ok / mismatch / unconfigured / stale / error states

### Scenarios

- Given the observed IP differs from `expected_ips`, when two checks fail in a row, then `egress.status = ip_mismatch`, a critical alert reaches every channel, and the D16 tile turns red
- Given the observed IP is expected but GeoIP says a non-AU country, when checked, then `country_mismatch` is raised (safety only; nothing writes to tax residency)
- Given a C3 change to `expected_ips` is requested, when it hasn't been approved with TOTP and the cool-down hasn't passed, then the old value stays in force

### Stress / failure injection

- Fault: observers time out → `unreachable` after 2 checks (alert), never `ok`; GeoIP file missing or corrupt → status keeps IP checking and flags `geoip_unavailable`; NATS down → the check logs and retries, KV keeps the last value with its timestamp (consumers treat an old value as failed)

## Acceptance criteria

- [ ] `egress.status` published every interval with the documented states; KV `egress` holds the latest
- [ ] Mismatch alerts fire on every channel after the default 2 checks; D16 tile shows the state
- [ ] Changing the expected IP or residency requires C3; tightening is C1 (tested)
- [ ] CI green (ruff, mypy, pytest, `pit` bypass check, gitleaks, Playwright viewport matrix for the tile)

## Exceptions & edge cases

- Before P7 there is no static exit node: the expected IP is your current allow-listed IP; a home-broadband IP change shows as `ip_mismatch` (correct: testnet keys would also stop working)
- 4G failover before P7 changes the IP: mismatch is expected and alerted; P7's tunnel removes this
- GeoIP databases lag re-assignments: a single country mismatch with a matching expected IP is still raised (fail safe) and the runbook explains how to check it

## Cardinal rules (do NOT)

- Do NOT use the egress country as a tax-residency input; residency is your legal status (D15 timeline) ([16 §3.2](../../../docs/16-configuration-and-safety-model.md#32-network-egress-and-ip-locked-keys))
- Do NOT use a VPN/proxy to change the apparent location; the check exists to prove traffic leaves from Australia ([12 §3](../../../docs/12-policy-and-compliance.md#3-exchange-conduct--self-trade-prevention))
- Do NOT treat `unconfigured`, `unreachable` or an old KV value as `ok`
- Do NOT let any path loosen the egress settings without C3; tightening is C1
- Do NOT add paid data or APIs (DB-IP Lite is free, CC BY with attribution) ([03 §1](../../../docs/03-build-spec.md#1-ground-rules))
- Do NOT commit secrets; do NOT skip, weaken or delete a test to get CI green

## Doc sync on completion

- `docs/roadmap/phase-1-data-and-monitoring.md`: tick T1.33; note P1-T071 next to it.
- `docs/02-v1-architecture.md` §6: confirm the `egress.status` payload (states listed above) and KV `egress` in §5.1.
- `docs/ui/dashboards/D16-system.md`: confirm the Egress panel fields and the DB-IP attribution.

## Branch & PR

- Branch: `p1/P1-T071-egress-ip-country-check`
- PR title: `P1-T071: Build the egress IP and country check`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P1-T071` run

## Progress log

- 2026-10-22 00:00 · aligner · created for T1.33 / R1.16 (docs/16–17 alignment)
