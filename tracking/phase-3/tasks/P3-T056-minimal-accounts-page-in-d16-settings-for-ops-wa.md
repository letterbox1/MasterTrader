---
id: P3-T056
kind: task
title: Minimal Accounts page in D16 settings for ops.wallets
phase: 3
type: BUILD
status: backlog
priority: high
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P3-T012, P0-T048, P0-T049, P0-T052]
requirements: [R3.17, R3.04]
roadmap_todos: [T3.33]
modules: [M18, web, mt_api]
dashboards: [D16]
tools: [git, node>=20, pnpm, uv, docker]
mcp: []
env: []
services: [postgres, mt-api]
branch: p3/P3-T056-minimal-accounts-page-in-d16-settings-for-ops-wa
pr: ""
doc_sync: [docs/ui/dashboards/D16-system.md, docs/roadmap/phase-3-journal-and-tax.md]
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

# P3-T056 · Minimal Accounts page in D16 settings for ops.wallets

## Goal / expected outcome

D16 Settings has an **Accounts** section where you list, register and tag every exchange/broker account and on-chain address in `ops.wallets` (`investment` / `trading`, venue, residency use) through `wallet.register` / `wallet.tag` (C1), or load the seed file through `mt_api`, so the USER task P3-T042 can be done on screen instead of by hand-editing YAML. D18 extends this page in Phase 5.

## Context & references

- Roadmap: [R3.17, R3.04, T3.33](../../../docs/roadmap/phase-3-journal-and-tax.md)
- Spec: [D16 Settings → Accounts (Phase 3)](../../../docs/ui/dashboards/D16-system.md) · backend `/wallets?kind=account`, commands `wallet.register` / `wallet.tag` (C1) in [02 §7.2](../../../docs/02-v1-architecture.md#72-commands-rest-write)
- Registry: [09 goals §6–7](../../../docs/09-journal-and-tax.md#goals) · [13 §3](../../../docs/13-wallets-treasury-and-onchain.md#3-unified-wallet-view) · decision [17 §D P3-B011](../../../docs/17-decisions-register.md#d-other-decisions) and [17 §B](../../../docs/17-decisions-register.md#b-cross-doc-conflicts-one-canonical-answer) (one registry `ops.wallets`, created in P3)
- Viewport matrix [DESIGN §6.8](../../../DESIGN.md#68-test-matrix-every-screen-must-pass) · settings pattern [ui §3.7](../../../docs/ui/README.md#37-settings-show-configurable-defaults-and-their-layer)
- Cross-phase prerequisites (depends_on): P0-T048 (typed API + WS client), P0-T049 (component library, confirm sheets), P0-T052 (D16 Audit/Security/Settings pages)
- Related: P3-T012 (registry, commands, seed loader), P3-T042 (your registration), P5 D18 (extends the page)

## Requirements

- Route `/system/settings/accounts` (a section of `/system/settings`): table of `ops.wallets` rows (kind, venue/chain, masked account id or public address, provider label, role, custody, account mode paper/live, current tag + effective date, residency use) with the tag history drawer (`journal.account_tag`).
- **Register** form → `wallet.register` (C1, confirm sheet showing the exact row); **Tag** form → `wallet.tag` (C1; `investment` | `trading`, effective-from date; mid-FY change shows the D15 warning text from P3-T012).
- **Load seed file** → uploads `accounts.yaml` to `mt_api`, which validates it and issues the same `wallet.register`/`wallet.tag` commands (preview of the diff first, one C1 confirm for the batch is **not** allowed: each row is confirmed, matching "no bulk approve" in 17 §D).
- Validation: account ids must be masked (last 4 only), addresses are public addresses; anything that looks like a key, seed phrase or full account number is rejected client- and server-side with a reason; nothing secret is ever rendered or logged (D16 acceptance 2).
- Layout tiers: ≥ xl table + side form; md–lg table + drawer; ≤ ph cards + full-screen form. Empty state explains why registration matters (internal transfers are never disposals).
- Unknown-account quarantine count (from P3-T012) shown with a link to D14 so you can see what still needs registering.

## ToDo

- [ ] Query endpoint `/wallets?kind=account` (and `kind=address`) + tag history in `packages/mt_api/routers/wallets.py` if not already exposed by P3-T012
- [ ] Seed-file upload endpoint with diff preview (reuses the P3-T012 loader logic)
- [ ] Route + components in `apps/web/src/routes/system/settings/accounts/*` (table, register/tag forms, confirm sheets)
- [ ] Secret-pattern validator shared by UI and API
- [ ] Vitest + Playwright (viewport matrix + axe) tests; docs

## Verification

### Tests
- Vitest: masked-id validator rejects a 12-digit account number and a 12-word phrase; accepts `****1234`.
- Playwright: register an address, tag it `investment`, see it in the table with the C1 confirm recorded; viewport matrix 240×320 → 2560×1440 with overflow checks; axe no serious violations.
- API: `wallet.register` without the C1 confirm token → refused; seed upload with a secret-looking value → 422 with the line number.

### Scenarios
- Given an unknown-account quarantine item, when you register that account here, then the item is re-processed and the count drops to 0.
- Given you change an account's tag mid-FY, when saved, then the history shows both rows and D15 shows the split-year warning.
- Given Postgres is down, when the page opens, then it is read-only with the red system banner (02 §9.3).

### Stress / failure injection
- Table with 500 registry rows stays responsive (virtualised); seed upload of 200 rows previews in < 2 s.

## Acceptance criteria

- [ ] Accounts section lists, registers and tags `ops.wallets` entries via C1 commands
- [ ] Seed-file load goes through `mt_api` with a preview; no direct SQL
- [ ] No secret, full account number or seed phrase can be entered or shown
- [ ] Viewport matrix + axe green in CI
- [ ] CI green (lint, types, tests)

## Exceptions & edge cases

- An address registered twice (same chain + address) → server returns the existing row; no duplicate.
- An account later found not to be yours → a superseding row with `owner = not_self` (P3-T012), never a delete.
- P5 D18 adds roles, balances and approvals; this page must not block those additive columns (render unknown columns generically).

## Cardinal rules (do NOT)

- Do NOT accept or display API keys, seed phrases or full account numbers.
- Do NOT write `ops.wallets` or `journal.account_tag` outside `wallet.register` / `wallet.tag`.
- Do NOT add bulk confirmation for registry changes.
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order goes through M11.
- Do NOT commit secrets or paste them into chats/issues; secrets live only in the sops/age file ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.

## Doc sync on completion

- `docs/ui/dashboards/D16-system.md`: Accounts section — confirm fields and actions as built.
- `docs/roadmap/phase-3-journal-and-tax.md`: tick T3.33 once every item mapped to it is done.

## Branch & PR

- Branch: `p3/P3-T056-minimal-accounts-page-in-d16-settings-for-ops-wa`
- PR title: `P3-T056: Minimal Accounts page in D16 settings for ops.wallets`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P3-T056` run

## Progress log

- 2026-10-22 00:00 · aligner · created for R3.17/T3.33 (docs/16–17 alignment; implementation owner for P3-B011)
