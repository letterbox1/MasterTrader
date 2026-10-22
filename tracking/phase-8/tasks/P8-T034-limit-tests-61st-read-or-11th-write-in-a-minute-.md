---
id: P8-T034
kind: task
title: "Limit tests: 61st read or 11th write in a minute throttled; results over 256 KB capped"
phase: 8
type: VERIFY
status: backlog
priority: high
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P8-T003, P8-T030]
requirements: [R8.10]
roadmap_todos: [T8.65]
modules: [M20]
dashboards: [D17]
tools: [uv, docker, git]
mcp: []
env: []
services: [postgres, nats]
branch: p8/P8-T034-limit-tests-61st-read-or-11th-write-in-a-minute-
pr: ""
doc_sync: [docs/roadmap/phase-8-mcp.md]
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

# P8-T034 · Limit tests: 61st read or 11th write in a minute throttled; results over 256 KB capped

## Goal / expected outcome

A suite `tests/security/test_mcp_limits.py` proves T8.65 end to end through `mt_mcp` and through raw `mt_api` calls with an MCP token, using the 16 §2.12 defaults: within one minute the 61st read and the 11th write from a token are throttled (429, nothing executed, audited), kill ON is never throttled, and a tool result over 256 KB arrives capped with a marker. It also proves the limits are settings, not constants. Test stack, SDK client, injected clock; no keys.

## Context & references

- Roadmap: [R8.10](../../../docs/roadmap/phase-8-mcp.md#3-requirements) · ToDo [T8.65](../../../docs/roadmap/phase-8-mcp.md#4-todo-sets)
- Decisions: [16 §2.12](../../../docs/16-configuration-and-safety-model.md#212-mcp-phase-8) (60 reads/min, 10 writes/min per token; 256 KB per result) · [17 §C P8-B013](../../../docs/17-decisions-register.md#c-defaults-that-were-n-or-unspecified)
- Related: P8-T030 (implementation), P8-T007 (`rate_limited`/`capped` audit statuses), P8-T027 (load).

## Requirements

- Read limit: 60 read calls succeed within a minute; the 61st returns 429 `rate_limited` with `retry_after`; after the window it succeeds again.
- Write limit: 10 commands succeed (each creates its card or C1 effect); the 11th returns 429 and creates nothing (no card, no command row; one `audit.mcp_call` row with `rate_limited`).
- Independence: read and write buckets are separate; two tokens don't share buckets; a raw call skipping `mt_mcp` is counted the same.
- Kill ON: `risk.kill.on` succeeds even with the write bucket empty.
- Cap: a seeded query whose result is ~1 MB returns ≤ 256 KB with `capped: true`, `limit_bytes` and a cursor that pages the rest; the audit row has status `capped` and `result_bytes`.
- Configurability: lowering a token's write limit to 5 (C1) makes the 6th write fail; raising it above the default requires C3 (fake Telegram + TOTP harness); changing the cap setting changes the cut point.
- Results stored as CI artefacts.

## ToDo

- [ ] Write the suite (injected clock for windows; fixtures for the large result).
- [ ] Run and record results in the Progress log.
- [ ] Doc sync.

## Verification

### Tests
- The suite itself (≥ 10 cases above); plus a mutation check: forcing the limiter to allow-all makes the throttle tests fail.

### Scenarios
- Given a client in a tight loop of reads, when it passes 60 in a minute, then it is throttled and D17 shows the token's usage at the limit.
- Given Claude asks for a year of 1-minute bars, then it gets a capped result with a marker and pages with the cursor.

### Stress / failure injection
- 20 tokens hammering at 10× their limits for 5 min: no token ever exceeds its limit (count from `audit.mcp_call`), mt_api web p95 regression ≤ 10%.

## Acceptance criteria

- [ ] 61st read and 11th write in a minute throttled; kill ON never throttled
- [ ] Result over 256 KB capped with a marker and cursor
- [ ] Limits proven configurable (lower C1, raise C3)
- [ ] CI green (lint, types, tests, `pit` check)

## Exceptions & edge cases

- Window boundary: calls exactly at the minute edge are counted by server monotonic time; the test pins the clock.
- A single oversized record: capped inside the record with a marker (asserted).

## Cardinal rules (do NOT)

- Do NOT raise production limits or the cap to make tests pass; use injected settings in the test stack.
- Do NOT throttle or delay kill ON or protective exits.
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.
- Do NOT commit secrets or paste them into chats/issues (including the Claude conversation); secrets live in the sops/age file (07 §2).

## Doc sync on completion

- `docs/roadmap/phase-8-mcp.md`: tick T8.65; R8.10 verified (link to CI run).

## Branch & PR

- Branch: `p8/P8-T034-limit-tests-61st-read-or-11th-write-in-a-minute-`
- PR title: `P8-T034: Limit tests: 61st read or 11th write in a minute throttled; results over 256 KB capped`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P8-T034` run

## Progress log

- 2026-10-22 00:00 · aligner · created for R8.10 / T8.65 (16 §2.12 defaults: 60 reads/min, 10 writes/min per token, 256 KB per result; kill exemption; configurability)
