---
id: P5-B013
kind: gap
title: Tenderly free tier: "120K simulations/month" (research) vs "no simulation API" (06, 13)
phase: 5
type: DOC
status: done
priority: low
size: XS
severity: S4
owner: agent
claimed_by: ""
depends_on: []
requirements: [R5.02]
roadmap_todos: []
modules: [M22]
dashboards: []
tools: []
mcp: []
env: []
services: []
branch: p5/P5-B013-tenderly-free-tier-contradiction
pr: ""
doc_sync: [docs/research/airdrops-rugpull-discord.md]
doc_sync_status: done
found_in: "docs/research/airdrops-rugpull-discord.md §Safety sources"
created: 2026-10-21
updated: 2026-10-22
started: ""
completed: 2026-10-22
blocked_reason: ""
checkpoint: ""
review_result: ""
---

# P5-B013 · Tenderly free tier: "120K simulations/month" (research) vs "no simulation API" (06, 13)

## Goal / expected outcome

The research note agrees with the decision (Anvil fork; Tenderly free plan has no simulation API).

## Context & references

- Research: "Tenderly free tier (120K simulations/month) for EVM"
- 06 skip list and 13 §2: Tenderly free plan has no simulation API → Anvil

## Requirements

- **Steps to reproduce:** Read both.
- **Expected:** Consistent statement.
- **Actual:** Contradiction.
- **Suggested fix:** Annotate the research line as superseded (Anvil chosen; Tenderly free API not available).
- **Impact:** S4: documentation only; design already uses Anvil.

## ToDo

- [x] Resolution per 17 §D (Tenderly not used; Anvil + simulateTransaction)
- [x] docs/research/airdrops-rugpull-discord.md line 60 annotated as superseded
- [x] P5-T016 already uses Anvil/simulateTransaction only

## Verification

### Tests
- Doc review: every listed doc states the same value/name after the fix; `python3 tools/kanban/kanban.py validate` stays at 0 errors

### Scenarios
- Given the fixed docs, when a developer picks up the affected P5 tasks, then there is exactly one authoritative answer to follow

### Stress / failure injection
- n/a: documentation/spec gap

## Acceptance criteria

- [x] Docs listed under Doc sync are consistent
- [x] Affected P5 tasks reference the resolved value/name
- [x] Resolution recorded in the progress log

## Exceptions & edge cases

- Until resolved, implementers use the suggested fix as the default and flag it in their PR description

## Cardinal rules (do NOT)

- Do NOT resolve by silently picking a looser (less safe) value; when in doubt choose the stricter option.
- Do NOT edit WORM records to "fix" data; append a correction instead.

## Doc sync on completion

- `docs/research/airdrops-rugpull-discord.md`: align with the resolution

## Branch & PR

- Branch: `p5/P5-B013-tenderly-free-tier-contradiction`
- PR title: `P5-B013: Tenderly free tier: "120K simulations/month" (research) vs "no simulation API" (06, 13)`

## Progress log

- 2026-10-21 00:00 · planner · opened
- 2026-10-22 00:00 · aligner · left open: 17 §D records the decision (Tenderly not used; Anvil + `simulateTransaction` only) and 13 §2, 06 (Anvil row + skip list), 11 and roadmap R5.02 carry it, but docs/research/airdrops-rugpull-discord.md line 60 still reads "Simulation: Tenderly free tier (120K simulations/month) for EVM" with no superseded note (the suggested fix). Needs a one-line "superseded: Anvil/simulateTransaction only (17 §D)" annotation by the doc owner. Implementation already owned by P5-T016 (Anvil/simulateTransaction only)
- 2026-10-22 00:00 · wrap-up doc agent · closed in the wrap-up: research note marked superseded per 17 §D
- 2026-10-22 02:30 · cloud:vm:be04b6ae61f8 · verified: docs/research/airdrops-rugpull-discord.md Simulation line (superseded note: Anvil + simulateTransaction, 17 §D)
- 2026-10-22 02:30 · cloud:vm:be04b6ae61f8 · done
- 2026-10-22 02:30 · cloud:vm:be04b6ae61f8 · doc sync done: docs updated in the wrap-up
