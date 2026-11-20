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
depends_on: [P0-T020, P0-T039]
requirements: [R2.44, R2.47]
roadmap_todos: [T2.41]
modules: [M7, M21]
dashboards: []
tools: [docker, cargo, uv]
mcp: []
env: []
services: [mlflow, supabase-postgres]
branch: p2/P2-T046-mlflow-artifacts-registry-stages
pr: ""
doc_sync: [docs/02-v1-architecture.md, docs/roadmap/phase-2-strategies-risk-lab.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-11-20
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
review_result: ""
---

# P2-T046 · MLflow artefact storage and model registry stages

## Goal / expected outcome

MLflow (running since P0) stores artefacts on the NVMe volume with restic backup, has registry stages/aliases (`candidate`, `staging`, `production`, `archived`) and per-service access so Part B's lab and tier-A pipeline can track runs and promote models.

## Context & references

- Roadmap: [R2.44, R2.47](../../../docs/roadmap/phase-2-strategies-risk-lab.md) · ToDo T2.41
- Architecture: [02 §5.1 stores: MLflow forever, restic](../../../docs/02-v1-architecture.md#51-stores)
- Cross-phase (`depends_on`): mlflow container (P0-T020, T0.41), restic backups (P0-T039, T0.44).
- Consumers: lab (P2-T107), tier A (P2-T125–T128; training via `models.tiera.train`, C1).

## Requirements

- Backend store: the Supabase Postgres (`mlflow` schema), artefact root `/data/mlflow/artifacts` (local volume), included in restic backups.
- Registry aliases: `candidate` → `staging` → `production`, `archived`; promotion to `production` only via `models.promote` command (mt-api, audited) — not via MLflow UI (UI bound to localhost, read-mostly; Tailscale only for optional phone access, 18 §8).
- Service tokens: backtest-worker (`mt-lab-core` and `mt_research` jobs) read/write runs; engine and `mt-models` read-only for `production` models (ONNX artefacts).
- Retention: artefacts forever (02 §5.1).

## ToDo

- [ ] Compose config + volume
- [ ] Registry bootstrap script
- [ ] Backup include + restore smoke
- [ ] Tests
- [ ] Update the docs listed under *Doc sync on completion* and tick the roadmap ToDo box(es) once every task mapped to them is done

## Verification

### Tests
- Commands: `cargo test -p mt-lab-core mlflow` (REST client used by the production harness) and `uv run pytest packages/mt_research -k mlflow` (Python client used by notebooks and training) against the compose stack.
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
- [ ] CI green: compose config check, image digests pinned, smoke tests

## Exceptions & edge cases

- MLflow down: lab runs queue; engine keeps the loaded production model.

## Cardinal rules (do NOT)

- Do NOT expose MLflow outside localhost (or your tailnet when you use one).
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
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (cross-phase deps; consumers named)
- 2026-11-19 00:00 · aligner · re-platformed per docs/18 (workstation wording, `infra/` paths, CI line; MLflow backend on Supabase Postgres; Tailscale optional; services [mlflow, postgres] → [mlflow, supabase-postgres])
- 2026-11-20 00:00 · aligner · Rust-max per 17 §H (MLflow clients are `mt-lab-core` (REST, Rust) and `mt_research` (Python); `packages/mt_lab` → those two; tools [docker, uv] → [docker, cargo, uv])
