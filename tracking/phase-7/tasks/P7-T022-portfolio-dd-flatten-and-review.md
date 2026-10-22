---
id: P7-T022
kind: task
title: System drawdown stages on live accounts: stage-2 flatten, 30-day lock, two-strike end
phase: 7
type: BUILD
status: backlog
priority: critical
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P7-T020, P2-T012, P2-T031]
requirements: [R7.06, R7.05]
roadmap_todos: [T7.21]
modules: [M11, M22, M12]
dashboards: [D06, D01, D18]
tools: [git, uv]
mcp: []
env: []
services: [postgres, nats, mt-api]
branch: p7/P7-T022-portfolio-dd-flatten-and-review
pr: ""
doc_sync: [docs/14-strategy-evidence-and-validation.md, docs/03-build-spec.md, docs/roadmap/phase-7-prove-and-go-live.md]
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

# P7-T022 · System drawdown stages on live accounts: stage-2 flatten, 30-day lock, two-strike end

## Goal / expected outcome

The two-stage system drawdown that P2-T012 evaluates on paper works on live sub-accounts: stage 1 (default 10% below the portfolio peak) stops new entries everywhere while exits and protective orders continue; stage 2 (default 25%) flattens every live position to stablecoins/AUD on the venue, halts every sleeve and starts a 30-day review lock; a second stage-2 event ends the trading programme and capital moves to hold-and-earn (a USER task until the P6 treasury exists).

## Context & references

- Roadmap: [R7.06, R7.05 · ToDo T7.21](../../../docs/roadmap/phase-7-prove-and-go-live.md)
- Spec: [14 §7](../../../docs/14-strategy-evidence-and-validation.md#7-phase-capital-steps--kill-criteria-refines-04-phase-7) (stage 2 → flatten to stables + 30-day review; two such events end the programme, capital to hold-and-earn) · [14 §5](../../../docs/14-strategy-evidence-and-validation.md#5-risk-engine-additions-m11) (system stage 1 → no new entries) · [16 §2.1](../../../docs/16-configuration-and-safety-model.md#21-risk-sizing-and-drawdown) (stages, drawdown basis, peak reset) · [17 §B P7-B005](../../../docs/17-decisions-register.md#b-cross-doc-conflicts-one-canonical-answer) · [13 §4](../../../docs/13-wallets-treasury-and-onchain.md#4-hold-and-earn-module-m22-mt_treasury) (M22 hold-and-earn) · [02 §8 flows](../../../docs/02-v1-architecture.md#8-end-to-end-flows) F6
- Cross-phase (`depends_on`): P2-T012 (both system drawdown stages as L1 evaluators on paper; this item extends them to live venues), P2-T031 (kill switch). P6's `mt_treasury` (P6-T038) is **not** required: before it exists the fallback is stables on the venue + a USER task (14 §7 note, [17 §D P7-B011](../../../docs/17-decisions-register.md#d-other-decisions)).
- Related: P7-T020, P7-T048, gap P7-B005 (resolved: two stages, 16 §2.1)

## Requirements

- Drawdown basis (16 §2.1): trading equity in AUD, marked to market every minute (realised + unrealised), excluding the vault and hold-and-earn, adjusted for your deposits and withdrawals, measured from its running peak; the peak resets only after a review lock ends or by a C3 reset.
- Stage 1 (default 10%): new entries rejected everywhere (`system_drawdown_stage1`), exits and protective orders continue, positions keep their resting stops; restart C3. Stage 2 (default 25%): kill switch ON with reason `system_drawdown_stage2`; flatten every live position via marketable limit orders through M11 (protective, never waits for approval); convert non-stable proceeds to the venue's AUD/stablecoin pair where allowed; publish `risk.event`. Stage values are L1 settings (stage 1 < stage 2 enforced at save).
- Review lock: all sleeves `review_30d` for 30 days; turning kill OFF before day 30 is refused; after day 30, restart is C3 with a written review (`risk.review.close`).
- Strike counter persisted in `risk.programme_state` (WORM); second stage-2 event → programme `ended`: live modes disabled. Clearing it is a loosening of the L1 system policy, only via `risk.policy.update` (C3) with a written reason, recorded WORM; there is no other path ([17 §E](../../../docs/17-decisions-register.md#e-ratification-2026-10-22): no host-only file).
- Hold-and-earn routing is a **task** for you (transfers are manual, 07 §3) plus a treasury proposal in D18 if M22 exists.

## ToDo

- [ ] Live equity/peak feed for the P2-T012 system-drawdown evaluator (live venue balances + mark-to-market, cash-flow adjusted).
- [ ] Flatten-to-stables routine using existing `position.close` paths via M11.
- [ ] Review lock + strike counter (WORM) + `risk.review.close` (C3).
- [ ] `programme_ended` flag in the L1 system policy; clearing only via `risk.policy.update` (C3).
- [ ] D01 banner and the lock-countdown data for the D06 Live tab (P7-T067); Telegram critical alert.
- [ ] Tests; docs.

## Verification

### Tests
- Unit: 9.9% vs 10.1% (stage 1: entries rejected, exits pass); 24.9% vs 25.1% (stage 2); peak tracking with deposits/withdrawals excluded (cash-flow adjusted); peak resets only after the lock ends or a C3 reset.
- Integration (paper venues): breach flattens all positions, converts to stables, kill ON, lock set; kill OFF refused until day 30 (clock-injected).
- Integration: second strike sets `programme_ended`; `bot.set_mode` live refused; clearing it without C3 refused.

### Scenarios
- Given DD reaches 25.3% overnight, then by the next minute all live positions are being closed and you get a critical alert on three channels.
- Given day 31 and a written review, when you approve `risk.review.close` (C3), then sleeves return to `halted` (not live) and must restart individually.

### Stress / failure injection
- Venue disconnect during flatten: positions marked unconfirmed; retries with backoff; resting broker-side stops remain; alert every 60 s until flat or reconciled.

## Acceptance criteria

- [ ] Stage 1 blocks entries; stage 2 → flatten + lock + alert, verified on paper venues.
- [ ] Two-strike end enforced; cleared only by C3 with a reason.
- [ ] CI green.

## Exceptions & edge cases

- Deposits/withdrawals: the basis is adjusted for cash flows, so a manual withdrawal is not a drawdown (16 §2.1).
- Venue without stable pair: flatten to AUD cash.
- Clock: 30 days measured in UTC from breach time.

## Cardinal rules (do NOT)

- Do NOT let anything but a C3 `risk.policy.update` with a reason clear the programme-ended flag; never reset the strike counter.
- Do NOT move funds off venues automatically.
- Do NOT add discretionary overrides; the only manual trading action outside HITL approvals is flatten-and-halt with a required reason (14 §4).
- Do NOT let loosening risk, autonomous mode or a capital step apply without C3 (Telegram + TOTP + cool-down); protective exits never wait for approval.
- Do NOT update or delete WORM rows; corrections are new rows with `supersedes_id` (15 §2).
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order goes through M11.
- Do NOT use keys that are not trade-only, IP-locked and withdrawal-disabled; no live money before the P7 gates pass.
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.

## Doc sync on completion

- `docs/14-strategy-evidence-and-validation.md` §7: DD basis and lock mechanics.
- `docs/03-build-spec.md` M11: live stage-2 flatten and lock mechanics.
- `docs/roadmap/phase-7-prove-and-go-live.md`: tick T7.21 when this item is done.

## Branch & PR

- Branch: `p7/P7-T022-portfolio-dd-flatten-and-review`
- PR title: `P7-T022: System drawdown stages on live accounts: stage-2 flatten, 30-day lock, two-strike end`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P7-T022` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (two-stage system drawdown 10%/25% on the 16 §2.1 basis (17 §B P7-B005); extends P2-T012; programme-ended cleared only by C3 (17 §E, no host file); P6 treasury not required)
