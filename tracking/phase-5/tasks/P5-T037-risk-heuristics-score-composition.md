---
id: P5-T037
kind: task
title: Risk heuristics (solana-rugchecker, CRPWarner concepts, EVM/Solana features) and 0–100 score
phase: 5
type: BUILD
status: backlog
priority: high
size: L
severity: ""
owner: agent
claimed_by: ""
depends_on: [P5-T036]
requirements: [R5.13]
roadmap_todos: [T5.26]
modules: [M4]
dashboards: [D12]
tools: [uv, docker]
mcp: []
env: []
services: []
branch: p5/P5-T037-risk-heuristics-score-composition
pr: ""
doc_sync: [docs/08-airdrops-and-token-launches.md, docs/roadmap/phase-5-airdrops-wallets-curation.md]
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

# P5-T037 · Risk heuristics (solana-rugchecker, CRPWarner concepts, EVM/Solana features) and 0–100 score

## Goal / expected outcome

A deterministic, explainable risk score 0–100 combines re-implemented solana-rugchecker signals, CRPWarner concepts (hidden mint, limiting sell order, leaking token), EVM contract features, Solana token features (incl. Token-2022 extensions), liquidity, distribution, deployer, market and off-chain features, emitting top-3 reasons for D12 and tasks.

## Context & references

- Roadmap: [R5.13](../../../docs/roadmap/phase-5-airdrops-wallets-curation.md) · ToDo T5.26
- [08 scored features](../../../docs/08-airdrops-and-token-launches.md#risk-score-0100-any-hard-fail--100--reject) · [research: solana-rugchecker signals and CRPWarner](../../../docs/research/airdrops-rugpull-discord.md)
- Rule-based baseline is authoritative; the calibrated model (P5-T039) is advisory

## Requirements

- solana-rugchecker signals: mint authority (+80), freeze authority (+65), mutable metadata (+50), top-20 holders ≥ 50/35/20% (+80/60/50) excluding Raydium authority, LP < 95% burned (+80), large individual holders — plus our additions (Token-2022 transfer-fee, permanent delegate, transfer hook, default frozen; LP lockers; creator history).
- EVM: owner not renounced with privileged functions, hidden mint/balance changes, blacklist/trading pause, modifiable taxes, upgradeable proxy with EOA admin and no timelock, `selfdestruct`/mutable `delegatecall`; optional Slither high findings on verified source (AGPL CLI, sandboxed).
- Liquidity (LP burned/locked % and expiry, liquidity USD, liquidity/FDV, pair age), distribution (top-10/20 excl. pools/lockers/burn, deployer share), deployer (age, prior tokens and rug count, mixer funding), market (wash patterns, liquidity pulls), off-chain (domain age, social age/consistency, allow-listed audit firm, docs exist, template site).
- Composition: weighted, capped at 99 unless a hard fail (100); weights in versioned config; each feature contributes a signed reason; score version stored on the report.
- Optional Gigahorse deep-scan worker: sandboxed (`--network none`), off by default.

## ToDo

- [ ] Implement feature extractors in `packages/mt_airdrop/risk/features/` (evm.py, solana.py, liquidity.py, distribution.py, deployer.py, offchain.py).
- [ ] Implement `risk/score.py` composition with explanation output and config versioning.
- [ ] Optional `risk/deep_scan/` worker container definition (disabled).
- [ ] Golden tests per feature and end-to-end score snapshots; doc sync.

## Verification

### Tests
- Unit: each feature extractor on fixtures (one positive, one negative).
- Golden: score snapshots for 20 fixture tokens (10 known rugs from SoK, 10 established tokens) stable across runs.
- Property: adding a risk flag never lowers the score.

### Scenarios
- Given a Solana token with mint authority active and top-20 holding 60%, then score ≥ 80 with those two as top reasons.
- Given an EVM proxy whose admin is an EOA with no timelock, then the reason appears in the top 3 and autonomous paths are blocked by policy.

### Stress / failure injection
- Score 1,000 tokens from cached enrichment in < 60 s.

## Acceptance criteria

- [ ] All 08 feature groups implemented
- [ ] Score deterministic with top-3 reasons
- [ ] Weights versioned
- [ ] Golden tests green

## Exceptions & edge cases

- Missing feature data scores as risk (conservative default), flagged `data_missing`.

## Cardinal rules (do NOT)

- Do NOT use Telegram-derived postures as model features; they may only feed deterministic rules (12 §4).
- Do NOT vendor solana-rugchecker code (no clear licence) — reimplement from the feature list.
- Do NOT let Telegram text reach any model, RAG index or training set; Telegram contributes deterministic postures only (12 §4–5).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.

## Doc sync on completion

- `docs/08-airdrops-and-token-launches.md`: weights table and score version.
- `docs/roadmap/phase-5-airdrops-wallets-curation.md`: tick T5.26 when this lands (with the other tasks sharing that ToDo).

## Branch & PR

- Branch: `p5/P5-T037-risk-heuristics-score-composition`
- PR title: `P5-T037: Risk heuristics (solana-rugchecker, CRPWarner concepts, EVM/Solana features) and 0–100 score`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P5-T037` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (run fields; content already matches 08 risk score)
