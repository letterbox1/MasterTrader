---
id: P2-T017
kind: task
title: Default-deny pre-trade RiskGate in front of Nautilus RiskEngine
phase: 2
type: BUILD
status: backlog
priority: critical
size: L
severity: ""
owner: agent
claimed_by: ""
depends_on: [P2-T011, P2-T012, P2-T013, P2-T014, P2-T015, P2-T016]
requirements: [R2.10, R2.16, R2.N1]
roadmap_todos: [T2.22]
modules: [M11]
dashboards: [D06]
branch: p2/P2-T017-pre-trade-risk-gate
pr: ""
doc_sync: [docs/03-build-spec.md, docs/02-v1-architecture.md, docs/roadmap/phase-2-strategies-risk-lab.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P2-T017 · Default-deny pre-trade RiskGate in front of Nautilus RiskEngine

## Goal / expected outcome

`mt_risk.RiskGate` is the single, default-deny pre-trade layer every `OrderIntent` passes (strategy, agent, UI, Telegram, later MCP) before Nautilus' own `RiskEngine`; it runs all checks in a fixed order, returns a reasoned decision in p99 < 1 ms, and exposes the same logic as `POST /risk/preview`.

## Context & references

- Roadmap: [R2.10, R2.16, R2.N1](../../../docs/roadmap/phase-2-strategies-risk-lab.md) · ToDo T2.22
- Spec: [03 M11 pre-trade checks](../../../docs/03-build-spec.md#m11-risk-manager--mt_risk-built-in-user-inputs-via-uitelegram-later-mcp) · [SPEC NN2, NN3](../../../SPEC.md#non-negotiable-requirements) · SLO: [02 §9.2](../../../docs/02-v1-architecture.md#92-observability--slos)
- Flow: [02 F2 step 4](../../../docs/02-v1-architecture.md#8-end-to-end-flows) · NATS: [02 §6 `ord.intent.*` → `ord.risk.{decision}`](../../../docs/02-v1-architecture.md#6-messaging-nats)
- Cross-phase: `dq.status.*` + KV `feed_status` (P1 R1.10), `cost.*` spreads (P1 R1.11).
- Related: P2-B003 (collar %, deadlines), P2-T052 bypass tests, P2-T058 latency benchmark.

## Requirements

- Check order (first failure wins, all results recorded): kill (global/sleeve) → ceilings present → venue registry + leverage → mode/approval routing marker → DQ status of instrument (`stale|bad` → hold) → data staleness (2 s/60 s) + decision deadline → event blackout (manual windows now; `cal.*` from P4) → duplicate (client-order-ID / intent-ID seen) → price collar (within X% of last trade; X from policy) → liquidity/spread (`spread_bps` vs policy max, `cost.*` spread > N× normal) → limits (P2-T012) → sleeve/netting (P2-T014) → portfolio (P2-T015) → sizing cap (P2-T013) → ladder adjustment (P2-T018).
- Default-deny: any exception, missing state or unknown field → reject with `internal_default_deny`.
- Decision record: `ord.risk.{approve|reject|hold|needs_approval}` with reason codes, observed vs limit; `risk.event` for rejects/holds; latency histogram `mt_risk_check_seconds`.
- Protective exits (stop, TP set at entry, kill flatten, risk-forced reduce) are flagged `protective=true`: they skip approval routing and staleness holds but still run kill/venue/duplicate checks and can only reduce exposure.
- Nautilus `RiskEngine` configured as second line with ceilings (`max_notional_per_order`, `max_order_submit_rate`).
- In-process, no network or DB calls in the hot path; state from in-memory caches fed by NATS KV.
- `POST /risk/preview` runs the same pipeline with no side effects (used by `RiskPreview`, approval cards).

## ToDo

- [ ] `packages/mt_risk/gate.py` pipeline + `checks/` modules (dq, staleness, blackout, duplicate, collar, liquidity)
- [ ] Caches: KV watchers for `risk_state`, `feed_status`, `kill`; spread cache from `cost.*`
- [ ] Wire into `MTStrategy.submit_intent` (P2-T003) and the engine intent actor (P2-T021)
- [ ] Nautilus RiskEngine config from ceilings
- [ ] `/risk/preview` endpoint in mt_api (shared library)
- [ ] Prometheus histogram + exemplars with `trace_id`
- [ ] Tests + microbenchmark (pytest-benchmark)
- [ ] Update the docs listed under *Doc sync on completion* and tick the roadmap ToDo box(es) once every task mapped to them is done

## Verification

### Tests
- Unit per check: pass/fail boundaries.
- Golden: 200-case table of intents × states → decision + reason (part of the mandatory suite).
- Property: random exceptions injected in any check → reject (never approve).
- Integration: `ord.intent.manual` from mt_api → decision published on `ord.risk.*`.

### Scenarios
- Given BTCUSDT `dq.status=stale`, when a strategy submits an entry, then decision `hold` and no venue order.
- Given the same intent ID twice, when submitted, then the second is rejected `duplicate`.
- Given a protective stop during a stale feed, when triggered, then it is sent (reduce-only) and logged as protective.

### Stress / failure injection
- Benchmark 1M intents with full policy (50 venues × 200 strategies): p99 < 1 ms, p50 < 100 µs on the host; regression > 20% fails CI.
- Fault: KV watcher disconnect → state marked unknown → default-deny within 1 s.

## Acceptance criteria

- [ ] All 03 M11 pre-trade checks implemented in the stated order
- [ ] Default-deny on errors proven by property tests
- [ ] p99 < 1 ms benchmark recorded
- [ ] `/risk/preview` shares the code path
- [ ] CI green: ruff, mypy, pytest (and the `mt_risk` golden suite, `pit` check, viewport matrix where relevant)

## Exceptions & edge cases

- Postgres down: gate unaffected (in-memory); audit writes buffered via NATS (02 §9.3).
- Clock skew > policy threshold (P1 DQ): treat feed as `bad` → hold.
- Unknown instrument: reject `instrument_unknown`.

## Cardinal rules (do NOT)

- Do NOT add a fast path that skips checks for any source (UI, Telegram, agents, MCP).
- Do NOT perform I/O in the hot path.
- Do NOT let protective exits increase exposure.
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order goes through M11, whatever its source.
- Do NOT commit secrets or paste them into chats/issues/logs; secrets live in the sops/age file (07 §2).
- Do NOT skip, weaken or delete a test to get green; risk-manager golden tests are mandatory for merge.
- Loosening risk, autonomous mode and mandates are C3 (Telegram approve + TOTP + cool-down); protective exits never wait for approval.

## Doc sync on completion

- `docs/03-build-spec.md` M11: check order and reason codes.
- `docs/02-v1-architecture.md` F2: decision subjects as built.
- `docs/roadmap/phase-2-strategies-risk-lab.md`: tick T2.22 when all tasks mapped to it are done.

## Branch & PR

- Branch: `p2/P2-T017-pre-trade-risk-gate`
- PR title: `P2-T017: Default-deny pre-trade RiskGate in front of Nautilus RiskEngine`
- PR checklist: tests added and green · docs synced · task file ticked · no secrets (gitleaks) · `./kanban done P2-T017` run

## Progress log

- 2026-10-21 00:00 · planner · created
