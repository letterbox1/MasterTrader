---
id: P2-T001
kind: task
title: Create trade-only, IP-locked testnet/practice keys per mode
phase: 2
type: USER
status: backlog
priority: critical
size: S
severity: ""
owner: user
claimed_by: ""
depends_on: []
requirements: [R2.N3]
roadmap_todos: [T2.03]
modules: [M12]
dashboards: []
branch: p2/P2-T001-testnet-trade-only-keys
pr: ""
doc_sync: [docs/07-security-notes.md, docs/roadmap/phase-2-strategies-risk-lab.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P2-T001 · Create trade-only, IP-locked testnet/practice keys per mode

## Goal / expected outcome

Trade-only, IP-allow-listed, no-withdrawal API keys exist on every testnet/practice venue Phase 2 trades on, one sub-account (or account) per mode (`paper`, `hitl`, `autonomous`), stored only in the sops/age secrets file. This is a roadmap entry criterion and unblocks the engine adapters (P2-T023–P2-T026).

## Context & references

- Roadmap: [R2.N3](../../../docs/roadmap/phase-2-strategies-risk-lab.md) · ToDo T2.03 · entry criterion §2
- Security: [07 §3 broker & exchange keys](../../../docs/07-security-notes.md#3-broker--exchange-keys) · [07 §2 secrets](../../../docs/07-security-notes.md#2-secrets) · [SPEC NN5](../../../SPEC.md#non-negotiable-requirements)
- Spec: [03 M12 key safety](../../../docs/03-build-spec.md#m12-execution--mt_engine)
- Cross-phase: practice/demo accounts from P0 (T0.09); read-only recon keys from P1 (T1.02) stay separate; sops file from P0 (T0.43).
- Unblocks: P2-T022–P2-T026 (engine + adapters), P2-T045 (key audit).

## Requirements

- Venues: Binance spot testnet + Binance futures testnet, Bybit testnet (paper only, per registry), Alpaca paper, OANDA v20 practice, IG demo, IBKR paper (optional).
- Per key: **trade + read only**, withdrawals/transfers disabled, IP allow-list = the host's static egress IP (or Tailscale exit node IP).
- One sub-account (or separate practice account where sub-accounts don't exist) per mode: `paper`, `hitl`, `autonomous`.
- Key metadata (venue, account, mode, scopes, created date, IP list) goes into the secrets file alongside the key; key age > 90 days alerts (07 §2).
- Read-only recon keys (P1) are **not** reused for trading.

## ToDo

- [ ] For each venue above: create the sub-accounts (or note why the venue has none) named `mt-paper`, `mt-hitl`, `mt-auto`
- [ ] Create an API key per sub-account with only trade + read permissions; screenshot (locally, not in git) the permission page showing withdrawals OFF
- [ ] Set the IP allow-list to the host egress IP (run `curl -s https://ifconfig.me` on the host to read it)
- [ ] Add each key to the sops file: `sops secrets/secrets.enc.yaml` → under `venues.<venue>.<mode>` add `api_key`, `api_secret`, `created`, `scopes`, `ip_allow`
- [ ] Re-encrypt and confirm `git diff` shows only ciphertext changes; run `gitleaks detect` locally
- [ ] Tell the agent (in the task progress log, no secrets) which venues/modes are ready
- [ ] Record completion in the progress log (no secrets) and run `./kanban done P2-T001`

## Verification

### Tests
- Agent runs the key-audit script from P2-T045 against each key (permission introspection where the venue API exposes it).

### Scenarios
- Given a key from the secrets file, when a withdrawal endpoint is called on testnet, then the venue rejects it (permission denied).
- Given a request from a non-allow-listed IP, when the key is used, then the venue rejects it.

### Stress / failure injection
- n/a: account set-up action; the failure checks live in P2-T045.

## Acceptance criteria

- [ ] Every venue/mode pair above has a key or a written reason why not (e.g. IG demo has no sub-accounts → separate demo logins)
- [ ] All keys are in the sops file only; gitleaks clean
- [ ] Withdrawals disabled and IP lock confirmed per key (venue UI check)

## Exceptions & edge cases

- Venue lacks sub-accounts (Alpaca paper, OANDA practice): use separate practice accounts per mode or record the shared-account exception (then STP cancel-both applies, P2-T022).
- Venue lacks IP allow-listing on testnet: record it; the live key in P7 must have it.
- Bybit/OKX derivatives are blocked for AU retail live; testnet use is paper-only research (see P2-B008).

## Cardinal rules (do NOT)

- Do NOT enable withdrawal, transfer or universal-transfer permissions on any key.
- Do NOT paste keys into chat, issues, the task file or shell history (use `sops` editor).
- Do NOT commit secrets or paste them into chats/issues/logs; secrets live in the sops/age file (07 §2).
- Keys are trade-only, IP-locked, withdrawals disabled. No live money before the P7 gates; this phase is paper/testnet/practice only.

## Doc sync on completion

- `docs/07-security-notes.md` §3: note the per-mode sub-account names actually used.
- `docs/roadmap/phase-2-strategies-risk-lab.md`: tick T2.03 when all tasks mapped to it are done.

## Branch & PR

- Branch: `p2/P2-T001-testnet-trade-only-keys` (only if a repo change results, e.g. non-secret config or manifests; secrets never go in git)
- PR title: `P2-T001: Create trade-only, IP-locked testnet/practice keys per mode`
- PR checklist: no secrets in diff (gitleaks clean) · task file ticked · `./kanban done P2-T001` run

## Progress log

- 2026-10-21 00:00 · planner · created
