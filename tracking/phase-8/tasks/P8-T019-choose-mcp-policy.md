---
id: P8-T019
kind: task
title: Choose MCP policy and enable the write tool groups you want
phase: 8
type: USER
status: backlog
priority: high
size: XS
severity: ""
owner: user
claimed_by: ""
depends_on: [P8-T016, P8-T018, P8-B010]
requirements: [R8.04]
roadmap_todos: [T8.03]
modules: [M20, M11]
dashboards: [D17]
branch: p8/P8-T019-choose-mcp-policy
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

# P8-T019 · Choose MCP policy and enable the write tool groups you want

## Goal / expected outcome

You've decided which venues/sizes (if any) may skip approve mode for MCP orders (the default and recommendation is **none**) and enabled the trade, strategies and risk tools you want. Each loosening went through C3.

## Context & references

- Roadmap: [R8.04](../../../docs/roadmap/phase-8-mcp.md#3-requirements) · ToDo [T8.03](../../../docs/roadmap/phase-8-mcp.md#4-todo-sets)
- Spec: [03 M20 safeguards](../../../docs/03-build-spec.md#m20-mcp-control-plane--mt_mcp-built-last-phase-8-only-if-wanted) · [07 §6](../../../docs/07-security-notes.md#6-application-controls) · [12 §4 Anthropic row](../../../docs/12-policy-and-compliance.md#4-per-platform-data--automation-rules) (human approval on trade decisions)
- UI: [D17 Policy + Tool registry](../../../docs/ui/dashboards/D17-mcp-console.md)
- Gap: P8-B010 (policy stance on skipping approval). Unblocks P8-T024, P8-T026, P8-T028, P8-T029.

## Requirements

- Recommended: keep "always approve" for at least the 2-week RUN (P8-T028).
- If you add an auto rule: venue, optional asset class, `max_notional_aud`, `max_orders_per_day`. It's C3 (Telegram approve + TOTP + 15-min cool-down) and never skips M11.
- Enabling each trade/risk/strategies tool is C3; disabling later is C1 and instant.

## ToDo

- [ ] Read P8-B010 and decide: no auto rules (recommended) or a specific rule.
- [ ] D17 → Tool registry: enable the Trade & adjust, Strategies and Risk tools you want (approve each C3 on Telegram with TOTP; wait out the cool-down).
- [ ] D17 → Policy: leave "Always approve" or add your rule (C3).
- [ ] Check `/mcp/tools` in D17 shows the states you expect.
- [ ] Write the choices in the Progress log (tools enabled, policy rule or "none").

## Verification

### Tests
- n/a: user configuration; confirmed by D17 state and the `ops.mcp_policy` version row.

### Scenarios
- Given no auto rules, when Claude places any order, then it waits for your Telegram tap.
- Given you enable `order_place`, when the cool-down ends, then the tool appears in your client within 60 s.

### Stress / failure injection
- n/a: one-off configuration.

## Acceptance criteria

- [ ] Policy decision recorded (default none or explicit rule)
- [ ] Chosen write tools enabled via C3 and visible in D17

## Exceptions & edge cases

- You change your mind during the cool-down: cancel the pending C3 in D17.
- Kill ON while enabling: enable still possible, but trade tools are refused until kill is off (C3).

## Cardinal rules (do NOT)

- Do NOT add auto rules above your M11 per-order limits.
- Do NOT approve C3 cards you didn't start yourself.
- Do NOT make loosening risk, autonomous mode, mandates or kill-switch OFF anything less than C3 (Telegram + TOTP + cool-down); protective exits never wait for approval.
- Do NOT use live money before the P7 gates; keys stay trade-only, IP-locked, withdrawals disabled.

## Doc sync on completion

- `docs/roadmap/phase-8-mcp.md`: tick T8.03 with the chosen policy.

## Branch & PR

- Branch: `p8/P8-T019-choose-mcp-policy`
- PR title: `P8-T019: Choose MCP policy and enable the write tool groups you want`
- PR checklist: no PR (user setup) · Progress log entry written · `./kanban done P8-T019` run

## Progress log

- 2026-10-21 00:00 · planner · created
