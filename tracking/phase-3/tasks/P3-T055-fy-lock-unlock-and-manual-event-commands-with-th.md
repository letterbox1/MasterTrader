---
id: P3-T055
kind: task
title: FY lock/unlock and manual-event commands with the residency-change contract
phase: 3
type: BUILD
status: backlog
priority: high
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P3-T005, P3-T008, P0-T034, P0-T035, P2-T016, P2-T019]
requirements: [R3.16, R3.02, R3.09]
roadmap_todos: [T3.32]
modules: [M18, M11, mt_api]
dashboards: [D14, D15]
tools: [git, uv, docker]
mcp: []
env: []
services: [postgres, nats, mt-api]
branch: p3/P3-T055-fy-lock-unlock-and-manual-event-commands-with-th
pr: ""
doc_sync: [docs/02-v1-architecture.md, docs/09-journal-and-tax.md, docs/roadmap/phase-3-journal-and-tax.md]
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

# P3-T055 · FY lock/unlock and manual-event commands with the residency-change contract

## Goal / expected outcome

`mt_api` has the three journal/tax commands decided in 17 §D (P3-B006/B007): `tax.fy.lock` / `tax.fy.unlock` (C3) and `journal.manual_event.add` (C2), and the residency-change contract works end to end: a residency change emits `tax.residency.changed`, the venue registry recomputes, tightening applies at once, and any loosening that results waits for C3. `task.answer` (C1) completes the R3.16 command set and is delivered with the `curation.task` store in P3-T038.

## Context & references

- Roadmap: [R3.16, T3.32](../../../docs/roadmap/phase-3-journal-and-tax.md) · verified by P3-T058 (T3.65)
- Commands: [02 §7.2](../../../docs/02-v1-architecture.md#72-commands-rest-write) (Journal & tax row; `task.answer` C1) · [09 Commands](../../../docs/09-journal-and-tax.md#architecture) · D15 actions [D15](../../../docs/ui/dashboards/D15-tax.md) (lock/unlock C3, unlock needs a reason) · D14 manual event (C2, reason required) [D14](../../../docs/ui/dashboards/D14-journal.md)
- Residency contract: `tax.residency.changed` in [02 §6](../../../docs/02-v1-architecture.md#6-messaging-nats) and flow step 7 in [02 §8](../../../docs/02-v1-architecture.md#8-end-to-end-flows) · [12 §1 moving countries](../../../docs/12-policy-and-compliance.md#1-australian-boundary-the-load-bearing-assumption) · [12 §2 venue registry](../../../docs/12-policy-and-compliance.md#2-venue-access-registry) · [09 Egypt finding](../../../docs/09-journal-and-tax.md#️-key-findings-that-shape-the-design)
- Confirmation levels: [17 §D P0-B003](../../../docs/17-decisions-register.md#d-other-decisions) (C2 = risk-preview hash bound to the command + session re-authenticated within 12 h; C3 = C2 + Telegram approve + TOTP + cool-down) · C3 cool-down 15 min default [16 §2.3](../../../docs/16-configuration-and-safety-model.md#23-decisions-approvals-and-hitl)
- Decisions: [17 §D P3-B006, P3-B007](../../../docs/17-decisions-register.md#d-other-decisions)
- Cross-phase prerequisites (depends_on): P0-T034 (command bus + `audit.command`), P0-T035 (C0–C3 engine), P2-T016 (M11 venue-registry check), P2-T019 (change-control service: tighten/loosen classifier and C3 flow)
- Related: P3-T031 (timeline + `tax.residency.add` publishes the event), P3-T033 (Egypt block via the recompute), P3-T038 (`task.answer`), P3-T021 (manual opening lots use `journal.manual_event.add`), P3-T019/T025 (lot select and regime set refused in a locked FY)

## Requirements

- **`tax.fy.lock` (C3)** and **`tax.fy.unlock` (C3, reason required):** each writes a `journal.fy_lock` row (WORM: FY, action lock|unlock, reason, command id, ts); the current state = latest row per FY. Typical trigger: you mark an FY report "lodged" in D15.
- **Locked-FY effect:** while an FY is locked, new events whose taxpayer-local date falls in it are **not dropped**: the writer (P3-T008) appends them to `journal.ingest_held` (append-only, reason `fy_locked`), raises `alert.warning.fy_locked_event`, and they are released in order after a C3 unlock. `tax.lot.select`, `tax.regime.set`, retroactive `tax.residency.add` and `journal.manual_event.add` for that FY return 423 problem+json naming the unlock path. Report generation stays allowed (read-only).
- **`journal.manual_event.add` (C2, reason required):** the only way to add an off-system event (opening lot, off-platform transfer); payload is a `JournalEvent` with `source = manual`, optional evidence attachment (content-addressed under `data/attachments/`, referenced by hash, P3-T039), validated by the same normaliser and FX/valuation stamping (P3-T011) as adapters; recorded in `audit.command`. Never direct SQL.
- **`tax.residency.changed` contract:** msgspec schema `mt_core.schemas.ResidencyChanged` v1 {`residency_version`, `periods_before`, `periods_after`, `effective_from`, `command_id`}; published by `journal` after the residency row commits (P3-T031).
- **Venue-registry recompute:** an `mt-api` consumer applies the per-country registry rules (12 §2: venue/product status per residency, e.g. EG → crypto products `blocked`) to produce a proposed registry diff. Tightening entries apply immediately (`venue.registry.changed`); loosening entries (status moves towards `allowed`, a block removed) become a C3 change request through the P2 change-control service and apply only after approval + TOTP + cool-down.
- **Fail closed while recomputing:** the registry records the `residency_version` it last applied; M11 (P2-T016) rejects new entries on products whose rules depend on residency while the registry's applied version is behind the latest `tax.residency.changed`; protective exits (reduce-only) always pass.
- Levels are enforced server-side; every command and its approval is in `audit.command`. Numbers (cool-down, re-auth window) come from config defaults (16 §2.3), never constants.

## ToDo

- [ ] Migration `journal_0004_fy_lock` (`journal.fy_lock`, `journal.ingest_held`), registered with the WORM helper
- [ ] Command handlers `packages/mt_api/commands/tax_fy.py` (`tax.fy.lock`/`unlock`) and `journal_manual.py` (`journal.manual_event.add`) with C-levels in the command registry
- [ ] Locked-FY guard shared by the writer and the lot/regime/residency handlers (`mt_journal.fylock.guard`)
- [ ] Held-event release job on unlock (ordered, idempotent)
- [ ] `ResidencyChanged` schema in `packages/mt_core/schemas/tax.py`; registry recompute consumer `packages/mt_api/consumers/residency.py`; tighten/loosen split via the change-control service
- [ ] Registry `applied_residency_version` + M11 fail-closed hook for residency-dependent products
- [ ] Unit + integration tests (see Verification); docs

## Verification

### Tests
- Unit: `tax.fy.lock` without C3 approval → refused; with approval → lock row written after the cool-down; `tax.fy.unlock` without reason → 422.
- Unit: an event dated in a locked FY goes to `journal.ingest_held`, not `journal.event`; after unlock it is released exactly once.
- Unit: `journal.manual_event.add` without a valid C2 preview hash or with a stale session (> 12 h) → refused; valid → event with `source = manual` and an `audit.command` row.
- Integration: publish `tax.residency.changed` adding EG → registry tightens immediately; publish one removing EG → a pending C3 change request, registry unchanged until approval.

### Scenarios
- Given FY2026-27 is locked, when a late funding payment for June 2027 arrives, then it is held, an alert fires, and D15 shows "1 held event"; after a C3 unlock with a reason it lands in the journal and reports regenerate as new rows.
- Given a residency change is saved, when the registry has not yet applied it, then M11 rejects new entries on residency-dependent products and allows reduce-only exits.
- Given a residency change would remove a block, when you approve via Telegram + TOTP, then the registry loosens only after the 15 min (default) cool-down.

### Stress / failure injection
- Kill `mt-api` between the residency commit and the registry recompute: on restart the consumer replays `tax.residency.changed` (durable) and M11 stays fail-closed until it applies.
- 1,000 held events released after unlock: ordered, no duplicates, < 60 s.

## Acceptance criteria

- [ ] `tax.fy.lock`/`unlock` (C3) and `journal.manual_event.add` (C2) live with server-side levels and audit rows
- [ ] Locked FY holds new events and refuses lot/regime/residency/manual changes until a C3 unlock
- [ ] `tax.residency.changed` emitted, registry recomputed; loosening only via C3, tightening immediate
- [ ] M11 fails closed for residency-dependent products while the recompute is pending
- [ ] CI green (lint, types, tests, `pit` check; `tax-golden` once P3-T045 lands)

## Exceptions & edge cases

- Unlock requested while held events exceed the JetStream/held bound → release proceeds in batches; nothing is dropped (R3.N3, P3-T057).
- C3 path unavailable (Telegram down) → the host break-glass `mtctl approve <id>` + TOTP is used only until Telegram C3 exists ([17 §D P0-B002](../../../docs/17-decisions-register.md#d-other-decisions)); afterwards C3 waits.
- Residency change with no registry effect → event still emitted and logged; no change request.

## Cardinal rules (do NOT)

- Do NOT let a residency edit, an FY unlock or any registry loosening skip C3; protective exits never wait for approval.
- Do NOT drop or discard events for a locked FY; hold them.
- Do NOT add manual events by SQL; only `journal.manual_event.add`.
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order goes through M11.
- Do NOT UPDATE or DELETE `journal.*` (WORM) rows; corrections are new rows referencing the superseded row ([15 §2](../../../docs/15-bots-hitl-and-worm-audit.md#2-worm-records-write-once-read-many)).
- Do NOT hard-code cool-downs or re-auth windows; read the configured defaults ([16 §2.3](../../../docs/16-configuration-and-safety-model.md#23-decisions-approvals-and-hitl)).
- Do NOT commit secrets or paste them into chats/issues; secrets live only in the sops/age file ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Do NOT skip, weaken or delete a test to get green.

## Doc sync on completion

- `docs/02-v1-architecture.md` §6/§7.2: confirm the `ResidencyChanged` payload and the held-event behaviour for locked FYs.
- `docs/09-journal-and-tax.md` Commands: add the locked-FY holding rule.
- `docs/roadmap/phase-3-journal-and-tax.md`: tick T3.32 once every item mapped to it is done.

## Branch & PR

- Branch: `p3/P3-T055-fy-lock-unlock-and-manual-event-commands-with-th`
- PR title: `P3-T055: FY lock/unlock and manual-event commands with the residency-change contract`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P3-T055` run

## Progress log

- 2026-10-22 00:00 · aligner · created for R3.16/T3.32 (docs/16–17 alignment; closes the implementation side of P3-B006/P3-B007)
