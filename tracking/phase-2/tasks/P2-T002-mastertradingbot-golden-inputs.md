---
id: P2-T002
kind: task
title: Provide MasterTradingBot rules and historical outputs for golden files
phase: 2
type: USER
status: backlog
priority: high
size: M
severity: ""
owner: user
claimed_by: ""
depends_on: []
requirements: [R2.48]
roadmap_todos: [T2.04]
modules: [M0]
dashboards: []
tools: []
mcp: []
env: []
services: [mt5-terminal]
branch: p2/P2-T002-mastertradingbot-golden-inputs
pr: ""
doc_sync: [docs/14-strategy-evidence-and-validation.md, docs/roadmap/phase-2-strategies-risk-lab.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-22
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
review_result: ""
---

# P2-T002 · Provide MasterTradingBot rules and historical outputs for golden files

## Goal / expected outcome

The rule descriptions and historical signal/trade outputs of your MasterTradingBot strategies are exported into a private, git-ignored fixtures folder so Part B can build the shared indicator/sizing libraries and their golden-file tests (R2.48, T2.31, T2.67).

## Context & references

- Roadmap: [R2.48](../../../docs/roadmap/phase-2-strategies-risk-lab.md) · ToDo T2.04
- Spec: [14 §8 MasterTradingBot integration](../../../docs/14-strategy-evidence-and-validation.md#8-mastertradingbot-integration)
- Consumers: P2-T130/P2-T131 (shared libraries), P2-T133 (golden-file check, T2.67).

## Requirements

- Per strategy: a plain-English rule description (indicators + parameters, entry/exit triggers, stop/target logic, sizing, session filters, instrument list).
- Historical outputs: per bar/tick signal values and trades (timestamp UTC, instrument, side, size, price, SL/TP) for ≥ 3 months per strategy, as CSV/Parquet.
- The matching input price data (or the exact FP Markets symbol + timeframe so it can be re-fetched) so goldens are reproducible.
- Timezone/bar-close convention of MT5 (server time offset) recorded per file.

## ToDo

- [ ] Export from MT5 (Strategy Tester or live journal) the signal/trade history per strategy
- [ ] Write `rules.md` per strategy (no account numbers or credentials)
- [ ] Place files under `tests/fixtures/mastertradingbot/<strategy>/` (path is git-ignored via `.gitignore` entry `tests/fixtures/mastertradingbot/`) or in the encrypted data share named in the progress log
- [ ] Note the MT5 server timezone offset and any broker symbol suffixes
- [ ] Record completion in the progress log (no secrets) and run `./kanban done P2-T002`

## Verification

### Tests
- Part B's golden harness loads every file and reproduces ≥ 1 signal per strategy before full golden runs.

### Scenarios
- Given the exported files, when Part B's library computes EMA/ATR on the same input bars, then values match within the tolerance agreed in the golden test.

### Stress / failure injection
- n/a: data hand-over.

## Acceptance criteria

- [ ] Every MasterTradingBot strategy you want ported has rules + ≥ 3 months of outputs + inputs
- [ ] No account numbers, passwords or broker credentials in any file

## Exceptions & edge cases

- If MT5 history is shorter than 3 months for a strategy, provide what exists and flag it.
- Proprietary rule text stays out of any LLM prompt unless you say otherwise.

## Cardinal rules (do NOT)

- Do NOT include FP Markets credentials, account numbers or statements.
- Do NOT commit secrets or paste them into chats/issues/logs; secrets live in the sops/age file (07 §2).

## Doc sync on completion

- `docs/14-strategy-evidence-and-validation.md` §8: list which strategies have golden inputs.
- `docs/roadmap/phase-2-strategies-risk-lab.md`: tick T2.04 when all tasks mapped to it are done.

## Branch & PR

- Branch: `p2/P2-T002-mastertradingbot-golden-inputs` (only if a repo change results, e.g. non-secret config or manifests; secrets never go in git)
- PR title: `P2-T002: Provide MasterTradingBot rules and historical outputs for golden files`
- PR checklist: no secrets in diff (gitleaks clean) · task file ticked · `./kanban done P2-T002` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (front-matter run fields; consumer links fixed)
