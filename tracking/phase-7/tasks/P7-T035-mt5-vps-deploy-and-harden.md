---
id: P7-T035
kind: task
title: Deploy and harden the MT5 bridge on the Windows VPS
phase: 7
type: OPS
status: backlog
priority: medium
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P7-T005, P7-T034]
requirements: [R7.10]
roadmap_todos: [T7.43, T7.24]
modules: [M12, M17]
dashboards: [D16]
tools: [git, tailscale, nmap, uv]
mcp: []
env: []
services: [Windows VPS (P7-T005), tailscale, loki, FP Markets MT5 demo]
branch: p7/P7-T035-mt5-vps-deploy-and-harden
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

# P7-T035 · Deploy and harden the MT5 bridge on the Windows VPS

## Goal / expected outcome

The Windows VPS is hardened to the 07 §5.1 baseline (Tailscale-only, inbound deny-all, only the MT5 trade-only login and no other secrets) and the MT5 bridge runs on it as a monitored Windows service, with logs shipped to Loki, health in D16, controlled update windows, a demo-account round-trip and a documented rebuild procedure.

## Context & references

- Roadmap: [R7.10 · ToDo T7.43, T7.24](../../../docs/roadmap/phase-7-prove-and-go-live.md)
- Spec: [07 §5.1](../../../docs/07-security-notes.md#51-optional-windows-vps-mt5-bridge) (VPS baseline) · [07 §5](../../../docs/07-security-notes.md#5-network--host) · [07 §2](../../../docs/07-security-notes.md#2-secrets) · [14 §8](../../../docs/14-strategy-evidence-and-validation.md#8-mastertradingbot-integration)
- Related: P7-T005 (VPS), P7-T034 (bridge), P7-T043 (runbook 'MT5 VPS down'), decision [17 §D P7-B010](../../../docs/17-decisions-register.md#d-other-decisions)

## Requirements

- Windows firewall: inbound deny-all except Tailscale interface → bridge port; no RDP or other port open to the internet; Defender on; automatic security updates; auto-login disabled; local admin password in sops (not stored on the VPS).
- Secrets on the VPS: **only** the MT5 trade-only login (and the bridge's own token); nothing else from the sops file (07 §5.1). Where FP Markets supports IP allow-listing, only the VPS's static IP is allow-listed.
- Bridge token/mTLS cert from sops, delivered once via Tailscale SSH/SCP; stored with Windows DPAPI.
- Logs → Vector agent (pinned) → Loki on the host; heartbeat visible in D16 Services.
- Windows Update: active hours set to cover trading sessions; reboot window weekends only.
- Rebuild procedure documented and timed (target < 60 min).

## ToDo

- [ ] Install bridge service, Vector agent, Tailscale ACL (only `engine` host may reach bridge port).
- [ ] Firewall and update policy.
- [ ] D16 service entry for `mt5-bridge`.
- [ ] Port-scan and auth tests from outside and inside the tailnet.
- [ ] Secret inventory on the VPS: only the MT5 trade-only login and the bridge token present (scripted check).
- [ ] Run the P7-T034 demo-account integration script (place/modify/cancel round-trip; deals match the terminal; 1,000 round-trips without leaks).
- [ ] Write the rebuild procedure (feeds P7-T043).

## Verification

### Tests
- External `nmap` shows no open ports; tailnet request without token → 401.
- Reboot VPS → service back within 2 min; D16 shows the gap.

### Scenarios
- Given Windows Update reboots on Saturday, then the bridge restarts and positions reconcile before Monday open.

### Stress / failure injection
- Kill the bridge process 5 times: auto-restart each time; engine marks account unconfirmed then confirmed after recon.

## Acceptance criteria

- [ ] Bridge reachable only via Tailscale ACL from the host.
- [ ] Only the MT5 trade-only login and the bridge token on the VPS; demo round-trip passes.
- [ ] Logs/heartbeat in Loki/D16.
- [ ] Rebuild procedure written and timed.

## Exceptions & edge cases

- Tailscale down on VPS: engine marks account unconfirmed; resting broker-side stops protect positions.

## Cardinal rules (do NOT)

- Do NOT enable public RDP even temporarily.
- Do NOT store the bridge token in plain files.
- Do NOT commit secrets or paste them into chats, issues, PRs or logs; secrets live only in the sops/age file (07 §2).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.

## Doc sync on completion

- `docs/07-security-notes.md` §5.1: VPS hardening as built.
- `docs/02-v1-architecture.md` §3: optional Windows VPS node.
- `docs/roadmap/phase-7-prove-and-go-live.md`: tick T7.08, T7.24 when this item is done.

## Branch & PR

- Branch: `p7/P7-T035-mt5-vps-deploy-and-harden`
- PR title: `P7-T035: Deploy and harden the MT5 bridge on the Windows VPS`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P7-T035` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (T7.43: VPS hardened to 07 §5.1 / 17 §D P7-B010 (Tailscale-only, only the MT5 trade-only login); demo round-trip moved here from P7-T034)
