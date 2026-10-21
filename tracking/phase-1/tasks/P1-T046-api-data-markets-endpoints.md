---
id: P1-T046
kind: task
title: Expose data and markets queries and commands in mt_api
phase: 1
type: BUILD
status: backlog
priority: critical
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P1-T030, P1-T038, P1-T041, P1-T006, P1-T013]
requirements: [R1.15, R1.08, R1.10, R1.11, R1.12]
roadmap_todos: [T1.32]
modules: [M15, M16, M1]
dashboards: [D07, D02]
branch: p1/P1-T046-api-data-markets-endpoints
pr: ""
doc_sync: [docs/roadmap/phase-1-data-and-monitoring.md, docs/02-v1-architecture.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P1-T046 · Expose data and markets queries and commands in mt_api

## Goal / expected outcome

`mt_api` serves every P1 query and command the D07/D02 backend contracts list, with OpenAPI types for the web app and audited, confirmation-levelled commands.

## Context & references

- Roadmap: requirements [R1.15](../../../docs/roadmap/phase-1-data-and-monitoring.md#3-requirements), [R1.08](../../../docs/roadmap/phase-1-data-and-monitoring.md#3-requirements), [R1.10](../../../docs/roadmap/phase-1-data-and-monitoring.md#3-requirements), [R1.11](../../../docs/roadmap/phase-1-data-and-monitoring.md#3-requirements), [R1.12](../../../docs/roadmap/phase-1-data-and-monitoring.md#3-requirements) · ToDo [T1.32](../../../docs/roadmap/phase-1-data-and-monitoring.md#4-todo-sets)
- API: [02 §7.1](../../../docs/02-v1-architecture.md#71-queries-rest-read) (queries) · [02 §7.2](../../../docs/02-v1-architecture.md#72-commands-rest-write) (commands, confirmation levels) · contracts in [D07 Data & Quality](../../../docs/ui/dashboards/D07-data-quality.md) and [D02 Markets](../../../docs/ui/dashboards/D02-markets.md) "Backend contract"
- P0 prerequisite: T0.24 `mt_api` skeleton (auth, command bus, `audit.command`, problem+json)
- Depends on (this phase): P1-T030, P1-T038, P1-T041, P1-T006, P1-T013

## Requirements

- Queries: `/data/feeds`, `/data/quotas`, `/data/dq-events`, `/data/costs` (incl. `?instrument=`, `?compare=1`), `/data/recon`, `/data/feeds?storage=1`, `/lab/jobs?kind=backfill`, `/markets/instruments` (+`/{id}`), `/markets/{id}/bars?spec=&from=&to=`, `/markets/{id}/book`, `/markets/matrix` (+`?group=macro|positioning|correlation`), `/venues/registry`, `/notifications`
- Commands: `data.feed.pause|resume` (C1, response lists dependent strategies, none yet in P1), `data.backfill.run` (C1), `data.recon.run` (C1), `system.settings.update` for DQ thresholds (tighten C1, loosen C3) and incident ack (see P1-B018); `intel.watchlist.update` (C0)
- Paid-feed guard: resuming a `cost: paid` source returns 409 problem+json
- Cursor pagination; Decimals as strings; ISO-8601 UTC; read paths use `mt_store` query helpers (bars via P1-T013 helper)
- Latency: p95 < 150 ms for `/data/feeds` and cached bar ranges (budget inside the 500 ms D02 timeframe-switch target)

## ToDo

- [ ] Implement routers, schemas and command handlers
- [ ] Regenerate OpenAPI and `openapi-typescript` types for `apps/web`
- [ ] Contract test against the D07/D02 backend-contract lists
- [ ] Write the tests listed under Verification
- [ ] Update the docs listed under Doc sync and tick the roadmap ToDo box(es)

## Verification

### Tests

- Unit: each handler's validation; confirmation level per command (C3 path rejects without approval)
- Integration: endpoints against a seeded DB; pagination; problem+json errors
- Contract: every endpoint/topic named in D07/D02 for P1 exists in OpenAPI (CI check)

### Scenarios

- Given a loosening threshold change via `system.settings.update`, when sent without approval + TOTP, then it is held as pending C3 and not applied
- Given `/markets/{id}/bars?spec=7m`, when requested, then it returns time_bucket bars with `on_the_fly=true`

### Stress / failure injection

- Load: 50 concurrent bar requests over 1 year of 1m data; p95 < 300 ms on the target host

## Acceptance criteria

- [ ] All P1 endpoints and commands exist, are typed in OpenAPI, and every command lands in `audit.command`
- [ ] CI green (ruff, mypy, pytest, `pit` bypass check, gitleaks)

## Exceptions & edge cases

- Postgres down: endpoints return 503 problem+json and the UI shows read-only banner (02 §9.3)

## Cardinal rules (do NOT)

- Do NOT bypass `mt_api`, the risk manager (M11) or `mt_store.pit(as_of)`; research and backtest reads go through `pit` only.
- Do NOT UPDATE or DELETE WORM rows (`audit.*`); resolutions and corrections are new rows with `supersedes_id` ([15 §2](../../../docs/15-bots-hitl-and-worm-audit.md#2-worm-records-write-once-read-many)).
- Do NOT skip, weaken or delete a test (or widen a tolerance) to get CI green.
- Do NOT let any path loosen DQ thresholds, risk or alert routing without C3 (Telegram + TOTP + cool-down); tightening is C1.
- Do NOT commit secrets or paste them into chats, issues, logs or test fixtures; credentials come only from the sops/age secrets file mounted on tmpfs ([07 §2](../../../docs/07-security-notes.md#2-secrets)).

## Doc sync on completion

- `docs/roadmap/phase-1-data-and-monitoring.md`: tick T1.32 once every task traced to it in PHASE.md is done; note P1-T046 next to it.
- `docs/02-v1-architecture.md` §7.1: confirm the `/data/*` and `/markets/*` parameters actually implemented

## Branch & PR

- Branch: `p1/P1-T046-api-data-markets-endpoints`
- PR title: `P1-T046: Expose data and markets queries and commands in mt_api`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P1-T046` run

## Progress log

- 2026-10-21 00:00 · planner · created
