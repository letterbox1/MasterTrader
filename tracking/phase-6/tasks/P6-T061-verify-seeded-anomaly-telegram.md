---
id: P6-T061
kind: task
title: Seeded anomaly is detected and explained on Telegram
phase: 6
type: VERIFY
status: backlog
priority: high
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P6-T015, P1-T060]
requirements: [R6.05]
roadmap_todos: [T6.68]
modules: [M10, M15]
dashboards: [D09]
tools: [git, uv, python>=3.12, docker]
mcp: []
env: [TELEGRAM_BOT_TOKEN, TELEGRAM_ALERT_CHAT_ID]
services: [anomaly, telegram-bot-api]
branch: p6/P6-T061-verify-seeded-anomaly-telegram
pr: ""
doc_sync: [docs/03-build-spec.md, docs/roadmap/phase-6-ai-models-treasury.md]
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

# P6-T061 · Seeded anomaly is detected and explained on Telegram

## Goal / expected outcome

End-to-end proof for R6.05: a seeded anomaly in a replayed bar stream is detected by the right detector, explained by the explain agent with sources, and delivered to Telegram and D09 within 2 minutes.

## Context & references

- Roadmap: [R6.05](../../../docs/roadmap/phase-6-ai-models-treasury.md#3-requirements) · ToDo T6.68
- Roadmap: R6.05 'Seeded anomaly' · [03 M10](../../../docs/03-build-spec.md#m10-anomaly-monitor--mt_anomaly) · [roadmap §6 exit criteria](../../../docs/roadmap/phase-6-ai-models-treasury.md#6-exit-criteria-demo) item 2
- Decision: [17 §D](../../../docs/17-decisions-register.md#d-other-decisions) (P6-B001: VERIFY ToDo added, this is T6.68)
- Cross-phase: P1-T060 (alert path to Telegram verified with your existing bot; no new key)
- Depends on (this phase): P6-T015

## Requirements

- Seed four cases: volume spike (robust z), regime shift (change point), multivariate outlier (IsolationForest), correlation break.
- Measure detection latency and end-to-end time to Telegram.
- Check cool-down and that the brief cites real sources.

## ToDo

- [ ] Replay fixtures with seeded anomalies.
- [ ] Run in staging with the real Telegram bot to a test chat.
- [ ] Record screenshots/IDs in the progress log.

## Verification

### Tests
- E2E test (Telegram mocked in CI; real bot once in staging).

### Scenarios
- Given a seeded 8σ ETH volume spike, then within 2 min Telegram shows a brief with the bar and a news/calendar source.

### Stress / failure injection
- Seed 20 anomalies in 1 min: rate limits respected; no duplicates.

## Acceptance criteria

- [ ] All four seeded cases detected and explained.
- [ ] End-to-end < 2 min.

## Exceptions & edge cases

- If the explain LLM is down, the templated numeric alert still arrives.

## Cardinal rules (do NOT)

- Do NOT seed into production data tables; use replay fixtures.
- Do NOT UPDATE or DELETE WORM rows (`audit.*`, `journal.*`, policy changes); corrections are new rows referencing the original (15 §2).
- Do NOT commit secrets or paste them into chats/issues/PRs; secrets live only in the sops/age file (07 §2).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral/broker IDs in vendored code.

## Doc sync on completion

- `docs/03-build-spec.md` M10: verified latency.
- `docs/roadmap/phase-6-ai-models-treasury.md`: tick T6.68 (and note this task ID) once all items covering it are done.

## Branch & PR

- Branch: `p6/P6-T061-verify-seeded-anomaly-telegram`
- PR title: `P6-T061: Seeded anomaly is detected and explained on Telegram`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P6-T061` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (maps to new T6.68; Telegram uses the P1 alert bot (P1-T060), CI mocked; run fields)
