---
id: P6-T033
kind: task
title: Treasury policy and protocol allow-list store
phase: 6
type: BUILD
status: backlog
priority: critical
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P0-T024, P2-T010, P2-T011, P2-T017, P2-T019]
requirements: [R6.20, R6.22, R6.24]
roadmap_todos: [T6.28]
modules: [M22, M11]
dashboards: [D18]
tools: [git, uv, python>=3.12, docker]
mcp: []
env: []
services: [postgres, nats]
branch: p6/P6-T033-treasury-policy-allow-list
pr: ""
doc_sync: [docs/13-wallets-treasury-and-onchain.md, docs/02-v1-architecture.md, docs/roadmap/phase-6-ai-models-treasury.md]
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

# P6-T033 · Treasury policy and protocol allow-list store

## Goal / expected outcome

A versioned treasury policy (floats per sleeve, reserve 20–40%, caps per protocol/chain/stablecoin, HLP cap, auto-move scope) and a protocol allow-list live in `mt_treasury`, change only via audited commands (tighten C1, loosen/add protocol C3) and are read by M11 for every treasury intent.

## Context & references

- Roadmap: [R6.20](../../../docs/roadmap/phase-6-ai-models-treasury.md#3-requirements) · [R6.22](../../../docs/roadmap/phase-6-ai-models-treasury.md#3-requirements) · [R6.24](../../../docs/roadmap/phase-6-ai-models-treasury.md#3-requirements) · ToDo T6.28
- Spec: [13 §4](../../../docs/13-wallets-treasury-and-onchain.md#4-hold-and-earn-module-m22-mt_treasury) (allow-listed protocols, adding is manual) · [13 §5](../../../docs/13-wallets-treasury-and-onchain.md#5-treasury) (split, reserve) · [13 §6](../../../docs/13-wallets-treasury-and-onchain.md#6-monitors-feed-m16-and-m11) (concentration) · [03 M22](../../../docs/03-build-spec.md#m22-wallets-treasury--hold-and-earn--mt_treasury) · [02 §7.2](../../../docs/02-v1-architecture.md#72-commands-rest-write) (`treasury.allocate` C2; loosening C3)
- UI: [D18](../../../docs/ui/dashboards/D18-wallets-treasury.md) Treasury policy widget
- Cross-phase: P0-T024 (`treasury` schema), P2-T010 (layered risk policy), P2-T011 (L0 hard ceilings), P2-T017 (M11 RiskGate), P2-T019 (tighten/loosen + C3 flow)
- Decisions: [17 §B](../../../docs/17-decisions-register.md#b-cross-doc-conflicts-one-canonical-answer) (P6-B005 `treasury` schema from P0 + `ops.wallets`; P6-B013 HLP cap; P6-B008 venue cap one value, 25%) · defaults [16 §2.7](../../../docs/16-configuration-and-safety-model.md#27-wallets-signer-and-gas-13), [16 §2.1](../../../docs/16-configuration-and-safety-model.md#21-risk-sizing-and-drawdown)

## Requirements

- Policy fields: `reserve_min_pct`/`reserve_max_pct` (default band 20–40%, 13 §5), `floats` per sleeve, `per_protocol_max_pct` (default ≤ 20% of treasury, 16 §2.7), `per_chain_max_pct`, `per_stablecoin_max_pct`, `hlp_max_pct_stables` / `hlp_max_pct_portfolio` (defaults ≤ 10% of stablecoins **and** ≤ 5% of total portfolio, whichever is smaller, 16 §2.7; raising is C3; disabled unless Hyperliquid is approved in the venue registry), `auto_move_scope` (stablecoin lending within allow-list only), depeg threshold (default 50 bps, 16 §2.7), exploit auto-withdraw flag per protocol.
- Allow-list entries: protocol, chain, type (LST, lending, PT, HLP), contract addresses, audits, launch date, `auto_ok` flag, added_by, reason.
- Storage: `treasury.policy` and `treasury.allow_list` versioned, change rows WORM; current version cached in NATS KV `treasury_policy` for M11.
- Commands: `treasury.policy.update` (diff classified: tighten C1, loosen C3), `treasury.allow_list.add` (C3), `treasury.allow_list.remove` (C1, triggers exit task).
- L0 hard ceilings (edited in the agent/bot strategy settings, P2-T011, 17 §E) also bound treasury caps; values above them are rejected.
- Venue concentration is **not** a treasury field: M11 reads the single L1 risk-policy value (default ≤ 25% of total equity per venue, range 10–30%, 16 §2.1; loosening C3).

## ToDo

- [ ] Migration adding `treasury.policy` and `treasury.allow_list` to the `treasury` schema created in P0 (P0-T024, 17 §B); wallets come from `ops.wallets`.
- [ ] Policy model + diff classifier.
- [ ] Commands + KV publish.
- [ ] M11 hook: `treasury.intent` checks against policy.
- [ ] Seed a draft policy for P6-T034 approval.
- [ ] Tests; docs.

## Verification

### Tests
- Unit: diff classifier (raising any cap = loosen); hard-ceiling rejection.
- Integration: loosen requires Telegram + TOTP + cool-down (P0/P2 C3 flow).
- WORM tests on change rows.

### Scenarios
- Given a request to raise per-protocol cap from 20% to 25%, then it is C3 and also rejected if above the hard ceiling.
- Given Hyperliquid is not `allowed` in the venue registry, then HLP entries can't be enabled.
- Given stables are 40% of the portfolio, then the effective HLP cap is 4% of the portfolio (10% of stables < 5% of portfolio).

### Stress / failure injection
- n/a: low-rate config path; correctness covered by tests.

## Acceptance criteria

- [ ] Policy + allow-list versioned and audited.
- [ ] M11 reads policy for every treasury intent.
- [ ] C3 enforced server-side.

## Exceptions & edge cases

- KV unavailable: M11 uses last-known policy from Postgres; if both unavailable, treasury intents are denied (default-deny).

## Cardinal rules (do NOT)

- Do NOT add protocols automatically (adding is a manual C3 decision).
- Do NOT loosen anything (risk, LLM budgets, treasury policy, allow-list, autonomous mode, mandates) without C3 (Telegram + TOTP + cool-down); protective exits never wait for approval.
- Do NOT UPDATE or DELETE WORM rows (`audit.*`, `journal.*`, policy changes); corrections are new rows referencing the original (15 §2).
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order and on-chain move goes through M11.
- Do NOT commit secrets or paste them into chats/issues/PRs; secrets live only in the sops/age file (07 §2).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral/broker IDs in vendored code.

## Doc sync on completion

- `docs/13-wallets-treasury-and-onchain.md` §4–5: policy field list.
- `docs/02-v1-architecture.md` §7.2: treasury policy commands.
- `docs/roadmap/phase-6-ai-models-treasury.md`: tick T6.28 (and note this task ID) once all items covering it are done.

## Branch & PR

- Branch: `p6/P6-T033-treasury-policy-allow-list`
- PR title: `P6-T033: Treasury policy and protocol allow-list store`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P6-T033` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (HLP cap both bounds (17 §B P6-B013), venue cap from L1 25% (P6-B008), treasury schema from P0 (P6-B005), L0 ceilings in settings (17 §E), defaults 16 §2.7; cross-phase deps P0-T024/P2-T010/T011/T017/T019; run fields)
