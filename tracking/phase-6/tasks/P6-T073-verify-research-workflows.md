---
id: P6-T073
kind: task
title: "Verify research workflows and persona lenses (PIT, sources, shadow comparison)"
phase: 6
type: VERIFY
status: backlog
priority: low
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P6-T071, P6-T072]
requirements: [R6.08]
roadmap_todos: [T6.74]
modules: [M8]
dashboards: [D10]
tools: [git, cargo]
mcp: []
env: []
services: [litellm, llm-local, supabase-postgres]
branch: p6/P6-T073-verify-research-workflows
pr: ""
doc_sync: [docs/roadmap/phase-6-ai-models-treasury.md]
doc_sync_status: n/a
found_in: ""
created: 2026-11-19
updated: 2026-11-20
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
review_result: ""
---

# P6-T073 · Verify research workflows and persona lenses (PIT, sources, shadow comparison)

## Goal / expected outcome

Evidence that the research workflows use point-in-time inputs and cite their sources, and a shadow comparison of the debate with and without each persona lens.

## Context & references

- Roadmap: [R6.08 / T6.74](../../../docs/roadmap/phase-6-ai-models-treasury.md#4-todo-sets)
- Builds on P6-T071, P6-T072
- Vetting and decision: [01 §8](../../../docs/01-repo-vetting-report.md#8-addendum-2026-11-19-eleven-more-repositories) · [17 §F](../../../docs/17-decisions-register.md#f-vetted-additions-2026-11-19)

## Requirements

- PIT leak test on each workflow.
- Shadow run over at least 4 weeks of decisions: debate with vs without each lens; report calibration and hit rate per lens.
- Tools & access: listed in the front matter (`tools`, `mcp`, `env`, `services`); `./kanban preflight P6-T073` checks them before start.

## ToDo

- [ ] Run PIT leak tests
- [ ] Run the shadow comparison
- [ ] Record results and the on/off recommendation per lens

## Verification

### Tests
- Inject a post-`as_of` filing: the workflow refuses it.

### Scenarios
- Given a lens that improves calibration in shadow, then the report recommends enabling it for that strategy class (you decide).

### Stress / failure injection
- n/a

## Acceptance criteria

- [ ] PIT tests pass
- [ ] Shadow comparison report attached

## Exceptions & edge cases

- Too few decisions in the window: extend the shadow period and note it.

## Cardinal rules (do NOT)

- Do NOT commit secrets or paste them into chats, issues or logs; they live only in the sops/age file ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Do NOT add paid data/APIs, scraping that breaks a site's terms, self-bots/user tokens, or any sybil/fake engagement.
- Do NOT let Telegram text (or any `model_input_ok = false` row) reach a model, RAG index or training set ([12 §4–5](../../../docs/12-policy-and-compliance.md#4-per-platform-data--automation-rules)).
- Do NOT read research data except through `pit(as_of)`; do NOT route any order around M11 via `mt-api`.
- Do NOT skip, weaken or delete a test to get green.
- Do NOT copy code from repositories without a compatible licence; keep copyright and NOTICE files for MIT/Apache code ([01 §8](../../../docs/01-repo-vetting-report.md#8-addendum-2026-11-19-eleven-more-repositories)).

## Doc sync on completion

- `docs/roadmap/phase-6-ai-models-treasury.md`: tick T6.74

## Branch & PR

- Branch: `p6/P6-T073-verify-research-workflows`
- PR title: `P6-T073: Verify research workflows and persona lenses (PIT, sources, shadow comparison)`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P6-T073` run

## Progress log

- 2026-11-19 00:00 · coordinator · created from the 2026-11-19 repository vetting (01 §8, 17 §F)
- 2026-11-19 00:00 · aligner · re-platformed per docs/18 (services `postgres` → `supabase-postgres`; `mt_api` → `mt-api`)
- 2026-11-20 00:00 · aligner · Rust-max per 17 §H (workflows under test are Rust (`mt-agents`); tools cargo)
