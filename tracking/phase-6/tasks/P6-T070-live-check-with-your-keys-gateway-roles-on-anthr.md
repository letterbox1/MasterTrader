---
id: P6-T070
kind: task
title: "Live check with your keys: gateway roles on Anthropic/custom endpoint and the Tally feed"
phase: 6
type: VERIFY
status: backlog
priority: medium
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P0-T007, P0-T068, P6-T001, P6-T002, P6-T067, P6-T053, P6-T015, P6-T025, P6-T040]
requirements: [R6.01, R6.07, R6.03, R6.23]
roadmap_todos: []
modules: [M8, M10, M21, M22]
dashboards: [D09, D10]
tools: [uv, docker, sops, curl]
mcp: []
env: [ANTHROPIC_API_KEY, MT_CUSTOM_LLM_BASE_URL, MT_CUSTOM_LLM_API_KEY, TALLY_API_KEY]
services: [anthropic-api, custom-llm-endpoint, tally-api, litellm, llm-local, agents, postgres]
branch: p6/P6-T070-live-check-with-your-keys-gateway-roles-on-anthr
pr: ""
doc_sync: [docs/10-memory-rag-and-models.md, docs/13-wallets-treasury-and-onchain.md, docs/roadmap/phase-6-ai-models-treasury.md]
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

# P6-T070 · Live check with your keys: gateway roles on Anthropic/custom endpoint and the Tally feed

## Goal / expected outcome

The last, keyed step for the Phase 6 integrations that were built and tested keyless (build first, keys last): with your real keys from the sops file, the Phase 6 gateway roles (`debate`, `explain`, `memory`, `shadow`) work against `research-primary` (Anthropic) and `research-custom`, every call lands in `audit.llm_call` with real cost, the budgets and local fallback behave as in the fake-provider test, and the DAO monitor reads the live Tally API with your free key. Spend stays inside the daily role budgets.

## Context & references

- Requirements: [R6.01](../../../docs/roadmap/phase-6-ai-models-treasury.md#3-requirements) · [R6.07](../../../docs/roadmap/phase-6-ai-models-treasury.md#3-requirements) · [R6.03](../../../docs/roadmap/phase-6-ai-models-treasury.md#3-requirements) · [R6.23](../../../docs/roadmap/phase-6-ai-models-treasury.md#3-requirements) · ToDo none (supporting live check)
- Decision: [17 §E](../../../docs/17-decisions-register.md#e-ratification-2026-10-22) (live checks needing your keys are separate final VERIFY tasks depending on the USER task that provides them) · budgets [16 §2.10](../../../docs/16-configuration-and-safety-model.md#210-models-tier-b-and-llm-budgets)
- Spec: [10 §5](../../../docs/10-memory-rag-and-models.md#5-model-gateway-research-chat--debate-routing-m21) · [13 §4](../../../docs/13-wallets-treasury-and-onchain.md#4-hold-and-earn-module-m22-mt_treasury) (Tally free key) · [07 §2](../../../docs/07-security-notes.md#2-secrets)
- Cross-phase: P0-T007 (USER: Anthropic + custom endpoint keys in sops), P0-T068 (P0 live gateway smoke)
- Depends on (this phase): P6-T001 (budgets reviewed, endpoint confirmed), P6-T002 (USER: Tally key), P6-T067 (keyless sample runs), P6-T053 (fake-provider budget test), P6-T015 (explain), P6-T025 (shadow), P6-T040 (DAO monitor)

## Requirements

- One standard-depth debate on a crypto instrument via `research-primary`, one via `research-custom` (if configured); both return complete 03 M8 Signals.
- One anomaly brief via the `explain` role; one Hindsight reflection via `memory`; 20 shadow checks via `shadow`.
- `audit.llm_call`: one row per call with real `cost`, `role`, model, hashes; spend endpoint matches the provider's reported usage within rounding.
- Budget behaviour: temporarily lower the `shadow` daily budget to $0.01 (C1, tightening) → the next shadow call pauses/falls back as designed; restore the default afterwards (raising back is C3: do it with your approval or leave it lowered and note it).
- Tally: one live poll of proposals for a protocol in the test watch list; quota counter increments; the key never appears in logs.
- Total spend for this task ≤ US$2 (stated before starting; stop if exceeded).

## ToDo

- [ ] Preflight: `./kanban preflight P6-T070` (env names present in the tmpfs secrets; values never printed).
- [ ] Run the live debate(s), explain, memory and shadow calls; collect ids.
- [ ] Reconcile `audit.llm_call` with the spend endpoint and provider usage.
- [ ] Run the shadow-budget tightening check; restore per the requirement.
- [ ] Run one live Tally poll; record proposal ids.
- [ ] Record ids, spend and outcomes (no keys) in the progress log.

## Verification

### Tests
- Re-run `tests/integration/test_llm_budgets.py` in `--live` mode limited to the shadow-budget case.
- Tally client contract test against the live response (schema matches the recorded fixture used in CI).

### Scenarios
- Given your Anthropic key, when a debate runs on `research-primary`, then the Signal is complete and each call has an audit row with real cost.
- Given the `shadow` budget is tightened to $0.01, then the next shadow call is skipped (sampling pauses) and counted, never served by the model being checked.
- Given a wrong Tally key (simulated by an empty env var in a throwaway shell), then the client reports `auth_failed` and alerts without retry storms.

### Stress / failure injection
- Provider returns 429 during the run: fallback to `research-custom` then `local-advisor`, flagged `fallback_used`; no hard failure.

## Acceptance criteria

- [ ] Live Signals complete; audit rows with real cost for every call.
- [ ] Spend ≤ US$2 and within every role budget.
- [ ] Live Tally poll succeeded; quota tracked.
- [ ] No key in git, logs, chat or this file.

## Exceptions & edge cases

- No custom endpoint configured (P6-T001 left it disabled): skip that part and note it.
- Tally key not provided (P6-T002 declined): DAO monitor stays on Snapshot only; note it and pass the Tally part as "n/a by your decision".

## Cardinal rules (do NOT)

- Do NOT paste or print API keys; secrets stay in the sops file and tmpfs (07 §2).
- Do NOT raise any budget without C3; tightening is C1.
- Do NOT run load or budget-exhaustion tests against the paid provider (those are P6-T053 on the fake provider).
- Do NOT let Telegram text reach any prompt (12 §4–5).
- Do NOT commit secrets; do NOT skip, weaken or delete a test to get green.

## Doc sync on completion

- `docs/10-memory-rag-and-models.md` §5: live behaviour confirmed (no numbers that are secrets).
- `docs/13-wallets-treasury-and-onchain.md` §4: Tally live check noted.
- `docs/roadmap/phase-6-ai-models-treasury.md`: note this live check under R6.07 / T6.70 (no separate ToDo).

## Branch & PR

- Branch: `p6/P6-T070-live-check-with-your-keys-gateway-roles-on-anthr`
- PR title: `P6-T070: Live check with your keys: gateway roles on Anthropic/custom endpoint and the Tally feed`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P6-T070` run

## Progress log

- 2026-10-22 00:00 · aligner · created (build first, keys last: live LLM roles and Tally split out of P6-T002/P6-T040/P6-T053 per 17 §E)
