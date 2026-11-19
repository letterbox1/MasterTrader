---
id: P7-T073
kind: task
title: Shift to the go-live runtime host: harden, migrate, deploy, re-verify
phase: 7
type: OPS
status: backlog
priority: critical
size: L
severity: ""
owner: agent
claimed_by: ""
depends_on: [P7-T071, P7-T072, P0-T003, P7-T066]
requirements: [R7.18, R7.04]
roadmap_todos: [T7.44]
modules: [M17, M11, M12]
dashboards: [D16]
tools: [git, cargo, uv, pnpm, docker, supabase, vercel, tailscale]
mcp: []
env: []
services: [supabase-postgres, mt-api, nats, engine, deadman]
branch: p7/P7-T073-shift-to-the-go-live-runtime-host-harden-migrate
pr: ""
doc_sync: [docs/18-platform-and-deployment.md, docs/02-v1-architecture.md, docs/07-security-notes.md, docs/roadmap/phase-7-prove-and-go-live.md]
doc_sync_status: n/a
found_in: ""
created: 2026-11-19
updated: 2026-11-19
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
review_result: ""
---
# P7-T073 · Shift to the go-live runtime host: harden, migrate, deploy, re-verify

## Goal / expected outcome

The system that was built and paper-traded on the workstation runs on the runtime host chosen in P7-T071 (default: the same workstation), hardened for live money, and the **full verification suite passes on that target** before any live funding. Workstation first, test, then shift ([18 §9](../../../docs/18-platform-and-deployment.md#9-workstation-first-build-path)).

## Context & references

- Modes: [18 §5](../../../docs/18-platform-and-deployment.md#5-deployment-modes) · DB: [18 §4](../../../docs/18-platform-and-deployment.md#4-database-supabase-postgres) · hardening baseline: P0-T019, [07 §5](../../../docs/07-security-notes.md#5-network--host) · Decisions: [17 §G](../../../docs/17-decisions-register.md#g-platform-rust-and-python-supabase-vercel-workstation-first-2026-11-19)
- Depends on: P7-T071 (choice), P7-T072 (YubiKey), P0-T003 (Tailscale). Related: P7-T065/P7-T066 (egress exit node; conditional: cancelled if the runtime host is a static-IP VM, in which case that VM's IP is the egress IP), P7-T009 (UPS/4G for a workstation host).
- Unblocks: P7-T057 (fund micro-live).

## Requirements

- **Host hardening for live:** LUKS full-disk encryption verified (required now, warning-only before); SSH keys-only and reachable only over Tailscale; firewall allows inbound only on `tailscale0`; unattended security upgrades; chrony; the P0-T019 checklist passes in `live` profile.
- **Database:** `local` stays self-hosted Supabase; `supabase_cloud`: `supabase link` + `supabase db push`, data migrated with a verified row-count and hash-chain check on every WORM table, the external seal re-anchored, backups configured (18 §4.7).
- **Web:** `local` stays on Caddy; `vercel`: deploy `apps/web` with `api.exposure: tailnet` by default; Deployment Protection on.
- **Re-verify on the target:** the full suite (risk, `pit`, WORM and tax golden tests; dead-man drill; restore test; egress check) passes on the target; results linked in the progress log.
- Secrets: env var names only here (`SUPABASE_ACCESS_TOKEN`, `SUPABASE_DB_PASSWORD`, `VERCEL_TOKEN` when used); values in the sops file.
- **Egress:** the P1-T071 egress check points at the egress IP (the exit node's static IP from P7-T065, or the runtime host's own static IP when P7-T071 chose a static-IP Sydney VM, [18 §8](../../../docs/18-platform-and-deployment.md#8-tailscale-and-the-hardware-key-per-mode)) and reports `ok` on the target before the suite runs.

## ToDo

- [ ] Apply the runtime host playbook in `live` profile; checklist PASS
- [ ] Database migration path for the chosen `db.target`, with WORM chain verification
- [ ] Web deploy for the chosen `web.host`
- [ ] Run the full verification suite on the target; attach results
- [ ] Update 18 and 02 with what was actually deployed

## Verification

### Tests
- Host checklist (`infra/host/checklist.sh --profile live`) all PASS.
- WORM: hash chains verify end to end after migration; seal re-anchored.
- Golden suites green on the target.

### Scenarios
- Given `deploy.mode: workstation` (default), when the shift runs, then only the hardening and re-verification steps apply and nothing moves.
- Given `db.target: supabase_cloud`, when migration completes, then row counts and chain heads match the source.

### Stress / failure injection
- Pull the network on the runtime host with a paper position open: venue timers and resting stops behave as in the dead-man drill.

## Acceptance criteria

- [ ] Target hardened (live profile) and the full suite green on it
- [ ] Data migrated with WORM chains intact (if moved)

## Exceptions & edge cases

- If verification fails on the target, stay on the workstation (paper continues) and file the failures as bugs; no live funding until green.

## Cardinal rules (do NOT)

- No live money before this passes. Never edit WORM rows during migration; copy and verify.
- No secrets in the repo or logs.

## Doc sync on completion

- docs/18-platform-and-deployment.md, docs/02-v1-architecture.md, docs/07-security-notes.md, docs/roadmap/phase-7-prove-and-go-live.md: update to match what was built.

## Branch & PR

- Branch: `p7/P7-T073-shift-to-the-go-live-runtime-host-harden-migrate`
- PR title: `P7-T073: Shift to the go-live runtime host: harden, migrate, deploy, re-verify`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P7-T073` run

## Progress log

- 2026-11-19 09:16 · cloud:vm:be04b6ae61f8 · created
- 2026-11-19 00:00 · aligner · re-platformed per docs/18 (requirements R7.18, R7.04 / ToDo T7.44; added dep P7-T066 (egress; cancelled counts as done when the runtime host is a static-IP VM); egress check points at the exit node or the runtime host's static IP)
