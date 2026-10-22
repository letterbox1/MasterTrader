---
id: P7-T032
kind: task
title: Live key audit job: scopes, IP lock, withdrawals, age
phase: 7
type: BUILD
status: backlog
priority: high
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P0-T052]
requirements: [R7.04, R7.14]
roadmap_todos: [T7.40]
modules: [M17, M12]
dashboards: [D16, D05]
tools: [git, uv]
mcp: []
env: []
services: [postgres, prefect-server, mt-api]
branch: p7/P7-T032-live-key-audit-job
pr: ""
doc_sync: [docs/07-security-notes.md, docs/ui/dashboards/D16-system.md, docs/roadmap/phase-7-prove-and-go-live.md]
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

# P7-T032 · Live key audit job: scopes, IP lock, withdrawals, age

## Goal / expected outcome

A key audit (`system.key.audit`, daily and at engine start) verifies for every live key: trade-only scopes, withdrawals disabled, IP allow-list equal to exactly the exit node's static IP (16 §3.2), and age < 90 days (rotation, 16 §2.3), using each venue's permission endpoint where one exists and a documented manual attestation where not.

## Context & references

- Roadmap: [R7.04 · ToDo T7.40](../../../docs/roadmap/phase-7-prove-and-go-live.md)
- Spec: [07 §3](../../../docs/07-security-notes.md#3-broker--exchange-keys) · [16 §3.2](../../../docs/16-configuration-and-safety-model.md#32-network-egress-and-ip-locked-keys) · [07 §2](../../../docs/07-security-notes.md#2-secrets) (90-day rotation, key-age alert) · [12 §2](../../../docs/12-policy-and-compliance.md#2-venue-access-registry) (key model per venue) · [D16](../../../docs/ui/dashboards/D16-system.md) (keys metadata only)
- Related: P7-T007, P7-T031, P7-T047 (live run, T7.65) · cross-phase P0-T052 (`depends_on`: D16 Security/keys page)

## Requirements

- Per venue: use permission introspection where available (e.g. Binance `apiRestrictions`, Kraken key info, OKX `account/config`/API key perms); otherwise require a signed manual attestation row (date, screenshot reference) renewed every 90 days.
- Fail if: any withdrawal/transfer scope; no IP restriction, or an allow-list containing anything other than the configured exit-node IP (and the VPS IP for FP Markets); age ≥ 90 days (warn at 80; both settings); attestation missing/expired.
- Results in `audit.key_audit` (WORM); D16 keys view shows status (masked metadata only).
- Engine start-up guard consumes the latest result.

## ToDo

- [ ] `packages/mt_obs/key_audit/` with per-venue introspectors.
- [ ] Attestation command `system.key.attest` (C1).
- [ ] Daily Prefect flow + start-up hook.
- [ ] Tests; docs.

## Verification

### Tests
- Unit: introspector parsers for each supported venue (fixtures).
- Integration (fixtures, no keys): key with withdrawal scope fails audit and blocks start; key allow-listed to an extra IP fails with `ip_allowlist_mismatch`.

### Scenarios
- Given a key is 85 days old, then D16 shows amber and Telegram warns; at 90 days the sub-account stops.

### Stress / failure injection
- Venue permission endpoint down: result `unknown` → warn; after 24 h unknown → treated as fail.

## Acceptance criteria

- [ ] Daily audit with WORM results; failing keys block live start.
- [ ] CI green.

## Exceptions & edge cases

- Venue doesn't expose IP lock state: attestation required.
- Rotation: new key audited before old is revoked.

## Cardinal rules (do NOT)

- Do NOT log key material; only key id suffix and metadata.
- Do NOT commit secrets or paste them into chats, issues, PRs or logs; secrets live only in the sops/age file (07 §2).
- Do NOT use keys that are not trade-only, IP-locked and withdrawal-disabled; no live money before the P7 gates pass.
- Do NOT update or delete WORM rows; corrections are new rows with `supersedes_id` (15 §2).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.

## Doc sync on completion

- `docs/07-security-notes.md` §3: audit method per venue.
- `docs/ui/dashboards/D16-system.md`: key audit status.
- `docs/roadmap/phase-7-prove-and-go-live.md`: tick T7.40 when this item is done.

## Branch & PR

- Branch: `p7/P7-T032-live-key-audit-job`
- PR title: `P7-T032: Live key audit job: scopes, IP lock, withdrawals, age`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P7-T032` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (allow-list must equal the exit-node IP (16 §3.2); 90-day rotation (16 §2.3); keyless fixtures, live run in P7-T047)
