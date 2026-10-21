---
id: P0-T010
kind: task
title: Register the free data API keys
phase: 0
type: USER
status: ready
priority: medium
size: M
severity: ""
owner: user
claimed_by: ""
depends_on: []
requirements: []
roadmap_todos: [T0.10]
modules: [M1, M2, M4, M5]
dashboards: []
branch: p0/P0-T010-free-data-api-keys
pr: ""
doc_sync: [docs/06-aggregators-and-market-providers.md, docs/roadmap/phase-0-foundations.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P0-T010 · Register the free data API keys

## Goal / expected outcome

Free-tier API keys exist for FRED, EIA, Myfxbook, CoinGecko Demo, CryptoRank Sandbox, Helius, Alchemy, GoPlus, Finnhub and CryptoPanic, each registered once, recorded with its free-tier limits, and stored in the secrets file.

## Context & references

- [Roadmap P0 T0.10](../../../docs/roadmap/phase-0-foundations.md#4-todo-sets)
- [06 data sources](../../../docs/06-aggregators-and-market-providers.md)
- [04 do-this-week](../../../docs/04-plan-of-action.md#️-do-this-week-regardless-of-phase)
- [12 §4 platform rules](../../../docs/12-policy-and-compliance.md#4-per-platform-data--automation-rules)
- [03 §1 ground rules](../../../docs/03-build-spec.md#1-ground-rules) (quota tracker throttles before each limit)
- Unblocks: P1 connectors, P4/P5 enrichment

## Requirements

- One account per provider (12 §4: no multi-accounting, no key multiplexing).
- Record each key's free limit (e.g. Myfxbook 100 calls/day; Finnhub 60 calls/min; CoinGecko Demo cache ≤ 24 h with attribution) in the log for P1's quota tracker.
- Blockscout needs no key; Etherscan is manual lookups only (never a decision input); Anvil is local.
- Outputs → the sops secrets file `/etc/mastertrader/secrets.sops.yaml` (created by the secrets task, P0-T022) under `data_keys:` (`fred`, `eia`, `myfxbook`, `coingecko_demo`, `cryptorank`, `helius`, `alchemy`, `goplus`, `finnhub`, `cryptopanic`). Until the secrets file exists, keep values **only** in your password manager; never in chat, email, git, issues or notes apps.

## ToDo

- [ ] Register each provider with a dedicated email alias; log 'done' + the free limit per provider.
- [ ] Note attribution requirements (CoinGecko, CryptoPanic).
- [ ] Store keys in the password manager; move to the secrets file after P0-T022.

## Verification

### Tests
- Confirmation: one manual call per key from the host via `sops exec-env` (so keys never hit shell history) returns 200.

### Scenarios
- Given a provider changes its free tier, then log it; P1's monthly ToS check (04 standing rules) picks it up.

### Stress / failure injection
- n/a: account action.

## Acceptance criteria

- [ ] 10 keys registered (or a logged reason per missing one)
- [ ] Free limits logged for the quota tracker
- [ ] Keys only in password manager / secrets file

## Exceptions & edge cases

- A provider requires a card for the free tier: skip it and log; never upgrade to a paid tier.

## Cardinal rules (do NOT)

- Do NOT create second accounts to raise limits.
- Do NOT sign up for paid plans or trials that auto-convert.
- Do NOT commit secrets or paste them into chats, issues, PRs or logs; secrets live only in the sops/age file ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Do NOT add paid data/APIs, ToS-breaking scraping, self-bots or user tokens; free tiers only ([03 §1](../../../docs/03-build-spec.md#1-ground-rules)).

## Doc sync on completion

- `docs/06-aggregators-and-market-providers.md`: correct any free-limit numbers that differ from what you saw.
- `docs/roadmap/phase-0-foundations.md`: tick T0.10 when every item mapped to it is done.

## Branch & PR

- Branch: `p0/P0-T010-free-data-api-keys`
- PR title: `P0-T010: Register the free data API keys`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P0-T010` run

## Progress log

- 2026-10-21 00:00 · planner · created
