---
id: P0-T074
kind: task
title: Licence audit and copyleft register check (just licence-audit)
phase: 0
type: BUILD
status: ready
priority: medium
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P0-T014]
requirements: [R0.N1]
roadmap_todos: []
modules: [M17]
dashboards: []
tools: [git, cargo, uv]
mcp: []
env: []
services: []
branch: p0/P0-T074-licence-audit-and-copyleft-register-check-just-l
pr: ""
doc_sync: [docs/19-third-party-register.md, docs/05-saas-legal-and-licensing.md]
doc_sync_status: n/a
found_in: ""
created: 2026-11-20
updated: 2026-11-20
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
review_result: ""
---
# P0-T074 · Licence audit and copyleft register check (just licence-audit)

## Goal / expected outcome

One command, `just licence-audit`, lists the licence of every Rust crate, Python package, container image and vendored file, flags every copyleft or non-standard licence (⚑), and fails if anything ⚑ isn't in the register ([19 §4](../../../docs/19-third-party-register.md#4-copyleft-register--and-the-release-plan)) or if copyleft code sits outside `third_party/copyleft/`. Private use is unaffected; this keeps a possible future release a known checklist.

## Context & references

- Register: [19](../../../docs/19-third-party-register.md) · decision [17 §H](../../../docs/17-decisions-register.md#h-rust-max-borrowed-code-rebuilt-in-rust-scenario-simulator-copyleft-register-2026-11-20) · supply chain [07 §7](../../../docs/07-security-notes.md#7-supply-chain)
- Builds on P0-T014 (repo skeleton, gitleaks); runs in the pre-push hook as a warning and in the manual CI job.

## Requirements

- `cargo deny check licenses` with an allow-list (MIT, Apache-2.0, BSD-2/3, ISC, Zlib, MPL-2.0, Unicode, CC0) and explicit ⚑ exceptions mirroring 19 §4 (NautilusTrader LGPL-3.0).
- `pip-licenses` over the uv workspace (vectorbt Commons Clause and MetaTrader5 flagged ⚑).
- Container images: licence label or a maintained map in `infra/licences/images.yaml` (Grafana/Loki AGPL ⚑ marked "unmodified, separate").
- `third_party/`: every folder has a LICENSE; copyleft only under `third_party/copyleft/`; NOTICE entries for MIT/Apache text we adapted (TradingAgents, FinRobot, Vibe-Trading, Anthropic skills).
- Output: a Markdown report `reports/licence-audit.md` with a ⚑ section; exit non-zero on an unregistered ⚑.
- Verify the (U) licence facts in 19 (Supabase components, Hindsight, crawl4ai attribution, rss-bridge, trafilatura, MetaTrader5) and update 19 with source and date.

## ToDo

- [ ] `deny.toml` licence policy and exceptions
- [ ] pip-licenses step and image map
- [ ] `third_party/` scanner and NOTICE check
- [ ] `just licence-audit` + report; hook warning
- [ ] Verify the (U) rows in 19 and update them
- [ ] Tests; docs

## Verification

### Tests
- Fixture crate with a GPL dependency → audit fails naming it; adding it to the register exceptions → passes.
- A GPL file outside `third_party/copyleft/` → fails.

### Scenarios
- Given the vendored freqtrade analysers are still present, when the audit runs, then it lists them as ⚑ "to be replaced by mt-lab-core (17 §H)".

### Stress / failure injection
- n/a: static audit.

## Acceptance criteria

- [ ] `just licence-audit` produces the report and fails on unregistered ⚑ items
- [ ] 19's (U) licence facts verified with sources

## Exceptions & edge cases

- Dual-licensed crates: record the licence we use (e.g. ntfy Apache-2.0).

## Cardinal rules (do NOT)

- Do NOT remove a ⚑ by editing the register without the evidence; do NOT vendor copyleft code outside `third_party/copyleft/`.

## Doc sync on completion

- docs/19-third-party-register.md, docs/05-saas-legal-and-licensing.md: update with the verified facts.

## Branch & PR

- Branch: `p0/P0-T074-licence-audit-and-copyleft-register-check-just-l`
- PR title: `P0-T074: Licence audit and copyleft register check (just licence-audit)`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P0-T074` run

## Progress log

- 2026-11-20 00:53 · cloud:vm:be04b6ae61f8 · created
