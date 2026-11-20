---
id: P6-T003
kind: task
title: Record the optional-module defaults (all off) in settings
phase: 6
type: BUILD
status: ready
priority: medium
size: XS
severity: ""
owner: agent
claimed_by: ""
depends_on: []
requirements: [R6.30, R6.31, R6.35]
roadmap_todos: [T6.04]
modules: [M13, M23, M9, M8]
dashboards: [D11, D13]
tools: [git, cargo]
mcp: []
env: []
services: [supabase-postgres, mt-api]
branch: p6/P6-T003-decide-optional-modules
pr: ""
doc_sync: [tracking/phase-6/PHASE.md, docs/roadmap/phase-6-ai-models-treasury.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-11-20
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
review_result: ""
---

# P6-T003 · Record the optional-module defaults (all off) in settings

## Goal / expected outcome

The optional modules of [16 §2.14a](../../../docs/16-configuration-and-safety-model.md#214a-optional-modules) have explicit settings, **all off by default** as the docs say: Hummingbot MM sidecar, M23 social drafts, credibility scoring, the LightRAG filings graph and the investor-persona lenses. Nothing waits for a decision from you: you can switch any module on later in D16 → Settings, and only then does its build item (P6-T046, P6-T047, P6-T048, P6-T051) get worked (the persona lenses are built by P6-T072 and stay off until shadow results justify them). The scenario & crowd simulator (M14) is **not** optional any more: it is a go-live tool with its own settings (16 §2.14b, P6-T050, P6-T076). The values appear in the go-live pack (P7-T070).

## Context & references

- Roadmap: [R6.30](../../../docs/roadmap/phase-6-ai-models-treasury.md#3-requirements) · [R6.31](../../../docs/roadmap/phase-6-ai-models-treasury.md#3-requirements) · [R6.35](../../../docs/roadmap/phase-6-ai-models-treasury.md#3-requirements) · ToDo T6.04
- Spec: [03 M13](../../../docs/03-build-spec.md#m13-market-making-sidecar) · [03 M23](../../../docs/03-build-spec.md#m23-social-participation--mt_social) · [03 M9](../../../docs/03-build-spec.md#m9-memory--rag--mt_memory) (LightRAG optional) · [14 §3](../../../docs/14-strategy-evidence-and-validation.md#3-strategy-catalogue-evidence-ranked-templates) (market-making must beat HLP)
- Decisions: [17 §H](../../../docs/17-decisions-register.md#h-rust-max-borrowed-code-rebuilt-in-rust-scenario-simulator-copyleft-register-2026-11-20) (the crowd simulator is a go-live tool, not an optional module; supersedes P6-B009) · [17 §G](../../../docs/17-decisions-register.md#g-platform-rust-and-python-supabase-vercel-workstation-first-2026-11-19) (configurable values are seeded, not asked)
- Used by: P6-T046, P6-T047, P6-T048, P6-T051, P6-T072 (each checks its module flag); P6-T066 (cancels items whose module is still off at exit).

## Requirements

- Settings with source `seed`: `modules.hummingbot.enabled: false`, `modules.social_drafts.enabled: false`, `modules.credibility.enabled: false`, `modules.lightrag.enabled: false`, `modules.persona_lenses.enabled: false`, each with a one-line reason and its doc link. `modules.crowdsim.enabled` is not seeded (superseded, 16 §2.14a); the `crowdsim.*` settings are seeded by P6-T076.
- Seeded through `mt-api` (`system.settings.update`), idempotent, never overwriting a value you set.
- Turning a module on is a settings change under the usual rules: Hummingbot can place orders, so enabling it is a loosening (C3, and it still needs the venue approved in the registry); the others are C1.
- While a module is off, its containers are not started and its UI is hidden from navigation (D11 for Hummingbot).

## ToDo

- [ ] Add the five `modules.*.enabled` settings with defaults `false` to the defaults file and seed them via `mt-api`
- [ ] Settings classifier: Hummingbot on = C3; others C1
- [ ] Compose profiles and nav read the flags (off → not started, hidden)
- [ ] Add the module rows to the go-live pack generator (P7-T070)
- [ ] Tests; progress log; `./kanban done P6-T003`

## Verification

### Tests
- `cargo test -p mt-api settings_seed_modules`: five settings seeded `false` with source `seed`; re-run adds nothing; your `true` survives a re-seed.
- Enabling `modules.hummingbot.enabled` is classified C3; the others C1.

### Scenarios
- Given the defaults, when D16 → Settings loads, then all five modules show "off (default)" with their doc links and D11 is not in the nav.
- Given you enable LightRAG, then P6-T051 becomes workable and its container profile can start.

### Stress / failure injection
- n/a: four settings rows.

## Acceptance criteria

- [ ] All five module settings seeded `false` with source `seed`
- [ ] Confirmation levels for turning them on are enforced
- [ ] Module rows appear in the go-live pack

## Exceptions & edge cases

- You can turn a module on at any time; if its build item was cancelled at P6 exit, re-open it (`./kanban reopen <ID>`).

## Cardinal rules (do NOT)

- Do NOT turn a module on for the user; defaults stay off.
- Do NOT enable any optional module that adds auto-posting, extra accounts or telemetry.
- Do NOT commit secrets or paste them into chats/issues/PRs; secrets live only in the sops/age file (07 §2).
- Do NOT skip, weaken or delete a test to get green.

## Doc sync on completion

- `docs/16-configuration-and-safety-model.md` §2.14a: confirm the five `modules.*.enabled` defaults (off).
- `tracking/phase-6/PHASE.md`: planning notes say the optional modules are off by default.
- `docs/roadmap/phase-6-ai-models-treasury.md`: tick T6.04 (and note this task ID) once all items covering it are done.

## Branch & PR

- Branch: `p6/P6-T003-decide-optional-modules`
- PR title: `P6-T003: Record the optional-module defaults (all off) in settings`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P6-T003` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (crowd-sim condition per 17 §D P6-B009; run fields)
- 2026-11-19 00:00 · aligner · re-platformed per docs/18 (converted from a USER decision to a short agent task (17 §G): optional modules are seeded off by default and can be enabled any time in settings; P6-T046..T051 now depend on nothing human)
- 2026-11-20 00:00 · aligner · Rust-max per 17 §H (optional modules per 16 §2.14a: crowd-sim removed (go-live tool, 16 §2.14b), credibility and persona lenses added; LightRAG now R6.35)
