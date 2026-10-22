---
id: P1-T066
kind: task
title: Review the first week of DQ alerts and flag noisy thresholds
phase: 1
type: USER
status: backlog
priority: high
size: S
severity: ""
owner: user
claimed_by: ""
depends_on: [P1-T065]
requirements: [R1.10]
roadmap_todos: [T1.04]
modules: [M16]
dashboards: [D07]
tools: []
mcp: []
env: []
services: [mt-api]
branch: p1/P1-T066-review-first-week-dq-alerts
pr: ""
doc_sync: [docs/roadmap/phase-1-data-and-monitoring.md, docs/03-build-spec.md]
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

# P1-T066 · Review the first week of DQ alerts and flag noisy thresholds

## Goal / expected outcome

You review the soak week's DQ alerts and tell the agent which ones were noise, so thresholds are tuned (tightening applied directly, C1; loosening is C3, completed via the break-glass CLI `mtctl approve` + TOTP until Telegram C3 lands in P2) before P2 relies on DQ to pause strategies.

## Context & references

- Roadmap: requirements [R1.10](../../../docs/roadmap/phase-1-data-and-monitoring.md#3-requirements) · ToDo [T1.04](../../../docs/roadmap/phase-1-data-and-monitoring.md#4-todo-sets)
- Roadmap T1.04 · [D07 Data & Quality](../../../docs/ui/dashboards/D07-data-quality.md) Quality tab · loosening is C3 ([02 §7.2](../../../docs/02-v1-architecture.md#72-commands-rest-write)); in P1 via the break-glass CLI ([17 §D](../../../docs/17-decisions-register.md#d-other-decisions) P0-B002/P1-B009)
- Depends on (this phase): P1-T065

## Requirements

- Open D07 Quality filtered to the soak week (or the soak report from P1-T065)
- For each alert kind, mark: useful / noisy / missing (should have fired)
- Send the list to the agent (no secrets involved); the agent proposes threshold changes as `system.settings.update` commands (defaults from [16 §2.2](../../../docs/16-configuration-and-safety-model.md#22-data-freshness-what-stale-means))
- Approve loosening changes yourself with `mtctl approve <id>` + TOTP (C3, 15 min cool-down by default); tightening applies directly (C1)

## ToDo

- [ ] Review the week's incidents and alerts in D07 and on your phone
- [ ] Write the useful/noisy/missing list and send it to the agent
- [ ] Approve the resulting C3 requests with the break-glass CLI (tightening needs only C1)
- [ ] Confirm the following 48 h are quieter in the progress log

## Verification

### Tests

- Agent check: replay the soak week's data through the new thresholds and show the alert count before/after

### Scenarios

- Given bad-tick alerts fire at every US open, when you mark them noisy, then the agent proposes a session-open widening and you approve it via C3

### Stress / failure injection

- n/a: review

## Acceptance criteria

- [ ] Every alert kind from the soak week classified; threshold changes applied (C1) or approved (C3) and recorded as WORM setting versions

## Exceptions & edge cases

- Never loosen a freshness threshold or the ≤ 250 ms reaction SLO to reduce noise; a bot that tolerates older data uses the slow profile (60 s default); fix the cause of noisy alerts

## Cardinal rules (do NOT)

- Do NOT approve loosening that hides genuine stale/bad data from the risk manager
- Do NOT let any path loosen DQ thresholds, risk or alert routing without C3 (Telegram + TOTP + cool-down; in P1 via the break-glass CLI `mtctl approve` + TOTP); tightening is C1.

## Doc sync on completion

- `docs/roadmap/phase-1-data-and-monitoring.md`: tick T1.04 once every task traced to it in PHASE.md is done; note P1-T066 next to it.
- `docs/03-build-spec.md` §M16: record the tuned default thresholds

## Branch & PR

- Branch: `p1/P1-T066-review-first-week-dq-alerts`
- PR title: `P1-T066: Review the first week of DQ alerts and flag noisy thresholds`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P1-T066` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (C3 via break-glass CLI (P1-B009); thresholds as settings with 16 §2.2 defaults)
