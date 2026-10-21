---
id: P8-T007
kind: task
title: "MCP call audit: `audit.command` source=mcp and WORM `audit.mcp_call` session log"
phase: 8
type: BUILD
status: backlog
priority: critical
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P8-T002, P8-B012]
requirements: [R8.07]
roadmap_todos: [T8.20, T8.22]
modules: [M17, M20]
dashboards: [D17, D16]
branch: p8/P8-T007-mcp-call-audit
pr: ""
doc_sync: [docs/02-v1-architecture.md, docs/03-build-spec.md, docs/15-bots-hitl-and-worm-audit.md, docs/ui/dashboards/D16-system.md, docs/roadmap/phase-8-mcp.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P8-T007 · MCP call audit: `audit.command` source=mcp and WORM `audit.mcp_call` session log

## Goal / expected outcome

Every MCP tool call, reads included, leaves a tamper-evident trail. Commands are written to `audit.command` with `source = mcp`, `token_id` and session id. Every call (query or command, allowed or denied) is written to a new WORM table `audit.mcp_call` linked to the command row. `/audit/log?source=mcp` serves D17 and D16.

## Context & references

- Roadmap: [R8.07](../../../docs/roadmap/phase-8-mcp.md#3-requirements) · ToDos [T8.20, T8.22](../../../docs/roadmap/phase-8-mcp.md#4-todo-sets)
- Spec: [03 M17](../../../docs/03-build-spec.md#m17-observability--audit--mt_obs) (every `mt_api` command audited) · [02 §7.2](../../../docs/02-v1-architecture.md#72-commands-rest-write) (`audit.command` with source)
- WORM: [15 §2](../../../docs/15-bots-hitl-and-worm-audit.md#2-worm-records-write-once-read-many) (layers and the §2.4 test suite required for every new WORM table)
- UI: [D17 Session activity](../../../docs/ui/dashboards/D17-mcp-console.md) · [D16 Audit](../../../docs/ui/dashboards/D16-system.md)
- Cross-phase: P0 R0.07 / T0.23 (WORM layer, hash chain, daily Merkle seal, `audit.verify`), R0.08 (`audit.command`).
- Gap: P8-B012 (read calls have no audit home in the docs).

## Requirements

- `audit.mcp_call` columns: `id, ts, mcp_session_id, token_id, client_label, tool, kind (query|command), args_redacted (jsonb), args_hash (sha256 of canonical raw args), result_status (ok|error|pending_approval|rejected|expired|rate_limited|denied), result_summary (≤ 500 chars), linked_command_id, latency_ms, prev_hash, row_hash`.
- WORM like R0.07: owned by offline `worm_owner`; mt_api role has INSERT/SELECT only; UPDATE/DELETE/TRUNCATE blocked by triggers; per-row hash chain; included in the daily Merkle seal; retention ≥ 7 years.
- Denied calls (never-exposed, disabled, scope missing, rate limited) are recorded too, with `token_id` when known.
- Fail closed: if the audit insert fails, the command isn't executed and the read returns 503.
- Queries: `/audit/log?source=mcp&session=&tool=` (cursor), `/mcp/sessions` (session list with call counts, first/last seen). Also add `source=` filters on `/orders` and `/risk/changes` if P2 didn't (D17 contract).
- Approval outcomes (approved / rejected / expired, by whom) link back to the originating `audit.mcp_call` row via `linked_command_id`.

## ToDo

- [ ] Migration for `audit.mcp_call` with WORM grants, blocking triggers and hash-chain trigger; register it with the daily seal job.
- [ ] Insert path in `McpGuard` / command bus (single transaction with the command row where applicable).
- [ ] Add `/audit/log` filters, `/mcp/sessions`, and `source=` filters on `/orders` and `/risk/changes`.
- [ ] Run the 15 §2.4 WORM test suite for the new table.
- [ ] Update docs.

## Verification

### Tests
- WORM suite (15 §2.4): UPDATE/DELETE/TRUNCATE blocked; `audit.verify` detects a tampered row in a restored copy; seal includes the table.
- Integration: one `audit.mcp_call` row per call; a command call links to exactly one `audit.command` row with `source = mcp`.
- Integration: a never-exposed attempt is recorded as `denied`; a rate-limited call as `rate_limited`.
- Unit: `args_redacted` contains no secret/PII fields; `args_hash` is stable for canonicalised args.

### Scenarios
- Given an MCP session of 5 calls, when you open D17, then all 5 appear in order with linked audit entries.
- Given Postgres refuses the insert, when Claude calls `order_place`, then nothing is executed and Claude gets 503.

### Stress / failure injection
- 200 calls/s for 5 min → no chain gaps, insert p95 < 5 ms, nightly `audit.verify` passes.

## Acceptance criteria

- [ ] Every MCP call (allowed or denied) has exactly one `audit.mcp_call` row
- [ ] WORM suite passes for `audit.mcp_call`; it is in the daily seal
- [ ] Audit failure blocks execution (fail closed)
- [ ] CI green (lint, types, tests, `pit` check)

## Exceptions & edge cases

- Postgres down: MCP is unavailable (503); there is no NATS buffering for new commands.
- Restart mid-session: the chain resumes from the last row hash; session ids survive in the client header.
- Clock step: `ts` from the DB clock (chrony-synced); ordering by id, not ts.

## Cardinal rules (do NOT)

- Do NOT store raw args that may contain secrets or PII; store the redacted copy and a hash.
- Do NOT let an audit failure be silent or execute a command without its audit row.
- Do NOT update or delete WORM rows; corrections are new rows (15 §2).
- Do NOT commit secrets or paste them into chats/issues (including into the Claude conversation); secrets live in the sops/age file (07 §2).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code (including the MCP SDK).

## Doc sync on completion

- `docs/02-v1-architecture.md` §4 (M20 owns `audit.mcp_call`) and §5.3 entities.
- `docs/03-build-spec.md` M17: MCP calls in audit.
- `docs/15-bots-hitl-and-worm-audit.md` §2.1: add `audit.mcp_call` to WORM scope.
- `docs/ui/dashboards/D16-system.md`: audit source filter includes mcp calls.
- `docs/roadmap/phase-8-mcp.md`: progress on T8.20/T8.22.

## Branch & PR

- Branch: `p8/P8-T007-mcp-call-audit`
- PR title: `P8-T007: MCP call audit: `audit.command` source=mcp and WORM `audit.mcp_call` session log`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P8-T007` run

## Progress log

- 2026-10-21 00:00 · planner · created
