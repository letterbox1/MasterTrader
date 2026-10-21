---
id: P0-T019
kind: task
title: Harden the host (LUKS, firewall, SSH, updates, Tailscale, chrony)
phase: 0
type: OPS
status: backlog
priority: high
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P0-T005, P0-T003]
requirements: [R0.N2]
roadmap_todos: [T0.40]
modules: [ops]
dashboards: []
branch: p0/P0-T019-host-hardening
pr: ""
doc_sync: [docs/07-security-notes.md, docs/roadmap/phase-0-foundations.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P0-T019 · Harden the host (LUKS, firewall, SSH, updates, Tailscale, chrony)

## Goal / expected outcome

The host meets 07 §5 and is reproducible from a script: LUKS verified, deny-inbound firewall, SSH keys-only reachable only over Tailscale, unattended security upgrades, chrony synced, Docker from the official repo with a hardened daemon config, and a host checklist that passes.

## Context & references

- [Roadmap P0 R0.N2](../../../docs/roadmap/phase-0-foundations.md#3-requirements)
- [Roadmap P0 T0.40](../../../docs/roadmap/phase-0-foundations.md#4-todo-sets)
- [07 §5 network & host](../../../docs/07-security-notes.md#5-network--host)
- [03 §2 target environment](../../../docs/03-build-spec.md#2-target-environment)
- Related: this checklist is re-run in P0-T056; P0-T012 (NUT)
- Depends on: P0-T005, P0-T003

## Requirements

- Idempotent provisioning in `infra/host/` (Ansible playbook or shell + `make host`).
- Firewall: default deny inbound on all interfaces; allow inbound only on `tailscale0` for 22 (SSH) and 443 (Caddy). `DOCKER-USER` chain drops non-Tailscale ingress; no compose `ports:` on `0.0.0.0` (enforced by P0-T020's lint).
- SSH: `PasswordAuthentication no`, `PermitRootLogin no`, `KbdInteractiveAuthentication no`, `AllowUsers <admin>`, listen on the Tailscale IP only; ed25519 keys (optionally `sk-ssh-ed25519` on the YubiKey).
- Tailscale: host joined with tag `tag:mt-host`; ACL lets only your devices reach 22/443; Funnel off.
- Updates: `unattended-upgrades` security-only, automatic reboot window 04:00 Australia/Sydney (log the choice).
- chrony: ≥ 3 NTP sources (e.g. `au.pool.ntp.org`), `makestep 1.0 3`; offset exported to Prometheus (node_exporter textfile) for D16 and M16 skew checks.
- Host login events shipped via journald → Vector → Loki (alert in P0-T045).
- Docker: official repo, pinned version; `live-restore: true`; `log-opts` `max-size 50m`, `max-file 5`; `no-new-privileges: true`; userns-remap evaluated (log decision).
- NUT client if the UPS (P0-T012) is connected: clean shutdown at ≤ 20 % battery.

## ToDo

- [ ] Write the playbook/scripts under `infra/host/`.
- [ ] Apply on the host; verify with `infra/host/checklist.sh` (PASS/FAIL per control).
- [ ] Configure the Docker daemon and `DOCKER-USER` rules.
- [ ] Configure chrony and the offset metric.
- [ ] Attach checklist output to the PR (no IPs or secrets).

## Verification

### Tests
- `checklist.sh` asserts: LUKS on all data volumes, firewall default-deny, effective sshd config (`sshd -T`), unattended-upgrades enabled, chrony offset < 50 ms, Docker daemon settings, no listening sockets on non-Tailscale, non-loopback addresses (`ss -tlnp`).

### Scenarios
- Given an attacker on the LAN, when they scan the host's LAN IP, then no TCP port answers.
- Given a container is added with `ports: ['8080:8080']`, then the DOCKER-USER rule still drops LAN ingress and the compose lint rejects the file.

### Stress / failure injection
- Reboot test: Tailscale, Docker and chrony come back and the checklist passes without manual steps except the LUKS unlock (if not TPM-bound).

## Acceptance criteria

- [ ] `checklist.sh` all PASS on the host (output attached)
- [ ] LAN nmap from another machine shows 0 open TCP ports
- [ ] chrony offset < 50 ms and exported
- [ ] Re-running the playbook changes nothing
- [ ] CI green (ruff, mypy, pytest, gitleaks, `pit` check)

## Exceptions & edge cases

- Laptop/VM stage: same playbook; LUKS may be WARN on a VM and must be PASS on the real host before exit.
- Tailscale outage: no remote access but the box keeps running; local console access remains (documented in P0-T060).

## Cardinal rules (do NOT)

- Do NOT open any port on the LAN/WAN interface or use router port-forwarding.
- Do NOT disable the firewall to debug.
- Do NOT commit secrets or paste them into chats, issues, PRs or logs; secrets live only in the sops/age file ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Pin every image by digest (no `:latest` or floating tags); no telemetry or referral IDs in vendored code.

## Doc sync on completion

- `docs/07-security-notes.md` §5: link `infra/host/checklist.sh` as the host checklist.
- `docs/roadmap/phase-0-foundations.md`: tick T0.40 when every item mapped to it is done.

## Branch & PR

- Branch: `p0/P0-T019-host-hardening`
- PR title: `P0-T019: Harden the host (LUKS, firewall, SSH, updates, Tailscale, chrony)`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P0-T019` run

## Progress log

- 2026-10-21 00:00 · planner · created
