---
id: P4-T044
kind: task
title: D08 Intel: Feed, Document detail and Sources tabs
phase: 4
type: BUILD
status: backlog
priority: high
size: L
severity: ""
owner: agent
claimed_by: ""
depends_on: [P4-T043]
requirements: [R4.13]
roadmap_todos: [T4.29]
modules: [M2, M21, M9]
dashboards: [D08]
branch: p4/P4-T044-d08-feed-detail-sources
pr: ""
doc_sync: [docs/ui/dashboards/D08-intel.md, docs/roadmap/phase-4-intel.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P4-T044 · D08 Intel: Feed, Document detail and Sources tabs

## Goal / expected outcome

`/intel` renders the Feed tab (virtualised `DocumentCard` list with sources, published + ingested times, tickers, FinBERT sentiment, tier-B chips, dedup count, filters), the Document detail sheet (text where licence allows, entity links, tier-B probabilities with model version, related docs via RAG, "Ask decision model"), and the Sources tab (status, items/day, relevance hit-rate, licence/ToS tag, provenance flags, mute/unmute, add source, deferred Reddit/X shown disabled), following DESIGN.md tiers.

## Context & references

- Roadmap: [R4.13](../../../docs/roadmap/phase-4-intel.md#3-requirements) · ToDo [T4.29](../../../docs/roadmap/phase-4-intel.md#4-todo-sets)
- UI spec: [D08](../../../docs/ui/dashboards/D08-intel.md) (layout by tier, tabs, actions, states & rules, acceptance) · [DESIGN §6.8](../../../DESIGN.md#68-test-matrix-every-screen-must-pass)
- Cross-phase: P0 R0.11 component library; P2 D01/D02.
- Gap: P4-B002 (Feed source list includes Telegram).

## Requirements

- Scraped content rendered **as text only** (no HTML injection); links show destination domain and open with `rel=noopener`.
- Approximate timestamps shown as '≈ 2h ago (source-claimed)'.
- New docs appear within 5 s of ingestion; 'Scoring…' until tier B returns.
- Feed stays smooth at 1,000+ items on phones (virtualised list).
- Telegram never appears as a `DocumentCard`; a 'Telegram postures' panel shows per subject velocity/channel count/new-channel share/time since first call.
- Sources tab shows `train_ok`, `model_input_ok`, `retention_days`, attribution (CryptoPanic) and disabled reasons.

## ToDo

- [ ] Feed tab + filters (sheet on phones).
- [ ] Document detail sheet + related docs + `models.tierb.ask`.
- [ ] Sources tab + add/mute flows (C1/C0 confirmations).
- [ ] Telegram postures panel.
- [ ] Playwright specs (viewport matrix) + axe.
- [ ] Storybook stories for new components.

## Verification

### Tests
- Playwright: feed updates live via WS within 5 s of a seeded doc.
- Playwright: XSS payload in a seeded title renders inert text.
- Unit: approx timestamp formatter.

### Scenarios
- Given a paywalled doc, then detail shows headline + link only.
- Given tier B is degraded, then chips show 'Tier B unavailable' and the feed still updates.

### Stress / failure injection
- Seed 5,000 docs: scroll at 60 fps target on a mid phone profile; memory stable.

## Acceptance criteria

- [ ] All D08 Feed/Detail/Sources widgets per spec
- [ ] D08 acceptance 1 (≤ 5 s) and 3 (1,000+ items smooth) met
- [ ] No Telegram text rendered anywhere (test)
- [ ] CI green (ruff, mypy, pytest, `pit` bypass check, viewport matrix + axe)

## Exceptions & edge cases

- WS disconnect: banner + REST re-sync via `seq`.

## Cardinal rules (do NOT)

- Do NOT use `dangerouslySetInnerHTML` for scraped content.
- Do NOT call backend services directly; only `mt_api`.
- Do NOT bypass `mt_api`, the risk manager (M11) or `mt_store.pit(as_of)`; every order goes through M11.
- Do NOT let Telegram text (or any `model_input_ok = false` row) reach a model, RAG index or training set ([12 §4–5](../../../docs/12-policy-and-compliance.md#4-per-platform-data--automation-rules)).
- Do NOT skip, weaken or delete a test to get green.

## Doc sync on completion

- `docs/ui/dashboards/D08-intel.md`: mark implemented widgets; add the Telegram postures panel
- `docs/roadmap/phase-4-intel.md`: tick T4.29 when all items mapped to it are done

## Branch & PR

- Branch: `p4/P4-T044-d08-feed-detail-sources`
- PR title: `P4-T044: D08 Intel: Feed, Document detail and Sources tabs`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P4-T044` run

## Progress log

- 2026-10-21 00:00 · planner · created
