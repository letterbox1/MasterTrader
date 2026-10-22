---
id: P2-T043
kind: task
title: D06 policy editor, Events and Changes tabs with DiffView and C3Flow
phase: 2
type: BUILD
status: backlog
priority: critical
size: L
severity: ""
owner: agent
claimed_by: ""
depends_on: [P2-T042, P2-T019, P2-T011, P2-T069]
requirements: [R2.50, R2.19, R2.11, R2.55, R2.57]
roadmap_todos: [T2.32, T2.38]
modules: [M15, M11]
dashboards: [D06, D03]
tools: [pnpm]
mcp: []
env: []
services: []
branch: p2/P2-T043-d06-policy-editor-events-changes
pr: ""
doc_sync: [docs/ui/dashboards/D06-risk.md, docs/ui/dashboards/D03-strategies.md, docs/ui/components.md, docs/roadmap/phase-2-strategies-risk-lab.md]
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

# P2-T043 · D06 policy editor, Events and Changes tabs with DiffView and C3Flow

## Goal / expected outcome

You edit the risk policy at every layer (L1–L4 in D06; L0 ceilings, bot defaults and the gate profile on the D03 `/strategies/settings` page) with the effective value, its layer, the L0 ceiling and the 16 default visible, save through a `DiffView` that tags each change tighten/loosen, complete loosenings via `C3Flow`, browse risk events, roll back any version from the Changes tab, and see the Stress tab as a **placeholder** ("arrives in P7").

## Context & references

- Roadmap: [R2.50, R2.19, R2.11](../../../docs/roadmap/phase-2-strategies-risk-lab.md) · ToDo T2.32
- UI: [D06 Policy/Events/Changes tabs](../../../docs/ui/dashboards/D06-risk.md) · [components DiffView, C3Flow, ParamForm](../../../docs/ui/components.md) · [ui §3.3](../../../docs/ui/README.md#33-actions--confirmation)
- Roadmap: Stress tab placeholder [R2.57](../../../docs/roadmap/phase-2-strategies-risk-lab.md) · ToDo **T2.38** (the shock replay and `risk.stress.run` are P7 R7.16 / T7.27)
- UI: [D03 `/strategies/settings`](../../../docs/ui/dashboards/D03-strategies.md#strategiessettings-strategy-settings-and-hard-ceilings) (Ceilings L0, Bot defaults L4, Gate profile) · [ui §3.7 settings show defaults and layer](../../../docs/ui/README.md#37-settings-show-configurable-defaults-and-their-layer)
- Decisions: [16 §1](../../../docs/16-configuration-and-safety-model.md#1-configuration-layers-tighten-only-inheritance) (layers, strictest wins, save-time validation) · [17 §E](../../../docs/17-decisions-register.md#e-ratification-2026-10-22) (ceilings edited in the strategy settings) · [17 §D P2-B013](../../../docs/17-decisions-register.md#d-other-decisions) (Stress tab placeholder in P2).
- Related: P2-T019 classifier (server), P2-T011 L0 API, P2-T069 effective-limits API, P2-T053 C3 tests.

## Requirements

- Policy tree mapped to the layers (D06 Policy tab): Hard ceilings (L0, shown with an "Edit ceilings" link to D03 settings), Global (L1), Venues/accounts (L2), Sleeves (L3), Bots (L4, read-through; edited in D03 Bots), Instruments/asset classes, Portfolio, Sizing defaults, Data freshness, Blackouts, Dead-man/kill config (watchdog timers, `on_system_failure`, `auto_resume_after_crash`, venue cancel-after timers); select on phones.
- Each field (`SettingField`): effective value + `LayerBadge` (strictest across layers), the L0 ceiling, the 16 §2 default with a link ("Default: 3% of sleeve"), inheritance with override toggle, help text; `NumberInput` decimal, sliders for leverage/risk %.
- D03 `/strategies/settings` page: Ceilings (L0; tighten C1, loosen C3), Bot defaults (L4: decision deadlines, HITL TTLs, large-order threshold, `on_system_failure`, `auto_resume_after_crash`, stale thresholds), Gate profile (defaults per strategy class; loosening C3), all through the same form generator, `DiffView` and `C3Flow`.
- Save-time validation messages from the server shown inline (e.g. sleeve de-risk drawdown ≥ halt drawdown → rejected with the reason).
- Save → `DiffView` (tighten mint / loosen flare) → only tightenings C1; any loosening C3 (`C3Flow`: Telegram approve + TOTP → cool-down → applied); above ceiling blocked with explanation. Pending C3 changes listed at top with countdown + Cancel.
- YAML export (C0) / import (same diff + C3 path).
- Events tab: `DataTable` of `risk.event` (time, type, scope, rule, observed vs limit, action, related order/strategy; expand → context + audit hash; filters).
- Changes tab: `risk.change` (who/source, when, diff, classification, status, hash) + Rollback (new change through the same rules).
- Stress tab: **placeholder** empty state "Stress tests aren't available yet (arrives in P7)", never sample numbers; `risk.stress.run` button hidden/disabled (D06 acceptance 6).

## ToDo

- [ ] Routes `apps/web/src/routes/risk/{policy,events,changes,stress}.tsx` (stress = placeholder) and `apps/web/src/routes/strategies/settings.tsx`
- [ ] `DiffView`, `C3Flow` components
- [ ] Policy form generator from the policy JSON Schema
- [ ] Playwright flows
- [ ] Update the docs listed under *Doc sync on completion* and tick the roadmap ToDo box(es) once every task mapped to them is done

## Verification

### Tests
- Playwright: tighten applies immediately; loosen shows C3Flow and does not apply until server says applied (D06 acceptance 1, UI side).
- API-level test (shared with P2-T053): crafted request bypassing the UI still classified server-side.
- Component: ceiling lock on every field (D06 acceptance 2).

### Scenarios
- Given you raise max leverage above the ceiling, when you save, then save is blocked with 'above hard ceiling (2×)' and a link to loosen the ceiling itself (C3) in D03 settings.
- Given you open the Stress tab, when it renders, then it shows the "arrives in P7" empty state and no sample results.
- Given you lower the L0 max daily loss in D03 settings, when you save, then it applies immediately (C1) and D06 shows the new ceiling on the affected fields.
- Given a pending loosen, when you tap Cancel, then status becomes cancelled in Changes.

### Stress / failure injection
- Policy with 200 strategies: tree virtualised; diff of 500 fields renders < 500 ms.

## Acceptance criteria

- [ ] Editor covers every layer with effective value, layer badge, ceiling, default link and inheritance; D03 settings page live
- [ ] Stress tab placeholder present (R2.57)
- [ ] Classification shown and enforced server-side
- [ ] Events + Changes + Rollback working
- [ ] CI green: ruff, mypy, pytest (and the `mt_risk` golden suite, `pit` check, viewport matrix where relevant)

## Exceptions & edge cases

- Policy changed elsewhere while editing: 409 → reload diff on top of the new version.
- Telegram unavailable: loosen stays pending with a clear message.

## Cardinal rules (do NOT)

- Do NOT apply loosenings client-side or optimistically.
- Do NOT render ceilings as editable in D06 (they are edited only in the D03 settings Ceilings section, through C1/C3).
- Do NOT show sample stress results in the placeholder.
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order goes through M11, whatever its source.
- Do NOT commit secrets or paste them into chats/issues/logs; secrets live in the sops/age file (07 §2).
- Do NOT skip, weaken or delete a test to get green; risk-manager golden tests are mandatory for merge.
- Loosening risk, autonomous mode and mandates are C3 (Telegram approve + TOTP + cool-down); protective exits never wait for approval.

## Doc sync on completion

- `docs/ui/dashboards/D06-risk.md`: tabs as built (Stress placeholder).
- `docs/ui/dashboards/D03-strategies.md`: `/strategies/settings` as built.
- `docs/ui/components.md`: DiffView/C3Flow props.
- `docs/roadmap/phase-2-strategies-risk-lab.md`: tick T2.32 and T2.38 when all tasks mapped to them are done.

## Branch & PR

- Branch: `p2/P2-T043-d06-policy-editor-events-changes`
- PR title: `P2-T043: D06 policy editor, Events and Changes tabs with DiffView and C3Flow`
- PR checklist: tests added and green · docs synced · task file ticked · no secrets (gitleaks) · `./kanban done P2-T043` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (layered policy editor (effective value, layer, ceiling, default), D03 settings page (L0 ceilings, bot defaults, gate profile), Stress tab placeholder (R2.57/T2.38))
