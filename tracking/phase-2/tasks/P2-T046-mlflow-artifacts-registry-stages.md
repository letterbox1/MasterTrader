---
id: P2-T046
kind: task
title: MLflow artefact storage and model registry stages
phase: 2
type: OPS
status: backlog
priority: medium
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: []
requirements: [R2.44, R2.47]
roadmap_todos: [T2.41]
modules: [M7, M21]
dashboards: []
branch: p2/P2-T046-mlflow-artifacts-registry-stages
pr: ""
doc_sync: [docs/02-v1-architecture.md, docs/roadmap/phase-2-strategies-risk-lab.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P2-T046 · MLflow artefact storage and model registry stages

## Goal / expected outcome

MLflow (running since P0) stores artefacts on the NVMe volume with restic backup, has registry stages/aliases (`candidate`, `staging`, `production`, `archived`) and per-service access so Part B's lab and tier-A pipeline can track runs and promote models.

## Context & references

- Roadmap: [R2.44, R2.47](../../../docs/roadmap/phase-2-strategies-risk-lab.md) · ToDo T2.41
- Architecture: [02 §5.1 stores: MLflow forever, restic](../../../docs/02-v1-architecture.md#51-stores)
- Cross-phase: mlflow container (P0 T0.41), restic (P0 T0.44).
- Consumer: Part B (lab, tier A).

## Requirements

- Backend store Postgres (`mlflow` DB/schema), artefact root `/data/mlflow/artifacts` (local volume), included in restic backups.
- Registry aliases: `candidate` → `staging` → `production`, `archived`; promotion to `production` only via `models.promote` command (mt_api, audited) — not via MLflow UI (UI bound to localhost/Tailscale, read-mostly).
- Service tokens: backtest-worker read/write runs; engine read-only for `production` models.
- Retention: artefacts forever (02 §5.1).

## ToDo

- [ ] Compose config + volume
- [ ] Registry bootstrap script
- [ ] Backup include + restore smoke
- [ ] Tests
- [ ] Update the docs listed under *Doc sync on completion* and tick the roadmap ToDo box(es) once every task mapped to them is done

## Verification

### Tests
- Smoke: log a run with params/metrics/artefact; register model; set alias; engine token can read but not write.
- Restore test: artefact restored from restic matches hash.

### Scenarios
- Given a tier-A model at `staging`, when promoted via `models.promote`, then alias moves to `production` and `audit.command` has the row.

### Stress / failure injection
- n/a: low volume service.

## Acceptance criteria

- [ ] Artefacts persisted + backed up
- [ ] Stages/aliases configured
- [ ] Promotion only via audited command
- [ ] CI green: ruff, mypy, pytest (and the `mt_risk` golden suite, `pit` check, viewport matrix where relevant)

## Exceptions & edge cases

- MLflow down: lab runs queue; engine keeps the loaded production model.

## Cardinal rules (do NOT)

- Do NOT expose MLflow outside localhost/Tailscale.
- Do NOT commit secrets or paste them into chats/issues/logs; secrets live in the sops/age file (07 §2).
- Do NOT skip, weaken or delete a test to get green; risk-manager golden tests are mandatory for merge.
- Pin images by digest; no telemetry or referral/broker IDs in vendored code.

## Doc sync on completion

- `docs/02-v1-architecture.md` §5.1: registry aliases.
- `docs/roadmap/phase-2-strategies-risk-lab.md`: tick T2.41 when all tasks mapped to it are done.

## Branch & PR

- Branch: `p2/P2-T046-mlflow-artifacts-registry-stages`
- PR title: `P2-T046: MLflow artefact storage and model registry stages`
- PR checklist: tests added and green · docs synced · task file ticked · no secrets (gitleaks) · `./kanban done P2-T046` run

## Progress log

- 2026-10-21 00:00 · planner · created
