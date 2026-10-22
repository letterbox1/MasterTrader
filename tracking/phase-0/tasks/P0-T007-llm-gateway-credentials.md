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
requirements: [R0.09, R0.13]
roadmap_todos: [T0.13]
modules: [M21]
dashboards: []
tools: []
mcp: []
env: []
services: [anthropic-console, custom-llm-endpoint]
branch: p0/P0-T007-llm-gateway-credentials
pr: ""
doc_sync: [docs/10-memory-rag-and-models.md, docs/roadmap/phase-0-foundations.md]
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

# P0-T007 · Provide LLM gateway credentials and spend caps

## Goal / expected outcome

LiteLLM has what it needs for its routes: an Anthropic API key with a monthly spend limit set in the Anthropic console (`research-primary`), your custom OpenAI-compatible endpoint URL + key (`research-custom`), and your chosen daily per-role budgets. This is roadmap ToDo T0.13 (added for P0-B009, [17 §D](../../../docs/17-decisions-register.md#d-other-decisions)).

## Context & references

- [Roadmap P0 R0.09, R0.13 · T0.13](../../../docs/roadmap/phase-0-foundations.md#3-requirements)
- [16 §2.10 LLM budgets](../../../docs/16-configuration-and-safety-model.md#210-models-tier-b-and-llm-budgets) (defaults)
- [10 §5 model gateway](../../../docs/10-memory-rag-and-models.md#5-model-gateway-research-chat--debate-routing-m21)
- [03 §7 LLM cost control](../../../docs/03-build-spec.md#7-llm-cost-control)
- [03 M21](../../../docs/03-build-spec.md#m21-decision-one--model-serving--mt_models)
- Related: P0-T042 LiteLLM (built keyless against a mock provider), P0-T044 `llm-local`
- Unblocks: P0-T068, the live gateway smoke with your keys (T0.69)

## Requirements

- Anthropic Console: workspace `mastertrader`, API key scoped to it, **monthly spend limit** set at or slightly above the gateway's monthly cap (log the number).
- Custom endpoint: base URL + key, OpenAI-compatible, reachable from the host (log the hostname only).
- Budgets are configurable defaults from [16 §2.10](../../../docs/16-configuration-and-safety-model.md#210-models-tier-b-and-llm-budgets), not numbers you have to invent: monthly cap **US$40**; daily per-role budgets debate $1.00, strategy-gen $0.50, explain $0.30, memory $0.30, chat $0.40, shadow $0.30; over budget → `local-advisor` fallback. Changing one later is a setting (`system.settings.update`; raising it is C3).
- Outputs → the sops secrets file `~/.config/mastertrader/secrets.sops.yaml` (created by the secrets task, P0-T022) under `litellm:` (`anthropic_api_key`, `custom_endpoint_url`, `custom_endpoint_key`). P0-T068 uses the env names `ANTHROPIC_API_KEY`, `MT_CUSTOM_LLM_BASE_URL`, `MT_CUSTOM_LLM_API_KEY` (names only). Until the secrets file exists, keep values **only** in your password manager; never in chat, email, git, issues or notes apps.

## ToDo

- [ ] Create the Anthropic API key and set the monthly limit; log the limit (not the key).
- [ ] Collect the custom endpoint URL/key (or log 'none yet'; the route is then disabled).
- [ ] Confirm the 16 §2.10 budget defaults, or log the values you want instead (they become settings, never code).
- [ ] Add the values to the secrets file once P0-T022 lands.

## Verification

### Tests
- Confirmation happens in the P0-T068 live smoke calls (`research-primary` and `research-custom` return 200 and land in `audit.llm_call`).

### Scenarios
- Given the monthly limit is reached, when an agent calls `research-primary`, then LiteLLM falls back to `research-custom` then `local-advisor` (10 §5).

### Stress / failure injection
- n/a: account action.

## Acceptance criteria

- [ ] Anthropic key exists with a monthly limit
- [ ] Custom endpoint details collected or route explicitly disabled
- [ ] Budget defaults confirmed (or changes logged); secrets only in the secrets file

## Exceptions & edge cases

- No custom endpoint yet: P0 ships with `research-custom` disabled; adding it later is a config change (10 §5).

## Cardinal rules (do NOT)

- Do NOT give LiteLLM broker/exchange keys; it only gets LLM keys (07 §2).
- Do NOT put an LLM key in the web app or any client.
- Do NOT commit secrets or paste them into chats, issues, PRs or logs; secrets live only in the sops/age file ([07 §2](../../../docs/07-security-notes.md#2-secrets)).

## Doc sync on completion

- `docs/10-memory-rag-and-models.md` §5: note the chosen budgets if they become defaults.
- `docs/roadmap/phase-0-foundations.md`: tick T0.13 when every item mapped to it is done.

## Branch & PR

- Branch: `p0/P0-T007-llm-gateway-credentials`
- PR title: `P0-T007: Provide LLM gateway credentials and spend caps`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P0-T007` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (now roadmap T0.13 (R0.09, R0.13); budgets = 16 §2.10 defaults (US$40/month, six roles incl. shadow); unblocks live smoke P0-T068 instead of P0-T042; secrets file path → `~/.config/mastertrader/`, outside the repo (17 §D P0-B018); run fields added)
