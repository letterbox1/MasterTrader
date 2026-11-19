---
id: P0-T019
kind: task
title: Harden the workstation baseline (firewall, Docker, updates, chrony; live profile at the shift)
phase: 0
type: OPS
status: backlog
priority: high
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P0-T005]
requirements: [R0.N2]
roadmap_todos: [T0.40]
modules: [ops]
dashboards: []
tools: [ansible, nmap, chronyc, docker, just]
mcp: []
env: []
services: []
branch: p0/P0-T019-host-hardening
pr: ""
doc_sync: [docs/07-security-notes.md, docs/roadmap/phase-0-foundations.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-11-19
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
review_result: ""
---

# P0-T019 · Harden the workstation baseline (firewall, Docker, updates, chrony; live profile at the shift)

## Goal / expected outcome

The workstation meets the **`workstation` profile** of 07 §5 and is reproducible from a script: deny-inbound firewall, every service bound to localhost, Docker from the official repo with a hardened daemon config, automatic security updates, chrony synced, and a checklist that passes. Tailscale rules apply only if `tailscale0` exists (P0-T003 is optional before P7), and full-disk encryption is reported as a warning. The stricter **`live` profile** (LUKS required, SSH only over Tailscale, Tailscale ACLs, egress exit node) is the same playbook with a different profile, applied at the shift (P7-T073) ([18 §8–9](../../../docs/18-platform-and-deployment.md#8-tailscale-and-the-hardware-key-per-mode)).

## Context & references

- [Roadmap P0 R0.N2](../../../docs/roadmap/phase-0-foundations.md#3-requirements) · [T0.40](../../../docs/roadmap/phase-0-foundations.md#4-todo-sets)
- [07 §5 network & host](../../../docs/07-security-notes.md#5-network--host)
- [18 §8](../../../docs/18-platform-and-deployment.md#8-tailscale-and-the-hardware-key-per-mode) · [18 §9](../../../docs/18-platform-and-deployment.md#9-workstation-first-build-path)
- [03 §2 target environment](../../../docs/03-build-spec.md#2-target-environment)
- Related: this checklist is re-run in P0-T056; P0-T012 (NUT, if the UPS is connected); P7-T073 (live profile)
- Depends on: P0-T005 (workstation profile)

## Requirements

- Idempotent provisioning in `infra/host/` (Ansible playbook or shell) with `just host profile=workstation|live`; the `workstation` profile changes only what a personal desktop tolerates.
- Firewall (`workstation`): default deny inbound on all interfaces; nothing allowed inbound except, if `tailscale0` exists, 443 (Caddy) and 22 (only if SSH is enabled) on `tailscale0`. `DOCKER-USER` chain drops non-loopback, non-Tailscale ingress to containers; no compose `ports:` on `0.0.0.0` (enforced by P0-T020's lint).
- SSH: off by default on the workstation; if enabled: `PasswordAuthentication no`, `PermitRootLogin no`, `KbdInteractiveAuthentication no`, `AllowUsers <admin>`, listening on localhost/Tailscale only; ed25519 keys.
- Updates: unattended security updates (OS-appropriate), reboot window a setting (default 04:00 Australia/Sydney, log the choice).
- chrony (or the OS time service): ≥ 3 NTP sources (e.g. `au.pool.ntp.org`), offset exported to Prometheus (node_exporter textfile) for D16 and M16 skew checks.
- Login events shipped via journald → Vector → Loki (alert in P0-T045) where the OS has journald.
- Docker: official repo, pinned version; `live-restore: true`; `log-opts` `max-size 50m`, `max-file 5`; `no-new-privileges: true`; userns-remap evaluated (log decision).
- Disk encryption: `checklist.sh` reports LUKS/FileVault/BitLocker status as **WARN** in `workstation`, **FAIL** in `live`.
- NUT client if the UPS (P0-T012) is connected: clean shutdown at ≤ 20 % battery.
- `live` profile (written now, applied in P7-T073): LUKS required, SSH only on Tailscale, host tag `tag:mt-host` with ACLs, Funnel off.

## ToDo

- [ ] Write the playbook/scripts under `infra/host/` with the two profiles.
- [ ] Apply `workstation` on the workstation; verify with `infra/host/checklist.sh` (PASS/WARN/FAIL per control).
- [ ] Configure the Docker daemon and `DOCKER-USER` rules.
- [ ] Configure time sync and the offset metric.
- [ ] Attach checklist output to the PR (no IPs or secrets).

## Verification

### Tests
- `checklist.sh --profile workstation` asserts: firewall default-deny, no listening sockets on non-loopback, non-Tailscale addresses (`ss -tlnp`), Docker daemon settings, updates enabled, time offset < 50 ms, SSH off or hardened (`sshd -T`); disk encryption reported as WARN if absent.
- `checklist.sh --profile live` run in a VM fixture fails on missing LUKS (proves the live profile is stricter).

### Scenarios
- Given a device on the LAN, when it scans the workstation's LAN IP, then no TCP port answers.
- Given a container is added with `ports: ['8080:8080']`, then the DOCKER-USER rule still drops LAN ingress and the compose lint rejects the file.
- Given Tailscale is not installed, then the playbook skips the Tailscale rules and the checklist passes.

### Stress / failure injection
- Reboot test: Docker, the stack (`just up`) and time sync come back and the checklist passes without manual steps.

## Acceptance criteria

- [ ] `checklist.sh --profile workstation` all PASS (WARN allowed only for disk encryption) on the workstation (output attached)
- [ ] LAN nmap from another machine shows 0 open TCP ports
- [ ] Time offset < 50 ms and exported
- [ ] Re-running the playbook changes nothing; the `live` profile exists for P7-T073
- [ ] CI green (clippy, cargo test, ruff, mypy, pytest, `supabase test db`, gitleaks, `pit` check)

## Exceptions & edge cases

- macOS or Windows workstation: the playbook covers what the OS allows (pf / Windows Firewall, Docker Desktop settings); controls that don't apply are reported N/A, not PASS (log which).
- Tailscale outage (if used): no remote access, but the stack keeps running locally.

## Cardinal rules (do NOT)

- Do NOT open any port on the LAN/WAN interface or use router port-forwarding.
- Do NOT disable the firewall to debug.
- Do NOT require LUKS, Tailscale or a YubiKey before Phase 7.
- Do NOT commit secrets or paste them into chats, issues, PRs or logs; secrets live only in the sops/age file ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Pin every image by digest (no `:latest` or floating tags); no telemetry or referral IDs in vendored code.

## Doc sync on completion

- `docs/07-security-notes.md` §5: link `infra/host/checklist.sh` and name the two profiles.
- `docs/roadmap/phase-0-foundations.md`: tick T0.40 when every item mapped to it is done.

## Branch & PR

- Branch: `p0/P0-T019-host-hardening`
- PR title: `P0-T019: Harden the workstation baseline (firewall, Docker, updates, time sync; live profile for the shift)`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P0-T019` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (no decision changes (host task, needs the real box and tailnet); run fields added)
- 2026-11-19: Workstation-first (17 §G): two profiles. `workstation` (now): deny-inbound firewall, every service bound to localhost, hardened Docker daemon, chrony, updates; the Tailscale rules apply only if `tailscale0` exists, LUKS is reported as a warning. `live` (P7-T073): LUKS required, SSH only over Tailscale, Tailscale ACLs. No longer depends on P0-T003 (Tailscale) or a dedicated host.
- 2026-11-19 00:00 · aligner · re-platformed per docs/18 (body rewritten for the two profiles (`workstation` now, `live` at P7-T073): localhost binding, SSH off by default, Tailscale rules only if present, LUKS a warning; tailscale/ssh tools and the tailscale service dropped from the front matter)
