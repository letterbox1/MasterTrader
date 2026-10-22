---
id: P2-T011
kind: task
title: L0 hard-ceilings section in the strategy settings (tighten immediate, loosen C3)
phase: 2
type: BUILD
status: backlog
priority: critical
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P2-T010]
requirements: [R2.19, R2.55]
roadmap_todos: [T2.24]
modules: [M11]
dashboards: [D03, D06]
tools: [uv]
mcp: []
env: []
services: [postgres, nats]
branch: p2/P2-T011-hard-ceilings-file
pr: ""
doc_sync: [docs/03-build-spec.md, docs/ui/dashboards/D03-strategies.md, docs/roadmap/phase-2-strategies-risk-lab.md]
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

# P2-T011 · L0 hard-ceilings section in the strategy settings (tighten immediate, loosen C3)

## Goal / expected outcome

The **L0 hard ceilings** (absolute maxima such as crypto-derivatives leverage ≤ 2×, max daily loss, max per-transaction signer value) live as a versioned, WORM-recorded config layer that you edit in the **agent/bot strategy settings** (the ceilings section applies to every bot). Tightening is immediate (C1); loosening is C3 (Telegram approve + TOTP + cool-down). Every lower layer (L1–L4) and every runtime check is clamped to L0. There is **no host-only ceilings file** (17 §E ratification replaces the earlier file design).

## Context & references

- Roadmap: [R2.19](../../../docs/roadmap/phase-2-strategies-risk-lab.md) · ToDo T2.24 · layering [R2.55](../../../docs/roadmap/phase-2-strategies-risk-lab.md)
- Decisions: [16 §1 configuration layers](../../../docs/16-configuration-and-safety-model.md#1-configuration-layers-tighten-only-inheritance) (L0 row) · [17 §E ratification](../../../docs/17-decisions-register.md#e-ratification-2026-10-22) (ceilings edited in the strategy settings, loosening C3) · [16 §2.3 C3 cool-down 15 min](../../../docs/16-configuration-and-safety-model.md#23-decisions-approvals-and-hitl)
- Spec: [03 M11 change control](../../../docs/03-build-spec.md#m11-risk-manager--mt_risk-built-in-user-inputs-via-uitelegram-later-mcp) · [07 §6 application controls](../../../docs/07-security-notes.md#6-application-controls) · Flow: [02 F5](../../../docs/02-v1-architecture.md#8-end-to-end-flows) · command `risk.policy.update` (diff on any layer L0–L4, [02 §7.2](../../../docs/02-v1-architecture.md#72-commands-rest-write))
- UI: [D03 strategy settings → Ceilings (L0)](../../../docs/ui/dashboards/D03-strategies.md) (editable there) · [D06](../../../docs/ui/dashboards/D06-risk.md) shows the ceiling on every field and links to D03
- Related: P2-T010 policy store (layer rows), P2-T069 layering merge (L0 clamps everything), P2-T019 change control (classifier + C3), P2-T048 (you set the initial ceilings), P2-T053 C3 tests, P2-T043 (D06 shows ceilings).

## Requirements

- L0 schema `mt.risk-ceilings/v1` inside the policy store (P2-T010): per-field maxima mirroring lower-layer fields (e.g. `max_daily_loss_pct`, `max_leverage`, `crypto_derivatives.max_leverage` default 2 (12 §1), `sleeve.max_drawdown_halt_pct`, `per_trade.max_risk_pct`, `signer.max_per_tx_aud` placeholder for P5). Each field carries direction metadata (`tighter: lower|higher`).
- Edited only through `risk.policy.update` with `layer: L0`, from the D03 strategy settings Ceilings section (and D06 links). The server classifies the diff (P2-T019): **tightening → C1, immediate**; **loosening → C3** (Telegram approve + TOTP + cool-down, default 15 min). Every change is a new version row (WORM `risk.change`); rollback re-applies an earlier version as a new row, classified the same way.
- Save-time validation: a ceiling lower than the current effective value of a lower layer is allowed (tightening) and the lower-layer values are clamped at runtime and flagged in D06 as "above ceiling"; a lower-layer update above L0 is rejected with the reason (`ceiling_exceeded`), whatever its confirmation level.
- On load/apply: publish `risk.event{type: ceilings_applied, version, hash}` and KV `risk_state.ceilings_version`; the engine recompiles the policy (P2-T010) within 1 s.
- Missing/invalid L0 → default-deny all new orders + critical alert (protective exits still allowed).
- MCP (P8) can never loosen; `risk_tighten` scope may only tighten (16 §2.12). Telegram/web loosening always goes through C3.

## ToDo

- [ ] `packages/mt_risk/ceilings.py`: L0 model, validation, clamp helper used by the compiler and every evaluator
- [ ] Store L0 as a layer in `risk.policy` versions (P2-T010) with an install default that prefills the 16 §2 values (e.g. crypto-derivatives leverage ≤ 2×)
- [ ] Wire `risk.policy.update {layer: L0}` through the change-control classifier (P2-T019): tighten C1 immediate, loosen C3
- [ ] Expose ceilings in `/risk/policy` (value, version, who/when) for D03 Ceilings section and D06 per-field markers
- [ ] Remove/avoid any host file path for ceilings; CI guard: no code reads `/etc/mastertrader/risk-ceilings*`
- [ ] Tests
- [ ] Update the docs listed under *Doc sync on completion* and tick the roadmap ToDo box(es) once every task mapped to them is done

## Verification

### Tests
- Unit: a lower-layer value above L0 → `CeilingExceeded` at save; runtime clamp to L0 when L0 is tightened below an existing value.
- Unit: L0 missing/corrupt → `trading_allowed=false`, reason `ceilings_missing`; protective exits still pass.
- Integration: `risk.policy.update {layer: L0}` lowering max leverage → applied immediately (C1) and a `risk.change` row written; raising it → C3 pending until Telegram approve + TOTP + cool-down, then applied.
- WORM: UPDATE/DELETE on L0 version rows and `risk.change` fails for app roles.

### Scenarios
- Given the L0 ceiling crypto-derivatives leverage 2×, when an L2 venue update sets 3×, then it is rejected `ceiling_exceeded` even with C3 (raise L0 first, itself C3).
- Given you lower the L0 max daily loss below a sleeve's daily loss, when applied, then checks clamp to the new ceiling immediately and D06 flags the sleeve field as above ceiling.
- Given you raise the L0 max daily loss from the D03 settings, when you confirm, then the change waits for Telegram approve + TOTP and takes effect only after the 15 min cool-down.

### Stress / failure injection
- Apply 100 L0 versions in a row; each recompiles in < 200 ms and the order path never reads a half-applied ceiling (atomic swap).
- Kill the engine mid-apply: on restart the last fully applied version is in force.

## Acceptance criteria

- [ ] L0 is a versioned layer edited via `risk.policy.update`, tighten C1 / loosen C3, with WORM change rows
- [ ] Ceilings enforced at save time and clamped at runtime on every check
- [ ] No host-only ceilings file or path exists (CI guard)
- [ ] CI green: ruff, mypy, pytest (and the `mt_risk` golden suite, `pit` check, viewport matrix where relevant)

## Exceptions & edge cases

- Ceiling changed while orders are in flight: orders already checked are not cancelled; the next check uses the new values.
- C3 loosening pending when a kill or tightening happens: the tightening applies immediately; the pending loosening still needs its cool-down and is re-validated against the latest L0 before applying.
- Postgres down: the engine keeps the last compiled ceilings; changes are refused until the DB is back.

## Cardinal rules (do NOT)

- Do NOT add any path that loosens L0 without C3 (UI, Telegram, MCP, CLI, migration scripts).
- Do NOT reintroduce a host-only ceilings file; L0 lives in the strategy settings (17 §E).
- Do NOT hard-code ceiling numbers in code; install defaults come from 16 §2 and stay editable.
- Do NOT UPDATE or DELETE WORM rows (`risk.change`, policy versions); rollback is a new row.
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order goes through M11, whatever its source.
- Do NOT commit secrets or paste them into chats/issues/logs; secrets live in the sops/age file (07 §2).
- Do NOT skip, weaken or delete a test to get green; risk-manager golden tests are mandatory for merge.
- Loosening risk, autonomous mode and mandates are C3 (Telegram approve + TOTP + cool-down); protective exits never wait for approval.

## Doc sync on completion

- `docs/03-build-spec.md` M11: L0 ceilings schema and the edit path.
- `docs/ui/dashboards/D03-strategies.md`: Ceilings (L0) section as built.
- `docs/roadmap/phase-2-strategies-risk-lab.md`: tick T2.24 when all tasks mapped to it are done.

## Branch & PR

- Branch: `p2/P2-T011-hard-ceilings-file`
- PR title: `P2-T011: L0 hard-ceilings section in the strategy settings (tighten immediate, loosen C3)`
- PR checklist: tests added and green · docs synced · task file ticked · no secrets (gitleaks) · `./kanban done P2-T011` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (reworked: L0 ceilings are a versioned layer edited in the strategy settings (tighten C1, loosen C3) instead of a host-only file (17 §E))
