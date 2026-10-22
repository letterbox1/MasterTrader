---
id: P2-T061
kind: task
title: "Bot scenarios: HITL approvals, protective exits, autonomous C3 and isolation"
phase: 2
type: VERIFY
status: backlog
priority: critical
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P2-T037, P2-T039, P2-T040, P2-T041]
requirements: [R2.53, R2.54]
roadmap_todos: [T2.69]
modules: [M11, M15]
dashboards: [D03]
tools: [uv, docker]
mcp: []
env: []
services: [nats, postgres]
branch: p2/P2-T061-verify-bot-scenarios
pr: ""
doc_sync: [docs/15-bots-hitl-and-worm-audit.md, docs/roadmap/phase-2-strategies-risk-lab.md]
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

# P2-T061 · Bot scenarios: HITL approvals, protective exits, autonomous C3 and isolation

## Goal / expected outcome

End-to-end scenarios on paper prove: HITL approve / approve ½ / reject / expiry (never executes late); protective stop fires without approval; autonomous needs C3 and auto-downgrades on an injected DQ fault; two bots on one strategy with different modes stay isolated.

## Context & references

- Roadmap: [R2.53, R2.54](../../../docs/roadmap/phase-2-strategies-risk-lab.md) · ToDo T2.69
- Design: [15 §1](../../../docs/15-bots-hitl-and-worm-audit.md#1-trading-bots) · [15 §1.3](../../../docs/15-bots-hitl-and-worm-audit.md#13-hitl-approval-via-telegram)
- Defaults: TTLs 60 s / 15 min / 4 h, large orders > 2% of sleeve or > A$5,000 → TOTP / hold-to-confirm, paper → HITL C2, HITL → autonomous C3 ([16 §2.3](../../../docs/16-configuration-and-safety-model.md#23-decisions-approvals-and-hitl)).
- Build first, keys last: runs on paper with a fake Telegram Bot API (no secrets); the real-Telegram run is your P2-T066.
- Related: P2-T066 (your manual run).

## Requirements

- S1 approve: card → Approve → order submitted once, filled (paper), `risk.approval` rows (request + decision + snapshot).
- S2 approve ½: size halved (lot-rounded down), re-checked.
- S3 reject: nothing submitted.
- S4 expiry: TTL 5 s (test bot), tap at 6 s → 'Expired', nothing submitted, audit 'expired'.
- S5 protective stop on a hitl bot fires with no card.
- S6 autonomous request without C3 refused; with C3 applied after cool-down.
- S7 injected DQ degraded on the autonomous bot's instrument → hitl within 1 s, alert.
- S8 two bots (same strategy version; BTC autonomous, gold hitl) → BTC submits directly, gold produces cards; positions/P&L attributed per bot; pausing one doesn't affect the other.
- S9 paper → HITL asks for C2; a large order (> 2% of sleeve) asks for TOTP on Telegram and hold-to-confirm on web.
- S10 restricting the strategy's mode ceiling to `hitl` drops its autonomous bot to HITL at once (C1).
- Run via the Telegram fake in CI; the real-Telegram run is P2-T066.

## ToDo

- [ ] Scenario tests in `tests/e2e/bots/`
- [ ] Record results (numbers, run IDs, screenshots) in the progress log and tick the roadmap ToDo box

## Verification

### Tests
- S1–S8 automated.

### Scenarios
- S1–S8 above, each given/when/then in the test docstrings.

### Stress / failure injection
- 20 hitl cards in 10 s from a dynamic bot: all decided or expired correctly; no late execution.

## Acceptance criteria

- [ ] S1–S10 green in CI

## Exceptions & edge cases

- Telegram rate-limit during the real run: retry; never shorten TTL semantics.

## Cardinal rules (do NOT)

- Do NOT test against live accounts.
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order goes through M11, whatever its source.
- Do NOT skip, weaken or delete a test to get green; risk-manager golden tests are mandatory for merge.
- Loosening risk, autonomous mode and mandates are C3 (Telegram approve + TOTP + cool-down); protective exits never wait for approval.
- Do NOT UPDATE or DELETE WORM rows (`audit.*`, `risk.change`, `risk.approval`, `strategy.bot_version`); corrections are new rows with `supersedes_id` (15 §2).

## Doc sync on completion

- `docs/15-bots-hitl-and-worm-audit.md` §1: link scenario tests.
- `docs/roadmap/phase-2-strategies-risk-lab.md`: tick T2.69 when all tasks mapped to it are done.

## Branch & PR

- Branch: `p2/P2-T061-verify-bot-scenarios`
- PR title: `P2-T061: Bot scenarios: HITL approvals, protective exits, autonomous C3 and isolation`
- PR checklist: tests added and green · docs synced · task file ticked · no secrets (gitleaks) · `./kanban done P2-T061` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (keyless (fake Telegram), C2 paper→HITL, large-order TOTP, strategy ceiling scenario; real run is P2-T066)
