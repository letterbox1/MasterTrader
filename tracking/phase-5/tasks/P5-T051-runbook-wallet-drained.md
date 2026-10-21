---
id: P5-T051
kind: task
title: Runbook: wallet drained (revoke, isolate, sweep)
phase: 5
type: DOC
status: backlog
priority: high
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P5-T025, P5-T028]
requirements: [R5.03, R5.07]
roadmap_todos: [T5.90]
modules: [M22, M4]
dashboards: [D18, D12]
branch: p5/P5-T051-runbook-wallet-drained
pr: ""
doc_sync: [docs/runbooks/wallet-drained.md, docs/07-security-notes.md, docs/roadmap/phase-5-airdrops-wallets-curation.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P5-T051 · Runbook: wallet drained (revoke, isolate, sweep)

## Goal / expected outcome

`docs/runbooks/wallet-drained.md` gives a step-by-step, phone-first procedure for a drained or suspicious hot/identity/burner wallet: kill switch, freeze the wallet in the signer, revoke approvals, sweep remaining assets to the vault, rotate keys, check nonce authorities, preserve evidence, journal the loss and review — linked from the alerts that can trigger it.

## Context & references

- Roadmap: ToDo T5.90 → [07 §9](../../../docs/07-security-notes.md#9-monitoring--incident-response) ("Wallet drained") · drill in P7 (T7.60)
- Signer/sweeps/monitors: P5-T013, P5-T025, P5-T028 · P2 runbooks format (T2.90)

## Requirements

- Triggers: unexpected outflow alert, new approval alert, nonce-authority change, signer refusal spike, recon break on a hot wallet.
- Steps with exact commands/UI paths: `/kill` (Telegram) → `wallet.freeze` (signer flag) → revoke via `wallet.revoke_approval` (or revoke.cash manually from a clean device for user wallets) → `wallet.sweep` to vault → rotate keys (`mt-signer keys rotate`, C3) and retire the old address (`legacy`) → check durable nonce accounts → collect tx hashes and ledger rows → journal loss event (correction rows) → TAX_QUESTION task → post-mortem.
- Time targets: kill + freeze < 2 min from alert; sweep attempt < 10 min.
- No secrets in the runbook.

## ToDo

- [ ] Write the runbook in the P2 runbook format with a one-screen phone checklist at the top.
- [ ] Link it from the alert annotations (Grafana/Telegram) for the triggers listed.
- [ ] Dry-run on a testnet burner and record timings in the progress log.
- [ ] Update 07 §9 to link the runbook.

## Verification

### Tests
- Tabletop + testnet dry run: drain simulation on a burner (approve to a test spender, pull funds) → follow the runbook → timings recorded.

### Scenarios
- Given a nonce-authority change alert at 03:00, when you follow the phone checklist, then the wallet is frozen and swept within targets.

### Stress / failure injection
- Dry run with the web UI down: all steps achievable via Telegram commands and CLI.

## Acceptance criteria

- [ ] Runbook merged and linked from alerts
- [ ] Testnet dry run completed within time targets

## Exceptions & edge cases

- Vault compromise is out of scope here (manual, offline) — runbook points to the estate letter/shares process instead.

## Cardinal rules (do NOT)

- Do NOT include any secret, seed or key in the runbook or screenshots.
- Do NOT commit secrets or paste them into chats, issues or logs; secrets live only in the sops/age file or OpenBao (07 §2).
- Do NOT UPDATE or DELETE WORM rows (`curation.mandate`, `curation.exec_log`, the signer ledger, `journal.*`, `audit.*`); corrections are new rows with `supersedes_id` (15 §2).

## Doc sync on completion

- `docs/07-security-notes.md` §9: link to the new runbook.
- `docs/runbooks/wallet-drained.md`: new file.
- `docs/roadmap/phase-5-airdrops-wallets-curation.md`: tick T5.90 when this lands (with the other tasks sharing that ToDo).

## Branch & PR

- Branch: `p5/P5-T051-runbook-wallet-drained`
- PR title: `P5-T051: Runbook: wallet drained (revoke, isolate, sweep)`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P5-T051` run

## Progress log

- 2026-10-21 00:00 · planner · created
