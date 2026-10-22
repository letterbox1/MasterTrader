---
id: P5-T011
kind: task
title: Phase 5 contracts: NATS subjects, mt_api commands/queries and WebSocket topics
phase: 5
type: BUILD
status: backlog
priority: high
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P5-T009, P0-T034, P0-T035, P0-T036, P1-T004]
requirements: [R5.20, R5.23, R5.15, R5.05]
roadmap_todos: [T5.28, T5.30, T5.31]
modules: [M4, M19, M22, M15]
dashboards: [D12, D13, D18]
tools: [uv]
mcp: []
env: []
services: [nats, postgres]
branch: p5/P5-T011-p5-contracts-nats-api
pr: ""
doc_sync: [docs/02-v1-architecture.md, docs/roadmap/phase-5-airdrops-wallets-curation.md]
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

# P5-T011 · Phase 5 contracts: NATS subjects, mt_api commands/queries and WebSocket topics

## Goal / expected outcome

Versioned msgspec schemas for every P5 subject and typed `mt_api` commands/queries with their confirmation levels are registered (handlers may be stubs), so the services and the UI can be built in parallel against one contract.

## Context & references

- Roadmap: R5.15, R5.20, R5.23 · ToDos T5.28, T5.30, T5.31
- NATS taxonomy: [02 §6](../../../docs/02-v1-architecture.md#6-messaging-nats) (`task.new`, `task.updated`, `wallet.{chain}.{address}.balance|transfer|approval|nonce_authority`, `treasury.depeg`, `kill.set`)
- API: [02 §7.1–7.3](../../../docs/02-v1-architecture.md#7-api-contract-mt_api) (`/airdrops`, `/airdrops/{id}`, `/airdrops/mandates`, `/airdrops/wallet`, `/tasks`, `/community`, `/wallets`, `/wallets/transfers`)
- Commands: `airdrop.add_url` C0, `airdrop.rescore` C0, `airdrop.reject` C1, `airdrop.mandate.create` C3, `airdrop.mandate.revoke` C1, `airdrop.claim.execute` C2, `wallet.revoke_approval` C2, `wallet.sweep` C2, `wallet.register` C1, `wallet.tag` C1, `task.done|skip|snooze` C0, `task.never` C1, `task.answer` C1; wallet/signer/gas limits through `risk.policy.update` (tighten C1, loosen and the first signing enable C3; 16 §2.7)
- WS topics: `airdrop`, `tasks`, `alert`, `wallet` (P5); `treasury` arrives in P6 ([02 §7.3](../../../docs/02-v1-architecture.md#73-real-time-websocket-apiv1ws); decision P5-B005)
- Task types: the canonical list in [03 M19](../../../docs/03-build-spec.md#m19-user-task-queue--community-curation--mt_curation) (decision P5-B004)
- Signer intents come only from the policy service (`airdrop-exec` in P5; decision P5-B003)

## Requirements

- Schemas in `packages/mt_core/schemas/` for: `airdrop.opportunity.updated`, `airdrop.decision`, `airdrop.claim.result`, `task.new`, `task.updated`, `wallet.*` events, `signer.intent` (internal), `costgate.quote`, `sweep.result`, `monitor.event` (depeg/exploit/venue/bridge/concentration).
- Command registry entries with C-level, idempotency, `audit.command` writes and problem+json errors (P0 framework).
- Never-offered commands (connect wallet, sign permit, approve unknown contract, social automation) are **absent** from the registry and rejected with a specific problem type if called by name.
- WS topics `airdrop`, `tasks`, `wallet` and `alert` (02 §7.3) fanned out with ≤ 1 Hz throttling in tables; envelope `{topic, seq, ts, data}`.
- OpenAPI regenerated and versioned.
- Task `type` enum = the canonical 03 M19 list (incl. `REG_CHANGE`); no aliases (`TAX_RECORD` is retired).

## ToDo

- [ ] Define msgspec structs and subject constants; add schema version fields.
- [ ] Register commands and queries in `mt_api` with stub handlers returning 501 until the owning task lands.
- [ ] Add a `NeverAutomated` problem type and a denylist of command names (shared with P5-T042).
- [ ] Add WS topics with throttling (`wallet`, `alert` as listed in 02 §7.3).
- [ ] Contract tests: schema round-trip; each command's C-level enforced; OpenAPI snapshot.
- [ ] Update 02 §6/§7 tables.

## Verification

### Tests
- Unit: msgspec encode/decode round-trip for every schema; backward-compat test (v1 payload accepted by v1.1 decoder).
- Integration: calling `airdrop.mandate.create` without Telegram approve + TOTP never applies (C3), reusing the P0 confirmation tests.
- Snapshot: OpenAPI diff reviewed.

### Scenarios
- Given a client calls `wallet.sign_permit`, when the request arrives, then it gets problem+json `never-automated` and an `audit.command` row with outcome rejected.

### Stress / failure injection
- WS fan-out: 200 `airdrop` updates/s are throttled to ≤ 1 Hz per table subscription without dropping the latest state.

## Acceptance criteria

- [ ] All P5 subjects and commands registered with correct C-levels
- [ ] Never-offered commands rejected with a typed error
- [ ] Contract tests green

## Exceptions & edge cases

- mt-api down: services keep publishing to NATS; UI re-syncs via REST on `seq` gap.

## Cardinal rules (do NOT)

- Do NOT expose mandates, keys or withdrawals to the future MCP surface (02 §7.4).
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order goes through M11, and until the P7 live gates pass, disposal sales are manual USER tasks (never automated).
- Do NOT apply loosening (new mandate, higher caps, autonomous claims) without C3 (Telegram approve + TOTP + cool-down); protective actions (revoke, sweep, kill) never wait for approval.
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.

## Doc sync on completion

- `docs/02-v1-architecture.md` §6 and §7: add the new subjects and any command names introduced (the `wallet` and `alert` topics are already listed).
- `docs/roadmap/phase-5-airdrops-wallets-curation.md`: tick T5.28, T5.30, T5.31 when this lands (with the other tasks sharing that ToDo).

## Branch & PR

- Branch: `p5/P5-T011-p5-contracts-nats-api`
- PR title: `P5-T011: Phase 5 contracts: NATS subjects, mt_api commands/queries and WebSocket topics`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P5-T011` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (WS topics per 02 §7.3/P5-B005; canonical task types per P5-B004; limits via risk.policy.update; P0/P1 contract deps added)
