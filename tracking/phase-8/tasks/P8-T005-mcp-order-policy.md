---
id: P8-T005
kind: task
title: "MCP order policy: every order creates your approval card, confirmation mapping (`mcp.policy.set`)"
phase: 8
type: BUILD
status: backlog
priority: critical
size: L
severity: ""
owner: agent
claimed_by: ""
depends_on: [P8-T004, P2-T020, P2-T033, P2-T035, P2-T038, P2-T039]
requirements: [R8.04, R8.05]
roadmap_todos: [T8.21]
modules: [M20, M11]
dashboards: [D17, D06, D05]
tools: [uv, docker, git]
mcp: []
env: []
services: [postgres, nats]
branch: p8/P8-T005-mcp-order-policy
pr: ""
doc_sync: [docs/02-v1-architecture.md, docs/03-build-spec.md, docs/07-security-notes.md, docs/15-bots-hitl-and-worm-audit.md, docs/ui/dashboards/D17-mcp-console.md, docs/roadmap/phase-8-mcp.md]
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

# P8-T005 · MCP order policy: every order creates your approval card, confirmation mapping (`mcp.policy.set`)

## Goal / expected outcome

Every MCP-sourced command is routed by a **server-side** policy in `mt_api`, exactly as [02 §7.4](../../../docs/02-v1-architecture.md#74-telegram--mcp) and [16 §2.3](../../../docs/16-configuration-and-safety-model.md#23-decisions-approvals-and-hitl) decide: C0 reads run directly; C1 runs if the token has the scope; C2 orders **always** create your approval card on Telegram/web (TTL default 5 min, expiry = reject); C3 goes through Telegram + TOTP + cool-down as usual. There is **no** "skip approval" option, MCP can never approve, and MCP can tighten risk but never apply a loosening (that is always C3, completed by you out of band). Every order still passes M11. Built and tested against paper/sandbox venues and a fake Telegram harness.

## Context & references

- Roadmap: [R8.04, R8.05](../../../docs/roadmap/phase-8-mcp.md#3-requirements) · ToDo [T8.21](../../../docs/roadmap/phase-8-mcp.md#4-todo-sets) (confirmation mapping; limits are P8-T030)
- Decisions: [17 §A P8-B002](../../../docs/17-decisions-register.md#a-s2-items-all-resolved) (C0/C1/C2/C3 mapping, TTL 5 min, no skip option; resolves P8-B010) · [17 §A P8-B001](../../../docs/17-decisions-register.md#a-s2-items-all-resolved) (MCP can never approve) · [17 §E](../../../docs/17-decisions-register.md#e-ratification-2026-10-22) (L0 ceilings in settings, loosening C3)
- Spec: [03 M20 safeguards](../../../docs/03-build-spec.md#m20-mcp-control-plane--mt_mcp-built-last-phase-8-only-if-wanted) · [SPEC NN2](../../../SPEC.md#non-negotiable-requirements) · [07 §6](../../../docs/07-security-notes.md#6-application-controls) · [16 §1 layers](../../../docs/16-configuration-and-safety-model.md#1-configuration-layers-tighten-only-inheritance) · [02 F5](../../../docs/02-v1-architecture.md#8-end-to-end-flows) ("MCP can only tighten")
- HITL rules: [15 §1.3](../../../docs/15-bots-hitl-and-worm-audit.md#13-hitl-approval-via-telegram) (MCP-originated orders always raise this card, TTL 5 min; approvals only from you, bound to your Telegram id or web session)
- UI: [D17 Actions](../../../docs/ui/dashboards/D17-mcp-console.md) (`mcp.policy.set`: tighten C1, loosen C3; no skip-approval option)
- Cross-phase (depends_on): P2-T020 (risk/order command surface), P2-T033 (modes and approval routing), P2-T035 (Telegram C3 TOTP prompt), P2-T038 (approvals API), P2-T039 (Telegram HITL cards).

## Requirements

- Mapping for `source = mcp` (implemented before command dispatch, in `mt_api`):
  - **C0** (queries, `risk.preview`, `models.tierb.ask`) → run directly.
  - **C1** → run immediately if the token has the tool's scope (e.g. `risk_tighten` tightening, `strategy` C1 edits, `curation`, `analyse` runs).
  - **C2** → every order command (`order.place`, `order.modify`, `order.cancel`, `order.cancel_all`, `position.close`, `position.reduce`, `position.set_brackets`; flatten = `position.close` with strategy scope) and any other C2 command → `pending_approval` → your approval card (Telegram + web, P8-T014). Approve within TTL or it's rejected; never executed late.
  - **C3** (e.g. `bot.set_mode autonomous`, loosening a bot's parameters or approval policy) → the standard C3 flow: Telegram approve + TOTP + cool-down (default 15 min, 16 §2.3), never shortened by MCP.
  - **Risk loosening** (loosening fields of `risk.policy.update` on any layer, `risk.kill.off`): never a scope, never applied by MCP. It always becomes a C3 request completed only by you, out of band, with Telegram approve + TOTP + cool-down; ignored requests expire. MCP may tighten, L0 ceilings included (16 §1).
  - **Kill ON** (`risk.kill.on`, scope `risk_tighten`) → immediate, never blocked.
- MCP approval TTL: default 5 min (16 §2.3), a setting; expiry = reject, logged `expired`.
- `ops.mcp_policy` (versioned rows) holds scopes allowed per client label, venue allow-list for MCP orders and the rate-limit settings used by P8-T030. **No** auto-execute or skip-approval field exists in the schema. `mcp.policy.set` (web/Telegram only, never MCP): tighten C1, loosen C3.
- M11 runs at request time (its preview goes on the card) and again at release; the order is submitted only if M11 passes at release. Venue registry, leverage caps, STP and DQ checks are unchanged.
- MCP orders book to the `manual` sleeve unless a strategy/bot is named; retries with the same `idempotency_key` yield one command; client order IDs follow the P2 rule `{bot}-{engine_epoch}-{seq}` (17 §D P2-B007).
- MCP-initiated closes/reductions are not protective exits: they wait for your card. Protective exits (entry stop/TP, kill flatten, risk-forced reductions, dead-man) are outside MCP policy and never wait.
- Approvals for MCP requests are accepted only from `web` or `telegram` sources bound to you; an `approval.*` call with an MCP token never reaches this code (P8-T004).

## ToDo

- [ ] Implement `packages/mt_api/mcp/policy.py` hooked into the confirmation engine before command dispatch.
- [ ] Migration `ops.mcp_policy`; command `mcp.policy.set` (web/Telegram only) with tighten/loosen classification; schema has no skip-approval field (test).
- [ ] Pending-approval path: reuse `risk.approval` and `risk.approval.request/result` NATS subjects; add `source = mcp`, `client_label`, `reason` to the payload (P8-T014 renders it).
- [ ] TTL expiry worker (server UTC, TTL from settings); auto-reject pending MCP approvals on Kill ON.
- [ ] Route risk-loosening fields and `risk.kill.off` from MCP into the C3 flow (never C1, whatever the scopes).
- [ ] Golden decision table `tests/golden/mcp_policy.csv` (command × level × scopes × kill state → outcome) as a mandatory-for-merge test.
- [ ] Update docs.

## Verification

### Tests
- Golden: full decision table (≥ 60 rows) incl. every order command → card, cancel → card, bracket widening → card, risk tighten → applied, risk loosen → C3 pending, kill ON → immediate, kill OFF → C3 pending, C3 bot autonomous → C3 flow.
- Integration (sandbox paper venue + fake Telegram): MCP `order.place` → pending → approve on web → M11 passes → paper fill; reject path; expiry after 5 min (injected clock) → rejected.
- Integration: M11 rejects at release (limit, DQ `stale`, venue not `allowed`) after you approved → not submitted; the card shows the reason.
- Integration: MCP `risk.kill.on` → engine cancels all in < 1 s; pending MCP approvals auto-rejected.
- Schema test: `ops.mcp_policy` and `mcp.policy.set` accept no field that could skip approval.

### Scenarios
- Given any MCP order, when Claude closes half of EURUSD, then a card appears on Telegram and web and nothing executes until you approve.
- Given you tap Approve after the TTL (5 min default), then the order is rejected as expired.
- Given Claude tries to raise max daily loss, then a C3 request goes to your Telegram; without your approve + TOTP nothing changes, and after approval it applies only after the cool-down.
- Given Claude tightens BTC max position, then it applies immediately (C1, `risk_tighten` scope).

### Stress / failure injection
- 100 MCP order requests in 60 s → rate limiting by P8-T030 applies; the ones admitted each create a card; each gets its own card (no batching or bulk approve for MCP, 15 §1.3); Telegram sends are queued within its rate limits.
- Pre-trade risk check p99 stays < 1 ms with MCP load (02 §9.2).
- Fake Telegram down: cards still on the web queue; otherwise they expire as rejects.

## Acceptance criteria

- [ ] Golden decision table green and mandatory for merge
- [ ] Every MCP order creates an approval card; there is no skip-approval option anywhere
- [ ] No MCP order reaches a venue without M11; MCP tightens instantly but every loosening is C3 out of band
- [ ] C3 flows never shortened by MCP; kill ON immediate
- [ ] TTL is a setting (default 5 min); expiry = reject
- [ ] CI green (lint, types, tests, `pit` check)

## Exceptions & edge cases

- Telegram down: approvals still possible from web (D01/D05/D17); otherwise they expire as rejects.
- mt_api restart with pending approvals: they persist in `risk.approval`; TTL runs on wall clock; expired ones are rejected on startup.
- Kill ON: trade commands rejected with `kill_on`; pending MCP approvals auto-rejected.
- DQ degraded or blackout at release time: M11 rejects; the card shows the reason.
- Unreconciled position: close/reduce rejected (D05 rule) except flatten via kill.
- WORM integrity `block_new_entries` (16 §2.11): new MCP entries rejected; exits continue.

## Cardinal rules (do NOT)

- Do NOT add any "skip approval", auto-execute or auto-rule option for MCP orders.
- Do NOT let MCP approve anything or change its own policy, tools or tokens.
- Do NOT let any setting skip M11, the venue registry, STP or DQ checks.
- Do NOT decide confirmation levels in `mt_mcp`.
- Do NOT hard-code the TTL or cool-down; they are settings with 16 §2.3 defaults.
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order goes through M11, whatever its source.
- Do NOT make loosening risk, autonomous mode, mandates or kill-switch OFF anything less than C3 (Telegram + TOTP + cool-down); protective exits never wait for approval.
- Do NOT use live money before the P7 gates; keys stay trade-only, IP-locked, withdrawals disabled.
- Do NOT update or delete WORM rows; corrections are new rows (15 §2).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.

## Doc sync on completion

- `docs/02-v1-architecture.md` §7.2 and §7.4: mapping as built.
- `docs/03-build-spec.md` M20 and `docs/07-security-notes.md` §6: confirm mapping and TTL.
- `docs/15-bots-hitl-and-worm-audit.md` §1.3/§1.5: MCP card fields.
- `docs/ui/dashboards/D17-mcp-console.md`: policy fields as built.
- `docs/roadmap/phase-8-mcp.md`: tick T8.21 when P8-T004, P8-T014 and P8-T030 are also done.

## Branch & PR

- Branch: `p8/P8-T005-mcp-order-policy`
- PR title: `P8-T005: MCP order policy: every order creates your approval card, confirmation mapping (mcp.policy.set)`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P8-T005` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (C2 orders always create your card, TTL default 5 min, auto rules and skip-approval removed, MCP never applies a loosening (always C3 out of band), L0 tightening allowed, scopes per 16 §2.12; rate limits moved to P8-T030; dropped gap dep P8-B002; cross-phase deps P2-T020/T033/T035/T038/T039; tools/env/services)
