---
id: P1-B019
kind: gap
title: USDA QuickStats needs a free API key that T0.10 does not list
phase: 1
type: DOC
status: done
priority: medium
size: S
severity: S3
owner: agent
claimed_by: ""
depends_on: []
requirements: [R1.06]
roadmap_todos: [T1.24]
modules: [M1]
dashboards: []
tools: []
mcp: []
env: []
services: []
branch: p1/P1-B019-usda-quickstats-key-missing
pr: ""
doc_sync: [docs/roadmap/phase-0-foundations.md, docs/06-aggregators-and-market-providers.md, docs/03-build-spec.md]
doc_sync_status: done
found_in: docs/roadmap/phase-0-foundations.md T0.10; docs/03-build-spec.md M1
created: 2026-10-22
updated: 2026-10-22
started: ""
completed: 2026-10-22
blocked_reason: ""
checkpoint: ""
review_result: ""
---

# P1-B019 · USDA QuickStats needs a free API key that T0.10 does not list

## Goal / expected outcome

The docs say whether USDA data is loaded keyless (WASDE report files only) or via the QuickStats API with a free key, and if the key is needed, the P0 key list (T0.10) and the secrets file name it, so the commodities flow (P1-T026) and its live check (P1-T073) have a defined input.

## Context & references

- Found in: [03 M1](../../../docs/03-build-spec.md#m1-market--macro-data--mt_datamarket) ("USDA (WASDE/QuickStats)") vs [P0 roadmap T0.10](../../../docs/roadmap/phase-0-foundations.md) (free key list: FRED, EIA, Myfxbook, CoinGecko Demo, CryptoRank Sandbox, Helius, Alchemy, GoPlus, Finnhub, CryptoPanic; no USDA)
- Related requirement: [R1.06](../../../docs/roadmap/phase-1-data-and-monitoring.md#3-requirements) · ToDo T1.24 · tasks P1-T026 (build), P1-T073 (live check)
- Source list: [06 §3 Reports, nowcasts & forecasts](../../../docs/06-aggregators-and-market-providers.md#reports-nowcasts--forecasts-m6-features-m5-release-events) (USDA WASDE)

## Requirements

- **Steps to reproduce:** read 03 M1 (QuickStats named) and T0.10 (no USDA key); the NASS QuickStats API requires a free key requested by email
- **Expected:** either (a) USDA = WASDE report files only (keyless) and 03 M1 drops "QuickStats", or (b) T0.10 adds a free USDA NASS QuickStats key (`USDA_QUICKSTATS_API_KEY` in the sops file) and P1-T073 checks it live
- **Actual:** QuickStats is named but no USER task obtains its key
- **Suggested fix:** (b): add the key to T0.10 (it is free and needs only an email); until then P1-T026 ships QuickStats disabled with the reason and loads WASDE keylessly
- **Impact:** S3: no QuickStats series until decided; WASDE, EIA, COT and Baker Hughes unaffected

## ToDo

- [x] Decided (b): free USDA NASS QuickStats key, recorded via 17 §E (configurable/free inputs follow the suggested fix)
- [x] Edited 03 M1, P0 roadmap T0.10 and 06 §3 (WASDE keyless; QuickStats with a free key)
- [x] P0-T010 (adds `usda_quickstats` / `USDA_QUICKSTATS_API_KEY`), P1-T026 (fixtures) and P1-T073 (live check) updated

## Verification

### Tests

- Doc review: 03 M1, 06 §3 and T0.10 agree; P1-T026 shows QuickStats either keyed or out of scope

### Scenarios

- Given a developer picks up P1-T026 cold, when they read the docs, then they know whether QuickStats needs a key and where it comes from

### Stress / failure injection

- n/a: documentation gap

## Acceptance criteria

- [x] Decision recorded (suggested fix (b), per 17 preamble) and the docs updated
- [x] P1-T026 and P1-T073 match the decision

## Exceptions & edge cases

- Until decided, P1-T026 loads WASDE keylessly and keeps QuickStats disabled with a visible reason in D07

## Cardinal rules (do NOT)

- Do NOT resolve by silently picking an option in code; the decision lands in the docs first
- Do NOT use a paid data source as a substitute ([03 §1](../../../docs/03-build-spec.md#1-ground-rules))

## Doc sync on completion

- `docs/roadmap/phase-0-foundations.md` T0.10: add the key if (b)
- `docs/06-aggregators-and-market-providers.md` §3 and `docs/03-build-spec.md` M1: state the USDA access path

## Branch & PR

- Branch: `p1/P1-B019-usda-quickstats-key-missing`
- PR title: `P1-B019: Define USDA QuickStats access (free key or WASDE only)`

## Progress log

- 2026-10-22 00:00 · aligner · opened during docs/16–17 task alignment; owned by P1-T026 (keyless WASDE meanwhile) and P1-T073 (live check once decided)
- 2026-10-22 00:00 · wrap-up doc agent · closed in the wrap-up: suggested fix (b) adopted; T0.10, 03 M1, 06 §3 and P0-T010/P1-T026/P1-T073 name the free QuickStats key
- 2026-10-22 02:30 · cloud:vm:be04b6ae61f8 · verified: docs/roadmap/phase-0-foundations.md T0.10, docs/03-build-spec.md M1, docs/06 §3 (USDA QuickStats free key); P0-T010, P1-T026, P1-T073 updated
- 2026-10-22 02:30 · cloud:vm:be04b6ae61f8 · done
- 2026-10-22 02:30 · cloud:vm:be04b6ae61f8 · doc sync done: docs updated in the wrap-up
