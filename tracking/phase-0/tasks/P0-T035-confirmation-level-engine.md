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
requirements: [R0.08, R0.12]
roadmap_todos: [T0.24, T0.27]
modules: [mt_api, M11]
dashboards: []
tools: [git, uv, python>=3.12, docker]
mcp: []
env: []
services: [postgres, nats]
branch: p0/P0-T035-confirmation-level-engine
pr: ""
doc_sync: [docs/02-v1-architecture.md, docs/ui/README.md, docs/roadmap/phase-0-foundations.md]
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

# P0-T035 · Implement the server-side confirmation-level engine (C0–C3, Kill)

## Goal / expected outcome

Confirmation levels are enforced **in mt_api**, never only in the UI: C0 runs; C1 requires the `confirm_token` from the preview call; C2 requires a token carrying the risk-preview hash bound to the exact command plus a session re-authenticated within 12 h; C3 requires C2 + an approval on an out-of-band channel + a fresh TOTP + a cool-down (default 15 min, [16 §2.3](../../../docs/16-configuration-and-safety-model.md#23-decisions-approvals-and-hitl)) before it applies and stays cancellable; Kill ON is a single confirm that is never blocked; Kill OFF is C3.

## Context & references

- [Roadmap P0 R0.08](../../../docs/roadmap/phase-0-foundations.md#3-requirements)
- [02 §7.2 commands](../../../docs/02-v1-architecture.md#72-commands-rest-write) (confirmation levels)
- [02 §8 flows (F5, F6, F11)](../../../docs/02-v1-architecture.md#8-end-to-end-flows)
- [07 §6 application controls](../../../docs/07-security-notes.md#6-application-controls)
- [ui §3.3 confirmation](../../../docs/ui/README.md#33-actions--confirmation)
- [components §4 forms](../../../docs/ui/components.md#4-forms--controls) (`ConfirmSheet`, `C3Flow`)
- Decided in [17 §D](../../../docs/17-decisions-register.md#d-other-decisions) (P0-B002, P0-B003, both closed): until Telegram C3 exists (P2, T2.07/T2.24 retire it), C3 completes through the host-only break-glass CLI `mtctl approve <id>` + TOTP over SSH/Tailscale, audited (R0.12, T0.27); C1/C2 use the preview-token contract of 02 §7.2.
- Depends on: P0-T034, P0-T033

## Requirements

- Preview: `POST /commands/{command}/preview` returns `{level, summary, diff?, risk_preview?, preview_hash?, confirm_token, expires_at}` (02 §7.2); token = HMAC(server key, command‖args_hash‖preview_hash‖session‖nonce), single use, TTL a setting (default 120 s, `ops.setting confirm_token_ttl_s`, [16 §2.3](../../../docs/16-configuration-and-safety-model.md#23-decisions-approvals-and-hitl)).
- C1: execution requires `confirm_token` in the body; missing/mismatch/expired → 428 problem+json `confirmation_required`.
- C2: the token also binds the risk-preview hash of the exact command (stub preview `not_applicable` in P0; M11 fills it in P2) **and** the session must have re-authenticated within 12 h (default, setting `c2_reauth_max_age_s`; P0-T033 `/auth/reauth`) → otherwise 428 `reauth_required`.
- C3: execution creates `ops.pending_confirmation` (status `awaiting_approval → awaiting_totp → cooling_down → applied | cancelled | expired`), audit row `pending_confirmation`; requires (1) approval via an `ApprovalChannel` (Protocol; implementations: `BreakGlassCliChannel` in P0 — `mtctl approve <id>` over SSH on the host — and `TelegramChannel` in P2), (2) a fresh TOTP verified by mt-api after approval, (3) cool-down `ops.setting c3_cooldown_s` (default 900 s = 15 min, [16 §2.3](../../../docs/16-configuration-and-safety-model.md#23-decisions-approvals-and-hitl)); then applies. Session is re-checked at apply time (ui §3.6). Approval TTL a setting (default 10 min, `c3_approval_ttl_s`, [16 §2.3](../../../docs/16-configuration-and-safety-model.md#23-decisions-approvals-and-hitl)) → `expired`. While the UI waits it shows 'Waiting for break-glass approval' (ui §3.3).
- Cancel: `POST /commands/pending/{id}/cancel` (C0) at any state before applied.
- Kill ON (`risk.kill.on`): single confirm token, **bypasses** lockouts, rate limits and C-level queues; writes NATS KV `kill = {on: true, reason, by, ts}` and publishes `kill.set`; must succeed even if Postgres is down (its record goes through the JetStream WORM buffer, P0-T031, [16 §3.3](../../../docs/16-configuration-and-safety-model.md#33-records-the-write-path-vs-the-integrity-check), and lands in `audit.command` when the DB returns). Kill OFF (`risk.kill.off`) is C3 and requires the trigger condition cleared (P0: always clear).
- Level classification can depend on args via a `classify(args, current) -> Level` hook (tighten vs loosen; used by `system.settings.update` and in P2 by `risk.policy.update`).
- Every transition is a new `audit.command` row (WORM).

## ToDo

- [ ] Implement preview/token issuance and verification.
- [ ] Implement the C3 state machine, `ApprovalChannel` protocol, `BreakGlassCliChannel` (`mtctl` CLI talking to mt-api over a Unix socket), cool-down scheduler (Prefect or in-process timer with persistence on restart).
- [ ] Implement Kill ON fast path (KV first, record via the JetStream buffer); Kill OFF as C3.
- [ ] Implement `classify` hook and wire `system.settings.update`.
- [ ] Publish pending/applied events on WS `notifications`.
- [ ] Unit/integration tests; the adversarial set is P0-T054.

## Verification

### Tests
- Unit: token binding (args change → invalid), single use, expiry; C2 preview-hash mismatch → 428.
- Integration: C2 with a session re-authenticated 12 h + 1 s ago → 428 `reauth_required`; after `/auth/reauth` → accepted.
- Integration: C3 path through `mtctl approve` + TOTP + the configured cool-down (default 900 s; FrozenClock/SimClock) → applied; each audit row present.
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
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (preview contract with confirm_token + C2 risk-preview hash + 12 h re-auth (17 §D P0-B003), break-glass mtctl approve (P0-B002, R0.12/T0.27), cool-down/TTLs as settings (16 §2.3), Kill recorded via JetStream buffer; run fields added)
