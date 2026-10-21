---
id: P4-T060
kind: task
title: Run two weeks of morning briefs and tune sources by relevance hit-rate
phase: 4
type: RUN
status: backlog
priority: high
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P4-T047, P4-T030, P4-T044, P4-T049]
requirements: [R4.14, R4.01]
roadmap_todos: [T4.80]
modules: [M2, M15]
dashboards: [D08]
branch: p4/P4-T060-run-two-weeks-briefs
pr: ""
doc_sync: [docs/roadmap/phase-4-intel.md, docs/06-aggregators-and-market-providers.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P4-T060 · Run two weeks of morning briefs and tune sources by relevance hit-rate

## Goal / expected outcome

For 14 consecutive days the morning brief is delivered, you mark items useful/not useful, and once a week the agent tunes sources (mute/raise caps/replace feeds/adjust keywords) using relevance hit-rate and your feedback, ending with a short tuning log and the final source set.

## Context & references

- Roadmap: [R4.14](../../../docs/roadmap/phase-4-intel.md#3-requirements) · ToDo [T4.80](../../../docs/roadmap/phase-4-intel.md#4-todo-sets) · Risk 'Source volume overwhelms the relevance gate'
- Related: P4-T047 (brief), P4-T030 (hit-rate), P4-T044 (Sources tab).

## Requirements

- 14 briefs, ≥ 13 on time (≤ 5 min late).
- Weekly tuning at day 7 and day 14: sources with hit-rate < 5% and no useful votes muted or replaced; changes via `intel.source.mute`/`intel.watchlist.update` (audited).
- Track daily: docs ingested, gated relevant, briefs' useful ratio.

## ToDo

- [ ] Start the run (record start date in this file).
- [ ] Daily: check brief delivered; you vote on items (≈ 2 min).
- [ ] Day 7 tuning pass + log.
- [ ] Day 14 tuning pass + final source set + summary metrics.
- [ ] Hand results to the exit demo.

## Verification

### Tests
- Daily automated check: brief record exists in `ops.notification` by 07:05.

### Scenarios
- Given a brief fails one day, then the cause is fixed and the run continues (one miss allowed).
- Given a tuning change mutes a source by mistake, then unmute is C0 and logged.

### Stress / failure injection
- n/a: soak run (the run itself is the soak).

## Acceptance criteria

- [ ] 14-day log with ≥ 13 on-time briefs
- [ ] Two tuning passes recorded with before/after hit-rates
- [ ] Useful ratio in week 2 ≥ week 1

## Exceptions & edge cases

- Public holidays/weekends: briefs still sent (markets like crypto never close).

## Cardinal rules (do NOT)

- Do NOT add paid sources to improve the brief.
- Do NOT include Telegram text in the brief.
- Do NOT let Telegram text (or any `model_input_ok = false` row) reach a model, RAG index or training set ([12 §4–5](../../../docs/12-policy-and-compliance.md#4-per-platform-data--automation-rules)).
- Do NOT add paid data/APIs, scraping that breaks a site's terms, self-bots/user tokens, or any sybil/fake engagement.

## Doc sync on completion

- `docs/roadmap/phase-4-intel.md`: tick T4.80; add tuning outcome to §7
- `docs/06-aggregators-and-market-providers.md`: §2: final source set notes

## Branch & PR

- Branch: `p4/P4-T060-run-two-weeks-briefs`
- PR title: `P4-T060: Run two weeks of morning briefs and tune sources by relevance hit-rate`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P4-T060` run

## Progress log

- 2026-10-21 00:00 · planner · created
