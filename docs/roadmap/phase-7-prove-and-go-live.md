# Phase 7 · Prove It, Then Go Small-Live

| | |
|---|---|
| **Goal** | Only strategies that pass every gate on paper reach live money, in small sub-accounts with withdrawals disabled, stepping up capital only on evidence and stopping on pre-written kill criteria. |
| **Duration** | Months 7–10+ (the paper clock started at the end of P2, so P1 sleeves can be ready on entry) |
| **Depends on** | P2 (gates, risk, engine), P3 (journal/tax + **tax agent's answer**), P5/P6 for strategies that use on-chain or model signals |
| **Unlocks** | P8 (only once the platform is in daily use) |
| **Modules** | M11 (capital steps, decay monitoring, health checks), M12 (live adapters incl. MT5/cTrader), M16 (live TCA + reconciliation hardening), M18, MasterTradingBot merge |
| **Containers** | `engine` (live sub-accounts), optional Windows VPS for the MT5 bridge |
| **Dashboards** | All; approvals and mobile polish ([mob](../ui/mobile-and-telegram.md)) |
| **Primary docs** | [03 §8](../03-build-spec.md#8-promotion-gates-per-strategy-configurable) · [14 §1](../14-strategy-evidence-and-validation.md#1-viability-verdict-set-expectations-before-building) · [14 §6](../14-strategy-evidence-and-validation.md#6-validation-harness-extends-03-8) · [14 §7](../14-strategy-evidence-and-validation.md#7-phase-capital-steps--kill-criteria-refines-04-phase-7) · [14 §8](../14-strategy-evidence-and-validation.md#8-mastertradingbot-integration) · [12](../12-policy-and-compliance.md) · [07](../07-security-notes.md) |

## 1. Scope

**In:** the paper/approve period and weekly reviews; gate evaluation per strategy; live sub-accounts and keys; capital steps and kill criteria; live decay monitoring; reconciliation hardening; MT5/cTrader adapters and the MasterTradingBot merge; continuity (UPS, 4G, fail-flat); professional-advice items that must be closed before live; approvals/mobile polish; the 12-month review.

**Out:** anything that weakens a gate to "get live sooner".

## 2. Entry criteria (all must hold)

- ≥ 8 weeks of paper for each P1 sleeve through the real policy/risk/execution path (started T2.80).
- **Tax agent has answered investor vs trader-in-business** (T3.01).
- The venue registry marks each target venue/product `allowed` for you (AUSTRAC re-check < 90 days).
- Runbooks drilled at least once (kill, keys leaked, server down with open positions, bad data, wallet drained).

## 3. Requirements

| ID | Requirement | Source | Verified by |
|---|---|---|---|
| R7.01 | Every promoted strategy passes **all §8 gates** incl. harness extensions (per-year/regime, 2×/3× costs, deflated Sharpe > 0.95 with trial counter, worst fold, leakage review, survivorship-free, benchmark) | [03 §8](../03-build-spec.md#8-promotion-gates-per-strategy-configurable), [14 §6](../14-strategy-evidence-and-validation.md#6-validation-harness-extends-03-8) | Gate report |
| R7.02 | Paper/approve period per strategy (default ≥ 3 months; P1 sleeves ≥ 8 weeks; memecoin ≥ 300 trades); paper P&L and costs within tolerance of the backtest | [03 §8](../03-build-spec.md#8-promotion-gates-per-strategy-configurable), [14 §6](../14-strategy-evidence-and-validation.md#6-validation-harness-extends-03-8) | Tracking report |
| R7.03 | **Weekly review:** paper vs backtest tracking error, realised vs modelled costs, DQ incidents, journal reconciliation, five worst trades | [04 Phase 7](../04-plan-of-action.md#phase-7--prove-it-then-go-small-live-months-710), [14 §4](../14-strategy-evidence-and-validation.md#4-trading-methods-enforced-in-code-defaults-user-editable-in-d06) | Review log |
| R7.04 | Live **sub-accounts per mandate**, trade-only IP-locked keys, **withdrawals disabled**; Travel Rule addresses pre-registered | [07 §3](../07-security-notes.md#3-broker--exchange-keys), [12 §1](../12-policy-and-compliance.md#1-australian-boundary-the-load-bearing-assumption) | Key audit |
| R7.05 | **Capital steps:** micro-live A$2–5k → scale P1 + add P2 in **25% steps after 4 clean weeks each** → 12-month review | [14 §7](../14-strategy-evidence-and-validation.md#7-phase-capital-steps--kill-criteria-refines-04-phase-7) | Step log |
| R7.06 | **Kill criteria:** live shortfall > 2× modelled; live Sharpe after 60 trades < backtest 5th percentile; **unexplained recon mismatch > 24 h halts everything**; memecoin kills; **portfolio DD > 25% → flatten to stables + 30-day review** | [14 §7](../14-strategy-evidence-and-validation.md#7-phase-capital-steps--kill-criteria-refines-04-phase-7) | Simulated breach |
| R7.07 | Live decay monitoring: rolling 60-trade Sharpe/hit rate vs 5th percentile, CUSUM, daily health check | [03 §8 item 8](../03-build-spec.md#8-promotion-gates-per-strategy-configurable), [14 §5](../14-strategy-evidence-and-validation.md#5-risk-engine-additions-m11) | Alerts |
| R7.08 | `auto` mode is C3 per strategy; approve mode first | [02 F7](../02-v1-architecture.md#8-end-to-end-flows) | Audit |
| R7.09 | Reconciliation hardening: venue vs engine vs journal every N minutes and EOD; positions "unconfirmed" after disconnects until reconciled | [03 M16](../03-build-spec.md#m16-live-cost--data-quality-monitor--mt_monitor-always-on-autonomous), [02 §9.3](../02-v1-architecture.md#93-degraded-modes) | Recon report |
| R7.10 | **MT5 (Windows VPS) and/or cTrader Open API** adapters for FP Markets; MasterTradingBot strategies run as M0 "deterministic rule-based" strategies sharing risk, journal, tax and UI | [14 §8](../14-strategy-evidence-and-validation.md#8-mastertradingbot-integration), [03 M12](../03-build-spec.md#m12-execution--mt_engine) | Paper parity |
| R7.11 | Continuity: UPS + 4G failover; **fail flat** on link/power loss; resting broker-side stops | [07 §5](../07-security-notes.md#5-network--host) | Pull-the-plug drill |
| R7.12 | Approvals and mobile polish: phone flows ≤ 3 taps from cold open; PWA installed | [mob §2](../ui/mobile-and-telegram.md#2-phone-flows-must-be--3-taps-from-a-cold-open) | Phone test |
| R7.13 | Professional-advice items closed or explicitly deferred (venue products blocked until then) | [12 §6](../12-policy-and-compliance.md#6-professional-advice-triggers-tracked-as-tasks-in-d13--d15) | Task log |

## 4. ToDo sets

### A. Your actions (`USER`)
- [ ] **T7.01** `USER` **Tax agent decision recorded** (investor vs trader) and set in D15 for the FY. → entry criterion · R7.13
- [ ] **T7.02** `USER` Open/verify **live accounts** (KYC) at the venues the registry allows; create live **sub-accounts per mandate**. → R7.04
- [ ] **T7.03** `USER` Create live keys: trade-only, IP-locked, no withdrawals; pre-register withdrawal addresses (Travel Rule). → R7.04
- [ ] **T7.04** `USER` Fund micro-live (A$2–5k) only after the gate report passes. → R7.05
- [ ] **T7.05** `USER` Run the **weekly review** (30–45 min) and sign it off in the journal. → R7.03
- [ ] **T7.06** `USER` Approve each promotion (approve → auto is C3); approve each capital step after 4 clean weeks. → R7.05, R7.08
- [ ] **T7.07** `USER` Optional professional advice: Hyperliquid exposure, OKX AU derivatives status, a written "private, non-commercial" boundary. → R7.13
- [ ] **T7.08** `USER` FP Markets: read client-agreement clauses on algo trading/scalping/hedging; set up the Windows VPS near the MT5 server (if MT5 route). → R7.10
- [ ] **T7.09** `USER` Install the UPS and 4G failover; do the pull-the-plug drill with paper positions. → R7.11
- [ ] **T7.10** `USER` 12-month review: keep only sleeves with positive live net P&L, live Sharpe > 0.5 and beating the benchmark. → R7.05

### B. Build (`BUILD`, code)
- [ ] **T7.20** `BUILD` Gate report generator per strategy (all §8 + harness sections, paper tracking). → R7.01, R7.02
- [ ] **T7.21** `BUILD` Capital-step state machine and kill-criteria evaluators wired to M11 (halt, flatten, review). → R7.05, R7.06
- [ ] **T7.22** `BUILD` Live decay monitoring jobs (rolling stats, CUSUM, health check). → R7.07
- [ ] **T7.23** `BUILD` Reconciliation hardening (three-way venue/engine/journal; unconfirmed state). → R7.09
- [ ] **T7.24** `BUILD` MT5 bridge and/or cTrader Open API adapter; MasterTradingBot strategy port. → R7.10
- [ ] **T7.25** `BUILD` Approvals/mobile polish; PWA install prompts; Telegram Mini App (optional). → R7.12

### C. Ops & config (`OPS`)
- [ ] **T7.40** `OPS` Live engine config per sub-account; separate secrets; alert routing for live incidents. → R7.04
- [ ] **T7.41** `OPS` Dead-man fail-flat config verified with the 4G link. → R7.11

### D. Verify & test (`VERIFY`)
- [ ] **T7.60** `VERIFY` All runbooks drilled (kill, keys leaked, server down with open positions, bad data, wallet drained). → entry criterion
- [ ] **T7.61** `VERIFY` Simulated kill-criteria breaches halt the right sleeve or everything. → R7.06
- [ ] **T7.62** `VERIFY` MT5/cTrader adapter paper parity vs MasterTradingBot outputs. → R7.10
- [ ] **T7.63** `VERIFY` Venue registry re-check (< 90 days) before each funding. → [12 §2](../12-policy-and-compliance.md#2-venue-access-registry)

### E. Run / soak (`RUN`)
- [ ] **T7.80** `RUN` Paper/approve period per strategy (≥ 8 weeks P1; default ≥ 3 months). → R7.02
- [ ] **T7.81** `RUN` Micro-live 4-week windows; each clean window allows one 25% step. → R7.05
- [ ] **T7.82** `RUN` 12 months live → review. → R7.05

## 5. Deliverables

Gate reports · live sub-accounts · capital-step + kill-criteria automation · decay monitoring · hardened reconciliation · MT5/cTrader adapters · drilled runbooks · weekly review log.

## 6. Exit criteria

1. At least one strategy live in a micro sub-account with all gates passed and the audit trail complete.
2. Kill criteria and decay monitoring proven by simulated breaches.
3. Weekly reviews logged for every live week.

## 7. Risks & open questions

| Risk | Mitigation |
|---|---|
| Live diverges from paper | Kill on shortfall > 2× modelled; small steps; worst-fold validation |
| Temptation to override | No discretionary overrides; only flatten-and-halt with a reason (14 §4) |
| Venue status changes (AUSTRAC, DAF from 9 Apr 2027, ASIC 2:1 order to 23 May 2027) | Quarterly registry re-check; products blocked until reconciled |
