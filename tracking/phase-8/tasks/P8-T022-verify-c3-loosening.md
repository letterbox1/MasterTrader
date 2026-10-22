---
id: P8-T022
kind: task
title: "C3 tests: every loosening reachable from MCP needs Telegram + TOTP + cool-down; MCP tightening (L0 included) is instant"
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
tools: [uv, docker, git]
mcp: []
env: []
services: [postgres, nats]
branch: p8/P8-T022-verify-c3-loosening
pr: ""
doc_sync: [docs/roadmap/phase-8-mcp.md]
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

# P8-T022 · C3 tests: every loosening reachable from MCP needs Telegram + TOTP + cool-down; MCP tightening (L0 included) is instant

## Goal / expected outcome

Tests (`tests/security/test_mcp_c3.py`) prove the R8.05 "C3 tests" and T8.60's loosening half: loosening is never an MCP scope; every loosening reachable from MCP (any layer, L0 hard ceilings included) is applied only after your Telegram approve + TOTP and the cool-down, out of band; MCP tightening applies instantly. Fake Telegram + TOTP harness and an injected clock; no keys.

## Context & references

- Roadmap: [R8.05](../../../docs/roadmap/phase-8-mcp.md#3-requirements) · ToDo [T8.60](../../../docs/roadmap/phase-8-mcp.md#4-todo-sets)
- Spec: [07 §6](../../../docs/07-security-notes.md#6-application-controls) · [02 §7.2 C3](../../../docs/02-v1-architecture.md#72-commands-rest-write) · [02 F5](../../../docs/02-v1-architecture.md#8-end-to-end-flows) · [15 §1.2](../../../docs/15-bots-hitl-and-worm-audit.md#1-trading-bots)
- Decisions: [16 §1](../../../docs/16-configuration-and-safety-model.md#1-configuration-layers-tighten-only-inheritance) (tighten immediate, loosen C3, every layer) · [17 §E](../../../docs/17-decisions-register.md#e-ratification-2026-10-22) (L0 ceilings in the bot strategy settings, loosening C3) · [16 §2.3](../../../docs/16-configuration-and-safety-model.md#23-decisions-approvals-and-hitl) (cool-down 15 min) · [16 §2.12](../../../docs/16-configuration-and-safety-model.md#212-mcp-phase-8) (loosening never a scope)
- Precedent: P2-T053 (change-control C3 and hard-ceilings tests).

## Requirements

- Loosening paths covered: `risk.policy.update` loosen fields on each layer L0–L4; `risk.kill.off`; `strategy.set_mode` allow `autonomous`; `strategy.promote` to the autonomous stage; `bot.set_mode autonomous`; `bot.update_scope` / `bot.update_params` loosening (incl. widening an autonomous bot's scope); `bot.approval_policy.set` loosen; `strategy.update_params` that increases risk.
- Each case: no Telegram approval → not applied; approval without TOTP → not applied; wrong TOTP ×3 → locked + alert; correct TOTP → applied only after the cool-down (default 15 min, using an injected clock); cancel during cool-down works.
- L0 hard ceilings: tightening from MCP applies instantly; loosening from MCP follows the same C3 path; a value that would exceed the effective L0 on a lower layer is rejected at save time (16 §1 validation).
- No token scope, policy setting or tool flag makes any of these C1 (scope matrix test).
- MCP can't call `mcp.policy.set` / `mcp.tool.set` / `mcp.token.create` / `approval.*` at all (never exposed).

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
- [ ] L0 tightening instant; L0 loosening C3; values above a parent layer rejected at save time
- [ ] CI green (lint, types, tests, `pit` check)

## Exceptions & edge cases

- Clock jump during cool-down (NTP step): the cool-down uses monotonic time + DB timestamp; the test covers it.

## Cardinal rules (do NOT)

- Do NOT shorten cool-downs in production config to make tests fast; inject the clock.
- Do NOT make loosening risk, autonomous mode, mandates or kill-switch OFF anything less than C3 (Telegram + TOTP + cool-down); protective exits never wait for approval.
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.

## Doc sync on completion

- `docs/roadmap/phase-8-mcp.md`: R8.05 verified (link to CI run).

## Branch & PR

- Branch: `p8/P8-T022-verify-c3-loosening`
- PR title: `P8-T022: C3 tests: every loosening reachable from MCP needs Telegram + TOTP + cool-down; MCP tightening (L0 included) is instant`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P8-T022` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (hard-ceilings file replaced by L0 in settings (17 §E): L0 tighten instant, loosen C3; loosening never a scope; path list per 02 §7.2; tools/env/services)
