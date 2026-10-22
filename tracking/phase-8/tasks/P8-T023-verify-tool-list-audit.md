---
id: P8-T023
kind: task
title: "Tool-list and thin-adapter audit: no tool from the 16 §2.12 never-exposed list exists"
phase: 8
type: VERIFY
status: backlog
priority: critical
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P8-T004, P8-T008, P8-T009, P8-T010, P8-T011, P8-T012, P8-T013, P8-T032]
requirements: [R8.06, R8.01]
roadmap_todos: [T8.61]
modules: [M20]
dashboards: [D17]
tools: [uv, docker, git]
mcp: []
env: []
services: [postgres, nats]
branch: p8/P8-T023-verify-tool-list-audit
pr: ""
doc_sync: [docs/roadmap/phase-8-mcp.md, docs/03-build-spec.md]
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

# P8-T023 · Tool-list and thin-adapter audit: no tool from the 16 §2.12 never-exposed list exists

## Goal / expected outcome

A CI job proves R8.06 ("Tool list audit") and supports R8.01 ("Code review"). With every enableable tool switched on and a token holding every scope, the served tool list (and the resource list from P8-T032) contains nothing from the [16 §2.12](../../../docs/16-configuration-and-safety-model.md#212-mcp-phase-8) / [02 §7.4](../../../docs/02-v1-architecture.md#74-telegram--mcp) never-exposed list: withdrawals, `wallet.sweep`, `treasury.*` moves, `airdrop.claim.execute`, mandates, key/token management, `approval.*`, `mcp.*`, restore/delete, `system.service.restart`, `risk.deadman.ack`, `/system/keys`, `/system/logs`, audit writes. `mt_mcp` is shown to be a thin adapter.

## Context & references

- Roadmap: [R8.06, R8.01](../../../docs/roadmap/phase-8-mcp.md#3-requirements) · ToDo [T8.61](../../../docs/roadmap/phase-8-mcp.md#4-todo-sets)
- Spec: [03 M20 never exposed](../../../docs/03-build-spec.md#m20-mcp-control-plane--mt_mcp-built-last-phase-8-only-if-wanted) · [02 §7.4](../../../docs/02-v1-architecture.md#74-telegram--mcp)
- Decisions: [17 §A P8-B001](../../../docs/17-decisions-register.md#a-s2-items-all-resolved) · [17 §D P8-B005](../../../docs/17-decisions-register.md#d-other-decisions)
- Related: P8-T004 (registry), P8-T003 (import-linter contract).

## Requirements

- Start mt_api + `mt_mcp` with a token holding all six scopes and every non-never tool enabled; dump `tools/list` and `resources/list`.
- Assert the dump contains none of the never-exposed operations by exact command/route mapping, and no tool name, description or input schema matches the deny patterns: `withdraw`, `transfer`, `sweep`, `treasury_allocate`, `earn_enter`, `earn_exit`, `key`, `secret`, `mandate`, `sign`, `approv`, `approval_reject`, `mcp_`, `token`, `password`, `totp`, `pepper`, `restore`, `delete`, `service_restart`, `deadman_ack`, `system_logs`, `claim_execute`, `audit_ack`, `integrity_ack`.
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
- Do NOT expose anything on the 16 §2.12 never-exposed list, in any form (R8.06).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.

## Doc sync on completion

- `docs/roadmap/phase-8-mcp.md`: tick T8.61.
- `docs/03-build-spec.md` M20: link to the audit.

## Branch & PR

- Branch: `p8/P8-T023-verify-tool-list-audit`
- PR title: `P8-T023: Tool-list and thin-adapter audit: no tool from the 16 §2.12 never-exposed list exists`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P8-T023` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (audit against the full 16 §2.12 / 02 §7.4 never-exposed list incl. `approval.*`, `mcp.*`, restore/delete, audit writes; six-scope token; resources list included; dep P8-T032; dropped gap refs; tools/env/services)
