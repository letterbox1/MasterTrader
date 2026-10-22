---
id: P0-T069
kind: task
title: Run the WORM integrity drill
phase: 0
type: VERIFY
status: backlog
priority: high
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P0-T038, P0-T052, P0-T061]
requirements: [R0.12, R0.07]
roadmap_todos: [T0.66]
modules: [M17, M11, mt_risk, mt_api]
dashboards: [D16]
tools: [git, uv, python>=3.12, docker, psql]
mcp: []
env: []
services: [postgres, nats, mt-api, minio, prefect-server]
branch: p0/P0-T069-worm-integrity-drill
pr: ""
doc_sync: [docs/15-bots-hitl-and-worm-audit.md, docs/runbooks/README.md, docs/roadmap/phase-0-foundations.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-22
updated: 2026-10-22
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
review_result: ""
---

# P0-T069 · Run the WORM integrity drill

## Goal / expected outcome

An end-to-end drill on a scratch copy of the full stack proves the integrity response (R0.12): a tampered WORM row is detected by `audit.verify`, the `audit.integrity` status switches to the configured action (default `block_new_entries`), new entries are blocked while exits and protective orders still pass the M11 hook point, other loosening is refused, and only a C3 `audit.integrity.ack` (break-glass `mtctl approve` + TOTP + cool-down in P0) clears it, as a new WORM row. The drill follows the WORM incident runbook (P0-T061) literally.

## Context & references

- Roadmap: [R0.12 · T0.66](../../../docs/roadmap/phase-0-foundations.md#3-requirements)
- [16 §2.11 WORM integrity](../../../docs/16-configuration-and-safety-model.md#211-worm-integrity), [16 §3.3](../../../docs/16-configuration-and-safety-model.md#33-records-the-write-path-vs-the-integrity-check)
- [15 §2.2 integrity response](../../../docs/15-bots-hitl-and-worm-audit.md#22-layers), [15 §2.4 tests](../../../docs/15-bots-hitl-and-worm-audit.md#24-tests-part-of-every-phase-that-adds-a-worm-table)
- [02 §9.3 degraded modes](../../../docs/02-v1-architecture.md#93-degraded-modes) (WORM verify mismatch row), [D16 Integrity](../../../docs/ui/dashboards/D16-system.md)
- Decisions: [17 §A](../../../docs/17-decisions-register.md#a-s2-items-all-resolved) P0-B001, [17 §D](../../../docs/17-decisions-register.md#d-other-decisions) P0-B002 (break-glass C3)
- Implementation: P0-T038 (verify, KV status, `integrity_gate`, ack), P0-T035 (C3 engine + `mtctl`), P0-T052 (D16 banner + Acknowledge), P0-T061 (incident runbook)
- P2 re-runs the gate part inline in M11 (R2.58, T2.71)
- Depends on: P0-T038, P0-T052, P0-T061

## Requirements

- Functional (each step's outcome recorded with evidence):
  1. Baseline: hourly incremental and daily full verify `ok`; KV `audit.integrity = ok`; D16 shows no banner.
  2. Tamper: as superuser on the **scratch** DB with triggers disabled, change one payload field of a sealed `audit.command` row.
  3. Detect: run `audit.verify` (incremental, then full) → mismatch at the right table/seq; an `audit.integrity_incident` row (critical); `alert.critical.audit_verify` published; KV `audit.integrity = block_new_entries`; red D16 banner on every route.
  4. Gate: through the `mt_risk.integrity_gate` hook (a test harness standing in for P2's M11) an entry intent and a risk-increasing intent are rejected; a reduce-only exit and a protective stop pass; Kill ON still works.
  5. No loosening: a C3 loosening (e.g. raising an LLM budget) is refused while the incident is open; tightening still applies.
  6. Clear: `audit.integrity.ack` (C3) → `mtctl approve <id>` over SSH + TOTP → the configured cool-down (default 15 min, [16 §2.3](../../../docs/16-configuration-and-safety-model.md#23-decisions-approvals-and-hitl)) → applied: a new `audit.integrity_incident` ack row referencing the incident, the incident row unchanged, KV back to `ok`, banner gone.
  7. Repeat steps 3–4 with the action set to `halt_all` (exits also rejected, Kill still works) and to `alert_only` (alerts fire, nothing blocked); changing the action towards `alert_only` is itself C3.
- Non-functional: the automated version runs in CI with SimClock for the cool-down; the host run uses real time (no shortened cool-down). Evidence in `docs/runbooks/evidence/p0-integrity-drill-<date>.md`.
- Tools & access: listed in the front matter; no secrets beyond your own TOTP for the host run.

## ToDo

- [ ] Write `tests/verify/test_integrity_drill.py` (steps 1–7, SimClock) and wire it into CI (`verify` marker, nightly).
- [ ] Run the drill once on a scratch copy of the production stack following the WORM incident runbook (P0-T061) literally; note any step that needed improvising and fix the runbook.
- [ ] Capture evidence: verify output, incident/ack rows (ids + hashes), KV values, gate decisions, D16 screenshots.
- [ ] File a bug for any deviation.

## Verification

### Tests
- The automated drill (steps 1–7) with assertions on rows, KV, alerts and gate decisions.

### Scenarios
- Given a mismatch at 03:00 while you sleep, then entries stay blocked, exits and stops still work, and nothing loosens until you acknowledge after investigating.
- Given someone tries to clear the status by writing KV directly, then the next verify run re-sets it (incident still open, no ack row) and the attempt shows in the NATS audit/logs.

### Stress / failure injection
- Tamper while Postgres is briefly paused and resumed (rows buffered in JetStream and drained) → verify still detects only the tampered row; buffered rows verify clean.

## Acceptance criteria

- [ ] Steps 1–7 pass in CI (SimClock) and once on the scratch host stack (real cool-down)
- [ ] Entries blocked, exits/protective orders/Kill allowed under `block_new_entries`
- [ ] Only a C3 `audit.integrity.ack` clears it, as a new row; the incident row is never updated
- [ ] Runbook followed literally and corrected where needed; evidence committed
- [ ] CI green (ruff, mypy, pytest, gitleaks, `pit` check)

## Exceptions & edge cases

- The scratch stack must use its own seal bucket prefix (or MinIO) so drill incidents never mix with production anchors.
- If the tamper lands in an unsealed day, the hourly incremental chain check detects it before any seal comparison; the drill covers both a sealed and an unsealed row.

## Cardinal rules (do NOT)

- Do NOT tamper with production data or production anchors; scratch environments only.
- Do NOT shorten the cool-down on the host run or skip TOTP; SimClock only in CI.
- Do NOT clear the status any way other than `audit.integrity.ack`.
- Do NOT UPDATE or DELETE WORM rows, ever (the drill's tamper is a deliberate superuser fault on a scratch DB); corrections are new rows with `supersedes_id` ([15 §2](../../../docs/15-bots-hitl-and-worm-audit.md#2-worm-records-write-once-read-many)).
- Loosening risk, autonomous mode and mandates are C3 (Telegram + TOTP + cool-down; break-glass CLI in P0); protective exits never wait for approval.
- Do NOT skip, weaken or delete a test to get CI green.

## Doc sync on completion

- `docs/15-bots-hitl-and-worm-audit.md` §2.4: link the drill test and evidence.
- `docs/runbooks/README.md`: link the drill evidence from the WORM incident runbook.
- `docs/roadmap/phase-0-foundations.md`: tick T0.66 when every item mapped to it is done.

## Branch & PR

- Branch: `p0/P0-T069-worm-integrity-drill`
- PR title: `P0-T069: Run the WORM integrity drill`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P0-T069` run

## Progress log

- 2026-10-22 02:01 · cloud:vm:be04b6ae61f8 · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (new task for R0.12 / T0.66, decided in 17 §A P0-B001 and 16 §2.11)
