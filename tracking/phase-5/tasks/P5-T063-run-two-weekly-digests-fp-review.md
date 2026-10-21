---
id: P5-T063
kind: task
title: Run two weekly digests and review rejected-with-reasons for false positives
phase: 5
type: RUN
status: backlog
priority: medium
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P5-T030, P5-T041, P5-T047]
requirements: [R5.22, R5.13]
roadmap_todos: [T5.80]
modules: [M4, M19]
dashboards: [D12, D13]
branch: p5/P5-T063-run-two-weekly-digests-fp-review
pr: ""
doc_sync: [docs/08-airdrops-and-token-launches.md, docs/roadmap/phase-5-airdrops-wallets-curation.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P5-T063 · Run two weekly digests and review rejected-with-reasons for false positives

## Goal / expected outcome

Two consecutive weekly digests (with the daily digests between them) go out on schedule; at each, the rejected-with-reasons list is reviewed with you for false positives, and thresholds/weights are tuned (tightening freely; loosening only with your sign-off). The second digest is the artefact for exit criterion 1.

## Context & references

- Roadmap: ToDo T5.80 → R5.22 · exit criterion 1 ([§6](../../../docs/roadmap/phase-5-airdrops-wallets-curation.md))
- Runs alongside USER P5-T008 · digests P5-T030

## Requirements

- Both weekly digests contain: vetted opportunities with EV, numbered steps, verified links; curation queue; tasks expiring; approvals audit; income summary.
- False-positive review: sample ≥ 20 rejects per week; label each FP/TP with you; record FP rate; propose changes.
- Changes go through config PRs with the score version bumped.

## ToDo

- [ ] Confirm digest schedule; watch both weeks' runs.
- [ ] Hold two review sessions (≈ 30 min each); record labels in `curation.decision` feedback.
- [ ] Tune weights/thresholds; record FP rate before/after in the progress log.

## Verification

### Tests
- Digest delivery logs for 14 days; FP review sheets.

### Scenarios
- Given a legit project rejected for `domain_conflict`, when reviewed, then the official-domain resolution rule is fixed and the project re-scored.

### Stress / failure injection
- n/a: observation window

## Acceptance criteria

- [ ] Two weekly digests delivered on time
- [ ] ≥ 40 rejects reviewed; FP rate recorded
- [ ] Tuning changes merged or explicitly deferred

## Exceptions & edge cases

- A missed digest (outage) extends the window by one week.

## Cardinal rules (do NOT)

- Do NOT loosen risk thresholds without your explicit sign-off.
- Do NOT let Telegram text reach any model, RAG index or training set; Telegram contributes deterministic postures only (12 §4–5).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.

## Doc sync on completion

- `docs/08-airdrops-and-token-launches.md`: note tuned thresholds/score version.
- `docs/roadmap/phase-5-airdrops-wallets-curation.md`: tick T5.80 when this lands (with the other tasks sharing that ToDo).

## Branch & PR

- Branch: `p5/P5-T063-run-two-weekly-digests-fp-review`
- PR title: `P5-T063: Run two weekly digests and review rejected-with-reasons for false positives`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P5-T063` run

## Progress log

- 2026-10-21 00:00 · planner · created
