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
depends_on: [P0-T007, P0-T042]
requirements: [R6.07]
roadmap_todos: [T6.01]
modules: [M21]
dashboards: [D10]
tools: [sops]
mcp: []
env: []
services: [litellm, custom-llm-endpoint]
branch: p6/P6-T001-set-llm-budgets
pr: ""
doc_sync: [docs/10-memory-rag-and-models.md, docs/roadmap/phase-6-ai-models-treasury.md]
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

# P6-T001 · Set LLM budgets and confirm the custom endpoint

## Goal / expected outcome

You have reviewed the **LLM budget defaults** ([16 §2.10](../../../docs/16-configuration-and-safety-model.md#210-models-tier-b-and-llm-budgets): monthly cap US$40; daily per-role budgets debate $1.00, strategy-gen $0.50, explain $0.30, memory $0.30, chat $0.40, shadow $0.30), kept or tightened them in the settings, and confirmed your custom OpenAI-compatible endpoint. P6-T009 enforces whatever the settings hold; the defaults apply until you change them.

## Context & references

- Roadmap: [R6.07](../../../docs/roadmap/phase-6-ai-models-treasury.md#3-requirements) · ToDo T6.01
- Spec: [03 §7](../../../docs/03-build-spec.md#7-llm-cost-control) · [10 §5](../../../docs/10-memory-rag-and-models.md#5-model-gateway-research-chat--debate-routing-m21) (virtual key per role, `max_budget`, `budget_duration: 1d`, global provider budget)
- Defaults: [16 §2.10](../../../docs/16-configuration-and-safety-model.md#210-models-tier-b-and-llm-budgets) · decision [17 §C](../../../docs/17-decisions-register.md#c-defaults-that-were-n-or-unspecified) (P6-B012: LLM budgets)
- Cross-phase: P0-T042 (LiteLLM with per-role keys and default budgets), P0-T007 (your keys in the sops file, T0.13), P0-T068 (live gateway smoke)
- Unblocks: P6-T009 (budget enforcement), P6-T010 (spend panel), P6-T053 (budget test)

## Requirements

- Review the defaults (16 §2.10): monthly cap US$40 per UTC month (checked month-to-date) and daily per-role budgets debate $1.00, strategy-gen $0.50, explain $0.30, memory $0.30, chat $0.40, shadow $0.30 (5% tier-B shadow checks, P6-T025). Keep or lower them (C1); raising any is C3.
- Confirm the alert thresholds (P6-T010 defaults: 80% and 100% of each budget and of the monthly cap).
- Confirm the custom endpoint: base URL, model name(s), context window, whether it may see untrusted scraped text.
- Secrets (endpoint API key, Anthropic key) go **only** into the sops file, never chat or git.

## ToDo

- [ ] Open the D10 Gateway tab (or `/models/gateway/spend`) and review the last 30 days of spend by role from P0–P5 usage.
- [ ] Keep or lower each budget in D10 → Gateway → Adjust gateway budget (`system.settings.update`: lowering C1; raising C3). Budgets are settings, not secrets: they never go in the sops file.
- [ ] If the custom endpoint changed: edit the sops file outside the repo (`sops ~/.config/mastertrader/secrets.enc.yaml`, names `MT_CUSTOM_LLM_BASE_URL` and `MT_CUSTOM_LLM_API_KEY`, as in P0-T007); save, then restart `litellm` from D16 (`system.service.restart`).
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

- [ ] Monthly cap and every role budget (incl. `shadow`) show your values (defaults or tighter) in D10.
- [ ] `research-custom` shows healthy in D10 (P0-T068 live smoke passed), or is deliberately left disabled.
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
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (budgets are 16 §2.10 defaults to review (incl. shadow $0.30), settings not secrets; sops file outside the repo; deps P0-T007/P0-T042; run fields)
