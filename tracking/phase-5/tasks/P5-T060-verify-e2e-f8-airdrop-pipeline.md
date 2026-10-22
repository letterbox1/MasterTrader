---
id: P5-T060
kind: task
title: End-to-end F8 scenarios: scam rejected with reasons, task, watch and auto-claim
phase: 5
type: VERIFY
status: backlog
priority: high
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P5-T033, P5-T041, P5-T044, P5-T045, P5-T046, P5-T048, P5-T068]
requirements: [R5.10, R5.11, R5.12, R5.13, R5.14, R5.17]
roadmap_todos: []
modules: [M4, M19]
dashboards: [D12, D13]
tools: [uv, pnpm, anvil]
mcp: []
env: [GOPLUS_API_KEY, CRYPTORANK_API_KEY, COINGECKO_DEMO_API_KEY, HELIUS_API_KEY, ALCHEMY_API_KEY]
services: [postgres, nats, goplus, cryptorank, coingecko, helius, alchemy]
branch: p5/P5-T060-verify-e2e-f8-airdrop-pipeline
pr: ""
doc_sync: [docs/roadmap/phase-5-airdrops-wallets-curation.md]
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

# P5-T060 · End-to-end F8 scenarios: scam rejected with reasons, task, watch and auto-claim

## Goal / expected outcome

A scenario suite drives the whole F8 flow from discovery to journal with recorded fixtures: a known scam (honeypot + clustered supply + lookalike domain) is rejected with all reasons visible in D12; a legitimate points programme becomes a task with verified links and EV; a single-source rumour stays in watch; an eligible claim auto-executes; a fresh launch is default-rejected; an AU-excluded ICO is excluded before any task.

## Context & references

- Roadmap: R5.10–R5.14, R5.17 · exit criterion 2 ("a scam rejected with reasons")
- [02 F8](../../../docs/02-v1-architecture.md#8-end-to-end-flows) · [08 pipeline](../../../docs/08-airdrops-and-token-launches.md#pipeline) · [D12 acceptance](../../../docs/ui/dashboards/D12-airdrops.md)

## Requirements

- Fixtures: recorded API responses for 8 projects (scam EVM, scam Solana Pump.fun-style, legit points, rumour, eligible claim, fresh launch, AU-excluded ICO, burner-first protocol).
- Each scenario asserts the stage reached, the decision, reasons, tasks created (type, links verified), and records. The eligible-claim scenario also asserts the identity wallet was used and a manual-sale disposal task was created (no automated sale; P5-B010, P5-B017).
- Unhappy paths: provider outage mid-run (risk `incomplete` → no autonomy), blocklist update mid-run (task link becomes plain text).
- Runs in CI nightly (fixtures, no keys) and once on live free APIs (manual) for the demo, after the keys-last check P5-T068.

## ToDo

- [ ] Build fixture set under `tests/scenarios/f8/` (sanitised, no dataset redistribution).
- [ ] Write scenario tests with D12 Playwright assertions for reasons/links.
- [ ] Run live once; record outcomes.

## Verification

### Tests
- Scenario suite (≥ 10 scenarios) + Playwright assertions.

### Scenarios
- Given the scam fixture, then D12 shows hard fails: sell simulation failed, cluster holds 45% of supply, domain lookalike — and no task is created.
- Given the burner-first protocol, then the first task uses the burner and the identity task appears only after a clean run.

### Stress / failure injection
- Run the 8 projects × 50 copies (400 opportunities) through the pipeline: completes < 15 min within mocked quotas.

## Acceptance criteria

- [ ] All scenarios pass in CI
- [ ] Live run recorded with a scam rejected with reasons
- [ ] Unhappy paths behave as specified

## Exceptions & edge cases

- Fixture drift vs live APIs: live run differences logged, fixtures refreshed.

## Cardinal rules (do NOT)

- Do NOT weaken risk thresholds to make a scenario pass.
- Do NOT let Telegram text reach any model, RAG index or training set; Telegram contributes deterministic postures only (12 §4–5).
- Do NOT add paid data/APIs or scraping that breaks terms; no self-bots or user tokens; no sybil, multi-wallet or fake-engagement patterns.
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.

## Doc sync on completion

- No doc change beyond ticking verification of R5.10–R5.14/R5.17.
- `docs/roadmap/phase-5-airdrops-wallets-curation.md`: tick the related exit criterion when this lands (with the other tasks sharing that ToDo).

## Branch & PR

- Branch: `p5/P5-T060-verify-e2e-f8-airdrop-pipeline`
- PR title: `P5-T060: End-to-end F8 scenarios: scam rejected with reasons, task, watch and auto-claim`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P5-T060` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (live run after P5-T068 with env names only; identity wallet + manual disposal asserted)
