---
id: P7-T070
kind: task
title: Approve the go-live pack: risk values, ceilings, sleeves and manifests
phase: 7
type: USER
status: backlog
priority: critical
size: S
severity: ""
owner: user
claimed_by: ""
depends_on: [P7-T011, P2-T048, P2-T049, P2-T050, P2-T066, P1-T001, P1-T066]
requirements: [R7.17]
roadmap_todos: [T7.12]
modules: [M11, M0]
dashboards: [D16, D06, D03]
tools: []
mcp: []
env: []
services: [mt-web, telegram]
branch: p7/P7-T070-approve-the-go-live-pack-risk-values-ceilings-sl
pr: ""
doc_sync: [docs/roadmap/phase-7-prove-and-go-live.md]
doc_sync_status: n/a
found_in: ""
created: 2026-11-19
updated: 2026-11-19
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
review_result: ""
---
# P7-T070 · Approve the go-live pack: risk values, ceilings, sleeves and manifests

## Goal / expected outcome

Before any live money, you review one page, the **go-live pack** (D16 → Go-live preflight → Settings pack), and approve it with one C3 action. It lists every effective value the agents seeded or drafted during the build: the L0 ceilings and L1–L3 policy (P2-T048), the sleeves and their budgets (P2-T049), and the strategy manifests (P2-T050), plus every other value agents seeded from the docs' defaults, when present: the starting universe (P1-T001), tuned DQ thresholds (P1-T066), keywords/cashtags/feeds (P4-T003), the disposal rule and EV hurdle (P5-T007), wallet/signer/gas limits (P5-T065), LLM budgets (P6-T001), optional modules (P6-T003, all off) and the treasury policy (P6-T033). Each row shows the default and any change made since. This is the **only** point where those values are put to you; everything stays editable afterwards in D03/D06.

## Context & references

- Seeds: P2-T048, P2-T049, P2-T050. Preflight: P7-T011 (refuses live mode while the pack is unapproved).
- Defaults: [16 §2](../../../docs/16-configuration-and-safety-model.md#2-default-values-all-configurable), [14 §3/§7](../../../docs/14-strategy-evidence-and-validation.md#3-strategy-catalogue-evidence-ranked-templates).
- Decisions: [17 §G](../../../docs/17-decisions-register.md#g-platform-rust-and-python-supabase-vercel-workstation-first-2026-11-19) (agents draft values; you approve once at go-live).
- Unblocks: P7-T057 (fund micro-live).

## Requirements

- Read the pack (about 10 minutes). Any value you want different: change it in D03/D06 first (tightening applies at once; loosening is C3), then approve.
- Approve with the pack's **Approve** button, which issues `ops.golive_pack.approve` (C3: Telegram approve + TOTP + cool-down). The approval is a WORM row naming the policy and manifest versions approved; a later loosening needs its own C3 as usual.

## ToDo

- [ ] Open D16 → Go-live preflight → Settings pack and read it
- [ ] Change anything you want different in D03/D06
- [ ] Approve the pack (C3)
- [ ] Agent confirms the approval row and the manifests' `approved: true`, then runs `./kanban done P7-T070`

## Verification

### Tests
- Agent confirms: `ops.golive_pack.approve` row in `audit.command` naming the versions; preflight check "settings pack approved" passes.

### Scenarios
- Given the pack is approved, when a policy value is later loosened, then that change needs its own C3 and the pack shows "changed since approval".

### Stress / failure injection
- n/a: approval action.

## Acceptance criteria

- [ ] Pack approved (C3) with the versions recorded
- [ ] P7-T011 preflight shows the settings-pack check as pass

## Exceptions & edge cases

- If you change values after approving, the pack shows "changed since approval"; a loosening needs its own C3 and the preflight check fails until the pack is re-approved.
- Values a later phase seeds after your approval (e.g. P5/P6 modules) appear as "new since approval"; the preflight requires a re-approval before any bot that uses them goes live.

## Cardinal rules (do NOT)

- The agent never approves the pack for you; it only prepares it and confirms the result.

## Doc sync on completion

- docs/roadmap/phase-7-prove-and-go-live.md: update to match what was built.

## Branch & PR

- Branch: `p7/P7-T070-approve-the-go-live-pack-risk-values-ceilings-sl`
- PR title: `P7-T070: Approve the go-live pack: risk values, ceilings, sleeves and manifests`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P7-T070` run

## Progress log

- 2026-11-19 09:14 · cloud:vm:be04b6ae61f8 · created
- 2026-11-19 00:00 · aligner · re-platformed per docs/18 (requirements R7.17 / ToDo T7.12; approval command `ops.golive_pack.approve` (C3); the pack also lists P1/P4/P5/P6 seeded values; added deps P1-T001, P1-T066 (seeded values reviewed here))
