---
id: P6-T072
kind: task
title: "Optional investor-persona lenses as debate viewpoints (off by default)"
phase: 6
type: BUILD
status: backlog
priority: low
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P6-T007, P6-T003]
requirements: [R6.08]
roadmap_todos: [T6.34]
modules: [M8]
dashboards: [D10]
tools: [git, cargo]
mcp: []
env: []
services: [litellm, llm-local]
branch: p6/P6-T072-investor-persona-lenses
pr: ""
doc_sync: [docs/03-build-spec.md, docs/roadmap/phase-6-ai-models-treasury.md]
doc_sync_status: n/a
found_in: ""
created: 2026-11-19
updated: 2026-11-20
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
review_result: ""
---

# P6-T072 · Optional investor-persona lenses as debate viewpoints (off by default)

## Goal / expected outcome

Optional analyst viewpoints modelled on well-known investment styles (value, quality, growth-at-a-reasonable-price, macro), idea from ai-hedge-fund's persona signals (MIT), added to the debate graph as configurable lenses, off by default and enabled only if they improve shadow results.

## Context & references

- Roadmap: [R6.08 / T6.34](../../../docs/roadmap/phase-6-ai-models-treasury.md#4-todo-sets)
- Debate graph P6-T007
- Vetting and decision: [01 §8](../../../docs/01-repo-vetting-report.md#8-addendum-2026-11-19-eleven-more-repositories) · [17 §F](../../../docs/17-decisions-register.md#f-vetted-additions-2026-11-19)

## Requirements

- Lenses are prompt/config only; no new data sources (ai-hedge-fund's paid data and wallet payments are not used).
- Each lens is a setting (on/off per strategy), off by default.
- Lens outputs are recorded in the decision run like other analysts.
- Tools & access: listed in the front matter (`tools`, `mcp`, `env`, `services`); `./kanban preflight P6-T072` checks them before start.

## ToDo

- [ ] Lens configs and prompts
- [ ] Debate graph wiring in `mt-agents` behind `modules.persona_lenses.enabled` (seeded off by P6-T003)
- [ ] Write tests (see Verification)
- [ ] Update docs listed under Doc sync

## Verification

### Tests
- Unit: with lenses off the debate output is unchanged; with a lens on its view appears in the run record.

### Scenarios
- Given a lens enabled for one strategy, then other strategies are unaffected.

### Stress / failure injection
- n/a: prompt-level feature within existing budgets

## Acceptance criteria

- [ ] Off by default
- [ ] Shadow comparison possible (P6-T073)
- [ ] CI green (`cargo test -p mt-agents persona_lenses`, `cargo clippy`)

## Exceptions & edge cases

- If a lens consistently worsens shadow results, it stays off and is noted in the bake-off report.

## Cardinal rules (do NOT)

- Do NOT commit secrets or paste them into chats, issues or logs; they live only in the sops/age file ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Do NOT add paid data/APIs, scraping that breaks a site's terms, self-bots/user tokens, or any sybil/fake engagement.
- Do NOT let Telegram text (or any `model_input_ok = false` row) reach a model, RAG index or training set ([12 §4–5](../../../docs/12-policy-and-compliance.md#4-per-platform-data--automation-rules)).
- Do NOT read research data except through `pit(as_of)`; do NOT route any order around M11 via `mt-api`.
- Do NOT skip, weaken or delete a test to get green.
- Do NOT copy code from repositories without a compatible licence; keep copyright and NOTICE files for MIT/Apache code ([01 §8](../../../docs/01-repo-vetting-report.md#8-addendum-2026-11-19-eleven-more-repositories)).
- Do NOT name lenses after living people in user-facing text; describe the style.

## Doc sync on completion

- `docs/03-build-spec.md`: M8 optional lenses
- `docs/roadmap/phase-6-ai-models-treasury.md`: tick T6.34

## Branch & PR

- Branch: `p6/P6-T072-investor-persona-lenses`
- PR title: `P6-T072: Optional investor-persona lenses as debate viewpoints (off by default)`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P6-T072` run

## Progress log

- 2026-11-19 00:00 · coordinator · created from the 2026-11-19 repository vetting (01 §8, 17 §F)
- 2026-11-19 00:00 · aligner · re-platformed per docs/18 (services `postgres` → `supabase-postgres`; `mt_api` → `mt-api`)
- 2026-11-20 00:00 · aligner · Rust-max per 17 §H (lenses wired into the Rust debate graph; setting seeded off by P6-T003; tools cargo)
