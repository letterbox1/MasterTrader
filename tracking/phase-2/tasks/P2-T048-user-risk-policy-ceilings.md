---
id: P2-T048
kind: task
title: Write the initial risk policy values and the hard-ceilings file
phase: 2
type: USER
status: backlog
priority: critical
size: S
severity: ""
owner: user
claimed_by: ""
depends_on: [P2-T011, P2-T012]
requirements: [R2.14, R2.19]
roadmap_todos: [T2.01]
modules: [M11]
dashboards: [D06]
branch: p2/P2-T048-user-risk-policy-ceilings
pr: ""
doc_sync: [docs/14-strategy-evidence-and-validation.md, docs/roadmap/phase-2-strategies-risk-lab.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P2-T048 · Write the initial risk policy values and the hard-ceilings file

## Goal / expected outcome

Your initial risk policy (starting from the 14 §5 defaults) is loaded as policy version 1, and your hard-ceilings file exists on the host at `/etc/mastertrader/risk-ceilings.yaml`, editable only by you.

## Context & references

- Roadmap: [R2.14, R2.19](../../../docs/roadmap/phase-2-strategies-risk-lab.md) · ToDo T2.01
- Spec: [14 §5 defaults](../../../docs/14-strategy-evidence-and-validation.md#5-risk-engine-additions-m11) · [14 §4 sizing/leverage](../../../docs/14-strategy-evidence-and-validation.md#4-trading-methods-enforced-in-code-defaults-user-editable-in-d06) · [03 M11](../../../docs/03-build-spec.md#m11-risk-manager--mt_risk-built-in-user-inputs-via-uitelegram-later-mcp)
- Format: `packages/mt_risk/policy/defaults.yaml` (P2-T012) and the ceilings schema (P2-T011).
- Open numbers to decide: P2-B001, P2-B003.
- Unblocks: paper trading (P2-T067), D06 shows real values.

## Requirements

- Policy: daily loss, drawdown (sleeve 15% / system 10% or your values), risk per trade, max position, open positions, stale data, decision deadlines per sleeve, API-error pause, venue concentration, leverage, price collar %, dead-man N seconds, cost-ratio pause.
- Ceilings: one value per field you never want exceeded (e.g. crypto derivative leverage 2×, risk/trade ≤ 2%, system DD ≤ 10%).
- Ceilings file is owned by root, mode 0644, edited only over SSH on the host.

## ToDo

- [ ] Copy `defaults.yaml` to a scratch file and edit values (or edit in D06 Policy once P2-T043 lands)
- [ ] Load with `mt risk policy import my-policy.yaml` (first import of an empty system is applied as version 1)
- [ ] On the host: `sudo install -o root -g root -m 0644 risk-ceilings.yaml /etc/mastertrader/risk-ceilings.yaml` (start from `packages/mt_risk/ceilings.example.yaml`)
- [ ] Restart `engine` and `mt-api`; confirm D06 shows each ceiling with a lock icon and `risk.event ceilings_loaded` with the file hash
- [ ] Record decisions for the open numbers in P2-B001/P2-B003 progress logs
- [ ] Record completion in the progress log (no secrets) and run `./kanban done P2-T048`

## Verification

### Tests
- Agent confirms: policy version 1 present; ceilings hash logged; a test loosen above a ceiling is rejected.

### Scenarios
- Given the ceilings file says max leverage 2×, when you try 3× in D06, then save is blocked.

### Stress / failure injection
- n/a: configuration action.

## Acceptance criteria

- [ ] Policy v1 loaded with your values
- [ ] Ceilings file on host with correct owner/permissions
- [ ] Decisions recorded for the open numbers

## Exceptions & edge cases

- You want to change ceilings later: edit the host file; the system reloads and alerts (no API path exists).

## Cardinal rules (do NOT)

- Do NOT commit your personal ceilings file to git.
- Do NOT set ceilings looser than 12 §1 (2× crypto derivatives).
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order goes through M11, whatever its source.
- Do NOT commit secrets or paste them into chats/issues/logs; secrets live in the sops/age file (07 §2).
- Loosening risk, autonomous mode and mandates are C3 (Telegram approve + TOTP + cool-down); protective exits never wait for approval.

## Doc sync on completion

- `docs/14-strategy-evidence-and-validation.md` §5: note that defaults were reviewed and your chosen values live in policy v1.
- `docs/roadmap/phase-2-strategies-risk-lab.md`: tick T2.01 when all tasks mapped to it are done.

## Branch & PR

- Branch: `p2/P2-T048-user-risk-policy-ceilings` (only if a repo change results, e.g. non-secret config or manifests; secrets never go in git)
- PR title: `P2-T048: Write the initial risk policy values and the hard-ceilings file`
- PR checklist: no secrets in diff (gitleaks clean) · task file ticked · `./kanban done P2-T048` run

## Progress log

- 2026-10-21 00:00 · planner · created
