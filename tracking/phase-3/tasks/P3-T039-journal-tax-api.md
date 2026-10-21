---
id: P3-T039
kind: task
title: Journal and tax API queries, commands and WebSocket topic
phase: 3
type: BUILD
status: backlog
priority: critical
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P3-T025, P3-T027, P3-T028, P3-T031, P3-T034, P3-T038]
requirements: [R3.13, R3.14]
roadmap_todos: [T3.29]
modules: [M18, M15]
dashboards: [D14, D15]
branch: p3/P3-T039-journal-tax-api
pr: ""
doc_sync: [docs/02-v1-architecture.md, docs/roadmap/phase-3-journal-and-tax.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P3-T039 · Journal and tax API queries, commands and WebSocket topic

## Goal / expected outcome

`mt_api` exposes the D14/D15 backend contract — `/journal/trades` (+ `/{id}`, `?analytics=1`), `/journal/events`, `/journal/lots`, `/tax/summary?fy=` (+ sections cgt/income/payg), `/tax/reports`, `/tax/residency`, `/data/recon?scope=journal` — and the commands `journal.note.add`, `journal.tag`, `tax.report.generate`, `tax.export`, `tax.residency.add`, `tax.regime.set`, `tax.lot.select` at their confirmation levels, plus the `journal` WS topic.

## Context & references

- Roadmap: [R3.13, R3.14, T3.29](../../../docs/roadmap/phase-3-journal-and-tax.md)
- [02 §7 API](../../../docs/02-v1-architecture.md#7-api-contract-mt_api) · [02 §7.2 commands](../../../docs/02-v1-architecture.md#72-commands-rest-write) · backend contracts in [D14](../../../docs/ui/dashboards/D14-journal.md) and [D15](../../../docs/ui/dashboards/D15-tax.md)
- Cross-phase: P0 T0.24 (`mt_api` skeleton, command bus, C-levels, WS hub)

## Requirements

- Queries read via `journal_ro`; cursor pagination; Decimals as strings; problem+json errors; every tax response includes `rule_version`, `fx_source`, `price_sources`, `result_hash`, `regime`, and the not-advice string.
- Round-trip trades: derived from events (open → close per position) with gross, fees, funding, net, R-multiple (if the strategy supplied initial risk), strategy, signal source (strategy / agent / tier B / manual / MCP), tags, review status.
- Trade detail `/journal/trades/{id}`: provenance chain (signal → decision run / tier-B scores → risk checks → order → fills), costs vs modelled (from M16 TCA), notes/tags/screenshots, correction chain.
- Commands: `journal.note.add` C0, `journal.tag` C0, `tax.export` C0, `tax.report.generate` C1, `tax.residency.add` C1 (+ preview; C3 when it removes a compliance flag, P3-T033), `tax.regime.set` C1 (answer id required), `tax.lot.select` C1 (not in locked FY); all written to `audit.command`.
- Notes/tags/screenshots are WORM rows (`journal.note`, `journal.tag`; screenshots stored as files with hash, see P3-B013).
- WS `journal` topic publishes `journal.event.new` (throttled ≤ 1 Hz for tables per 02 §6 rules); `recon` topic for recon status.
- Paper vs live: `mode` filter, default `live` when any live account exists else `paper`.

## ToDo

- [ ] Implement routers `packages/mt_api/routers/journal.py`, `tax.py`; command handlers in `mt_api/commands/journal.py`, `tax.py`
- [ ] OpenAPI schemas + regenerated TS types (`openapi-typescript`)
- [ ] WS fan-out
- [ ] Contract tests; docs

## Verification

### Tests

- Contract: OpenAPI snapshot; schemathesis run against a fixture DB.
- Unit: each command enforces its C-level server-side (C1 without confirm → 409/problem).
- Integration: `/tax/summary?fy=2026-27` returns both regimes + PAYG with provenance fields.

### Scenarios

- Given a paper fill arrives, when the WS `journal` topic is subscribed, then the client gets the event with `seq` and can re-sync via REST on a gap.
- Given Postgres is down, when queries are called, then the API returns 503 problem+json and the UI goes read-only (02 §9.3).

### Stress / failure injection

- `/journal/events` p95 < 300 ms for a 1-year range with 100k events (paginated, indexed); WS fan-out of 2,000 events/10 s without client lag > 500 ms p95.

## Acceptance criteria

- [ ] All D14/D15 endpoints and commands implemented with C-levels server-side
- [ ] Every tax payload has provenance + not-advice fields
- [ ] OpenAPI + TS types regenerated
- [ ] CI green (lint, types, tests, `pit` check; `tax-golden` once P3-T045 lands)

## Exceptions & edge cases

- FY param formats (`2026-27`) validated; invalid → 422 problem.
- Locked FY → mutating commands return 423 with the unlock path (P3-B006).

## Cardinal rules (do NOT)

- Do NOT render any edit control on journal records; corrections are server-side superseding events.
- Do NOT expose decrypted tax-sensitive fields through any endpoint except the accountant-pack download (with `include_identity`).
- Do NOT commit secrets or paste them into chats/issues; secrets live only in the sops/age file ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order goes through M11.
- Do NOT UPDATE or DELETE `journal.*` (WORM) rows; corrections are new rows referencing the superseded row ([15 §2](../../../docs/15-bots-hitl-and-worm-audit.md#2-worm-records-write-once-read-many)).
- Do NOT expose tax-sensitive fields (TFN, addresses, raw statements) to any LLM prompt, RAG index or the LiteLLM gateway ([07 §8](../../../docs/07-security-notes.md#8-data-protection-backups--audit)).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.

## Doc sync on completion

- `docs/02-v1-architecture.md` §7.1/§7.2: confirm endpoints/commands match; add any new ones (`task.answer`, `journal.manual_event.add`).
- `docs/roadmap/phase-3-journal-and-tax.md`: tick T3.29 once every item mapped to it is done.

## Branch & PR

- Branch: `p3/P3-T039-journal-tax-api`
- PR title: `P3-T039: Journal and tax API queries, commands and WebSocket topic`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P3-T039` run · OpenAPI diff reviewed

## Progress log

- 2026-10-21 00:00 · planner · created
