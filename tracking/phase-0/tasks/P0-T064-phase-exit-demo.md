---
id: P0-T064
kind: task
title: Phase 0 exit demo: run every exit criterion
phase: 0
type: VERIFY
status: backlog
priority: critical
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P0-T063, P0-T058, P0-T057, P0-T053, P0-T055, P0-T054, P0-T028, P0-T056, P0-T026, P0-T059, P0-T060, P0-T061, P0-T066, P0-T067, P0-T068, P0-T069, P0-T070, P0-T071, P0-T072, P0-T073, P0-T062, P0-T074]
requirements: [R0.01, R0.02, R0.03, R0.04, R0.05, R0.06, R0.07, R0.08, R0.09, R0.10, R0.11, R0.12, R0.13, R0.14, R0.N1, R0.N2, R0.N3, R0.N4, R0.N5, R0.N6, R0.N7]
roadmap_todos: [T0.80]
modules: [ops, mt-api, M17, M15, M21]
dashboards: [D16]
tools: [docker, supabase, cargo, just, gh]
mcp: []
env: []
services: [supabase-postgres, supabase-auth]
branch: p0/P0-T064-phase-exit-demo
pr: ""
doc_sync: [tracking/phase-0/PHASE.md, docs/roadmap/phase-0-foundations.md]
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

# P0-T064 · Phase 0 exit demo: run every exit criterion

## Goal / expected outcome

A recorded walkthrough on the always-on workstation stack (self-hosted Supabase + Compose, [18 §9](../../../docs/18-platform-and-deployment.md#9-workstation-first-build-path)) proves all four roadmap exit criteria and every P0 requirement's verification, so PHASE.md's exit boxes can be ticked and Phase 1 opens.

## Context & references

- [Roadmap P0 §6 exit criteria](../../../docs/roadmap/phase-0-foundations.md#6-exit-criteria-demo)
- [Roadmap P0 §5 deliverables](../../../docs/roadmap/phase-0-foundations.md#5-deliverables)
- [Roadmap P0 §3 requirements (Verified by column)](../../../docs/roadmap/phase-0-foundations.md#3-requirements)
- Depends on: P0-T063 (soak; brings in the whole stack), P0-T058, P0-T057, P0-T053, P0-T055, P0-T054, P0-T028, P0-T056, P0-T026, P0-T059, P0-T060, P0-T061, P0-T066, P0-T067, P0-T068, P0-T069, P0-T070 (Supabase stack), P0-T071 (`mt_store` binding), P0-T072 (partitions), P0-T073 (real seal target + bot), and the USER walkthrough P0-T062 (your own login for exit 2)

## Requirements

- Exit 1: `just up` (`supabase start` or the self-hosted Supabase stack + `docker compose up`, from stopped) → all services healthy (table); Grafana shows workstation/DB/NATS health; logs visible in Loki.
- Exit 2: log in with password + TOTP through Supabase Auth (your account from P0-T062, reaching `aal2`); a test command appears in `audit.command` with a valid hash chain (D16 Audit ✓ + `mt_store::worm::recompute_chain` output).
- Exit 3: restore from the off-site backup succeeds (latest `ops.restore_test` pass, from P0-T057 or a fresh run).
- Exit 4: the shell passes the viewport matrix 240 → 2560 px (latest green CI run of P0-T053).
- Requirement evidence: CI green on `main` (R0.01, R0.N5 scans) + the `just licence-audit` report with every ⚑ item registered (R0.N5, P0-T074); `supabase db reset` + `supabase test db` with all 13 schemas, RLS deny-all and Data API/Realtime off (R0.03, P0-T070); monthly partitions (P0-T072); `pit` golden tests in Rust and through the Python binding + the bypass guard for both languages (R0.04, P0-T071, P0-T028); schema test for provenance (R0.05); venue registry seeded (R0.06); WORM suite + the real seal target (R0.07, P0-T073); API + C-level tests (R0.08); live LiteLLM/TEI smoke with `audit.llm_call` rows (R0.09, R0.13, P0-T068); integrity drill (R0.12, P0-T069); restart refusal (R0.14, P0-T067); WORM insert benchmark (R0.N7, P0-T066); Grafana board (R0.10); D16 Playwright (R0.11); gitleaks + secrets review (R0.N1); workstation baseline checklist (R0.N2); port scan + netprobe (R0.N3); restore test (R0.N4); viewport matrix (R0.N6); soak report.
- Open S1/S2 bugs in Phase 0 = 0; all tasks done/cancelled.

## ToDo

- [ ] Prepare a checklist page `docs/runbooks/evidence/p0-exit-<date>.md` with one row per item above and a link to its evidence.
- [ ] Run the live demo steps 1–4 on the workstation and capture screenshots/log excerpts (no secrets).
- [ ] Confirm no open S1/S2 bugs and all other P0 tasks done/cancelled (`./kanban list --phase 0`).
- [ ] Tick PHASE.md exit criteria and the roadmap ToDo boxes per doc sync; hand over to the main agent for `./kanban build`.

## Verification

### Tests
- The demo steps and the evidence checklist.

### Scenarios
- Given any criterion fails, then the demo stops, a bug is filed with severity, and the demo is re-run after the fix.

### Stress / failure injection
- Covered by P0-T063 and P0-T059 evidence.

## Acceptance criteria

- [ ] Exit 1–4 demonstrated with evidence linked
- [ ] Every R0.xx has linked evidence
- [ ] 0 open S1/S2 bugs; all tasks closed
- [ ] PHASE.md exit boxes ticked
- [ ] CI green (clippy, cargo test, ruff, mypy, pytest, `supabase test db`, gitleaks, `pit` check)

## Exceptions & edge cases

- Deferred hardware items (UPS/4G, P0-T012) don't block exit if ordered; they're required before P7.

## Cardinal rules (do NOT)

- Do NOT tick an exit box without linked evidence.
- Do NOT demo on the CI or Supabase CLI test stack; use the always-on workstation stack (the runtime host comes at the shift, P7-T073).
- Do NOT skip, weaken or delete a test to get CI green.
- Do NOT commit secrets or paste them into chats, issues, PRs or logs; secrets live only in the sops/age file ([07 §2](../../../docs/07-security-notes.md#2-secrets)).

## Doc sync on completion

- `tracking/phase-0/PHASE.md`: tick exit criteria; `docs/roadmap/README.md`: nothing by hand (generated) — the main agent runs build.
- `docs/roadmap/phase-0-foundations.md`: tick T0.80 when every item mapped to it is done.

## Branch & PR

- Branch: `p0/P0-T064-phase-exit-demo`
- PR title: `P0-T064: Phase 0 exit demo: run every exit criterion`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P0-T064` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (exit evidence covers R0.12–R0.14 and R0.N7 via P0-T066–P0-T069; deps trimmed; run fields added)
- 2026-11-19 00:00 · aligner · re-platformed per docs/18 (demo on the always-on workstation; depends on the new P0-T070–P0-T073 and the USER walkthrough P0-T062 (exit demos may list it); Supabase/pgTAP evidence replaces the Alembic migration test)
- 2026-11-20 00:00 · aligner · Rust-max per 17 §H (exit demo depends on P0-T074 and cites the licence-audit report for R0.N5)
