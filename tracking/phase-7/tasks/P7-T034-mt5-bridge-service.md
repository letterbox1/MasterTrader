---
id: P7-T034
kind: task
title: MT5 bridge service for the Windows VPS
phase: 7
type: BUILD
status: backlog
priority: medium
size: L
severity: ""
owner: agent
claimed_by: ""
depends_on: [P7-T004]
requirements: [R7.10]
roadmap_todos: [T7.24]
modules: [M12]
dashboards: [D05, D16]
tools: [git, uv]
mcp: []
env: []
services: []
branch: p7/P7-T034-mt5-bridge-service
pr: ""
doc_sync: [docs/03-build-spec.md, docs/14-strategy-evidence-and-validation.md, docs/roadmap/phase-7-prove-and-go-live.md]
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

# P7-T034 · MT5 bridge service for the Windows VPS

## Goal / expected outcome

A small, licence-clean Python service runs next to the MT5 terminal on Windows, wraps the official `MetaTrader5` Python package and exposes a narrow, authenticated, idempotent API (orders, positions, history, ticks/bars, account) over Tailscale to the `engine`.

## Context & references

- Roadmap: [R7.10 · ToDo T7.24](../../../docs/roadmap/phase-7-prove-and-go-live.md)
- Spec: [14 §8](../../../docs/14-strategy-evidence-and-validation.md#8-mastertradingbot-integration) (MT5 Python API on a Windows VPS; no community adapter touches live money until tested in paper) · [03 M12](../../../docs/03-build-spec.md#m12-execution--mt_engine) (custom adapters; idempotent client IDs) · [07 §6](../../../docs/07-security-notes.md#6-application-controls)
- Related: P7-T004 (route choice; cancel if `ctrader` only), P7-T035 (deployment and hardening, T7.43), P7-T036 (engine adapter), P7-T051 (parity) · [07 §5.1](../../../docs/07-security-notes.md#51-optional-windows-vps-mt5-bridge) (VPS baseline, [17 §D P7-B010](../../../docs/17-decisions-register.md#d-other-decisions))

## Requirements

- API (gRPC or HTTP+JSON over Tailscale, mTLS or token from sops): `place_order`, `modify_order`, `cancel_order`, `positions`, `orders`, `deals(from,to)`, `account_info`, `symbol_info`, `ticks/bars stream`, `heartbeat`.
- Idempotency: client order id → MT5 `comment`/`magic` mapping; duplicate submits return the existing ticket.
- Safety: refuses any non-trading call (no withdrawals exist in MT5, but no account/password change, no EA install); refuses requests not from the host's tailnet identity.
- Heartbeat every 1 s to the engine; terminal disconnect reported within 2 s.
- No telemetry; pinned dependencies with hashes; packaged as a Windows service (nssm or pywin32) with auto-restart.
- Code lives in `services/mt5-bridge/` (MIT/our licence); no MasterTradingBot code copied in.

## ToDo

- [ ] Service skeleton, auth middleware, endpoint implementations over `MetaTrader5`.
- [ ] Idempotency store (SQLite on the VPS) keyed by client order id.
- [ ] Heartbeat publisher + terminal state watcher.
- [ ] Windows service packaging + `uv lock` with hashes.
- [ ] Unit tests with an MT5 API fake; an integration script for the FP Markets demo account (run in P7-T035 after deployment).
- [ ] Docs.

## Verification

### Tests
- Unit: request validation, idempotent submit, auth rejection (fake MT5).
- Integration against the MT5 API fake (keyless): place/modify/cancel round-trip; deals history matches. The demo-account run happens in P7-T035.
- Contract: OpenAPI/proto schema checked into `services/mt5-bridge/schema/`.

### Scenarios
- Given the same client order id is submitted twice, then one ticket exists.
- Given the terminal loses its broker connection, then heartbeat reports `broker_disconnected` within 2 s and the engine marks the account unconfirmed.

### Stress / failure injection
- 1,000 order round-trips against the fake in 1 h: no leaks, p95 bridge latency < 50 ms (excluding broker); kill the service mid-order → restart, idempotency prevents duplicates (repeated on demo in P7-T035).

## Acceptance criteria

- [ ] Bridge passes unit + fake-backed integration tests.
- [ ] Only tailnet-authenticated requests accepted.
- [ ] CI green (Windows job or cross-platform tests with the fake).

## Exceptions & edge cases

- MT5 terminal auto-updates: version pinned where possible; bridge reports terminal build in heartbeat.
- Weekend market close: bridge stays up; orders rejected by broker are surfaced verbatim.

## Cardinal rules (do NOT)

- Do NOT expose the bridge outside Tailscale.
- Do NOT copy MasterTradingBot source into this repo; port logic via the shared libraries.
- Do NOT commit secrets or paste them into chats, issues, PRs or logs; secrets live only in the sops/age file (07 §2).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.
- Do NOT use keys that are not trade-only, IP-locked and withdrawal-disabled; no live money before the P7 gates pass.

## Doc sync on completion

- `docs/03-build-spec.md` M12: MT5 bridge API.
- `docs/14-strategy-evidence-and-validation.md` §8: bridge status.
- `docs/roadmap/phase-7-prove-and-go-live.md`: tick T7.24 when this item is done.

## Branch & PR

- Branch: `p7/P7-T034-mt5-bridge-service`
- PR title: `P7-T034: MT5 bridge service for the Windows VPS`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P7-T034` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (build first: fake-backed tests, demo run moved to P7-T035; 07 §5.1 baseline; dep P7-T004)
