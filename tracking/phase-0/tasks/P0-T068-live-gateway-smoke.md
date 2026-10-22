---
id: P0-T068
kind: task
title: Run the live gateway smoke with your LLM keys
phase: 0
type: VERIFY
status: backlog
priority: medium
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P0-T007, P0-T042, P0-T043, P0-T044, P0-T022]
requirements: [R0.09, R0.13]
roadmap_todos: [T0.69]
modules: [M21, M17]
dashboards: [D16]
tools: [docker, uv, sops, curl]
mcp: []
env: [ANTHROPIC_API_KEY, MT_CUSTOM_LLM_BASE_URL, MT_CUSTOM_LLM_API_KEY]
services: [anthropic-api, custom-llm-endpoint, litellm, llm-local, tei-embed, postgres]
branch: p0/P0-T068-live-gateway-smoke
pr: ""
doc_sync: [docs/10-memory-rag-and-models.md, docs/roadmap/phase-0-foundations.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-22
updated: 2026-10-22
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
review_result: ""
---

# P0-T068 · Run the live gateway smoke with your LLM keys

## Goal / expected outcome

With your real keys from P0-T007 in the secrets file, the LiteLLM gateway built keyless in P0-T042 answers on every route — `research-primary` (Claude), `research-custom` (your endpoint, if configured) and `local-advisor` (`llm-local`) — within budget, the budget fallback works against the real provider, and every call lands in `audit.llm_call` (WORM) with tokens, cost and `trace_id`. This is the late live check split from T0.28 (build first, keys last).

## Context & references

- Roadmap: [R0.09, R0.13 · T0.69](../../../docs/roadmap/phase-0-foundations.md#3-requirements) (split from T0.28, which keeps the keyless build)
- [10 §5 model gateway](../../../docs/10-memory-rag-and-models.md#5-model-gateway-research-chat--debate-routing-m21)
- [16 §2.10 LLM budgets](../../../docs/16-configuration-and-safety-model.md#210-models-tier-b-and-llm-budgets) (monthly cap US$40; daily per-role budgets)
- [17 §D](../../../docs/17-decisions-register.md#d-other-decisions) P6-B010 (`audit.llm_call` from P0), P0-B008 (`llm-local`), P0-B009 (USER key task)
- [17 §E](../../../docs/17-decisions-register.md#e-ratification-2026-10-22) (build first, keys last)
- Keyless build: P0-T042 (LiteLLM), P0-T043 (TEI), P0-T044 (`llm-local`); keys: P0-T007 (USER)
- Depends on: P0-T007, P0-T042, P0-T043, P0-T044, P0-T022

## Requirements

- Functional:
  - Run on the host (or the dev stack) with the secrets file decrypted into tmpfs as usual; the agent's checks read the env names in the front matter via `sops exec-env` only, so no value is typed, echoed or logged.
  - One short completion per route through LiteLLM with a test virtual key: `research-primary` and `local-advisor` return 200; `research-custom` returns 200 if P0-T007 provided it, otherwise the log records "disabled" and the fallback chain skips it.
  - One embedding via `local-embed` (`tei-embed`) returns 384 dims; one rerank via `tei-rerank` orders a relevant passage first.
  - Budget fallback against the real provider: a test role with a tiny daily budget (e.g. US$0.001) → the second call is served by `local-advisor` and marked `fallback_used`.
  - Every call above has an `audit.llm_call` row (model, route, role, prompt/response hashes, tokens, cost, latency, `trace_id`) with a valid hash chain; the Prometheus spend metric rises by the reported cost.
  - Total spend of the whole check ≤ US$0.10 (logged); budgets used are the 16 §2.10 defaults from settings, plus the throwaway test role.
- Non-functional: prompts are fixed, harmless strings; no Telegram text and no `model_input_ok = false` rows are ever sent (12 §4–5).
- Tools & access: listed in the front matter (`env` holds names only; values stay in the secrets file).

## ToDo

- [ ] Confirm P0-T007 is done and the values are in the secrets file (`./kanban preflight P0-T068` inside `sops exec-env`).
- [ ] Write `tools/smoke/llm_live.py` (calls via LiteLLM only, fixed prompts, prints status + cost + model, never keys).
- [ ] Run it; collect the `audit.llm_call` rows (hashes/ids only) and the spend metric delta.
- [ ] Run the budget-fallback case with the throwaway test role, then delete that virtual key.
- [ ] Log results here (no values) and file a bug for any failure.

## Verification

### Tests
- The live smoke script: per-route status, embedding dims, rerank order, fallback marker.
- Audit check: `recompute_chain` over the new `audit.llm_call` rows → valid; each row's `trace_id` matches the script's request.

### Scenarios
- Given your Anthropic monthly limit is reached, when `research-primary` is called, then the gateway falls back to `research-custom` then `local-advisor` and says which.
- Given `research-custom` isn't configured, then the route is reported disabled and nothing fails.

### Stress / failure injection
- Kill `llm-local` mid-run → `local-advisor` calls fail fast with 503 and the fallback chain reports it; restart it via D16 (allow-listed) and re-run.

## Acceptance criteria

- [ ] Each configured route answers within budget with real keys
- [ ] Budget exhaustion falls back to `local-advisor` against the real provider
- [ ] Every call is in `audit.llm_call` with a valid chain and matching `trace_id`
- [ ] Spend ≤ US$0.10 logged; no key value appears in any log, output or file
- [ ] CI green (ruff, mypy, pytest, gitleaks, `pit` check)

## Exceptions & edge cases

- Provider rate limit (429): back off and retry once; persistent 429 is logged, not treated as a gateway bug.
- Keys not yet provided: block this task (`./kanban block P0-T068 --reason "waiting on P0-T007"`); nothing else in P0 waits on it except the exit demo.

## Cardinal rules (do NOT)

- Do NOT paste, echo or log any key; use `sops exec-env` and names only.
- Do NOT send Telegram text, private data or `model_input_ok = false` rows to any model ([12 §4–5](../../../docs/12-policy-and-compliance.md#4-per-platform-data--automation-rules)).
- Do NOT raise the real budgets to make the test pass (raising is C3); use the throwaway test role.
- Do NOT commit secrets or paste them into chats, issues, PRs or logs; secrets live only in the sops/age file ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Do NOT skip, weaken or delete a test to get CI green.

## Doc sync on completion

- `docs/10-memory-rag-and-models.md` §5: record the live-checked routes, the fallback mechanism and the measured latency per route.
- `docs/roadmap/phase-0-foundations.md`: tick T0.69 when every item mapped to it is done.

## Branch & PR

- Branch: `p0/P0-T068-live-gateway-smoke`
- PR title: `P0-T068: Run the live gateway smoke with your LLM keys`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P0-T068` run

## Progress log

- 2026-10-22 02:01 · cloud:vm:be04b6ae61f8 · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (new task for T0.69: live smoke split from T0.28 per build first, keys last, 17 §E)
