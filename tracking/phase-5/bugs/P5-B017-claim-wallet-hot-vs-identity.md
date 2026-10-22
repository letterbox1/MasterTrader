---
id: P5-B017
kind: gap
title: Autonomous claims: "hot wallet" (08, D12) vs "airdrop identity wallet" (03 M4, R5.15)
phase: 5
type: DOC
status: done
priority: medium
size: XS
severity: S3
owner: agent
claimed_by: ""
depends_on: []
requirements: [R5.15, R5.17]
roadmap_todos: []
modules: [M4, M22]
dashboards: [D12]
tools: []
mcp: []
env: []
services: []
branch: p5/P5-B017-claim-wallet-hot-vs-identity
pr: ""
doc_sync: [docs/08-airdrops-and-token-launches.md, docs/ui/dashboards/D12-airdrops.md]
doc_sync_status: done
found_in: "docs/08-airdrops-and-token-launches.md §What may run autonomously; docs/ui/dashboards/D12-airdrops.md /airdrops/wallet"
created: 2026-10-21
updated: 2026-10-22
started: ""
completed: 2026-10-22
blocked_reason: ""
checkpoint: ""
review_result: ""
---

# P5-B017 · Autonomous claims: "hot wallet" (08, D12) vs "airdrop identity wallet" (03 M4, R5.15)

## Goal / expected outcome

All docs say auto-claims run from the chain's airdrop identity wallet (signer-held, capped), with burners for vetting, and D12's wallet page covers identity + burner wallets.

## Context & references

- 08 item 2: "Claiming an airdrop your hot wallet is already eligible for"; D12 "hot wallet & mandates"
- 03 M4 and R5.15: "eligible claims from the chain's airdrop identity wallet"; 13 §1 separates hot (trading) from identity
- Tasks P5-T043/T044 use identity wallets

## Requirements

- **Steps to reproduce:** Compare 08, D12, 03 M4 and 13 §1.
- **Expected:** Identity wallet named consistently.
- **Actual:** Mixed terminology.
- **Suggested fix:** Replace "hot wallet" with "airdrop identity wallet (signer-held)" in 08 and D12; keep "hot" for trading.
- **Impact:** S3: could route claims through the trading hot wallet, breaking wallet separation for tax.

## ToDo

- [x] Resolution per 17 §B (airdrop identity wallet, never the hot trading wallet)
- [x] 02 §2 system-context diagram relabelled 'airdrop identity-wallet claims' (08, D12, 03 M4, 13 §1 already agree)
- [x] P5-T004/T006/T041/T044/T053 already use identity wallets

## Verification

### Tests
- Doc review: every listed doc states the same value/name after the fix; `python3 tools/kanban/kanban.py validate` stays at 0 errors

### Scenarios
- Given the fixed docs, when a developer picks up the affected P5 tasks, then there is exactly one authoritative answer to follow

### Stress / failure injection
- n/a: documentation/spec gap

## Acceptance criteria

- [x] Docs listed under Doc sync are consistent
- [x] Affected P5 tasks reference the resolved value/name
- [x] Resolution recorded in the progress log

## Exceptions & edge cases

- Until resolved, implementers use the suggested fix as the default and flag it in their PR description

## Cardinal rules (do NOT)

- Do NOT resolve by silently picking a looser (less safe) value; when in doubt choose the stricter option.
- Do NOT edit WORM records to "fix" data; append a correction instead.

## Doc sync on completion

- `docs/08-airdrops-and-token-launches.md`: align with the resolution
- `docs/ui/dashboards/D12-airdrops.md`: align with the resolution

## Branch & PR

- Branch: `p5/P5-B017-claim-wallet-hot-vs-identity`
- PR title: `P5-B017: Autonomous claims: "hot wallet" (08, D12) vs "airdrop identity wallet" (03 M4, R5.15)`

## Progress log

- 2026-10-21 00:00 · planner · opened
- 2026-10-22 00:00 · aligner · left open: 17 §B records the decision (autonomous claims use the chain's airdrop identity wallet, never the hot trading wallet) and 08, D12, 03 M4, 13 §1, 07 §4 and 02 F8 carry it, but the 02 §2 system-context diagram still labels chain access "hot-wallet claims only" (docs/02-v1-architecture.md line 55). Needs that label changed to identity-wallet claims. Implementation owned by P5-T041/P5-T044 (identity wallet only) and tested in P5-T053
- 2026-10-22 00:00 · wrap-up doc agent · closed in the wrap-up: 02 §2 diagram label fixed; all docs name the airdrop identity wallet
- 2026-10-22 02:30 · cloud:vm:be04b6ae61f8 · verified: docs/02-v1-architecture.md §2 diagram (airdrop identity-wallet claims); 08, D12, 03 M4 already aligned
- 2026-10-22 02:30 · cloud:vm:be04b6ae61f8 · done
- 2026-10-22 02:30 · cloud:vm:be04b6ae61f8 · doc sync done: docs updated in the wrap-up
