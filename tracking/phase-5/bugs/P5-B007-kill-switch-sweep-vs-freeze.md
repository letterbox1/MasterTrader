---
id: P5-B007
kind: gap
title: Kill switch: "sweep hot balances" (14 §5) vs "treasury moves frozen" (D18, F6)
phase: 5
type: DOC
status: done
priority: medium
size: XS
severity: S3
owner: agent
claimed_by: ""
depends_on: []
requirements: [R5.N2, R5.07]
roadmap_todos: []
modules: [M22, M11]
dashboards: [D18, D12]
tools: []
mcp: []
env: []
services: []
branch: p5/P5-B007-kill-switch-sweep-vs-freeze
pr: ""
doc_sync: [docs/02-v1-architecture.md, docs/ui/dashboards/D18-wallets-treasury.md, docs/13-wallets-treasury-and-onchain.md]
doc_sync_status: done
found_in: "docs/14-strategy-evidence-and-validation.md §5 rung 6; docs/ui/dashboards/D18-wallets-treasury.md §Rules; docs/02-v1-architecture.md F6"
created: 2026-10-21
updated: 2026-10-22
started: ""
completed: 2026-10-22
blocked_reason: ""
checkpoint: ""
review_result: ""
---

# P5-B007 · Kill switch: "sweep hot balances" (14 §5) vs "treasury moves frozen" (D18, F6)

## Goal / expected outcome

The docs say explicitly that kill ON freezes auto-claims, treasury moves and new exposure, while protective actions (sweep to the vault, revoke approvals, exits) still run.

## Context & references

- 14 §5 rung 6: "hot balances sweep to the vault address"
- D18: "Kill switch ON: treasury moves … are frozen; exits stay available"; F6 lists "airdrop-exec freezes" without the sweep
- Tasks P5-T028, P5-T058

## Requirements

- **Steps to reproduce:** Read the three passages; a sweep is a treasury move.
- **Expected:** Explicit exemption for protective sweeps/revokes.
- **Actual:** Contradictory reading possible.
- **Suggested fix:** Add to F6 and D18: "kill ON also sweeps hot/identity/burner balances above gas reserve to the vault; revokes and sweeps-to-vault are exempt from the freeze".
- **Impact:** S3: implementers could block the protective sweep.

## ToDo

- [x] Resolution recorded: Decided (17 §B P5-B007): kill stops new trading, cancels orders, applies each bot's failure policy, freezes new treasury/earn moves and, from P5 (default on), sweeps hot trading balances to the vault address; sweeps to the vault and approval revokes are protective and exempt from the freeze
- [x] Docs carry it: 13 §1 rules (kill switch), 02 F6 (from P5 hot balances sweep; protective sweeps/revokes exempt), 14 §5 rung 6, D18 rules (kill ON), roadmap R5.07/R5.N2
- [x] P5 tasks aligned: P5-T028 (kill sweep, `kill_sweep_enabled` default true), P5-T058 (drill), P5-T012 (setting)

## Verification

### Tests
- Doc review: every listed doc states the same value/name after the fix; `python3 tools/kanban/kanban.py validate` stays at 0 errors

### Scenarios
- Given the fixed docs, when a developer picks up the affected P5 tasks, then there is exactly one authoritative answer to follow

### Stress / failure injection
- n/a: documentation/spec gap

## Acceptance criteria

- [x] Docs listed under Doc sync (and the other docs named in the ToDo) state the decided value/name
- [x] Affected P5 tasks reference the decided value/name and an owning task exists
- [x] Resolution recorded in the progress log

## Exceptions & edge cases

- Until resolved, implementers use the suggested fix as the default and flag it in their PR description

## Cardinal rules (do NOT)

- Do NOT resolve by silently picking a looser (less safe) value; when in doubt choose the stricter option.
- Do NOT edit WORM records to "fix" data; append a correction instead.

## Doc sync on completion

- `docs/02-v1-architecture.md`: align with the resolution
- `docs/ui/dashboards/D18-wallets-treasury.md`: align with the resolution
- `docs/13-wallets-treasury-and-onchain.md`: align with the resolution

## Branch & PR

- Branch: `p5/P5-B007-kill-switch-sweep-vs-freeze`
- PR title: `P5-B007: Kill switch: "sweep hot balances" (14 §5) vs "treasury moves frozen" (D18, F6)`

## Progress log

- 2026-10-21 00:00 · planner · opened
- 2026-10-22 00:00 · aligner · aligned for docs/16–17: Decided (17 §B P5-B007): kill stops new trading, cancels orders, applies each bot's failure policy, freezes new treasury/earn moves and, from P5 (default on), sweeps hot trading balances to the vault address; sweeps to the vault and approval revokes are protective and exempt from the freeze. Docs checked: 13 §1 rules (kill switch), 02 F6 (from P5 hot balances sweep; protective sweeps/revokes exempt), 14 §5 rung 6, D18 rules (kill ON), roadmap R5.07/R5.N2. Implementation owned by P5-T028 (kill sweep, `kill_sweep_enabled` default true), P5-T058 (drill), P5-T012 (setting)
- 2026-10-22 02:10 · cloud:vm:be04b6ae61f8 · verified: decided in docs/17 (17 §B P5-B007); docs updated: 13 §1 rules (kill switch), 02 F6 (from P5 hot balances sweep; protective sweeps/revokes exempt), 14 §5 rung 6, D18 rules (kill ON), roadmap R5.07/R5.N2; implementation owned by P5-T028 (kill sweep, `kill_sweep_enabled` default true), P5-T058 (drill), P5-T012 (setting)
- 2026-10-22 02:10 · cloud:vm:be04b6ae61f8 · done
- 2026-10-22 02:10 · cloud:vm:be04b6ae61f8 · doc sync done: docs updated in the alignment wave
