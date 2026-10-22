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
depends_on: [P4-T043, P4-T035, P4-T038, P4-T040, P2-T035]
requirements: [R4.14]
roadmap_todos: [T4.29]
modules: [M15, M2, M3, M5, M6, M16]
dashboards: [D08]
tools: [uv, git]
mcp: []
env: []
services: [postgres, nats, telegram-bot, prefect-server]
branch: p4/P4-T047-morning-brief
pr: ""
doc_sync: [docs/ui/mobile-and-telegram.md, docs/runbooks/morning-brief.md, docs/roadmap/phase-4-intel.md]
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

# P4-T047 · Morning brief job on Telegram (and /brief)

## Goal / expected outcome

A Prefect flow composes and sends a **deterministic, template-based** morning brief to your Telegram at the time you set in D13 Digests (configurable default 07:00 Australia/Sydney) and on `/brief`. Its contents are the **canonical list in [mobile-and-telegram §3](../../../docs/ui/mobile-and-telegram.md#3-telegram-bot)**: overnight news for your positions and watchlist, sentiment movers, events mapped to assets, today's calendar with trading blackouts, Telegram postures as numbers only, positions and P&L (paper and live labelled separately), data and cost health, and new vetted airdrops (that section arrives with Phase 5). Each item deep-links to its dashboard.

## Context & references

- Roadmap: [R4.14](../../../docs/roadmap/phase-4-intel.md#3-requirements) · ToDo [T4.29](../../../docs/roadmap/phase-4-intel.md#4-todo-sets) · Exit criterion 1
- Telegram digests: [mobile-and-telegram §3](../../../docs/ui/mobile-and-telegram.md#3-telegram-bot) · [04 Phase 4 demo](../../../docs/04-plan-of-action.md#phase-4--news-social-events--calendars-weeks-1619)
- Cross-phase: P1 R1.14 (Telegram alerts bot), P2 R2.52 (`/status` etc.).
- Decision: [17 §D](../../../docs/17-decisions-register.md#d-other-decisions) (P4-B011): the morning-brief contents are canonical in [mobile-and-telegram §3](../../../docs/ui/mobile-and-telegram.md#3-telegram-bot); 04 and the roadmap link there.
- Cross-phase: P2-T035 (Telegram v1 commands, where `/brief` registers) is a `depends_on` entry; the P1 alerts bot (P1-T045) is reused.
- Blackout defaults in the calendar section: [16 §2.8](../../../docs/16-configuration-and-safety-model.md#28-calendar-blackouts).

## Requirements

- Built from `mt_api` queries only; no LLM summarisation in P4 (template + numbers) so no text flows to a model and the brief is reproducible.
- Sections, in the canonical mob §3 order (item counts are configurable defaults): 1 News (≤ 8 items, each 'title — source — link'), 2 Sentiment movers (top 5 Δ24h z), 3 Events (≤ 5 with mapped instruments + score), 4 Calendar today (high/med importance, consensus/previous, blackout windows from the M11 API), 5 Telegram postures (top 5 subjects by velocity; numbers only), 6 Positions and P&L (paper and live labelled separately), 7 Data and cost health (stale/bad feeds, cost blow-outs, quota headroom, LLM spend), 8 New vetted airdrops (hidden until P5 provides it; the template has the slot so P5 adds no P4 change). Deep links to D08, D01, D07, D12.
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

- `docs/ui/mobile-and-telegram.md`: §3 stays the canonical list; only correct it if the built brief differs
- `docs/runbooks/morning-brief.md`: new: schedule, resend, troubleshooting
- `docs/roadmap/phase-4-intel.md`: tick T4.29 when all items mapped to it are done

## Branch & PR

- Branch: `p4/P4-T047-morning-brief`
- PR title: `P4-T047: Morning brief job on Telegram (and /brief)`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P4-T047` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (contents follow the canonical mob §3 list (17 §D P4-B011), incl. paper/live labels and P5 airdrop slot; time set in D13; explicit depends_on P2-T035)
