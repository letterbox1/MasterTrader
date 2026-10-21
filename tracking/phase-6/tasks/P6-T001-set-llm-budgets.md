---
id: P6-T001
kind: task
title: Set LLM budgets and confirm the custom endpoint
phase: 6
type: USER
status: backlog
priority: high
size: XS
severity: ""
owner: user
claimed_by: ""
depends_on: []
requirements: [R6.07]
roadmap_todos: [T6.01]
modules: [M21]
dashboards: [D10]
branch: p6/P6-T001-set-llm-budgets
pr: ""
doc_sync: [docs/10-memory-rag-and-models.md, docs/roadmap/phase-6-ai-models-treasury.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P6-T001 · Set LLM budgets and confirm the custom endpoint

## Goal / expected outcome

You have decided the **monthly LLM spend cap**, the **per-role daily budgets** (debate, strategy-gen, explain, memory, chat, shadow) and confirmed your custom OpenAI-compatible endpoint, and the values sit in the settings store / sops file so P6-T009 can enforce them.

## Context & references

- Roadmap: [R6.07](../../../docs/roadmap/phase-6-ai-models-treasury.md#3-requirements) · ToDo T6.01
- Spec: [03 §7](../../../docs/03-build-spec.md#7-llm-cost-control) · [10 §5](../../../docs/10-memory-rag-and-models.md#5-model-gateway-research-chat--debate-routing-m21) (virtual key per role, `max_budget`, `budget_duration: 1d`, global provider budget)
- Cross-phase: P0 R0.09 / T0.45 (LiteLLM config with per-role virtual keys already exists)
- Unblocks: P6-T009 (budget enforcement), P6-T010 (spend panel), P6-T053 (budget test)

## Requirements

- Decide: monthly global cap (AUD/USD), per-role daily budgets for `debate`, `strategy-gen`, `explain`, `memory`, `chat` and the new `shadow` role (5% tier-B shadow checks, P6-T025).
- Decide the warning threshold for alerts (suggested 80% and 100% of each budget).
- Confirm the custom endpoint: base URL, model name(s), context window, whether it may see untrusted scraped text.
- Secrets (endpoint API key, Anthropic key) go **only** into the sops file, never chat or git.

## ToDo

- [ ] Open the D10 Gateway tab (or `/models/gateway/spend`) and review the last 30 days of spend by role from P0–P5 usage.
- [ ] Write the monthly cap and per-role daily budgets on the host: `sops secrets/mt.enc.yaml` → `llm.budgets.{monthly_cap, roles.*}` (numbers are not secrets but keep them with the key set), or enter them via D10 → Adjust gateway budget (`system.settings.update`; raising later is C3).
- [ ] If the custom endpoint changed: `sops secrets/mt.enc.yaml` → `litellm.research_custom.{api_base, api_key}`; save, then `docker compose restart litellm`.
- [ ] Confirm in D10 Gateway that `research-custom` shows healthy and the budgets display.
- [ ] Tick this item and note the chosen numbers (not the keys) in the progress log.

## Verification

### Tests
- n/a: human decision; P6-T053 tests enforcement of the values set here.

### Scenarios
- Given the budgets are saved, when D10 Gateway loads, then each role shows its budget and today's spend.

### Stress / failure injection
- n/a: configuration only.

## Acceptance criteria

- [ ] Monthly cap and every role budget (incl. `shadow`) are set and visible in D10.
- [ ] Custom endpoint smoke call succeeds through LiteLLM (`research-custom`).
- [ ] No key appears in git, chat or the progress log.

## Exceptions & edge cases

- If you have no custom endpoint yet, leave `research-custom` disabled; fallback goes Claude → local.
- Budgets can be lowered any time (C1); raising later needs C3.

## Cardinal rules (do NOT)

- Do NOT paste API keys into the task file, chat or a PR.
- Do NOT loosen anything (risk, LLM budgets, treasury policy, allow-list, autonomous mode, mandates) without C3 (Telegram + TOTP + cool-down); protective exits never wait for approval.
- Do NOT commit secrets or paste them into chats/issues/PRs; secrets live only in the sops/age file (07 §2).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral/broker IDs in vendored code.

## Doc sync on completion

- `docs/10-memory-rag-and-models.md` §5: note the `shadow` role and where budgets live (no numbers).
- `docs/roadmap/phase-6-ai-models-treasury.md`: tick T6.01 (and note this task ID) once all items covering it are done.

## Branch & PR

- Branch: `p6/P6-T001-set-llm-budgets`
- PR title: `P6-T001: Set LLM budgets and confirm the custom endpoint`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P6-T001` run

## Progress log

- 2026-10-21 00:00 · planner · created
