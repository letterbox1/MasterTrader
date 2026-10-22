---
id: P0-T003
kind: task
title: Create the Tailscale tailnet with MFA and assign a hardware key for age
phase: 0
type: USER
status: ready
priority: high
size: S
severity: ""
owner: user
claimed_by: ""
depends_on: []
requirements: [R0.N1, R0.N2]
roadmap_todos: [T0.03]
modules: [ops]
dashboards: []
tools: [age, age-plugin-yubikey, tailscale]
mcp: []
env: []
services: [tailscale, yubikey]
branch: p0/P0-T003-tailscale-mfa-and-age-hardware-key
pr: ""
doc_sync: [docs/roadmap/phase-0-foundations.md]
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

# P0-T003 · Create the Tailscale tailnet with MFA and assign a hardware key for age

## Goal / expected outcome

A Tailscale tailnet whose identity provider has MFA, with your laptop/phone joined, and a YubiKey (or OS keychain) holding the age identities: one **host** identity that decrypts the runtime secrets file, and one **offline** identity used only for the `worm_owner` credential and secrets-file recovery.

## Context & references

- [Roadmap P0 T0.03](../../../docs/roadmap/phase-0-foundations.md#4-todo-sets)
- [07 §2 secrets](../../../docs/07-security-notes.md#2-secrets)
- [07 §5 network & host](../../../docs/07-security-notes.md#5-network--host)
- [15 §2.2 layers](../../../docs/15-bots-hitl-and-worm-audit.md#22-layers) (offline `worm_owner`)
- Related: P0-T019 host hardening, P0-T022 secrets, P0-T013 worm_owner ceremony
- Unblocks: P0-T019 host hardening, P0-T013 worm_owner ceremony and the production secrets file on the host. P0-T022 is built and tested with a throwaway age key, so it doesn't wait for this task (build first, keys last)

## Requirements

- Tailscale Personal (free) plan; sign in with an IdP that has **MFA on** (hardware key or TOTP).
- Tailnet settings: device approval on, key expiry on for user devices, MagicDNS + HTTPS certificates enabled (Caddy uses `*.ts.net` certs).
- Two YubiKeys (primary + spare) or one YubiKey + OS keychain backup. age identities via `age-plugin-yubikey`: slot 1 = `host` (PIN cached once at boot, touch policy *never* so restarts decrypt unattended), slot 2 = `offline` (touch *always*, never left plugged in).
- The age identity must **not** live on the backup disk or in any backup set (07 §2).
- Outputs: tailnet name and the two age **recipients** (public `age1yubikey…` strings, not secret) in `infra/secrets/recipients.txt`, from which P0-T022 generates `.sops.yaml`; PIN/PUK in the password manager.

## ToDo

- [ ] Create the Tailscale account with your chosen IdP; turn on MFA at the IdP; log 'MFA on' here.
- [ ] In the Tailscale admin console enable MagicDNS, HTTPS certificates and device approval.
- [ ] Join your laptop and phone; leave the host for P0-T019.
- [ ] Buy two YubiKey 5 series (or decide on one + OS keychain) and log the choice.
- [ ] Install `age` and `age-plugin-yubikey`; generate slot 1 (`--touch-policy never --pin-policy once --name mt-host`) and slot 2 (`--touch-policy always --name mt-offline`); repeat on the spare key.
- [ ] Put the two public recipients in `infra/secrets/recipients.txt` (or hand them to the agent for a PR) and run `sops updatekeys` on the secrets file; store the YubiKey PINs/PUKs in your password manager.
- [ ] Label the spare key and store it in a separate physical location from the backup disk.

## Verification

### Tests
- `age-plugin-yubikey --list` shows both slots on both keys.
- Round trip: encrypt `ok` to each recipient and decrypt with its identity stub.

### Scenarios
- Given the host reboots, when Compose starts, then the host identity decrypts without a touch (PIN cached once at boot).
- Given the primary key is lost, when you use the spare, then both the runtime file and the offline file still decrypt.

### Stress / failure injection
- n/a: account and hardware setup.

## Acceptance criteria

- [ ] Tailnet exists, IdP MFA on, MagicDNS + HTTPS certs on
- [ ] Two age identities (host, offline) on two keys, round trip passes
- [ ] Recipients in `infra/secrets/recipients.txt`; PIN/PUK in password manager
- [ ] No identity file on any backup disk

## Exceptions & edge cases

- No YubiKey yet: use the OS keychain for the host identity temporarily and log it; the offline identity must still be on removable media kept offline.
- Tailscale Personal is for private use only (12 §4); a commercial pivot means a paid plan.

## Cardinal rules (do NOT)

- Do NOT store an age identity or YubiKey PIN on the backup disk or in the repo.
- Do NOT disable MFA on the IdP 'temporarily'.
- Do NOT commit secrets or paste them into chats, issues, PRs or logs; secrets live only in the sops/age file ([07 §2](../../../docs/07-security-notes.md#2-secrets)).

## Doc sync on completion

- `docs/07-security-notes.md` §2: record that the host and offline age identities are on hardware keys (no values).
- `docs/roadmap/phase-0-foundations.md`: tick T0.03 when every item mapped to it is done.

## Branch & PR

- Branch: `p0/P0-T003-tailscale-mfa-and-age-hardware-key`
- PR title: `P0-T003: Create the Tailscale tailnet with MFA and assign a hardware key for age`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P0-T003` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (keys-last: P0-T022 builds with a test age key; recipients go to infra/secrets/recipients.txt; run fields added)
