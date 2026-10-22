---
id: P7-T065
kind: task
title: Provision the Sydney egress exit-node VM with a static IP
phase: 7
type: USER
status: backlog
priority: critical
size: S
severity: ""
owner: user
claimed_by: ""
depends_on: []
requirements: [R7.14]
roadmap_todos: [T7.11]
modules: [M17]
dashboards: [D16]
tools: []
mcp: []
env: []
services: [cloud VM provider (Sydney region, static IP), tailscale]
branch: p7/P7-T065-provision-the-sydney-egress-exit-node-vm-with-a-
pr: ""
doc_sync: [docs/07-security-notes.md, docs/16-configuration-and-safety-model.md, docs/roadmap/phase-7-prove-and-go-live.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-22
updated: 2026-10-22
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
review_result: ""
---

# P7-T065 · Provision the Sydney egress exit-node VM with a static IP

## Goal / expected outcome

A small cloud VM in a Sydney region with a **static public IP** exists, is joined to your tailnet and ready to act as the WireGuard/Tailscale exit node for all exchange traffic. Its IP is the only one you will allow-list on every live key (P7-T007), so a broadband → 4G failover never changes the IP the exchanges see.

## Context & references

- Roadmap: [R7.14 · ToDo T7.11](../../../docs/roadmap/phase-7-prove-and-go-live.md)
- Design: [16 §3.2](../../../docs/16-configuration-and-safety-model.md#32-network-egress-and-ip-locked-keys) (one fixed AU egress IP via an exit node; free-tier VM where available (U), else a few dollars a month; not location masking) · [07 §3](../../../docs/07-security-notes.md#3-broker--exchange-keys) (allow-list one fixed egress IP) · [07 §5](../../../docs/07-security-notes.md#5-network--host) · [12 §3](../../../docs/12-policy-and-compliance.md#3-exchange-conduct--self-trade-prevention) (no VPN/proxy to hide location; an AU exit node matching your KYC country is not that)
- Decision: [17 §A P7-B004](../../../docs/17-decisions-register.md#a-s2-items-all-resolved) (static AU egress via exit node)
- Related: P7-T066 (tunnel config on this VM), P7-T007 (keys allow-listed to this IP), P7-T047 (key audit checks the allow-list), P1-T071 (egress check)

## Requirements

- Region: Sydney (`ap-southeast-2` or the provider's Sydney equivalent), so the egress IP geolocates to Australia, matching your KYC country and residency (16 §3.2).
- Static (reserved) public IPv4; smallest instance that runs WireGuard/Tailscale (1 vCPU, ≤ 1 GB RAM is enough). Free tier where available (U, verify the provider's current always-free offer), otherwise a small paid VM; record the monthly cost on this task (infrastructure, not data).
- Hardening: SSH key-only (no password), inbound deny-all except the WireGuard/Tailscale port; automatic security updates; no other workloads; no secrets on the VM except its own tailnet node key.
- Credentials (provider login MFA, SSH key, Tailscale auth) go into the sops secrets file outside the repo (17 §D P0-B018), never chat or git.
- Unblocks P7-T066 (tunnel) and P7-T007 (keys allow-listed to this IP).

## ToDo

- [ ] Pick a provider with a Sydney region and a static IP; check whether an always-free instance is still offered (record the answer: this closes the (U) in 16 §3.2).
- [ ] Create the VM; reserve/attach a static public IPv4; enable MFA on the provider account.
- [ ] Set inbound firewall to deny-all except the tunnel port; disable SSH password auth; enable automatic security updates.
- [ ] Install Tailscale (or WireGuard), join your tailnet, and advertise it as an exit node (`tailscale up --advertise-exit-node`); approve it in the tailnet admin console.
- [ ] Record on this task: provider, region, static IP (not secret), monthly cost; store the SSH key and any auth secret in the sops file.
- [ ] Check the IP's country with a free GeoIP lookup (e.g. DB-IP Lite) shows `AU`.
- [ ] Tell the agent the VM is ready so P7-T066 can configure the tunnel and the egress check.

## Verification

### Tests
- n/a (user action); P7-T066 tests the tunnel and P1-T071's egress check confirms the IP and country every minute.

### Scenarios
- Given the VM is up, when you scan its public IP from outside, then only the tunnel port answers (no SSH from the internet if you restricted it to the tailnet).
- Given the exit node is advertised, when the host routes a test request through it, then `api.ipify.org` returns the static IP and the GeoIP country is `AU`.

### Stress / failure injection
- Reboot the VM: the static IP is unchanged and the node rejoins the tailnet automatically.

## Acceptance criteria

- [ ] VM in a Sydney region with a static public IP that geolocates to `AU`, recorded on this task.
- [ ] VM joined to the tailnet as an approved exit node; inbound closed except the tunnel port.
- [ ] Credentials only in the sops file; monthly cost recorded.

## Exceptions & edge cases

- Provider recycles IPs on stop/start: use a reserved/elastic IP; never rely on an ephemeral IP.
- No free tier available: a small paid VM is acceptable (16 §3.2); this is infrastructure, not a paid data source.
- Provider outage: the tunnel is down → fail-flat via venue timers + resting stops (16 §3.1–3.2); recovery is a rebuild from this task's steps.

## Cardinal rules (do NOT)

- Do NOT pick a region outside Australia, and do NOT use a commercial VPN or proxy service; the exit node exists to keep one AU IP, not to mask location (12 §3).
- Do NOT run any other service or store any exchange key on the VM.
- Do NOT commit secrets or paste them into chats, issues, PRs or logs; secrets live only in the sops/age file (07 §2).
- Do NOT use keys that are not trade-only, IP-locked and withdrawal-disabled; no live money before the P7 gates pass.

## Doc sync on completion

- `docs/07-security-notes.md` §3/§5: note the exit node provider/region (no IP needed in docs).
- `docs/16-configuration-and-safety-model.md` §3.2: clear the free-tier (U) with what you found.
- `docs/roadmap/phase-7-prove-and-go-live.md`: tick T7.11 when this item and P7-T007 are done.

## Branch & PR

- Branch: `p7/P7-T065-provision-the-sydney-egress-exit-node-vm-with-a-`
- PR title: `P7-T065: Provision the Sydney egress exit-node VM with a static IP`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P7-T065` run · evidence (redacted, no secrets) linked in the progress log

## Progress log

- 2026-10-22 02:12 · cloud:vm:be04b6ae61f8 · created
- 2026-10-22 00:00 · aligner · created for docs/16–17 (R7.14/T7.11: static AU egress exit node, 16 §3.2, 17 §A P7-B004)
