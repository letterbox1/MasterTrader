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
updated: 2026-10-21
---

# Phase 0 · Foundations & security baseline

## Summary

Phase 0 delivers a secure, reproducible single-box stack that every later phase plugs into ([roadmap](../../docs/roadmap/phase-0-foundations.md)): a hardened, Tailscale-only host; a Compose stack pinned by digest (Postgres 16 + TimescaleDB + pgvector, NATS JetStream, Prefect, MLflow, Caddy, observability, LiteLLM ≥ 1.83, TEI); the nine Postgres schemas with provenance columns, `ops.venue_registry` and `pit(as_of)` with a CI bypass test; the **WORM audit layer** (offline `worm_owner`, blocking triggers, per-row hash chain, daily Merkle seal anchored to Object-Locked storage + OpenTimestamps + Telegram witness, `audit.verify` with incident path and trading halt, immutable backups and monthly exports); the `mt_api` skeleton (Argon2 + TOTP, command bus with idempotency and `audit.command`, server-side C0–C3/Kill, WebSocket `seq`); and the web shell + D16 System on the DESIGN.md v2 preset, proven by the Playwright viewport matrix.

Work is organised in workstreams (below). The **"do now" USER items run in parallel from day one** — P0-T001 (Reddit, deadline **2026-10-31**) is the most urgent; P0-T005 (hardware) is the only entry criterion; P0-T003, P0-T006 and P0-T002 unblock secrets, backups and seal anchoring. 64 tasks (14 USER · 25 BUILD · 13 OPS · 9 VERIFY · 2 DOC · 1 RUN) and 18 gap items.

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
| Your actions (USER), later in phase | P0-T013, P0-T062 |
| Repo, CI & core libraries (BUILD/OPS) | P0-T014, P0-T015, P0-T016, P0-T017, P0-T018 |
| Host, Compose, networks, secrets (OPS) | P0-T019, P0-T020, P0-T021, P0-T022, P0-T023 |
| Data store, provenance, venue registry, `pit` (BUILD) | P0-T024, P0-T025, P0-T026, P0-T027, P0-T028 |
| WORM audit layer (BUILD) | P0-T029, P0-T030, P0-T031, P0-T037, P0-T038, P0-T040 |
| `mt_api` (BUILD) | P0-T032, P0-T033, P0-T034, P0-T035, P0-T036, P0-T046 |
| Backups & restore (OPS) | P0-T039, P0-T041 |
| Model gateway & embedder (OPS) | P0-T042, P0-T043, P0-T044 |
| Observability (OPS) | P0-T023, P0-T045 |
| Web shell & D16 (BUILD) | P0-T047, P0-T048, P0-T049, P0-T050, P0-T051, P0-T052 |
| Verify (tests, scenarios, stress, scans) | P0-T028, P0-T053, P0-T054, P0-T055, P0-T056, P0-T057, P0-T058, P0-T059 |
| Docs / runbooks | P0-T060, P0-T061 |
| Run / soak | P0-T063 |
| Phase exit | P0-T064 |

## Critical path

By size weight (≈ 44 units, the longest dependency chain): P0-T014 → P0-T020 → P0-T022 → P0-T013 → P0-T029 → P0-T030 → P0-T031 → P0-T033 → P0-T036 → P0-T048 → P0-T050 → P0-T051 → P0-T053 → P0-T064.

In elapsed time the real gate is the **72-hour soak** (P0-T063), which can only start when the whole stack runs on the production host, and the USER chain P0-T005 → P0-T019 and P0-T003 → P0-T022 → P0-T013 (offline `worm_owner` ceremony) → P0-T029. Start the USER items now; build on a laptop/VM until the host arrives.

## Traceability

| Requirement | Tasks |
|---|---|
| R0.01 | P0-T014, P0-T015, P0-T016, P0-T017, P0-T064 |
| R0.02 | P0-T005, P0-T020, P0-T023, P0-T059, P0-T063, P0-T064 |
| R0.03 | P0-T024, P0-T064 |
| R0.04 | P0-T027, P0-T028, P0-T064 |
| R0.05 | P0-T025, P0-T064 |
| R0.06 | P0-T011, P0-T025, P0-T026, P0-T064 |
| R0.07 | P0-T006, P0-T013, P0-T029, P0-T030, P0-T031, P0-T037, P0-T038, P0-T039, P0-T040, P0-T041, P0-T052, P0-T055, P0-T058, P0-T059, P0-T061, P0-T063, P0-T064 |
| R0.08 | P0-T031, P0-T032, P0-T033, P0-T034, P0-T035, P0-T036, P0-T046, P0-T048, P0-T050, P0-T054, P0-T058, P0-T059, P0-T062, P0-T064 |
| R0.09 | P0-T007, P0-T042, P0-T043, P0-T044, P0-T059, P0-T064 |
| R0.10 | P0-T018, P0-T023, P0-T045, P0-T059, P0-T063, P0-T064 |
| R0.11 | P0-T046, P0-T047, P0-T048, P0-T049, P0-T050, P0-T051, P0-T052, P0-T053, P0-T058, P0-T064 |
| R0.N1 | P0-T003, P0-T004, P0-T013, P0-T015, P0-T017, P0-T022, P0-T061, P0-T064 |
| R0.N2 | P0-T003, P0-T012, P0-T019, P0-T056, P0-T060, P0-T064 |
| R0.N3 | P0-T021, P0-T056, P0-T064 |
| R0.N4 | P0-T006, P0-T039, P0-T040, P0-T041, P0-T057, P0-T060, P0-T063, P0-T064 |
| R0.N5 | P0-T004, P0-T014, P0-T015, P0-T056, P0-T064 |
| R0.N6 | P0-T049, P0-T050, P0-T053, P0-T064 |

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
| T0.20 | P0-T014, P0-T015 |
| T0.21 | P0-T016, P0-T017 |
| T0.22 | P0-T024, P0-T025, P0-T026, P0-T027 |
| T0.23 | P0-T013, P0-T029, P0-T030, P0-T031, P0-T037, P0-T038, P0-T040, P0-T058 |
| T0.24 | P0-T032, P0-T033, P0-T034, P0-T035, P0-T036, P0-T046, P0-T058, P0-T059 |
| T0.25 | P0-T018 |
| T0.26 | P0-T046, P0-T047, P0-T048, P0-T049, P0-T050, P0-T051, P0-T052 |
| T0.40 | P0-T019 |
| T0.41 | P0-T020, P0-T023, P0-T042, P0-T043, P0-T059 |
| T0.42 | P0-T021 |
| T0.43 | P0-T022 |
| T0.44 | P0-T039, P0-T040, P0-T041 |
| T0.45 | P0-T007, P0-T042, P0-T043, P0-T044, P0-T059 |
| T0.46 | P0-T023, P0-T045 |
| T0.60 | P0-T028 |
| T0.61 | P0-T055 |
| T0.62 | P0-T054 |
| T0.63 | P0-T057 |
| T0.64 | P0-T053 |
| T0.65 | P0-T015, P0-T056 |
| T0.80 | P0-T063, P0-T064 |
| T0.90 | P0-T060, P0-T061 |

Every R0.xx and T0.xx is covered. P0-T007 (LLM credentials) and P0-T013 (offline `worm_owner` credential) are USER steps the roadmap doesn't list; they are mapped to T0.45 and T0.23 and filed as gaps where the roadmap is silent (P0-B009).

## Planning notes & risks

- **Reddit deadline 2026-10-31** (P0-T001): decide this week; "no" is fine (06 §0 treats Reddit as sunsetting and deferred).
- **Hardware lead time / GPU** (P0-T005): build on a laptop/VM; GPU decision due by P4. CPU-only means `local-advisor` is slow (P0-T044) and TEI runs on CPU.
- **C3 before Telegram exists**: the Telegram approval channel is P2 (T2.33). P0 uses a host-only break-glass channel (`mt-admin approve` over SSH + TOTP) so C3 is testable and Kill OFF is possible (P0-T035, P0-B002).
- **Trading halt on verify mismatch** has no agreed mechanism (P0-B001, S2): P0 sets `risk_state.trading_halt`; P2's M11 must honour it. This S2 gap blocks phase completion until the docs are reconciled.
- **Secrets file location**: decided outside the repo (`/etc/mastertrader/secrets.sops.yaml`) to satisfy "no secret in git" strictly (P0-B018).
- **Object Lock arithmetic**: pgBackRest expiry fails if bucket lock > repo retention; buckets use 35 days, seals/exports 7 years (P0-T006, P0-T039).
- **Provisional SLOs**: audit insert p99 < 5 ms at ≥ 1,000 rows/s and command p99 < 50 ms until the docs set numbers (P0-B004).
- **CI minutes**: GitHub Free private repos get 2,000 min/month; the 33-viewport Playwright matrix runs on web changes + nightly, sharded.
- **Paid-but-allowed items**: Claude API (spend-capped, P0-T007) and Backblaze B2 storage (first 10 GB free; rest-server box is the free alternative). No paid data.
- **RAM budget** on a 32 GB host: Postgres ~8 GB, TEI rerank ~2 GB, local-advisor ~4–6 GB, obs ~2 GB, rest ~3 GB; fits, but P1 recorders will need the 64 GB end.
- **Shell placeholders**: engine version, feed summary and mode badge show `n/a`/`PAPER` until P1/P2 provide data; no fake data (DESIGN §10).
- Layout follows 02 §11 (`infra/`, `migrations/`, `apps/web/`) per P0-B006; nine schemas only per P0-B005.

## Cross-phase prerequisites

Phase 0 depends on no earlier phase. Its tasks rely on these later-phase roadmap items to complete the designs they start:

| Later item | Phase | What P0 relies on it for |
|---|---|---|
| T2.33 / R2.51 (Telegram C3 approve + TOTP) | P2 | Replaces the P0 break-glass C3 channel as the primary approval path (P0-T035) |
| R2.10, R2.16 (M11 default-deny pre-trade checks) | P2 | Honouring `risk_state.trading_halt` set by `audit.verify` (P0-T038, P0-B001) |
| R2.19 / T2.24 (change-control classifier) | P2 | Tighten/loosen classification beyond P0's settings classifier (P0-T035) |
| R1.14 / T1.31 (Telegram + email + ntfy alerts) | P1 | Second independent alert channel for WORM incidents and backup failures (P0-T045) |
| R1.09 (provenance population + retention jobs) | P1 | Filling the provenance columns created in P0 (P0-T025) |
| R1.13 / T1.30 (venue-health collector, quarterly AUSTRAC re-check) | P1 | Keeping `ops.venue_registry` current after the P0 seed (P0-T026) |

Later phases that add WORM tables (P2 `risk.change`, `strategy.bot_version`; P3 `journal.*`; P5 mandates, signer ledger) must use `create_worm_table()` (P0-T029) and re-run the WORM suite (P0-T055).
