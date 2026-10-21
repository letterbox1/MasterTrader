---
id: P0-T035
kind: task
title: Implement the server-side confirmation-level engine (C0–C3, Kill)
phase: 0
type: BUILD
status: backlog
priority: critical
size: L
severity: ""
owner: agent
claimed_by: ""
depends_on: [P0-T034, P0-T033]
requirements: [R0.08]
roadmap_todos: [T0.24]
modules: [mt_api, M11]
dashboards: []
branch: p0/P0-T035-confirmation-level-engine
pr: ""
doc_sync: [docs/02-v1-architecture.md, docs/ui/README.md, docs/roadmap/phase-0-foundations.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P0-T035 · Implement the server-side confirmation-level engine (C0–C3, Kill)

## Goal / expected outcome

Confirmation levels are enforced **in mt_api**, never only in the UI: C0 runs; C1/C2 require a server-issued confirmation token bound to the exact args; C3 requires C2 + an approval on an out-of-band channel + a fresh TOTP + a cool-down (default 15 min) before it applies and stays cancellable; Kill ON is a single confirm that is never blocked; Kill OFF is C3.

## Context & references

- [Roadmap P0 R0.08](../../../docs/roadmap/phase-0-foundations.md#3-requirements)
- [02 §7.2 commands](../../../docs/02-v1-architecture.md#72-commands-rest-write) (confirmation levels)
- [02 §8 flows (F5, F6, F11)](../../../docs/02-v1-architecture.md#8-end-to-end-flows)
- [07 §6 application controls](../../../docs/07-security-notes.md#6-application-controls)
- [ui §3.3 confirmation](../../../docs/ui/README.md#33-actions--confirmation)
- [components §4 forms](../../../docs/ui/components.md#4-forms--controls) (`ConfirmSheet`, `C3Flow`)
- Telegram approval channel is built in P2 (T2.33); until then C3 uses the host break-glass channel — see P0-B002. C1/C2 server-side mechanism is unspecified in 02 §7.2 — see P0-B003.
- Depends on: P0-T034, P0-T033

## Requirements

- Preview: `POST /commands/{command}/preview` returns `{level, summary, diff?, risk_preview?, confirmation_token, expires_at}`; token = HMAC(server key, command‖args_hash‖session‖nonce), TTL 120 s, single use.
- C1/C2: execution requires `confirmation_token` in the body; mismatch/expired → 428 problem+json `confirmation_required`. C2 preview carries the risk-preview payload (stub `not_applicable` in P0; M11 fills it in P2).
- C3: execution creates `ops.pending_confirmation` (status `awaiting_approval → awaiting_totp → cooling_down → applied | cancelled | expired`), audit row `pending_confirmation`; requires (1) approval via an `ApprovalChannel` (Protocol; implementations: `BreakGlassCliChannel` in P0 — `mt-admin approve <id>` over SSH on the host — and `TelegramChannel` in P2), (2) a fresh TOTP verified by mt-api after approval, (3) cool-down `ops.setting c3_cooldown_s` default 900; then applies. Session is re-checked at apply time (ui §3.6). Approval TTL 10 min → `expired`.
- Cancel: `POST /commands/pending/{id}/cancel` (C0) at any state before applied.
- Kill ON (`risk.kill.on`): single confirm token, **bypasses** lockouts, rate limits and C-level queues; writes NATS KV `kill = {on: true, reason, by, ts}` and publishes `kill.set`; must succeed even if Postgres is down (audit retried from a local spool file, then written). Kill OFF (`risk.kill.off`) is C3 and requires the trigger condition cleared (P0: always clear).
- Level classification can depend on args via a `classify(args, current) -> Level` hook (tighten vs loosen; used by `system.settings.update` and in P2 by `risk.policy.update`).
- Every transition is a new `audit.command` row (WORM).

## ToDo

- [ ] Implement preview/token issuance and verification.
- [ ] Implement the C3 state machine, `ApprovalChannel` protocol, `BreakGlassCliChannel` (`mt-admin` CLI talking to mt-api over a Unix socket), cool-down scheduler (Prefect or in-process timer with persistence on restart).
- [ ] Implement Kill ON fast path + spool; Kill OFF as C3.
- [ ] Implement `classify` hook and wire `system.settings.update`.
- [ ] Publish pending/applied events on WS `notifications`.
- [ ] Unit/integration tests; the adversarial set is P0-T054.

## Verification

### Tests
- Unit: token binding (args change → invalid), single use, expiry.
- Integration: C3 path through break-glass approve + TOTP + 900 s cool-down (FrozenClock/SimClock) → applied; each audit row present.
- Integration: Kill ON with Postgres paused → KV set, response 200, audit row appears after DB returns.

### Scenarios
- Given a C3 change is approved but no TOTP is supplied within 10 min, then it expires and nothing applies.
- Given mt-api restarts during a cool-down, then the pending change resumes its timer from `ops.pending_confirmation` and applies at the original time.
- Given a stolen session cookie, when the attacker submits a C3 command, then nothing applies without the out-of-band approval and TOTP.

### Stress / failure injection
- Kill ON latency: p99 < 200 ms from request to KV write under 200 req/s background load (supports the 02 §9.2 'kill → cancels < 1 s' SLO later).

## Acceptance criteria

- [ ] C0–C3/Kill enforced server-side (UI cannot skip by calling the API directly — tested)
- [ ] C3 requires approval + TOTP + cool-down; cancellable; survives restart
- [ ] Kill ON never blocked (DB down, lockout, rate limit tested)
- [ ] Every transition audited
- [ ] CI green (ruff, mypy, pytest, gitleaks, `pit` check)

## Exceptions & edge cases

- Clock jumps during cool-down: timers use wall-clock `apply_at` stored in DB + monotonic checks; never apply early.
- Break-glass channel requires SSH over Tailscale + host TOTP prompt; it is audited `source=system` with the approving channel name.

## Cardinal rules (do NOT)

- Do NOT implement confirmation only in the UI.
- Do NOT let anything delay or block Kill ON.
- Do NOT allow C3 apply without TOTP, even from the break-glass CLI.
- Loosening risk, autonomous mode and mandates are C3 (Telegram + TOTP + cool-down); Kill ON and protective exits never wait for approval.
- Do NOT bypass `mt_api`, the risk manager (M11) or `mt_store.pit(as_of)`; every order goes through M11.
- Do NOT UPDATE or DELETE WORM rows, ever; corrections are new rows with `supersedes_id` ([15 §2](../../../docs/15-bots-hitl-and-worm-audit.md#2-worm-records-write-once-read-many)).
- Do NOT skip, weaken or delete a test to get CI green.

## Doc sync on completion

- `docs/02-v1-architecture.md` §7.2: document preview tokens, the C3 state machine and the P0 break-glass channel; `docs/ui/README.md` §3.3: note the 428 `confirmation_required` contract.
- `docs/roadmap/phase-0-foundations.md`: tick T0.24 when every item mapped to it is done.

## Branch & PR

- Branch: `p0/P0-T035-confirmation-level-engine`
- PR title: `P0-T035: Implement the server-side confirmation-level engine (C0–C3, Kill)`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P0-T035` run

## Progress log

- 2026-10-21 00:00 · planner · created
