# Phase 7 · Prove It, Then Go Small-Live

| | |
|---|---|
| **Goal** | Only strategies that pass every gate on paper reach live money, in small sub-accounts with withdrawals disabled, stepping up capital only on evidence and stopping on pre-written kill criteria. |
| **Duration** | Months 7–10+ (the paper clock started at the end of P2, so P1 sleeves can be ready on entry) |
| **Depends on** | P2 (gates, risk, engine), P3 (journal/tax + **tax agent's answer**), P5/P6 for strategies that use on-chain or model signals. **Hard-gated** ([17 §E](../17-decisions-register.md#e-ratification-2026-10-22)): the phase opens only after P3 exits (P2 transitively); items that need P5/P6 deliverables carry their own task dependencies |
| **Unlocks** | P8 (only once the platform is in daily use) |
| **Modules** | M11 (capital steps, decay monitoring, health checks), M12 (live adapters incl. MT5/cTrader), M16 (live TCA + reconciliation hardening), M18, MasterTradingBot merge, M14 (the scenario-twin report in weekly reviews and simulated scenarios in the stress tests, built in P6); the go-live pack and the shift to the runtime host ([18 §9](../18-platform-and-deployment.md#9-workstation-first-build-path)) |
| **Containers** | `engine` (live sub-accounts) on the runtime host you choose (default: the workstation); optional Vercel (web app) and Supabase cloud (database); optional Windows VPS for the MT5 bridge |
| **Dashboards** | All; approvals and mobile polish ([mob](../ui/mobile-and-telegram.md)) |
| **Primary docs** | [18 §5–9](../18-platform-and-deployment.md#5-deployment-modes) · [03 §8](../03-build-spec.md#8-promotion-gates-per-strategy-configurable) · [14 §1](../14-strategy-evidence-and-validation.md#1-viability-verdict-set-expectations-before-building) · [14 §6](../14-strategy-evidence-and-validation.md#6-validation-harness-extends-03-8) · [14 §7](../14-strategy-evidence-and-validation.md#7-phase-capital-steps--kill-criteria-refines-04-phase-7) · [14 §8](../14-strategy-evidence-and-validation.md#8-mastertradingbot-integration) · [12](../12-policy-and-compliance.md) · [07](../07-security-notes.md) |

## 1. Scope

**In:** the paper/HITL period and weekly reviews; gate evaluation per strategy; live sub-accounts and keys; capital steps and kill criteria; live decay monitoring; reconciliation hardening; MT5/cTrader adapters and the MasterTradingBot merge; continuity (UPS, 4G, fail-flat); professional-advice items that must be closed before live; the go-live pack (one approval of the values agents seeded during the build); the runtime host and cloud choice, the hardware key and **the shift** (harden, migrate, deploy, re-verify on the target); approvals/mobile polish; the D06 Stress tab; scheduling the 12-month review (a recurring calendar review after P7 closes, not a phase item).

**Out:** anything that weakens a gate to "get live sooner".

## 2. Entry criteria (all must hold)

- Phase 7 is hard-gated: it opens after P3 exits ([17 §D](../17-decisions-register.md#d-other-decisions), P7-B011); work that needs P5/P6 deliverables waits on its own task dependencies.
- ≥ 8 weeks of paper for each P1 sleeve through the real policy/risk/execution path (started T2.80).
- **Tax agent has answered investor vs trader-in-business** (T3.01).
- The venue registry marks each target venue/product `allowed` for you (AUSTRAC re-check < 90 days).
- Runbooks drilled at least once (kill, keys leaked, server down with open positions, bad data; wallet drained only if a hot/burner wallet exists by then).

**Before the first funding** (inside the phase, not entry criteria): the go-live pack is approved (T7.12), the age identities are on the YubiKey (T7.14), and the shift is done with the full verification suite passing on the target (T7.44). Workstation first, test, then shift.

## 3. Requirements

| ID | Requirement | Source | Verified by |
|---|---|---|---|
| R7.01 | Every promoted strategy passes **all §8 gates** incl. harness extensions (per-year/regime, 2×/3× costs, deflated Sharpe ≥ 0.95 (a probability) with trial counter, worst fold, leakage review, survivorship-free, benchmark, safety drills: kill, dead-man and restart on the bot's venue). A Python research strategy is ported to Rust (ONNX via `ort`) and re-checked on paper before it can go live ([18 §2.1](../18-platform-and-deployment.md#21-rust-cargo-workspace-crates)). Gate profile defaults in [16 §2.4](../16-configuration-and-safety-model.md#24-validation-gates-per-strategy-gate-profile), configurable; loosening a gate is C3 | [03 §8](../03-build-spec.md#8-promotion-gates-per-strategy-configurable), [14 §6](../14-strategy-evidence-and-validation.md#6-validation-harness-extends-03-8) | Gate report |
| R7.02 | Paper/HITL period per bot before autonomous or a capital step (default ≥ 8 weeks **and** ≥ 50 trades; class overrides: P1 sleeves ≥ 8 weeks, memecoin ≥ 300 trades, low-frequency bots ≥ 26 weeks; configurable, [16 §2.4](../16-configuration-and-safety-model.md#24-validation-gates-per-strategy-gate-profile)); paper P&L and costs within tolerance of the backtest | [03 §8](../03-build-spec.md#8-promotion-gates-per-strategy-configurable), [14 §6](../14-strategy-evidence-and-validation.md#6-validation-harness-extends-03-8) | Tracking report |
| R7.03 | **Weekly review:** paper vs backtest tracking error, realised vs modelled costs, DQ incidents, journal reconciliation, five worst trades; plus the **scenario-twin report** per bot (R6.33) once the simulator exists: how each bot behaved under the week's simulated shocks. The twin report is an extra input, not a gate ([16 §2.14b](../16-configuration-and-safety-model.md#214b-scenario--crowd-simulator-m14)) | [04 Phase 7](../04-plan-of-action.md#phase-7--prove-it-then-go-small-live-months-710), [14 §4](../14-strategy-evidence-and-validation.md#4-trading-methods-enforced-in-code-defaults-user-editable-in-d06) | Review log |
| R7.04 | Live **sub-accounts per mandate**, trade-only IP-locked keys, **withdrawals disabled**; Travel Rule addresses pre-registered | [07 §3](../07-security-notes.md#3-broker--exchange-keys), [12 §1](../12-policy-and-compliance.md#1-australian-boundary-the-load-bearing-assumption) | Key audit |
| R7.05 | **Capital steps:** the starting live allocation is set per bot in its strategy settings when it goes live (default A$2,000; suggested micro-live range A$2–5k) → after **4 consecutive clean weeks**, +25% of the **current** allocation up to the sleeve's target cap, each step C3; a kill-criterion warning steps back one step, a halt returns to the starting allocation after your review; "clean week" and all values per [16 §2.5](../16-configuration-and-safety-model.md#25-capital-steps-per-sleevebot), configurable. The 12-month review is a recurring calendar review ([README §10](README.md#10-standing-operations-recurring-outside-the-phases)) | [14 §7](../14-strategy-evidence-and-validation.md#7-phase-capital-steps--kill-criteria-refines-04-phase-7), [17 §E](../17-decisions-register.md#e-ratification-2026-10-22) | Step log |
| R7.06 | **Kill criteria** (halt the sleeve + capital step-down): live shortfall > 2× modelled; the sleeve's live Sharpe, once it has 60 live trades, below the backtest 5th percentile; **unexplained recon mismatch > 24 h halts everything**; memecoin kills. **System drawdown:** stage 1 10% → no new entries; stage 2 25% → flatten to stables/AUD + 30-day lock (two stage-2 events end the programme). Before the P6 treasury exists, flattened capital stays as stables on the venue + a USER task. Defaults, configurable ([16 §2.1](../16-configuration-and-safety-model.md#21-risk-sizing-and-drawdown), [§2.6](../16-configuration-and-safety-model.md#26-decay-and-kill-signals-one-meaning-each)) | [14 §7](../14-strategy-evidence-and-validation.md#7-phase-capital-steps--kill-criteria-refines-04-phase-7) | Simulated breach |
| R7.07 | Live decay monitoring extends the P2 jobs (R2.21) to live accounts, with one meaning per signal ([16 §2.6](../16-configuration-and-safety-model.md#26-decay-and-kill-signals-one-meaning-each)): rolling 60-trade Sharpe/hit rate below the 5th percentile (26-week window for low-frequency bots), a CUSUM break or 5 consecutive losing trades → downgrade to HITL; daily health check fails → halt the bot; kill criteria → halt the sleeve (R7.06) | [03 §8 item 8](../03-build-spec.md#8-promotion-gates-per-strategy-configurable), [14 §5](../14-strategy-evidence-and-validation.md#5-risk-engine-additions-m11) | Alerts |
| R7.08 | Mode is set **per bot**: HITL → autonomous is C3; every bot starts live in `hitl` | [02 F7](../02-v1-architecture.md#8-end-to-end-flows) | Audit |
| R7.09 | Reconciliation hardening: venue vs engine vs journal: positions and open orders every 60 s, balances every 5 min, full EOD; quantities match exactly, balances within 0.01% or dust; a mismatch not matched to a journal event within 24 h is unexplained (kill criterion); positions "unconfirmed" after disconnects until reconciled. Defaults, configurable ([16 §2.9](../16-configuration-and-safety-model.md#29-reconciliation)) | [03 M16](../03-build-spec.md#m16-live-cost--data-quality-monitor-always-on-autonomous), [02 §9.3](../02-v1-architecture.md#93-degraded-modes) | Recon report |
| R7.10 | **MT5 (Windows VPS) and/or cTrader Open API** adapters for FP Markets; MasterTradingBot strategies run as M0 "deterministic rule-based" strategies sharing risk, journal, tax and UI. The Windows VPS is hardened, Tailscale-only and holds only the MT5 trade-only login (no other secrets) | [14 §8](../14-strategy-evidence-and-validation.md#8-mastertradingbot-integration), [03 M12](../03-build-spec.md#m12-execution) | Paper parity |
| R7.11 | Continuity: UPS + 4G failover; **fail flat** on link/power loss via the three-layer dead-man (defaults 5 s cancel / 10 s flatten, R2.56); resting venue-side stops on every position from entry | [07 §5](../07-security-notes.md#5-network--host) | Pull-the-plug drill |
| R7.12 | Approvals and mobile polish: phone flows ≤ 3 taps from cold open; PWA installed | [mob §2](../ui/mobile-and-telegram.md#2-phone-flows-must-be--3-taps-from-a-cold-open) | Phone test |
| R7.13 | Professional-advice items closed or explicitly deferred (venue products blocked until then) | [12 §6](../12-policy-and-compliance.md#6-professional-advice-triggers-tracked-as-tasks-in-d13--d15) | Task log |
| R7.14 | **Static AU egress:** WireGuard/Tailscale exit node with a fixed IP in Sydney; only that IP allow-listed on every key; broadband and 4G both tunnel to it; tunnel down → fail-flat via venue timers + resting stops | [16 §3.2](../16-configuration-and-safety-model.md#32-network-egress-and-ip-locked-keys) | Failover drill |
| R7.15 | **Phase 7 state in the API and UI:** capital steps, kill-criteria state, gate reports and weekly reviews exposed through `mt-api` queries/commands and shown in D06/D03 | [02 §7](../02-v1-architecture.md#7-api-contract-mt-api), [D06](../ui/dashboards/D06-risk.md), [D03](../ui/dashboards/D03-strategies.md), [17 §D](../17-decisions-register.md#d-other-decisions) | API tests + Playwright |
| R7.16 | **D06 Stress tab** (replaces the P2 placeholder, R2.57): replay historical shocks (May 2022, Nov 2022, Aug 2024, Feb–Mar 2026) **plus simulated scenarios** from the scenario & crowd simulator (R6.32, capped by `crowdsim.max_shock`) against current positions and policy via `risk.stress.run` (C1), run before live capital. The historical replay is what must pass; simulated results are reported alongside and don't gate unless 16 says so ([18 §2.4](../18-platform-and-deployment.md#24-scenario--crowd-simulator-m14-a-go-live-tool)) | [D06](../ui/dashboards/D06-risk.md), [17 §D](../17-decisions-register.md#d-other-decisions) | Scenario test |
| R7.17 | **Go-live pack:** the values agents seeded during the build (L0 ceilings and L1–L3 risk policy, sleeves and budgets, first manifests; T2.01, T2.02, T2.05) are shown on one page (D16 → Go-live preflight → Settings pack), each with its default and any change since, and you approve them once (C3) before the first funding. The approval is a WORM row naming the policy and manifest versions; the preflight refuses live mode while the pack is unapproved. Everything stays editable afterwards; loosening is C3 as usual | [17 §G](../17-decisions-register.md#g-platform-rust-and-python-supabase-vercel-workstation-first-2026-11-19), [16 §2](../16-configuration-and-safety-model.md#2-default-values-all-configurable), [D16](../ui/dashboards/D16-system.md) | Preflight refusal test + approval row |
| R7.18 | **Runtime host and the shift:** you choose where the always-on services run for live money (default: stay on the workstation, `deploy.mode: workstation`) and whether to use the paid options: web app on Vercel (`web.host: vercel`), database on Supabase cloud in Sydney (`db.target: supabase_cloud`). The shift then applies the live hardening profile (LUKS required; SSH keys only, over Tailscale; firewall inbound only on Tailscale; automatic security updates; chrony), migrates the database if it moves (row counts and hash chains checked on every WORM table, seal re-anchored, backups set up), deploys `apps/web` if it moves (`api.exposure: tailnet` by default; `public` is C3), points the egress check at the static IP, and reruns the full verification suite on the target (risk, `pit`, WORM and tax golden tests, dead-man drill, restore test, egress check). Live money starts only after it passes. Engine, dead-man, recorder, NATS, workers and signer never run on Vercel | [18 §5–6](../18-platform-and-deployment.md#5-deployment-modes), [18 §9](../18-platform-and-deployment.md#9-workstation-first-build-path), [16 §2.15](../16-configuration-and-safety-model.md#215-platform-deployment-and-regions), [07 §5](../07-security-notes.md#5-network--host) | Suite run on the target |
| R7.19 | **Hardware key:** before live keys exist, the host and offline age identities move from the OS keychain onto a YubiKey (`secrets.age_identity_store: yubikey`) and the sops file is re-encrypted to the new recipients; a spare key is recommended | [18 §8](../18-platform-and-deployment.md#8-tailscale-and-the-hardware-key-per-mode), [07 §2](../07-security-notes.md#2-secrets) | Decrypt test with the key; keychain identity removed |

## 4. ToDo sets

### A. Your actions (`USER`)
- [ ] **T7.01** `USER` **Tax agent decision recorded** (investor vs trader) and set in D15 for the FY. → entry criterion · R7.13
- [ ] **T7.02** `USER` Open/verify **live accounts** (KYC) at the venues the registry allows; create live **sub-accounts per mandate**. → R7.04
- [ ] **T7.03** `USER` Create live keys: trade-only, IP-locked, no withdrawals; pre-register withdrawal addresses (Travel Rule). → R7.04
- [ ] **T7.04** `USER` Set each bot's starting live allocation in its strategy settings (default A$2,000) and fund the sub-account only after the gate report passes. → R7.05
- [ ] **T7.05** `USER` Run the **weekly review** (30–45 min) and sign it off in the journal. → R7.03
- [ ] **T7.06** `USER` Approve each promotion (bot HITL → autonomous is C3); approve each capital step (+25% of the current allocation) after 4 consecutive clean weeks. → R7.05, R7.08
- [ ] **T7.07** `USER` Optional professional advice: Hyperliquid exposure, OKX AU derivatives status, a written "private, non-commercial" boundary. → R7.13
- [ ] **T7.08** `USER` FP Markets: read client-agreement clauses on algo trading/scalping/hedging; set up the Windows VPS near the MT5 server (if MT5 route). → R7.10
- [ ] **T7.09** `USER` Install the UPS and 4G failover; do the pull-the-plug drill with paper positions. → R7.11
- [ ] **T7.10** `USER` Put the 12-month review in your calendar as a recurring review (not a phase item; [README §10](README.md#10-standing-operations-recurring-outside-the-phases)): keep only sleeves with positive live net P&L, live Sharpe > 0.5 and beating the benchmark. → R7.05
- [ ] **T7.11** `USER` Provision the egress VM (free tier where available, else a small paid VM in Sydney) and allow-list its IP on every live key. → R7.14
- [ ] **T7.12** `USER` Approve the **go-live pack** (D16 → Go-live preflight → Settings pack): the risk values, L0 ceilings, sleeves and manifests the agents seeded (T2.01, T2.02, T2.05), in one C3 approval before the first funding. → R7.17
- [ ] **T7.13** `USER` Choose the go-live **runtime host** (workstation, home server or Sydney cloud VM) and the cloud options (Vercel for the web app, Supabase cloud for the database); default: stay on the workstation. The agent prepares a one-page comparison first. → R7.18 · [18 §5](../18-platform-and-deployment.md#5-deployment-modes)
- [ ] **T7.14** `USER` Move the age identities onto a **YubiKey** before live keys exist (moved here from T0.03), following the agent's step-by-step instructions. → R7.19 · [18 §8](../18-platform-and-deployment.md#8-tailscale-and-the-hardware-key-per-mode)

### B. Build (`BUILD`, code)
- [ ] **T7.20** `BUILD` Gate report generator per strategy (all §8 + harness sections, safety drills, paper tracking). → R7.01, R7.02
- [ ] **T7.21** `BUILD` Capital-step state machine (clean-week evaluator, +25% of current, step-down rules) and kill-criteria evaluators wired to M11 (halt, flatten, review). → R7.05, R7.06
- [ ] **T7.22** `BUILD` Extend the P2 decay and health jobs (T2.22) to live accounts and wire them to the kill criteria (R7.06). → R7.07, R7.06
- [ ] **T7.23** `BUILD` Reconciliation hardening (three-way venue/engine/journal at the 16 §2.9 defaults; 24 h "explained" rule; unconfirmed state). → R7.09
- [ ] **T7.24** `BUILD` MT5 bridge (`mt-engine` MT5 adapter + the Python `mt_mt5_bridge` on the VPS, which executes only orders that already passed `mt-risk`) and/or cTrader Open API adapter (Rust); MasterTradingBot strategy port. → R7.10
- [ ] **T7.25** `BUILD` Approvals/mobile polish; PWA install prompts; Telegram Mini App (optional). → R7.12
- [ ] **T7.26** `BUILD` Phase 7 API and UI: capital-step, kill-state, gate-report and weekly-review queries/commands in `mt-api`; D06/D03 views; the weekly review pack includes the scenario-twin report (R6.33) when one exists. → R7.15, R7.03
- [ ] **T7.27** `BUILD` D06 Stress tab + `risk.stress.run` (historical shock replay plus the simulated `mt-crowdsim` scenarios against current positions and policy; simulated results labelled as such). → R7.16

### C. Ops & config (`OPS`)
- [ ] **T7.40** `OPS` Live engine config per sub-account; separate secrets; alert routing for live incidents. → R7.04
- [ ] **T7.41** `OPS` Dead-man fail-flat config verified with the 4G link. → R7.11
- [ ] **T7.42** `OPS` Exit-node tunnel config for broadband and 4G; egress check points at the static IP. → R7.14
- [ ] **T7.43** `OPS` Windows VPS hardening for the MT5 bridge (if MT5 route): Tailscale-only, MT5 trade-only login, no other secrets. → R7.10
- [ ] **T7.44** `OPS` **The shift** to the runtime host chosen in T7.13 (after T7.14): live hardening profile, database migration if it moves, web deploy if it moves, egress IP, then the full verification suite on the target; live money only after it passes. → R7.18, R7.04 · [18 §9](../18-platform-and-deployment.md#9-workstation-first-build-path)

### D. Verify & test (`VERIFY`)
- [ ] **T7.60** `VERIFY` All runbooks drilled (kill, keys leaked, server down with open positions, bad data; wallet drained only if a hot/burner wallet exists). → entry criterion
- [ ] **T7.61** `VERIFY` Simulated kill-criteria breaches halt the right sleeve or everything. → R7.06
- [ ] **T7.62** `VERIFY` MT5/cTrader adapter paper parity vs MasterTradingBot outputs. → R7.10
- [ ] **T7.63** `VERIFY` Venue registry re-check (< 90 days) before each funding. → [12 §2](../12-policy-and-compliance.md#2-venue-access-registry)
- [ ] **T7.64** `VERIFY` Failover drill: cut broadband → traffic continues via 4G through the tunnel with the same egress IP; then cut the tunnel → venue timers cancel orders, resting stops remain. → R7.14, R7.11
- [ ] **T7.65** `VERIFY` Live key audit (after T7.03, T7.11): every live key is trade-only, withdrawals disabled, IP-locked to the egress IP; one trading key per sub-account, plus the dead-man sidecar's own trade-only key and a read-only reconciliation key ([16 §3.1](../16-configuration-and-safety-model.md#31-three-layer-dead-mans-switch)). → R7.04
- [ ] **T7.66** `VERIFY` Stress tests before the first funding: replay of the four historical shocks plus the simulated scenarios (R6.32) against current positions and policy; results attached to the gate report (the historical replay must pass; simulated results are reported). → R7.16

### E. Run / soak (`RUN`)
- [ ] **T7.80** `RUN` Paper/HITL period per bot (default ≥ 8 weeks and ≥ 50 trades; P1 sleeves ≥ 8 weeks; low-frequency ≥ 26 weeks; memecoin ≥ 300 trades). → R7.02
- [ ] **T7.81** `RUN` Micro-live: each run of 4 consecutive clean weeks allows one step of +25% of the current allocation (C3). → R7.05
- [ ] **T7.82** `RUN` 12 months live → review (deferred: a recurring calendar review after P7 closes, not a phase item; see [README §10](README.md#10-standing-operations-recurring-outside-the-phases)). → R7.05

## 5. Deliverables

Approved go-live pack · runtime host shifted, hardened and re-verified · gate reports · live sub-accounts · capital-step + kill-criteria automation · decay monitoring · hardened reconciliation · MT5/cTrader adapters · drilled runbooks · weekly review log.

## 6. Exit criteria

1. At least one strategy live in a micro sub-account with all gates passed and the audit trail complete.
2. Kill criteria and decay monitoring proven by simulated breaches.
3. Weekly reviews logged for every live week.
4. The phase closes once micro-live is stable; the 12-month review carries on as a recurring calendar review.

## 7. Risks & open questions

| Risk | Mitigation |
|---|---|
| Live diverges from paper | Kill on shortfall > 2× modelled; small steps; worst-fold validation |
| Temptation to override | No discretionary overrides; only flatten-and-halt with a reason (14 §4) |
| Cloud costs grow | Default stays on the workstation (free); Vercel, Supabase cloud and a VM are your choice at T7.13, with costs shown first |
| The shift breaks something | The full verification suite reruns on the target (T7.44); no live funding until it passes; the workstation setup stays as the fallback |
| Venue status changes (AUSTRAC, DAF from 9 Apr 2027, ASIC 2:1 order to 23 May 2027) | Quarterly registry re-check; products blocked until reconciled |
