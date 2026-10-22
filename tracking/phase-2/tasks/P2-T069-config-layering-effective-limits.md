---
id: P2-T069
kind: task
title: "Config layering service: strictest-wins merge, save-time validation, effective-limits API"
phase: 2
type: BUILD
status: backlog
priority: critical
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P2-T010, P2-T011]
requirements: [R2.55, R2.11]
roadmap_todos: [T2.35]
modules: [M11]
dashboards: [D06, D03]
tools: [uv]
mcp: []
env: []
services: [postgres, nats]
branch: p2/P2-T069-config-layering-effective-limits
pr: ""
doc_sync: [docs/16-configuration-and-safety-model.md, docs/03-build-spec.md, docs/roadmap/phase-2-strategies-risk-lab.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-22
updated: 2026-10-22
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
review_result: ""
---

# P2-T069 · Config layering service: strictest-wins merge, save-time validation, effective-limits API

## Goal / expected outcome

`mt_risk.layers` merges the five configuration layers (L0 hard ceilings → L1 system → L2 venue/account → L3 sleeve → L4 bot) into one **effective** value per field and scope, where the effective value is always the **strictest** across layers; inconsistent settings are rejected at save time with the reason; and `/risk/policy` returns each effective limit with the layer that set it and its 16 default, so D06, D03 and the RiskGate all read the same merged view.

## Context & references

- Roadmap: [R2.55](../../../docs/roadmap/phase-2-strategies-risk-lab.md) · ToDo T2.35
- Decisions: [16 §1 configuration layers](../../../docs/16-configuration-and-safety-model.md#1-configuration-layers-tighten-only-inheritance) (effective = strictest; manifest values are proposals only; every change a WORM version row; save-time validation; the UI shows which layer sets each limit) · [17 §E ratification](../../../docs/17-decisions-register.md#e-ratification-2026-10-22)
- Defaults: [16 §2](../../../docs/16-configuration-and-safety-model.md#2-default-values-all-configurable) (each field carries its default and a link)
- UI consumers: [D06 Policy tab `LayerBadge`](../../../docs/ui/dashboards/D06-risk.md) · [D03 settings + bot wizard](../../../docs/ui/dashboards/D03-strategies.md) · [ui §3.7 settings show defaults and their layer](../../../docs/ui/README.md#37-settings-show-configurable-defaults-and-their-layer)
- Related: P2-T010 layer store, P2-T011 L0 ceilings, P2-T019 tighten/loosen classifier, P2-T017 RiskGate (consumes the compiled effective view), P2-T036 bot wizard (rejects proposals looser than a parent).

## Requirements

- Merge rule per field, using the field's direction metadata (`tighter: lower|higher|enable|disable`, P2-T010): effective = min/max/AND across every layer that applies to the scope (bot → its sleeve → its venue/account → system → L0). A bot can never exceed its sleeve, a sleeve its system policy, or anything L0.
- Scope resolution: (bot, instrument, venue/account, sleeve) → the applicable layer documents; asset-class values (collars) resolved through L2.
- Effective-limits API: `GET /risk/policy?scope=…` returns per field `{effective, layer, value_by_layer, default, default_ref: "16 §2.1", ceiling}`; `GET /risk/policy/effective?bot_id=…` for the D03 wizard and approval cards.
- **Save-time validation** (called by `risk.policy.update` before classification): reject with a reason when a lower layer is looser than a parent (`parent_stricter: L3 daily_loss 3% > L1 2%`), when sleeve/system drawdown stage 1 ≥ stage 2, when a per-transaction cap exceeds the 24 h cap, when a value is outside its accepted range (16 §2 brackets, e.g. venue concentration 10–30%), or above L0.
- Manifest proposals (P2-T004) are evaluated with the same function: the wizard receives `accepted|tightened|rejected_looser_than_parent` per field; nothing from a manifest is applied without the bot creation command.
- Compile: on any layer version change, recompile the flat effective tables for the engine (P2-T010 compiler) and publish `risk_state.policy_version`; the order path never merges at request time (O(1) lookups; keeps the RiskGate p99 < 1 ms).
- Every number comes from the layer documents with 16 defaults; nothing hard-coded.

## ToDo

- [ ] `packages/mt_risk/layers/merge.py` (direction-aware merge, scope resolution) and `validate.py` (save-time rules with reason codes)
- [ ] Hook validation into `risk.policy.update` and `bot.create`/`bot.update_*` before the P2-T019 classifier
- [ ] Effective-limits endpoints in `mt_api` (`/risk/policy` fields, `/risk/policy/effective`)
- [ ] Recompile + publish on version change; engine reload test
- [ ] Golden tests + property tests (see Verification)
- [ ] Update the docs listed under *Doc sync on completion* and tick the roadmap ToDo box(es) once every task mapped to them is done

## Verification

### Tests
- Golden: table of layer stacks → expected effective value and layer for every field kind (lower-is-tighter, higher-is-tighter, enable/disable).
- Property (hypothesis): for random layer stacks the effective value is never looser than any layer; changing any layer to a tighter value never loosens the effective value.
- Unit: each save-time rule rejects with its reason code (stage 1 ≥ stage 2, per-tx cap > 24 h cap, out of range, looser than parent, above L0).
- Integration: `/risk/policy` returns layer, default and the 16 reference for every field.

### Scenarios
- Given L1 daily loss 3% and a sleeve set to 2%, when a bot in that sleeve is resolved, then the effective daily loss is 2% with layer L3.
- Given you try to set a bot's risk per trade to 2% while its sleeve allows 1%, when saved, then it is rejected `parent_stricter` (not routed to C3).
- Given a manifest proposing a 5 s stale threshold for a fast bot whose L1 default is 2 s, when the bot is created, then the wizard shows 'proposal looser than parent' and keeps 2 s.

### Stress / failure injection
- Recompile 50 venues × 20 sleeves × 500 bots after a single L1 change in < 500 ms; the engine swaps atomically (no order sees a half-merged view).
- Inject a corrupt layer document: validation rejects it at save; if found at load, the engine default-denies new orders and alerts.

## Acceptance criteria

- [ ] Effective value = strictest across L0–L4 for every field (golden + property tests)
- [ ] Save-time validation rejects inconsistent settings with reasons
- [ ] `/risk/policy` shows effective value, layer, default and ceiling per field
- [ ] CI green: ruff, mypy, pytest (and the `mt_risk` golden suite)

## Exceptions & edge cases

- A parent is tightened below a child's value: the child's stored value is kept but the effective value follows the parent; D06 flags the child field 'overridden by L1'.
- Missing layer document (e.g. no sleeve config yet): the field inherits the parent; a missing L1 or L0 → default-deny.
- Postgres down: the engine keeps its last compiled view; saves are refused until the DB is back.

## Cardinal rules (do NOT)

- Do NOT let any layer, manifest or bot override loosen beyond a parent layer; loosening within limits is C3 (P2-T019).
- Do NOT merge layers on the order path; use the compiled tables.
- Do NOT hard-code limits or defaults in the merge code.
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order goes through M11, whatever its source.
- Do NOT commit secrets or paste them into chats/issues/logs; secrets live in the sops/age file outside the repo (07 §2).
- Do NOT skip, weaken or delete a test to get green; risk-manager golden tests are mandatory for merge.
- Do NOT UPDATE or DELETE WORM rows (`audit.*`, `risk.change`, `risk.approval`, `strategy.bot_version`); corrections are new rows (15 §2).
- Keys are trade-only, IP-locked, withdrawals disabled. No live money before the P7 gates; this phase is paper/testnet/practice only.
- Loosening risk, autonomous mode and mandates are C3 (Telegram approve + TOTP + cool-down); protective exits never wait for approval.

## Doc sync on completion

- `docs/16-configuration-and-safety-model.md` §1: confirm the merge and save-time validation rules as built (no value change).
- `docs/03-build-spec.md` M11: effective-limits API.
- `docs/roadmap/phase-2-strategies-risk-lab.md`: tick T2.35 when all tasks mapped to it are done.

## Branch & PR

- Branch: `p2/P2-T069-config-layering-effective-limits`
- PR title: `P2-T069: Config layering service: strictest-wins merge, save-time validation, effective-limits API`
- PR checklist: tests added and green · docs synced · task file ticked · no secrets (gitleaks) · `./kanban done P2-T069` run

## Progress log

- 2026-10-22 00:00 · aligner · created for docs/16–17 (T2.35: R2.55, R2.11)
