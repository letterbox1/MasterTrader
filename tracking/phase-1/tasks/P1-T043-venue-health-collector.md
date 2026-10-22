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
depends_on: [P1-T005, P0-T025]
requirements: [R1.13]
roadmap_todos: [T1.30]
modules: [M16]
dashboards: [D07]
tools: [git, uv, docker]
mcp: []
env: []
services: [nats, postgres]
branch: p1/P1-T043-venue-health-collector
pr: ""
doc_sync: [docs/roadmap/phase-1-data-and-monitoring.md, docs/12-policy-and-compliance.md, docs/13-wallets-treasury-and-onchain.md]
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

# P1-T043 · Collect venue health into the venue registry

## Goal / expected outcome

A collector maintains the health fields of `ops.venue_registry` from our own measured withdrawal/deposit times, venue deposit/withdraw flags and your proof-of-reserve/incident notes, accepts venue status-page/feed signals from the P4 regulatory & venue watch (R4.15) through a defined input, and raises the quarterly AUSTRAC re-check reminder that drives your USER task (P1-T069); a D07 panel shows it.

## Context & references

- Roadmap: requirements [R1.13](../../../docs/roadmap/phase-1-data-and-monitoring.md#3-requirements) · ToDo [T1.30](../../../docs/roadmap/phase-1-data-and-monitoring.md#4-todo-sets)
- Spec: [12 §2](../../../docs/12-policy-and-compliance.md#2-venue-access-registry) (registry fields incl. health; AUSTRAC status re-checked quarterly) · [13 §6](../../../docs/13-wallets-treasury-and-onchain.md#6-monitors-feed-m16-and-m11) (venue health monitor) · [12 §6](../../../docs/12-policy-and-compliance.md#6-professional-advice-triggers-tracked-as-tasks-in-d13--d15)
- Registry table seeded in P0 (R0.06); venue registry changes emit `venue.registry.changed` ([02 §6](../../../docs/02-v1-architecture.md#6-messaging-nats))
- Decision: [17 §D](../../../docs/17-decisions-register.md#d-other-decisions) P1-B014 (our measured withdrawal times + venue status pages/feeds via the regulatory & venue watch + a quarterly AUSTRAC register check as a USER task) · [12 §2](../../../docs/12-policy-and-compliance.md#2-venue-access-registry) health row · [13 §6](../../../docs/13-wallets-treasury-and-onchain.md#6-monitors-feed-m16-and-m11)
- Status pages/feeds and PoR pages arrive with the P4 regulatory & venue watch (R4.15, T4.30); this task defines the `venue.health.signal` input it publishes to
- Cross-phase prerequisite (depends_on): P0-T025 (`ops.venue_registry`)
- Depends on (this phase): P1-T005

## Requirements

- Health table `ops.venue_health` (venue, signal, value, observed_at, source) linked to the registry; registry gets derived `health_status` (ok|watch|degraded) and `austrac_checked_at`
- Signals: (1) **our measured withdrawal/deposit times** (request → completion) from the venue's withdrawal/deposit history via read-only endpoints (fixtures in P1; live once live read-only keys exist) and from transfers you record by hand, rolled into p50/p95 per venue × asset; (2) per-asset deposit/withdraw enabled flags from public endpoints where offered; (3) your PoR/incident notes via `venue.registry.update` (health note, C1); (4) status-page/feed signals published on `venue.health.signal` by the P4 venue watch (schema defined here, fixture-tested)
- Health changes never change `allowed/read_only/blocked` (policy is user/C3 only); they emit `venue.registry.changed` with `kind=health` and `alert.warning.venue_health`
- AUSTRAC reminder: when `austrac_checked_at` is older than 90 days (default, configurable) → notification + Telegram via `alert.info.austrac_recheck` with the venue list and the register URL (a `VENUE_CHECK` task once the P5 task queue exists); you do the check (USER task P1-T069) and record it via `venue.registry.update`; the system never scrapes the AUSTRAC site; `mt-monitor venue-health remind --now` forces a cycle

## ToDo

- [ ] Migration for `ops.venue_health` and the derived columns
- [ ] Withdrawal/deposit-time measurement from history endpoints (fixtures) and hand-recorded transfers; deposit/withdraw flag collectors; the `venue.health.signal` input for P4
- [ ] AUSTRAC reminder job (daily check, quarterly trigger)
- [ ] D07 panel data via `/venues/registry` (P1-T046)
- [ ] Write the tests listed under Verification
- [ ] Update the docs listed under Doc sync and tick the roadmap ToDo box(es)

## Verification

### Tests

- Unit: signal → health_status rules; reminder date maths
- Integration: fixtures of withdrawal history and deposit/withdraw flags → rows and p50/p95 times; a fixture `venue.health.signal` message → health change; `venue.registry.changed` emitted

### Scenarios

- Given Binance reports withdrawals suspended for USDT, when collected, then health is `watch` with that reason and an alert fires; the registry `status` stays unchanged
- Given 91 days since the last AUSTRAC check, when the daily job runs, then the reminder appears in notifications and Telegram

### Stress / failure injection

- n/a: polling every 15 min (default); low volume

## Acceptance criteria

- [ ] Health fields populated for every registry venue from the P1 signals (fixtures where keys are needed); the reminder fires in a time-travel test and drives P1-T069
- [ ] CI green (ruff, mypy, pytest, `pit` bypass check, gitleaks)

## Exceptions & edge cases

- A signal source down: that signal is `unknown`, not `degraded`; before P4 there are no status-page signals and the panel says they arrive with the venue watch

## Cardinal rules (do NOT)

- Do NOT let the collector change a venue's allow/block status
- Do NOT scrape the AUSTRAC register or venue websites against their terms
- Do NOT commit secrets or paste them into chats, issues, logs or test fixtures; credentials come only from the sops/age secrets file (kept outside the repo) mounted on tmpfs ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Do NOT skip, weaken or delete a test (or widen a tolerance) to get CI green.
- Do NOT add paid data or APIs, exceed a free tier, or scrape against a site's terms; no self-bots or user tokens ([03 §1](../../../docs/03-build-spec.md#1-ground-rules)).
- Do NOT let any path loosen DQ thresholds, risk or alert routing without C3 (Telegram + TOTP + cool-down; in P1 via the break-glass CLI `mtctl approve` + TOTP); tightening is C1.

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
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (venue-health inputs per P1-B014 (own withdrawal times, flags, notes; status feeds via P4 watch); AUSTRAC reminder drives USER task P1-T069; P0 dep on registry)
