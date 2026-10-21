---
id: P2-T019
kind: task
title: Change-control service: tighten/loosen classifier and C3 flow
phase: 2
type: BUILD
status: backlog
priority: critical
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P2-T010, P2-T011]
requirements: [R2.19]
roadmap_todos: [T2.24]
modules: [M11]
dashboards: [D06]
branch: p2/P2-T019-change-control-service
pr: ""
doc_sync: [docs/02-v1-architecture.md, docs/07-security-notes.md, docs/roadmap/phase-2-strategies-risk-lab.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P2-T019 · Change-control service: tighten/loosen classifier and C3 flow

## Goal / expected outcome

`risk.policy.update` (and every other risk-affecting command: ladder, venue registry, strategy/bot params, approval policy, mode) is classified per field into tighten / loosen / above-ceiling; tightenings apply immediately, loosenings go through C3 (Telegram approve + TOTP + 15-min cool-down), above-ceiling is always rejected, and everything is audited and versioned.

## Context & references

- Roadmap: [R2.19](../../../docs/roadmap/phase-2-strategies-risk-lab.md) · ToDo T2.24
- Flow: [02 F5 risk policy change](../../../docs/02-v1-architecture.md#8-end-to-end-flows) · Levels: [02 §7.2](../../../docs/02-v1-architecture.md#72-commands-rest-write) · [07 §6](../../../docs/07-security-notes.md#6-application-controls)
- UI: [D06 Saving + Changes tab](../../../docs/ui/dashboards/D06-risk.md) · [ui §3.3 C3 pattern](../../../docs/ui/README.md#33-actions--confirmation)
- Cross-phase: P0 confirmation-level engine with C3 = approve + TOTP + cool-down (T0.24) — this task supplies the risk-specific classifier and pending-change store.
- Related: P2-T053 C3 tests, P2-T065 your test loosening.

## Requirements

- Classifier library `classify(diff) -> [FieldChange(path, old, new, kind: tighten|loosen|ceiling_violation)]` using direction metadata (P2-T010); a mixed diff is C3 as a whole (or split into an immediate tighten part + pending loosen part, configurable, default split).
- Loosen examples: raising a limit, enabling `autonomous`, widening a bot's scope, enabling a venue/product, ladder step up, kill off, loosening approval policy (longer TTL, higher large-order threshold).
- Pending C3 changes stored with cool-down end; cancellable (C1); applied by a timer; expired if not approved in 10 min (configurable).
- Every change writes `risk.change` (WORM): who/source (web/telegram/mcp/system), diff, classification, status (applied / pending / rejected / cancelled), policy version, approval refs.
- Rollback reuses the same path.
- Classifier is reused by P2-T006 (risk-increasing params), P2-T016, P2-T018, P2-T036/37.

## ToDo

- [ ] `packages/mt_risk/change_control.py` classifier + pending store
- [ ] Hook into the P0 confirmation engine for C3
- [ ] Cool-down scheduler (survives restart: pending rows re-armed on boot)
- [ ] `/risk/changes` query
- [ ] Tests
- [ ] Update the docs listed under *Doc sync on completion* and tick the roadmap ToDo box(es) once every task mapped to them is done

## Verification

### Tests
- Unit: every policy field classified correctly in both directions (generated from the model).
- Integration: loosen via web without Telegram approval → stays pending, never applied; with approval but wrong TOTP → rejected; correct TOTP → applied only after cool-down.
- Unit: above-ceiling rejected even with valid C3.

### Scenarios
- Given you lower daily loss 3% → 2%, when saved, then applied immediately and notified on Telegram.
- Given you raise BTC max position 0.5 → 0.8, when saved, then Telegram asks approve → TOTP → '15 min cool-down' → 'Applied'.
- Given a pending loosen, when the system restarts mid cool-down, then the timer resumes from the stored end time.

### Stress / failure injection
- Submit 50 conflicting changes concurrently: serialised by policy version (optimistic locking); no lost update; each audited.

## Acceptance criteria

- [ ] Server-side classification for all risk-affecting commands
- [ ] C3 path enforced and audited
- [ ] Ceilings always win
- [ ] CI green: ruff, mypy, pytest (and the `mt_risk` golden suite, `pit` check, viewport matrix where relevant)

## Exceptions & edge cases

- Telegram down: loosenings can't complete (by design); tightenings still apply.
- Concurrent edits: second writer gets 409 with the new version to diff against.

## Cardinal rules (do NOT)

- Do NOT trust a client-provided classification.
- Do NOT apply a loosening before its cool-down ends.
- Do NOT allow MCP or agents to approve C3.
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order goes through M11, whatever its source.
- Do NOT commit secrets or paste them into chats/issues/logs; secrets live in the sops/age file (07 §2).
- Do NOT skip, weaken or delete a test to get green; risk-manager golden tests are mandatory for merge.
- Do NOT UPDATE or DELETE WORM rows (`audit.*`, `risk.change`, `risk.approval`, `strategy.bot_version`); corrections are new rows with `supersedes_id` (15 §2).
- Loosening risk, autonomous mode and mandates are C3 (Telegram approve + TOTP + cool-down); protective exits never wait for approval.

## Doc sync on completion

- `docs/02-v1-architecture.md` F5: split-diff behaviour.
- `docs/07-security-notes.md` §6: cool-down default and expiry.
- `docs/roadmap/phase-2-strategies-risk-lab.md`: tick T2.24 when all tasks mapped to it are done.

## Branch & PR

- Branch: `p2/P2-T019-change-control-service`
- PR title: `P2-T019: Change-control service: tighten/loosen classifier and C3 flow`
- PR checklist: tests added and green · docs synced · task file ticked · no secrets (gitleaks) · `./kanban done P2-T019` run

## Progress log

- 2026-10-21 00:00 · planner · created
