---
id: P1-T021
kind: task
title: Stream Alpaca IEX real-time trades and quotes for 30 symbols
phase: 1
type: BUILD
status: backlog
priority: high
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P1-T005, P1-T006, P1-T007, P1-T009]
requirements: [R1.05]
roadmap_todos: [T1.34]
modules: [M1]
dashboards: [D02, D07]
tools: [git, uv, docker]
mcp: []
env: []
services: [nats]
branch: p1/P1-T021-alpaca-iex-realtime-stream
pr: ""
doc_sync: [docs/roadmap/phase-1-data-and-monitoring.md, docs/03-build-spec.md]
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

# P1-T021 · Stream Alpaca IEX real-time trades and quotes for 30 symbols

## Goal / expected outcome

The Alpaca Basic (free) IEX WebSocket streams trades and quotes for up to 30 universe stocks/ETFs into `md.alpaca.{symbol}.trade|quote`, flagged as IEX (not NBBO).

## Context & references

- Roadmap: requirements [R1.05](../../../docs/roadmap/phase-1-data-and-monitoring.md#3-requirements) · ToDo [T1.34](../../../docs/roadmap/phase-1-data-and-monitoring.md#4-todo-sets)
- Spec: [03 M1](../../../docs/03-build-spec.md#m1-market--macro-data--mt_datamarket) (Alpaca Basic, real-time IEX, 30 WebSocket symbols) · [03 §6](../../../docs/03-build-spec.md#6-smallest-free-timeframe-by-asset-class) (IEX ≠ NBBO: fine for swing, weak for scalping cost measurement) · [phase 1 §7 risks](../../../docs/roadmap/phase-1-data-and-monitoring.md#7-risks--open-questions)
- Roadmap ToDo T1.34 now names the Alpaca real-time stream (gap P1-B003 closed)
- Build first, keys last ([17 §E](../../../docs/17-decisions-register.md#e-ratification-2026-10-22)): built keyless against fixtures in Alpaca's documented message format; the live IEX stream is checked with your paper keys in P1-T073
- Depends on (this phase): P1-T005, P1-T006, P1-T007, P1-T009

## Requirements

- Market-data WS `v2/iex` with paper keys from the secrets file at runtime (none in CI); subscribe trades + quotes (+ minute bars as a cross-check)
- Hard cap 30 symbols enforced by config validation and at subscribe time
- Every message tagged `feed=iex`; D02 shows an "IEX only, not NBBO" badge (P1-T050)
- Session-aware: pre/post-market flagged; stale suppression outside sessions via `exchange_calendars`

## ToDo

- [ ] Implement the Alpaca stream connector (alpaca-py pinned, or thin client)
- [ ] Enforce the 30-symbol cap and surface it in D07 quotas
- [ ] Golden fixtures; tests; docs
- [ ] Update the docs listed under Doc sync and tick the roadmap ToDo box(es)

## Verification

### Tests

- Unit: message parsing (trades, quotes, bars); cap enforcement
- Integration: golden replay; auth failure reported as `auth_failed` feed status

### Scenarios

- Given 31 symbols configured, when the connector starts, then it refuses with a clear error and D07 shows the quota breach
- Given the US market is closed, when no messages arrive, then no stale incident is raised

### Stress / failure injection

- Burst: replay the US open (first 5 min) at 5× speed; publish p99 < 50 ms

## Acceptance criteria

- [ ] Golden replay passes keyless with the IEX flag on every message; the live check during US hours runs in P1-T073
- [ ] CI green (ruff, mypy, pytest, `pit` bypass check, gitleaks)

## Exceptions & edge cases

- Alpaca allows one market-data WS connection on the free plan; reconnect must close the old one first
- Symbols halted (LULD) are not stale: mark `halted` when Alpaca sends status updates

## Cardinal rules (do NOT)

- Do NOT commit secrets or paste them into chats, issues, logs or test fixtures; credentials come only from the sops/age secrets file (kept outside the repo) mounted on tmpfs ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Do NOT use keys with withdrawal rights, or without an IP allow-list where the venue supports one; practice/testnet/paper only, no live money before the P7 gates.
- Do NOT place, modify or cancel orders from this code; P1 is read-only toward venues (orders arrive in P2 through M11).
- Do NOT skip, weaken or delete a test (or widen a tolerance) to get CI green.
- Do NOT add paid data or APIs, exceed a free tier, or scrape against a site's terms; no self-bots or user tokens ([03 §1](../../../docs/03-build-spec.md#1-ground-rules)).

## Doc sync on completion

- `docs/roadmap/phase-1-data-and-monitoring.md`: tick T1.34 once every task traced to it in PHASE.md is done; note P1-T021 next to it.
- `docs/03-build-spec.md` §M1: note the enforced 30-symbol cap

## Branch & PR

- Branch: `p1/P1-T021-alpaca-iex-realtime-stream`
- PR title: `P1-T021: Stream Alpaca IEX real-time trades and quotes for 30 symbols`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P1-T021` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (traced to new T1.34 (P1-B003 closed); keyless build, live stream in P1-T073)
