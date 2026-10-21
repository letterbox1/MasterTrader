---
id: P2-T023
kind: task
title: Testnet configs for Nautilus built-in venues and sandbox paper venue
phase: 2
type: BUILD
status: backlog
priority: critical
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P2-T022, P2-T001]
requirements: [R2.30, R2.N3]
roadmap_todos: [T2.25]
modules: [M12]
dashboards: []
branch: p2/P2-T023-nautilus-testnet-venue-configs
pr: ""
doc_sync: [docs/03-build-spec.md, docs/roadmap/phase-2-strategies-risk-lab.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P2-T023 · Testnet configs for Nautilus built-in venues and sandbox paper venue

## Goal / expected outcome

The engine trades Binance spot/futures testnet (and Bybit testnet for paper-only research, IBKR paper if keys exist) through Nautilus' built-in adapters, plus a sandbox simulated venue for every instrument without a testnet, all configured per mode sub-account.

## Context & references

- Roadmap: [R2.30, R2.N3](../../../docs/roadmap/phase-2-strategies-risk-lab.md) · ToDo T2.25
- Spec: [03 M12 Nautilus adapters](../../../docs/03-build-spec.md#m12-execution--mt_engine) · [07 §3 per-mode sub-accounts](../../../docs/07-security-notes.md#3-broker--exchange-keys)
- Policy: [12 §2 registry](../../../docs/12-policy-and-compliance.md#2-venue-access-registry) · P2-B008
- Related: P2-T021, P2-T022, P2-T027.

## Requirements

- `config/engine.testnet.yaml`: Binance spot testnet + USD-M futures testnet, Bybit testnet (marked paper-only research), IBKR paper (optional); one account block per mode (`paper`, `hitl`, `autonomous`) → separate keys.
- Sandbox venue (`SandboxExecutionClient`) for paper on any instrument with P1 live data; fill model uses measured spreads/fees from `cost.*` (M16) rather than fixed bps.
- Testnet endpoints only; a config validator refuses mainnet URLs while `environment != live` and refuses `live` entirely in P2.
- STP + client-ID hooks active for all of them.

## ToDo

- [ ] Configs + validator
- [ ] Sandbox fill model using M16 costs
- [ ] Smoke scripts `mt engine smoke --venue binance-testnet`
- [ ] Tests
- [ ] Update the docs listed under *Doc sync on completion* and tick the roadmap ToDo box(es) once every task mapped to them is done

## Verification

### Tests
- Unit: config validator rejects mainnet URLs and `environment: live`.
- Integration (nightly, testnet): place/cancel/fill on Binance testnet.
- Unit: sandbox fill price includes measured spread/fee.

### Scenarios
- Given someone sets a mainnet URL in the testnet config, when the engine starts, then it refuses to start with a clear error.
- Given a hitl-mode bot, when it trades, then it uses the `mt-hitl` sub-account keys, not paper's.

### Stress / failure injection
- Testnet rate-limit burst: 2× the documented limit for 10 s → client throttles, no 418 ban.

## Acceptance criteria

- [ ] Binance testnet + sandbox venues working per mode
- [ ] Live/mainnet impossible in P2 config
- [ ] Sandbox costs come from M16
- [ ] CI green: ruff, mypy, pytest (and the `mt_risk` golden suite, `pit` check, viewport matrix where relevant)

## Exceptions & edge cases

- Testnet resets/wipes: recon flags; engine resyncs.
- Bybit derivatives are blocked live for AU: testnet only for paper research (registry rule).

## Cardinal rules (do NOT)

- Do NOT point any P2 config at a mainnet/live endpoint.
- Do NOT share keys across modes.
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order goes through M11, whatever its source.
- Do NOT commit secrets or paste them into chats/issues/logs; secrets live in the sops/age file (07 §2).
- Do NOT skip, weaken or delete a test to get green; risk-manager golden tests are mandatory for merge.
- Keys are trade-only, IP-locked, withdrawals disabled. No live money before the P7 gates; this phase is paper/testnet/practice only.

## Doc sync on completion

- `docs/03-build-spec.md` M12: list testnet venues configured.
- `docs/roadmap/phase-2-strategies-risk-lab.md`: tick T2.25 when all tasks mapped to it are done.

## Branch & PR

- Branch: `p2/P2-T023-nautilus-testnet-venue-configs`
- PR title: `P2-T023: Testnet configs for Nautilus built-in venues and sandbox paper venue`
- PR checklist: tests added and green · docs synced · task file ticked · no secrets (gitleaks) · `./kanban done P2-T023` run

## Progress log

- 2026-10-21 00:00 · planner · created
