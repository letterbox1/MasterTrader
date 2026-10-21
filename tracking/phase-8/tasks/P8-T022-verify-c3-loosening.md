---
id: P8-T022
kind: task
title: "C3 tests: loosening via MCP needs Telegram + TOTP; hard ceilings unwritable"
phase: 8
type: VERIFY
status: backlog
priority: critical
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P8-T005, P8-T011, P8-T012]
requirements: [R8.05]
roadmap_todos: [T8.60]
modules: [M11, M20]
dashboards: [D06, D17]
branch: p8/P8-T022-verify-c3-loosening
pr: ""
doc_sync: [docs/roadmap/phase-8-mcp.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P8-T022 · C3 tests: loosening via MCP needs Telegram + TOTP; hard ceilings unwritable

## Goal / expected outcome

Tests (`tests/security/test_mcp_c3.py`) prove the R8.05 "C3 tests": every loosening reachable from MCP needs Telegram approve + TOTP and waits out the cool-down, and hard ceilings can't be written.

## Context & references

- Roadmap: [R8.05](../../../docs/roadmap/phase-8-mcp.md#3-requirements) · ToDo [T8.60](../../../docs/roadmap/phase-8-mcp.md#4-todo-sets)
- Spec: [07 §6](../../../docs/07-security-notes.md#6-application-controls) · [02 §7.2 C3](../../../docs/02-v1-architecture.md#72-commands-rest-write) · [02 F5](../../../docs/02-v1-architecture.md#8-end-to-end-flows) · [15 §1.2](../../../docs/15-bots-hitl-and-worm-audit.md#1-trading-bots)
- Cross-phase: P2 R2.19 / T2.24 (change control), R2.51 (C3 TOTP in Telegram).

## Requirements

- Loosening paths covered: `risk.policy.update` loosen fields; `risk.kill.off`; `strategy.set_mode autonomous`; promotion to auto; `bot.set_mode autonomous`; `bot.update_scope` widening an autonomous bot; `bot.approval_policy.set` loosen; `risk.ladder.set` up (if enabled).
- Each case: no Telegram approval → not applied; approval without TOTP → not applied; wrong TOTP ×3 → locked + alert; correct TOTP → applied only after the cool-down (default 15 min, using an injected clock); cancel during cool-down works.
- Hard ceilings: a value above the ceiling is rejected even with valid TOTP; static scan shows no route writes the file; the file is read-only in the container.
- MCP can't call `mcp.policy.set` / `mcp.tool.set` / `mcp.token.create` at all (never).

## ToDo

- [ ] Write the suite with a fake Telegram + TOTP harness and injected clock.
- [ ] Run and record.
- [ ] Doc sync.

## Verification

### Tests
- The suite (≥ 8 paths × 5 outcomes).

### Scenarios
- Given Claude asks to raise max leverage, when you ignore the card, then nothing changes and the request expires.

### Stress / failure injection
- Two concurrent C3 requests on the same field: the second is rejected as conflicting; no double apply.

## Acceptance criteria

- [ ] Every loosening path needs C3 via MCP
- [ ] Hard ceilings rejected even with TOTP; no writer exists
- [ ] CI green (lint, types, tests, `pit` check)

## Exceptions & edge cases

- Clock jump during cool-down (NTP step): the cool-down uses monotonic time + DB timestamp; the test covers it.

## Cardinal rules (do NOT)

- Do NOT shorten cool-downs in production config to make tests fast; inject the clock.
- Do NOT make loosening risk, autonomous mode, mandates or kill-switch OFF anything less than C3 (Telegram + TOTP + cool-down); protective exits never wait for approval.
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code (including the MCP SDK).

## Doc sync on completion

- `docs/roadmap/phase-8-mcp.md`: R8.05 verified (link to CI run).

## Branch & PR

- Branch: `p8/P8-T022-verify-c3-loosening`
- PR title: `P8-T022: C3 tests: loosening via MCP needs Telegram + TOTP; hard ceilings unwritable`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P8-T022` run

## Progress log

- 2026-10-21 00:00 · planner · created
