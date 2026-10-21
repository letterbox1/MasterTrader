---
id: P0-T007
kind: task
title: Provide LLM gateway credentials and spend caps
phase: 0
type: USER
status: ready
priority: medium
size: XS
severity: ""
owner: user
claimed_by: ""
depends_on: []
requirements: [R0.09]
roadmap_todos: [T0.45]
modules: [M21]
dashboards: []
branch: p0/P0-T007-llm-gateway-credentials
pr: ""
doc_sync: [docs/10-memory-rag-and-models.md, docs/roadmap/phase-0-foundations.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P0-T007 · Provide LLM gateway credentials and spend caps

## Goal / expected outcome

LiteLLM has what it needs for its routes: an Anthropic API key with a monthly spend limit set in the Anthropic console (`research-primary`), your custom OpenAI-compatible endpoint URL + key (`research-custom`), and your chosen daily per-role budgets. The roadmap's USER list doesn't include this step (see P0-B009).

## Context & references

- [Roadmap P0 R0.09](../../../docs/roadmap/phase-0-foundations.md#3-requirements)
- [10 §5 model gateway](../../../docs/10-memory-rag-and-models.md#5-model-gateway-research-chat--debate-routing-m21)
- [03 §7 LLM cost control](../../../docs/03-build-spec.md#7-llm-cost-control)
- [03 M21](../../../docs/03-build-spec.md#m21-decision-one--model-serving--mt_models)
- Related: P0-T042 LiteLLM, P0-T044 local-advisor
- Unblocks: P0-T042 LiteLLM gateway smoke calls

## Requirements

- Anthropic Console: workspace `mastertrader`, API key scoped to it, **monthly spend limit** set (your choice; log the number).
- Custom endpoint: base URL + key, OpenAI-compatible, reachable from the host (log the hostname only).
- Per-role daily budgets for LiteLLM virtual keys `debate`, `strategy-gen`, `explain`, `memory`, `chat` (e.g. US$1/day each to start) + a global provider budget.
- Outputs → the sops secrets file `/etc/mastertrader/secrets.sops.yaml` (created by the secrets task, P0-T022) under `litellm:` (`anthropic_api_key`, `custom_endpoint_url`, `custom_endpoint_key`). Until the secrets file exists, keep values **only** in your password manager; never in chat, email, git, issues or notes apps.

## ToDo

- [ ] Create the Anthropic API key and set the monthly limit; log the limit (not the key).
- [ ] Collect the custom endpoint URL/key (or log 'none yet'; the route is then disabled).
- [ ] Write the per-role daily budgets into this task's progress log for P0-T042.
- [ ] Add the values to the secrets file once P0-T022 lands.

## Verification

### Tests
- Confirmation happens in P0-T042 smoke calls (`research-primary` and `research-custom` return 200).

### Scenarios
- Given the monthly limit is reached, when an agent calls `research-primary`, then LiteLLM falls back to `research-custom` then `local-advisor` (10 §5).

### Stress / failure injection
- n/a: account action.

## Acceptance criteria

- [ ] Anthropic key exists with a monthly limit
- [ ] Custom endpoint details collected or route explicitly disabled
- [ ] Budgets logged; secrets only in the secrets file

## Exceptions & edge cases

- No custom endpoint yet: P0 ships with `research-custom` disabled; adding it later is a config change (10 §5).

## Cardinal rules (do NOT)

- Do NOT give LiteLLM broker/exchange keys; it only gets LLM keys (07 §2).
- Do NOT put an LLM key in the web app or any client.
- Do NOT commit secrets or paste them into chats, issues, PRs or logs; secrets live only in the sops/age file ([07 §2](../../../docs/07-security-notes.md#2-secrets)).

## Doc sync on completion

- `docs/10-memory-rag-and-models.md` §5: note the chosen budgets if they become defaults.
- `docs/roadmap/phase-0-foundations.md`: tick T0.45 when every item mapped to it is done.

## Branch & PR

- Branch: `p0/P0-T007-llm-gateway-credentials`
- PR title: `P0-T007: Provide LLM gateway credentials and spend caps`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P0-T007` run

## Progress log

- 2026-10-21 00:00 · planner · created
