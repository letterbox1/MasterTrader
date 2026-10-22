---
id: P2-T048
kind: task
title: Review the prefilled defaults and set your initial risk values and L0 ceilings in the settings
phase: 2
type: USER
status: backlog
priority: critical
size: S
severity: ""
owner: user
claimed_by: ""
depends_on: [P2-T011, P2-T012, P2-T043, P0-T062]
requirements: [R2.14, R2.19, R2.55]
roadmap_todos: [T2.01]
modules: [M11]
dashboards: [D03, D06]
tools: []
mcp: []
env: []
services: [mt-web, telegram]
branch: p2/P2-T048-user-risk-policy-ceilings
pr: ""
doc_sync: [docs/16-configuration-and-safety-model.md, docs/roadmap/phase-2-strategies-risk-lab.md]
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

# P2-T048 · Review the prefilled defaults and set your initial risk values and L0 ceilings in the settings

## Goal / expected outcome

You have reviewed the prefilled defaults ([16 §2](../../../docs/16-configuration-and-safety-model.md#2-default-values-all-configurable)) and set your **initial risk policy values** (L1–L3) and the **L0 hard ceilings** in the agent/bot strategy settings (the ceilings section applies to every bot). Every value stays a setting you can change later: tightening is immediate, loosening is C3. There is no host file to edit (17 §E).

## Context & references

- Roadmap: [R2.14, R2.19](../../../docs/roadmap/phase-2-strategies-risk-lab.md) · ToDo T2.01
- Defaults: [16 §2.1 risk/sizing/drawdown](../../../docs/16-configuration-and-safety-model.md#21-risk-sizing-and-drawdown) · [§2.2 data freshness](../../../docs/16-configuration-and-safety-model.md#22-data-freshness-what-stale-means) · [§2.3 decisions/approvals](../../../docs/16-configuration-and-safety-model.md#23-decisions-approvals-and-hitl) · [§2.8 blackouts](../../../docs/16-configuration-and-safety-model.md#28-calendar-blackouts) · [§3.1 dead-man](../../../docs/16-configuration-and-safety-model.md#31-three-layer-dead-mans-switch)
- Decisions: [17 §E ratification](../../../docs/17-decisions-register.md#e-ratification-2026-10-22) (ceilings edited in the strategy settings; configurable values are settings, not decisions) · [17 §A P2-B001, §C P2-B003](../../../docs/17-decisions-register.md#a-s2-items-all-resolved) (the open numbers now have defaults).
- Where you edit: D03 [`/strategies/settings`](../../../docs/ui/dashboards/D03-strategies.md#strategiessettings-strategy-settings-and-hard-ceilings) (Ceilings L0, bot defaults, gate profile) and D06 Policy tab (L1–L3), both built in P2-T043.
- Cross-phase (`depends_on`): your TOTP is enrolled (P0-T062), needed for any C3 loosening.
- Unblocks: paper trading (P2-T067); D06 shows your values.

## Requirements

- Review each prefilled default and keep or change it: risk per trade (1% of sleeve), max position (10%; memecoin 2%), daily loss (3% of sleeve, Sydney day), **sleeve drawdown stages** (10% halve / 15% halt), **system drawdown stages** (10% no new entries / 25% flatten + 30-day lock), open positions (10 per sleeve), leverage (1×; crypto derivatives ≤ 2×), venue concentration (≤ 25%), price collar (2% / 0.5% / 1%), API-error pause (5 in 60 s → 10 min), cost blow-out (1.5× over 20 fills → pause the bot), stale thresholds (2 s fast / 60 s slow), decision deadlines (1 s / 10 s / 5 min / 1 h), HITL TTLs (60 s / 15 min / 4 h), large-order threshold (> 2% of sleeve or > A$5,000), dead-man timers (5 s / 10 s), `on_system_failure` default (`flatten`), blackouts (15 min either side for `event_sensitive` bots).
- **L0 ceilings:** one absolute maximum per field you never want exceeded (e.g. crypto-derivatives leverage 2×, risk/trade ≤ 2%, max daily loss).
- Tightening any value applies immediately; any value **looser than the prefilled default** is a loosening and needs C3 (Telegram approve + TOTP + 15 min cool-down).
- Stage 1 must stay below stage 2 for both drawdown pairs (the form rejects it otherwise).

## ToDo

- [ ] Open D03 → Strategy settings → **Ceilings (L0)** and set each ceiling; save (tightening applies at once; any loosening asks for Telegram approve + TOTP)
- [ ] Open D06 → Policy and walk L1 Global, L2 Venues, L3 Sleeves: keep or change each prefilled default (each field shows its default and a link to 16)
- [ ] Review D03 → Strategy settings → **Bot defaults** (deadlines, TTLs, large-order threshold, `on_system_failure`, `auto_resume_after_crash`)
- [ ] Optional: export the policy as YAML (C0) and keep a private copy outside git
- [ ] Record completion in the progress log (values summarised, no secrets) and run `./kanban done P2-T048`

## Verification

### Tests
- Agent confirms: a policy version with your values exists (`/risk/changes` shows your rows, source `web`); the L0 version is recorded; a test value above a ceiling is rejected at save.

### Scenarios
- Given the L0 ceiling says max leverage 2×, when you try 3× in D06, then save is blocked with a link to loosen the ceiling (C3).
- Given you raise the daily loss above its 3% default, when you save, then Telegram asks for approve + TOTP and the change applies after the cool-down.

### Stress / failure injection
- n/a: configuration action.

## Acceptance criteria

- [ ] Your initial values are saved as policy versions (L1–L3) and L0 ceilings are set in the strategy settings
- [ ] Every value you didn't change still shows its 16 default
- [ ] Any loosening you made went through C3

## Exceptions & edge cases

- You want to change a value later: edit it in the same settings; tightening is immediate, loosening is C3.
- Telegram C3 not live yet (P2-T035 pending): loosenings wait for the break-glass `mtctl approve` + TOTP path (P0) or stay pending; tightenings work.

## Cardinal rules (do NOT)

- Do NOT set the crypto-derivatives leverage ceiling above 2× (12 §1).
- Do NOT paste values that identify accounts or secrets into the progress log.
- Do NOT commit secrets or paste them into chats/issues/logs; secrets live in the sops/age file (07 §2).
- Loosening risk, autonomous mode and mandates are C3 (Telegram approve + TOTP + cool-down); protective exits never wait for approval.

## Doc sync on completion

- `docs/16-configuration-and-safety-model.md` §2: note that defaults were reviewed (values stay as defaults; your values live in the policy versions).
- `docs/roadmap/phase-2-strategies-risk-lab.md`: tick T2.01 when all tasks mapped to it are done.

## Branch & PR

- Branch: `p2/P2-T048-user-risk-policy-ceilings` (only if a repo change results, e.g. non-secret config or manifests; secrets never go in git)
- PR title: `P2-T048: Review the prefilled defaults and set your initial risk values and L0 ceilings in the settings`
- PR checklist: no secrets in diff (gitleaks clean) · task file ticked · `./kanban done P2-T048` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (reworked: review prefilled 16 §2 defaults and set values and L0 ceilings in the settings (no host file, 17 §E); loosening C3)
