---
id: P0-T026
kind: task
title: Seed ops.venue_registry from your venue checks
phase: 0
type: OPS
status: backlog
priority: medium
size: XS
severity: ""
owner: agent
claimed_by: ""
depends_on: [P0-T025, P0-T011]
requirements: [R0.06]
roadmap_todos: [T0.11, T0.22]
modules: [ops, M11]
dashboards: []
branch: p0/P0-T026-seed-venue-registry
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

# P0-T026 · Seed ops.venue_registry from your venue checks

## Goal / expected outcome

`infra/seed/venue_registry.yaml` (from P0-T011) is committed, validated and loaded, so `ops.venue_registry_current` lists every checked venue with status, products, leverage and `austrac_checked_at`.

## Context & references

- [Roadmap P0 R0.06](../../../docs/roadmap/phase-0-foundations.md#3-requirements)
- [12 §2 venue registry](../../../docs/12-policy-and-compliance.md#2-venue-access-registry)
- Related: P0-T011 (your data), P0-T025 (table + loader)
- Depends on: P0-T025, P0-T011

## Requirements

- Seed is idempotent: re-running with the same file creates no new versions; a changed row creates one new version.
- Unverified fields carry `(U)` in `reason`; OKX AU derivatives `blocked` (paper only); Bybit/Bitget/MEXC/Gate/KuCoin `read_only`; Hyperliquid `read_only` pending advice; Polymarket `blocked`.
- No secrets in the YAML (venue names, ABNs and public facts only).

## ToDo

- [ ] Review the YAML from P0-T011 against 12 §2; fix schema errors.
- [ ] Run `uv run python -m mt_store.seed.venues infra/seed/venue_registry.yaml`.
- [ ] Add a CI check that the YAML validates.
- [ ] Paste `SELECT venue, status, austrac_checked_at FROM ops.venue_registry_current` output into the PR.

## Verification

### Tests
- CI: YAML validates against the loader schema.
- Integration: seed twice → version count unchanged.

### Scenarios
- Given you re-check a venue next quarter and edit the YAML, when the seed runs, then exactly one new version row is created.

### Stress / failure injection
- n/a: one-off data load.

## Acceptance criteria

- [ ] Every venue from P0-T011 present in the current view with a checked date
- [ ] Idempotent re-run proven
- [ ] Statuses match 12 §2 rules above
- [ ] CI green (ruff, mypy, pytest, gitleaks, `pit` check)

## Exceptions & edge cases

- A venue missing from your checks stays absent (absent = blocked by M11 default-deny in P2).

## Cardinal rules (do NOT)

- Do NOT mark a venue `allowed` without an AUSTRAC/licence check date.
- Do NOT skip, weaken or delete a test to get CI green.

## Doc sync on completion

- `docs/12-policy-and-compliance.md` §2: replace starting classifications with verified ones.
- `docs/roadmap/phase-0-foundations.md`: tick T0.11, T0.22 when every item mapped to it is done.

## Branch & PR

- Branch: `p0/P0-T026-seed-venue-registry`
- PR title: `P0-T026: Seed ops.venue_registry from your venue checks`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P0-T026` run

## Progress log

- 2026-10-21 00:00 · planner · created
