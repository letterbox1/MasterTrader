---
id: P7-T022
kind: task
title: Portfolio DD > 25%: flatten to stables, 30-day review, two-strike end
phase: 7
type: BUILD
status: backlog
priority: critical
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P7-T020]
requirements: [R7.06, R7.05]
roadmap_todos: [T7.21]
modules: [M11, M22, M12]
dashboards: [D06, D01, D18]
branch: p7/P7-T022-portfolio-dd-flatten-and-review
pr: ""
doc_sync: [docs/14-strategy-evidence-and-validation.md, docs/03-build-spec.md, docs/roadmap/phase-7-prove-and-go-live.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P7-T022 · Portfolio DD > 25%: flatten to stables, 30-day review, two-strike end

## Goal / expected outcome

If total portfolio drawdown from peak exceeds 25%, the system flattens all trading positions to stablecoins/AUD cash on venue, halts every sleeve, enters a 30-day review lock; a second such event ends the trading programme and routes capital to hold-and-earn.

## Context & references

- Roadmap: [R7.06, R7.05 · ToDo T7.21](../../../docs/roadmap/phase-7-prove-and-go-live.md)
- Spec: [14 §7](../../../docs/14-strategy-evidence-and-validation.md#7-phase-capital-steps--kill-criteria-refines-04-phase-7) (portfolio DD > 25% → flatten to stables + 30-day review; two such events end the programme, capital to hold-and-earn) · [14 §5](../../../docs/14-strategy-evidence-and-validation.md#5-risk-engine-additions-m11) (system DD 10% halt) · [13 §4](../../../docs/13-wallets-treasury-and-onchain.md#4-hold-and-earn-module-m22-mt_treasury) (M22 hold-and-earn) · [02 §8 flows](../../../docs/02-v1-architecture.md#8-end-to-end-flows) F6
- Cross-phase: P6 T6.28 (`mt_treasury`) for the hold-and-earn destination; P2 T2.23 kill switch.
- Related: P7-T020, P7-T048, gap P7-B005 (interaction with the 10% system halt)

## Requirements

- Portfolio DD computed on total trading equity (all live sleeves + venue cash, AUD, mark-to-market every minute; excludes vault/hold-and-earn).
- Breach: kill switch ON with reason `portfolio_dd_25`; flatten every live position via marketable limit orders through M11 (protective, never waits for approval); convert non-stable proceeds to the venue's AUD/USD stable where allowed; publish `risk.event`.
- Review lock: all sleeves `review_30d` for 30 days; turning kill OFF before day 30 is refused; after day 30, restart is C3 with a written review (`risk.review.close`).
- Strike counter persisted in `risk.programme_state` (WORM); second strike → programme `ended`: live modes disabled permanently; re-enabling requires editing the hard-ceilings file on the host (not via any API).
- Hold-and-earn routing is a **task** for you (transfers are manual, 07 §3) plus a treasury proposal in D18 if M22 exists.

## ToDo

- [ ] Portfolio equity/peak tracker (`packages/mt_risk/portfolio_dd.py`).
- [ ] Flatten-to-stables routine using existing `position.close` paths via M11.
- [ ] Review lock + strike counter (WORM) + `risk.review.close` (C3).
- [ ] Hard-ceilings flag `programme_ended` read-only to APIs.
- [ ] D06/D01 banner and countdown; Telegram critical alert.
- [ ] Tests; docs.

## Verification

### Tests
- Unit: DD at 24.9% (no action) vs 25.1% (breach); peak tracking with deposits/withdrawals excluded (cash-flow adjusted).
- Integration (paper venues): breach flattens all positions, converts to stables, kill ON, lock set; kill OFF refused until day 30 (clock-injected).
- Integration: second strike sets `programme_ended`; `bot.set_mode` live refused.

### Scenarios
- Given DD reaches 25.3% overnight, then by the next minute all live positions are being closed and you get a critical alert on three channels.
- Given day 31 and a written review, when you approve `risk.review.close` (C3), then sleeves return to `halted` (not live) and must restart individually.

### Stress / failure injection
- Venue disconnect during flatten: positions marked unconfirmed; retries with backoff; resting broker-side stops remain; alert every 60 s until flat or reconciled.

## Acceptance criteria

- [ ] Breach → flatten + lock + alert, verified on paper venues.
- [ ] Two-strike end enforced via the hard-ceilings file only.
- [ ] CI green.

## Exceptions & edge cases

- Deposits/withdrawals: DD uses time-weighted equity so a manual withdrawal is not a drawdown.
- Venue without stable pair: flatten to AUD cash.
- Clock: 30 days measured in UTC from breach time.

## Cardinal rules (do NOT)

- Do NOT let any API clear the strike counter or the programme-ended flag.
- Do NOT move funds off venues automatically.
- Do NOT add discretionary overrides; the only manual action outside approve mode is flatten-and-halt with a required reason (14 §4).
- Do NOT let loosening risk, autonomous mode or a capital step apply without C3 (Telegram + TOTP + cool-down); protective exits never wait for approval.
- Do NOT update or delete WORM rows; corrections are new rows with `supersedes_id` (15 §2).
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order goes through M11.
- Do NOT use keys that are not trade-only, IP-locked and withdrawal-disabled; no live money before the P7 gates pass.
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.

## Doc sync on completion

- `docs/14-strategy-evidence-and-validation.md` §7: DD basis and lock mechanics.
- `docs/03-build-spec.md` M11: portfolio DD rule.
- `docs/roadmap/phase-7-prove-and-go-live.md`: tick T7.21 when this item is done.

## Branch & PR

- Branch: `p7/P7-T022-portfolio-dd-flatten-and-review`
- PR title: `P7-T022: Portfolio DD > 25%: flatten to stables, 30-day review, two-strike end`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P7-T022` run

## Progress log

- 2026-10-21 00:00 · planner · created
