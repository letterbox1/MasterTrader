---
id: P6-T015
kind: task
title: Explain agent: anomaly briefs to Telegram
phase: 6
type: BUILD
status: backlog
priority: high
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P6-T014, P6-T005, P6-T006, P6-T009, P1-T045, P0-T034]
requirements: [R6.05]
roadmap_todos: [T6.22]
modules: [M10, M8, M15]
dashboards: [D09]
tools: [git, uv, python>=3.12, docker]
mcp: []
env: []
services: [litellm, llm-local, nats, telegram-bot-api]
branch: p6/P6-T015-anomaly-explain-agent
pr: ""
doc_sync: [docs/03-build-spec.md, docs/ui/mobile-and-telegram.md, docs/roadmap/phase-6-ai-models-treasury.md]
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

# P6-T015 · Explain agent: anomaly briefs to Telegram

## Goal / expected outcome

For each high/warn anomaly the explain agent gathers `pit` context (bars, news via RAG, calendar, events, tier-B scores) and writes a short sourced brief, delivered to Telegram and shown in D09; it may trigger an M8 run per the trigger rules.

## Context & references

- Roadmap: [R6.05](../../../docs/roadmap/phase-6-ai-models-treasury.md#3-requirements) · ToDo T6.22
- Spec: [03 M10](../../../docs/03-build-spec.md#m10-anomaly-monitor--mt_anomaly) (explain agent → Telegram) · [10 §4.3](../../../docs/10-memory-rag-and-models.md#43-design) (tier-B scores feed M10 explanations) · [03 §7](../../../docs/03-build-spec.md#7-llm-cost-control)
- UI: [D09](../../../docs/ui/dashboards/D09-agents.md) Anomaly explanations (`/notifications?kind=anomaly`)
- Exit: [roadmap §6 exit criteria](../../../docs/roadmap/phase-6-ai-models-treasury.md#6-exit-criteria-demo) item 2
- Depends on (this phase): P6-T014, P6-T005, P6-T009, P6-T006
- Cross-phase: P1-T045 (Telegram/ntfy alert fan-out), P0-T034 (command bus)
- Command: [02 §7.2](../../../docs/02-v1-architecture.md#72-commands-rest-write) `anomaly.explain` (C1; result arrives as a notification)

## Requirements

- Consumer of `alert.anomaly.*`; builds a context pack with the P6-T006 tools (`as_of` = anomaly `event_time`).
- Brief: ≤ 120 words, what happened, likely drivers with source links, what to watch; every number sourced; uses gateway role `explain` (budgeted, local fallback).
- Delivery: Telegram bot message (alert channel) + `ops.notification` (kind=anomaly) + WS `notifications`; brief text stored with the anomaly id.
- Rate limit: ≤ 1 brief per (subject) per 60 min; info-severity anomalies batched into the daily digest.
- Telegram output only: Telegram content is never an input to the brief.
- Command `anomaly.explain` (C1): explain any anomaly id on request; the brief arrives as a notification (02 §7.2).
- Built keyless: tests use `local-advisor` and recorded responses; the `explain` role's default daily budget is $0.30 (16 §2.10).

## ToDo

- [ ] `mt_anomaly.explain` consumer + prompt (registry versioned).
- [ ] Context-pack builder using the tool belt.
- [ ] Telegram + notification delivery; link to D09.
- [ ] `anomaly.explain` command handler (C1).
- [ ] Tests with recorded LLM responses; docs.

## Verification

### Tests
- Unit: context pack contains only `as_of`-valid items; brief length limit.
- Integration: anomaly event → Telegram mock receives one message with source links.

### Scenarios
- Given a high-severity spike on gold with a CPI release 5 min earlier, then the brief cites the calendar item and the bar.
- Given the explain budget is exhausted, then the brief comes from the local model and is labelled "local model".
- Given the gateway and local model are both down, then a plain templated alert (numbers only) is sent.

### Stress / failure injection
- 50 anomalies in one minute: briefs rate-limited, queue drains, Telegram stays < 30 msg/s.

## Acceptance criteria

- [ ] Seeded anomaly → Telegram brief end-to-end (also proven in P6-T061).
- [ ] Every brief's LLM call audited.

## Exceptions & edge cases

- Telegram API down: notification stored and retried; ntfy fallback for high severity.

## Cardinal rules (do NOT)

- Do NOT include Telegram channel text in any prompt; Telegram postures (counts) only.
- Do NOT let Telegram text (or any `model_input_ok = false` / `train_ok = false` row) reach a model, prompt, RAG index, memory bank or training set (12 §4–5).
- Do NOT commit secrets or paste them into chats/issues/PRs; secrets live only in the sops/age file (07 §2).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral/broker IDs in vendored code.

## Doc sync on completion

- `docs/03-build-spec.md` M10: brief format and rate limits.
- `docs/ui/mobile-and-telegram.md`: anomaly message format.
- `docs/roadmap/phase-6-ai-models-treasury.md`: tick T6.22 (and note this task ID) once all items covering it are done.

## Branch & PR

- Branch: `p6/P6-T015-anomaly-explain-agent`
- PR title: `P6-T015: Explain agent: anomaly briefs to Telegram`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P6-T015` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (anomaly.explain command (C1, 02 §7.2); explain budget default 16 §2.10; keyless; cross-phase deps P1-T045/P0-T034; run fields)
