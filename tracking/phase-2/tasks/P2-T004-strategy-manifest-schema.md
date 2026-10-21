---
id: P2-T004
kind: task
title: Strategy manifest schema and validator CLI
phase: 2
type: BUILD
status: backlog
priority: critical
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: []
requirements: [R2.04]
roadmap_todos: [T2.20]
modules: [M0]
dashboards: [D03]
branch: p2/P2-T004-strategy-manifest-schema
pr: ""
doc_sync: [docs/03-build-spec.md, docs/ui/dashboards/D03-strategies.md, docs/roadmap/phase-2-strategies-risk-lab.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P2-T004 · Strategy manifest schema and validator CLI

## Goal / expected outcome

A versioned manifest schema (`strategies/<name>/manifest.yaml`) with every M0 + 14 §3 field, exported as JSON Schema for the UI `ParamForm`/Optuna, and a `mt strategy validate <path>` CLI used by CI, the builder and the registry.

## Context & references

- Roadmap: [R2.04](../../../docs/roadmap/phase-2-strategies-risk-lab.md) · ToDo T2.20
- Spec: [03 M0 manifest](../../../docs/03-build-spec.md#m0-strategy-framework--mt_strategy-strategy-agnostic-any-timeframe) · [14 §3 counterparty rule + priorities](../../../docs/14-strategy-evidence-and-validation.md#3-strategy-catalogue-evidence-ranked-templates) · [14 §5 kill criteria](../../../docs/14-strategy-evidence-and-validation.md#5-risk-engine-additions-m11)
- UI: [D03 builder + manifest fields](../../../docs/ui/dashboards/D03-strategies.md)
- Related: P2-T005 never-build, P2-T006 registry, P2-T050 your first manifests; Part B consumes the param schema for Optuna.

## Requirements

- Fields: `name`, `version`, `template`, `description`, `universe` (instruments/venues or dynamic rule), `subscriptions` (data kinds + BarSpecs), `params` (type, range, default, step, `risk_increasing: bool`), `features`, `risk_policy_ref`, `mode` (`backtest|paper|hitl|autonomous`), **`counterparty`** (required, one sentence, ≥ 20 chars), **`sleeve`** (required, must exist in policy), **`kill_criteria`** (required list of measurable rules), **`benchmark`** (required, asset-class passive alternative), `priority` (P1/P2/P3 from template), `evidence` (link/text), `regime_filter`, `exit_plan` defaults.
- Validation errors are structured (`field`, `code`, `message`) for the D03 Review step.
- Schema version field `schema: mt.manifest/v1`; unknown keys rejected.
- JSON Schema export at `/strategies/templates` consumers (`packages/mt_strategy/schema/manifest.v1.json`).

## ToDo

- [ ] Implement `packages/mt_strategy/manifest.py` (pydantic v2 models, Decimal for money/limits)
- [ ] Generate JSON Schema to `packages/mt_strategy/schema/manifest.v1.json` in a build step; test it is up to date
- [ ] CLI `mt strategy validate` (exit code ≠ 0 on error; `--json` output)
- [ ] Pre-commit hook: validate every `strategies/**/manifest.yaml`
- [ ] Fixtures: valid and invalid manifests (missing counterparty, unknown sleeve, empty kill criteria, bad BarSpec)
- [ ] Update the docs listed under *Doc sync on completion* and tick the roadmap ToDo box(es) once every task mapped to them is done

## Verification

### Tests
- Unit: each required field missing → specific error code.
- Unit: param ranges (min ≤ default ≤ max), types, enums.
- Property (hypothesis): any generated valid manifest round-trips YAML → model → YAML unchanged.
- Integration: pre-commit hook rejects an invalid manifest.

### Scenarios
- Given a manifest without `counterparty`, when validated, then it fails with `counterparty.required` and the D03 Review step shows that message.
- Given `mode: autonomous` in a new manifest, when validated, then it passes schema but the registry stores it as `draft` (mode changes go through lifecycle P2-T007).

### Stress / failure injection
- n/a: pure validation; performance irrelevant (< 10 ms per manifest asserted in a unit test).

## Acceptance criteria

- [ ] Schema covers every field listed in 03 M0 and 14 §3/§5
- [ ] JSON Schema export versioned and CI-checked
- [ ] CLI + pre-commit hook in place
- [ ] CI green: ruff, mypy, pytest (and the `mt_risk` golden suite, `pit` check, viewport matrix where relevant)

## Exceptions & edge cases

- Legacy `approve`/`auto` mode values are accepted as aliases of `hitl`/`autonomous` with a deprecation warning (see P2-B053).
- Sleeve unknown because policy not yet written (P2-T048): validation error, not silent default.

## Cardinal rules (do NOT)

- Do NOT allow a manifest to set looser risk than its policy (risk overrides are tighter-only).
- Do NOT accept manifests missing counterparty, kill criteria, sleeve or benchmark.
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order goes through M11, whatever its source.
- Do NOT commit secrets or paste them into chats/issues/logs; secrets live in the sops/age file (07 §2).
- Do NOT skip, weaken or delete a test to get green; risk-manager golden tests are mandatory for merge.

## Doc sync on completion

- `docs/03-build-spec.md` M0: link the schema file and field table.
- `docs/ui/dashboards/D03-strategies.md`: Review step lists the validation codes.
- `docs/roadmap/phase-2-strategies-risk-lab.md`: tick T2.20 when all tasks mapped to it are done.

## Branch & PR

- Branch: `p2/P2-T004-strategy-manifest-schema`
- PR title: `P2-T004: Strategy manifest schema and validator CLI`
- PR checklist: tests added and green · docs synced · task file ticked · no secrets (gitleaks) · `./kanban done P2-T004` run

## Progress log

- 2026-10-21 00:00 · planner · created
