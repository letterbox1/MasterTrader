---
id: P6-T003
kind: task
title: Decide on Hummingbot, social drafts, crowd-sim and LightRAG
phase: 6
type: USER
status: ready
priority: low
size: XS
severity: ""
owner: user
claimed_by: ""
depends_on: []
requirements: [R6.30, R6.31, R6.32]
roadmap_todos: [T6.04]
modules: [M13, M14, M23, M9]
dashboards: [D11, D13]
tools: []
mcp: []
env: []
services: []
branch: p6/P6-T003-decide-optional-modules
pr: ""
doc_sync: [tracking/phase-6/PHASE.md, docs/roadmap/phase-6-ai-models-treasury.md]
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

# P6-T003 · Decide on Hummingbot, social drafts, crowd-sim and LightRAG

## Goal / expected outcome

A recorded yes/no for each optional module, so the optional build items (P6-T046–P6-T051) are either started or cancelled and don't hold the phase open.

## Context & references

- Roadmap: [R6.30](../../../docs/roadmap/phase-6-ai-models-treasury.md#3-requirements) · [R6.31](../../../docs/roadmap/phase-6-ai-models-treasury.md#3-requirements) · [R6.32](../../../docs/roadmap/phase-6-ai-models-treasury.md#3-requirements) · ToDo T6.04
- Spec: [03 M13](../../../docs/03-build-spec.md#m13-market-making-sidecar) · [03 M23](../../../docs/03-build-spec.md#m23-social-participation--mt_social) · [03 M14](../../../docs/03-build-spec.md#m14-crowd-simulation-optional) · [03 M9](../../../docs/03-build-spec.md#m9-memory--rag--mt_memory) (LightRAG optional) · [14 §3](../../../docs/14-strategy-evidence-and-validation.md#3-strategy-catalogue-evidence-ranked-templates) (market-making is P3 priority; must beat HLP)
- Decision: [17 §D](../../../docs/17-decisions-register.md#d-other-decisions) (P6-B009: MiroFish/OASIS only with a local memory backend and hardened config, no Zep Cloud; otherwise M14 is skipped)

## Requirements

- Decide each: Hummingbot MM sidecar (needs Hyperliquid/venue approval and A$20k+ to be meaningful); M23 social drafts; crowd-sim experiment (possible only with a local memory backend and hardened config, no Zep Cloud; otherwise M14 is skipped); LightRAG graph over filings.
- Record the reason in one line each.

## ToDo

- [ ] Read the R6.30–R6.32 rows in the roadmap and the evidence row for market making in 14 §3.
- [ ] Record decisions in this file's progress log as `hummingbot=yes|no, social=yes|no, crowdsim=yes|no, lightrag=yes|no`.
- [ ] For each 'no': run `./kanban cancel <ID>` on the matching item (P6-T046 Hummingbot, P6-T047/P6-T048/P6-T049 social, P6-T050 crowd-sim, P6-T051 LightRAG).
- [ ] For each 'yes': leave it in backlog; triage will promote it.

## Verification

### Tests
- n/a: decision item.

### Scenarios
- Given hummingbot=no, when the item is cancelled, then the phase progress excludes it and D11 stays hidden from nav.

### Stress / failure injection
- n/a

## Acceptance criteria

- [ ] All four decisions recorded.
- [ ] Optional items cancelled or kept to match.

## Exceptions & edge cases

- You can revisit later; re-opening a cancelled item is allowed.

## Cardinal rules (do NOT)

- Do NOT enable any optional module that adds auto-posting, extra accounts or telemetry.
- Do NOT add paid data/APIs or scraping that breaks terms; no self-bots, user tokens, sybil/multi-wallet or fake engagement.
- Do NOT commit secrets or paste them into chats/issues/PRs; secrets live only in the sops/age file (07 §2).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral/broker IDs in vendored code.

## Doc sync on completion

- `tracking/phase-6/PHASE.md`: planning notes updated with the decisions.
- `docs/roadmap/phase-6-ai-models-treasury.md`: tick T6.04 (and note this task ID) once all items covering it are done.

## Branch & PR

- Branch: `p6/P6-T003-decide-optional-modules`
- PR title: `P6-T003: Decide on Hummingbot, social drafts, crowd-sim and LightRAG`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P6-T003` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (crowd-sim condition per 17 §D P6-B009; run fields)
