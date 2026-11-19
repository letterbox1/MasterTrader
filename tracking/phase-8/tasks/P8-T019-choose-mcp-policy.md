---
id: P8-T019
kind: task
title: Seed the MCP token and tool defaults: read-only scopes, write tool groups off, expiry rules per 16 §2.12
phase: 8
type: BUILD
status: backlog
priority: high
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P8-T002, P8-T004, P8-T016]
requirements: [R8.04, R8.08]
roadmap_todos: [T8.03]
modules: [M20, M11]
dashboards: [D17]
tools: [cargo, git]
mcp: []
env: []
services: [supabase-postgres, mt-api]
branch: p8/P8-T019-choose-mcp-policy
pr: ""
doc_sync: [docs/roadmap/phase-8-mcp.md, docs/16-configuration-and-safety-model.md]
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

# P8-T019 · Seed the MCP token and tool defaults: read-only scopes, write tool groups off, expiry rules per 16 §2.12

## Goal / expected outcome

MCP starts safe without asking you anything: the token-create form and OAuth consent default to read-only scopes, the write tool groups (trade & adjust, strategies, risk tighten) are seeded **disabled** in the registry, and the expiry options and rules are exactly those in [16 §2.12](../../../docs/16-configuration-and-safety-model.md#212-mcp-phase-8). The defaults are seeded through `mt-api` with source `seed`. You review them in D17 (or in the go-live pack, P7-T070, if it is still open) and can change them any time; enabling a write tool group or creating a write-scope token stays a C3 action that only you take.

## Context & references

- Roadmap: [R8.04, R8.08](../../../docs/roadmap/phase-8-mcp.md#3-requirements) · ToDo [T8.03](../../../docs/roadmap/phase-8-mcp.md#4-todo-sets)
- Platform: [18 §2.1](../../../docs/18-platform-and-deployment.md#21-rust-cargo-workspace-crates) (`mt-api` in Rust; `mt-mcp` on `rmcp`)
- Decisions: [16 §2.12](../../../docs/16-configuration-and-safety-model.md#212-mcp-phase-8) (scopes; `trade` creates approval cards only; C1 for `read`/`analyse`/`curation`, C3 for `trade`/`strategy`/`risk_tighten` and indefinite expiry; rate limits; response cap) · [16 §2.3](../../../docs/16-configuration-and-safety-model.md#23-decisions-approvals-and-hitl) (MCP orders always need your card, TTL 5 min) · [17 §D P8-B010](../../../docs/17-decisions-register.md#d-other-decisions) (no skip-approval) · [17 §G](../../../docs/17-decisions-register.md#g-platform-rust-and-python-supabase-vercel-workstation-first-2026-11-19) (agents seed configurable values; you review once)
- Spec: [03 M20 safeguards](../../../docs/03-build-spec.md#m20-mcp-control-plane--mt_mcp-built-last-phase-8-only-if-wanted)
- UI: [D17 Tokens + Tool registry](../../../docs/ui/dashboards/D17-mcp-console.md)
- Built on: P8-T002 (tokens, scopes), P8-T004 (registry, never-exposed list), P8-T016 (D17). Unblocks P8-T028, P8-T029, P8-T035.

## Requirements

- One machine-readable defaults file `config/defaults/mcp.yaml`, checked against 16 §2.12 by a doc-parse test so they can't drift:
  - default scopes offered pre-selected on token create and OAuth consent: `read`, `analyse` (read-only); `curation`, `trade`, `strategy`, `risk_tighten` unselected;
  - expiry options exactly 1 day · 7 days · 30 days · 1 year · custom · indefinite; indefinite is never pre-selected and always shows the red warning, needs C3 and gets the monthly reminder;
  - rate limits 60 reads/min and 10 writes/min per token; response cap 256 KB per tool result.
- Registry seed (matches P8-T004): read & analyse, talk-to-agents and curation tools `enabled` (C1 scopes); trade & adjust, strategies and risk-tighten tools `disabled`; never-exposed entries stay `never` and can't be seeded otherwise. A token still sees only the tools its scopes allow.
- Seeding goes through `mt-api` commands with source `seed`; idempotent (re-run adds nothing when nothing changed); never overwrites a value you've set (your rows win).
- Enabling a write tool group or creating a `trade`/`strategy`/`risk_tighten` token stays C3 (Telegram approve + TOTP + cool-down); enabling read/analyse/curation tools stays C1. The seed never enables a write group and never creates a token.
- There is no skip-approval or auto-execute setting to seed.

## ToDo

- [ ] Write `config/defaults/mcp.yaml` from 16 §2.12 and the doc-parse test
- [ ] `mt mcp seed` (CLI over `mt-api`) seeding the token-form defaults, limits and the registry states with source `seed`
- [ ] Run it on the stack; screenshot D17 Tokens (create form defaults) and Tool registry (write groups off)
- [ ] Add the effective MCP defaults to the go-live pack generator if P7-T070 is still open; otherwise list them in D17 → Policy with their 16 links
- [ ] Tests; progress log; `./kanban done P8-T019`

## Verification

### Tests
- `cargo test -p mt-api mcp_seed`: every seeded value equals the defaults file; defaults file equals 16 §2.12 (doc-parse test).
- Re-run the seed: no new rows. Enable `order_place` by hand (C3 in the test harness), re-run: it stays enabled.
- The seed can't set a never-exposed tool to anything but `never`.

### Scenarios
- Given a fresh stack, when `mt mcp seed` runs, then D17 shows only read/analyse/agent/curation tools enabled and the create form pre-selects `read` + `analyse` with no expiry pre-selected as indefinite.
- Given the defaults, when you enable `order_place` in D17, then the C3 flow starts (Telegram approve + TOTP + cool-down) and the tool appears only after it completes.
- Given you look for an "auto-approve" option in D17, then there is none.

### Stress / failure injection
- Seed while Postgres restarts: the command fails cleanly with no partial registry update (one transaction).

## Acceptance criteria

- [ ] Defaults file matches 16 §2.12 (doc-parse test green)
- [ ] Registry seeded with every write group disabled; idempotent; never overwrites your changes
- [ ] Token form and OAuth consent default to read-only scopes; indefinite never pre-selected

## Exceptions & edge cases

- P8-T001 decided `go-read-only`: the seed is the same; the write groups simply stay off.
- Kill ON while you later enable a write tool: enabling is still possible, but trade tools return `kill_on` until you turn kill off (C3).

## Cardinal rules (do NOT)

- Do NOT enable any write tool group, create any token or choose an expiry for you; those are your actions (C3 for write scopes and indefinite expiry).
- Do NOT add a skip-approval or auto-execute setting; MCP can never approve.
- Do NOT hard-code the defaults in code; they come from the defaults file.
- Do NOT make loosening risk, autonomous mode, mandates or kill-switch OFF anything less than C3; protective exits never wait for approval.
- Do NOT commit secrets or paste them into chats/issues (including the Claude conversation); secrets live in the sops/age file (07 §2).

## Doc sync on completion

- `docs/roadmap/phase-8-mcp.md`: tick T8.03 noting the seeded defaults (T8.03's per-client choice is yours, any time, in D17).
- `docs/16-configuration-and-safety-model.md` §2.12: note the seeded default scopes if the doc owner agrees.

## Branch & PR

- Branch: `p8/P8-T019-choose-mcp-policy`
- PR title: `P8-T019: Seed the MCP token and tool defaults: read-only scopes, write tool groups off, expiry rules per 16 §2.12`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P8-T019` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (T8.03 is now scopes + expiry per client; auto rules / skip-approval removed (17 §D P8-B010); write-scope tokens and tool enables are C3; dropped gap dep P8-B010; added R8.08; tools/env/services)
- 2026-11-19 00:00 · aligner · re-platformed per docs/18 (converted USER → agent BUILD (17 §G, brief §2): seeds read-only defaults; dropped USER dep P8-T018; enabling write tool groups stays C3)
