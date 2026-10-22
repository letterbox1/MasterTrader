---
id: P1-T007
kind: task
title: Tag provenance on every ingested row at write time
phase: 1
type: BUILD
status: backlog
priority: critical
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P1-T005, P0-T024, P0-T025]
requirements: [R1.09]
roadmap_todos: [T1.26]
modules: [M1]
dashboards: [D07]
tools: [git, uv, docker]
mcp: []
env: []
services: [postgres]
branch: p1/P1-T007-provenance-tagging-at-write
pr: ""
doc_sync: [docs/roadmap/phase-1-data-and-monitoring.md, docs/12-policy-and-compliance.md, docs/03-build-spec.md]
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

# P1-T007 · Tag provenance on every ingested row at write time

## Goal / expected outcome

All writers in `mt_store` (Timescale tables and Parquet files) stamp `source`, `licence`, `train_ok`, `model_input_ok`, `display_ok`, `retention_days` and `commercial_ok` from the source registry, and untagged rows are rejected.

## Context & references

- Roadmap: requirements [R1.09](../../../docs/roadmap/phase-1-data-and-monitoring.md#3-requirements) · ToDo [T1.26](../../../docs/roadmap/phase-1-data-and-monitoring.md#4-todo-sets)
- Policy: [12 §5](../../../docs/12-policy-and-compliance.md#5-data-provenance-tagging-one-mechanism-for-all-data-terms) (one mechanism for all data terms) · [03 §1](../../../docs/03-build-spec.md#1-ground-rules) (data provenance) · [SPEC non-negotiables](../../../SPEC.md#non-negotiable-requirements) NN10
- Cross-phase prerequisites (depends_on): P0-T024 (schemas, roles, Alembic), P0-T025 (the canonical provenance columns `source`, `licence`, `train_ok`, `model_input_ok`, `display_ok`, `retention_days`, `commercial_ok`, [17 §B](../../../docs/17-decisions-register.md#b-cross-doc-conflicts-one-canonical-answer) P0-B010)
- Depends on (this phase): P1-T005

## Requirements

- `mt_store.provenance.Tagged` writer wrapper: every batch insert gets the source's defaults from `config/sources.yaml`; per-row overrides only to be stricter (e.g. a row can set `train_ok=false`, never flip false → true)
- DB: provenance columns `NOT NULL` plus a CHECK that `retention_days >= 0 OR retention_days IS NULL` (NULL = keep forever); writers fail closed
- Parquet: provenance stored as file-level key-value metadata and as columns on mixed-source files; the recorder (P1-T012) uses it
- Defaults per 12 §5: exchange public data `train_ok=true, model_input_ok=true, commercial_ok=false` unless 06 says otherwise; CoinGecko `retention_days=1`; yfinance/Twelve Data `licence=personal`
- A read helper `mt_store.provenance.filter(rows, purpose="train"|"model_input"|"display")` for P2/P4/P6 consumers

## ToDo

- [ ] Implement the writer wrapper and plug it into the bar, macro, filing and instrument writers
- [ ] Add the DB constraints migration (only if P0 left them nullable) and a Parquet metadata helper
- [ ] Implement the purpose filter and expose it from `mt_store`
- [ ] Write the tests listed under Verification
- [ ] Update the docs listed under Doc sync and tick the roadmap ToDo box(es)

## Verification

### Tests

- Unit: defaults applied; stricter override allowed; looser override rejected; missing source → error
- Integration: insert without provenance via raw SQL as the app role fails (NOT NULL); Parquet file metadata round-trips
- Property: for random rows and overrides, `train_ok` after tagging ≤ source default

### Scenarios

- Given a connector forgets to set its source, when it writes bars, then the write fails and `alert.warning.untagged_rows` fires with the connector name
- Given a row with `model_input_ok=false`, when a consumer asks for `purpose="model_input"`, then the row is excluded

### Stress / failure injection

- Load: tagging adds < 5% overhead to a 100k-row bar insert (benchmark recorded in the PR)

## Acceptance criteria

- [ ] No ingest table accepts an untagged row (tested per table)
- [ ] Every source in the registry has complete provenance defaults
- [ ] CI green (ruff, mypy, pytest, `pit` bypass check, gitleaks)

## Exceptions & edge cases

- Rows derived from several sources (e.g. a cross-source mid) take the strictest flags of their inputs
- Changing a source's licence later does not rewrite history; a re-tag job is a separate, logged operation

## Cardinal rules (do NOT)

- Do NOT loosen a source's flags without a doc change in 06/12 in the same PR
- Do NOT put Telegram text into any model input, RAG index or training set ([12 §4–5](../../../docs/12-policy-and-compliance.md#4-per-platform-data--automation-rules)); the bot only sends alerts.
- Do NOT skip, weaken or delete a test (or widen a tolerance) to get CI green.
- Do NOT add paid data or APIs, exceed a free tier, or scrape against a site's terms; no self-bots or user tokens ([03 §1](../../../docs/03-build-spec.md#1-ground-rules)).
- Do NOT bypass `mt_api`, the risk manager (M11) or `mt_store.pit(as_of)`; research and backtest reads go through `pit` only.

## Doc sync on completion

- `docs/roadmap/phase-1-data-and-monitoring.md`: tick T1.26 once every task traced to it in PHASE.md is done; note P1-T007 next to it.
- `docs/12-policy-and-compliance.md` §5: link the writer and the purpose filter as the enforcement point
- `docs/03-build-spec.md` §1: note "untagged rows are rejected at write time"

## Branch & PR

- Branch: `p1/P1-T007-provenance-tagging-at-write`
- PR title: `P1-T007: Tag provenance on every ingested row at write time`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P1-T007` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (P0 deps explicit; canonical provenance columns cited)
