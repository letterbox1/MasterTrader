---
id: P3-T033
kind: task
title: Egypt crypto hard flag wired to the risk manager
phase: 3
type: BUILD
status: backlog
priority: high
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P3-T031, P3-T055, P2-T016, P2-T017]
requirements: [R3.09, R3.16]
roadmap_todos: [T3.26]
modules: [M18, M11]
dashboards: [D15, D06]
tools: [git, uv, docker]
mcp: []
env: []
services: [postgres, nats, mt-api, engine]
branch: p3/P3-T033-egypt-crypto-hard-flag-m11
pr: ""
doc_sync: [docs/03-build-spec.md, docs/roadmap/phase-3-journal-and-tax.md]
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

# P3-T033 · Egypt crypto hard flag wired to the risk manager

## Goal / expected outcome

While the residency timeline says Egypt, crypto is blocked through the **venue registry**: the residency change emits `tax.residency.changed`, the registry recompute (P3-T055) marks every crypto product `blocked` for residency EG, M11's existing venue-registry check rejects crypto entries and crypto mandates, protective exits continue, and D15 shows a red compliance flag on any crypto activity. Removing the block (leaving Egypt) is a loosening and only applies after C3.

## Context & references

- Roadmap: [R3.09, R3.16, T3.26](../../../docs/roadmap/phase-3-journal-and-tax.md)
- [09 key findings: Egypt](../../../docs/09-journal-and-tax.md#️-key-findings-that-shape-the-design) (M11 fails closed until the registry has recomputed; loosening C3) · [12 §1 moving countries](../../../docs/12-policy-and-compliance.md#1-australian-boundary-the-load-bearing-assumption) · [12 §2 venue registry](../../../docs/12-policy-and-compliance.md#2-venue-access-registry) · D15 rules (Egypt red flag) [D15](../../../docs/ui/dashboards/D15-tax.md)
- Decision: [17 §D P3-B006/B007](../../../docs/17-decisions-register.md#d-other-decisions) (event + registry recompute; replaces the earlier KV `compliance_state` proposal)
- Cross-phase prerequisites (depends_on): P2-T016 (M11 venue-registry check), P2-T017 (default-deny pre-trade RiskGate); P5 mandates consume the same registry status
- Related: P3-T031 (timeline publishes the event), P3-T055 (contract, recompute consumer, C3 routing), P3-T058 (command tests)

## Requirements

- Registry rule set `config/risk/residency_rules.yaml` (per country; EG: all crypto spot, perp and token products `blocked`, mandates disabled); applied by the P3-T055 recompute on every `tax.residency.changed`, effective from the period's local start date.
- M11: uses the existing venue-registry check (P2-T016) — a `blocked` product → reject with reason `venue_registry_blocked:residency_EG`; reduce-only closes and protective orders still pass. No extra KV store is introduced.
- Fail closed: while the registry's applied `residency_version` is behind the latest `tax.residency.changed`, M11 rejects new crypto entries (P3-T055 hook); at engine start with neither registry nor residency available → default-deny for crypto.
- Removing EG (or any change that unblocks) is a loosening → C3 (Telegram approve + TOTP + cool-down, 16 §2.3) through the change-control service; tightening is immediate.
- D15: red compliance flag on every crypto row while EG is active (AU_2026/EG plugin `compliance_flags`).

## ToDo

- [ ] Write the EG rule set and its loader for the P3-T055 recompute
- [ ] Reason code + reduce-only exemption check in `packages/mt_risk/checks/venue_registry.py` (extend, don't duplicate)
- [ ] Mandate check: crypto mandates refused while blocked (hook for P5 consumers)
- [ ] D15 compliance flag wiring
- [ ] Tests; docs

## Verification

### Tests
- Unit (M11): crypto order with the EG block → rejected with the registry reason; reduce-only close → allowed.
- Integration: add an EG residency period → `tax.residency.changed` → registry blocked → paper crypto order rejected within 5 s.
- Unit: removing EG produces a C3 change request; a C1 attempt is refused; the block stays until approval + cool-down.

### Scenarios
- Given residency EG from a date, when a bot tries a crypto entry, then M11 rejects it and D06 shows the reason.
- Given the recompute consumer is down after a residency change, when a crypto order arrives, then it's denied (fail-closed).

### Stress / failure injection
- Pre-trade latency benchmark with the registry check: p99 still within the P2 pre-trade SLO.

## Acceptance criteria

- [ ] Crypto blocked while EG is active, via the venue registry (tests)
- [ ] Protective exits never blocked
- [ ] Unblocking needs C3
- [ ] Latency SLO unchanged
- [ ] CI green (lint, types, tests, `pit` check; `tax-golden` once P3-T045 lands)

## Exceptions & edge cases

- Future-dated residency → the registry block activates at the local start date (scheduled recompute).

## Cardinal rules (do NOT)

- Do NOT block protective exits.
- Do NOT let a residency edit loosen risk without C3.
- Do NOT commit secrets or paste them into chats/issues; secrets live only in the sops/age file ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order goes through M11.
- Loosening risk, autonomous mode and mandates are C3 (Telegram + TOTP + cool-down); protective exits never wait for approval.
- Do NOT UPDATE or DELETE `journal.*` (WORM) rows; corrections are new rows referencing the superseded row ([15 §2](../../../docs/15-bots-hitl-and-worm-audit.md#2-worm-records-write-once-read-many)).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.

## Doc sync on completion

- `docs/03-build-spec.md` M11: note the residency-driven registry block and fail-closed rule.
- `docs/roadmap/phase-3-journal-and-tax.md`: tick T3.26 once every item mapped to it is done.

## Branch & PR

- Branch: `p3/P3-T033-egypt-crypto-hard-flag-m11`
- PR title: `P3-T033: Egypt crypto hard flag wired to the risk manager`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P3-T033` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (Egypt block now via `tax.residency.changed` → venue-registry recompute (P3-T055) + existing M11 registry check; dropped KV `compliance_state` proposal (P3-B007 closed); explicit P2 depends_on; tools/services filled)
