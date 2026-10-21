---
id: P0-T025
kind: task
title: Add provenance columns and the ops.venue_registry table
phase: 0
type: BUILD
status: backlog
priority: high
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P0-T024]
requirements: [R0.05, R0.06]
roadmap_todos: [T0.22]
modules: [mt_store, M11]
dashboards: []
branch: p0/P0-T025-provenance-columns-venue-registry
pr: ""
doc_sync: [docs/12-policy-and-compliance.md, docs/roadmap/phase-0-foundations.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P0-T025 · Add provenance columns and the ops.venue_registry table

## Goal / expected outcome

Every ingest table created from now on carries the provenance columns `source`, `licence`, `train_ok`, `model_input_ok`, `display_ok`, `retention_days`, `commercial_ok` via one helper, enforced by the migration lint; `ops.venue_registry` exists with the 12 §2 fields, history, and a YAML seed loader.

## Context & references

- [Roadmap P0 R0.05, R0.06](../../../docs/roadmap/phase-0-foundations.md#3-requirements)
- [12 §5 provenance](../../../docs/12-policy-and-compliance.md#5-data-provenance-tagging-one-mechanism-for-all-data-terms)
- [12 §2 venue registry](../../../docs/12-policy-and-compliance.md#2-venue-access-registry)
- [03 §1 ground rules](../../../docs/03-build-spec.md#1-ground-rules) (provenance row)
- [SPEC non-negotiables](../../../SPEC.md#non-negotiable-requirements) (NN10, NN11)
- Column-set mismatch (03 §1 omits `display_ok`; 12 §5 calls them `use_flags`) is P0-B010; this task follows R0.05 (seven separate columns).
- Depends on: P0-T024

## Requirements

- `mt_store.migrate.provenance_columns()` adds: `source text NOT NULL`, `licence text NOT NULL` (`personal|commercial_ok|unknown`), `train_ok bool NOT NULL DEFAULT false`, `model_input_ok bool NOT NULL DEFAULT false`, `display_ok bool NOT NULL DEFAULT true`, `retention_days int NULL` (NULL = forever), `commercial_ok bool NOT NULL DEFAULT false`. Defaults are **deny** for model/training use.
- `ops.data_source` table: per-source defaults (`source` PK, licence, cost `free|paid`, the five flags, `retention_days`, attribution text). Insert trigger on provenance tables fills missing flags from `ops.data_source`; a `cost = 'paid'` source cannot be `enabled` (CHECK).
- Seed `ops.data_source` with the known restrictive defaults: `telegram` (train_ok=false, model_input_ok=false), `birdeye` (disabled), `etherscan` (model_input_ok=false, train_ok=false), `coingecko` (retention_days=1).
- `ops.venue_registry`: `venue`, `entity`, `abn`, `licence_ids`, `austrac_status`, `austrac_checked_at`, `products` (jsonb: spot/margin/perps/cfd → allowed + max_leverage), `key_model` (jsonb), `stp_param`, `stp_mode`, `rate_limits` (jsonb), `health` (jsonb), `concentration_cap_pct` (default 25), `status` (`allowed|read_only|blocked`), `reason`, `residency` (default `AU`), `valid_from`, `valid_to`; current view `ops.venue_registry_current`.
- Changes create a new version row (no in-place UPDATE of history); `venue.registry.update` command wiring is P2 (tighten C1 / allow C3).
- CHECK: crypto-derivative `max_leverage ≤ 2` for residency AU (12 §1).

## ToDo

- [ ] Implement `provenance_columns()` and extend `mt_store.lint` to require them on tables tagged `ingest`.
- [ ] Migration: `ops.data_source` + seed rows + fill trigger.
- [ ] Migration: `ops.venue_registry` + current view + CHECKs.
- [ ] Write `infra/seed/venue_registry.example.yaml` (template for P0-T011) and `mt_store.seed.venues` loader with a JSON-schema check.
- [ ] Tests below.

## Verification

### Tests
- Schema test: a fixture ingest table without provenance fails the lint.
- Trigger test: inserting a `telegram` row without flags yields `model_input_ok=false, train_ok=false`.
- CHECK test: AU crypto perps `max_leverage = 3` rejected.
- Loader test: invalid YAML (unknown status) rejected with a clear message.

### Scenarios
- Given a new source is added without an `ops.data_source` row, when a row is inserted, then the insert fails (FK) rather than defaulting to permissive flags.
- Given a venue status changes from `allowed` to `blocked`, then a new version row exists and the current view shows `blocked`.

### Stress / failure injection
- n/a: schema; trigger cost is measured in P1 ingest benchmarks.

## Acceptance criteria

- [ ] Provenance helper + lint enforced; seven columns with deny defaults
- [ ] `ops.data_source` seeded with Telegram/Birdeye/Etherscan/CoinGecko restrictions
- [ ] `ops.venue_registry` with history, current view, 2× CHECK
- [ ] Seed loader + example YAML ready for P0-T026
- [ ] CI green (ruff, mypy, pytest, gitleaks, `pit` check)

## Exceptions & edge cases

- Rows ingested before P1 don't exist; P1 populates flags (R1.09). Retention jobs are P1.

## Cardinal rules (do NOT)

- Do NOT default `train_ok` or `model_input_ok` to true.
- Do NOT let any Telegram row be model input (12 §4–5).
- Do NOT put Telegram text into any model, RAG index or training set ([12 §4–5](../../../docs/12-policy-and-compliance.md#4-per-platform-data--automation-rules)).
- Do NOT add paid data/APIs, ToS-breaking scraping, self-bots or user tokens; free tiers only ([03 §1](../../../docs/03-build-spec.md#1-ground-rules)).
- Do NOT bypass `mt_api`, the risk manager (M11) or `mt_store.pit(as_of)`; every order goes through M11.
- Do NOT skip, weaken or delete a test to get CI green.

## Doc sync on completion

- `docs/12-policy-and-compliance.md` §5: name the exact columns and the `ops.data_source` defaults table.
- `docs/roadmap/phase-0-foundations.md`: tick T0.22 when every item mapped to it is done.

## Branch & PR

- Branch: `p0/P0-T025-provenance-columns-venue-registry`
- PR title: `P0-T025: Add provenance columns and the ops.venue_registry table`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P0-T025` run

## Progress log

- 2026-10-21 00:00 · planner · created
