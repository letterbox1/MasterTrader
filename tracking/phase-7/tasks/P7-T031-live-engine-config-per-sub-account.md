---
id: P7-T031
kind: task
title: Live engine config per sub-account, separate secrets and live alert routing
phase: 7
type: OPS
status: backlog
priority: critical
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P1-T045, P2-T021]
requirements: [R7.04]
roadmap_todos: [T7.40]
modules: [M12, M17, M15]
dashboards: [D05, D16]
tools: [git, docker, sops, uv]
mcp: []
env: []
services: [postgres, nats, alertmanager, telegram bot api, ntfy]
branch: p7/P7-T031-live-engine-config-per-sub-account
pr: ""
doc_sync: [docs/07-security-notes.md, docs/02-v1-architecture.md, docs/roadmap/phase-7-prove-and-go-live.md]
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

# P7-T031 · Live engine config per sub-account, separate secrets and live alert routing

## Goal / expected outcome

The `engine` container can run live trading per sub-account with its own config block and only that sub-account's secrets, exchange-facing containers use the exit-node egress (P7-T066), and live incidents route as critical alerts on Telegram + ntfy + email with quiet-hours override. Built and tested keyless (testnet/sandbox sub-accounts, fixture secret refs); the real live entries are added and audited in P7-T047 once P7-T007 provides keys.

## Context & references

- Roadmap: [R7.04 · ToDo T7.40](../../../docs/roadmap/phase-7-prove-and-go-live.md)
- Spec: [07 §3](../../../docs/07-security-notes.md#3-broker--exchange-keys) (sub-accounts per mandate) · [07 §2](../../../docs/07-security-notes.md#2-secrets) (per-service least privilege) · [07 §9](../../../docs/07-security-notes.md#9-monitoring--incident-response) (alerts on three channels) · [mob §3](../../../docs/ui/mobile-and-telegram.md#3-telegram-bot) (severity routing)
- Cross-phase (`depends_on`): P1-T045 (alert fan-out consumer, [17 §D P1-B007](../../../docs/17-decisions-register.md#d-other-decisions)), P2-T021 (engine node).
- Related: P7-T007 (keys, used later in P7-T047), P7-T032 (key audit at start-up), P7-T066 (egress namespace)

## Requirements

- Config `infra/engine/live/<venue>-<subaccount>.yaml`: venue, sub-account id, mandate/sleeve, mode ceiling (`hitl` or `autonomous`), STP mode, rate limits, secret refs (`live.<venue>.<subaccount>.*`).
- Secrets mounted to tmpfs per sub-account; `engine` gets its trade keys, the `deadman` sidecar its own trade-only keys (16 §3.1), `monitor` read-only recon keys only; LLM/agent containers get none. `engine`, `deadman` and `monitor` venue traffic uses the egress namespace (P7-T066).
- Engine refuses to start a live sub-account if the key audit (P7-T032) fails or preflight fails.
- Alert routes (Alertmanager + `alert.{severity}.{kind}`): live kill/criterion breach/system drawdown stage/recon unexplained/unconfirmed > 5 min/dead-man/resting-stop failure/egress mismatch or tunnel down → **critical** (all channels, ignores quiet hours); decay/downgrade → warning.
- Paper and live configs can never share a sub-account id (config validator).

## ToDo

- [ ] Config schema + validator in `mt_engine` (pydantic).
- [ ] Compose overrides for live; sops → tmpfs mapping per sub-account.
- [ ] Alertmanager routes + Telegram/ntfy/email templates for live incidents.
- [ ] Start-up guard (key audit + preflight).
- [ ] Tests; docs.

## Verification

### Tests
- Unit: validator rejects shared sub-account between paper and live; missing secret ref.
- Integration: engine start with a failing key audit → sub-account not started, critical alert.
- Integration: synthetic critical alert during quiet hours reaches all three channels.

### Scenarios
- Given two testnet sub-accounts configured live-shaped, when one key is revoked, then only that sub-account stops and the other continues.
- Given ntfy is down, then Telegram and email still deliver.

### Stress / failure injection
- Alert flood (100 critical in 1 min): grouped per kind, nothing dropped; Telegram 30 msg/s limit respected.

## Acceptance criteria

- [ ] Each live sub-account has its own config and secrets; least privilege verified by container inspection.
- [ ] Critical live alerts reach three channels.
- [ ] CI green.

## Exceptions & edge cases

- Secret rotation: reload without restart where the venue client supports it; else rolling restart outside sessions.
- Config drift: config hash logged at start in `audit.command`.

## Cardinal rules (do NOT)

- Do NOT mount live keys into any container other than `engine` and `deadman` (trade-only) and `monitor` (read-only).
- Do NOT commit secrets or paste them into chats, issues, PRs or logs; secrets live only in the sops/age file (07 §2).
- Do NOT use keys that are not trade-only, IP-locked and withdrawal-disabled; no live money before the P7 gates pass.
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.

## Doc sync on completion

- `docs/07-security-notes.md` §2–3: per-sub-account secret mounts.
- `docs/02-v1-architecture.md` §3.2: engine live configs.
- `docs/roadmap/phase-7-prove-and-go-live.md`: tick T7.40 when this item is done.

## Branch & PR

- Branch: `p7/P7-T031-live-engine-config-per-sub-account`
- PR title: `P7-T031: Live engine config per sub-account, separate secrets and live alert routing`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P7-T031` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (build first, keys last: keyless with testnet sub-accounts, live entries verified in P7-T047; deadman sidecar keys (16 §3.1); exit-node egress; deps P1-T045/P2-T021)
