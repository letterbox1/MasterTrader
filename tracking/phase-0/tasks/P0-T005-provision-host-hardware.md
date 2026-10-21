---
id: P0-T005
kind: task
title: Provision the host hardware and decide on the GPU
phase: 0
type: USER
status: ready
priority: critical
size: M
severity: ""
owner: user
claimed_by: ""
depends_on: []
requirements: [R0.02]
roadmap_todos: [T0.01]
modules: [ops]
dashboards: []
branch: p0/P0-T005-provision-host-hardware
pr: ""
doc_sync: [docs/03-build-spec.md, docs/roadmap/phase-0-foundations.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P0-T005 · Provision the host hardware and decide on the GPU

## Goal / expected outcome

One Linux box that meets 03 §2 (8–16 cores, 32–64 GB RAM, 2–4 TB NVMe + an HDD for cold Parquet) runs Ubuntu Server LTS or Debian stable installed with **LUKS full-disk encryption** chosen at install time, and there is a written GPU decision (16–24 GB VRAM now, by P4, or never). This is the only P0 entry criterion; everything else can start on a laptop/VM.

## Context & references

- [Roadmap P0 T0.01](../../../docs/roadmap/phase-0-foundations.md#4-todo-sets)
- [Roadmap P0 §2 entry criteria](../../../docs/roadmap/phase-0-foundations.md#2-entry-criteria)
- [03 §2 target environment](../../../docs/03-build-spec.md#2-target-environment)
- [02 §3.2 containers](../../../docs/02-v1-architecture.md#32-containers) (hardware line)
- [07 §5 network & host](../../../docs/07-security-notes.md#5-network--host)
- [Roadmap P0 §7 risks](../../../docs/roadmap/phase-0-foundations.md#7-risks--open-questions)
- Unblocks: P0-T019 host hardening and every OPS item that needs the real box

## Requirements

- CPU 8–16 cores; RAM 32–64 GB (ECC preferred); NVMe 2–4 TB (Postgres, hot Parquet 90 d); HDD ≥ 4 TB (cold Parquet, local staging); wired Ethernet.
- GPU decision: 16–24 GB VRAM recommended (tier B ~150–300 ms/decision, vLLM, Hindsight). Without one, tier B is seconds-scale and local models run on CPU. **Decide by P4 at the latest.**
- OS: Ubuntu Server 24.04 LTS (or Debian 12) minimal; LUKS2 on root and data volumes **at install**; separate volume for Docker data on NVMe.
- BIOS: Secure Boot on, restore-on-AC-loss on (pairs with the UPS), virtualisation on.
- Outputs: hardware spec + GPU decision in this task's progress log; LUKS passphrase in your password manager (never in git/chat).

## ToDo

- [ ] Choose and order/assemble the box (or re-purpose one); log the spec (CPU, RAM, disks, GPU or 'no GPU').
- [ ] Write the GPU decision: buy now / buy by P4 / CPU only, with the reason.
- [ ] Install the OS with LUKS2 on all internal volumes; create a non-root admin user.
- [ ] Set BIOS: Secure Boot, restore-on-AC-loss, VT-x/AMD-V.
- [ ] Connect wired Ethernet; hand over to P0-T019 (log 'ready for hardening').

## Verification

### Tests
- `lsblk -f` shows `crypto_LUKS` under every internal data volume.
- `nproc`, `free -g`, `lsblk` match the logged spec.

### Scenarios
- Given the hardware is delayed, when P0 starts, then the stack is built on a laptop/VM and moved later (roadmap risk table).

### Stress / failure injection
- n/a: hardware provisioning.

## Acceptance criteria

- [ ] Box meets 03 §2 minimums
- [ ] LUKS2 on every internal volume (verified with `lsblk -f`)
- [ ] GPU decision logged with a date
- [ ] Admin user created; ready for P0-T019

## Exceptions & edge cases

- Lead time: start on a laptop/VM; migrate with the backup/restore runbook (P0-T060) later.
- Unattended reboot with LUKS: a TPM2-bound unlock (systemd-cryptenroll) for the root volume is optional; otherwise the box needs a passphrase after each power loss (log the choice).

## Cardinal rules (do NOT)

- Do NOT install without disk encryption 'to save time'.
- Do NOT expose SSH to the LAN/internet; access will be Tailscale only.
- Do NOT commit secrets or paste them into chats, issues, PRs or logs; secrets live only in the sops/age file ([07 §2](../../../docs/07-security-notes.md#2-secrets)).

## Doc sync on completion

- `docs/03-build-spec.md` §2: note the actual hardware and GPU decision if it differs from the ranges.
- `docs/roadmap/phase-0-foundations.md`: tick T0.01 when every item mapped to it is done.

## Branch & PR

- Branch: `p0/P0-T005-provision-host-hardware`
- PR title: `P0-T005: Provision the host hardware and decide on the GPU`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P0-T005` run

## Progress log

- 2026-10-21 00:00 · planner · created
