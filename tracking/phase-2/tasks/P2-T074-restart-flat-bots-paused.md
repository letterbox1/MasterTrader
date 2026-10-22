---
id: P2-T074
kind: task
title: "Clean restart after an unplanned stop: reconcile, flat, bots paused until you resume"
phase: 2
type: BUILD
status: backlog
priority: high
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P2-T027, P2-T036, P2-T032]
requirements: [R2.56, R2.32]
roadmap_todos: [T2.36]
modules: [M12, M11]
dashboards: [D06, D03]
tools: [uv]
mcp: []
env: []
services: [nats, postgres]
branch: p2/P2-T074-restart-flat-bots-paused
pr: ""
doc_sync: [docs/02-v1-architecture.md, docs/roadmap/phase-2-strategies-risk-lab.md]
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

# P2-T074 · Clean restart after an unplanned stop: reconcile, flat, bots paused until you resume

## Goal / expected outcome

After any unplanned stop (crash, kill -9, host reboot), the engine starts with **every bot paused**, reconciles each venue (P2-T027), handles any residual position or order per policy so trading resumes from **flat**, and keeps bots paused until you resume them with one tap (C1) on Telegram/web, unless a bot has `auto_resume_after_crash: true`.

## Context & references

- Roadmap: [R2.56](../../../docs/roadmap/phase-2-strategies-risk-lab.md) · ToDo T2.36
- Decisions: [16 §3.1 clean restart](../../../docs/16-configuration-and-safety-model.md#31-three-layer-dead-mans-switch) · [17 §A P2-B002](../../../docs/17-decisions-register.md#a-s2-items-all-resolved) · [02 F6 step 4](../../../docs/02-v1-architecture.md#8-end-to-end-flows)
- Related: P2-T027 (reconciliation), P2-T036 (`auto_resume_after_crash`, `on_system_failure` per bot), P2-T040/P2-T041 (resume from Telegram/web), P2-T055 (restart-duplicate chaos test asserts this flow), P2-T075 (kill-the-engine drill).

## Requirements

- Planned vs unplanned stop: a clean shutdown writes a `clean_stop` marker (WORM event); its absence at boot = unplanned.
- On unplanned boot: every bot `paused` (status published on `bot.{id}.status`); reconciliation first (P2-T027); then residue per bot policy: `flatten` → residual positions closed reduce-only and orders cancelled; `cancel_orders_only` → orders cancelled, position kept under its resting venue stop and flagged for review; `hold` → kept and flagged; hold-and-earn exempt. Orders not attributable to a bot are cancelled and reported.
- Bots stay paused until `bot.resume` (C1, Telegram one tap or web) per bot or `resume all` (C1); `auto_resume_after_crash: true` bots resume automatically after reconciliation completes clean.
- A summary card is sent to Telegram and shown in D06: what was found, what was closed/cancelled, which bots wait for you.
- Pending approvals at crash time are expired (P2-T033); no decision older than its deadline is acted on.

## ToDo

- [ ] Clean-stop marker and boot classification
- [ ] Boot sequence: pause all → reconcile → residue handling per policy → summary
- [ ] Resume commands wiring (`bot.resume`, resume all) and the `auto_resume_after_crash` path
- [ ] Telegram/D06 summary
- [ ] Tests
- [ ] Update the docs listed under *Doc sync on completion* and tick the roadmap ToDo box(es) once every task mapped to them is done

## Verification

### Tests
- Integration (sandbox + venue emulator): kill -9 with open positions and orders → boot → all bots paused, residue handled per policy, summary sent; resume one bot (C1) → only it trades.
- Unit: planned shutdown → bots keep their previous state (no forced pause).

### Scenarios
- Given the engine crashed with a `flatten` bot holding 0.1 BTC, when it restarts, then the position is closed, the bot stays paused and you get a summary with a Resume button.
- Given a bot with `auto_resume_after_crash: true`, when reconciliation completes clean, then it resumes and the summary says so.

### Stress / failure injection
- Crash again during the residue handling: the next boot repeats the sequence idempotently (no double close; signal-hash ledger respected).

## Acceptance criteria

- [ ] Unplanned restart always starts with bots paused and trades from flat per policy
- [ ] Resume is C1 per bot, or automatic only where `auto_resume_after_crash: true`
- [ ] CI green: ruff, mypy, pytest (and the `mt_risk` golden suite)

## Exceptions & edge cases

- A venue unreachable at boot: its bots stay paused and its positions 'unconfirmed' (P2-T027); others proceed.
- Kill switch ON at crash time: it stays ON after restart (KV persisted); resuming bots doesn't turn kill off.

## Cardinal rules (do NOT)

- Do NOT auto-resume bots after an unplanned stop unless `auto_resume_after_crash: true` is set for that bot.
- Do NOT resubmit pre-crash intents.
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order goes through M11, whatever its source.
- Do NOT commit secrets or paste them into chats/issues/logs; secrets live in the sops/age file outside the repo (07 §2).
- Do NOT skip, weaken or delete a test to get green; risk-manager golden tests are mandatory for merge.
- Do NOT UPDATE or DELETE WORM rows (`audit.*`, `risk.change`, `risk.approval`, `strategy.bot_version`); corrections are new rows (15 §2).
- Keys are trade-only, IP-locked, withdrawals disabled. No live money before the P7 gates; this phase is paper/testnet/practice only.
- Loosening risk, autonomous mode and mandates are C3 (Telegram approve + TOTP + cool-down); protective exits never wait for approval.

## Doc sync on completion

- `docs/02-v1-architecture.md` F6: restart sequence as built.
- `docs/roadmap/phase-2-strategies-risk-lab.md`: tick T2.36 when all tasks mapped to it are done.

## Branch & PR

- Branch: `p2/P2-T074-restart-flat-bots-paused`
- PR title: `P2-T074: Clean restart after an unplanned stop: reconcile, flat, bots paused until you resume`
- PR checklist: tests added and green · docs synced · task file ticked · no secrets (gitleaks) · `./kanban done P2-T074` run

## Progress log

- 2026-10-22 00:00 · aligner · created for docs/16–17 (T2.36: R2.56, R2.32)
