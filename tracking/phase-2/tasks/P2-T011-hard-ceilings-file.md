---
id: P2-T011
kind: task
title: Hard-ceilings file reader that no API can write
phase: 2
type: BUILD
status: backlog
priority: critical
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P2-T010]
requirements: [R2.19]
roadmap_todos: [T2.24]
modules: [M11]
dashboards: [D06]
branch: p2/P2-T011-hard-ceilings-file
pr: ""
doc_sync: [docs/07-security-notes.md, docs/03-build-spec.md, docs/roadmap/phase-2-strategies-risk-lab.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P2-T011 · Hard-ceilings file reader that no API can write

## Goal / expected outcome

Absolute risk ceilings are read from a host file (`/etc/mastertrader/risk-ceilings.yaml`, root-owned, mounted read-only) that no API, command or container can write; any policy value beyond a ceiling is rejected and every check clamps to it.

## Context & references

- Roadmap: [R2.19](../../../docs/roadmap/phase-2-strategies-risk-lab.md) · ToDo T2.24
- Spec: [03 M11 change control](../../../docs/03-build-spec.md#m11-risk-manager--mt_risk-built-in-user-inputs-via-uitelegram-later-mcp) · [07 §6 application controls](../../../docs/07-security-notes.md#6-application-controls) · Flow: [02 F5](../../../docs/02-v1-architecture.md#8-end-to-end-flows)
- UI: [D06 ceilings shown read-only with a lock](../../../docs/ui/dashboards/D06-risk.md)
- Related: P2-T048 (you write the file), P2-T019 change control, P2-T053 C3 tests.

## Requirements

- File schema `mt.risk-ceilings/v1`: per-field maxima mirroring policy fields (e.g. `global.max_daily_loss_pct`, `global.max_leverage`, `crypto_derivatives.max_leverage: 2`, `sleeve.*.max_drawdown_pct`, `per_trade.max_risk_pct`).
- Mounted `:ro` into `engine` and `mt-api` only; host perms `root:root 0644`; containers run as non-root.
- On load: validate schema, compute sha256, log + publish `risk.event{type: ceilings_loaded, hash}`; change detection via inotify → reload + alert (the file is changed by you on the host only).
- Missing/invalid file → default-deny all new orders + critical alert (protective exits still allowed).
- No route, command, MCP tool or Telegram command writes this path; a CI test greps the codebase for writes to it and scans the OpenAPI for any ceilings write.

## ToDo

- [ ] `packages/mt_risk/ceilings.py` loader, validator, watcher
- [ ] Compose mounts (`:ro`) for engine and mt-api
- [ ] Expose read-only values to `/risk/policy` responses (for D06 lock icons)
- [ ] CI guard test
- [ ] Tests
- [ ] Update the docs listed under *Doc sync on completion* and tick the roadmap ToDo box(es) once every task mapped to them is done

## Verification

### Tests
- Unit: policy value above ceiling → `CeilingExceeded`.
- Unit: missing file → `trading_allowed=false`, reason `ceilings_missing`.
- Integration: container attempting to write the mounted file gets EROFS.
- CI: static scan finds no write path; OpenAPI has no ceilings mutation.

### Scenarios
- Given ceiling max leverage 2× for crypto derivatives, when a policy update sets 3×, then it is rejected regardless of C3.
- Given you lower a ceiling on the host below the current policy value, when reloaded, then checks clamp to the new ceiling immediately and D06 flags the policy field as above ceiling.

### Stress / failure injection
- Corrupt the file mid-run (truncate): watcher flags invalid, trading new entries halts within 1 s, alert fires.

## Acceptance criteria

- [ ] Read-only mount in place and tested
- [ ] Ceilings enforced in both policy updates and runtime checks
- [ ] No write path exists (CI guard)
- [ ] CI green: ruff, mypy, pytest (and the `mt_risk` golden suite, `pit` check, viewport matrix where relevant)

## Exceptions & edge cases

- File edited while orders in flight: in-flight orders already checked are not cancelled; next check uses new values.
- Clock: watcher debounce 500 ms to avoid partial writes.

## Cardinal rules (do NOT)

- Do NOT add any API, command, UI or Telegram path that writes the ceilings file.
- Do NOT ship a default ceilings file in git with live values; ship only a schema + example with obviously-safe numbers.
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order goes through M11, whatever its source.
- Do NOT commit secrets or paste them into chats/issues/logs; secrets live in the sops/age file (07 §2).
- Do NOT skip, weaken or delete a test to get green; risk-manager golden tests are mandatory for merge.
- Loosening risk, autonomous mode and mandates are C3 (Telegram approve + TOTP + cool-down); protective exits never wait for approval.

## Doc sync on completion

- `docs/07-security-notes.md` §6: record the file path and permissions.
- `docs/03-build-spec.md` M11: reference the ceilings schema.
- `docs/roadmap/phase-2-strategies-risk-lab.md`: tick T2.24 when all tasks mapped to it are done.

## Branch & PR

- Branch: `p2/P2-T011-hard-ceilings-file`
- PR title: `P2-T011: Hard-ceilings file reader that no API can write`
- PR checklist: tests added and green · docs synced · task file ticked · no secrets (gitleaks) · `./kanban done P2-T011` run

## Progress log

- 2026-10-21 00:00 · planner · created
