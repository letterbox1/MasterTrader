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
depends_on: [P2-T061]
requirements: [R2.53, R2.54]
roadmap_todos: [T2.09]
modules: [M0, M15]
dashboards: [D03]
branch: p2/P2-T066-user-first-bots-hitl
pr: ""
doc_sync: [docs/15-bots-hitl-and-worm-audit.md, docs/roadmap/phase-2-strategies-risk-lab.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P2-T066 · Create your first bots and do one HITL approval from Telegram

## Goal / expected outcome

You create your first bots (scope + mode) in the D03 Bots wizard and approve one HITL order end to end from Telegram — exit criterion 2 (approval part).

## Context & references

- Roadmap: [R2.53, R2.54](../../../docs/roadmap/phase-2-strategies-risk-lab.md) · ToDo T2.09 · exit criterion 2
- Design: [15 §1](../../../docs/15-bots-hitl-and-worm-audit.md#1-trading-bots)

## Requirements

- At least: one paper bot (e.g. Trend on BTC/ETH) and one hitl bot (e.g. Trend on gold or ETH) on the P1 trend strategy version.
- Choose TTL and large-order threshold for the hitl bot.
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
