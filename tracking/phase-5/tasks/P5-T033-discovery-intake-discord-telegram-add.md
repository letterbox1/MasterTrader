---
id: P5-T033
kind: task
title: Discovery intake: Discord inbox classification, Telegram postures, news and /add <url>
phase: 5
type: BUILD
status: backlog
priority: high
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P5-T032, P4-T019, P4-T020, P4-T025, P4-T028]
requirements: [R5.10]
roadmap_todos: [T5.25]
modules: [M4, M2]
dashboards: [D12]
tools: [uv]
mcp: []
env: []
services: [nats, postgres]
branch: p5/P5-T033-discovery-intake-discord-telegram-add
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

# P5-T033 · Discovery intake: Discord inbox classification, Telegram postures, news and /add <url>

## Goal / expected outcome

Airdrop candidates also arrive from the P4 Discord inbox (followed announcement posts classified as airdrop / snapshot / claim live / phishing warning), Telegram **postures** (regex-extracted addresses and mention counts only), news/RSS items and manual `/add <url>` (Telegram or `airdrop.add_url`), all normalised into `source_observation`.

## Context & references

- Roadmap: [R5.10](../../../docs/roadmap/phase-5-airdrops-wallets-curation.md) · ToDo T5.25
- P4 prerequisites: Discord bot ingest (P4-T020), Telegram postures (P4-T019; table `text.telegram_posture`, subject `posture.telegram.*`, 17 §D P4-B002), provenance gate (P4-T025), tier B question registry (P4-T028)
- [08 autonomous 4](../../../docs/08-airdrops-and-token-launches.md#what-may-run-autonomously) (Discord classification) · [12 §4](../../../docs/12-policy-and-compliance.md#4-per-platform-data--automation-rules) (Telegram)

## Requirements

- Discord: consume P4 `text.doc.new` for docs from the Discord source; classify with rules + the P4 tier B relevance gate (Discord text is model-eligible); labels: airdrop_announce, snapshot, claim_live, phishing_warning, other.
- Telegram: consume only posture tables (address, channel count, mention velocity, new-channel share, time since first call); rows keep `model_input_ok=false`; no message text read.
- News/RSS: P4 documents tagged crypto + airdrop/launch entities.
- `/add <url>`: resolve URL → domain → candidate; immediately blocklist-checked; result reply in Telegram.
- A `phishing_warning` for a tracked project triggers an instant alert (P5-T030).

## ToDo

- [ ] Implement `packages/mt_airdrop/discover/intake_discord.py`, `intake_telegram_postures.py`, `intake_news.py`, `add_url.py`.
- [ ] Rule-based classifier + tier B question `airdrop_announce_type` registered in the P4 question registry.
- [ ] Command handler `airdrop.add_url` (C0) and Telegram `/add`.
- [ ] Provenance gate test (Telegram rows never passed to tier B); doc sync.

## Verification

### Tests
- Unit: classifier golden set (30 labelled Discord posts) ≥ 90% accuracy on claim_live/phishing_warning.
- Integration: a Telegram posture row cannot be sent to the tier B client (provenance gate raises).
- Integration: `/add https://example.org` creates a candidate and replies with blocklist status.

### Scenarios
- Given an announcement "Claim is live at claim.project.xyz" whose domain ≠ official domain, then the candidate is created with a domain-mismatch flag (hard fail later).
- Given a Telegram posture spike for an address with no other source, then the candidate is `watch` only (< 2 sources).

### Stress / failure injection
- Burst of 1,000 Discord posts in 10 min (launch day): processed < 15 min, no backlog growth after.

## Acceptance criteria

- [ ] Four intake paths live
- [ ] Telegram text never reaches any model (test)
- [ ] `/add` works from Telegram and UI

## Exceptions & edge cases

- P4 decision-svc down: rules-only classification with `degraded` flag.

## Cardinal rules (do NOT)

- Do NOT read or store Telegram message text in M4; postures only.
- Do NOT use user tokens or self-bots for Discord.
- Do NOT let Telegram text reach any model, RAG index or training set; Telegram contributes deterministic postures only (12 §4–5).
- Do NOT add paid data/APIs or scraping that breaks terms; no self-bots or user tokens; no sybil, multi-wallet or fake-engagement patterns.
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.

## Doc sync on completion

- `docs/08-airdrops-and-token-launches.md`: intake paths and labels.
- `docs/roadmap/phase-5-airdrops-wallets-curation.md`: tick T5.25 when this lands (with the other tasks sharing that ToDo).

## Branch & PR

- Branch: `p5/P5-T033-discovery-intake-discord-telegram-add`
- PR title: `P5-T033: Discovery intake: Discord inbox classification, Telegram postures, news and /add <url>`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P5-T033` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (explicit P4 deps; Telegram postures only per 02 F3/P4-B001)
