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
depends_on: [P2-T042, P2-T019, P2-T011]
requirements: [R2.50, R2.19, R2.11]
roadmap_todos: [T2.32]
modules: [M15, M11]
dashboards: [D06]
branch: p2/P2-T043-d06-policy-editor-events-changes
pr: ""
doc_sync: [docs/ui/dashboards/D06-risk.md, docs/ui/components.md, docs/roadmap/phase-2-strategies-risk-lab.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P2-T043 · D06 policy editor, Events and Changes tabs with DiffView and C3Flow

## Goal / expected outcome

You edit the risk policy at every level in D06 with ceilings and inheritance visible, save through a `DiffView` that tags each change tighten/loosen, complete loosenings via `C3Flow`, browse risk events, and roll back any version from the Changes tab.

## Context & references

- Roadmap: [R2.50, R2.19, R2.11](../../../docs/roadmap/phase-2-strategies-risk-lab.md) · ToDo T2.32
- UI: [D06 Policy/Events/Changes tabs](../../../docs/ui/dashboards/D06-risk.md) · [components DiffView, C3Flow, ParamForm](../../../docs/ui/components.md) · [ui §3.3](../../../docs/ui/README.md#33-actions--confirmation)
- Related: P2-T019 classifier (server), P2-T053 C3 tests, P2-B013 (Stress tab not in roadmap).

## Requirements

- Policy tree: Global, Venues/accounts, Strategies, Instruments/asset classes, Portfolio, Sizing defaults, Blackouts, Dead-man/kill config, Sleeves (select on phones).
- Each field: current value, hard ceiling (read-only, lock icon), inheritance with override toggle, help text; `NumberInput` decimal, sliders for leverage/risk %.
- Save → `DiffView` (tighten mint / loosen flare) → only tightenings C1; any loosening C3 (`C3Flow`: Telegram approve + TOTP → cool-down → applied); above ceiling blocked with explanation. Pending C3 changes listed at top with countdown + Cancel.
- YAML export (C0) / import (same diff + C3 path).
- Events tab: `DataTable` of `risk.event` (time, type, scope, rule, observed vs limit, action, related order/strategy; expand → context + audit hash; filters).
- Changes tab: `risk.change` (who/source, when, diff, classification, status, hash) + Rollback (new change through the same rules).
- Stress tab: placeholder 'not in Phase 2' (see P2-B013).

## ToDo

- [ ] Routes `apps/web/src/routes/risk/{policy,events,changes}.tsx`
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
- Given you raise max leverage above the ceiling, when you save, then save is blocked with 'above hard ceiling (2×)'.
- Given a pending loosen, when you tap Cancel, then status becomes cancelled in Changes.

### Stress / failure injection
- Policy with 200 strategies: tree virtualised; diff of 500 fields renders < 500 ms.

## Acceptance criteria

- [ ] Editor covers every policy level with ceilings + inheritance
- [ ] Classification shown and enforced server-side
- [ ] Events + Changes + Rollback working
- [ ] CI green: ruff, mypy, pytest (and the `mt_risk` golden suite, `pit` check, viewport matrix where relevant)

## Exceptions & edge cases

- Policy changed elsewhere while editing: 409 → reload diff on top of the new version.
- Telegram unavailable: loosen stays pending with a clear message.

## Cardinal rules (do NOT)

- Do NOT apply loosenings client-side or optimistically.
- Do NOT render ceilings as editable.
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order goes through M11, whatever its source.
- Do NOT commit secrets or paste them into chats/issues/logs; secrets live in the sops/age file (07 §2).
- Do NOT skip, weaken or delete a test to get green; risk-manager golden tests are mandatory for merge.
- Loosening risk, autonomous mode and mandates are C3 (Telegram approve + TOTP + cool-down); protective exits never wait for approval.

## Doc sync on completion

- `docs/ui/dashboards/D06-risk.md`: tabs as built.
- `docs/ui/components.md`: DiffView/C3Flow props.
- `docs/roadmap/phase-2-strategies-risk-lab.md`: tick T2.32 when all tasks mapped to it are done.

## Branch & PR

- Branch: `p2/P2-T043-d06-policy-editor-events-changes`
- PR title: `P2-T043: D06 policy editor, Events and Changes tabs with DiffView and C3Flow`
- PR checklist: tests added and green · docs synced · task file ticked · no secrets (gitleaks) · `./kanban done P2-T043` run

## Progress log

- 2026-10-21 00:00 · planner · created
