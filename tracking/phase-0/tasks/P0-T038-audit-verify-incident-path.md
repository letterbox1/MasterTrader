---
id: P0-T038
kind: task
title: Implement audit.verify, the daily verify flow and the incident path
phase: 0
type: BUILD
status: backlog
priority: critical
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P0-T037, P0-T034, P0-T023]
requirements: [R0.07]
roadmap_todos: [T0.23]
modules: [M17, M11]
dashboards: []
branch: p0/P0-T038-audit-verify-incident-path
pr: ""
doc_sync: [docs/15-bots-hitl-and-worm-audit.md, docs/runbooks/README.md, docs/roadmap/phase-0-foundations.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P0-T038 · Implement audit.verify, the daily verify flow and the incident path

## Goal / expected outcome

`audit.verify` (command, C1) and a daily Prefect flow recompute every WORM chain and compare each day's Merkle root against the **externally anchored** seal (fetched from the Object-Locked store, not from `audit.seal`). Any mismatch is a critical incident: `audit.incident` row, alerts on all available channels, a red D16 banner and — configurable, default **on** — a trading halt flag that P2's risk manager honours.

## Context & references

- [Roadmap P0 R0.07](../../../docs/roadmap/phase-0-foundations.md#3-requirements)
- [15 §2.2 layers](../../../docs/15-bots-hitl-and-worm-audit.md#22-layers) (Verification)
- [15 §2.3 threat coverage](../../../docs/15-bots-hitl-and-worm-audit.md#23-what-this-protects-against)
- [07 §8 backups & audit](../../../docs/07-security-notes.md#8-data-protection-backups--audit)
- [07 §9 monitoring & incident response](../../../docs/07-security-notes.md#9-monitoring--incident-response)
- [D16 System](../../../docs/ui/dashboards/D16-system.md) (acceptance 3: chain failure banner)
- The halt mechanism (kill vs new-entry halt) is unspecified across docs — P0-B001; this task implements a distinct KV flag.
- Depends on: P0-T037, P0-T034, P0-T023

## Requirements

- Verify steps per table: (1) recompute chain with `recompute_chain` (P0-T030): contiguous `seq`, `prev_hash` links, `row_hash` recomputation; (2) for each sealed day, rebuild the Merkle root and compare with the anchor object's root (download + verify object hash); (3) compare `audit.seal` row with the anchor (DB tamper of the seal itself).
- Result: `audit.verify_run` row (WORM) with per-table status, first bad `seq`, duration.
- On mismatch: `audit.incident` (severity critical, kind `audit_chain_mismatch`), NATS `alert.critical.audit_verify`, Alertmanager route (Telegram now; email/ntfy when P1 adds them), and if `halt_on_verify_failure` (default true): set NATS KV `risk_state` key `trading_halt = {on: true, reason: 'audit_verify_mismatch', incident_id}`; mt-api exposes it in `/risk/state` and the WS `kill`/`system` topics.
- Clearing the halt is **C3** (`risk.halt.clear` — new command registered here; 02 §7.2 catalogue update via P0-B001).
- Schedule: daily 01:00 UTC after seals; also on demand from D16 ('verify now'); full verify of 10 M rows < 10 min.
- Incremental mode: verifies from the last good checkpoint per chain (stored in `audit.verify_run`), full mode weekly.

## ToDo

- [ ] Implement verifier library + Prefect flow + `audit.verify` handler.
- [ ] Implement incident creation, alert publishing and the `trading_halt` KV write.
- [ ] Register `risk.halt.clear` (C3) and expose halt in `/risk/state` + WS.
- [ ] Add a Prometheus metric `mt_audit_verify_status{table}` (1 ok / 0 fail) and last-success timestamp for Grafana alerts.
- [ ] Write the incident runbook stub (filled in P0-T061).
- [ ] Tests below; adversarial suite in P0-T055.

## Verification

### Tests
- Integration: clean DB → all ok; tampered row (superuser, triggers disabled) → mismatch at the right seq; tampered `audit.seal` row → mismatch vs anchor; deleted anchor (simulated in MinIO without lock) → `anchor_missing` incident.
- Integration: mismatch sets `trading_halt` and an alert is emitted; `risk.halt.clear` requires C3.

### Scenarios
- Given someone with OS root rewrites a day's rows and recomputes the DB chain consistently, when verify compares with the external seal, then it detects the mismatch (15 §2.3 'detected').
- Given `halt_on_verify_failure=false`, then the incident and alerts still fire but no halt flag is set.

### Stress / failure injection
- Full verify of 10 M fixture rows across 6 tables < 10 min, memory < 1 GiB (streaming).

## Acceptance criteria

- [ ] `audit.verify` command and daily flow implemented
- [ ] External-seal comparison (not DB-only) proven
- [ ] Mismatch → incident + alert + halt flag (default on) + D16 banner data
- [ ] Halt clear is C3
- [ ] CI green (ruff, mypy, pytest, gitleaks, `pit` check)

## Exceptions & edge cases

- Anchor store unreachable: verify reports `anchor_unavailable` (warning, not mismatch) and retries; three consecutive days unavailable → critical.
- Late rows flagged by the seal are not mismatches.

## Cardinal rules (do NOT)

- Do NOT 'fix' a mismatch by editing rows; investigate per runbook and append corrections.
- Do NOT compare only against `audit.seal` in the DB.
- Do NOT UPDATE or DELETE WORM rows, ever; corrections are new rows with `supersedes_id` ([15 §2](../../../docs/15-bots-hitl-and-worm-audit.md#2-worm-records-write-once-read-many)).
- Loosening risk, autonomous mode and mandates are C3 (Telegram + TOTP + cool-down); Kill ON and protective exits never wait for approval.
- Do NOT bypass `mt_api`, the risk manager (M11) or `mt_store.pit(as_of)`; every order goes through M11.
- Do NOT skip, weaken or delete a test to get CI green.

## Doc sync on completion

- `docs/15-bots-hitl-and-worm-audit.md` §2.2: document the halt flag and `risk.halt.clear`; `docs/runbooks/README.md`: index the WORM incident runbook.
- `docs/roadmap/phase-0-foundations.md`: tick T0.23 when every item mapped to it is done.

## Branch & PR

- Branch: `p0/P0-T038-audit-verify-incident-path`
- PR title: `P0-T038: Implement audit.verify, the daily verify flow and the incident path`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P0-T038` run

## Progress log

- 2026-10-21 00:00 · planner · created
