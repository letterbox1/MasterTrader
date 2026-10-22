---
id: P2-T039
kind: task
title: HITL approval cards on Telegram
phase: 2
type: BUILD
status: backlog
priority: critical
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P2-T035, P2-T037, P2-T038]
requirements: [R2.54, R2.51]
roadmap_todos: [T2.33, T2.34]
modules: [M15]
dashboards: []
tools: [uv]
mcp: []
env: []
services: [nats]
branch: p2/P2-T039-telegram-hitl-approval-cards
pr: ""
doc_sync: [docs/ui/mobile-and-telegram.md, docs/15-bots-hitl-and-worm-audit.md, docs/roadmap/phase-2-strategies-risk-lab.md]
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

# P2-T039 · HITL approval cards on Telegram

## Goal / expected outcome

Each `risk.approval.request` from a hitl bot (or an escalated autonomous order) becomes a Telegram card with order, risk preview, reasons, chart link and live TTL, and buttons Approve · Approve ½ · Reject · Pause bot; large orders need a TOTP reply; every decision and expiry is stored with the card snapshot in WORM.

## Context & references

- Roadmap: [R2.54, R2.51](../../../docs/roadmap/phase-2-strategies-risk-lab.md) · ToDos T2.33, T2.34
- Design: [15 §1.3 HITL via Telegram](../../../docs/15-bots-hitl-and-worm-audit.md#13-hitl-approval-via-telegram) · [mob §3 HITL card](../../../docs/ui/mobile-and-telegram.md#3-telegram-bot)
- Related: P2-T033 approval service, P2-T038 web card (same snapshot), P2-T061 scenarios, P2-T066 your first approval.

## Requirements

- Card text (MarkdownV2, ≤ 4096 chars): bot, instrument, side, size, order type/price, stop/target; risk in R and % of sleeve, exposure after fill, blackout/DQ warnings; 'Why' = top reasons (features/tier-B flags/agent summary from signal metadata, never Telegram-sourced text); chart deep link (Tailscale URL); TTL countdown edited every 10 s (≤ 1 edit/s overall to respect Bot API limits).
- Buttons → `approval.approve|approve_partial|reject` and `bot.pause`; callback data signed + idempotent; bound to your user id.
- Large orders (above the bot's threshold, default > 2% of sleeve or > A$5,000 notional, [16 §2.3](../../../docs/16-configuration-and-safety-model.md#23-decisions-approvals-and-hitl)): after Approve, the bot asks for a TOTP reply within the TTL; wrong/missing → reject.
- TTLs come from the bot (defaults 60 s intraday · 15 min swing · 4 h position); expiry = reject.
- Batching for dynamic-selection bots: one card with per-line toggles + 'Approve selected' (the only bulk approve allowed, 17 §D).
- Expiry: card edited to 'Expired — not executed'; late taps answered 'Expired'.
- Snapshot of exactly what was shown stored in `risk.approval.card_snapshot` with decision latency.

## ToDo

- [ ] Card renderer + button handlers in `packages/mt_ui/telegram/approvals.py`
- [ ] TOTP reply sub-flow
- [ ] Batch card
- [ ] Rate-limit aware message editor
- [ ] Tests
- [ ] Update the docs listed under *Doc sync on completion* and tick the roadmap ToDo box(es) once every task mapped to them is done

## Verification

### Tests
- Unit: card render snapshot tests (normal, warnings, batch).
- Flow tests: approve, ½, reject, pause bot, expiry, large-order TOTP.
- Unit: callback from another user id ignored.

### Scenarios
- Given a hitl gold bot signal with TTL 15 min, when you tap Approve ½, then the order is re-checked at half size, submitted, and the card shows 'Approved ½ — filled 0.5 oz @ …'.
- Given you tap Approve after expiry, when processed, then nothing executes and the bot replies 'Expired'.

### Stress / failure injection
- 20 cards within 10 s (dynamic bot burst): batched or queued without hitting Telegram 429; no card lost; TTLs honoured.

## Acceptance criteria

- [ ] Card content matches 15 §1.3
- [ ] All four buttons + TOTP path work
- [ ] Snapshots stored WORM
- [ ] CI green: ruff, mypy, pytest (and the `mt_risk` golden suite, `pit` check, viewport matrix where relevant)

## Exceptions & edge cases

- Telegram 429/outage: approvals continue on web; cards re-sent when back if TTL remains.
- Quiet hours: no new-entry cards unless 'wake me' (P2-T037).

## Cardinal rules (do NOT)

- Do NOT include any Telegram-sourced text in 'Why'.
- Do NOT execute on a tap received after TTL.
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order goes through M11, whatever its source.
- Do NOT commit secrets or paste them into chats/issues/logs; secrets live in the sops/age file (07 §2).
- Do NOT skip, weaken or delete a test to get green; risk-manager golden tests are mandatory for merge.
- Do NOT UPDATE or DELETE WORM rows (`audit.*`, `risk.change`, `risk.approval`, `strategy.bot_version`); corrections are new rows with `supersedes_id` (15 §2).
- No Telegram text in any model, RAG index or training set (12 §4–5).
- Loosening risk, autonomous mode and mandates are C3 (Telegram approve + TOTP + cool-down); protective exits never wait for approval.

## Doc sync on completion

- `docs/ui/mobile-and-telegram.md` §3 and `docs/15-bots-hitl-and-worm-audit.md` §1.3: card format as built.
- `docs/roadmap/phase-2-strategies-risk-lab.md`: tick T2.33, T2.34 when all tasks mapped to it are done.

## Branch & PR

- Branch: `p2/P2-T039-telegram-hitl-approval-cards`
- PR title: `P2-T039: HITL approval cards on Telegram`
- PR checklist: tests added and green · docs synced · task file ticked · no secrets (gitleaks) · `./kanban done P2-T039` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (large-order and TTL defaults from 16 §2.3, batched card as the only bulk approve; keyless (fake Bot API))
