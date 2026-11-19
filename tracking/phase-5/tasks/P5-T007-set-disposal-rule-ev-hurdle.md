---
id: P5-T007
kind: task
title: Seed the disposal rule and EV hurdle from the 08/16 defaults
phase: 5
type: BUILD
status: backlog
priority: medium
size: XS
severity: ""
owner: agent
claimed_by: ""
depends_on: [P5-T040, P5-T045]
requirements: [R5.14, R5.17]
roadmap_todos: [T5.06]
modules: [M4]
dashboards: [D12]
tools: [git, uv]
mcp: []
env: []
services: [supabase-postgres, mt-api]
branch: p5/P5-T007-set-disposal-rule-ev-hurdle
pr: ""
doc_sync: [docs/roadmap/phase-5-airdrops-wallets-curation.md]
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

# P5-T007 · Seed the disposal rule and EV hurdle from the 08/16 defaults

## Goal / expected outcome

The airdrop settings section holds the **disposal rule** (default: sell 50% on claim; until the P7 gates each disposal is a manual-sale USER task, P5-T066) and the **EV inputs** (hurdle 5% p.a. on capital locked; time value and default haircut drafted by the agent because the docs give no default), seeded through `mt-api` with source `seed`, so the EV gate (P5-T040) and disposal tasks (P5-T045) run on documented defaults. Nothing is asked of you during the build: you review these once in the go-live pack (P7-T070) and can change them in D12 settings any time.

## Context & references

- Roadmap: ToDo T5.06 → R5.14, R5.17
- [08 EV gate](../../../docs/08-airdrops-and-token-launches.md#expected-value-gate-airdrops-icosidos-points-programmes) · [08 wallet discipline](../../../docs/08-airdrops-and-token-launches.md#wallet-discipline)
- Defaults: [16 §2.7](../../../docs/16-configuration-and-safety-model.md#27-wallets-signer-and-gas-13) (EV hurdle 5% p.a. on capital locked, an AUD cash-rate proxy; decision P5-B012) and [08 wallet discipline](../../../docs/08-airdrops-and-token-launches.md#wallet-discipline) (disposal 50%); both are settings ([17 §E](../../../docs/17-decisions-register.md#e-ratification-2026-10-22)); loosening is C3
- Time value and haircut: 08 names them but neither 08 nor 16 gives a default; the agent drafts conservative values and records them for 16 §2.7 (gap P5-B018).
- Disposal before P7: manual-sale task (decision P5-B010, [17 §B](../../../docs/17-decisions-register.md#b-cross-doc-conflicts-one-canonical-answer))
- Decision: [17 §G](../../../docs/17-decisions-register.md#g-platform-rust-and-python-supabase-vercel-workstation-first-2026-11-19): configurable values are seeded from the doc defaults and approved once in the go-live pack (P7-T070), never asked during the build.
- Depends on: P5-T040 (EV gate settings), P5-T045 (disposal rule)

## Requirements

- Disposal rule: percent to sell on claim (default 50%) and what happens to the rest (hold under M22 rules). Before the P7 gates every disposal is a manual-sale `ONCHAIN_ACTION_MANUAL` task; from P7 it becomes an M11 order.
- EV inputs: hurdle rate (default 5% p.a.), time value (AUD/min) and default haircut, each with `seed_source` (doc section, or "drafted, gap P5-B018").
- Drafted values must be conservative: they may only remove opportunities from the digest compared with a zero time value and zero haircut, never add them.
- Seeded through `system.settings.update` section `airdrop` via `mt-api` with source `seed`; idempotent; never overwrites your edits. Later changes by you: tightening applies at once; loosening (e.g. a lower hurdle → more tasks) is C3 ([02 §7.2](../../../docs/02-v1-architecture.md#72-commands-rest-write); 08 principle 5).

## ToDo

- [ ] Write `config/defaults/airdrop_settings.yaml` (disposal 50%, hurdle 5% p.a. from 16 §2.7 / 08; drafted time value and haircut) and a doc-parse test against 08 and 16 §2.7
- [ ] Extend the settings seed command with the `airdrop` section; run it; D12 settings show each value with its source
- [ ] Record the drafted time value and haircut in gap P5-B018 so 16 §2.7 can list them
- [ ] Tests; progress log; `./kanban done P5-T007`

## Verification

### Tests
- Seeded values match the defaults file; re-running the seed changes nothing; a value you edited keeps your value after a re-seed (`uv run pytest`).
- An opportunity's EV breakdown in D12 shows the seeded hurdle and time value.

### Scenarios
- Given hurdle 8% p.a. and time value A$1/min, when a 60-minute task's EV falls below 0, then it drops out of the digest.
- Given you later lower the hurdle in D12, then the change asks for C3 before it applies.

### Stress / failure injection
- n/a: seed data.

## Acceptance criteria

- [ ] Disposal rule and EV inputs seeded with source `seed` and visible in D12
- [ ] Digest EV values computed with the seeded inputs

## Exceptions & edge cases

- Every disposal is a manual-sale task until the P7 gates pass (P5-B010), whatever the venue; the rule here only sets the quantity.

## Cardinal rules (do NOT)

- Do NOT set up any automated sale path before the P7 gates; after them, every sale is an order through M11.
- Do NOT bypass `mt-api`, the risk manager (M11, `mt-risk`) or `pit(as_of)` (`mt-store`); every order goes through M11, and until the P7 live gates pass, disposal sales are manual USER tasks (never automated).
- Do NOT overwrite a value you edited; numbers come from the defaults file, never hard-coded.

## Doc sync on completion

- `docs/roadmap/phase-5-airdrops-wallets-curation.md`: tick T5.06 when this lands (with the other tasks sharing that ToDo).

## Branch & PR

- Branch: `p5/P5-T007-set-disposal-rule-ev-hurdle`
- PR title: `P5-T007: Seed the disposal rule and EV hurdle from the 08/16 defaults`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P5-T007` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (EV hurdle default 5% p.a. per 16 §2.7/P5-B012; disposal = manual-sale task until P7 per P5-B010; loosening C3)
- 2026-11-19 00:00 · aligner · re-platformed per docs/18 (converted from a USER task to an agent seed task per 17 §G: disposal 50% and hurdle 5% p.a. seeded from 08 / 16 §2.7 through `mt-api` with source `seed`; time value and haircut have no doc default, drafted conservatively and raised as gap P5-B018; you review in the go-live pack P7-T070; services `supabase-postgres`, `mt-api`)
