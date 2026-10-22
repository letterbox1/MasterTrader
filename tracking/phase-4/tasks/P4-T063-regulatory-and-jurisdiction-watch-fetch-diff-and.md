---
id: P4-T063
kind: task
title: Regulatory and jurisdiction watch: fetch, diff and REG_CHANGE review tasks
phase: 4
type: BUILD
status: backlog
priority: medium
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P4-T011, P4-T008, P3-T038, P3-T031, P1-T045]
requirements: [R4.15]
roadmap_todos: [T4.30]
modules: [M5, M16, M19]
dashboards: [D13, D07]
tools: [uv, git, docker]
mcp: []
env: []
services: [postgres, nats, crawl4ai, prefect-server]
branch: p4/P4-T063-regulatory-and-jurisdiction-watch-fetch-diff-and
pr: ""
doc_sync: [docs/06-aggregators-and-market-providers.md, docs/02-v1-architecture.md, docs/roadmap/phase-4-intel.md]
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

# P4-T063 · Regulatory and jurisdiction watch: fetch, diff and REG_CHANGE review tasks

## Goal / expected outcome

Official Australian sources (ATO, Treasury, AUSTRAC, ASIC, RBA), plus UAE/Cyprus/Egypt authorities only while your residency timeline has a planned period there, are fetched on a schedule, diffed against the last snapshot, and every material change becomes a `REG_CHANGE` review task for you (and your tax agent where relevant). **Rules are never auto-applied**: a reviewed change becomes a versioned rule or registry update through the normal C-level commands.

## Context & references

- Roadmap: [R4.15](../../../docs/roadmap/phase-4-intel.md#3-requirements) (verified by a diff + task test) · ToDo [T4.30](../../../docs/roadmap/phase-4-intel.md#4-todo-sets)
- Live inputs: [16 §4.3](../../../docs/16-configuration-and-safety-model.md#43-live-inputs-instead-of-constants) (regulatory & jurisdiction watch; never auto-applied) · [06 Regulatory & venue watch](../../../docs/06-aggregators-and-market-providers.md#2-final-m2-social--news-ingestion-stack) (sources, how fetched)
- Task type: `REG_CHANGE` in the canonical list ([03 M19](../../../docs/03-build-spec.md#m19-user-task-queue--community-curation--mt_curation), [08](../../../docs/08-airdrops-and-token-launches.md), [D13](../../../docs/ui/dashboards/D13-tasks-curation.md)); stored in `curation.task`, created minimally in P3
- Cross-phase (`depends_on`): P3-T038 (minimal `curation.task`), P3-T031 (residency timeline, decides which foreign authorities are watched), P1-T045 (alert fan-out; until the P5 task queue exists, the review task is also announced by notification)
- Related: P4-T011 (trafilatura/crawl4ai fetcher reused), P4-T008 (scrape NATS account may publish `raw.reg.>`), P4-T064 (venue status watch on the same machinery).

## Requirements

- Source list `config/intel/regwatch.yaml`: per source `authority`, `url`, `kind` (rss | page | headless), `selector` (main content), `cadence` (configurable default: RSS 1 h, pages 24 h), `jurisdiction`, `notify_tax_agent` (bool). Foreign sources carry `active_when: residency_planned(<country>)`.
- Fetch on the `scrape` network: RSS/Atom where offered; otherwise a low-frequency page fetch (trafilatura) or crawl4ai for JS-only pages; robots.txt and site terms respected; declared User-Agent; no logins.
- Fetcher publishes normalised snapshots (text + sha256 + fetched_at) on `raw.reg.{source}`; the core `intel-writer` stores them in `ops.reg_watch_snapshot` (insert-only) and diffs against the previous snapshot.
- Materiality filter: ignore whitespace/date-stamp/boilerplate changes (configurable ignore patterns); a material diff creates one `REG_CHANGE` task in `curation.task` with source, URL, diff summary (added/removed lines), and links to both snapshots, and emits `task.new` + an `alert.info.reg_change` notification.
- Nothing in this path changes a rule, limit, venue status or tax setting; the task text says which command you'd use after review.
- Scraped content is stored `untrusted = true`, provenance-tagged (`train_ok = false` by default), and never sent to a model in P4.

## ToDo

- [ ] `regwatch.yaml` with the AU sources and the dormant UAE/CY/EG entries
- [ ] Prefect flow + fetcher (reusing P4-T011 extraction) publishing `raw.reg.{source}`
- [ ] `ops.reg_watch_source` / `ops.reg_watch_snapshot` migrations and the `intel-writer` handler
- [ ] Differ + materiality filter + `REG_CHANGE` task writer (`curation.task`) + `task.new` / alert
- [ ] Residency-aware activation of foreign sources (reads the P3 residency timeline)
- [ ] Fixtures (two snapshots per source with a real-looking change) and tests
- [ ] Update docs listed under Doc sync

## Verification

### Tests
- Unit: differ ignores boilerplate/date-only changes and flags a changed paragraph.
- Unit: foreign sources inactive unless the residency timeline has a planned period there.
- Integration (diff + task test, R4.15): fixture page v1 → v2 creates exactly one `REG_CHANGE` task with the diff and an alert; v2 → v2 creates none.
- Static check: the regwatch package imports no risk-policy, venue-registry or tax-rule writers.

### Scenarios
- Given ATO updates its crypto guidance page, when the daily fetch runs, then a `REG_CHANGE` task appears in your tasks with the diff, and nothing else changes.
- Given you add a planned move to Cyprus in the residency timeline, then the Cyprus Tax Department and CySEC sources activate on the next run.
- Given a site starts blocking our User-Agent, then the source goes `bad` with an alert; we never spoof or bypass.

### Stress / failure injection
- Replay 30 days of snapshots for all sources in one burst: one task per material change, no duplicates, run < 10 min.

## Acceptance criteria

- [ ] All AU sources fetched on schedule with snapshots stored
- [ ] Diff + task test passes; no rule is ever auto-applied (static check + test)
- [ ] Foreign sources follow the residency timeline
- [ ] CI green (lint, types, tests, `pit` check)

## Exceptions & edge cases

- Page redesigns produce a large diff: one task flagged 'layout change, review selector'.
- Postgres down: snapshots stay in `RAW_REG` (30 d) and are diffed on recovery, in order.

## Cardinal rules (do NOT)

- Do NOT auto-apply any rule, limit, venue or tax change; review tasks only.
- Do NOT log in, solve captchas or break a site's terms or robots.txt.
- Do NOT add paid data/APIs, scraping that breaks a site's terms, self-bots/user tokens, or any sybil/fake engagement.
- Do NOT let Telegram text (or any `model_input_ok = false` row) reach a model, RAG index or training set ([12 §4–5](../../../docs/12-policy-and-compliance.md#4-per-platform-data--automation-rules)).
- Do NOT commit secrets or paste them into chats, issues or logs; they live only in the sops/age file outside the repo ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Do NOT skip, weaken or delete a test to get green.
- Do NOT use unpinned images (`:latest`) or vendored code with telemetry/referral IDs; pin by digest.

## Doc sync on completion

- `docs/06-aggregators-and-market-providers.md`: Regulatory & venue watch: final source list and cadences
- `docs/02-v1-architecture.md`: §5/§6: `ops.reg_watch_*` tables and `raw.reg.{source}` subject
- `docs/roadmap/phase-4-intel.md`: tick T4.30 when P4-T064 is also done

## Branch & PR

- Branch: `p4/P4-T063-regulatory-and-jurisdiction-watch-fetch-diff-and`
- PR title: `P4-T063: Regulatory and jurisdiction watch: fetch, diff and REG_CHANGE review tasks`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P4-T063` run

## Progress log

- 2026-10-22 00:00 · aligner · created for docs/16–17 (R4.15 / T4.30; REG_CHANGE watch per 16 §4.3)
