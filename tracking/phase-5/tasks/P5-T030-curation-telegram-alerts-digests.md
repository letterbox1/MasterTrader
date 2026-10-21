---
id: P5-T030
kind: task
title: Telegram task buttons, instant alerts and daily/weekly digests
phase: 5
type: BUILD
status: backlog
priority: high
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P5-T029]
requirements: [R5.20, R5.22]
roadmap_todos: [T5.30]
modules: [M19, M15]
dashboards: [D13]
branch: p5/P5-T030-curation-telegram-alerts-digests
pr: ""
doc_sync: [docs/ui/mobile-and-telegram.md, docs/08-airdrops-and-token-launches.md, docs/roadmap/phase-5-airdrops-wallets-curation.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P5-T030 · Telegram task buttons, instant alerts and daily/weekly digests

## Goal / expected outcome

Tasks reach you on Telegram with `✅ Done · ⏭ Skip · 💤 Snooze 1d/1w · 🔍 Details · 🚫 Never` buttons mapped to the same `mt_api` commands as the UI; instant alerts fire for eligible claims live, deadlines < 48 h and phishing warnings; a morning daily digest and a weekly curation/review digest are composed and sent in Australian time with quiet hours.

## Context & references

- Roadmap: [R5.20](../../../docs/roadmap/phase-5-airdrops-wallets-curation.md), [R5.22](../../../docs/roadmap/phase-5-airdrops-wallets-curation.md) · ToDo T5.30 · soak P5-T063
- [08 cadence](../../../docs/08-airdrops-and-token-launches.md#user-task-queue--digests) · [mobile & Telegram](../../../docs/ui/mobile-and-telegram.md) (buttons; quiet hours except critical) · P2 Telegram bot (T2.33)
- Buttons list in mobile doc lacks Details → P5-B014

## Requirements

- Instant: claim live and eligible, deadline < 48 h, phishing warning on a tracked project — sent immediately, quiet hours overridden only for critical.
- Daily (07:30 Australia/Sydney, configurable): new high-viability items, tasks due, auto-claims executed (with tx links), rejected count.
- Weekly (Sunday 18:00): Discord curation queue, pipeline review, tasks expiring, approvals audit (P5-T025), airdrop income summary for tax (P5-T046), rejected-with-reasons sample.
- Telegram limits: ≤ 30 msg/s globally, ≤ 1 msg/s per chat; long digests split; deep links into D12/D13.
- Digest settings via `system.settings.update` section `digests`; preview endpoint for D13 Digests tab.
- Buttons call `task.*` commands with the Telegram scoped token; identical effect to the UI (D13 acceptance 2).

## ToDo

- [ ] Implement digest composer (Jinja templates) and scheduler (Prefect, DST-aware Australia/Sydney).
- [ ] Implement instant-alert rules consuming `task.new`, `airdrop.*`, monitor events.
- [ ] Extend the P2 Telegram bot with task cards and callback handlers.
- [ ] Preview endpoint `/system/settings?section=digests&preview=1`; tests; doc sync.

## Verification

### Tests
- Unit: digest golden snapshots (daily, weekly) from fixture data.
- Unit: DST transition (first Sunday of April/October) schedules at the right local time.
- Integration: pressing Done in Telegram and in the UI produce identical `audit.command` rows except `source`.

### Scenarios
- Given quiet hours 22:00–07:00 and a non-critical deadline alert at 23:00, then it is held until 07:00; a phishing warning on a tracked project is sent immediately.
- Given Telegram API is down, then digests queue and the web D13 shows them; ntfy receives critical alerts.

### Stress / failure injection
- Weekly digest with 300 items: split correctly, total send < 30 s, no 429s (rate limiter).

## Acceptance criteria

- [ ] Buttons work with identical effect to the UI
- [ ] Instant/daily/weekly cadence with AU timezone and quiet hours
- [ ] Digest preview available

## Exceptions & edge cases

- User snoozes a task already expired: returns a friendly error, no state change.

## Cardinal rules (do NOT)

- Do NOT include Telegram channel text in digests or any model input; postures/counts only.
- Do NOT send unsolicited messages to anyone but the user.
- Do NOT let Telegram text reach any model, RAG index or training set; Telegram contributes deterministic postures only (12 §4–5).
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order, including disposal-rule sells, goes through M11.
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.

## Doc sync on completion

- `docs/ui/mobile-and-telegram.md`: task buttons include Details.
- `docs/08-airdrops-and-token-launches.md`: digest times.
- `docs/roadmap/phase-5-airdrops-wallets-curation.md`: tick T5.30 when this lands (with the other tasks sharing that ToDo).

## Branch & PR

- Branch: `p5/P5-T030-curation-telegram-alerts-digests`
- PR title: `P5-T030: Telegram task buttons, instant alerts and daily/weekly digests`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P5-T030` run

## Progress log

- 2026-10-21 00:00 · planner · created
