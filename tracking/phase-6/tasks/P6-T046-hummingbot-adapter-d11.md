---
id: P6-T046
kind: task
title: Optional: Hummingbot market-making sidecar behind M11 with D11
phase: 6
type: BUILD
status: backlog
priority: low
size: L
severity: ""
owner: agent
claimed_by: ""
depends_on: [P6-T003, P2-T017, P2-T031]
requirements: [R6.30]
roadmap_todos: [T6.35]
modules: [M13, M11, M16, mt-mm-adapter]
dashboards: [D11]
tools: [git, cargo, docker]
mcp: []
env: []
services: [hummingbot, nats]
branch: p6/P6-T046-hummingbot-adapter-d11
pr: ""
doc_sync: [docs/03-build-spec.md, docs/ui/dashboards/D11-market-making.md, docs/19-third-party-register.md, docs/roadmap/phase-6-ai-models-treasury.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-11-20
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
review_result: ""
---

# P6-T046 · Optional: Hummingbot market-making sidecar behind M11 with D11

## Goal / expected outcome

Hummingbot runs as a sidecar venue behind M11 (telemetry off, broker IDs stripped) in **paper** mode, with D11 live, and its paper P&L is compared against HLP on the same capital.

## Context & references

- Roadmap: [R6.30](../../../docs/roadmap/phase-6-ai-models-treasury.md#3-requirements) · ToDo T6.35
- Optional module, off by default (P6-T003, 16 §2.14a); built once you enable it in settings.
- Spec: [03 M13](../../../docs/03-build-spec.md#m13-market-making-sidecar) · [14 §3](../../../docs/14-strategy-evidence-and-validation.md#3-strategy-catalogue-evidence-ranked-templates) (market making P3; must beat HLP) · [07 §7](../../../docs/07-security-notes.md#7-supply-chain) (Hummingbot metrics + broker IDs)
- UI: [D11](../../../docs/ui/dashboards/D11-market-making.md)
- Kill: [02 F6](../../../docs/02-v1-architecture.md#8-end-to-end-flows) (Hummingbot stops)
- Depends on (this phase): P6-T003
- Cross-phase: P2-T017 (M11 RiskGate), P2-T031 (kill switch)

## Requirements

- Pinned image/commit; telemetry disabled check and broker-ID stripping check both block start if failing.
- Adapter `mt-mm-adapter` (Rust client of the Hummingbot API, REST + WebSocket, [18 §2.1](../../../docs/18-platform-and-deployment.md#21-rust-cargo-workspace-crates)): Hummingbot and the Hummingbot API run unmodified in their own containers ([19 §1](../../../docs/19-third-party-register.md#1-run-unmodified-separate-services-or-libraries-we-call)); the adapter maps Hummingbot API ↔ `mt-engine` venue abstraction, through `mt-api`/`mt-risk` like every other client; every order intent passes M11 (exposure counts toward global limits).
- Kill switch → all bots stop within 1 s; `mm.bot.cancel_all` (C1).
- Commands `mm.bot.create|start|stop|update|cancel_all` with D11 levels: create/start paper C1; live start C3 (quotes on its own, like `autonomous`); edit live C2, risk-increasing C3; stop and cancel_all C1. Live is out of scope in P6.
- Paper P&L decomposition (spread capture, inventory, fees/rebates, funding) vs HLP APR on the same notional, weekly.

## ToDo

- [ ] Pin the Hummingbot and Hummingbot API images by digest (unmodified); telemetry + broker-ID audit; Hummingbot API credentials as a generated line in `.env.example` §14 first (07 §2 naming), never in this file.
- [ ] `crates/mt-mm-adapter` + M11 integration.
- [ ] D11 UI + API.
- [ ] Weekly HLP comparison report.
- [ ] Tests; docs.

## Verification

### Tests
- `cargo test -p mt-mm-adapter` (recorded Hummingbot API responses) and `cargo clippy`.
- Integration: bot quote → M11 check → paper fill.
- Start blocked if telemetry check fails.
- Kill drill: bots stop < 1 s.

### Scenarios
- Given telemetry is re-enabled by an upgrade, then the bot can't start and D11 shows why.

### Stress / failure injection
- Hummingbot API disconnect: bots marked unknown, orders cancelled on reconnect, alert.

## Acceptance criteria

- [ ] Paper bot runs ≥ 1 week with HLP comparison report.
- [ ] Kill drill passes.

## Exceptions & edge cases

- Venue not `allowed` in registry → no bot can target it.
- Optional module, **off by default** (P6-T003 records `modules.*.enabled: false`). Build it only once you enable it in settings; while it stays off at phase exit, P6-T066 cancels this item with reason "optional module off by default (P6-T003)" and it can be re-opened any time you enable it.

## Cardinal rules (do NOT)

- Do NOT run live market making in P6.
- Do NOT bypass `mt-api`, the risk manager (M11) or `pit(as_of)`; every order and on-chain move goes through M11.
- Do NOT touch live money or live keys; keys stay trade-only, IP-locked, withdrawals disabled (live is gated to P7).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral/broker IDs in vendored code.
- Do NOT commit secrets or paste them into chats/issues/PRs; secrets live only in the sops/age file (07 §2).

## Doc sync on completion

- `docs/03-build-spec.md` M13: adapter notes.
- `docs/ui/dashboards/D11-market-making.md`: implemented.
- `docs/19-third-party-register.md` §1: confirm the Hummingbot row.
- `docs/roadmap/phase-6-ai-models-treasury.md`: tick T6.35 (and note this task ID) once all items covering it are done.

## Branch & PR

- Branch: `p6/P6-T046-hummingbot-adapter-d11`
- PR title: `P6-T046: Optional: Hummingbot market-making sidecar behind M11 with D11`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P6-T046` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (D11 levels incl. live start C3; cross-phase deps P2-T017/P2-T031; run fields)
- 2026-11-19 00:00 · aligner · re-platformed per docs/18 (Hummingbot adapter stays Python (18 §2.2) and reaches venues only through `mt-api`/`mt-risk`; depends on P6-T003 (agent default: off), not a human decision)
- 2026-11-20 00:00 · aligner · Rust-max per 17 §H (adapter is the Rust `mt-mm-adapter` driving the unmodified Hummingbot API; roadmap ToDo T6.30 → T6.35; tools cargo)
