---
id: P4-T019
kind: task
title: Telegram regex extractors, posture calculators, Bot API and RSS-Bridge fallback
phase: 4
type: BUILD
status: backlog
priority: critical
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P4-T018, P4-T012]
requirements: [R4.02, R4.03]
roadmap_todos: [T4.21]
modules: [M2]
dashboards: [D08]
branch: p4/P4-T019-telegram-postures
pr: ""
doc_sync: [docs/02-v1-architecture.md, docs/12-policy-and-compliance.md, docs/roadmap/phase-4-intel.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P4-T019 · Telegram regex extractors, posture calculators, Bot API and RSS-Bridge fallback

## Goal / expected outcome

Telegram messages are reduced, in memory, to regex-extracted contract addresses/tickers + counts; these become deterministic **postures** per subject (mention velocity, channel count, new-channel share, time since first call) stored in `text.tg_posture` with `model_input_ok = false`, `train_ok = false`, published on `posture.tg.{subject}` for code/policy consumers (P5 airdrop rules, D08). The Bot API (for channels where your bot is admin) and RSS-Bridge's Telegram bridge feed the same extractor as fallbacks.

## Context & references

- Roadmap: [R4.02, R4.03](../../../docs/roadmap/phase-4-intel.md#3-requirements) · ToDo [T4.21](../../../docs/roadmap/phase-4-intel.md#4-todo-sets)
- Policy: [12 §4](../../../docs/12-policy-and-compliance.md#4-per-platform-data--automation-rules) (allowed: regex-extracted addresses/tickers and counts → postures used by code/policy only; no Telegram-derived feature in a model input) · [12 §5](../../../docs/12-policy-and-compliance.md#5-data-provenance-tagging-one-mechanism-for-all-data-terms)
- UI: [D08 Additions](../../../docs/ui/dashboards/D08-intel.md) (Telegram shown as postures only)
- Gap: P4-B003 (no posture subject/table in 02 §4/§6 yet).
- Cross-phase: P5 R5.10 consumes postures for discovery.

## Requirements

- Extractors: EVM address `0x[a-fA-F0-9]{40}` (checksum-validated), Solana base58 32–44 chars (validated by decoding), cashtags `\$[A-Z]{2,10}`, symbol-master tickers; chain inferred from address format.
- Stored per mention: hashed channel id, message id, ts, extracted value, chain. **No text, no sender, no usernames.**
- Postures per subject over windows 15 m / 1 h / 24 h: `mention_velocity` (mentions/h), `channel_count`, `new_channel_share` (channels first seen < 7 d ago / total), `time_since_first_call`.
- Posture rows carry `source=telegram`, `model_input_ok=false`, `train_ok=false`, `retention_days` = 90 for mentions.
- Publish `posture.tg.{subject}` and maintain KV `tg_posture`; consumers must be deterministic code/policy (P5 rules, D08), **not** M6 features for tier A, tier B, agents or RAG.
- Bot API path: bot updates from admin channels → same extractor; RSS-Bridge `TelegramBridge` for public channels the account can't join (context-only cadence).

## ToDo

- [ ] `extractors.py` with validators + golden test corpus (synthetic messages, no real Telegram text in the repo).
- [ ] `postures.py` sliding-window calculators (pure functions, deterministic).
- [ ] Writers for `text.tg_mention`/`text.tg_posture`; NATS publisher; KV updater.
- [ ] Bot API listener (python-telegram-bot or aiogram, pinned) limited to channel posts.
- [ ] RSS-Bridge Telegram fallback via P4-T012 client.
- [ ] Consumer allow-list: `posture.tg.>` subscribers declared in `config/provenance/consumers.yaml`; CI fails if a model/feature service subscribes.
- [ ] Retention job entry for `text.tg_mention` (90 d).

## Verification

### Tests
- Golden: synthetic message corpus → exact extracted values and posture numbers.
- Property: postures are deterministic and order-independent within a window.
- Unit: invalid checksum EVM address rejected; random base58 noise rejected.
- CI: consumer allow-list check fails if `nlp`, `decision-svc`, `mt_features` or `agents` subscribe to `posture.tg.>`.

### Scenarios
- Given 40 channels mention the same new Solana address within 1 h, 30 of them new, then `new_channel_share = 0.75` and velocity is computed for the 1-h window.
- Given the Telethon client is down, then Bot API and RSS-Bridge keep postures flowing (degraded flag set).

### Stress / failure injection
- Replay 50k synthetic messages/hour: extractor p99 < 2 ms/message, postures update ≤ 1 s behind.

## Acceptance criteria

- [ ] Postures computed and visible via KV/NATS; rows carry `model_input_ok=false`, `train_ok=false`
- [ ] No Telegram text or usernames in any table, log or NATS message (grep/spy test)
- [ ] Consumer allow-list enforced in CI
- [ ] CI green (ruff, mypy, pytest, `pit` bypass check)

## Exceptions & edge cases

- Same address in many chains: store per chain.
- Clock: windows use `ingested_at` from our clock; Telegram message dates only for `time_since_first_call` with a skew guard.

## Cardinal rules (do NOT)

- Do NOT feed postures into M6 features used by tier A/B models, agents or RAG.
- Do NOT log message text, even at debug level.
- Do NOT let Telegram text (or any `model_input_ok = false` row) reach a model, RAG index or training set ([12 §4–5](../../../docs/12-policy-and-compliance.md#4-per-platform-data--automation-rules)).
- Do NOT add paid data/APIs, scraping that breaks a site's terms, self-bots/user tokens, or any sybil/fake engagement.
- Do NOT skip, weaken or delete a test to get green.
- Do NOT commit secrets or paste them into chats, issues or logs; they live only in the sops/age file ([07 §2](../../../docs/07-security-notes.md#2-secrets)).

## Doc sync on completion

- `docs/02-v1-architecture.md`: §6: add `posture.tg.{subject}` and KV `tg_posture`; §4 M2 row
- `docs/12-policy-and-compliance.md`: §4: name the posture fields and the consumer allow-list
- `docs/roadmap/phase-4-intel.md`: tick T4.21 when all items mapped to it are done

## Branch & PR

- Branch: `p4/P4-T019-telegram-postures`
- PR title: `P4-T019: Telegram regex extractors, posture calculators, Bot API and RSS-Bridge fallback`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P4-T019` run

## Progress log

- 2026-10-21 00:00 · planner · created
