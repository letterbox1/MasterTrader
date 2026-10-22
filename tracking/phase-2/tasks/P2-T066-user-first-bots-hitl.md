---
id: P2-T066
kind: task
title: Create your first bots and do one HITL approval from Telegram
phase: 2
type: USER
status: backlog
priority: high
size: S
severity: ""
owner: user
claimed_by: ""
depends_on: [P2-T061, P2-T071, P0-T002]
requirements: [R2.53, R2.54]
roadmap_todos: [T2.09]
modules: [M0, M15]
dashboards: [D03]
tools: []
mcp: []
env: []
services: [telegram, mt-web]
branch: p2/P2-T066-user-first-bots-hitl
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

# P2-T066 · Create your first bots and do one HITL approval from Telegram

## Goal / expected outcome

You create your first bots (scope + mode) in the D03 Bots wizard and approve one HITL order end to end from Telegram — exit criterion 2 (approval part).

## Context & references

- Roadmap: [R2.53, R2.54](../../../docs/roadmap/phase-2-strategies-risk-lab.md) · ToDo T2.09 · exit criterion 2
- Design: [15 §1](../../../docs/15-bots-hitl-and-worm-audit.md#1-trading-bots) · levels [16 §2.3](../../../docs/16-configuration-and-safety-model.md#23-decisions-approvals-and-hitl) (paper → HITL is C2; autonomous is C3)
- Keys last: a `hitl` bot sends real venue orders, so it runs on a testnet/practice account and needs the live testnet check with your keys done first (P2-T071); the paper bot runs on the sandbox venue.
- Cross-phase (`depends_on`): your Telegram bot and user id (P0-T002).

## Requirements

- At least: one paper bot (e.g. Trend on BTC/ETH) and one hitl bot (e.g. Trend on gold or ETH) on the P1 trend strategy version.
- In the wizard, review the manifest's **proposals** next to your sleeve/system limits and accept or tighten (16 §1); keep `on_system_failure: flatten` unless you have a reason.
- Choose TTL (default 60 s intraday · 15 min swing · 4 h position) and large-order threshold (default > 2% of sleeve or > A$5,000) for the hitl bot; switching it from paper to hitl asks for C2.
- Approve one card from Telegram; optionally try Approve ½ and Reject.

## ToDo

- [ ] D03 → Bots → New: strategy version → scope → venue & sleeve → mode → approval policy → review → Create
- [ ] Start both bots
- [ ] When a card arrives on Telegram, review the risk preview and tap Approve
- [ ] Check D03 bot detail: approval row with latency and outcome
- [ ] Record completion in the progress log (no secrets) and run `./kanban done P2-T066`

## Verification

### Tests
- Agent confirms `risk.approval` rows and the paper fill.

### Scenarios
- Given a hitl card, when you approve within the TTL, then the paper order fills and the card updates with the fill.

### Stress / failure injection
- n/a.

## Acceptance criteria

- [ ] Two bots created and running
- [ ] One HITL approval done from Telegram end to end

## Exceptions & edge cases

- No signal within your session: agent can trigger a test signal on the hitl bot (marked test).

## Cardinal rules (do NOT)

- Do NOT set any bot to autonomous unless gates pass (C3 enforces it).
- Loosening risk, autonomous mode and mandates are C3 (Telegram approve + TOTP + cool-down); protective exits never wait for approval.

## Doc sync on completion

- `docs/15-bots-hitl-and-worm-audit.md` §1: example bots.
- `docs/roadmap/phase-2-strategies-risk-lab.md`: tick T2.09 when all tasks mapped to it are done.

## Branch & PR

- Branch: `p2/P2-T066-user-first-bots-hitl` (only if a repo change results, e.g. non-secret config or manifests; secrets never go in git)
- PR title: `P2-T066: Create your first bots and do one HITL approval from Telegram`
- PR checklist: no secrets in diff (gitleaks clean) · task file ticked · `./kanban done P2-T066` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (wizard proposals vs limits, C2 paper→HITL, HITL bot on testnet after P2-T071, defaults from 16 §2.3)
