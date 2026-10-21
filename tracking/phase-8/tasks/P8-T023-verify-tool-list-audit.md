---
id: P8-T023
kind: task
title: "Tool-list and thin-adapter audit: no withdrawal, key or mandate tool exists"
phase: 8
type: VERIFY
status: backlog
priority: critical
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P8-T004, P8-T008, P8-T009, P8-T010, P8-T011, P8-T012, P8-T013]
requirements: [R8.06, R8.01]
roadmap_todos: [T8.61]
modules: [M20]
dashboards: [D17]
branch: p8/P8-T023-verify-tool-list-audit
pr: ""
doc_sync: [docs/roadmap/phase-8-mcp.md, docs/03-build-spec.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P8-T023 · Tool-list and thin-adapter audit: no withdrawal, key or mandate tool exists

## Goal / expected outcome

A CI job proves R8.06 ("Tool list audit") and supports R8.01 ("Code review"). With every enableable tool switched on, the served tool list contains nothing that withdraws, manages keys, signs or creates mandates, approves, or administers MCP. `mt_mcp` is shown to be a thin adapter.

## Context & references

- Roadmap: [R8.06, R8.01](../../../docs/roadmap/phase-8-mcp.md#3-requirements) · ToDo [T8.61](../../../docs/roadmap/phase-8-mcp.md#4-todo-sets)
- Spec: [03 M20 never exposed](../../../docs/03-build-spec.md#m20-mcp-control-plane--mt_mcp-built-last-phase-8-only-if-wanted) · [02 §7.4](../../../docs/02-v1-architecture.md#74-telegram--mcp)
- Related: P8-T004 (registry), P8-T003 (import-linter contract), gaps P8-B001, P8-B005.

## Requirements

- Start mt_api + `mt_mcp` with a full-scope token and every non-never tool enabled; dump `tools/list`.
- Assert no tool name, description or input schema matches the deny patterns: `withdraw`, `transfer`, `sweep`, `key`, `secret`, `mandate`, `sign`, `approve`, `mcp_`, `token`, `password`, `totp`, `restore`, `service_restart`, `memory_delete`, `claim_execute`, `treasury_`.
- Assert the never set in `registry.yaml` equals the code constant, and `mcp.tool.set` on each never tool → 409.
- Compare the dump with the committed `tools.snapshot.json`; CI fails on unreviewed differences.
- Thin adapter: import-linter contract green; grep shows no SQL, NATS or broker client in `mt_mcp`; reviewer checklist (one call per tool, no branching on business fields) signed in the PR.

## ToDo

- [ ] Write `tests/security/test_mcp_tool_list.py`.
- [ ] Add the code-review checklist to the PR template section for `mt_mcp`.
- [ ] Run and record.
- [ ] Doc sync.

## Verification

### Tests
- The audit suite; a planted fake `wallet_sweep` tool in a test registry makes it fail (proves it bites).

### Scenarios
- Given a future PR adds `/system/keys/rotate`, when CI runs, then registry completeness and the tool-list audit both fail until it is classified never.

### Stress / failure injection
- n/a: static/list audit; runtime abuse is covered by P8-T021.

## Acceptance criteria

- [ ] Tool list free of never-exposed capabilities with everything enabled
- [ ] Planted-tool check proves the audit bites
- [ ] Thin-adapter review recorded
- [ ] CI green (lint, types, tests, `pit` check)

## Exceptions & edge cases

- A legit tool name collides with a deny pattern (e.g. `get_keyword_stats`): add a reviewed, exact-name allow-list entry, never a broad exception.

## Cardinal rules (do NOT)

- Do NOT weaken deny patterns to get green.
- Do NOT expose withdrawals, API-key management or wallet mandate signing through MCP, in any form (R8.06).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code (including the MCP SDK).

## Doc sync on completion

- `docs/roadmap/phase-8-mcp.md`: tick T8.61.
- `docs/03-build-spec.md` M20: link to the audit.

## Branch & PR

- Branch: `p8/P8-T023-verify-tool-list-audit`
- PR title: `P8-T023: Tool-list and thin-adapter audit: no withdrawal, key or mandate tool exists`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P8-T023` run

## Progress log

- 2026-10-21 00:00 · planner · created
