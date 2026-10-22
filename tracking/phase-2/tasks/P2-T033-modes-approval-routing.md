---
id: P2-T033
kind: task
title: "Modes and approval routing: paper, hitl, autonomous"
phase: 2
type: BUILD
status: backlog
priority: critical
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P2-T017, P2-T021]
requirements: [R2.20]
roadmap_todos: [T2.25]
modules: [M11, M12]
dashboards: []
tools: [uv]
mcp: []
env: []
services: [nats, postgres]
branch: p2/P2-T033-modes-approval-routing
pr: ""
doc_sync: [docs/03-build-spec.md, docs/02-v1-architecture.md, docs/roadmap/phase-2-strategies-risk-lab.md]
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

# P2-T033 · Modes and approval routing: paper, hitl, autonomous

## Goal / expected outcome

After the gate approves an intent, routing follows the bot's mode (capped by its strategy's mode ceiling; the stricter applies): `paper` → simulated fill, `hitl` → `risk.approval.request` with TTL (expiry = reject), `autonomous` → submit; protective exits never wait for approval; every approval decision is recorded in `risk.approval` (WORM).

## Context & references

- Roadmap: [R2.20](../../../docs/roadmap/phase-2-strategies-risk-lab.md) · ToDo T2.25
- Spec: [03 M11 modes](../../../docs/03-build-spec.md#m11-risk-manager--mt_risk-built-in-user-inputs-via-uitelegram-later-mcp) · [15 §1.2 modes + rules](../../../docs/15-bots-hitl-and-worm-audit.md#1-trading-bots) · [15 §1.3 TTL defaults](../../../docs/15-bots-hitl-and-worm-audit.md#13-hitl-approval-via-telegram)
- Flow: [02 F2 step 5](../../../docs/02-v1-architecture.md#8-end-to-end-flows)
- Decisions: [17 §B](../../../docs/17-decisions-register.md#b-cross-doc-conflicts-one-canonical-answer) modes `paper`/`hitl`/`autonomous` per bot (P2-B053) and paper → HITL = C2 (P2-B005) · [16 §2.3](../../../docs/16-configuration-and-safety-model.md#23-decisions-approvals-and-hitl) TTLs, large-order rule, MCP cards.
- Related: P2-T037 bot policy, P2-T038/T039 approval UIs.

## Requirements

- Approval request: `risk.approval(id, intent snapshot, card snapshot, bot_id, strategy_version, ttl_s, created_at, decision, decided_by, decided_via, latency_ms, outcome)` insert-only (decision = new row referencing the request).
- NATS `risk.approval.request` / `risk.approval.result` with `bot_id`; TTL timer in engine; expiry → reject + log 'expired' (never act late).
- On approve: re-run `RiskGate` with current state (prices may have moved) before submit; on 'approve ½' re-size to 50% (rounded down) and re-check; on reject → done; on 'pause bot' → reject + bot paused.
- Protective classification: stop-loss, take-profit set at entry, kill flatten, risk-forced reductions bypass approval but not the gate.
- TTL defaults by bot horizon ([16 §2.3](../../../docs/16-configuration-and-safety-model.md#23-decisions-approvals-and-hitl), L4 settings): 60 s intraday/scalping · 15 min swing · 4 h position; expiry = reject. MCP-originated orders (P8) always need an approval card, TTL 5 min, whatever the bot's mode.
- **Large orders** (default > 2% of sleeve or > A$5,000 notional) are flagged `large_order` on the request so Telegram asks for TOTP and the web for hold-to-confirm (P2-T038/T039).
- Mode names: `paper|hitl|autonomous` canonical; `approve|auto` are retired aliases (accepted, normalised).

## ToDo

- [ ] `packages/mt_risk/modes.py` + approval service
- [ ] Engine routing after gate
- [ ] WORM registration of `risk.approval`
- [ ] Tests
- [ ] Update the docs listed under *Doc sync on completion* and tick the roadmap ToDo box(es) once every task mapped to them is done

## Verification

### Tests
- Flow tests: approve, approve ½, reject, expire, pause-bot; each with audit rows.
- Unit: approval arriving 1 ms after TTL → rejected 'expired'.
- Unit: protective stop on a hitl bot executes without an approval request.

### Scenarios
- Given a hitl intent with TTL 60 s, when no answer comes, then at 60 s it is rejected 'expired' and nothing is submitted later even if 'Approve' is tapped at 61 s.
- Given approval at 30 s after price moved beyond collar, when re-checked, then rejected `collar` and the card shows why.

### Stress / failure injection
- 1,000 pending approvals with staggered TTLs: all expire on time (±100 ms), no leak, engine latency unchanged.

## Acceptance criteria

- [ ] Three modes routed correctly
- [ ] Expiry never executes late
- [ ] Protective exits never wait
- [ ] CI green: ruff, mypy, pytest (and the `mt_risk` golden suite, `pit` check, viewport matrix where relevant)

## Exceptions & edge cases

- Engine restart with pending approvals: pending ones are expired on boot (never resumed).
- Telegram down: approvals still available on web; TTL unchanged.

## Cardinal rules (do NOT)

- Do NOT execute an approval after its TTL.
- Do NOT skip the gate re-check on approval.
- Do NOT make protective exits wait for approval.
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order goes through M11, whatever its source.
- Do NOT commit secrets or paste them into chats/issues/logs; secrets live in the sops/age file (07 §2).
- Do NOT skip, weaken or delete a test to get green; risk-manager golden tests are mandatory for merge.
- Do NOT UPDATE or DELETE WORM rows (`audit.*`, `risk.change`, `risk.approval`, `strategy.bot_version`); corrections are new rows with `supersedes_id` (15 §2).
- Loosening risk, autonomous mode and mandates are C3 (Telegram approve + TOTP + cool-down); protective exits never wait for approval.

## Doc sync on completion

- `docs/03-build-spec.md` M11 and `docs/02-v1-architecture.md` F2: canonical mode names and approval re-check.
- `docs/roadmap/phase-2-strategies-risk-lab.md`: tick T2.25 when all tasks mapped to it are done.

## Branch & PR

- Branch: `p2/P2-T033-modes-approval-routing`
- PR title: `P2-T033: Modes and approval routing: paper, hitl, autonomous`
- PR checklist: tests added and green · docs synced · task file ticked · no secrets (gitleaks) · `./kanban done P2-T033` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (bot mode capped by strategy ceiling, TTL and large-order defaults from 16 §2.3, MCP cards always need approval)
