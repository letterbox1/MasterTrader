---
id: P6-T047
kind: task
title: Optional: M23 social drafts → your approval → web intent
phase: 6
type: BUILD
status: backlog
priority: low
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P6-T003, P5-T029, P0-T044]
requirements: [R6.31]
roadmap_todos: [T6.30]
modules: [M23, M19]
dashboards: [D13]
tools: [git, uv, python>=3.12, docker]
mcp: []
env: []
services: [llm-local, postgres]
branch: p6/P6-T047-social-drafts-web-intent
pr: ""
doc_sync: [docs/13-wallets-treasury-and-onchain.md, docs/ui/dashboards/D13-tasks-curation.md, docs/roadmap/phase-6-ai-models-treasury.md]
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

# P6-T047 · Optional: M23 social drafts → your approval → web intent

## Goal / expected outcome

`mt_social` drafts posts/replies for social quest tasks in your voice with a local model, adds a holdings disclosure line, and on your approval (`social.draft.approve`, C1) opens an X web-intent link; you click Post; the proof URL is captured and the task closed.

## Context & references

- Roadmap: [R6.31](../../../docs/roadmap/phase-6-ai-models-treasury.md#3-requirements) · ToDo T6.30
- Optional: only if P6-T003 recorded `yes`; otherwise cancel this item.
- Spec: [13 §8](../../../docs/13-wallets-treasury-and-onchain.md#8-social-participation-m23-mt_social) · [03 M23](../../../docs/03-build-spec.md#m23-social-participation--mt_social) · [12 §4](../../../docs/12-policy-and-compliance.md#4-per-platform-data--automation-rules) (X: web intent after approval only; no auto-posting)
- UI: [D13](../../../docs/ui/dashboards/D13-tasks-curation.md) Social drafts tab
- Container: [02 §3.2](../../../docs/02-v1-architecture.md#32-containers) (`social`)
- Depends on (this phase): P6-T003
- Cross-phase: P5-T029 (task queue with social quest tasks), P0-T044 (`local-advisor`)

## Requirements

- Drafts grounded in real activity/holdings (journal, wallet view), local model only (`local-advisor`), prompt versioned and audited.
- Disclosure line auto-added for any token you hold; shilling/deceptive drafts refused by a rules + tier-B `scam_language` check.
- `social.draft.new` / `social.draft.decision` events; `curation.social_draft` table; approve = C1 opens `https://x.com/intent/post?text=…` (no API), reject/edit/skip.
- Proof URL pasted back → task done with link.
- Never: extra accounts, auto-posting, engagement pods, pay-to-post, captcha solving.

## ToDo

- [ ] `mt_social` service + `social` container.
- [ ] Draft prompt + disclosure logic + refusal rules.
- [ ] D13 tab + Telegram buttons.
- [ ] Tests; docs.

## Verification

### Tests
- Unit: disclosure added when holding; refusal of promotional claims.
- Playwright: approve opens intent URL with prefilled text; nothing posts by itself.

### Scenarios
- Given a quest requires a reply about a project you hold, then the draft includes the disclosure line and waits for you.

### Stress / failure injection
- n/a: human-paced flow.

## Acceptance criteria

- [ ] Flow test: draft → approve → intent URL → proof captured (R6.31).

## Exceptions & edge cases

- X intent format changes: link still opens; text may need manual paste (documented).

## Cardinal rules (do NOT)

- Do NOT post automatically or via any API; do NOT create personas.
- Do NOT add paid data/APIs or scraping that breaks terms; no self-bots, user tokens, sybil/multi-wallet or fake engagement.
- Do NOT let Telegram text (or any `model_input_ok = false` / `train_ok = false` row) reach a model, prompt, RAG index, memory bank or training set (12 §4–5).
- Do NOT commit secrets or paste them into chats/issues/PRs; secrets live only in the sops/age file (07 §2).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral/broker IDs in vendored code.

## Doc sync on completion

- `docs/13-wallets-treasury-and-onchain.md` §8: implemented flow.
- `docs/ui/dashboards/D13-tasks-curation.md`: social drafts tab.
- `docs/roadmap/phase-6-ai-models-treasury.md`: tick T6.30 (and note this task ID) once all items covering it are done.

## Branch & PR

- Branch: `p6/P6-T047-social-drafts-web-intent`
- PR title: `P6-T047: Optional: M23 social drafts → your approval → web intent`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P6-T047` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (cross-phase deps P5-T029/P0-T044; run fields)
