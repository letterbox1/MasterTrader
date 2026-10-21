---
id: P5-T029
kind: task
title: mt_curation task queue: types, verified links, ranking, expiry and feedback
phase: 5
type: BUILD
status: backlog
priority: high
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P5-T009, P5-T011, P5-T031]
requirements: [R5.20]
roadmap_todos: [T5.30]
modules: [M19, M4, M11, M18]
dashboards: [D13]
branch: p5/P5-T029-curation-task-queue-core
pr: ""
doc_sync: [docs/03-build-spec.md, docs/08-airdrops-and-token-launches.md, docs/roadmap/phase-5-airdrops-wallets-curation.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P5-T029 · mt_curation task queue: types, verified links, ranking, expiry and feedback

## Goal / expected outcome

`packages/mt_curation` provides one queue for everything that needs a human: typed `user_task` rows with numbered steps, **official verified links only**, deadline, estimated minutes, risk/viability/EV with top-3 reasons and standing warnings; ranking by urgency × value with feedback learning; automatic expiry; `task.done|skip|snooze|never` commands.

## Context & references

- Roadmap: [R5.20](../../../docs/roadmap/phase-5-airdrops-wallets-curation.md) · ToDo T5.30
- [03 M19](../../../docs/03-build-spec.md#m19-user-task-queue--community-curation--mt_curation) · [08 task queue](../../../docs/08-airdrops-and-token-launches.md#user-task-queue--digests) · [D13](../../../docs/ui/dashboards/D13-tasks-curation.md)
- P3 stored `TAX_QUESTION` tasks (P3 T3.30); [12 §6](../../../docs/12-policy-and-compliance.md#6-professional-advice-triggers-tracked-as-tasks-in-d13--d15) PRO_ADVICE/VENUE_CHECK
- Task-type naming conflict → P5-B004; flow F10 ([02 §8](../../../docs/02-v1-architecture.md#8-end-to-end-flows))

## Requirements

- Types: JOIN_DISCORD, FOLLOW_ANNOUNCEMENTS, JOIN_TELEGRAM, FOLLOW_X, QUEST, ONCHAIN_ACTION_MANUAL, CLAIM_MANUAL, ICO_REVIEW, REVOKE_APPROVAL, TAX_QUESTION (alias TAX_RECORD), GENUINE_USE, PRO_ADVICE, VENUE_CHECK, APPROVE_ORDER (approve-mode orders link to M11 approvals).
- Links: each link has `verified_via` (CoinGecko links, DefiLlama, official docs/X bio, governance forum) and is re-checked against blocklists **when rendered**; failing links render as plain text with a warning (D12/D13 rule).
- Standing warnings on every on-chain task: "never connect your main wallet; never sign Permit".
- Ranking score = f(deadline proximity, EV/viability, risk, estimated minutes, feedback weights); skips/nevers adjust per-project and per-type weights; never = project suppressed.
- Expiry: auto-close as `expired` at deadline; snooze 1d/1w; idempotent commands (C0, `never` C1).
- Publishes `task.new`/`task.updated`; sources: airdrop, curation, risk, journal, monitors.

## ToDo

- [ ] Implement models/repo, `TaskFactory` API used by other services, link verifier (uses blocklists from P5-T031 and official-domain data from P5-T034 when available).
- [ ] Implement ranking + feedback weights (persisted, explainable) and expiry job.
- [ ] Command handlers and queries `/tasks`, `/tasks/{id}`, `/tasks?opportunity=`, `/tasks?status=closed`.
- [ ] Import P3 `TAX_QUESTION` rows; tests; doc sync.

## Verification

### Tests
- Unit: ranking order golden test for a fixture set; feedback (3 skips of type QUEST) lowers QUEST rank.
- Unit: link re-check at render — a link added to the blocklist after task creation renders as plain text.
- Integration: expiry job closes overdue tasks exactly once; snooze hides until due.

### Scenarios
- Given a task with a deadline in 30 h, then it ranks above a higher-EV task due in 10 days and triggers the instant-alert path (P5-T030).
- Given the user taps Never on project X, then all open X tasks close and new X opportunities create no tasks.

### Stress / failure injection
- 10k open tasks: `/tasks` p95 < 200 ms; ranking recompute < 5 s.

## Acceptance criteria

- [ ] All task types supported with verified links
- [ ] Ranking with feedback and expiry live
- [ ] Commands idempotent and audited
- [ ] P3 tax questions visible

## Exceptions & edge cases

- Blocklist service unavailable at render: links render as plain text (fail closed) with "verification unavailable".

## Cardinal rules (do NOT)

- Do NOT render an unverified link as clickable.
- Do NOT create tasks that ask the user to sign permits/approvals for unknown contracts.
- Do NOT add paid data/APIs or scraping that breaks terms; no self-bots or user tokens; no sybil, multi-wallet or fake-engagement patterns.
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order, including disposal-rule sells, goes through M11.
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.

## Doc sync on completion

- `docs/03-build-spec.md` M19: final task-type list.
- `docs/08-airdrops-and-token-launches.md`: task types aligned (P5-B004).
- `docs/roadmap/phase-5-airdrops-wallets-curation.md`: tick T5.30 when this lands (with the other tasks sharing that ToDo).

## Branch & PR

- Branch: `p5/P5-T029-curation-task-queue-core`
- PR title: `P5-T029: mt_curation task queue: types, verified links, ranking, expiry and feedback`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P5-T029` run

## Progress log

- 2026-10-21 00:00 · planner · created
