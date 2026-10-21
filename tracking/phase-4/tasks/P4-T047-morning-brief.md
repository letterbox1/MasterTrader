---
id: P4-T047
kind: task
title: Morning brief job on Telegram (and /brief)
phase: 4
type: BUILD
status: backlog
priority: high
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P4-T043, P4-T035, P4-T038, P4-T040]
requirements: [R4.14]
roadmap_todos: [T4.29]
modules: [M15, M2, M3, M5, M6, M16]
dashboards: [D08]
branch: p4/P4-T047-morning-brief
pr: ""
doc_sync: [docs/ui/mobile-and-telegram.md, docs/runbooks/morning-brief.md, docs/roadmap/phase-4-intel.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P4-T047 · Morning brief job on Telegram (and /brief)

## Goal / expected outcome

A Prefect flow composes and sends a **deterministic, template-based** morning brief to your Telegram at a configured time (default 07:00 Australia/Sydney) and on `/brief`: top sourced news (titles + links, relevance-ranked, deduped), sentiment movers, global events mapped to assets with scores, today's calendar with **risk blackouts**, Telegram postures summary (numbers only), positions/P&L summary, and data/cost health — each item with a deep link into `/intel`.

## Context & references

- Roadmap: [R4.14](../../../docs/roadmap/phase-4-intel.md#3-requirements) · ToDo [T4.29](../../../docs/roadmap/phase-4-intel.md#4-todo-sets) · Exit criterion 1
- Telegram digests: [mobile-and-telegram §3](../../../docs/ui/mobile-and-telegram.md#3-telegram-bot) · [04 Phase 4 demo](../../../docs/04-plan-of-action.md#phase-4--news-social-events--calendars-weeks-1619)
- Cross-phase: P1 R1.14 (Telegram alerts bot), P2 R2.52 (`/status` etc.).
- Gap: P4-B011 (brief contents differ between docs).

## Requirements

- Built from `mt_api` queries only; no LLM summarisation in P4 (template + numbers) so no text flows to a model and the brief is reproducible.
- Sections: News (≤ 8 items, each 'title — source — link'), Sentiment movers (top 5 Δ24h z), Events (≤ 5 with mapped instruments + score), Calendar today (high/med importance, consensus/previous, blackout windows), Telegram postures (top 5 subjects by velocity; numbers only), Portfolio (positions/P&L), Health (feeds stale, quota > 80%, DQ incidents, LLM/gateway spend).
- Telegram limits: ≤ 4,096 chars per message, split into ≤ 3 messages; Bot API ≤ 30 msg/s respected.
- Brief record stored in `ops.notification` with content hash; idempotent per day (no double send on retry).
- Feedback buttons 'useful/not useful' per news item update source hit-rate (for P4-T060 tuning).

## ToDo

- [ ] Brief builder (pure function over a snapshot) + Telegram renderer (MarkdownV2 escaping).
- [ ] Prefect schedule + `/brief` handler.
- [ ] Feedback buttons → `intel.feedback` (C0) → `text.source` counters.
- [ ] Golden tests on fixed snapshots.
- [ ] Runbook entry.

## Verification

### Tests
- Golden: fixed snapshot → exact message text.
- Unit: MarkdownV2 escaping of hostile titles.
- Unit: splitting at 4,096 chars on section boundaries.
- Integration: scheduled run sends once even if the flow retries.

### Scenarios
- Given feeds are stale, then the Health section lists them first.
- Given no events today, then the Events section says 'none' rather than disappearing.
- Given mt-api is down at 07:00, then the flow retries for 30 min then sends a degraded brief from cached data with a banner.

### Stress / failure injection
- n/a: once-daily job; retry/idempotency tested above.

## Acceptance criteria

- [ ] Brief arrives at the configured time with all sections and deep links
- [ ] Golden tests green; no LLM call in the path
- [ ] CI green (ruff, mypy, pytest, `pit` bypass check)

## Exceptions & edge cases

- Quiet hours never suppress the brief (it is the scheduled digest), but suppress non-critical alerts around it.

## Cardinal rules (do NOT)

- Do NOT include Telegram message text; postures are numbers only.
- Do NOT send to any chat id other than your user id.
- Do NOT let Telegram text (or any `model_input_ok = false` row) reach a model, RAG index or training set ([12 §4–5](../../../docs/12-policy-and-compliance.md#4-per-platform-data--automation-rules)).
- Do NOT commit secrets or paste them into chats, issues or logs; they live only in the sops/age file ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Do NOT bypass `mt_api`, the risk manager (M11) or `mt_store.pit(as_of)`; every order goes through M11.
- Do NOT skip, weaken or delete a test to get green.

## Doc sync on completion

- `docs/ui/mobile-and-telegram.md`: §3 Digests: final brief sections
- `docs/runbooks/morning-brief.md`: new: schedule, resend, troubleshooting
- `docs/roadmap/phase-4-intel.md`: tick T4.29 when all items mapped to it are done

## Branch & PR

- Branch: `p4/P4-T047-morning-brief`
- PR title: `P4-T047: Morning brief job on Telegram (and /brief)`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P4-T047` run

## Progress log

- 2026-10-21 00:00 · planner · created
