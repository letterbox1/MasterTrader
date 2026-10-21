---
id: P8-B005
kind: gap
title: Never-exposed list doesn't cover other funds-moving or irreversible commands
phase: 8
type: DOC
status: backlog
priority: medium
size: XS
severity: S3
owner: agent
claimed_by: ""
depends_on: []
requirements: [R8.06]
roadmap_todos: [T8.21, T8.61]
modules: [M20]
dashboards: []
branch: p8/P8-B005-never-exposed-funds-commands
pr: ""
doc_sync: [docs/03-build-spec.md, docs/02-v1-architecture.md, docs/roadmap/phase-8-mcp.md]
doc_sync_status: n/a
found_in: docs/03-build-spec.md M20 safeguards; docs/02-v1-architecture.md §7.2 command catalogue
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P8-B005 · Never-exposed list doesn't cover other funds-moving or irreversible commands

## Goal / expected outcome

The docs agree and are specific about this point, so the P8 tasks that depend on it can be built and tested without guessing. Proposed resolution: classify as **never** for MCP: `wallet.sweep`, `treasury.allocate`, `treasury.earn.enter/exit`, `airdrop.claim.execute`, `system.service.restart`, `system.restore.test`, `memory.delete`, `risk.deadman.ack`, `/system/keys`, `/system/logs`. Leave `wallet.revoke_approval` disabled-but-enableable (it only reduces risk). Record the full list in 03 M20 and 02 §7.4.

## Context & references

- Spec: [03 M20](../../../docs/03-build-spec.md#m20-mcp-control-plane--mt_mcp-built-last-phase-8-only-if-wanted) · [02 §7.2](../../../docs/02-v1-architecture.md#72-commands-rest-write)
- Implementing tasks: P8-T004, P8-T023

## Requirements

- **Steps to reproduce:** Compare the never-exposed list (withdrawals, keys, mandates) with the command catalogue: `wallet.sweep`, `treasury.allocate`, `treasury.earn.enter/exit`, `airdrop.claim.execute`, `wallet.revoke_approval`, `system.service.restart`, `system.restore.test`, `memory.delete`, `risk.deadman.ack`, and the `/system/keys` and `/system/logs` queries.
- **Expected:** Each is either outside the M20 scope list (so not exposed) or explicitly classified.
- **Actual:** Unclassified. `wallet.sweep` moves funds between wallets (close to a withdrawal); `airdrop.claim.execute` triggers signing.
- **Impact:** Ambiguity about what the registry may enable later; risk of a funds-moving tool becoming enableable (S3)
- **Suggested fix:** classify as **never** for MCP: `wallet.sweep`, `treasury.allocate`, `treasury.earn.enter/exit`, `airdrop.claim.execute`, `system.service.restart`, `system.restore.test`, `memory.delete`, `risk.deadman.ack`, `/system/keys`, `/system/logs`. Leave `wallet.revoke_approval` disabled-but-enableable (it only reduces risk). Record the full list in 03 M20 and 02 §7.4.

## ToDo

- [ ] Confirm the proposed resolution (with the user if it changes behaviour)
- [ ] Edit the listed docs so they agree with each other
- [ ] Write or point to the test in the implementing P8 task that pins the behaviour
- [ ] Note the resolution in the Progress log

## Verification

### Tests
- Regression: the implementing task's test (named in Context) pins the documented behaviour.

### Scenarios
- Given the docs are fixed, when a developer reads only the linked sections, then they implement the same behaviour as the P8 task describes.

### Stress / failure injection
- n/a: documentation gap.

## Acceptance criteria

- [ ] Docs updated and mutually consistent
- [ ] Implementing task test exists and passes
- [ ] Resolution noted in the Progress log

## Exceptions & edge cases

- If the user rejects the proposal, record the alternative here and update the implementing task before it starts.

## Cardinal rules (do NOT)

- Do NOT close without the docs actually agreeing.
- Do NOT edit WORM records to "fix" data; append a correction instead.
- Do NOT expose withdrawals, API-key management or wallet mandate signing through MCP, in any form (R8.06).

## Doc sync on completion

- `docs/03-build-spec.md`: as described in the suggested fix.
- `docs/02-v1-architecture.md`: as described in the suggested fix.
- `docs/roadmap/phase-8-mcp.md`: note the clarified behaviour if it changes a requirement's wording.

## Branch & PR

- Branch: `p8/P8-B005-never-exposed-funds-commands`
- PR title: `P8-B005: fix never-exposed list doesn't cover other funds-moving or irreversible commands`
- PR checklist: docs consistent · implementing test referenced · `./kanban done P8-B005` run

## Progress log

- 2026-10-21 00:00 · planner · opened
