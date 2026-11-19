---
id: P0-T003
kind: task
title: Optional now: create the Tailscale tailnet with MFA (phone access; required at go-live)
phase: 0
type: USER
status: ready
priority: medium
size: S
severity: ""
owner: user
claimed_by: ""
depends_on: []
requirements: [R0.N2]
roadmap_todos: [T0.03]
modules: [ops]
dashboards: []
tools: [tailscale]
mcp: []
env: []
services: [tailscale]
branch: p0/P0-T003-tailscale-mfa-and-age-hardware-key
pr: ""
doc_sync: [docs/roadmap/phase-0-foundations.md]
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

# P0-T003 · Optional now: create the Tailscale tailnet with MFA (phone access; required at go-live)

## Goal / expected outcome

If you want to use MasterTrader from your phone or laptop away from the workstation, a Tailscale tailnet exists whose identity provider has MFA, with your devices joined. This is **optional before Phase 7**: on the workstation everything is on localhost and nothing in the build waits on it ([18 §8](../../../docs/18-platform-and-deployment.md#8-tailscale-and-the-hardware-key-per-mode)). It becomes required at go-live for the fixed-IP egress exit node and, in hybrid mode, for the private API (`api.exposure: tailnet`, [16 §2.15](../../../docs/16-configuration-and-safety-model.md#215-platform-deployment-and-regions)). The hardware key (YubiKey) for the age identities moved to P7-T072.

## Context & references

- [Roadmap P0 T0.03](../../../docs/roadmap/phase-0-foundations.md#4-todo-sets) · [R0.N2](../../../docs/roadmap/phase-0-foundations.md#3-requirements)
- [18 §8 Tailscale and the hardware key, per mode](../../../docs/18-platform-and-deployment.md#8-tailscale-and-the-hardware-key-per-mode) · [18 §5 deployment modes](../../../docs/18-platform-and-deployment.md#5-deployment-modes)
- [07 §5 network & host](../../../docs/07-security-notes.md#5-network--host)
- [17 §G](../../../docs/17-decisions-register.md#g-platform-rust-and-python-supabase-vercel-workstation-first-2026-11-19)
- Related: P0-T019 (applies the Tailscale firewall rules only if `tailscale0` exists), P7-T072 (YubiKey for the age identities), P7-T073 (live hardening and egress exit node)
- Unblocks: nothing in Phases 0–6. Needed before go-live (P7)

## Requirements

- Tailscale Personal (free) plan; sign in with an IdP that has **MFA on** (hardware key or TOTP).
- Tailnet settings: device approval on, key expiry on for user devices, MagicDNS + HTTPS certificates enabled (Caddy can use `*.ts.net` certs when Tailscale is on).
- Join only the devices you use (phone, laptop) and, if you want phone access to the workstation, the workstation itself (P0-T019 then applies the Tailscale-only rules).
- Outputs: tailnet name and 'MFA on' logged here (no secrets).
- The age identities stay in the OS keychain until P7-T072 (`secrets.age_identity_store: keychain`, [16 §2.15](../../../docs/16-configuration-and-safety-model.md#215-platform-deployment-and-regions)); nothing about them is done here.

## ToDo

- [ ] Decide whether you want phone/laptop access before go-live; if not, log 'deferred to P7' and stop here.
- [ ] Create the Tailscale account with your chosen IdP; turn on MFA at the IdP; log 'MFA on' here.
- [ ] In the Tailscale admin console enable MagicDNS, HTTPS certificates and device approval.
- [ ] Join your phone/laptop (and the workstation if you want remote access); tell the agent so P0-T019 enables the Tailscale rules.

## Verification

### Tests
- `tailscale status` on a joined device lists your devices; the IdP shows MFA enforced.

### Scenarios
- Given you skip this task, when the stack runs on the workstation, then everything works on localhost and no build or test waits on Tailscale.
- Given the workstation is joined, when you open the app from your phone over Tailscale, then it loads and nothing is reachable from the LAN or internet (P0-T056).

### Stress / failure injection
- n/a: account setup.

## Acceptance criteria

- [ ] Either 'deferred to P7' logged, or: tailnet exists, IdP MFA on, MagicDNS + HTTPS certs on, devices joined

## Exceptions & edge cases

- Tailscale Personal is for private use only (12 §4); a commercial pivot means a paid plan.
- If you defer this, P7-T073 includes it before live money (egress exit node).

## Cardinal rules (do NOT)

- Do NOT disable MFA on the IdP 'temporarily'.
- Do NOT enable Tailscale Funnel or any public exposure.
- Do NOT commit secrets or paste them into chats, issues, PRs or logs; secrets live only in the sops/age file ([07 §2](../../../docs/07-security-notes.md#2-secrets)).

## Doc sync on completion

- `docs/07-security-notes.md` §5: note whether the tailnet is in use before P7 (no values).
- `docs/roadmap/phase-0-foundations.md`: tick T0.03 when every item mapped to it is done.

## Branch & PR

- Branch: `p0/P0-T003-tailscale-mfa-and-age-hardware-key`
- PR title: `P0-T003: Optional: create the Tailscale tailnet with MFA`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P0-T003` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (keys-last: P0-T022 builds with a test age key; recipients go to infra/secrets/recipients.txt; run fields added)
- 2026-11-19: Re-scoped (17 §G, 18 §8): Tailscale is needed only for phone/laptop access to the app, the private API in hybrid mode and the go-live egress exit node; nothing in the build waits on it. The hardware-key part moved to P7-T072 (OS keychain until then).
- 2026-11-19 00:00 · aligner · re-platformed per docs/18 (body rewritten to the optional Tailscale task of 18 §8; YubiKey/age steps removed (now P7-T072); R0.N1 link and yubikey/age tools dropped)
