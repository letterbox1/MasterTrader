---
id: P5-B013
kind: gap
title: Tenderly free tier: "120K simulations/month" (research) vs "no simulation API" (06, 13)
phase: 5
type: DOC
status: backlog
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
branch: p5/P5-B013-tenderly-free-tier-contradiction
pr: ""
doc_sync: [docs/research/airdrops-rugpull-discord.md]
doc_sync_status: n/a
found_in: "docs/research/airdrops-rugpull-discord.md §Safety sources"
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
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

- [ ] Agree the resolution with the user (or record the decision in the progress log)
- [ ] Edit the source docs listed under Doc sync so they agree
- [ ] Update the affected P5 task files if the numbers/names change

## Verification

### Tests
- Doc review: every listed doc states the same value/name after the fix; `python3 tools/kanban/kanban.py validate` stays at 0 errors

### Scenarios
- Given the fixed docs, when a developer picks up the affected P5 tasks, then there is exactly one authoritative answer to follow

### Stress / failure injection
- n/a: documentation/spec gap

## Acceptance criteria

- [ ] Docs listed under Doc sync are consistent
- [ ] Affected P5 tasks reference the resolved value/name
- [ ] Resolution recorded in the progress log

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
