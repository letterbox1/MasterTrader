---
id: P2-T041
kind: task
title: D03 Bots tab, create wizard and bot detail
phase: 2
type: BUILD
status: backlog
priority: high
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P2-T036, P2-T037, P2-T038]
requirements: [R2.54, R2.50]
roadmap_todos: [T2.34]
modules: [M15]
dashboards: [D03]
branch: p2/P2-T041-d03-bots-tab-wizard
pr: ""
doc_sync: [docs/ui/dashboards/D03-strategies.md, docs/roadmap/phase-2-strategies-risk-lab.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P2-T041 · D03 Bots tab, create wizard and bot detail

## Goal / expected outcome

`/strategies/bots` lists bots with mode chips and pending approvals, a wizard creates bots (strategy version → scope → venue & sleeve → mode → approval policy → review with risk preview), and bot detail shows mode history (WORM), approvals and auto-downgrade events. The rest of D03 is Part B.

## Context & references

- Roadmap: [R2.54, R2.50](../../../docs/roadmap/phase-2-strategies-risk-lab.md) · ToDo T2.34
- UI: [D03 Bots tab](../../../docs/ui/dashboards/D03-strategies.md) · [components](../../../docs/ui/components.md) · Design: [15 §1.5](../../../docs/15-bots-hitl-and-worm-audit.md#1-trading-bots)
- Test matrix: [DESIGN §6.8](../../../DESIGN.md#68-test-matrix-every-screen-must-pass)
- Part B: D03 registry/builder/detail tabs.

## Requirements

- List: bot, strategy version, scope, venue & sleeve, mode chip (paper · HITL · autonomous), status, pending approvals, today P&L; `DataTable` priorities + card renderer ≤ ph.
- Wizard steps with zod validation from the manifest/param schema; review shows `RiskPreview` and the confirmation level the server will require.
- Actions: `bot.create` (C1), `bot.set_mode` (paper/HITL C1/C2 per server; autonomous C3 via `C3Flow`, disabled with the failing gate shown), `bot.pause|resume|stop` (C1), `bot.approval_policy.set` (tighten C1, loosen C3).
- Detail: mode history from `strategy.bot_version`, approvals table (shown card, decision, latency, outcome), downgrade events.
- All data states (loading/empty/error/stale) per ui README §3.1.

## ToDo

- [ ] Routes `apps/web/src/routes/strategies/bots/*`
- [ ] Wizard + detail components
- [ ] Typed client calls + WS subscriptions (`bot.{id}.status`, approvals)
- [ ] Playwright flows
- [ ] Update the docs listed under *Doc sync on completion* and tick the roadmap ToDo box(es) once every task mapped to them is done

## Verification

### Tests
- Component tests for wizard validation.
- Playwright: create a paper bot, switch to HITL, attempt autonomous (blocked by gate), approve a card from the detail page.

### Scenarios
- Given a gate fails, when you open the mode switch, then 'Autonomous' is disabled and the failing gate is named.
- Given you loosen the TTL in approval policy, when saved, then the C3Flow starts and the change shows as pending.

### Stress / failure injection
- List with 100 bots renders < 300 ms at 1920×1080 and 390×844.

## Acceptance criteria

- [ ] Bots tab, wizard, detail live and wired
- [ ] Server-side levels reflected in UI
- [ ] Phone usable (≤ 3 taps to pause a bot)
- [ ] CI green: ruff, mypy, pytest (and the `mt_risk` golden suite, `pit` check, viewport matrix where relevant)

## Exceptions & edge cases

- WS disconnected: stale banner, actions still go via REST.
- Strategy version without param schema (legacy): wizard refuses.

## Cardinal rules (do NOT)

- Do NOT enforce confirmation levels only in the UI; the server decides.
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order goes through M11, whatever its source.
- Do NOT commit secrets or paste them into chats/issues/logs; secrets live in the sops/age file (07 §2).
- Do NOT skip, weaken or delete a test to get green; risk-manager golden tests are mandatory for merge.
- Loosening risk, autonomous mode and mandates are C3 (Telegram approve + TOTP + cool-down); protective exits never wait for approval.

## Doc sync on completion

- `docs/ui/dashboards/D03-strategies.md`: Bots tab as built.
- `docs/roadmap/phase-2-strategies-risk-lab.md`: tick T2.34 when all tasks mapped to it are done.

## Branch & PR

- Branch: `p2/P2-T041-d03-bots-tab-wizard`
- PR title: `P2-T041: D03 Bots tab, create wizard and bot detail`
- PR checklist: tests added and green · docs synced · task file ticked · no secrets (gitleaks) · `./kanban done P2-T041` run

## Progress log

- 2026-10-21 00:00 · planner · created
