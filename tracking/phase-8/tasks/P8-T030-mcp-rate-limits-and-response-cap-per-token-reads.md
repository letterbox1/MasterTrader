---
id: P8-T030
kind: task
title: MCP rate limits and response cap (per-token reads/writes, 256 KB per result)
phase: 8
type: BUILD
status: backlog
priority: high
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P8-T004, P8-T007]
requirements: [R8.10]
roadmap_todos: [T8.21]
modules: [M20]
dashboards: [D17]
tools: [uv, docker, git]
mcp: []
env: []
services: [postgres, nats]
branch: p8/P8-T030-mcp-rate-limits-and-response-cap-per-token-reads
pr: ""
doc_sync: [docs/02-v1-architecture.md, docs/03-build-spec.md, docs/ui/dashboards/D17-mcp-console.md, docs/roadmap/phase-8-mcp.md]
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

# P8-T030 · MCP rate limits and response cap (per-token reads/writes, 256 KB per result)

## Goal / expected outcome

`mt_api` enforces the [R8.10](../../../docs/roadmap/phase-8-mcp.md#3-requirements) limits for every `source = mcp` call: by default **60 reads/min and 10 writes/min per token** and **256 KB per tool result**, all configurable ([16 §2.12](../../../docs/16-configuration-and-safety-model.md#212-mcp-phase-8)). Excess calls get a clean 429; oversized results are capped with a visible marker (and a cursor where the endpoint pages). The limits live server-side, so they hold for raw calls too. Tested on the test stack; no keys.

## Context & references

- Roadmap: [R8.10](../../../docs/roadmap/phase-8-mcp.md#3-requirements) · ToDo [T8.21](../../../docs/roadmap/phase-8-mcp.md#4-todo-sets) ("rate limits and response cap") · verified by P8-T034 (T8.65)
- Decisions: [16 §2.12](../../../docs/16-configuration-and-safety-model.md#212-mcp-phase-8) (60 reads/min, 10 writes/min per token; 256 KB per result) · [17 §C P8-B013](../../../docs/17-decisions-register.md#c-defaults-that-were-n-or-unspecified) (MCP limits are 16 defaults) · [17 §E](../../../docs/17-decisions-register.md#e-ratification-2026-10-22) (configurable values are settings)
- Spec: [03 M20 Limits](../../../docs/03-build-spec.md#m20-mcp-control-plane--mt_mcp-built-last-phase-8-only-if-wanted) · [02 §7.4 Audit](../../../docs/02-v1-architecture.md#74-telegram--mcp) · [07 §6](../../../docs/07-security-notes.md#6-application-controls)
- UI: [D17 Tool registry](../../../docs/ui/dashboards/D17-mcp-console.md) (rate limit per tool, configurable) · `mcp.policy.set` (tighten C1, loosen C3)
- Related: P8-T004 (registry marks each tool read/write), P8-T005 (`ops.mcp_policy` holds the settings), P8-T006 (guard runs before the cap), P8-T007 (`rate_limited` / `capped` audit statuses).

## Requirements

- Classification from the registry: **read** = C0 queries and previews; **write** = every command (C1–C3, incl. calls that only create an approval card). Kill ON (`risk.kill.on`) is exempt and never throttled.
- Token-bucket limiter keyed by `token_id` and class (read/write), window 1 min, state in NATS KV so restarts don't reset it; defaults 60/10 read from settings, overridable per token label via `mcp.policy.set` (lowering C1, raising C3).
- Over the limit → 429 problem+json `rate_limited` with `retry_after`; nothing executes; an `audit.mcp_call` row with status `rate_limited`; `alert.warn.mcp_rate` on sustained bursts; MCP counts toward the 07 §9 "unusual order rate" alert.
- Response cap (setting, default 256 KB) applied to the serialised tool result after the response guard: results above it are truncated at a record boundary, marked `{"capped": true, "limit_bytes": …, "next_cursor": …}` (cursor where the endpoint pages), and logged as `capped` with `result_bytes`.
- Notifications from subscriptions (P8-T032) count as neither reads nor writes but obey the same byte cap.
- Prometheus metrics `mt_api_mcp_rate_limited_total{class}`, `mt_api_mcp_result_bytes`; D17 shows current usage per token.

## ToDo

- [ ] Implement `packages/mt_api/mcp/limits.py` (token buckets in NATS KV, read/write classification from the registry, kill exemption).
- [ ] Implement the result cap with marker and cursor hand-off, after `McpResponseGuard`.
- [ ] Settings keys with 16 §2.12 defaults; `mcp.policy.set` fields for per-token overrides (tighten C1, loosen C3).
- [ ] Metrics, alert rule and D17 usage fields in `/mcp/tools` / `/mcp/tokens`.
- [ ] Tests; update docs.

## Verification

### Tests
- Unit: bucket math (60 reads then the 61st refused within the minute; refill after 60 s); write bucket separate from read bucket; kill ON never refused.
- Unit: cap at 256 KB on a 1 MB fixture: valid JSON, `capped: true`, cursor resumes at the next record.
- Integration: two tokens have independent buckets; a restart of mt_api keeps bucket state.
- Integration: raising a token's write limit via `mcp.policy.set` triggers C3; lowering applies at once.

### Scenarios
- Given a token that made 10 writes this minute, when Claude places another order, then it gets 429 with `retry_after` and no card is created.
- Given a fills query that would return 1 MB, then Claude receives 256 KB with a capped marker and a cursor.

### Stress / failure injection
- 1,000 calls/s across 20 tokens for 60 s → limiter p99 < 1 ms; no token exceeds its limit.
- NATS KV unavailable → MCP calls fail closed (503), web unaffected.

## Acceptance criteria

- [ ] Default 60 reads/min and 10 writes/min per token enforced server-side; kill ON exempt
- [ ] Results over 256 KB capped with a marker (and cursor where paged)
- [ ] Limits are settings; raising them is C3, lowering C1
- [ ] `rate_limited` and `capped` calls recorded in `audit.mcp_call`
- [ ] CI green (lint, types, tests, `pit` check)

## Exceptions & edge cases

- Clock: window based on server monotonic time; client clocks irrelevant.
- A single record larger than the cap (e.g. a long document): truncated with a marker inside the record; full text stays in the web UI.
- Approved orders released after approval don't count again against the write limit.

## Cardinal rules (do NOT)

- Do NOT implement limits only in `mt_mcp`; `mt_api` is the authority.
- Do NOT throttle or delay kill ON or protective exits.
- Do NOT hard-code the limits; they are 16 §2.12 defaults in settings.
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order goes through M11, whatever its source.
- Do NOT update or delete WORM rows; corrections are new rows (15 §2).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.

## Doc sync on completion

- `docs/02-v1-architecture.md` §7.4 and `docs/03-build-spec.md` M20: limits as built (429 shape, cap marker).
- `docs/ui/dashboards/D17-mcp-console.md`: usage fields.
- `docs/roadmap/phase-8-mcp.md`: progress on T8.21 (ticked with P8-T004, P8-T005, P8-T014).

## Branch & PR

- Branch: `p8/P8-T030-mcp-rate-limits-and-response-cap-per-token-reads`
- PR title: `P8-T030: MCP rate limits and response cap (per-token reads/writes, 256 KB per result)`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P8-T030` run

## Progress log

- 2026-10-22 00:00 · aligner · created for R8.10 / T8.21 (limits split out of P8-T005; defaults 60 reads/min, 10 writes/min per token, 256 KB per result from 16 §2.12)
