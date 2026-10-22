---
id: P7-T064
kind: task
title: Phase 7 exit demo
phase: 7
type: VERIFY
status: backlog
priority: critical
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P7-T048, P7-T049, P7-T050, P7-T051, P7-T052, P7-T054, P7-T055, P7-T057, P7-T058, P7-T059, P7-T060, P7-T061, P7-T063, P7-T067, P7-T069]
requirements: [R7.01, R7.02, R7.03, R7.04, R7.05, R7.06, R7.07, R7.08, R7.09, R7.10, R7.11, R7.12, R7.13, R7.14, R7.15, R7.16]
roadmap_todos: []
modules: [M11, M12, M16, M18]
dashboards: [D01, D03, D06, D14]
tools: [git, uv, pnpm]
mcp: []
env: []
services: [postgres, nats, mt-api]
branch: p7/P7-T064-phase-exit-demo
pr: ""
doc_sync: [docs/roadmap/README.md, docs/04-plan-of-action.md, docs/roadmap/phase-7-prove-and-go-live.md]
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

# P7-T064 · Phase 7 exit demo

## Goal / expected outcome

A recorded walkthrough proves every exit criterion: at least one strategy is live in a micro sub-account with all gates passed and a complete audit trail; kill criteria and decay monitoring are proven by simulated breaches; weekly reviews are logged for every live week.

## Context & references

- Roadmap: [R7.01, R7.02, R7.03, R7.04, R7.05, R7.06, R7.07, R7.08, R7.09, R7.10, R7.11, R7.12, R7.13, R7.14, R7.15, R7.16](../../../docs/roadmap/phase-7-prove-and-go-live.md)
- Roadmap §6 exit criteria ([phase 7](../../../docs/roadmap/phase-7-prove-and-go-live.md)) · [14 §7](../../../docs/14-strategy-evidence-and-validation.md#7-phase-capital-steps--kill-criteria-refines-04-phase-7) · [15 §2](../../../docs/15-bots-hitl-and-worm-audit.md#2-worm-records-write-once-read-many) (audit trail)
- Related: every Phase 7 item; PHASE.md exit checklist

## Requirements

- Exit 1: show the live sleeve in D06/D03 (state `micro_live` or later), its passing gate report, preflight snapshot, funding C3 record, and `audit.verify` clean over its chain.
- Exit 2: show the P7-T048, P7-T049 and P7-T021 (memecoin) suites green in CI and their observed-run evidence.
- Exit 3: `/journal/reviews` lists a signed review for every live week.
- Also: all Phase 7 tasks done/cancelled (cancelled with reasons, e.g. unchosen adapter, optional Mini App, P7-T062 moved to the recurring 12-month review); no open S1/S2 bugs; R7.01–R7.16 each traced to evidence in PHASE.md.
- Also: R7.14 failover drill evidence (P7-T052), R7.15 Phase 7 API/UI (P7-T067 contract tests + Playwright), R7.16 stress replay attached to the live bot's gate report (P7-T069).
- Exit 4: micro-live is stable (the first sleeve's 4-week window complete, P7-T059); the 12-month review is scheduled as a recurring review (P7-T042/P7-T063), not awaited ([17 §D P7-B012](../../../docs/17-decisions-register.md#d-other-decisions)).

## ToDo

- [ ] Run `mt preflight` and `audit.verify`; capture output.
- [ ] Walk through D03/D06/D14 on desktop and phone; capture redacted screenshots.
- [ ] Link CI runs for P7-T048/T049/T050/T055/T067 and the P7-T021 memecoin suite; attach P7-T052 and P7-T069 evidence.
- [ ] Tick PHASE.md exit criteria with evidence links.
- [ ] Run `./kanban validate --phase 7`.

## Verification

### Tests
- Re-run P7-T048, P7-T049, P7-T055 suites on the exit commit.

### Scenarios
- Given the exit commit, when the suites run, then all pass and `audit.verify` reports zero mismatches.

### Stress / failure injection
- n/a: covered by the referenced VERIFY items.

## Acceptance criteria

- [ ] All three exit criteria demonstrated with evidence.
- [ ] All tasks done/cancelled; no open S1/S2 bugs.
- [ ] PHASE.md exit boxes ticked.

## Exceptions & edge cases

- A sleeve was killed during the phase: exit 1 needs another (or the restarted) sleeve live with gates passed; record the history.

## Cardinal rules (do NOT)

- Do NOT tick an exit box without linked evidence.
- Do NOT weaken a gate, threshold or window to "get live sooner" (roadmap §1, Out).
- Do NOT update or delete WORM rows; corrections are new rows with `supersedes_id` (15 §2).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.

## Doc sync on completion

- `docs/roadmap/README.md` and `docs/04-plan-of-action.md`: mark Phase 7 complete (generated blocks via `./kanban build`, hand-written status lines by the main agent).
- `docs/roadmap/phase-7-prove-and-go-live.md`: tick the matching exit criteria when this item is done.

## Branch & PR

- Branch: `p7/P7-T064-phase-exit-demo`
- PR title: `P7-T064: Phase 7 exit demo`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P7-T064` run · evidence (redacted, no secrets) linked in the progress log

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (R7.14–R7.16 added (P7-T052, P7-T067, P7-T069); P7-T062 cancelled → recurring review; exit 4 per roadmap §6)
