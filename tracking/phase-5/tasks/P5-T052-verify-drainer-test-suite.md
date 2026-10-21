---
id: P5-T052
kind: task
title: Drainer test suite: every drainer pattern refused
phase: 5
type: VERIFY
status: backlog
priority: critical
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P5-T014, P5-T015, P5-T016, P5-T042, P5-T044]
requirements: [R5.03, R5.16, R5.02]
roadmap_todos: [T5.60]
modules: [M22, M4]
dashboards: []
branch: p5/P5-T052-verify-drainer-test-suite
pr: ""
doc_sync: [docs/07-security-notes.md, docs/roadmap/phase-5-airdrops-wallets-curation.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P5-T052 · Drainer test suite: every drainer pattern refused

## Goal / expected outcome

A dedicated CI suite (`tests/drainer/`) proves end to end — through `mt_api`/executor → signer → simulation — that permit, Permit2, `setApprovalForAll`, unlimited approval, unknown router, "claim fee" to an EOA, foreign durable nonce (plus SetAuthority/SPL Approve, EIP-712/`personal_sign`, non-gas outflow in simulation) are all refused, ledgered and surfaced. This is exit criterion 3.

## Context & references

- Roadmap: ToDo T5.60 → R5.03, R5.16 · exit criterion 3 ([§6](../../../docs/roadmap/phase-5-airdrops-wallets-curation.md))
- [13 §2](../../../docs/13-wallets-treasury-and-onchain.md#2-signer-service-the-only-process-that-sees-hot-keys) · [08 never automated](../../../docs/08-airdrops-and-token-launches.md#never-automated) · [research threat context](../../../docs/research/airdrops-rugpull-discord.md) (forged Permit and fake checkers dominate)

## Requirements

- Each case runs as a full-path integration test on Anvil fork / `solana-test-validator` with malicious mock contracts/programs.
- Cases: EIP-2612 permit; Permit2 permit/permitTransferFrom/permitBatch; `setApprovalForAll`; `approve(max)`; `increaseAllowance` large; unknown router swap; claim requiring `msg.value` fee; claim that transfers a fee to an EOA; claim whose simulation shows USDC outflow; EIP-712 typed-data request; `personal_sign` arbitrary payload; SIWE on unknown domain; Solana foreign `SetAuthority`; SPL `Approve` not built by us; foreign `AdvanceNonceAccount`; `AuthorizeNonceAccount`; unknown program ID.
- Assertions: refused with the expected rule/NA ID; no signature produced (ledger shows refusal); no broadcast; a task/alert surfaced where specified.
- Suite runs on every PR touching `mt_signer`, `mt_airdrop.exec` or `mt_core.policy` and nightly.

## ToDo

- [ ] Write malicious mock contracts (Foundry) and Solana test programs under `tests/drainer/fixtures/`.
- [ ] Write the parametrised suite with one case per pattern.
- [ ] Add CI job (required check) and nightly schedule.
- [ ] Record results in the progress log; update 07 §4 with the suite reference.

## Verification

### Tests
- The suite itself (≥ 17 cases), plus a meta-test that fails if a case is skipped or xfail'd.

### Scenarios
- Given a fake "eligibility checker" contract that requests Permit2 for USDC, when an intent targets it, then refusal `EVM-PERMIT2` and NA-03, no signature.
- Given a claim whose simulation shows −5 USDC besides gas, then refusal `SIM-OUTFLOW`, CLAIM_MANUAL task with that reason.

### Stress / failure injection
- Run the suite 20× in a loop to detect flakiness; 0 flaky failures allowed.

## Acceptance criteria

- [ ] All cases refused with expected IDs
- [ ] Required CI check on relevant paths
- [ ] Meta-test prevents skipping
- [ ] Results logged

## Exceptions & edge cases

- New drainer pattern discovered later: add a case first (failing), then fix (bug item).

## Cardinal rules (do NOT)

- Do NOT mark any drainer case skip/xfail to get green.
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.
- Do NOT give any LLM, agent or MCP path a route to keys, the signer socket or the `signer` network (R5.N1).

## Doc sync on completion

- `docs/07-security-notes.md` §4: reference the drainer suite and its case list.
- `docs/roadmap/phase-5-airdrops-wallets-curation.md`: tick T5.60 when this lands (with the other tasks sharing that ToDo).

## Branch & PR

- Branch: `p5/P5-T052-verify-drainer-test-suite`
- PR title: `P5-T052: Drainer test suite: every drainer pattern refused`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P5-T052` run

## Progress log

- 2026-10-21 00:00 · planner · created
