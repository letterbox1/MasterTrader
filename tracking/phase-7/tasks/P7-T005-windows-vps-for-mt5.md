---
id: P7-T005
kind: task
title: Provision the Windows VPS near the FP Markets MT5 server
phase: 7
type: USER
status: backlog
priority: medium
size: S
severity: ""
owner: user
claimed_by: ""
depends_on: [P7-T004]
requirements: [R7.10]
roadmap_todos: [T7.08]
modules: [M12]
dashboards: [D16]
branch: p7/P7-T005-windows-vps-for-mt5
pr: ""
doc_sync: [docs/07-security-notes.md, docs/roadmap/phase-7-prove-and-go-live.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P7-T005 · Provision the Windows VPS near the FP Markets MT5 server

## Goal / expected outcome

A Windows VPS in the same data centre region as your FP Markets MT5 server (LD4 or NY4) exists, is reachable only over Tailscale, and has a static egress IP you can allow-list — ready for the MT5 bridge deployment (P7-T035).

## Context & references

- Roadmap: [R7.10 · ToDo T7.08](../../../docs/roadmap/phase-7-prove-and-go-live.md)
- Spec: [14 §8](../../../docs/14-strategy-evidence-and-validation.md#8-mastertradingbot-integration) (MT5 Python API on a Windows VPS near FP's MT5 servers) · [07 §3](../../../docs/07-security-notes.md#3-broker--exchange-keys) (IP allow-list, static egress) · [07 §5](../../../docs/07-security-notes.md#5-network--host)
- Related: P7-T004 (route choice; skip this item and cancel it if route = `ctrader`), P7-T034, P7-T035, gap P7-B010 (VPS not in the security model)

## Requirements

- Region matches the MT5 server named in your client area; Windows Server 2022 (or the MT5-supported version), 2 vCPU / 4 GB RAM is enough.
- Lowest-cost tier you are comfortable paying for (this is infrastructure, not data; note the monthly cost on the task).
- Static public IP; RDP **not** exposed publicly — Tailscale only, with MFA on the identity provider.
- Credentials (VPS admin password, Tailscale auth key) go into the sops secrets file, never chat or git.

## ToDo

- [ ] Pick a VPS provider with a location next to the MT5 server; create the instance.
- [ ] Install Tailscale, join your tailnet, disable public RDP in the provider firewall (inbound deny-all).
- [ ] Record the static egress IP on the task (it is not secret) and store the admin credential in sops (`secrets/live.enc.yaml` → `mt5_vps.*`).
- [ ] Install the MT5 terminal from FP Markets only (no third-party builds); log in with your **demo** account first.
- [ ] Tell the planner the VPS is ready so P7-T035 can deploy the bridge.

## Verification

### Tests
- n/a (user action); P7-T035 runs reachability and port-scan checks.

### Scenarios
- Given the VPS is up, when you `nmap` its public IP from outside, then no RDP/SSH/bridge port answers.
- Given Tailscale is up, when the host pings the VPS's tailnet name, then it responds.

### Stress / failure injection
- n/a: provisioning.

## Acceptance criteria

- [ ] VPS reachable over Tailscale only; public inbound closed.
- [ ] Static egress IP recorded; credentials only in sops.
- [ ] MT5 terminal logged into the FP Markets demo account.

## Exceptions & edge cases

- Provider forces public RDP: use its firewall to restrict to nothing and rely on the Tailscale route.
- Windows Update reboots: schedule outside trading sessions (P7-T035 sets this).

## Cardinal rules (do NOT)

- Do NOT expose RDP or any bridge port to the internet.
- Do NOT install MT5 from unofficial sources or add third-party EAs.
- Do NOT commit secrets or paste them into chats, issues, PRs or logs; secrets live only in the sops/age file (07 §2).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.

## Doc sync on completion

- `docs/07-security-notes.md` §5: add the VPS as a second host (Tailscale-only, static egress) — see P7-B010.
- `docs/roadmap/phase-7-prove-and-go-live.md`: tick T7.08 when this item is done.

## Branch & PR

- Branch: `p7/P7-T005-windows-vps-for-mt5`
- PR title: `P7-T005: Provision the Windows VPS near the FP Markets MT5 server`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P7-T005` run · evidence (redacted, no secrets) linked in the progress log

## Progress log

- 2026-10-21 00:00 · planner · created
