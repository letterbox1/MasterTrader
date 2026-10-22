---
id: P2-T076
kind: task
title: "Safety-state golden tests: stale data, integrity block, bad egress and late decisions rejected"
phase: 2
type: VERIFY
status: backlog
priority: high
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P2-T070, P2-T017, P2-T018, P2-T051]
requirements: [R2.58, R2.N2]
roadmap_todos: [T2.71]
modules: [M11]
dashboards: []
tools: [uv]
mcp: []
env: []
services: []
branch: p2/P2-T076-verify-safety-state-goldens
pr: ""
doc_sync: [docs/04-plan-of-action.md, docs/roadmap/phase-2-strategies-risk-lab.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-22
updated: 2026-10-22
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
review_result: ""
---

# P2-T076 · Safety-state golden tests: stale data, integrity block, bad egress and late decisions rejected

## Goal / expected outcome

Golden tests in the mandatory `risk-golden` CI job prove that an order on data older than the bot's threshold, an entry while `audit.integrity = block_new_entries` (while an exit still passes), an order with a bad egress status and a late decision are all rejected with the right reason, and that the ladder holds each time.

## Context & references

- Roadmap: [R2.58](../../../docs/roadmap/phase-2-strategies-risk-lab.md) · ToDo T2.71
- Decisions: [16 §2.2](../../../docs/16-configuration-and-safety-model.md#22-data-freshness-what-stale-means) · [16 §2.11](../../../docs/16-configuration-and-safety-model.md#211-worm-integrity) · [16 §3.2](../../../docs/16-configuration-and-safety-model.md#32-network-egress-and-ip-locked-keys) · [16 §2.3 decision deadlines](../../../docs/16-configuration-and-safety-model.md#23-decisions-approvals-and-hitl) · [17 §A](../../../docs/17-decisions-register.md#a-s2-items-all-resolved)
- Standing rule: risk golden tests mandatory for merge ([04](../../../docs/04-plan-of-action.md#standing-rules), R2.N2)
- Inputs: P2-T070 (checks), P2-T017 (gate), P2-T018 (ladder), P2-T051 (golden suite + CI job).

## Requirements

- Golden cases (YAML, same format as P2-T051) for each state × order kind (entry, exit, protective) × bot class (fast/slow; scalping/intraday/swing/position):
  - data age at threshold −1 ms / +1 ms for 2 s and 60 s classes; closed session not stale;
  - `audit.integrity` `ok` / `alert_only` / `block_new_entries` / `halt_all` / unknown;
  - `egress.status` `ok` / `mismatch` / stale status / unknown;
  - decision deadline at the boundary for each horizon class.
- Each case asserts decision, reason code, observed vs threshold, and the ladder rung after the decision (hold for the scope).
- Property: no combination of blocking states ever yields an approved entry.
- Cases run in the required `risk-golden` job; any change to expected values needs a PR note.

## ToDo

- [ ] Write the golden case files under `tests/golden/risk/safety_state/`
- [ ] Add the property test
- [ ] Wire into the `risk-golden` CI job
- [ ] Record results (numbers, run IDs) in the progress log and tick the roadmap ToDo box

## Verification

### Tests
- The golden suite and property test themselves (CI).

### Scenarios
- Given `audit.integrity = block_new_entries`, when a bot sends an entry and an exit, then the entry is rejected `integrity_block` and the exit passes.
- Given a slow bot's data is 61 s old, when it submits, then it is rejected `data_stale` and its ladder scope holds.
- Given `egress.status = mismatch`, when any entry arrives, then it is rejected `egress_block`.

### Stress / failure injection
- Hypothesis: 20k random state combinations in nightly CI (2k per PR); zero approved entries under any blocking state.

## Acceptance criteria

- [ ] All golden cases green in the required CI job
- [ ] Property holds over the nightly run
- [ ] Ladder hold asserted for every rejection

## Exceptions & edge cases

- `alert_only` integrity mode passes orders by design; the golden asserts the warning is attached.

## Cardinal rules (do NOT)

- Do NOT mark any safety-state case skip/xfail.
- Do NOT change expected values without a PR note explaining why.
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order goes through M11, whatever its source.
- Do NOT commit secrets or paste them into chats/issues/logs; secrets live in the sops/age file outside the repo (07 §2).
- Do NOT skip, weaken or delete a test to get green; risk-manager golden tests are mandatory for merge.
- Do NOT UPDATE or DELETE WORM rows (`audit.*`, `risk.change`, `risk.approval`, `strategy.bot_version`); corrections are new rows (15 §2).
- Keys are trade-only, IP-locked, withdrawals disabled. No live money before the P7 gates; this phase is paper/testnet/practice only.
- Loosening risk, autonomous mode and mandates are C3 (Telegram approve + TOTP + cool-down); protective exits never wait for approval.

## Doc sync on completion

- `docs/04-plan-of-action.md` standing rules: the `risk-golden` job includes the safety-state cases.
- `docs/roadmap/phase-2-strategies-risk-lab.md`: tick T2.71 when all tasks mapped to it are done.

## Branch & PR

- Branch: `p2/P2-T076-verify-safety-state-goldens`
- PR title: `P2-T076: Safety-state golden tests: stale data, integrity block, bad egress and late decisions rejected`
- PR checklist: tests added and green · docs synced · task file ticked · no secrets (gitleaks) · `./kanban done P2-T076` run

## Progress log

- 2026-10-22 00:00 · aligner · created for docs/16–17 (T2.71: R2.58, R2.N2)
