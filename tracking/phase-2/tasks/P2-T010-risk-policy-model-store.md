---
id: P2-T010
kind: task
title: Risk policy model, store and versioning with rollback
phase: 2
type: BUILD
status: backlog
priority: critical
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: []
requirements: [R2.11]
roadmap_todos: [T2.22]
modules: [M11]
dashboards: [D06]
branch: p2/P2-T010-risk-policy-model-store
pr: ""
doc_sync: [docs/03-build-spec.md, docs/02-v1-architecture.md, docs/roadmap/phase-2-strategies-risk-lab.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P2-T010 · Risk policy model, store and versioning with rollback

## Goal / expected outcome

`packages/mt_risk/policy` holds a versioned, typed risk policy covering global, venue/account, strategy, instrument/asset-class, portfolio, sleeve, sizing, defaults, blackouts and dead-man/kill configuration, stored as YAML-compatible documents in `risk.policy` with immutable versions and rollback-as-new-version.

## Context & references

- Roadmap: [R2.11](../../../docs/roadmap/phase-2-strategies-risk-lab.md) · ToDo T2.22
- Spec: [03 M11 policy levels table](../../../docs/03-build-spec.md#m11-risk-manager--mt_risk-built-in-user-inputs-via-uitelegram-later-mcp) · [14 §5 sleeves + defaults](../../../docs/14-strategy-evidence-and-validation.md#5-risk-engine-additions-m11)
- UI: [D06 Policy tab tree](../../../docs/ui/dashboards/D06-risk.md) · Flow: [02 F5](../../../docs/02-v1-architecture.md#8-end-to-end-flows)
- Cross-phase: `mt_core.RiskPolicy` type (P0 T0.21), `risk` schema (P0 R0.03), WORM layer for `risk.change` (P0 R0.07).
- Related: P2-T011 ceilings, P2-T012 limits, P2-T019 change control.

## Requirements

- Pydantic models per level with Decimal values, units (`pct_of_sleeve`, `ccy`, `count`, `seconds`) and per-field **direction metadata** (`tighter: lower|higher|enable|disable`) used by change control.
- Inheritance: instrument → strategy → sleeve → venue → global; effective value resolver returns value + source level (D06 'inherits global: 3%').
- Tables: `risk.policy(version int pk, doc jsonb, doc_hash, created_at, created_by, parent_version)` insert-only; `risk.change` (WORM) rows reference versions; current = max applied version.
- Rollback = a new version whose doc equals an old one, classified by the normal tighten/loosen rules.
- YAML import/export (`mt risk policy export|import`) with schema `mt.risk-policy/v1`.
- In-engine cache: the effective policy is compiled into flat lookup tables on load for O(1) checks (keeps p99 < 1 ms).

## ToDo

- [ ] Models in `packages/mt_risk/policy/model.py`; resolver in `resolve.py`
- [ ] Migrations for `risk.policy`; register `risk.change` with the WORM layer
- [ ] Policy compiler to flat tables (`compiled.py`) + NATS KV `risk_state.policy_version` publish on change
- [ ] CLI import/export
- [ ] Tests
- [ ] Update the docs listed under *Doc sync on completion* and tick the roadmap ToDo box(es) once every task mapped to them is done

## Verification

### Tests
- Unit: inheritance resolution table tests (override vs inherit at each level).
- Property: export → import round-trip yields an identical hash.
- Unit: every field has direction metadata (test enumerates the model).
- DB: UPDATE/DELETE on `risk.policy` and `risk.change` by app roles fail.

### Scenarios
- Given global daily loss 3% and strategy override 2%, when resolving for that strategy, then 2% with source 'strategy'.
- Given version 7 applied, when rolling back to 5, then version 8 is created with doc(5) and a `risk.change` row marks it rollback.

### Stress / failure injection
- Compile a policy with 50 venues × 200 strategies × 1,000 instruments; compile < 200 ms; lookup p99 < 5 µs.

## Acceptance criteria

- [ ] All 03 M11 levels modelled with direction metadata
- [ ] Versions immutable; rollback creates a new version
- [ ] Compiled lookups benchmarked
- [ ] CI green: ruff, mypy, pytest (and the `mt_risk` golden suite, `pit` check, viewport matrix where relevant)

## Exceptions & edge cases

- No policy present at engine start: default-deny (no orders) and critical alert.
- Postgres down: engine keeps the last compiled policy in memory; changes are refused until DB is back.

## Cardinal rules (do NOT)

- Do NOT edit an applied policy version in place.
- Do NOT read limits from anywhere but the compiled policy + ceilings file in the order path.
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order goes through M11, whatever its source.
- Do NOT commit secrets or paste them into chats/issues/logs; secrets live in the sops/age file (07 §2).
- Do NOT skip, weaken or delete a test to get green; risk-manager golden tests are mandatory for merge.
- Do NOT UPDATE or DELETE WORM rows (`audit.*`, `risk.change`, `risk.approval`, `strategy.bot_version`); corrections are new rows with `supersedes_id` (15 §2).

## Doc sync on completion

- `docs/03-build-spec.md` M11: link the policy schema.
- `docs/02-v1-architecture.md` §4: confirm `risk.policy` columns.
- `docs/roadmap/phase-2-strategies-risk-lab.md`: tick T2.22 when all tasks mapped to it are done.

## Branch & PR

- Branch: `p2/P2-T010-risk-policy-model-store`
- PR title: `P2-T010: Risk policy model, store and versioning with rollback`
- PR checklist: tests added and green · docs synced · task file ticked · no secrets (gitleaks) · `./kanban done P2-T010` run

## Progress log

- 2026-10-21 00:00 · planner · created
