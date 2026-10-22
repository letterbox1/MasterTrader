---
id: P8-T007
kind: task
title: "MCP call audit: `audit.command` source=mcp and WORM `audit.mcp_call` for every call"
phase: 8
type: BUILD
status: backlog
priority: critical
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P8-T002, P0-T029, P0-T030, P0-T031, P0-T037, P0-T046]
requirements: [R8.07]
roadmap_todos: [T8.22, T8.24]
modules: [M17, M20]
dashboards: [D17, D16]
tools: [uv, docker, git]
mcp: []
env: []
services: [postgres, nats]
branch: p8/P8-T007-mcp-call-audit
pr: ""
doc_sync: [docs/02-v1-architecture.md, docs/03-build-spec.md, docs/15-bots-hitl-and-worm-audit.md, docs/ui/dashboards/D16-system.md, docs/roadmap/phase-8-mcp.md]
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

# P8-T007 · MCP call audit: `audit.command` source=mcp and WORM `audit.mcp_call` for every call

## Goal / expected outcome

Every MCP tool call, reads included, leaves a tamper-evident trail ([R8.07](../../../docs/roadmap/phase-8-mcp.md#3-requirements)). Commands are written to `audit.command` with `source = mcp`, `token_id` and session id. Every call (query or command, allowed or denied) is a row in the WORM table `audit.mcp_call`, linked to the command row. `/mcp/sessions`, `/audit/log?source=mcp` and the `source=` filters serve D17 and D16.

## Context & references

- Roadmap: [R8.07](../../../docs/roadmap/phase-8-mcp.md#3-requirements) · ToDos [T8.22, T8.24](../../../docs/roadmap/phase-8-mcp.md#4-todo-sets) (`audit.mcp_call` logging)
- Decisions: [17 §B P8-B007](../../../docs/17-decisions-register.md#b-cross-doc-conflicts-one-canonical-answer) (canonical singular names; source `web`/`telegram`/`mcp`/`system`) · [17 §D P8-B009/B012](../../../docs/17-decisions-register.md#d-other-decisions) (reads logged to `audit.mcp_call`; `/mcp/sessions`, `source=` filters)
- Spec: [03 M17](../../../docs/03-build-spec.md#m17-observability--audit--mt_obs) (every MCP call, reads included) · [02 §5](../../../docs/02-v1-architecture.md) (`audit` schema) · [02 §7.1](../../../docs/02-v1-architecture.md#71-queries-rest-read) (`/mcp/sessions`, `/approvals?status=&source=`, `/orders?source=`, `/audit/log?source=`) · [02 §7.4](../../../docs/02-v1-architecture.md#74-telegram--mcp)
- WORM: [15 §2](../../../docs/15-bots-hitl-and-worm-audit.md#2-worm-records-write-once-read-many) (layers, test suite) · [16 §2.11](../../../docs/16-configuration-and-safety-model.md#211-worm-integrity), [16 §3.3](../../../docs/16-configuration-and-safety-model.md#33-records-the-write-path-vs-the-integrity-check)
- UI: [D17 Session activity](../../../docs/ui/dashboards/D17-mcp-console.md) · [D16 Audit](../../../docs/ui/dashboards/D16-system.md)
- Cross-phase (depends_on): P0-T029 (WORM privileges/triggers), P0-T030 (hash chain), P0-T031 (P0 audit tables), P0-T037 (daily seal), P0-T046 (audit queries).

## Requirements

- `audit.mcp_call` columns: `id, ts, mcp_session_id, token_id, client_identity, transport (stdio|streamable_http|legacy_sse), tool, kind (query|command), args_redacted (jsonb), args_hash (sha256 of canonical raw args), result_status (ok|error|pending_approval|rejected|expired|rate_limited|denied|capped), result_bytes, result_summary (length-capped), linked_command_id, latency_ms, prev_hash, row_hash`.
- WORM like P0: owned by offline `worm_owner`; mt_api role has INSERT/SELECT only; UPDATE/DELETE/TRUNCATE blocked by triggers; per-row hash chain; in the daily externally anchored seal and `audit.verify`.
- Denied calls (never-exposed, disabled, scope missing, rate limited) are recorded too, with `token_id` when known.
- Fail closed: if the audit insert fails, the command isn't executed and the read returns 503. When Postgres is unreachable, the 16 §3.3 NATS buffer applies to existing write paths; MCP calls are refused rather than buffered.
- Queries: `/audit/log?source=mcp&session=&tool=` (cursor), `/mcp/sessions` (session list with client, token, call counts, first/last seen). Add `source=` filters on `/orders`, `/approvals` and `/risk/changes` where P2 didn't.
- Approval outcomes (approved / rejected / expired, by whom) link back to the originating `audit.mcp_call` row via `linked_command_id`.

## ToDo

- [ ] Migration for `audit.mcp_call` with WORM grants, blocking triggers and hash-chain trigger; register it with the daily seal and `audit.verify`.
- [ ] Insert path in `McpGuard` / command bus (single transaction with the command row where applicable).
- [ ] Add `/audit/log` filters, `/mcp/sessions`, and `source=` filters on `/orders`, `/approvals`, `/risk/changes`.
- [ ] Run the 15 §2.4 WORM test suite for the new table.
- [ ] Update docs.

## Verification

### Tests
- WORM suite (15 §2.4): UPDATE/DELETE/TRUNCATE blocked; `audit.verify` detects a tampered row in a restored copy; the seal includes the table.
- Integration: one `audit.mcp_call` row per call (reads included); a command call links to exactly one `audit.command` row with `source = mcp`.
- Integration: a never-exposed attempt is recorded as `denied`; a rate-limited call as `rate_limited`.
- Unit: `args_redacted` contains no secret/PII fields; `args_hash` is stable for canonicalised args.

### Scenarios
- Given an MCP session of 5 calls, when you open D17, then all 5 appear in order with linked audit entries.
- Given Postgres refuses the insert, when Claude calls `order_place`, then nothing is executed and Claude gets 503.

### Stress / failure injection
- 200 calls/s for 5 min → no chain gaps, insert p99 < 5 ms (17 §D P0-B004), nightly `audit.verify` passes.

## Acceptance criteria

- [ ] Every MCP call (allowed or denied, reads included) has exactly one `audit.mcp_call` row
- [ ] WORM suite passes for `audit.mcp_call`; it is in the daily seal
- [ ] Audit failure blocks execution (fail closed)
- [ ] `/mcp/sessions` and `source=` filters available for D17
- [ ] CI green (lint, types, tests, `pit` check)

## Exceptions & edge cases

- Postgres down: MCP is unavailable (503); no MCP call is buffered for later execution.
- Restart mid-session: the chain resumes from the last row hash; session ids survive in the client header.
- Clock step: `ts` from the DB clock (chrony-synced); ordering by id, not ts.
- Verify mismatch (`block_new_entries`, 16 §2.11): MCP reads still logged; new MCP entries rejected.

## Cardinal rules (do NOT)

- Do NOT store raw args that may contain secrets or PII; store the redacted copy and a hash.
- Do NOT let an audit failure be silent or execute a command without its audit row.
- Do NOT add any MCP-callable audit write (audit writes are never exposed).
- Do NOT update or delete WORM rows; corrections are new rows (15 §2).
- Do NOT commit secrets or paste them into chats/issues (including the Claude conversation); secrets live in the sops/age file (07 §2).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.

## Doc sync on completion

- `docs/02-v1-architecture.md` §4/§5/§7.1: confirm `audit.mcp_call` columns and queries as built.
- `docs/03-build-spec.md` M17: MCP calls in audit.
- `docs/15-bots-hitl-and-worm-audit.md` §2.1: `audit.mcp_call` in WORM scope (already listed; confirm).
- `docs/ui/dashboards/D16-system.md`: audit source filter includes MCP calls.
- `docs/roadmap/phase-8-mcp.md`: progress on T8.22/T8.24.

## Branch & PR

- Branch: `p8/P8-T007-mcp-call-audit`
- PR title: `P8-T007: MCP call audit: audit.command source=mcp and WORM audit.mcp_call for every call`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P8-T007` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (canonical `audit.mcp_call`, client identity/transport columns, `/mcp/sessions` and `source=` filters incl. `/approvals`, WORM p99 < 5 ms, 16 §2.11 behaviour; added T8.24; dropped gap dep P8-B012; cross-phase deps P0-T029/T030/T031/T037/T046; tools/env/services)
