---
id: P2-T045
kind: task
title: Engine secret wiring per mode and automated key audit
phase: 2
type: OPS
status: backlog
priority: high
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P2-T001, P2-T044]
requirements: [R2.N3]
roadmap_todos: [T2.03, T2.40]
modules: [M12]
dashboards: [D05]
branch: p2/P2-T045-engine-secrets-key-audit
pr: ""
doc_sync: [docs/07-security-notes.md, docs/roadmap/phase-2-strategies-risk-lab.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P2-T045 · Engine secret wiring per mode and automated key audit

## Goal / expected outcome

Venue keys from the sops file reach only the services and modes that need them, and `mt keys audit` verifies for every key that it is trade-only, withdrawals disabled, IP-restricted (where the venue API exposes this) and mapped to its own per-mode sub-account, with key age metadata feeding the 90-day alert.

## Context & references

- Roadmap: [R2.N3](../../../docs/roadmap/phase-2-strategies-risk-lab.md) · ToDos T2.03, T2.40
- Security: [07 §3](../../../docs/07-security-notes.md#3-broker--exchange-keys) · [07 §2 rotation 90 days](../../../docs/07-security-notes.md#2-secrets) · [SPEC NN5](../../../SPEC.md#non-negotiable-requirements)
- Related: P2-T001 (your keys), D05 Venues tab shows key age (Part B UI).

## Requirements

- Secret paths `venues.<venue>.<mode>` mapped to engine account configs; `deadman` gets cancel-only where the venue supports it.
- Audit checks: Binance `GET /sapi/v1/account/apiRestrictions` (`enableWithdrawals=false`, `ipRestrict=true`) on testnet where available; Alpaca/OANDA/IG: account id per mode distinct, manual attestation recorded from P2-T001; all: no key shared across modes.
- Output: `/system/keys` masked metadata (venue, mode, created, age, checks pass/fail) + Prometheus `mt_key_age_days`.
- Audit runs at engine start (fail → that account disabled) and nightly.

## ToDo

- [ ] Secret → config wiring
- [ ] `mt keys audit` CLI + nightly Prefect flow
- [ ] Metadata endpoint fields
- [ ] Tests
- [ ] Update the docs listed under *Doc sync on completion* and tick the roadmap ToDo box(es) once every task mapped to them is done

## Verification

### Tests
- Unit: duplicate key across modes detected.
- Integration (testnet): Binance restrictions parsed; withdrawal-enabled key → account disabled + alert.

### Scenarios
- Given a key with withdrawals enabled, when the engine starts, then that account is disabled and a critical alert names the venue/mode (no secret printed).

### Stress / failure injection
- n/a: periodic audit; covered by unit/integration tests.

## Acceptance criteria

- [ ] Every P2 key audited with results visible (masked)
- [ ] Withdrawal-enabled or shared keys block trading on that account
- [ ] CI green: ruff, mypy, pytest (and the `mt_risk` golden suite, `pit` check, viewport matrix where relevant)

## Exceptions & edge cases

- Venue API can't report restrictions: rely on recorded manual attestation and flag 'unverifiable'.

## Cardinal rules (do NOT)

- Do NOT print, log or return key material; masked metadata only.
- Do NOT commit secrets or paste them into chats/issues/logs; secrets live in the sops/age file (07 §2).
- Do NOT skip, weaken or delete a test to get green; risk-manager golden tests are mandatory for merge.
- Keys are trade-only, IP-locked, withdrawals disabled. No live money before the P7 gates; this phase is paper/testnet/practice only.

## Doc sync on completion

- `docs/07-security-notes.md` §3: audit checks per venue.
- `docs/roadmap/phase-2-strategies-risk-lab.md`: tick T2.03, T2.40 when all tasks mapped to it are done.

## Branch & PR

- Branch: `p2/P2-T045-engine-secrets-key-audit`
- PR title: `P2-T045: Engine secret wiring per mode and automated key audit`
- PR checklist: tests added and green · docs synced · task file ticked · no secrets (gitleaks) · `./kanban done P2-T045` run

## Progress log

- 2026-10-21 00:00 · planner · created
