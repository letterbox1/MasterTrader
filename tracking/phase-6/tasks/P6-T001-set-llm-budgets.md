---
id: P6-T001
kind: task
title: Seed the LLM budgets from the 16 §2.10 defaults
phase: 6
type: BUILD
status: backlog
priority: high
size: XS
severity: ""
owner: agent
claimed_by: ""
depends_on: [P0-T042]
requirements: [R6.07]
roadmap_todos: [T6.01]
modules: [M21]
dashboards: [D10]
tools: [git, cargo, docker]
mcp: []
env: []
services: [supabase-postgres, mt-api, litellm]
branch: p6/P6-T001-set-llm-budgets
pr: ""
doc_sync: [docs/10-memory-rag-and-models.md, docs/roadmap/phase-6-ai-models-treasury.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-11-19
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
review_result: ""
---

# P6-T001 · Seed the LLM budgets from the 16 §2.10 defaults

## Goal / expected outcome

The LLM budgets start populated without asking you anything: the monthly cap (US$40, checked month-to-date per UTC month) and the daily per-role budgets (debate $1.00, strategy-gen $0.50, explain $0.30, memory $0.30, chat $0.40, shadow $0.30) from [16 §2.10](../../../docs/16-configuration-and-safety-model.md#210-models-tier-b-and-llm-budgets) are seeded as settings with source `seed` and pushed to the LiteLLM per-role keys. P6-T009 enforces whatever the settings hold. You review them once in the go-live pack (P7-T070) or change them any time in D10 (lowering C1, raising C3). Your custom endpoint URL and key stay in P0-T007.

## Context & references

- Roadmap: [R6.07](../../../docs/roadmap/phase-6-ai-models-treasury.md#3-requirements) · ToDo T6.01
- Spec: [03 §7](../../../docs/03-build-spec.md#7-llm-cost-control) · [10 §5](../../../docs/10-memory-rag-and-models.md#5-model-gateway-research-chat--debate-routing-m21) (virtual key per role, `max_budget`, `budget_duration: 1d`, global provider budget)
- Defaults: [16 §2.10](../../../docs/16-configuration-and-safety-model.md#210-models-tier-b-and-llm-budgets) · decision [17 §C](../../../docs/17-decisions-register.md#c-defaults-that-were-n-or-unspecified) (P6-B012: LLM budgets)
- Decisions: [17 §G](../../../docs/17-decisions-register.md#g-platform-rust-and-python-supabase-vercel-workstation-first-2026-11-19) (configurable values are seeded by agents and approved once in the go-live pack)
- Cross-phase: P0-T042 (LiteLLM with per-role keys and default budgets). P0-T007 (your endpoint URL and keys, T0.13) and P0-T068 (live gateway smoke) are not needed to seed values.
- Unblocks: P6-T009 (budget enforcement), P6-T010 (spend panel), P6-T053 (budget test). Approval: P7-T070.

## Requirements

- One machine-readable defaults file (`config/defaults/llm_budgets.yaml`) whose values match 16 §2.10 exactly; a test parses the 16 §2.10 table and compares, so they can't drift.
- Seeded settings: `llm.monthly_cap_usd`, `llm.budget.<role>.daily_usd` for debate, strategy-gen, explain, memory, chat, shadow; alert thresholds 80% and 100% of each budget and of the cap (P6-T010 defaults).
- Seeding goes through `mt-api` (`system.settings.update`) with source `seed`, is idempotent (no new version when nothing changed) and never overwrites a value you set (your rows win; the seed only fills fields with no value).
- After seeding, the LiteLLM per-role keys carry the same `max_budget` values (one sync job; settings are the source of truth).
- Budgets are settings, not secrets: they never go in the sops file.

## ToDo

- [ ] Write `config/defaults/llm_budgets.yaml` from 16 §2.10 and the doc ↔ file test
- [ ] Seed command (`mt settings seed --group llm`) over `mt-api` with source `seed`
- [ ] Sync seeded values to the LiteLLM per-role keys; D10 Gateway shows each role's budget with its 16 link
- [ ] Add the LLM budget rows to the go-live pack generator (P7-T011 / P7-T070 reads it)
- [ ] Tests; progress log; `./kanban done P6-T001`

## Verification

### Tests
- `cargo test -p mt-api settings_seed_llm`: every seeded value equals the defaults file; the defaults file equals 16 §2.10 (doc-parse test).
- Re-run the seed: no new versions. Lower one budget by hand, re-run: your value stays.
- Raising a budget through `system.settings.update` is classified C3; lowering is C1.

### Scenarios
- Given a fresh workstation stack, when the seed runs, then D10 Gateway shows each role's budget and today's spend, and LiteLLM's role keys carry the same `max_budget`.
- Given you lowered `chat` to $0.20, when the seed runs again, then `chat` stays $0.20.

### Stress / failure injection
- LiteLLM down during the sync: settings are saved, the sync retries and D10 shows "gateway out of sync" until it succeeds; enforcement falls back to the local model (P6-T009).

## Acceptance criteria

- [ ] Monthly cap and every role budget (incl. `shadow`) seeded with source `seed`, matching 16 §2.10
- [ ] Doc ↔ defaults-file test passes; seed is idempotent and never overwrites your values
- [ ] LiteLLM role keys match the settings

## Exceptions & edge cases

- No custom endpoint configured yet (P0-T007 not done): `research-custom` stays disabled; fallback goes Claude → local. Seeding doesn't depend on it.
- A default marked (U) in 16 is seeded as written and flagged `unverified` in D10 until its RESEARCH task confirms it.

## Cardinal rules (do NOT)

- Every value comes from the defaults file; nothing hard-coded in code.
- Never raise a budget on a re-seed; raising is C3 and only yours.
- Do NOT put keys or endpoint URLs in this task, the defaults file, chat or a PR; secrets live only in the sops/age file (07 §2).
- Do NOT skip, weaken or delete a test to get green.

## Doc sync on completion

- `docs/10-memory-rag-and-models.md` §5: note the `shadow` role and that budgets are seeded settings (no numbers).
- `docs/roadmap/phase-6-ai-models-treasury.md`: tick T6.01 (and note this task ID) once all items covering it are done.

## Branch & PR

- Branch: `p6/P6-T001-set-llm-budgets`
- PR title: `P6-T001: Seed the LLM budgets from the 16 §2.10 defaults`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P6-T001` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (budgets are 16 §2.10 defaults to review (incl. shadow $0.30), settings not secrets; sops file outside the repo; deps P0-T007/P0-T042; run fields)
