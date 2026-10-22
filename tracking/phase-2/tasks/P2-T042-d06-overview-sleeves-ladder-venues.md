---
id: P2-T042
kind: task
title: "D06 Risk overview: kill, dead-man, gauges, sleeves, ladder, venue registry"
phase: 2
type: BUILD
status: backlog
priority: critical
size: L
severity: ""
owner: agent
claimed_by: ""
depends_on: [P2-T020, P2-T018, P2-T031, P2-T032, P2-T014, P2-T016, P2-T069, P2-T070, P0-T049, P0-T050]
requirements: [R2.50, R2.15, R2.18]
roadmap_todos: [T2.32]
modules: [M15, M11]
dashboards: [D06]
tools: [pnpm]
mcp: []
env: []
services: []
branch: p2/P2-T042-d06-overview-sleeves-ladder-venues
pr: ""
doc_sync: [docs/ui/dashboards/D06-risk.md, docs/roadmap/phase-2-strategies-risk-lab.md]
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

# P2-T042 · D06 Risk overview: kill, dead-man, gauges, sleeves, ladder, venue registry

## Goal / expected outcome

`/risk` Overview shows the kill switch (big HALT, ≥ 56 px on touch), dead-man heartbeats with an accurate countdown, risk state, limit gauges, exposure breakdown, recent events, sleeves, the live fallback ladder and the venue registry; the top-bar HALT is wired to `risk.kill.on`.

## Context & references

- Roadmap: [R2.50, R2.15, R2.18](../../../docs/roadmap/phase-2-strategies-risk-lab.md) · ToDo T2.32
- UI: [D06 Overview + CryptoTrader additions](../../../docs/ui/dashboards/D06-risk.md) · [components LimitBar, LadderIndicator, VenueStatusChip, KillSwitchButton](../../../docs/ui/components.md)
- Test matrix: [DESIGN §6.8](../../../DESIGN.md#68-test-matrix-every-screen-must-pass)
- Cross-phase (`depends_on`): app shell + top-bar kill placeholder (P0-T050, R0.11); component library v0 (P0-T049).
- Decisions: six-rung ladder and sleeves from policy ([17 §D P2-B004](../../../docs/17-decisions-register.md#d-other-decisions)); two-stage sleeve/system drawdowns ([16 §2.1](../../../docs/16-configuration-and-safety-model.md#21-risk-sizing-and-drawdown)); three-layer dead-man ([16 §3.1](../../../docs/16-configuration-and-safety-model.md#31-three-layer-dead-mans-switch)); kill actions per bot `on_system_failure`, no sweep in P2 ([17 §B P2-B010](../../../docs/17-decisions-register.md#b-cross-doc-conflicts-one-canonical-answer)); venue cap 25%.
- Related: P2-T069 (effective value + layer per limit), P2-T070 (safety state), P2-T072/P2-T073 (dead-man layers 2–3).

## Requirements

- Layout per tier exactly as D06 (≥ 2xl rows; xl/lg; md; ≤ ph stacked with kill card first).
- Kill tile: ARMED/HALTED, last trigger (reason, source, time), actions on halt (stop new trading, cancel all, each bot's `on_system_failure`, treasury/earn moves frozen; "vault sweep: from P5"), HALT button (Kill level single confirm); Resume = C3 with cause check.
- Dead-man tile: the **three layers** (in-engine watchdog per service, `deadman` sidecar heartbeat, venue timers refreshed/age per venue), last beat + thresholds (defaults 5 s cancel / 10 s `on_system_failure`), countdown when late (±1 s vs server); Ack (C1).
- Risk state: bot mode summary (paper / hitl / autonomous counts), trading allowed + reasons, ladder rung, **system drawdown stage**, **audit-integrity status** (`ok` / mismatch + action), **egress IP/country check**, active blackouts, DQ-paused instruments.
- `LimitBar` gauges (used/limit/warn/breach + the layer that set the limit): drawdown from peak with **both stages** marked (system 10% no new entries / 25% flatten + 30-day lock; sleeve 10% halve / 15% halt), daily loss, exposure, leverage, open orders, order rate, venue concentration vs the 25% cap; exposure breakdown + VaR/ES, recent `risk.event`s.
- Sleeves widget (sleeves from policy, never a fixed list; capital, usage, drawdown vs its two stages, daily loss, status), ladder widget (6 rungs rendered from the API, current + trigger; step down C1, up C3), venue registry widget (status, `paper_ok`, products, max leverage capped 2× for crypto derivatives, STP mode or `n/a (netting)`, AUSTRAC check age, concentration vs cap; tighten C1 / allow C3).
- WS topics `kill`, `heartbeat`, `risk.state`, `risk.event`, `dq.status`; REST fallbacks.

## ToDo

- [ ] Route `apps/web/src/routes/risk/overview.tsx` + widgets
- [ ] `KillSwitchButton` wiring in `TopBar`
- [ ] `LadderIndicator`, `VenueStatusChip`, `LimitBar` components (if not in library v0)
- [ ] Playwright flows
- [ ] Update the docs listed under *Doc sync on completion* and tick the roadmap ToDo box(es) once every task mapped to them is done

## Verification

### Tests
- Component tests per widget incl. all data states.
- Playwright: HALT from a cold load in one tap + confirm (D06 acceptance 3); countdown within ±1 s of server (D06 acceptance 4).

### Scenarios
- Given the monitor heartbeat stops, when D06 is open, then the dead-man tile counts down and turns red at threshold, matching server time ±1 s.
- Given the ladder is at rung 4, when viewing D06, then the widget shows 'Rules only — exits, no entries' with the trigger 'model service down'.

### Stress / failure injection
- Event storm: 50 `risk.event`/s for 1 min; UI stays responsive (≤ 1 Hz table updates), no memory growth > 50 MB.

## Acceptance criteria

- [ ] All Overview widgets + additions implemented
- [ ] HALT ≥ 56 px on touch and one tap + confirm
- [ ] Countdown ±1 s
- [ ] CI green: ruff, mypy, pytest (and the `mt_risk` golden suite, `pit` check, viewport matrix where relevant)

## Exceptions & edge cases

- Offline PWA: last known state + 'Offline: data may be stale'; HALT tries every channel (mob §1).
- mt-api down: page unreachable — Telegram `/kill` is the path (documented in runbook).

## Cardinal rules (do NOT)

- Do NOT hide or move the HALT button behind a menu at any viewport.
- Do NOT compute risk state in the browser; render server state.
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order goes through M11, whatever its source.
- Do NOT commit secrets or paste them into chats/issues/logs; secrets live in the sops/age file (07 §2).
- Do NOT skip, weaken or delete a test to get green; risk-manager golden tests are mandatory for merge.
- Loosening risk, autonomous mode and mandates are C3 (Telegram approve + TOTP + cool-down); protective exits never wait for approval.

## Doc sync on completion

- `docs/ui/dashboards/D06-risk.md`: Overview widgets as built (six rungs and policy sleeves already in the doc).
- `docs/roadmap/phase-2-strategies-risk-lab.md`: tick T2.32 when all tasks mapped to it are done.

## Branch & PR

- Branch: `p2/P2-T042-d06-overview-sleeves-ladder-venues`
- PR title: `P2-T042: D06 Risk overview: kill, dead-man, gauges, sleeves, ladder, venue registry`
- PR checklist: tests added and green · docs synced · task file ticked · no secrets (gitleaks) · `./kanban done P2-T042` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (risk state with integrity/egress/drawdown stage, two-stage gauges with layer, three-layer dead-man tile, kill actions per decision, sleeves from policy)
