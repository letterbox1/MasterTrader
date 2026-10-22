---
id: P5-T013
kind: task
title: mt_signer core: intent API, caller auth, key loading, allow-lists, caps and ledger
phase: 5
type: BUILD
status: backlog
priority: critical
size: L
severity: ""
owner: agent
claimed_by: ""
depends_on: [P5-T010, P5-T012, P2-T031]
requirements: [R5.02, R5.N2]
roadmap_todos: [T5.20]
modules: [M22, M4]
dashboards: []
tools: [uv, docker]
mcp: []
env: []
services: [postgres, nats]
branch: p5/P5-T013-mt-signer-core-intent-api
pr: ""
doc_sync: [docs/13-wallets-treasury-and-onchain.md, docs/03-build-spec.md, docs/roadmap/phase-5-airdrops-wallets-curation.md]
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

# P5-T013 · mt_signer core: intent API, caller auth, key loading, allow-lists, caps and ledger

## Goal / expected outcome

`packages/mt_signer` runs as the only process holding hot/identity/burner keys. It accepts typed **intents** over a Unix socket or mTLS from the policy service only, checks custody tier, per-wallet allow-lists, per-tx and rolling-24h caps and the kill switch, hands building to chain plug-ins (P5-T014/T015), requires simulation (P5-T016) and records every signature or refusal in the WORM signer ledger.

## Context & references

- Roadmap: [R5.02](../../../docs/roadmap/phase-5-airdrops-wallets-curation.md) · ToDo T5.20 · [SPEC NN6](../../../SPEC.md#non-negotiable-requirements)
- Signer design: [13 §2](../../../docs/13-wallets-treasury-and-onchain.md#2-signer-service-the-only-process-that-sees-hot-keys) · [07 §4](../../../docs/07-security-notes.md#4-crypto-wallets-airdrops-on-chain-claims)
- Callers (decision P5-B003, [17 §B](../../../docs/17-decisions-register.md#b-cross-doc-conflicts-one-canonical-answer)): intents only from the **policy service**: `airdrop-exec` in P5 (claims, revokes, sweeps); treasury (P6) and DEX execution (P7) also go through the policy service, never straight to the signer
- Kill switch KV `kill` (P2-T031; R2.18); F6 ([02 §8](../../../docs/02-v1-architecture.md#8-end-to-end-flows))
- Ledger table from P5-T010; custody limits from P5-T012

## Requirements

- Intent types v1: `claim` (contract, selector, args, chain, wallet), `revoke_approval` (token, spender), `sweep` (asset, amount|all-above-float, destination id), `refill_burner`, `genuine_use` (pre-approved protocol action), `nonce_close` (Solana), `key_create` (C3-approved).
- Transport: Unix socket in a shared volume or mTLS on the `signer` network; client cert pinned to the policy-service identity (`airdrop-exec` in P5); anything else refused and alerted.
- Checks in order: `signing_enabled` (limits confirmed in P5-T065, else `limits_unconfirmed`) → kill switch (refuse all except `sweep` to vault and `revoke_approval`) → custody tier allows op → per-wallet allow-list (program/contract + selector) → caps (per-transaction default A$250 and rolling 24 h default A$1,000 per wallet, read from the limits store of P5-T012, never hard-coded; Decimal, AUD valuation per [16 §4.1](../../../docs/16-configuration-and-safety-model.md#41-valuing-crypto-for-the-journal)) → cost-gate verdict (`mt_onchain.costgate`) attached and `allow` → build (plug-in) → hard blocks (plug-in) → simulation pass → sign → ledger append → return signed tx (broadcast by caller or signer per config).
- Keys loaded at start from OpenBao (preferred) or sops tmpfs into memory; zeroised on shutdown; never logged (log redaction test).
- Every refusal has a machine-readable reason code and is ledgered.
- Latency budget: decision (excluding simulation/RPC) p99 < 50 ms; kill switch checked from KV on every intent (no cache > 100 ms).

## ToDo

- [ ] Create `packages/mt_signer` (service entry, intent schemas, policy pipeline, plug-in interface `ChainPlugin.build/decode/hard_block/simulate`).
- [ ] Implement transport (Unix socket + optional mTLS) with caller authentication and rate limiting.
- [ ] Implement key store adapters: OpenBao KV v2 and sops-tmpfs; in-memory keyring with zeroisation.
- [ ] Implement allow-list store (per wallet, versioned, tighten C1 / loosen C3) and cap accounting (rolling 24h window persisted so restarts don't reset it).
- [ ] Implement ledger writer to `audit.signer_ledger` (P5-T010) including refusals.
- [ ] Kill-switch check via NATS KV `kill`; publish `sys.heartbeat.signer`.
- [ ] Unit/integration tests; update 13 §2 and 03 M22 with the intent list.

## Verification

### Tests
- Unit: each pipeline stage refuses with the right reason code (table-driven).
- Unit: rolling-24h cap survives a restart (persisted usage).
- Unit: with `signing_enabled = false` every intent is refused `limits_unconfirmed` and ledgered.
- Unit: log-redaction test — run the full pipeline with a known test key; grep logs/NATS captures for any key bytes → none.
- Integration: an uncertified client on the socket is refused and an `alert.critical.signer_auth` is published.

### Scenarios
- Given kill = ON, when a `claim` intent arrives, then it is refused (`kill_switch`) and ledgered; when a `sweep` to the vault arrives, then it proceeds.
- Given a wallet whose 24h cap is 90% used, when a claim needing 20% arrives, then it is refused `cap_24h` and becomes a manual task upstream.
- Given an intent naming the vault wallet as signer, then it is refused `watch_only_tier`.

### Stress / failure injection
- Fire 1,000 intents/min from the authorised client with 10% malformed: no crash, all malformed refused, p99 decision < 50 ms.
- Kill OpenBao mid-run: signer keeps in-memory keys; restart without OpenBao → starts `frozen` and alerts (fail closed).

## Acceptance criteria

- [ ] Intent API with caller auth live
- [ ] All checks enforced in the stated order with reason codes
- [ ] Ledger row for every signature and refusal
- [ ] No key material in logs (test)
- [ ] Fails closed on missing config/keys
- [ ] Refuses everything until the limits are confirmed (`limits_unconfirmed`)

## Exceptions & edge cases

- Postgres (ledger) down: refuse to sign (no signature without a ledger row); alert.
- NATS down: kill state unknown → treat as ON (fail closed) except sweeps to vault.
- Clock jump: rolling window uses monotonic + DB time; a > 1 s skew alert from P1 freezes signing.

## Cardinal rules (do NOT)

- Do NOT accept raw or pre-built transactions, raw messages or typed-data payloads from any caller — intents only; the signer re-builds and re-decodes everything itself (13 §2).
- Do NOT log, print, serialise to NATS or persist private keys anywhere except OpenBao/sops; keys are never in `.env`.
- Do NOT add an "admin bypass" flag or debug endpoint that signs arbitrary payloads.
- Do NOT commit secrets or paste them into chats, issues or logs; secrets live only in the sops/age file or OpenBao (07 §2).
- Do NOT UPDATE or DELETE WORM rows (`curation.mandate`, `curation.exec_log`, the signer ledger, `journal.*`, `audit.*`); corrections are new rows with `supersedes_id` (15 §2).
- Do NOT give any LLM, agent or MCP path a route to keys, the signer socket or the `signer` network (R5.N1).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.

## Doc sync on completion

- `docs/13-wallets-treasury-and-onchain.md` §2: list intent types and refusal codes.
- `docs/03-build-spec.md` M22: add `mt_signer` package and intent interface.
- `docs/roadmap/phase-5-airdrops-wallets-curation.md`: tick T5.20 when this lands (with the other tasks sharing that ToDo).

## Branch & PR

- Branch: `p5/P5-T013-mt-signer-core-intent-api`
- PR title: `P5-T013: mt_signer core: intent API, caller auth, key loading, allow-lists, caps and ledger`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P5-T013` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (intents only from the policy service per P5-B003; caps from the 16 §2.7 limits store; signing disabled until confirmed; P2 kill dep)
