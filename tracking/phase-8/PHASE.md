---
phase: 8
title: MCP control plane (last, optional)
roadmap: docs/roadmap/phase-8-mcp.md
status: not_started
opens_after: [6]
force_open: false
started: ""
completed: ""
doc_sync_status: n/a
updated: 2026-10-21
---

# Phase 8 · MCP control plane (last, optional)

## Summary

This phase lets you talk to and control MasterTrader from Claude (Desktop/Code) or another MCP client. You can read and analyse, ask the agents, trade and adjust positions, and manage strategies, bots, risk and curation. Every action goes through `mt_api`, the risk manager (M11) and the WORM audit log. `mt_mcp` (M20) is a **thin adapter**: its tools are generated from the `mt_api` OpenAPI. All policy lives server-side in `mt_api`:
- a tool registry with a locked never-exposed set;
- approve mode as the default for MCP orders;
- C3 for any loosening or autonomous mode;
- a response guard that keeps Telegram text and tax PII out of Claude's context;
- a WORM `audit.mcp_call` trail.

The phase is gated by **your decision** after ≥ 4 weeks of daily UI/Telegram use (P8-T001). It ends with bypass, C3, tool-list, prompt-injection, audit and stress verification, a 2-week RUN and the exit demo.

**How the work is organised:**
1. Decision gate.
2. Server foundations: tokens, `mt_mcp` skeleton, registry, policy, guard, audit.
3. One task per tool group: read & analyse, agents, trade & adjust, strategies + bots, risk, curation.
4. Approval cards, container, D17 and docs.
5. Your client and policy setup.
6. Verification.
7. The 2-week RUN and the exit demo.

## Entry criteria

- [ ] Phase 6 done (`opens_after: [6]`): agents (M8), Hindsight memory (M9), anomaly explain agent (M10) callable via `mt_api`
- [ ] P2 command layer, M11, C3 change control, approvals queue + Telegram approval/TOTP and bots in daily use
- [ ] P0 `mt_api` with versioned OpenAPI, confirmation engine (C0–C3/Kill), `audit.command`, WORM layer and sops secrets in place
- [ ] **Decision gate (T8.01, P8-T001):** you've used the web UI and Telegram daily for ≥ 4 weeks and still want MCP

## Exit criteria

- [ ] **Exit demo (roadmap §6):** from Claude, "how are my strategies doing, tighten BTC max position to X, and close half my EURUSD" → the tighten applies instantly, the close waits for your Telegram approval, and both appear in D17 and `audit.command` (P8-T029)
- [ ] R8.01 thin adapter confirmed by code review + import-linter contract (P8-T003, P8-T023)
- [ ] R8.02 auth tests green: scoped, expiring tokens revoked in < 1 s; exposure only via stdio/localhost/Tailscale (P8-T020)
- [ ] R8.03 tool tests green for all six tool groups (P8-T008–T013, P8-T026)
- [ ] R8.04 bypass tests green: no MCP order skips M11 or approve mode; prompt-injection scenario passes (P8-T021, P8-T024)
- [ ] R8.05 C3 tests green: loosening via MCP needs Telegram + TOTP + cool-down; hard ceilings unwritable (P8-T022)
- [ ] R8.06 tool-list audit green: no withdrawal, key, mandate, approval or MCP-admin tool exists (P8-T023)
- [ ] R8.07 audit check green: every MCP call in `audit.mcp_call` / `audit.command` with source = mcp, visible in D17 (P8-T025)
- [ ] Two-week RUN done with day-7 and day-14 reviews signed (P8-T028)
- [ ] All tasks done or cancelled
- [ ] No open S1/S2 bugs

## Workstreams

| Workstream | Tasks |
|---|---|
| Your actions (USER) | P8-T001 decision gate · P8-T018 configure client + token · P8-T019 choose MCP policy + enable write tools · (gap P8-B010 policy stance) |
| Build: foundations | P8-T002 scoped tokens · P8-T003 `mt_mcp` server + OpenAPI generator · P8-T004 registry + never-exposed filter · P8-T005 approve-mode policy · P8-T006 response guard · P8-T007 MCP call audit |
| Build: tool groups | P8-T008 read & analyse · P8-T009 agents · P8-T010 trade & adjust · P8-T011 strategies + bots · P8-T012 risk · P8-T013 curation |
| Build: UI | P8-T014 MCP approval cards + badges · P8-T016 D17 MCP Console |
| Ops | P8-T015 `mcp` container (localhost/Tailscale, digest, hardening) |
| Docs | P8-T017 incident runbook + client setup guide · gaps P8-B001–B013 |
| Verify | P8-T020 auth/transport · P8-T021 bypass · P8-T022 C3 · P8-T023 tool-list audit · P8-T024 prompt injection · P8-T025 audit check · P8-T026 conversational scenarios · P8-T027 stress/failure · P8-T029 exit demo |
| Run | P8-T028 two weeks of use + D17 review |

## Critical path

P8-T001 → (P8-B004) P8-T002 → (P8-B001, P8-B005) P8-T004 → (P8-B002) P8-T005 → P8-T010 → P8-T014 → P8-T016 → P8-T018 → P8-T019 → P8-T024 → P8-T028 → P8-T029

In parallel off P8-T002: P8-T003 → P8-T015; P8-T006 and P8-T007 (both feed every tool group). The S2 gaps (P8-B001–B004) are cheap doc decisions but sit on the critical path, so resolve them first.

## Traceability

| Requirement | Tasks |
|---|---|
| R8.01 Thin adapter over `mt_api` | P8-T003, P8-T008, P8-T023, P8-T029 |
| R8.02 Transport + scoped revocable tokens | P8-T002, P8-T003, P8-T015, P8-T017, P8-T018, P8-T020, P8-T027, P8-T029 · gaps P8-B004, P8-B011, P8-B013 |
| R8.03 Tool groups | P8-T003, P8-T004, P8-T006, P8-T008, P8-T009, P8-T010, P8-T011, P8-T012, P8-T013, P8-T026, P8-T029 · gaps P8-B003, P8-B008, P8-B009 |
| R8.04 Every MCP order through M11; approve mode default | P8-T005, P8-T010, P8-T014, P8-T019, P8-T021, P8-T024, P8-T026, P8-T027, P8-T028, P8-T029 · gaps P8-B001, P8-B002, P8-B010 |
| R8.05 Loosening = C3; hard ceilings unwritable | P8-T005, P8-T011, P8-T012, P8-T022, P8-T026, P8-T029 · gap P8-B002 |
| R8.06 Never exposed: withdrawals, keys, mandates | P8-T004, P8-T006, P8-T017, P8-T023, P8-T029 · gaps P8-B001, P8-B005 |
| R8.07 Every call audited; D17 | P8-T002, P8-T007, P8-T014, P8-T016, P8-T025, P8-T026, P8-T027, P8-T028, P8-T029 · gaps P8-B007, P8-B012 |

| Roadmap ToDo | Tasks |
|---|---|
| T8.01 `USER` Decide whether to build MCP | P8-T001 |
| T8.02 `USER` Configure MCP client + scoped token | P8-T018 (guide: P8-T017) |
| T8.03 `USER` Choose MCP policy | P8-T019 (stance: P8-B010) |
| T8.20 `BUILD` `mt_mcp` server, OpenAPI tool schemas, token auth | P8-T002, P8-T003, P8-T006, P8-T007, P8-T008, P8-T009, P8-T010, P8-T011, P8-T012, P8-T013, P8-T020, P8-T026 |
| T8.21 `BUILD` Policy layer (approve mode, never-exposed filter) | P8-T004, P8-T005, P8-T006, P8-T014, P8-T026 |
| T8.22 `BUILD` D17 MCP Console | P8-T007, P8-T016, P8-T025 |
| T8.40 `OPS` `mcp` container on localhost/Tailscale; token in secrets | P8-T015, P8-T020 |
| T8.60 `VERIFY` Bypass tests (M11, approve mode, TOTP) | P8-T021, P8-T022, P8-T027 |
| T8.61 `VERIFY` Tool-list audit | P8-T023 |
| T8.62 `VERIFY` Prompt-injection test | P8-T024 |
| T8.80 `RUN` Two weeks of use; review D17 audit | P8-T028 |

## Planning notes & risks

**Design choices:**
- **Policy lives in `mt_api`, not `mt_mcp`.** An MCP token calling `mt_api` directly (skipping `mt_mcp`) must hit the same registry, approve-mode policy, response guard and audit. The bypass suite (P8-T021) tests exactly this.
- **Write tools ship disabled.** Read, agents, curation and `risk.kill.on` are enabled by default. Trade, strategies and risk-write tools stay off until you enable them in D17 (C3, P8-T019).
- **Claude counts as a model.** MCP responses are treated as model input: Telegram text and `model_input_ok = false` rows never reach Claude, tax PII is redacted and third-party text is wrapped as untrusted (P8-T006, gap P8-B003).
- **Reads are audited too.** R8.07 says "every call", and reads aren't commands. The plan adds a WORM table `audit.mcp_call` linked to `audit.command` (P8-T007, gap P8-B012).
- **Proposed numbers** (pending P8-B013 / P8-B004 / P8-B002):
  - token expiry 30 days (max 90);
  - rate limits: reads 60/min, agents 10/h, trades 10/min and 50/day;
  - response cap 64 KB;
  - MCP approval TTL 15 min;
  - C3 cool-down 15 min (from 02 §7.2).
- **Optional phase.** If P8-T001 is `no-go`, cancel every item. If `go-read-only`, cancel P8-T010–T012 and amend the exit demo.

**Risks:**
- **Prompt injection via pasted or read content.** Mitigated server-side (approve mode, no approval tool, C3, untrusted wrapping) and tested (P8-T024).
- **Self-escalation** (MCP approving its own orders or loosening its own policy). Mitigated by the never-exposed set (P8-B001, P8-T004).
- **Usage-policy tension** if auto rules skip human approval (P8-B010). Default "always approve".
- **Chaos testing must not touch the stack running the P7 paper clock or live accounts** (P8-T027 rule).
- **SDK supply chain:** pin `mcp` 2.3.0 or FastMCP 4.1.3 by hash and check for telemetry (P8-T003).

## Cross-phase prerequisites

| Phase | Roadmap IDs relied on |
|---|---|
| P0 | R0.02 (compose, digests), R0.05 (provenance columns), R0.07 / T0.23 (WORM layer, `audit.verify`, seals), R0.08 / T0.24 (`mt_api` auth, command bus, confirmation engine, `audit.command`, OpenAPI), R0.10 (Grafana/Loki), R0.11 (web shell, D16), R0.N1 (sops/age), R0.N2 (Tailscale-only), R0.N3 (segmentation), R0.N6 (viewport matrix) |
| P2 | R2.04–R2.06 (manifest, never-build validator, lifecycle), R2.10 (M11 on every order), R2.13 (`manual` sleeve), R2.16–R2.17 (pre-trade checks, venue registry), R2.18 (kill + dead-man), R2.19 / T2.24 (change control, hard ceilings), R2.20 (modes), R2.31–R2.32 (STP, idempotent IDs), R2.40–R2.44 (lab), R2.50 / T2.32 (D01, D03–D06), R2.51 / T2.33 (approvals + Telegram C3), R2.53 / R2.54 / T2.34 (bots, HITL) |
| P4 | R4.03 / T4.21 (Telegram rows `model_input_ok = false`, postures), R4.07 / T4.24 (RAG with `as_of`) |
| P5 | R5.10–R5.13 (airdrop discovery + risk scoring), R5.20–R5.22 / T5.30 (task queue) |
| P6 | R6.01 / T6.20 (debate graph), R6.04 (Hindsight), R6.05 / T6.22 (anomaly explain agent), R6.07 (LLM budgets) |
| P7 | Daily use of the platform (roadmap flow "P7 -. daily use .-> P8"); no live gate is needed, since P8 runs on paper/practice accounts unless P7 already allows live |
