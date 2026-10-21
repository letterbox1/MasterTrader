---
id: P5-T043
kind: task
title: Mandates (C3 create, C1 revoke, expiry) and public-address eligibility checker
phase: 5
type: BUILD
status: backlog
priority: critical
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P5-T010, P5-T011, P5-T012, P5-T042]
requirements: [R5.15]
roadmap_todos: [T5.28]
modules: [M4, M22]
dashboards: [D12]
branch: p5/P5-T043-mandates-eligibility-checker
pr: ""
doc_sync: [docs/08-airdrops-and-token-launches.md, docs/roadmap/phase-5-airdrops-wallets-curation.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P5-T043 · Mandates (C3 create, C1 revoke, expiry) and public-address eligibility checker

## Goal / expected outcome

`airdrop.mandate.create` (C3) and `airdrop.mandate.revoke` (C1) manage WORM mandates — one wallet, one chain, allow-listed contracts + function selectors, gas/value caps, max claims/day, expiry — and an eligibility checker proves claims using only the **public address** against official Merkle proofs or claim-contract view functions (`isClaimed`, allocation).

## Context & references

- Roadmap: [R5.15](../../../docs/roadmap/phase-5-airdrops-wallets-curation.md) · ToDo T5.28 · USER P5-T006
- [08 what may run autonomously](../../../docs/08-airdrops-and-token-launches.md#what-may-run-autonomously) · [D12 /airdrops/wallet](../../../docs/ui/dashboards/D12-airdrops.md) · WORM table P5-T010 · [15 §2](../../../docs/15-bots-hitl-and-worm-audit.md#2-worm-records-write-once-read-many)

## Requirements

- Create validation: wallet tier = identity (or burner for burner runs); contracts verified; selectors decode to claim-type functions (no approve/permit/transfer-out — NA checks); `msg.value` cap = 0; expiry ≤ 90 days; gas cap within custody caps.
- C3 flow: preview in D12 → Telegram approve + TOTP → cool-down (default 15 min) → `created` row; revoke = immediate `revoked` row (C1); expiry job appends `expired` rows.
- Signer allow-list for the wallet derives from the union of active mandates (tighten on revoke/expiry within 1 min).
- Eligibility: fetch official Merkle tree/proof from the official domain (verified link) or call view functions via RPC with the public address; record proof hash and amount; never connect a wallet or post the address to third-party "checkers".
- Queries `/airdrops/mandates`, `/airdrops/wallet`.

## ToDo

- [ ] Implement `packages/mt_airdrop/mandates/` (model, validation, commands, expiry job, allow-list sync to signer).
- [ ] Implement `packages/mt_airdrop/eligibility/` (merkle.py with keccak/sha256 tree variants, claim_contract.py).
- [ ] Tests incl. C3 flow (reusing P0 confirmation tests) and WORM behaviour; doc sync.

## Verification

### Tests
- Unit: mandate validation rejects approve selector, non-zero value, expiry > 90 days, vault wallet.
- Integration: C3 create applies only after approve + TOTP + cool-down; revoke tightens the signer allow-list within 1 min.
- Unit: Merkle proof verification against OpenZeppelin MerkleProof test vectors and a real distributor fixture.

### Scenarios
- Given an expired mandate, when the executor polls, then it sees `expired` and no claim is attempted.
- Given the official Merkle JSON is hosted on a domain ≠ official domain, then eligibility = `unverified_source` and the path is CLAIM_MANUAL.

### Stress / failure injection
- n/a: low-volume admin path; signer allow-list sync tested under P5-T062

## Acceptance criteria

- [ ] Mandate lifecycle (create/revoke/expire) on WORM rows
- [ ] C3/C1 levels enforced
- [ ] Signer allow-list follows mandates
- [ ] Eligibility via public address only

## Exceptions & edge cases

- Cool-down interrupted by kill switch ON: mandate stays pending until kill OFF (C3).

## Cardinal rules (do NOT)

- Do NOT submit the user's address to third-party eligibility checker sites (08 never automated).
- Do NOT apply loosening (new mandate, higher caps, autonomous claims) without C3 (Telegram approve + TOTP + cool-down); protective actions (revoke, sweep, kill) never wait for approval.
- Do NOT UPDATE or DELETE WORM rows (`curation.mandate`, `curation.exec_log`, the signer ledger, `journal.*`, `audit.*`); corrections are new rows with `supersedes_id` (15 §2).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.

## Doc sync on completion

- `docs/08-airdrops-and-token-launches.md`: mandate fields and validation rules.
- `docs/roadmap/phase-5-airdrops-wallets-curation.md`: tick T5.28 when this lands (with the other tasks sharing that ToDo).

## Branch & PR

- Branch: `p5/P5-T043-mandates-eligibility-checker`
- PR title: `P5-T043: Mandates (C3 create, C1 revoke, expiry) and public-address eligibility checker`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P5-T043` run

## Progress log

- 2026-10-21 00:00 · planner · created
