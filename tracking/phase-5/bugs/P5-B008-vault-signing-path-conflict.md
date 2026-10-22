---
id: P5-B008
kind: gap
title: Vault signing from the UI (13 §3 step 5) vs vault/warm watch-only (D18, R5.01)
phase: 5
type: DOC
status: done
priority: medium
size: XS
severity: S3
owner: agent
claimed_by: ""
depends_on: []
requirements: [R5.01]
roadmap_todos: []
modules: [M22]
dashboards: [D18]
tools: []
mcp: []
env: []
services: []
branch: p5/P5-B008-vault-signing-path-conflict
pr: ""
doc_sync: [docs/13-wallets-treasury-and-onchain.md, docs/ui/dashboards/D18-wallets-treasury.md]
doc_sync_status: done
found_in: "docs/13-wallets-treasury-and-onchain.md §3 step 5"
created: 2026-10-21
updated: 2026-10-22
started: ""
completed: 2026-10-22
blocked_reason: ""
checkpoint: ""
review_result: ""
---

# P5-B008 · Vault signing from the UI (13 §3 step 5) vs vault/warm watch-only (D18, R5.01)

## Goal / expected outcome

One rule for manual signing from the UI and its phase.

## Context & references

- 13 §3.5: "Manual signing happens from the local UI via EIP-6963 browser wallets, WalletConnect (phone) and QR (vault)"
- D18: "Vault and warm wallets are watch-only (no signing path from the UI)"; R5.01: watch-only in the system

## Requirements

- **Steps to reproduce:** Read 13 §3 step 5 and D18 Rules.
- **Expected:** Consistent statement.
- **Actual:** 13 implies a UI signing path for the vault; D18 forbids it.
- **Suggested fix:** State that P5 has no UI signing path; any future manual-signing UI (P6 warm-wallet approvals) builds unsigned payloads only and is a separate, explicitly scoped feature; vault remains offline QR outside the app.
- **Impact:** S3: risk of building a signing surface the security model forbids.

## ToDo

- [x] Resolution recorded: Decided (17 §B P5-B008): vault and warm are watch-only; the system never holds their keys and may only prepare unsigned transactions (QR/WalletConnect) for you to sign in your own wallet; P5 has no UI signing path
- [x] Docs carry it: 13 §1 (watch-only statement), 13 §3 step 5 (manual signing in your own wallet; P5 has no UI signing path), 07 §4 item 1, D18 rules, roadmap R5.01
- [x] P5 tasks aligned: P5-T012 (watch-only tiers can't sign), P5-T050 (no signing controls), P5-T001 (USER)

## Verification

### Tests
- Doc review: every listed doc states the same value/name after the fix; `python3 tools/kanban/kanban.py validate` stays at 0 errors

### Scenarios
- Given the fixed docs, when a developer picks up the affected P5 tasks, then there is exactly one authoritative answer to follow

### Stress / failure injection
- n/a: documentation/spec gap

## Acceptance criteria

- [x] Docs listed under Doc sync (and the other docs named in the ToDo) state the decided value/name
- [x] Affected P5 tasks reference the decided value/name and an owning task exists
- [x] Resolution recorded in the progress log

## Exceptions & edge cases

- Until resolved, implementers use the suggested fix as the default and flag it in their PR description

## Cardinal rules (do NOT)

- Do NOT resolve by silently picking a looser (less safe) value; when in doubt choose the stricter option.
- Do NOT edit WORM records to "fix" data; append a correction instead.

## Doc sync on completion

- `docs/13-wallets-treasury-and-onchain.md`: align with the resolution
- `docs/ui/dashboards/D18-wallets-treasury.md`: align with the resolution

## Branch & PR

- Branch: `p5/P5-B008-vault-signing-path-conflict`
- PR title: `P5-B008: Vault signing from the UI (13 §3 step 5) vs vault/warm watch-only (D18, R5.01)`

## Progress log

- 2026-10-21 00:00 · planner · opened
- 2026-10-22 00:00 · aligner · aligned for docs/16–17: Decided (17 §B P5-B008): vault and warm are watch-only; the system never holds their keys and may only prepare unsigned transactions (QR/WalletConnect) for you to sign in your own wallet; P5 has no UI signing path. Docs checked: 13 §1 (watch-only statement), 13 §3 step 5 (manual signing in your own wallet; P5 has no UI signing path), 07 §4 item 1, D18 rules, roadmap R5.01. Implementation owned by P5-T012 (watch-only tiers can't sign), P5-T050 (no signing controls), P5-T001 (USER)
- 2026-10-22 02:10 · cloud:vm:be04b6ae61f8 · verified: decided in docs/17 (17 §B P5-B008); docs updated: 13 §1 (watch-only statement), 13 §3 step 5 (manual signing in your own wallet; P5 has no UI signing path), 07 §4 item 1, D18 rules, roadmap R5.01; implementation owned by P5-T012 (watch-only tiers can't sign), P5-T050 (no signing controls), P5-T001 (USER)
- 2026-10-22 02:10 · cloud:vm:be04b6ae61f8 · done
- 2026-10-22 02:10 · cloud:vm:be04b6ae61f8 · doc sync done: docs updated in the alignment wave
