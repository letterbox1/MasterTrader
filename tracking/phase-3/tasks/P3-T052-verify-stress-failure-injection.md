---
id: P3-T052
kind: task
title: Stress and failure injection for ingestion and reconciliation
phase: 3
type: VERIFY
status: backlog
priority: high
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P3-T013, P3-T014, P3-T015, P3-T016, P3-T011, P3-T034]
requirements: [R3.01, R3.02, R3.11]
roadmap_todos: [T3.20, T3.28]
modules: [M18]
dashboards: []
tools: [git, uv, docker]
mcp: []
env: []
services: [postgres, nats, journal, prefect-server, grafana]
branch: p3/P3-T052-verify-stress-failure-injection
pr: ""
doc_sync: [docs/roadmap/phase-3-journal-and-tax.md]
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

# P3-T052 · Stress and failure injection for ingestion and reconciliation

## Goal / expected outcome

The journal survives load and the 02 §9.3 degraded modes without data loss, duplicates or silent errors: fill bursts, Postgres outage (NATS buffering), NATS restart, journal crash mid-batch, venue API outage, FX/price source gaps, broker format drift and clock skew.

## Context & references

- Roadmap: [R3.01, R3.02, R3.11](../../../docs/roadmap/phase-3-journal-and-tax.md) · degraded modes [02 §9.3](../../../docs/02-v1-architecture.md#93-degraded-modes) · SLO-style target D14 ≤ 5 s
- Buffer bound: [16 §3.3](../../../docs/16-configuration-and-safety-model.md#33-records-the-write-path-vs-the-integrity-check) (default 1 GB or 24 h; new entries stop above 80%), built in P3-T057; the bound-specific drill is P3-T060

## Requirements

- Load: 2,000 fills in 10 s + 50k ledger backfill concurrently → no loss/dupes; fill p95 ≤ 5 s once the burst drains (≤ 2 min drain).
- Postgres down 15 min (well inside the bound) → consumer stops acking, writes buffer in `WORM_BUFFER`, alert fires, full catch-up afterwards with zero loss; journal never writes partial batches. (The 80% stop and exits-continue behaviour is drilled in P3-T060.)
- NATS restart / journal kill -9 mid-batch × 10 → no duplicates (idempotency), no gaps (cursor).
- Venue API down during ledger/recon → `skipped_venue_unavailable`, retries, no false `ok`.
- RBA F11 missing 6 business days → `pending_fx` + alert; crypto bars missing → next venue then `pending_price`.
- Statement format drift (renamed column, new XML attribute) → quarantine + alert, no partial import.
- Clock skew +10 min on a source → `clock_suspect` flags; taxpayer-local date unaffected by host skew.
- WORM: tamper attempt during load is rejected.

## ToDo

- [ ] Write chaos scripts in `tests/chaos/journal/` (toxiproxy for DB/NATS latency + outages, docker kill)
- [ ] Run each injection; capture Grafana screenshots + metrics
- [ ] File bugs for any failure; record results

## Verification

### Tests

- Each injection is an automated test with pass/fail assertions on counts, hashes and alerts.

### Scenarios

- Given Postgres is down for 15 min during active paper trading, when it returns, then every fill from the outage is journalled exactly once and recon is clean.

### Stress / failure injection

- As listed in Requirements (this item is the stress/failure-injection item for the phase).

## Acceptance criteria

- [ ] All injections pass with zero loss/duplicates
- [ ] Alerts observed for each degraded mode
- [ ] Results documented

## Exceptions & edge cases

- If the buffer bound is reached in the outage test, new entries stop and the test must report it loudly — records are never silently dropped (16 §3.3).

## Cardinal rules (do NOT)

- Do NOT run chaos tests against production data; use a staging compose project.
- Do NOT commit secrets or paste them into chats/issues; secrets live only in the sops/age file ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Do NOT UPDATE or DELETE `journal.*` (WORM) rows; corrections are new rows referencing the superseded row ([15 §2](../../../docs/15-bots-hitl-and-worm-audit.md#2-worm-records-write-once-read-many)).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.

## Doc sync on completion

- `docs/roadmap/phase-3-journal-and-tax.md`: tick T3.20, T3.28 once every item mapped to it is done.

## Branch & PR

- Branch: `p3/P3-T052-verify-stress-failure-injection`
- PR title: `P3-T052: Stress and failure injection for ingestion and reconciliation`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P3-T052` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (Postgres-down case uses the 16 §3.3 bound (P3-T057/P3-T060; P3-B015 closed); tools/services filled)
