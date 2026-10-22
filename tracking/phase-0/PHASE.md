---
phase: 0
title: Foundations & security baseline
roadmap: docs/roadmap/phase-0-foundations.md
status: not_started
opens_after: []
force_open: false
started: ""
completed: ""
doc_sync_status: n/a
updated: 2026-10-22
---

# Phase 0 · Foundations & security baseline

## Summary

Phase 0 delivers a secure, reproducible single-box stack that every later phase plugs into ([roadmap](../../docs/roadmap/phase-0-foundations.md)): a hardened, Tailscale-only host; a Compose stack pinned by digest (Postgres 16 + TimescaleDB + pgvector, NATS JetStream, Prefect, MLflow, Caddy, observability, LiteLLM ≥ 1.83, `tei-embed` + `tei-rerank`, `llm-local`, `docker-proxy`); all **13 canonical Postgres schemas** with provenance columns, `ops.venue_registry` and `pit(as_of)` with a CI bypass test; the **WORM audit layer** (offline `worm_owner`, blocking triggers, per-row hash chain, daily Merkle seal anchored to Object-Locked storage + OpenTimestamps + Telegram witness, hourly incremental + daily full `audit.verify`, JetStream write buffer, insert p99 < 5 ms) with the **integrity response** (KV `audit.integrity`, default `block_new_entries`, `mt_risk.integrity_gate` hook, cleared only by `audit.integrity.ack` C3); the `mt_api` skeleton (Argon2 + TOTP, command bus with idempotency and `audit.command`, server-side C0–C3/Kill with `confirm_token`, C2 risk-preview hash + 12 h re-auth, C3 via the break-glass `mtctl approve` + TOTP + cool-down until Telegram C3 in P2, WebSocket `seq`); `system.service.restart` only through the allow-listed `docker-proxy`; `audit.llm_call` from day one; and the web shell + D16 System on the DESIGN.md v2 preset, proven by the Playwright viewport matrix.

Aligned to [16](../../docs/16-configuration-and-safety-model.md) and [17](../../docs/17-decisions-register.md) on 2026-10-22: every number is a configurable default linked to 16; **build first, keys last**: integrations are built and tested keyless (mocks, MinIO, mocked Bot API, throwaway age/`worm_owner` credentials) and the live checks with your keys/accounts are late tasks (P0-T057 backup target, P0-T063 soak with real bucket and bot, P0-T068 LLM gateway). 69 tasks (14 USER · 25 BUILD · 14 OPS · 13 VERIFY · 2 DOC · 1 RUN); gap items P0-B001–P0-B018 closed with evidence, P0-B019 (S4) open.

## Entry criteria

- [ ] Host hardware exists (P0-T005), or a laptop/VM is designated to run the stack until it arrives (roadmap §2, §7)
- [ ] Phase opens immediately (`opens_after: []`); urgent USER items P0-T001 (by 2026-10-31), P0-T003, P0-T004 started

## Exit criteria

- [ ] `docker compose up` → all services healthy; Grafana shows host/DB/NATS health and logs in Loki (P0-T020, P0-T023, P0-T045, P0-T064)
- [ ] Log in with password + TOTP; a test command appears in `audit.command` with a valid hash chain (P0-T062, P0-T058, P0-T064)
- [ ] A restore from the off-site backup succeeds (P0-T057, P0-T064)
- [ ] The shell passes the viewport matrix from 240 px to 2560 px (P0-T053, P0-T064)
- [ ] All Phase 0 tasks are done or cancelled
- [ ] No open S1/S2 bugs or gaps in Phase 0

## Workstreams

| Workstream | Tasks |
|---|---|
| Your actions (USER), do now | P0-T001, P0-T002, P0-T003, P0-T004, P0-T005, P0-T006, P0-T007, P0-T008, P0-T009, P0-T010, P0-T011, P0-T012 |
| Your actions (USER), later in phase | P0-T013 (offline `worm_owner` ceremony, before production WORM migrations), P0-T062 (password + TOTP on the production host) |
| Repo, CI & core libraries (BUILD/OPS) | P0-T014, P0-T015, P0-T016, P0-T017, P0-T018 |
| Host, Compose, networks, secrets (OPS) | P0-T019, P0-T020, P0-T021, P0-T022, P0-T023, P0-T065 |
| Data store, provenance, venue registry, `pit` (BUILD) | P0-T024, P0-T025, P0-T026, P0-T027, P0-T028 |
| WORM audit layer + integrity response (BUILD) | P0-T029, P0-T030, P0-T031, P0-T037, P0-T038, P0-T040 |
| `mt_api` (BUILD) | P0-T032, P0-T033, P0-T034, P0-T035, P0-T036, P0-T046 |
| Backups & restore (OPS) | P0-T039, P0-T041 |
| Model gateway & embedder (OPS, keyless) | P0-T042, P0-T043, P0-T044 |
| Observability (OPS) | P0-T023, P0-T045 |
| Web shell & D16 (BUILD) | P0-T047, P0-T048, P0-T049, P0-T050, P0-T051, P0-T052 |
| Verify (tests, scenarios, stress, scans, drills) | P0-T028, P0-T053, P0-T054, P0-T055, P0-T056, P0-T058, P0-T059, P0-T066, P0-T067, P0-T069 |
| Late live checks (keys last) | P0-T057 (real backup target), P0-T068 (LLM gateway with your keys), P0-T063 (soak: real bucket + bot) |
| Docs / runbooks | P0-T060, P0-T061 |
| Run / soak | P0-T063 |
| Phase exit | P0-T064 |

Up to six agents can run in parallel: after P0-T014, the CI, core-library, Compose/network, web-scaffold and USER streams are independent; after P0-T024 the `pit`, provenance and WORM streams split; nothing in the build streams waits on a USER key task.

## Critical path

By size weight (≈ 44 units, the longest dependency chain): P0-T014 → P0-T020 → P0-T024 → P0-T029 → P0-T030 → P0-T031 → P0-T033 → P0-T035 → P0-T038 → P0-T046 → P0-T051 → P0-T053 → P0-T064. No USER task is on it any more: the age identity (P0-T003) and the `worm_owner` ceremony (P0-T013) were moved off the build chain (keyless builds with test credentials).

In elapsed time the real gate is the **72-hour soak** (P0-T063): it needs the production host (P0-T005 → P0-T019), the ceremony (P0-T013, after P0-T061) and your real accounts (P0-T006, P0-T002). Start the USER items now; build on a laptop/VM until the host arrives.

## Traceability

| Requirement | Tasks |
|---|---|
| R0.01 | P0-T014, P0-T015, P0-T016, P0-T017, P0-T064 |
| R0.02 | P0-T005, P0-T020, P0-T023, P0-T059, P0-T063, P0-T064, P0-T065 |
| R0.03 | P0-T024, P0-T064 |
| R0.04 | P0-T027, P0-T028, P0-T064 |
| R0.05 | P0-T025, P0-T064 |
| R0.06 | P0-T011, P0-T025, P0-T026, P0-T064 |
| R0.07 | P0-T006, P0-T013, P0-T029, P0-T030, P0-T031, P0-T037, P0-T038, P0-T039, P0-T040, P0-T041, P0-T052, P0-T055, P0-T057, P0-T058, P0-T059, P0-T061, P0-T063, P0-T064, P0-T066, P0-T069 |
| R0.08 | P0-T031, P0-T032, P0-T033, P0-T034, P0-T035, P0-T036, P0-T046, P0-T048, P0-T050, P0-T054, P0-T058, P0-T059, P0-T062, P0-T064 |
| R0.09 | P0-T007, P0-T042, P0-T043, P0-T044, P0-T059, P0-T064, P0-T068 |
| R0.10 | P0-T018, P0-T023, P0-T045, P0-T059, P0-T063, P0-T064 |
| R0.11 | P0-T046, P0-T047, P0-T048, P0-T049, P0-T050, P0-T051, P0-T052, P0-T053, P0-T058, P0-T064 |
| R0.12 | P0-T035, P0-T038, P0-T046, P0-T052, P0-T054, P0-T055, P0-T061, P0-T063, P0-T064, P0-T069 |
| R0.13 | P0-T007, P0-T031, P0-T042, P0-T043, P0-T044, P0-T064, P0-T068 |
| R0.14 | P0-T021, P0-T051, P0-T064, P0-T065, P0-T067 |
| R0.N1 | P0-T003, P0-T004, P0-T013, P0-T015, P0-T017, P0-T022, P0-T061, P0-T064 |
| R0.N2 | P0-T003, P0-T012, P0-T019, P0-T056, P0-T060, P0-T064 |
| R0.N3 | P0-T021, P0-T056, P0-T064 |
| R0.N4 | P0-T006, P0-T039, P0-T040, P0-T041, P0-T057, P0-T060, P0-T063, P0-T064 |
| R0.N5 | P0-T004, P0-T014, P0-T015, P0-T056, P0-T064 |
| R0.N6 | P0-T049, P0-T050, P0-T053, P0-T064 |
| R0.N7 | P0-T030, P0-T031, P0-T037, P0-T055, P0-T059, P0-T064, P0-T066 |

| Roadmap ToDo | Tasks |
|---|---|
| T0.01 | P0-T005 |
| T0.02 | P0-T012 |
| T0.03 | P0-T003 |
| T0.04 | P0-T006 |
| T0.05 | P0-T004 |
| T0.06 | P0-T002 |
| T0.07 | P0-T008 |
| T0.08 | P0-T001 |
| T0.09 | P0-T009 |
| T0.10 | P0-T010 |
| T0.11 | P0-T011, P0-T026 |
| T0.12 | P0-T033, P0-T062 |
| T0.13 | P0-T007 |
| T0.20 | P0-T014, P0-T015 |
| T0.21 | P0-T016, P0-T017 |
| T0.22 | P0-T024, P0-T025, P0-T026, P0-T027 |
| T0.23 | P0-T013, P0-T029, P0-T030, P0-T031, P0-T037, P0-T038, P0-T040, P0-T058 |
| T0.24 | P0-T032, P0-T033, P0-T034, P0-T035, P0-T036, P0-T046, P0-T058, P0-T059 |
| T0.25 | P0-T018 |
| T0.26 | P0-T046, P0-T047, P0-T048, P0-T049, P0-T050, P0-T051, P0-T052 |
| T0.27 | P0-T035, P0-T038 |
| T0.28 | P0-T031, P0-T042, P0-T043, P0-T044 |
| T0.40 | P0-T019 |
| T0.41 | P0-T020, P0-T023, P0-T042, P0-T043, P0-T044, P0-T059, P0-T065 |
| T0.42 | P0-T021 |
| T0.43 | P0-T022 |
| T0.44 | P0-T039, P0-T040, P0-T041 |
| T0.45 | P0-T042, P0-T043, P0-T044, P0-T059 |
| T0.46 | P0-T023, P0-T045 |
| T0.47 | P0-T065 |
| T0.60 | P0-T028 |
| T0.61 | P0-T055 |
| T0.62 | P0-T054 |
| T0.63 | P0-T057 |
| T0.64 | P0-T053 |
| T0.65 | P0-T015, P0-T056 |
| T0.66 | P0-T069 |
| T0.67 | P0-T066 |
| T0.68 | P0-T067 |
| T0.69 | P0-T068 |
| T0.80 | P0-T063, P0-T064 |
| T0.90 | P0-T060, P0-T061 |

Every R0.xx and T0.xx is covered. P0-T013 (offline `worm_owner` credential) is a USER step the roadmap folds into T0.23. Roadmap T0.28 (LiteLLM callback, TEI split, `llm-local`, keyless) is unrelated to task P0-T028 (`pit` bypass test).

## Planning notes & risks

- **Reddit deadline 2026-10-31** (P0-T001): decide this week; "no" is fine (06 §0 treats Reddit as sunsetting and deferred).
- **Hardware lead time / GPU** (P0-T005): build on a laptop/VM; GPU decision due by P4. CPU-only means `llm-local` is slow and TEI runs on CPU; tier B on CPU is ~100–400 ms per decision (17 §B P6-B002).
- **Build first, keys last** (17 §E): P0-T022 uses a throwaway age key, P0-T029–P0-T031 a throwaway `worm_owner` password, P0-T037/P0-T039/P0-T040 MinIO with Object Lock, P0-T045 a mocked Bot API, P0-T042 a mock LLM provider. The real accounts are first used in P0-T057 (backup target), P0-T063 (seals/witness/alerts) and P0-T068 (LLM keys), which carry the env names.
- **C3 before Telegram**: until Telegram C3 lands in P2 (T2.33, retired via T2.24), C3 completes through the host-only break-glass CLI `mtctl approve <id>` + TOTP, audited (17 §D P0-B002; P0-T035).
- **Integrity response** (17 §A P0-B001, 16 §2.11): KV `audit.integrity`, default `block_new_entries`; P0 builds the `mt_risk.integrity_gate` hook point and P2 calls it inline on every order (R2.58/T2.39).
- **Secrets file location**: outside the repo, e.g. `~/.config/mastertrader/secrets.sops.yaml`, backed up by restic (17 §D P0-B018).
- **WORM write path**: if Postgres is unreachable, WORM writes buffer in JetStream (default 1 GB or 24 h; new entries stop above 80 %, exits/Kill still recorded; 16 §3.3).
- **Object Lock arithmetic**: pgBackRest expiry fails if bucket lock > repo retention; buckets use 35 days, seals/exports 7 years (P0-T006, P0-T039).
- **SLOs** (02 §9.2): WORM insert p99 < 5 ms (gated in P0-T066), command bus p99 < 50 ms excl. handler.
- **Defaults not yet in 16** (P0-B019, S4): confirm-token/C3-approval TTLs, login lockout, absolute session lifetime, Loki retention, seal grace, backup times/retention, restart allow-list. Tasks keep them as settings meanwhile.
- **Audit table names**: canonical singular names (17 §B); P0 also adds `audit.auth_event` and `audit.verify_run` (same convention), to be added to the canonical list at P0-T031 doc sync.
- **CI minutes**: GitHub Free private repos get 2,000 min/month; the 33-viewport Playwright matrix runs on web changes + nightly, sharded.
- **Paid-but-allowed items**: Claude API (spend-capped at the 16 §2.10 US$40/month default, P0-T007) and Backblaze B2 storage (first 10 GB free; rest-server box is the free alternative). No paid data.
- **RAM budget** on a 32 GB host: Postgres ~8 GB, `tei-rerank` ~2 GB, `llm-local` ~4–6 GB, obs ~2 GB, rest ~3 GB; fits, but P1 recorders will need the 64 GB end.
- **Shell placeholders**: engine version, feed summary and mode badge show `n/a`/`PAPER` until P1/P2 provide data; modes are only `paper` / `hitl` / `autonomous` (17 §B); no fake data (DESIGN §10).
- Layout follows 03 §3 (canonical; 02 §11 points to it, P0-B006); all 13 schemas are created in P0 (P0-B005).

## Cross-phase prerequisites

Phase 0 depends on no earlier phase, so no task here has a cross-phase `depends_on`. Later phases build on these P0 hooks:

| Later item | Phase | What it takes over from P0 |
|---|---|---|
| T2.33 / R2.51 (Telegram C3 approve + TOTP), T2.24 / R2.19 | P2 | Replace the break-glass `mtctl approve` channel (P0-T035) as the primary C3 path |
| T2.39 / R2.58, T2.71 | P2 | M11 calls `mt_risk.integrity_gate` inline on every order (P0-T038) |
| R2.19 / T2.24 (change-control classifier) | P2 | Tighten/loosen classification beyond P0's settings classifier (P0-T035) |
| R1.14 / T1.31 (single alert fan-out) | P1 | Replaces P0's direct Alertmanager → Telegram route (P0-T045) |
| R1.09 (provenance population + retention jobs) | P1 | Filling the provenance columns created in P0 (P0-T025) |
| R1.13 / T1.30 (venue-health collector, quarterly AUSTRAC re-check) | P1 | Keeping `ops.venue_registry` current after the P0 seed (P0-T026) |

Later phases that add WORM tables (P2 `risk.change`, `risk.approval`, `strategy.bot_version`; P3 `journal.*`; P5 mandates, signer ledger; P8 `audit.mcp_call`) must use `create_worm_table()` (P0-T029) and re-run the WORM suite (P0-T055) and benchmark (P0-T066).
