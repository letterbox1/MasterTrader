---
id: P4-T012
kind: task
title: RSS-Bridge client and bridged-site configuration
phase: 4
type: BUILD
status: backlog
priority: high
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P4-T010, P4-T007]
requirements: [R4.01, R4.N1]
roadmap_todos: [T4.20]
modules: [M2]
dashboards: [D07, D08]
tools: [uv, git, docker]
mcp: []
env: []
services: [nats, rss-bridge]
branch: p4/P4-T012-rss-bridge-client
pr: ""
doc_sync: [docs/runbooks/rss-bridge.md, docs/roadmap/phase-4-intel.md]
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

# P4-T012 · RSS-Bridge client and bridged-site configuration

## Goal / expected outcome

`mt_data.text.rssbridge` reads whitelisted bridges from the internal RSS-Bridge sidecar with `?format=Json` and auth, for each `kind: site` entry in `feeds.yaml` (CssSelector/XPath bridges for AP, Reuters, Economist WIB, Substack, Bundesbank, Binance blog, …), and publishes items on `raw.text.rss_bridge` marked context-only.

## Context & references

- Roadmap: [R4.01, R4.N1](../../../docs/roadmap/phase-4-intel.md#3-requirements) · ToDo [T4.20](../../../docs/roadmap/phase-4-intel.md#4-todo-sets)
- Sources: [06 §2](../../../docs/06-aggregators-and-market-providers.md#2-final-m2-social--news-ingestion-stack) · Spec: [03 M2](../../../docs/03-build-spec.md#m2-news--social--mt_datatext)
- Research: [social-aggregators](../../../docs/research/social-aggregators.md)
- Related: P4-T007 (sidecar), P4-T019 (Telegram fallback bridge: its items go only to the posture extractor, never to `raw.text.*` or `nlp`, 02 F3b).

## Requirements

- One bridge definition per site in `config/intel/bridges.yaml` (bridge name + params); CI checks each bridge is in the sidecar whitelist.
- Items flagged `latency_class = context` (15-min–3-h cache): never used as latency signals.
- Client uses the auth credentials scoped to `ingest-text`.

## ToDo

- [ ] Implement the JSON Feed parser + bridge URL builder.
- [ ] Write `bridges.yaml` for the example `kind: site` sources (your P4-T003 sites are bridged or rejected during P4-T060).
- [ ] Whitelist consistency check in CI.
- [ ] Fixtures + tests.

## Verification

### Tests
- Unit: JSON Feed fixtures → `RawTextItem`.
- CI: a bridge not on the whitelist fails the config check.
- Integration: against the real sidecar container in CI (local fixture site).

### Scenarios
- Given the sidecar returns 401 (rotated auth), then the source goes `bad` with a clear alert.
- Given a CssSelector bridge returns 0 items for 3 days, then D08 Sources flags 'selector broken?'.

### Stress / failure injection
- n/a: volume bounded by the sidecar cache; covered by P4-T058 RSS-Bridge-down injection.

## Acceptance criteria

- [ ] All example `kind: site` sources bridged or explicitly rejected with a reason
- [ ] Context-only flag set on every bridged item
- [ ] CI green (ruff, mypy, pytest, `pit` bypass check)

## Exceptions & edge cases

- StockTwits, ForexFactory, Investing.com have no bridge (research): don't write custom scrapers for them.
- Postgres down (02 §9.3): raw items stay in `RAW_TEXT` and are processed on recovery; the connector itself never needs the DB.

## Cardinal rules (do NOT)

- Do NOT use cookie/login bridges.
- Do NOT use the Reddit bridge.
- Do NOT commit secrets or paste them into chats, issues or logs; they live only in the sops/age file ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Do NOT add paid data/APIs, scraping that breaks a site's terms, self-bots/user tokens, or any sybil/fake engagement.
- Do NOT let Telegram text (or any `model_input_ok = false` row) reach a model, RAG index or training set ([12 §4–5](../../../docs/12-policy-and-compliance.md#4-per-platform-data--automation-rules)).
- Do NOT skip, weaken or delete a test to get green.
- Do NOT use unpinned images (`:latest`) or vendored code with telemetry/referral IDs; pin by digest.

## Doc sync on completion

- `docs/runbooks/rss-bridge.md`: how to add a site via bridges.yaml
- `docs/roadmap/phase-4-intel.md`: tick T4.20 when all items mapped to it are done

## Branch & PR

- Branch: `p4/P4-T012-rss-bridge-client`
- PR title: `P4-T012: RSS-Bridge client and bridged-site configuration`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P4-T012` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (Telegram bridge output routed only to postures (17 §A P4-B001); site list from P4-T003 handled in P4-T060)
