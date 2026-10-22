---
id: P8-T012
kind: task
title: "Risk tool group: view, tighten instantly (L0 included), kill on; loosening only as C3 out of band"
phase: 8
type: BUILD
status: backlog
priority: critical
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P8-T003, P8-T004, P8-T005, P8-T007, P2-T011, P2-T020, P2-T031, P2-T043]
requirements: [R8.03, R8.05]
roadmap_todos: [T8.20]
modules: [M11, M20]
dashboards: [D06, D17]
tools: [uv, docker, git]
mcp: []
env: []
services: [postgres, nats, mt-engine]
branch: p8/P8-T012-tools-risk
pr: ""
doc_sync: [docs/03-build-spec.md, docs/ui/dashboards/D17-mcp-console.md, docs/roadmap/phase-8-mcp.md]
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

# P8-T012 · Risk tool group: view, tighten instantly (L0 included), kill on; loosening only as C3 out of band

## Goal / expected outcome

Claude can view the risk policy and state, tighten limits on any layer instantly (L0 hard ceilings included) with the `risk_tighten` scope, run a stress test and turn the kill switch on. Loosening is never an MCP scope ([R8.05](../../../docs/roadmap/phase-8-mcp.md#3-requirements)): a loosening request from MCP becomes a C3 request that only you can complete, out of band, with Telegram approve + TOTP + cool-down. Tested on the paper stack with a fake Telegram + TOTP harness.

## Context & references

- Roadmap: [R8.03, R8.05](../../../docs/roadmap/phase-8-mcp.md#3-requirements) ("risk (view, tighten, loosen out-of-band, kill)") · ToDo [T8.20](../../../docs/roadmap/phase-8-mcp.md#4-todo-sets) · exit demo "tighten BTC max position to X"
- Decisions: [16 §1](../../../docs/16-configuration-and-safety-model.md#1-configuration-layers-tighten-only-inheritance) (L0–L4; tighten immediate, loosen C3) · [17 §E](../../../docs/17-decisions-register.md#e-ratification-2026-10-22) (L0 ceilings edited in the bot strategy settings, not a host file) · [16 §2.12](../../../docs/16-configuration-and-safety-model.md#212-mcp-phase-8) (`risk_tighten` scope; loosening never a scope, it's C3) · [16 §2.3](../../../docs/16-configuration-and-safety-model.md#23-decisions-approvals-and-hitl) (C3 cool-down 15 min)
- Spec: [03 M20 Risk row](../../../docs/03-build-spec.md#m20-mcp-control-plane--mt_mcp-built-last-phase-8-only-if-wanted) · [03 M11](../../../docs/03-build-spec.md#m11-risk-manager--mt_risk-built-in-user-inputs-via-uitelegram-later-mcp) · [02 §7.2 Risk row](../../../docs/02-v1-architecture.md#72-commands-rest-write) · [02 F5](../../../docs/02-v1-architecture.md#8-end-to-end-flows) ("MCP can only tighten") · [07 §6](../../../docs/07-security-notes.md#6-application-controls)
- UI: [D06 Risk](../../../docs/ui/dashboards/D06-risk.md) (Changes table shows source = mcp)
- Cross-phase (depends_on): P2-T011 (L0 hard-ceilings section in settings), P2-T020 (risk command surface), P2-T031 (kill switch), P2-T043 (D06 policy editor, Changes, C3Flow).

## Requirements

- Reads (scope `read`, C0): `get_risk_policy`, `get_risk_state`, `get_risk_events`, `get_risk_changes` (`source=` filter).
- Writes (scope `risk_tighten`, default disabled until you enable them in P8-T019):
  - `risk_policy_update` → `risk.policy.update` diff on any layer L0–L4. Each field is classified server-side: tighten → C1, applied immediately; loosen → C3 request (Telegram approve + TOTP + cool-down, completed only by you; expires if ignored). A mixed diff applies the tightening fields now and opens one C3 request for the loosening fields. The result lists each field as `applied` or `pending_c3 {approval_id, cooldown_until}`.
  - `risk_kill_on` → `risk.kill.on` (immediate, never blocked, exempt from rate limits).
  - `risk_kill_off` → `risk.kill.off`: always C3, only after the trigger condition is cleared.
  - `risk_stress_run` → `risk.stress.run` (C1).
- Not exposed to MCP: `risk.deadman.ack` (never, 02 §7.4); `risk.sleeve.restart`, `risk.capital.fund`, `risk.capital_step.approve`, `risk.review.close` (outside the 03 M20 Risk row; disabled, not enableable in v1).
- "Tighten BTC max position to X" maps to `risk_policy_update(layer=…, instrument=BTC…, field=max_position, value=X)` → applied instantly, audited (`audit.command` + `audit.mcp_call`), visible in D06 Changes with source mcp.
- Commands count as writes (default 10 writes/min per token, P8-T030).

## ToDo

- [ ] Add the registry entries (scope `risk_tighten`, disabled by default) and regenerate the snapshot.
- [ ] Make `risk.policy.update` return per-field classification for MCP (if P2 returns only an aggregate).
- [ ] Tests; update docs.

## Verification

### Tests
- Golden (F5): tighten-only diff applied on L0, L1, L3, L4; loosen-only diff → C3 pending; mixed diff → tighten fields applied now, loosen fields C3 pending.
- Integration (fake Telegram + TOTP, injected clock): a loosening from MCP is not applied without approve + TOTP; with them it applies only after the cool-down.
- Integration: `risk_kill_on` → all cancels sent < 1 s (engine metric); `risk_kill_off` → C3 pending and refused while the trigger is active.
- Integration: kill ON at the rate limit still goes through; `risk.deadman.ack` with an MCP token → 403 `tool_never_exposed`.

### Scenarios
- Given BTC max position 2.0, when Claude tightens it to 1.0, then D06 shows the change (source mcp) instantly.
- Given Claude raises daily loss from 2% to 3%, then you get a Telegram C3 card; without TOTP nothing changes; after approval it applies after the cool-down.
- Given Claude tightens an L0 ceiling, then it applies immediately.

### Stress / failure injection
- Kill ON from MCP during 100 open paper orders → all cancels sent < 1 s (02 §9.2).
- Telegram down: C3 loosening requests can't complete and expire; tightening and kill ON unaffected.

## Acceptance criteria

- [ ] Tighten instant on every layer incl. L0; every loosening (incl. kill off) is C3 out of band; kill on immediate
- [ ] Per-field outcome returned to Claude
- [ ] CI green (lint, types, tests, `pit` check)

## Exceptions & edge cases

- mt-api down: MCP can't kill; Telegram `/kill` via NATS still works (02 §9.3), and the runbook says so.
- Cool-down running when kill fires: the pending loosening is cancelled and audited.
- Policy version conflict (edited on web meanwhile): 409 with the current version; Claude must re-read.

## Cardinal rules (do NOT)

- Do NOT let any MCP scope or setting apply a loosening, turn kill off, restart a sleeve or ack the dead-man without the C3 flow (or at all, where never exposed).
- Do NOT block or delay kill ON for any reason.
- Do NOT hard-code limits; every value is a 16 setting.
- Do NOT make loosening risk, autonomous mode, mandates or kill-switch OFF anything less than C3 (Telegram + TOTP + cool-down); protective exits never wait for approval.
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order goes through M11, whatever its source.
- Do NOT update or delete WORM rows; corrections are new rows (15 §2).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.

## Doc sync on completion

- `docs/03-build-spec.md` M20: risk tool list.
- `docs/ui/dashboards/D17-mcp-console.md`: Risk group.
- `docs/roadmap/phase-8-mcp.md`: progress on T8.20.

## Branch & PR

- Branch: `p8/P8-T012-tools-risk`
- PR title: `P8-T012: Risk tool group: view, tighten instantly (L0 included), kill on; loosening only as C3 out of band`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P8-T012` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (`risk_tighten` scope; L0 ceilings now in settings (17 §E) and tightenable via MCP; loosening never a scope, always C3 out of band; read-only hard-ceilings file removed; `risk.deadman.ack` never exposed; cross-phase deps P2-T011/T020/T031/T043; tools/env/services)
