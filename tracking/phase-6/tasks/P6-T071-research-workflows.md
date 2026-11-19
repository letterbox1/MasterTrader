---
id: P6-T071
kind: task
title: "Research workflows: earnings preview/analysis, catalyst calendar, thesis tracker, morning note"
phase: 6
type: BUILD
status: backlog
priority: medium
size: L
severity: ""
owner: agent
claimed_by: ""
depends_on: [P6-T006, P6-T007, P4-T014, P4-T037]
requirements: [R6.08]
roadmap_todos: [T6.33]
modules: [M8, M15]
dashboards: [D08, D10]
tools: [uv, git]
mcp: []
env: []
services: [litellm, llm-local, postgres, nats]
branch: p6/P6-T071-research-workflows
pr: ""
doc_sync: [docs/03-build-spec.md, docs/10-memory-rag-and-models.md, docs/roadmap/phase-6-ai-models-treasury.md]
doc_sync_status: n/a
found_in: ""
created: 2026-11-19
updated: 2026-11-19
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
review_result: ""
---

# P6-T071 · Research workflows: earnings preview/analysis, catalyst calendar, thesis tracker, morning note

## Goal / expected outcome

Agent workflows adapted from Anthropic's financial-services equity-research and financial-analysis skills (Apache-2.0; NOTICE kept): earnings preview and earnings analysis from EDGAR filings and transcripts we're allowed to use, a catalyst calendar, a thesis tracker per strategy/position (thesis, evidence, invalidation conditions, status), and a morning note. DCF/comps run through the FinRobot valuation desk. Outputs feed the debate graph and the morning brief.

## Context & references

- Roadmap: [R6.08 / T6.33](../../../docs/roadmap/phase-6-ai-models-treasury.md#4-todo-sets)
- Agent tools P6-T006, debate P6-T007, EDGAR P4-T014, calendars P4-T037
- Source skills: anthropics/financial-services `plugins/vertical-plugins/equity-research` and `financial-analysis`
- Vetting and decision: [01 §8](../../../docs/01-repo-vetting-report.md#8-addendum-2026-11-19-eleven-more-repositories) · [17 §F](../../../docs/17-decisions-register.md#f-vetted-additions-2026-11-19)

## Requirements

- Adapt the skill prompts and steps; keep the Apache-2.0 licence and NOTICE with any copied text.
- All inputs through `pit(as_of)` tools; every output carries its sources and `as_of`.
- Runs on cadence/events (earnings dates, catalysts), never per tick; costs within the per-role LLM budgets (16 §2.10).
- Thesis tracker: each thesis has invalidation conditions; a breached condition raises an alert and a task, never an order.
- Tools & access: listed in the front matter (`tools`, `mcp`, `env`, `services`); `./kanban preflight P6-T071` checks them before start.

## ToDo

- [ ] Port the four workflows as agent workflows
- [ ] Thesis tracker store + invalidation alerts
- [ ] Wire outputs into the debate inputs and the morning brief
- [ ] Write tests (see Verification)
- [ ] Update docs listed under Doc sync

## Verification

### Tests
- Unit: each workflow on a fixture filing produces a sourced output with `as_of`.
- Integration: thesis invalidation raises an alert/task and no order.

### Scenarios
- Given an earnings date tomorrow, then an earnings preview is produced once, within budget.

### Stress / failure injection
- Earnings-season day with 50 watchlist reports: queue drains within the daily budget; overflow uses the local fallback model.

## Acceptance criteria

- [ ] Workflows produce sourced, PIT-correct outputs
- [ ] Licence/NOTICE kept for adapted content
- [ ] CI green (ruff, mypy, pytest, `pit` bypass check)

## Exceptions & edge cases

- Paid connectors in the source repo (LSEG, S&P) are not used.

## Cardinal rules (do NOT)

- Do NOT commit secrets or paste them into chats, issues or logs; they live only in the sops/age file ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Do NOT add paid data/APIs, scraping that breaks a site's terms, self-bots/user tokens, or any sybil/fake engagement.
- Do NOT let Telegram text (or any `model_input_ok = false` row) reach a model, RAG index or training set ([12 §4–5](../../../docs/12-policy-and-compliance.md#4-per-platform-data--automation-rules)).
- Do NOT read research data except through `pit(as_of)`; do NOT route any order around M11 via `mt_api`.
- Do NOT skip, weaken or delete a test to get green.
- Do NOT copy code from repositories without a compatible licence; keep copyright and NOTICE files for MIT/Apache code ([01 §8](../../../docs/01-repo-vetting-report.md#8-addendum-2026-11-19-eleven-more-repositories)).

## Doc sync on completion

- `docs/03-build-spec.md`: M8 research workflows
- `docs/10-memory-rag-and-models.md`: thesis tracker memory bank use
- `docs/roadmap/phase-6-ai-models-treasury.md`: tick T6.33

## Branch & PR

- Branch: `p6/P6-T071-research-workflows`
- PR title: `P6-T071: Research workflows: earnings preview/analysis, catalyst calendar, thesis tracker, morning note`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P6-T071` run

## Progress log

- 2026-11-19 00:00 · coordinator · created from the 2026-11-19 repository vetting (01 §8, 17 §F)
