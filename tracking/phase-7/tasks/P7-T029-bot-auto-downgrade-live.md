---
id: P7-T029
kind: task
title: Auto-downgrade rules for live autonomous bots
phase: 7
type: BUILD
status: backlog
priority: critical
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P7-T023, P7-T024, P7-T026]
requirements: [R7.08, R7.07]
roadmap_todos: [T7.06, T7.22]
modules: [M11, M0]
dashboards: [D03, D06]
branch: p7/P7-T029-bot-auto-downgrade-live
pr: ""
doc_sync: [docs/15-bots-hitl-and-worm-audit.md, docs/roadmap/phase-7-prove-and-go-live.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P7-T029 · Auto-downgrade rules for live autonomous bots

## Goal / expected outcome

Live autonomous bots drop to `hitl` (or `paused`, per bot) automatically and immediately on any downgrade trigger, including the new Phase 7 signals; upgrading back is C3 again.

## Context & references

- Roadmap: [R7.08, R7.07 · ToDo T7.06, T7.22](../../../docs/roadmap/phase-7-prove-and-go-live.md)
- Spec: [15 §1](../../../docs/15-bots-hitl-and-worm-audit.md#1-trading-bots) (automatic downgrade triggers; upgrade back is C3) · [14 §5](../../../docs/14-strategy-evidence-and-validation.md#5-risk-engine-additions-m11) (fallback ladder) · [12 §2](../../../docs/12-policy-and-compliance.md#2-venue-access-registry) (`venue.registry.changed`)
- Cross-phase: P2 T2.34 (auto-downgrade baseline on paper).
- Related: P7-T023 (decay), P7-T024 (health check), P7-T026 (unconfirmed), P7-T020/T027 (kill), P7-T049 (simulated triggers)

## Requirements

- Triggers (any): decay alert or CUSUM; daily health-check warn; fallback-ladder rung ≥ 3; DQ `degraded|stale|bad` on any in-scope instrument; N consecutive losses (default 5, per bot); model service down; `venue.registry.changed` for its venue/product; account `unconfirmed`; capital state not in {micro_live, step_k, full}; gate report older than 7 days or failing; MT5/cTrader adapter heartbeat lost.
- Action: `bot.set_mode hitl` (or `paused`) with `source=system`, reason and trigger evidence; pending autonomous orders not yet submitted are converted to approval cards; protective exits unaffected.
- Latency: trigger → downgrade < 2 s (DQ-pause SLO is < 2 s, 02 §9.2).
- Notification: Telegram warning with 'Re-enable (C3)' button that starts the C3 flow, which re-runs P7-T028 eligibility.

## ToDo

- [ ] Downgrade handler subscribed to `risk.event`, `dq.status.*`, `venue.registry.changed`, `recon.*`, `sys.heartbeat.*`.
- [ ] Per-bot setting `downgrade_to: hitl|paused` and `max_consecutive_losses`.
- [ ] Telegram notification + C3 re-enable entry point.
- [ ] Tests; docs.

## Verification

### Tests
- Integration: each trigger injected individually downgrades within 2 s and records the reason (table-driven, one row per trigger).
- Integration: in-flight autonomous intent becomes an approval card; stop-loss still fires unapproved.

### Scenarios
- Given a registry status change for Kraken AU, then every autonomous bot on Kraken AU drops to HITL and you get one grouped Telegram message.
- Given 5 consecutive losses, then the bot pauses (configured) and the D03 bot detail shows the downgrade event.

### Stress / failure injection
- Trigger storm (DQ flapping 10×/min): downgrade is idempotent, one notification per bot per 10 min; no upgrade happens without C3.

## Acceptance criteria

- [ ] All listed triggers downgrade within 2 s with reasons.
- [ ] Upgrade back always requires C3.
- [ ] CI green.

## Exceptions & edge cases

- Trigger clears by itself: bot stays downgraded (no auto-upgrade).
- NATS outage: engine-side watchdog treats missing heartbeat as a trigger (fail safe).

## Cardinal rules (do NOT)

- Do NOT auto-upgrade a bot after a trigger clears.
- Do NOT let loosening risk, autonomous mode or a capital step apply without C3 (Telegram + TOTP + cool-down); protective exits never wait for approval.
- Do NOT add discretionary overrides; the only manual action outside approve mode is flatten-and-halt with a required reason (14 §4).
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order goes through M11.
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.

## Doc sync on completion

- `docs/15-bots-hitl-and-worm-audit.md` §1.2: add Phase 7 triggers (unconfirmed, capital state, gate report age, adapter heartbeat).
- `docs/roadmap/phase-7-prove-and-go-live.md`: tick T7.06, T7.22 when this item is done.

## Branch & PR

- Branch: `p7/P7-T029-bot-auto-downgrade-live`
- PR title: `P7-T029: Auto-downgrade rules for live autonomous bots`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P7-T029` run

## Progress log

- 2026-10-21 00:00 · planner · created
