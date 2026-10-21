---
id: P1-T043
kind: task
title: Collect venue health into the venue registry
phase: 1
type: BUILD
status: backlog
priority: medium
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P1-T005]
requirements: [R1.13]
roadmap_todos: [T1.30]
modules: [M16]
dashboards: [D07]
branch: p1/P1-T043-venue-health-collector
pr: ""
doc_sync: [docs/roadmap/phase-1-data-and-monitoring.md, docs/12-policy-and-compliance.md, docs/13-wallets-treasury-and-onchain.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P1-T043 · Collect venue health into the venue registry

## Goal / expected outcome

A collector updates the health fields of `ops.venue_registry` (venue system status, withdrawal suspensions/delays, proof-of-reserve and incident notes) and raises a quarterly AUSTRAC re-check reminder, shown in a D07 panel.

## Context & references

- Roadmap: requirements [R1.13](../../../docs/roadmap/phase-1-data-and-monitoring.md#3-requirements) · ToDo [T1.30](../../../docs/roadmap/phase-1-data-and-monitoring.md#4-todo-sets)
- Spec: [12 §2](../../../docs/12-policy-and-compliance.md#2-venue-access-registry) (registry fields incl. health; AUSTRAC status re-checked quarterly) · [13 §6](../../../docs/13-wallets-treasury-and-onchain.md#6-monitors-feed-m16-and-m11) (venue health monitor) · [12 §6](../../../docs/12-policy-and-compliance.md#6-professional-advice-triggers-tracked-as-tasks-in-d13--d15)
- Registry table seeded in P0 (R0.06); venue registry changes emit `venue.registry.changed` ([02 §6](../../../docs/02-v1-architecture.md#6-messaging-nats))
- Gaps: free sources for these signals are undefined (P1-B014)
- Depends on (this phase): P1-T005

## Requirements

- Health table `ops.venue_health` (venue, signal, value, observed_at, source) linked to the registry; registry gets derived `health_status` (ok|watch|degraded) and `austrac_checked_at`
- Signals: venue system-status endpoints (e.g. Binance `/sapi/v1/system/status`, Kraken `/0/public/SystemStatus`, OKX `/api/v5/system/status`), per-asset deposit/withdraw enabled flags from public or read-only endpoints, official status-page RSS where offered, user-entered PoR/incident notes via `venue.registry.update` (health note, C1)
- Health changes never change `allowed/read_only/blocked` (policy is user/C3 only); they emit `venue.registry.changed` with `kind=health` and `alert.warning.venue_health`
- AUSTRAC reminder: when `austrac_checked_at` is older than 90 days → notification + `alert.info.austrac_recheck` with the venue list and the register URL; you record the check via `venue.registry.update` (no scraping of the AUSTRAC site)

## ToDo

- [ ] Migration for `ops.venue_health` and the derived columns
- [ ] Collectors per venue; status-page RSS reader
- [ ] AUSTRAC reminder job (daily check, quarterly trigger)
- [ ] D07 panel data via `/venues/registry` (P1-T046)
- [ ] Write the tests listed under Verification
- [ ] Update the docs listed under Doc sync and tick the roadmap ToDo box(es)

## Verification

### Tests

- Unit: signal → health_status rules; reminder date maths
- Integration: fixtures of status endpoints → rows; `venue.registry.changed` emitted

### Scenarios

- Given Binance reports withdrawals suspended for USDT, when collected, then health is `watch` with that reason and an alert fires; the registry `status` stays unchanged
- Given 91 days since the last AUSTRAC check, when the daily job runs, then the reminder appears in notifications and Telegram

### Stress / failure injection

- n/a: polling every 15 min

## Acceptance criteria

- [ ] Health fields populated for every registry venue; reminder fires in a time-travel test
- [ ] CI green (ruff, mypy, pytest, `pit` bypass check, gitleaks)

## Exceptions & edge cases

- Status endpoints down: health `unknown`, not `degraded`

## Cardinal rules (do NOT)

- Do NOT let the collector change a venue's allow/block status
- Do NOT scrape the AUSTRAC register or venue websites against their terms
- Do NOT commit secrets or paste them into chats, issues, logs or test fixtures; credentials come only from the sops/age secrets file mounted on tmpfs ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Do NOT skip, weaken or delete a test (or widen a tolerance) to get CI green.
- Do NOT add paid data or APIs, exceed a free tier, or scrape against a site's terms; no self-bots or user tokens ([03 §1](../../../docs/03-build-spec.md#1-ground-rules)).
- Do NOT let any path loosen DQ thresholds, risk or alert routing without C3 (Telegram + TOTP + cool-down); tightening is C1.

## Doc sync on completion

- `docs/roadmap/phase-1-data-and-monitoring.md`: tick T1.30 once every task traced to it in PHASE.md is done; note P1-T043 next to it.
- `docs/12-policy-and-compliance.md` §2: describe health signals actually collected
- `docs/13-wallets-treasury-and-onchain.md` §6: link the venue health implementation

## Branch & PR

- Branch: `p1/P1-T043-venue-health-collector`
- PR title: `P1-T043: Collect venue health into the venue registry`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P1-T043` run

## Progress log

- 2026-10-21 00:00 · planner · created
