---
phase: 8
title: MCP control plane (last, optional)
roadmap: docs/roadmap/phase-8-mcp.md
status: not_started
opens_after: [6]
force_open: false
hard_gate: true
started: ""
completed: ""
doc_sync_status: n/a
updated: 2026-10-22
---

# Phase 8 · MCP control plane (last, optional)

## Summary

This phase lets you talk to and control MasterTrader from Claude (Desktop/Code) or another MCP client. You can read and analyse, ask the agents (incl. `anomaly.explain`), trade and adjust positions, and manage strategies, bots, risk and curation. Every action goes through `mt_api`, the risk manager (M11) and the WORM audit log. `mt_mcp` (M20) is a **thin adapter**: its tools are generated from the `mt_api` OpenAPI. All policy lives server-side in `mt_api` ([16 §2.3, §2.12](../../docs/16-configuration-and-safety-model.md#212-mcp-phase-8), [02 §7.4](../../docs/02-v1-architecture.md#74-telegram--mcp), [17 §A](../../docs/17-decisions-register.md#a-s2-items-all-resolved)):
- a tool registry with the locked 16 §2.12 never-exposed set (incl. `approval.*` and `mcp.*`: MCP can never approve);
- C0 reads run; C1 per token scope; **every MCP order creates your approval card** (Telegram/web, TTL default 5 min, expiry = reject), with no skip-approval option; C3 via Telegram + TOTP + cool-down;
- loosening risk is never a scope (always C3 out of band); MCP may tighten, L0 included;
- tokens: opaque 256-bit, shown once, HMAC-SHA-256 with a server pepper, scoped (`read`, `analyse`, `trade`, `strategy`, `risk_tighten`, `curation`), instantly revocable, expiry 1d/7d/30d/1y/custom/indefinite (indefinite = warning + C3 + monthly reminder); OAuth 2.1 (PKCE, resource indicators);
- Streamable HTTP behind Caddy on Tailscale/TLS, stdio locally, optional legacy HTTP+SSE; resource subscriptions for fills, approvals, alerts;
- a response guard (provenance filter, no Telegram text, PII redacted, untrusted text wrapped);
- limits: 60 reads/min and 10 writes/min per token, 256 KB per result (configurable);
- every call, reads included, in WORM `audit.mcp_call` (commands also in `audit.command`, source `mcp`).

The phase is **hard-gated** ([17 §E](../../docs/17-decisions-register.md#e-ratification-2026-10-22)) and opens only after its prerequisite phases and **your decision** after ≥ 4 weeks of daily UI/Telegram use (P8-T001). Build first, keys last: everything is built and tested keyless with the MCP SDK client, fixtures, a fake Telegram harness, local models and the sandbox paper venue; your real client, tokens and Claude come in at the end (P8-T018, P8-T019, P8-T035). It ends with bypass, C3, tool-list, guard, limit, auth/transport, prompt-injection, audit and stress verification, a 2-week RUN and the exit demo.

**How the work is organised:**
1. Decision gate.
2. Server foundations: tokens, `mt_mcp` + transports, registry, order policy, response guard, audit, limits, OAuth, subscriptions.
3. One task per tool group: read & analyse, agents, trade & adjust, strategies + bots, risk, curation.
4. Approval cards, container, D17 and docs.
5. Keyless verification.
6. Your pepper, client, scopes and tool enables; the live client check.
7. The 2-week RUN and the exit demo.

## Entry criteria

- [ ] Phase 6 done (`opens_after: [6]`, hard gate): agents (M8), Hindsight memory (M9), anomaly explain agent (M10) callable via `mt_api`
- [ ] P2 command layer, M11, C3 change control, approvals queue + Telegram approval/TOTP and bots in daily use
- [ ] P0 `mt_api` with versioned OpenAPI, confirmation engine (C0–C3/Kill), `audit.command`, WORM layer and sops secrets in place
- [ ] **Decision gate (T8.01, P8-T001):** you've used the web UI and Telegram daily for ≥ 4 weeks and still want MCP

## Exit criteria

- [ ] **Exit demo (roadmap §6):** from Claude, "how are my strategies doing, tighten BTC max position to X, and close half my EURUSD" → the tighten applies instantly, the close waits for your Telegram approval, and both appear in D17, `audit.mcp_call` and `audit.command` (P8-T029)
- [ ] R8.01 thin adapter confirmed by code review + import-linter contract (P8-T003, P8-T023)
- [ ] R8.02 / R8.08 auth + transport tests green: tokens shown once and stored as HMAC, revocation < 1 s, expiry enforced and indefinite needs C3, Streamable HTTP resume + stdio (+ legacy if enabled), OAuth 2.1, `/mcp` only via Caddy on Tailscale/TLS (P8-T020); live client check passed (P8-T035)
- [ ] R8.03 tool tests green for all six tool groups incl. `anomaly.explain`, `/bots`, `/approvals`, `source=` filters (P8-T008–T013, P8-T026)
- [ ] R8.04 bypass tests green: no MCP order skips M11 or its approval card; MCP can't call `approval.*` or `mcp.*`; prompt-injection scenario passes keyless and with Claude (P8-T021, P8-T024, P8-T035)
- [ ] R8.05 C3 tests green: every loosening via MCP needs Telegram + TOTP + cool-down; tightening (L0 included) instant (P8-T022)
- [ ] R8.06 tool-list audit green: nothing from the 16 §2.12 never-exposed list exists (P8-T023)
- [ ] R8.07 audit check green: every MCP call, reads included, in `audit.mcp_call`; commands in `audit.command` with source = mcp; visible in D17 (P8-T025)
- [ ] R8.09 response-guard tests green: Telegram rows, `model_input_ok = false` rows and tax PII never reach the client unredacted (P8-T033)
- [ ] R8.10 limit tests green: 61st read / 11th write in a minute throttled; results over 256 KB capped (P8-T034)
- [ ] Two-week RUN done with day-7 and day-14 reviews signed (P8-T028)
- [ ] All tasks done or cancelled
- [ ] No open S1/S2 bugs

## Workstreams

| Workstream | Tasks |
|---|---|
| Your actions (USER) | P8-T001 decision gate · P8-T018 pepper + client + first token · P8-T019 scopes/expiry per client + enable write tools |
| Build: foundations | P8-T002 tokens · P8-T003 `mt_mcp` + Streamable HTTP/stdio · P8-T004 registry + never-exposed · P8-T005 order policy · P8-T006 response guard (T8.23) · P8-T007 MCP call audit · P8-T030 limits + cap · P8-T031 OAuth 2.1 · P8-T032 subscriptions + legacy HTTP+SSE |
| Build: tool groups | P8-T008 read & analyse · P8-T009 agents · P8-T010 trade & adjust · P8-T011 strategies + bots · P8-T012 risk · P8-T013 curation |
| Build: UI | P8-T014 MCP approval cards + badges · P8-T016 D17 MCP Console |
| Ops | P8-T015 `mcp` container (`edge`, Caddy `/mcp`, Tailscale, pepper in sops) |
| Docs | P8-T017 incident runbook + client setup guide |
| Verify (keyless) | P8-T020 auth/transport · P8-T021 bypass · P8-T022 C3 · P8-T023 tool-list audit · P8-T024 prompt injection · P8-T025 audit check · P8-T026 conversational scenarios · P8-T027 stress/failure · P8-T033 response guard · P8-T034 limits |
| Verify (keys last) | P8-T035 live client check with your client and Claude · P8-T029 exit demo |
| Run | P8-T028 two weeks of use + D17 review |

## Critical path

P8-T001 → P8-T002 → P8-T004 → P8-T005 → P8-T010 → P8-T014 → P8-T016 → P8-T017 → P8-T018 → P8-T019 → P8-T035 → P8-T028 → P8-T029

In parallel off P8-T002: P8-T003 → (P8-T015, P8-T031, P8-T032); P8-T006 and P8-T007 (feed every tool group); P8-T030 after P8-T004 + P8-T007. All keyless VERIFY tasks except P8-T035 run before your USER steps, so the live part is short. Cross-phase `depends_on` entries point at the P0/P2/P4/P5/P6 tasks each item builds on.

## Traceability

| Requirement | Tasks |
|---|---|
| R8.01 Thin adapter over `mt_api` | P8-T003, P8-T008, P8-T023, P8-T029 |
| R8.02 Transport + scoped revocable tokens | P8-T002, P8-T003, P8-T015, P8-T017, P8-T018, P8-T020, P8-T027, P8-T029, P8-T031, P8-T035 |
| R8.03 Tool groups (incl. `anomaly.explain`, `/bots`, `/approvals`, `source=`) | P8-T003, P8-T004, P8-T006, P8-T008, P8-T009, P8-T010, P8-T011, P8-T012, P8-T013, P8-T026, P8-T029, P8-T032 |
| R8.04 Every MCP order through M11 and your approval card; MCP can never approve | P8-T005, P8-T010, P8-T014, P8-T019, P8-T021, P8-T024, P8-T026, P8-T027, P8-T028, P8-T029, P8-T035 |
| R8.05 Loosening never a scope (C3 out of band); MCP may tighten | P8-T005, P8-T011, P8-T012, P8-T022, P8-T026, P8-T029 |
| R8.06 Never exposed (16 §2.12) | P8-T004, P8-T017, P8-T023, P8-T029 |
| R8.07 Every call audited (`audit.mcp_call`); D17 | P8-T002, P8-T007, P8-T014, P8-T016, P8-T020, P8-T025, P8-T026, P8-T027, P8-T028, P8-T029 |
| R8.08 Transport & tokens (HMAC + pepper, expiry options, OAuth 2.1, Streamable HTTP/stdio/legacy, subscriptions) | P8-T002, P8-T003, P8-T015, P8-T016, P8-T017, P8-T018, P8-T019, P8-T020, P8-T026, P8-T029, P8-T031, P8-T032, P8-T035 |
| R8.09 Response guard | P8-T006, P8-T024, P8-T029, P8-T033 |
| R8.10 Limits (60 reads/min, 10 writes/min per token, 256 KB) | P8-T029, P8-T030, P8-T034 |

| Roadmap ToDo | Tasks |
|---|---|
| T8.01 `USER` Decide whether to build MCP | P8-T001 |
| T8.02 `USER` Configure MCP client + scoped token | P8-T018 (guide: P8-T017) |
| T8.03 `USER` Choose token scopes and expiry per client | P8-T019 |
| T8.20 `BUILD` `mt_mcp` server, OpenAPI tool schemas, token auth | P8-T003, P8-T008, P8-T009, P8-T010, P8-T011, P8-T012, P8-T013, P8-T026 |
| T8.21 `BUILD` Policy layer (confirmation mapping, never-exposed filter, rate limits, response cap) | P8-T004, P8-T005, P8-T014, P8-T026, P8-T030 |
| T8.22 `BUILD` D17 MCP Console | P8-T007, P8-T016, P8-T025 |
| T8.23 `BUILD` Response guard | P8-T006 |
| T8.24 `BUILD` Token lifecycle, OAuth 2.1, transports, subscriptions, `audit.mcp_call` | P8-T002, P8-T003, P8-T007, P8-T031, P8-T032 |
| T8.40 `OPS` `mcp` container behind Caddy, Tailscale only; pepper in secrets | P8-T015, P8-T020 |
| T8.60 `VERIFY` Bypass tests | P8-T021, P8-T022, P8-T027 |
| T8.61 `VERIFY` Tool-list audit | P8-T023 |
| T8.62 `VERIFY` Prompt-injection test | P8-T024, P8-T035 |
| T8.63 `VERIFY` Response-guard test | P8-T033 |
| T8.64 `VERIFY` Auth + transport tests | P8-T020, P8-T025, P8-T035 |
| T8.65 `VERIFY` Limit tests | P8-T034 |
| T8.80 `RUN` Two weeks of use; review D17 audit | P8-T028 |

## Planning notes & risks

**Design choices:**
- **Policy lives in `mt_api`, not `mt_mcp`.** An MCP token calling `mt_api` directly (skipping `mt_mcp`) hits the same registry, policy, guard, limits and audit. The bypass (P8-T021), guard (P8-T033) and limit (P8-T034) suites test exactly this.
- **Write tools ship disabled.** `read`, `analyse` and `curation` tools are enabled by default; trade, strategy and risk tools stay off until you enable them in D17 (C3, P8-T019). Write-scope tokens are C3 to create.
- **Claude counts as a model.** MCP responses and notifications pass the response guard (P8-T006).
- **Reads are audited too** in WORM `audit.mcp_call` (17 §D P8-B012).
- **All numbers are 16 settings:** approval TTL 5 min (16 §2.3), C3 cool-down 15 min, 60 reads/min and 10 writes/min per token, 256 KB per result (16 §2.12). No hard-coded limits.
- **Optional phase.** If P8-T001 is `no-go`, cancel every item. If `go-read-only`, cancel P8-T010–T012 and amend the exit demo.

**Risks:**
- **Prompt injection via read content.** Mitigated server-side (cards for every order, no approval tool, C3 for loosening, untrusted wrapping) and tested keyless (P8-T024) and with Claude (P8-T035).
- **Self-escalation** (MCP approving its own orders or changing its own policy/tokens). Mitigated by the never-exposed set (`approval.*`, `mcp.*`) (P8-T004, P8-T021).
- **Indefinite tokens** widen exposure. Mitigated by C3, the red warning and the monthly reminder (P8-T002), and reviewed in the RUN (P8-T028).
- **Chaos testing must not touch the stack running the P7 paper clock or live accounts** (P8-T027 rule).
- **SDK / OAuth library supply chain:** pin `mcp` 2.3.0 or FastMCP 4.1.3 and the OAuth library by hash and check for telemetry (P8-T003, P8-T031).

## Cross-phase prerequisites

These are explicit `depends_on` entries in the task files.

| Phase | Tasks relied on |
|---|---|
| P0 | P0-T007 (LLM gateway credentials; live check only), P0-T014 (workspace), P0-T020 (compose + Caddy), P0-T021 (networks), P0-T022 (sops), P0-T023 (observability), P0-T025 (provenance columns), P0-T029/T030/T031/T037 (WORM layer, chain, audit tables, seal), P0-T032 (mt_api + OpenAPI), P0-T033 (auth), P0-T034 (command bus + `audit.command`), P0-T035 (confirmation engine), P0-T036 (WebSocket hub), P0-T042 (LiteLLM), P0-T044 (local model), P0-T046 (audit queries), P0-T049/T050 (components, shell) |
| P2 | P2-T006 (strategy commands), P2-T011 (L0 ceilings in settings), P2-T020 (risk/order command surface), P2-T021 (engine), P2-T023 (testnet + sandbox venue), P2-T031 (kill switch), P2-T033 (modes + approval routing), P2-T035 (Telegram C3 TOTP), P2-T036/T037 (bots), P2-T038/T039/T149 (approvals API, Telegram cards, web queue), P2-T043 (D06 changes), P2-T117 (lab API) |
| P4 | P4-T019 (Telegram postures), P4-T025 (provenance gate), P4-T032 (RAG retrieval), P4-T043 (intel queries/commands) |
| P5 | P5-T029 (task queue), P5-T033 (discovery intake / add URL) |
| P6 | P6-T007 (debate graph), P6-T012 (memory API), P6-T015 (anomaly explain agent) |
| P7 | Daily use of the platform (roadmap flow "P7 -. daily use .-> P8"); no live gate is needed, since P8 runs on paper/practice accounts unless P7 already allows live |
