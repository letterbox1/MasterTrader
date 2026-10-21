---
id: P8-T012
kind: task
title: "Risk tool group: view, tighten instantly, loosen via C3, kill switch"
phase: 8
type: BUILD
status: backlog
priority: critical
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P8-T003, P8-T004, P8-T005, P8-T007]
requirements: [R8.03, R8.05]
roadmap_todos: [T8.20]
modules: [M11, M20]
dashboards: [D06, D17]
branch: p8/P8-T012-tools-risk
pr: ""
doc_sync: [docs/03-build-spec.md, docs/ui/dashboards/D17-mcp-console.md, docs/roadmap/phase-8-mcp.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P8-T012 · Risk tool group: view, tighten instantly, loosen via C3, kill switch

## Goal / expected outcome

Claude can view the risk policy and state, tighten limits instantly, request loosening (which goes out of band to Telegram + TOTP + cool-down), run a stress test and turn the kill switch on. Hard ceilings can't be written by anything.

## Context & references

- Roadmap: [R8.03, R8.05](../../../docs/roadmap/phase-8-mcp.md#3-requirements) · ToDo [T8.20](../../../docs/roadmap/phase-8-mcp.md#4-todo-sets) · exit demo "tighten BTC max position to X"
- Spec: [03 M20 Risk row](../../../docs/03-build-spec.md#m20-mcp-control-plane--mt_mcp-built-last-phase-8-only-if-wanted) · [03 M11](../../../docs/03-build-spec.md#m11-risk-manager--mt_risk-built-in-user-inputs-via-uitelegram-later-mcp) · [02 F5, F6](../../../docs/02-v1-architecture.md#8-end-to-end-flows) · [07 §6 risk limits via any front-end](../../../docs/07-security-notes.md#6-application-controls)
- UI: [D06 Risk](../../../docs/ui/dashboards/D06-risk.md) (changes table shows who = mcp)
- Cross-phase: P2 R2.18 (kill + dead-man), R2.19 / T2.24 (change control, hard-ceilings file).

## Requirements

- Reads (group `read`): `get_risk_policy`, `get_risk_state`, `get_risk_events`, `get_risk_changes`.
- Writes (group `risk`): `risk_policy_update` → `risk.policy.update` (diff; each field classified: tighten = C1, applied immediately; loosen = C3; above the hard-ceilings file = rejected). The result lists every field as `applied`, `pending_c3 {approval_id, cooldown_until}` or `rejected_hard_ceiling`.
- `risk_kill_on` → `risk.kill.on` (enabled by default, immediate, never blocked); `risk_kill_off` → `risk.kill.off` (C3 and only after the trigger condition is cleared); `risk_stress_run` → `risk.stress.run` (C1).
- Disabled by default: `risk.ladder.set` (down C1 / up C3). Never: `risk.deadman.ack` (needs you present; proposed in P8-B005), `venue.registry.update`.
- "Tighten BTC max position to X" maps to `risk_policy_update(level=instrument, instrument=BTC…, field=max_position, value=X)` → applied instantly, audited, Telegram notice.
- The hard-ceilings file is mounted read-only into mt-api (owned by root, mode 0444); no endpoint writes it.

## ToDo

- [ ] Add the registry entries (risk writes disabled by default except `risk.kill.on`) and regenerate the snapshot.
- [ ] Make `risk.policy.update` return per-field classification (if P2 returns only an aggregate).
- [ ] Tests; update docs.

## Verification

### Tests
- Golden (F5): tighten-only diff applied; loosen-only diff → C3 pending; mixed diff → tighten fields applied now, loosen fields pending; above-ceiling field rejected.
- Integration: `risk_kill_on` → all cancels sent < 1 s (engine metric); `risk_kill_off` → C3 pending and refused while the trigger is active.
- Integration: no route can write the hard-ceilings file (static route scan + file-permission check in the container).

### Scenarios
- Given BTC max position 2.0, when Claude tightens it to 1.0, then D06 shows the change (who = mcp) instantly.
- Given Claude raises daily loss from 2% to 3%, then you get a Telegram C3 card; without TOTP nothing changes; after approval it applies after the 15-min cool-down.
- Given a request to raise above the hard ceiling, then it's rejected even with TOTP.

### Stress / failure injection
- Kill ON from MCP during 100 open paper orders → all cancels sent < 1 s (02 §9.2).

## Acceptance criteria

- [ ] Tighten instant, loosen C3, hard ceilings unwritable, kill on immediate, kill off C3
- [ ] Per-field outcome returned to Claude
- [ ] CI green (lint, types, tests, `pit` check)

## Exceptions & edge cases

- mt-api down: MCP can't kill; Telegram `/kill` via NATS still works (02 §9.3), and the runbook says so.
- Cool-down running when kill fires: the pending loosening is cancelled and audited.
- Policy version conflict (edited on web meanwhile): 409 with the current version; Claude must re-read.

## Cardinal rules (do NOT)

- Do NOT add any write path to the hard-ceilings file.
- Do NOT block or delay kill ON for any reason.
- Do NOT make loosening risk, autonomous mode, mandates or kill-switch OFF anything less than C3 (Telegram + TOTP + cool-down); protective exits never wait for approval.
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order goes through M11, whatever its source.
- Do NOT update or delete WORM rows; corrections are new rows (15 §2).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code (including the MCP SDK).

## Doc sync on completion

- `docs/03-build-spec.md` M20: risk tool list.
- `docs/ui/dashboards/D17-mcp-console.md`: Risk group.
- `docs/roadmap/phase-8-mcp.md`: progress on T8.20.

## Branch & PR

- Branch: `p8/P8-T012-tools-risk`
- PR title: `P8-T012: Risk tool group: view, tighten instantly, loosen via C3, kill switch`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P8-T012` run

## Progress log

- 2026-10-21 00:00 · planner · created
