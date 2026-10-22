---
id: P7-T039
kind: task
title: Approvals polish: ≤ 3-tap approve, hold-to-confirm, batching, Telegram cards
phase: 7
type: BUILD
status: backlog
priority: high
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P2-T149, P2-T039]
requirements: [R7.12, R7.08]
roadmap_todos: [T7.25]
modules: [M15]
dashboards: [D01, D05]
tools: [git, pnpm, node>=20, uv]
mcp: []
env: []
services: [mt-api, telegram bot api]
branch: p7/P7-T039-approvals-polish
pr: ""
doc_sync: [docs/ui/mobile-and-telegram.md, docs/ui/components.md, docs/roadmap/phase-7-prove-and-go-live.md]
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

# P7-T039 · Approvals polish: ≤ 3-tap approve, hold-to-confirm, batching, Telegram cards

## Goal / expected outcome

Approving a live HITL order or a C3 change from a cold phone open takes ≤ 3 taps on web/PWA and Telegram, with the full risk preview, TTL countdown and hold-to-confirm, and never executes late.

## Context & references

- Roadmap: [R7.12, R7.08 · ToDo T7.25](../../../docs/roadmap/phase-7-prove-and-go-live.md)
- Spec: [mob §2](../../../docs/ui/mobile-and-telegram.md#2-phone-flows-must-be--3-taps-from-a-cold-open) (approve an order: notification/Telegram → ApprovalCard → hold-to-confirm) · [15 §1.3](../../../docs/15-bots-hitl-and-worm-audit.md#13-hitl-approval-via-telegram) (card content, buttons, TTL defaults, large orders TOTP, batching) · [16 §2.3](../../../docs/16-configuration-and-safety-model.md#23-decisions-approvals-and-hitl) (TTLs, large-order threshold, C3 cool-down and approval TTL) · [mob §3](../../../docs/ui/mobile-and-telegram.md#3-telegram-bot) · [mob §4](../../../docs/ui/mobile-and-telegram.md#4-acceptance-criteria) (C3 completion on phone)
- Cross-phase (`depends_on`): P2-T149 (web approvals queue), P2-T039 (HITL approval cards on Telegram).
- Related: P7-T054 (phone test), P7-T019 (capital-step C3 card), P7-T028 (autonomous C3 card)

## Requirements

- `ApprovalCard` shows bot, instrument, side, size, type/price, stop/target, risk in R and % sleeve, exposure after fill, blackout/DQ warnings, signal reasons, chart deep link, TTL countdown; buttons Approve · Approve ½ · Reject · Pause bot.
- Tap budget from cold open: notification tap (1) → card (already open) → hold-to-confirm (2); C3 flows: Telegram Approve (1) → TOTP entry (2) → done.
- TTL defaults (16 §2.3, settings) 60 s intraday / 15 min swing / 4 h position; expiry = reject, logged 'expired'.
- Large orders (> 2% of sleeve or > A$5,000 notional by default, 16 §2.3) need TOTP on Telegram / hold-to-confirm on web.
- Batching: dynamic-selection bots group signals into one card with per-line toggles.
- Approval latency recorded per card (`risk.approval.latency_ms`) and shown in the weekly pack.
- Never queue approvals offline (mob §1).

## ToDo

- [ ] Refine `ApprovalCard` component (web) + Telegram card template.
- [ ] Deep links from push/Telegram to the specific card.
- [ ] Batch card with toggles.
- [ ] Latency metric.
- [ ] Tests; docs.

## Verification

### Tests
- Playwright: tap counts on 375×667, 280×653, 568×320 from cold start (service worker cached).
- Integration: approval after TTL rejected server-side even if the client shows time left (clock skew).
- Unit: batch toggles produce one approval per selected line.

### Scenarios
- Given a swing signal at 02:00 during quiet hours, then no entry card is sent unless 'wake me' is on.
- Given an order above 2% of sleeve or A$5,000 notional (defaults), then Telegram asks for TOTP before approving.

### Stress / failure injection
- 20 cards arriving in 1 min: UI remains responsive; Telegram 30 msg/s limit respected; no duplicate approvals on double-tap (idempotency key).

## Acceptance criteria

- [ ] Approve flow ≤ 3 taps from cold open on phone (web/PWA and Telegram).
- [ ] Late approvals never execute.
- [ ] CI green incl. viewport matrix + axe.

## Exceptions & edge cases

- Phone offline: card shows stale banner; approve disabled.
- Telegram and web approve the same card: first wins, second gets 'already decided'.

## Cardinal rules (do NOT)

- Do NOT execute an approval after TTL.
- Do NOT include Telegram message text in any model context.
- Do NOT let loosening risk, autonomous mode or a capital step apply without C3 (Telegram + TOTP + cool-down); protective exits never wait for approval.
- Do NOT put Telegram text into any model, RAG index or training set (12 §4–5).
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order goes through M11.
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.

## Doc sync on completion

- `docs/ui/mobile-and-telegram.md` §2–3: final tap paths.
- `docs/ui/components.md`: ApprovalCard spec update.
- `docs/roadmap/phase-7-prove-and-go-live.md`: tick T7.25 when this item is done.

## Branch & PR

- Branch: `p7/P7-T039-approvals-polish`
- PR title: `P7-T039: Approvals polish: ≤ 3-tap approve, hold-to-confirm, batching, Telegram cards`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P7-T039` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (TTLs and large-order TOTP threshold per 16 §2.3; deps P2-T149/P2-T039)
