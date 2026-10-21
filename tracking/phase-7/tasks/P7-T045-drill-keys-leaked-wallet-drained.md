---
id: P7-T045
kind: task
title: Drill runbooks: keys leaked and wallet drained
phase: 7
type: VERIFY
status: backlog
priority: critical
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P7-T043, P7-T011]
requirements: [R7.04]
roadmap_todos: [T7.60]
modules: [M17, M22]
dashboards: [D16, D18]
branch: p7/P7-T045-drill-keys-leaked-wallet-drained
pr: ""
doc_sync: [docs/runbooks/, docs/roadmap/phase-7-prove-and-go-live.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P7-T045 · Drill runbooks: keys leaked and wallet drained

## Goal / expected outcome

The keys-leaked and wallet-drained runbooks are drilled on testnet/practice keys and test wallets, and recorded in `ops.drill_log`, completing the 'all runbooks drilled' entry criterion.

## Context & references

- Roadmap: [R7.04 · ToDo T7.60](../../../docs/roadmap/phase-7-prove-and-go-live.md)
- Roadmap §2 entry criteria ([phase 7](../../../docs/roadmap/phase-7-prove-and-go-live.md)) · [07 §9](../../../docs/07-security-notes.md#9-monitoring--incident-response) ('Keys leaked': revoke, rotate, check withdrawals; 'Wallet drained': revoke approvals, isolate) · [07 §2](../../../docs/07-security-notes.md#2-secrets) (rotation)
- Cross-phase: P2 T2.90 (keys-leaked runbook), P5 T5.90 (wallet-drained runbook), P5 signer/wallet-indexer.
- Related: P7-T043, P7-T011, gap P7-B011 (wallet-drained runbook comes from P5)

## Requirements

- Keys leaked: treat a testnet key as leaked → revoke at the venue, rotate in sops, engine picks up the new key, key audit passes, withdrawal history checked; time to revoke ≤ 15 min.
- Wallet drained: on a testnet hot/burner wallet, simulate an unexpected outflow alert → signer freeze, approvals revoked, wallet isolated, sweep of remaining balance per runbook; time to freeze ≤ 5 min.
- Both recorded via `ops.drill.record` with evidence.

## ToDo

- [ ] Prepare a testnet key and a testnet hot wallet with a test approval.
- [ ] Run keys-leaked drill; record.
- [ ] Run wallet-drained drill; record.
- [ ] Fix runbook gaps; re-drill if needed.

## Verification

### Tests
- Evidence: key audit before/after; signer freeze event; approval revocation tx on testnet.

### Scenarios
- Given a leaked key alert, when you follow the runbook from your phone, then the key is revoked within 15 minutes.

### Stress / failure injection
- Drill under time pressure: start from a Telegram critical alert at an unannounced time.

## Acceptance criteria

- [ ] Two drills recorded as `pass`.
- [ ] Timings within the limits above.

## Exceptions & edge cases

- P5 wallet-drained runbook not yet available (P5 not done): this item stays blocked; P7-T057 funding is blocked with it.

## Cardinal rules (do NOT)

- Do NOT use live keys or funded mainnet wallets for the drill.
- Do NOT paste the 'leaked' key anywhere.
- Do NOT commit secrets or paste them into chats, issues, PRs or logs; secrets live only in the sops/age file (07 §2).
- Do NOT use keys that are not trade-only, IP-locked and withdrawal-disabled; no live money before the P7 gates pass.

## Doc sync on completion

- `docs/runbooks/`: fixes from the drill.
- `docs/roadmap/phase-7-prove-and-go-live.md`: tick T7.60 when this item is done.

## Branch & PR

- Branch: `p7/P7-T045-drill-keys-leaked-wallet-drained`
- PR title: `P7-T045: Drill runbooks: keys leaked and wallet drained`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P7-T045` run · evidence (redacted, no secrets) linked in the progress log

## Progress log

- 2026-10-21 00:00 · planner · created
