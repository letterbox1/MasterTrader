---
id: P0-T066
kind: task
title: Benchmark WORM inserts: p99 under 5 ms, order path never waits on seals
phase: 0
type: VERIFY
status: backlog
priority: high
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P0-T031, P0-T037]
requirements: [R0.N7, R0.07]
roadmap_todos: [T0.67]
modules: [M17, mt_obs, mt_store]
dashboards: []
tools: [git, uv, python>=3.12, docker]
mcp: []
env: []
services: [postgres, nats, prefect-server, minio]
branch: p0/P0-T066-worm-insert-benchmark
pr: ""
doc_sync: [docs/15-bots-hitl-and-worm-audit.md, docs/02-v1-architecture.md, docs/roadmap/phase-0-foundations.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-22
updated: 2026-10-22
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
review_result: ""
---

# P0-T066 · Benchmark WORM inserts: p99 under 5 ms, order path never waits on seals

## Goal / expected outcome

A repeatable benchmark (`make wormbench`) proves the WORM write-path SLO on the production host: inserts into hash-chained WORM tables stay at **p99 < 5 ms** under sustained load, including while the daily seal and a full verify run, and no call that later phases put on the order path (`mt_obs.audit.write` for `audit.order`/`audit.fill`/`audit.command`) ever waits on a seal or a verify (R0.N7, [17 §D](../../../docs/17-decisions-register.md#d-other-decisions) P0-B004).

## Context & references

- Roadmap: [R0.N7 · T0.67](../../../docs/roadmap/phase-0-foundations.md#3-requirements)
- SLO: [02 §9.2](../../../docs/02-v1-architecture.md#92-observability--slos) (WORM insert p99 < 5 ms; the order path never waits on seals)
- [15 §2.2 Write path](../../../docs/15-bots-hitl-and-worm-audit.md#22-layers), [15 §2.4 tests](../../../docs/15-bots-hitl-and-worm-audit.md#24-tests-part-of-every-phase-that-adds-a-worm-table)
- [16 §3.3 write path vs integrity check](../../../docs/16-configuration-and-safety-model.md#33-records-the-write-path-vs-the-integrity-check)
- Implementation under test: P0-T030 (chain trigger), P0-T031 (writer + JetStream buffer), P0-T037 (seal flow), P0-T038 (verify)
- Depends on: P0-T031, P0-T037

## Requirements

- Functional:
  - Load profile: 16 concurrent writers, 1,000 rows/s sustained into one chain of `audit.command` for 10 min, plus 60 s bursts of 5,000 rows/s spread over 4 chains; realistic row sizes (args jsonb ≈ 1 KB).
  - Measure client-side insert latency (`mt_obs.audit.write` call → commit) as an HDR histogram; report p50/p95/p99/p99.9 and max.
  - Run three phases: (a) inserts alone; (b) inserts while `seal_daily` seals 5 M rows; (c) inserts while a full `audit.verify` runs; plus (d) with the seal anchor store hung (MinIO paused) to show anchoring can't back-pressure inserts.
  - "Never waits on seals" is also checked statically: the seal and verify code paths take no locks on chain heads or WORM tables (no `pg_advisory_xact_lock`, `LOCK TABLE`, `SELECT … FOR UPDATE`), and `mt_obs.audit.write` exposes no call that awaits seal or verify state.
- Non-functional:
  - Gate: p99 < 5 ms in every phase on the production host; the CI run is a smaller smoke (non-gated, logged) because shared runners are noisy.
  - Results committed to `docs/runbooks/evidence/p0-worm-bench-<date>.md` with host spec and Postgres settings.
- Tools & access: listed in the front matter; no secrets (scratch database only).

## ToDo

- [ ] Write `tools/bench/worm_insert.py` (asyncio writers, HDR histogram, phase orchestration) and `make wormbench`.
- [ ] Add the static check (`tests/worm/test_no_seal_locks.py`) for seal/verify lock usage and the writer API.
- [ ] Run phases (a)–(d) on the host against a scratch DB; capture histograms and Grafana screenshots.
- [ ] Add the CI smoke variant (2 min, logged, not gated).
- [ ] File a bug for any phase over the SLO (do not relax the target).
- [ ] Write the evidence file and update docs listed under Doc sync.

## Verification

### Tests
- Static: the lock-usage check fails on a fixture flow that calls `pg_advisory_xact_lock` on a chain head.
- Benchmark: phases (a)–(d) with the p99 gate.

### Scenarios
- Given the daily seal starts at 00:15 UTC during heavy activity, when inserts continue, then their p99 stays < 5 ms and no insert blocks on the seal.
- Given the anchor store is unreachable, when the seal retries hourly, then insert latency is unchanged.

### Stress / failure injection
- The benchmark itself (sustained + burst load, concurrent seal/verify, hung anchor store).

## Acceptance criteria

- [ ] p99 < 5 ms in phases (a)–(d) on the production host (evidence committed)
- [ ] Static check proves seal/verify take no chain-head or table locks
- [ ] CI smoke variant runs and logs results
- [ ] CI green (ruff, mypy, pytest, gitleaks, `pit` check)

## Exceptions & edge cases

- Laptop/VM numbers don't count for the gate; only the production host run does.
- Autovacuum or checkpoints can cause outliers: report p99.9/max, but the gate is p99.
- If the host misses the SLO, tune (e.g. chain key granularity, `synchronous_commit` stays on) and re-run; never weaken the target or the hash.

## Cardinal rules (do NOT)

- Do NOT run the benchmark against production WORM tables; scratch DB only (rows can't be deleted afterwards).
- Do NOT relax the 5 ms target, drop the hash chain or turn off `synchronous_commit` to pass.
- Do NOT UPDATE or DELETE WORM rows, ever; corrections are new rows with `supersedes_id` ([15 §2](../../../docs/15-bots-hitl-and-worm-audit.md#2-worm-records-write-once-read-many)).
- Do NOT skip, weaken or delete a test to get CI green.

## Doc sync on completion

- `docs/15-bots-hitl-and-worm-audit.md` §2.4: link `make wormbench` and the evidence file.
- `docs/02-v1-architecture.md` §9.2: note the measured value next to the WORM insert SLO.
- `docs/roadmap/phase-0-foundations.md`: tick T0.67 when every item mapped to it is done.

## Branch & PR

- Branch: `p0/P0-T066-worm-insert-benchmark`
- PR title: `P0-T066: Benchmark WORM inserts: p99 under 5 ms, order path never waits on seals`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P0-T066` run

## Progress log

- 2026-10-22 02:01 · cloud:vm:be04b6ae61f8 · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (new task for R0.N7 / T0.67, decided in 17 §D P0-B004)
