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
depends_on: [P0-T037, P0-T035]
requirements: [R0.07, R0.12]
roadmap_todos: [T0.23, T0.27]
modules: [M17, M11, mt_risk]
dashboards: []
tools: [git, uv, python>=3.12, docker]
mcp: []
env: []
services: [postgres, nats, prefect-server, minio]
branch: p0/P0-T038-audit-verify-incident-path
pr: ""
doc_sync: [docs/15-bots-hitl-and-worm-audit.md, docs/runbooks/README.md, docs/roadmap/phase-0-foundations.md]
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

# P0-T038 · Implement audit.verify, the daily verify flow and the incident path

## Goal / expected outcome

`audit.verify` (command, C1) and a daily Prefect flow recompute every WORM chain and compare each day's Merkle root against the **externally anchored** seal (fetched from the Object-Locked store, not from `audit.seal`). Any mismatch is a critical incident and triggers the **integrity response** (R0.12, [16 §2.11](../../../docs/16-configuration-and-safety-model.md#211-worm-integrity)): an `audit.integrity_incident` row, the NATS KV status `audit.integrity` set to the configured action (default `block_new_entries`; options `alert_only` / `halt_all`), alerts on every available channel and a red D16 banner. M11 reads the status before every trade through the `mt_risk.integrity_gate` hook point built here; it clears only with `audit.integrity.ack` (C3), itself a new WORM row.

## Context & references

- [Roadmap P0 R0.07](../../../docs/roadmap/phase-0-foundations.md#3-requirements)
- [15 §2.2 layers](../../../docs/15-bots-hitl-and-worm-audit.md#22-layers) (Verification)
- [15 §2.3 threat coverage](../../../docs/15-bots-hitl-and-worm-audit.md#23-what-this-protects-against)
- [07 §8 backups & audit](../../../docs/07-security-notes.md#8-data-protection-backups--audit)
- [07 §9 monitoring & incident response](../../../docs/07-security-notes.md#9-monitoring--incident-response)
- [D16 System](../../../docs/ui/dashboards/D16-system.md) (acceptance 3: chain failure banner)
- Decided in [17 §A](../../../docs/17-decisions-register.md#a-s2-items-all-resolved) (P0-B001, closed) and [16 §2.11](../../../docs/16-configuration-and-safety-model.md#211-worm-integrity), [16 §3.3](../../../docs/16-configuration-and-safety-model.md#33-records-the-write-path-vs-the-integrity-check): KV `audit.integrity`, default `block_new_entries`, cleared by `audit.integrity.ack` (C3). It's separate from the kill switch: it never cancels or flattens by itself. P2 calls the hook inline on every order (R2.58, T2.39).
- Depends on: P0-T037 (seals), P0-T035 (C3 engine for the ack)

## Requirements

- Verify steps per table: (1) recompute chain with `recompute_chain` (P0-T030): contiguous `seq`, `prev_hash` links, `row_hash` recomputation; (2) for each sealed day, rebuild the Merkle root and compare with the anchor object's root (download + verify object hash); (3) compare `audit.seal` row with the anchor (DB tamper of the seal itself).
- Result: `audit.verify_run` row (WORM) with mode (`incremental|full`), per-table status, first bad `seq`, duration.
- On mismatch: `audit.integrity_incident` row (severity critical, kind `chain_mismatch` / `seal_mismatch` / `anchor_missing`), NATS `alert.critical.audit_verify`, Alertmanager route (Telegram now; email/ntfy when P1 adds them), and KV `audit.integrity = {status: <action>, incident_id, since}` where `<action>` is the setting `audit_integrity_action` (default `block_new_entries`). mt-api exposes it at `/audit/integrity` and on the WS `system` topic (banner).
- **Hook point** `mt_risk.integrity_gate(intent, status) -> Allow | Reject(reason)`: `ok` / `alert_only` → allow; `block_new_entries` → reject entries and risk-increasing orders, allow exits and protective orders (reduce-only, stops); `halt_all` → reject everything except Kill. A pure function + KV reader with a golden test table; P2's M11 calls it inline.
- The action is a setting: tightening (towards `halt_all`) is immediate; loosening (towards `alert_only`) is C3. While an incident is open, no other risk loosening is accepted (C3 changes other than the ack are refused).
- Clearing: `audit.integrity.ack` (C3; via the break-glass `mtctl approve` + TOTP until Telegram C3, P0-T035) writes a new `audit.integrity_incident` row (kind `ack`, referencing the incident; nothing is updated in place) and resets the KV status to `ok`.
- Schedule (defaults, [16 §2.11](../../../docs/16-configuration-and-safety-model.md#211-worm-integrity), configurable): an **hourly incremental** chain check from the last good checkpoint per chain (stored in `audit.verify_run`), plus the **daily full verify** against the external seals (01:00 UTC, after the seal); also on demand from D16 ('verify now'); full verify of 10 M rows < 10 min.

## ToDo

- [ ] Implement verifier library + Prefect flow + `audit.verify` handler.
- [ ] Implement incident creation, alert publishing and the `audit.integrity` KV write per the configured action.
- [ ] Implement `mt_risk.integrity_gate` (hook point) with golden tests.
- [ ] Implement the `audit.integrity.ack` handler (C3; appends an ack row, resets KV) and expose the status at `/audit/integrity` + WS `system`; refuse other loosening while an incident is open.
- [ ] Add a Prometheus metric `mt_audit_verify_status{table}` (1 ok / 0 fail) and last-success timestamp for Grafana alerts.
- [ ] Write the incident runbook stub (filled in P0-T061).
- [ ] Tests below; adversarial suite in P0-T055.

## Verification

### Tests
- Integration: clean DB → all ok; tampered row (superuser, triggers disabled) → mismatch at the right seq; tampered `audit.seal` row → mismatch vs anchor; deleted anchor (simulated in MinIO without lock) → `anchor_missing` incident.
- Integration: mismatch sets `audit.integrity` = `block_new_entries` and emits an alert; `audit.integrity.ack` requires C3 and appends an ack row (the incident row is unchanged).
- Golden: `integrity_gate` over {`ok`, `alert_only`, `block_new_entries`, `halt_all`} × {entry, increase, reduce/exit, protective stop, Kill}.

### Scenarios
- Given someone with OS root rewrites a day's rows and recomputes the DB chain consistently, when verify compares with the external seal, then it detects the mismatch (15 §2.3 'detected').
- Given the action is set to `alert_only`, then the incident and alerts still fire, the status reads `alert_only`, and the gate allows entries.

### Stress / failure injection
- Full verify of 10 M fixture rows across 6 tables < 10 min, memory < 1 GiB (streaming).

## Acceptance criteria

- [ ] `audit.verify` command and daily flow implemented
- [ ] External-seal comparison (not DB-only) proven
- [ ] Mismatch → incident + alert + `audit.integrity` status (default `block_new_entries`) + D16 banner data
- [ ] `integrity_gate` golden tests pass (entries blocked, exits and protective orders pass)
- [ ] `audit.integrity.ack` is C3 and appends a row; hourly incremental + daily full schedules live
- [ ] CI green (ruff, mypy, pytest, gitleaks, `pit` check)

## Exceptions & edge cases

- Anchor store unreachable: verify reports `anchor_unavailable` (warning, not mismatch) and retries; three consecutive days unavailable → critical.
- Late rows flagged by the seal are not mismatches.

## Cardinal rules (do NOT)

- Do NOT 'fix' a mismatch by editing rows; investigate per runbook and append corrections.
- Do NOT compare only against `audit.seal` in the DB.
- Do NOT clear the status by editing KV or rows by hand; only `audit.integrity.ack` clears it.
- Do NOT let the integrity response block exits, protective orders or Kill ON (except `halt_all`, which still allows Kill).
- Do NOT UPDATE or DELETE WORM rows, ever; corrections are new rows with `supersedes_id` ([15 §2](../../../docs/15-bots-hitl-and-worm-audit.md#2-worm-records-write-once-read-many)).
- Loosening risk, autonomous mode and mandates are C3 (Telegram + TOTP + cool-down); Kill ON and protective exits never wait for approval.
- Do NOT bypass `mt_api`, the risk manager (M11) or `mt_store.pit(as_of)`; every order goes through M11.
- Do NOT skip, weaken or delete a test to get CI green.

## Doc sync on completion

- `docs/15-bots-hitl-and-worm-audit.md` §2.2: link the `integrity_gate` hook and the verify cadence; `docs/runbooks/README.md`: index the WORM incident runbook.
- `docs/roadmap/phase-0-foundations.md`: tick T0.23 when every item mapped to it is done.

## Branch & PR

- Branch: `p0/P0-T038-audit-verify-incident-path`
- PR title: `P0-T038: Implement audit.verify, the daily verify flow and the incident path`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P0-T038` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (integrity response per 17 §A P0-B001 / 16 §2.11 (KV audit.integrity, block_new_entries default, M11 hook point, audit.integrity.ack C3) replaces trading_halt/risk.halt.clear; hourly incremental + daily full verify; roadmap T0.27; run fields added)
