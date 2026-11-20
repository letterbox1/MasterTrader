---
id: P6-T080
kind: task
title: Run the scenario twin every week alongside the paper bots until go-live
phase: 6
type: RUN
status: backlog
priority: high
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P6-T079, P6-T077, P1-T077]
requirements: [R6.33]
roadmap_todos: [T6.81]
modules: [M14, mt-scheduler]
dashboards: [D14]
tools: [git, docker]
mcp: []
env: []
services: [mt-scheduler, nats, supabase-postgres, llm-local]
branch: p6/P6-T080-run-the-scenario-twin-every-week-alongside-the-p
pr: ""
doc_sync: [docs/roadmap/phase-6-ai-models-treasury.md]
doc_sync_status: n/a
found_in: ""
created: 2026-11-20
updated: 2026-11-20
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
review_result: ""
---

# P6-T080 · Run the scenario twin every week alongside the paper bots until go-live

## Goal / expected outcome

The scenario twin runs **every week** alongside the paper bots, from the week it lands until go-live (`crowdsim.scenario_twin.enabled`), as an `mt-scheduler` job; each week's reports appear in D14 and feed the P7 weekly reviews. Like the distillation soak, this item is **started** here: it closes once the first weekly run is scheduled and has produced its report; later weeks are checked at P7 entry and in the weekly reviews.

## Context & references

- Roadmap: [R6.33](../../../docs/roadmap/phase-6-ai-models-treasury.md#3-requirements) · ToDo T6.81 · exit criterion 5
- Canonical: [18 §2.4](../../../docs/18-platform-and-deployment.md#24-scenario--crowd-simulator-m14-a-go-live-tool) ("paper weeks that run before it's ready simply have no twin report") · [16 §2.14b](../../../docs/16-configuration-and-safety-model.md#214b-scenario--crowd-simulator-m14)
- Cross-phase: P1-T077 (`mt-scheduler`: cron, retries, run history); consumers P7-T015 (weekly review pack), P7-T069 (stress replay)
- Depends on (this phase): P6-T079 (dry run passed), P6-T077 (D14 view)

## Requirements

- A weekly `mt-scheduler` job (default after the week closes, Sunday UTC; a setting) runs the pick, the simulator and the twin; retries per the scheduler defaults; status on D16/D07.
- Missed weeks are reported, not back-filled in a burst.
- Runs while `crowdsim.scenario_twin.enabled` is on; stops by itself when it's turned off (default: off after go-live).

## ToDo

- [ ] Register the weekly job in `mt-scheduler`.
- [ ] Confirm the first scheduled week produced reports visible in D14.
- [ ] Hand-over note for P7 (where the reports are, how missed weeks show).

## Verification

### Tests
- n/a: elapsed-time run; job health on D16/D07 and the D14 view.

### Scenarios
- Given the first scheduled week closes, when the job runs, then D14 shows that week's report per bot.

### Stress / failure injection
- Simulate a failed week (gateway down): the job retries, then records the week as missed and alerts; the next week runs normally.

## Acceptance criteria

- [ ] The weekly job is scheduled and its first run produced reports in D14.
- [ ] Hand-over note written for P7.

## Exceptions & edge cases

- The soak continues after this item is done; P7 reads the weekly reports.

## Cardinal rules (do NOT)

- Do NOT treat twin results as a gate unless 16 says so.
- Do NOT point the twin at real paper or live accounts.
- Do NOT commit secrets or paste them into chats/issues/PRs; secrets live only in the sops/age file (07 §2).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral/broker IDs in vendored code.

## Doc sync on completion

- `docs/roadmap/phase-6-ai-models-treasury.md`: tick T6.81 (and note this task ID) once all items covering it are done.

## Branch & PR

- Branch: `p6/P6-T080-run-the-scenario-twin-every-week-alongside-the-p`
- PR title: `P6-T080: Run the scenario twin every week alongside the paper bots until go-live`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P6-T080` run

## Progress log

- 2026-11-20 01:11 · cloud:vm:be04b6ae61f8 · created
- 2026-11-20 00:00 · aligner · Rust-max per 17 §H (new task for the scenario & crowd simulator workstream, 18 §2.4)
