# Phase 6 · AI Decision Layer, Memory, Models, Anomalies & Treasury

| | |
|---|---|
| **Goal** | Ask for an analysis of any instrument and get a sourced signal; agents learn from settled outcomes; own decision models are trained, benchmarked and promoted only through gates; anomalies are explained; idle capital earns under the cost gate. |
| **Duration** | Weeks 24–28 |
| **Depends on** | P2 (lab, tier A, gates), P4 (text, RAG, SemIf), P5 (signer, cost gate, wallet view) |
| **Unlocks** | P7 (LLM-signal strategies can enter the paper → live path), P8 (agents callable from MCP) |
| **Modules** | M8 agents, M9 Hindsight memory, M21 tier B stage 2 + bake-off + distillation, M10 anomaly, M22 hold-and-earn + treasury, M0 LLM-signal template; optional M13 Hummingbot, M14 crowd-sim, M23 social drafts, LightRAG |
| **Containers** | `agents`, `hindsight`, `decision-svc`, `anomaly`, `treasury`, optional `hummingbot`, `social` |
| **Dashboards** | [D09](../ui/dashboards/D09-agents.md) Agents & Decisions, [D10](../ui/dashboards/D10-models-memory.md) Models & Memory, [D11](../ui/dashboards/D11-market-making.md) Market Making (optional), [D18](../ui/dashboards/D18-wallets-treasury.md) Wallets & Treasury (earn), [D13](../ui/dashboards/D13-tasks-curation.md) social drafts |
| **Primary docs** | [03 M8](../03-build-spec.md#m8-ai-decision-layer--mt_agents) · [03 M9](../03-build-spec.md#m9-memory--rag--mt_memory) · [03 M21](../03-build-spec.md#m21-decision-one--model-serving--mt_models) · [03 M10](../03-build-spec.md#m10-anomaly-monitor--mt_anomaly) · [03 M22](../03-build-spec.md#m22-wallets-treasury--hold-and-earn--mt_treasury) · [03 M23](../03-build-spec.md#m23-social-participation--mt_social) · [10](../10-memory-rag-and-models.md) · [13 §4](../13-wallets-treasury-and-onchain.md#4-hold-and-earn-module-m22-mt_treasury) · [13 §5](../13-wallets-treasury-and-onchain.md#5-treasury) · [13 §8](../13-wallets-treasury-and-onchain.md#8-social-participation-m23-mt_social) · [03 §7](../03-build-spec.md#7-llm-cost-control) · [02 F4](../02-v1-architecture.md#8-end-to-end-flows) |

## 1. Scope

**In:** the debate graph and `Signal` with provenance; Hindsight memory with settlement and reflection; own tier B decision-model heads, the bake-off (incl. Kev), operating rules (shadow checks, labelling queue, thresholds, monthly fine-tune) and the distillation loop; anomaly detectors + explain agent; LLM-signal template; LLM cost controls; hold-and-earn, yield allocator, treasury split and sweeps, DAO monitoring; D09, D10, D18 earn. **Optional:** Hummingbot, crowd-sim, social drafts, LightRAG.

**Out:** live money (P7), MCP (P8).

## 2. Entry criteria

- P4 text + RAG + SemIf running ≥ 4 weeks (teacher/label data accumulating).
- P5 signer and cost gate passing their test suites.

## 3. Requirements

### Agents, memory, anomalies
| ID | Requirement | Source | Verified by |
|---|---|---|---|
| R6.01 | LangGraph debate (analysts → bull/bear → research manager → trader → risk debate → PM) with FinRobot valuation tools, `pit` tools, memory recall → structured `Signal` with provenance | [03 M8](../03-build-spec.md#m8-ai-decision-layer--mt_agents) | Sample runs |
| R6.02 | Agents run on cadence or events (anomaly, calendar, big news), **never per tick**; tool outputs cached per (instrument, as_of) | [03 §7](../03-build-spec.md#7-llm-cost-control) | Scheduler tests |
| R6.03 | Prompts/models versioned; **every LLM call audited** (model, hashes, text, tokens, cost, latency) | [03 M17](../03-build-spec.md#m17-observability--audit--mt_obs) | Audit check |
| R6.04 | Hindsight (slim, `hindsight` schema, TEI, LLM via gateway); banks `decisions`, `strategies`, `market-regimes`, `user`, `ops`; point-in-time recall; settlement + reflection | [10 §1](../10-memory-rag-and-models.md#1-hindsight-self-hosted-agent-memory), [03 M9](../03-build-spec.md#m9-memory--rag--mt_memory) | PIT recall test |
| R6.05 | Anomaly detectors (robust z, IsolationForest, change points, correlation breaks) + explain agent → Telegram | [03 M10](../03-build-spec.md#m10-anomaly-monitor--mt_anomaly) | Seeded anomaly |
| R6.06 | LLM-signal template (M0) consuming M8 signals; LLM strategies evaluated on **post-training-cutoff data** | [03 §8 item 4](../03-build-spec.md#8-promotion-gates-per-strategy-configurable) | Gate check |
| R6.07 | Monthly LLM spend cap; per-role budgets; local fallback when exhausted; spend panel | [03 §7](../03-build-spec.md#7-llm-cost-control), [10 §5](../10-memory-rag-and-models.md#5-model-gateway-research-chat--debate-routing-m21) | Budget test |

### Decision One tier B stage 2 (M21)
| ID | Requirement | Source | Verified by |
|---|---|---|---|
| R6.10 | Own **Qwen3-0.6B/1.7B + LoRA + classification head** (or joint schema head); distilled from M8 decisions and **corrected against outcomes**; CE + λ·Brier; temperature/isotonic calibration; abstention thresholds | [10 §4.3](../10-memory-rag-and-models.md#43-design) | Calibration report |
| R6.11 | Serving via vLLM `/classify` or ONNX; **p95 < 50 ms** on GPU; CPU ONNX FP32 for reproducible backtests; determinism controls | [10 §4.3](../10-memory-rag-and-models.md#43-design), [02 §9.2](../02-v1-architecture.md#92-observability--slos) | Benchmark |
| R6.12 | **Bake-off:** own head vs fine-tuned Laya vs Clef-flash vs **Kev-4B/9B** vs SemIf vs JSON generation, on our data + FinMMEval; Brier/ECE per regime, coverage at target precision, latency, flip rate | [10 §4.3](../10-memory-rag-and-models.md#43-design) | Bake-off report |
| R6.13 | **Operating rules:** no Telegram text; ~320-token state budget; per-question thresholds; **5% shadow checks**; labels from outcomes or you, never shadow outputs; monthly fine-tune; social battery questions | [10 §4.3 operating rules](../10-memory-rag-and-models.md#43-design) | Rule tests |
| R6.14 | Distillation loop (nightly): teacher log + outcomes → tier A / tier B candidates → calibration → **gated promotion**, teacher in shadow; direct veto only above a calibrated high-precision threshold | [02 F4](../02-v1-architecture.md#8-end-to-end-flows), [03 M21](../03-build-spec.md#m21-decision-one--model-serving--mt_models) | Promotion audit |

### Treasury & hold-and-earn (M22 part 2)
| ID | Requirement | Source | Verified by |
|---|---|---|---|
| R6.20 | Hold-and-earn on **allow-listed** protocols only (LSTs, core Aave/Spark/Kamino, Pendle PTs, HLP capped if approved); warm-wallet actions need your approval | [13 §4](../13-wallets-treasury-and-onchain.md#4-hold-and-earn-module-m22-mt_treasury) | Policy tests |
| R6.21 | Yield allocator on net `apyBase` minus amortised gas and risk haircut; ≤ 20% per protocol, per-chain/per-stablecoin caps; DefiLlama yields cached hourly | [13 §4](../13-wallets-treasury-and-onchain.md#4-hold-and-earn-module-m22-mt_treasury) | Allocator tests |
| R6.22 | Treasury: floats per sleeve, daily profit sweep to vault, stablecoin concentration limits, **20–40% reserve** | [13 §5](../13-wallets-treasury-and-onchain.md#5-treasury) | Sweep test |
| R6.23 | Node/validator net-earnings model (start only if positive; retire after two negative months); DAO proposal monitoring with drafted votes | [13 §4](../13-wallets-treasury-and-onchain.md#4-hold-and-earn-module-m22-mt_treasury) | Model review |
| R6.24 | Every treasury move passes the **on-chain cost gate** and M11; treasury loosening is C3 | [13 §7](../13-wallets-treasury-and-onchain.md#7-on-chain-cost-gate--dex-execution-extends-m12--m16), [D18](../ui/dashboards/D18-wallets-treasury.md) | Gate tests |

### Optional
| ID | Requirement | Source | Verified by |
|---|---|---|---|
| R6.30 | Hummingbot MM sidecar (telemetry off, broker IDs stripped) as a venue behind M11; must beat HLP on the same capital | [03 M13](../03-build-spec.md#m13-market-making-sidecar), [14 §3](../14-strategy-evidence-and-validation.md#3-strategy-catalogue-evidence-ranked-templates), [D11](../ui/dashboards/D11-market-making.md) | Paper P&L |
| R6.31 | M23 social drafts: drafts in your voice → your approval → **web intent** from your account; disclosure line; credibility scoring; shill-burst posture | [13 §8](../13-wallets-treasury-and-onchain.md#8-social-participation-m23-mt_social), [D13](../ui/dashboards/D13-tasks-curation.md) | Flow test |
| R6.32 | MiroFish/OASIS crowd-sim and LightRAG graph over filings (research path only) | [03 M14](../03-build-spec.md#m14-crowd-simulation-optional), [03 M9](../03-build-spec.md#m9-memory--rag--mt_memory) | Experiment notes |

### UI
| ID | Requirement | Source | Verified by |
|---|---|---|---|
| R6.40 | D09 Agents (runs, debate turns, consensus, provenance), D10 Models & Memory (registry, questions, bake-off, gateway spend, memory, RAG, **labelling queue**, shadow disagreement), D18 earn/treasury | [D09](../ui/dashboards/D09-agents.md) [D10](../ui/dashboards/D10-models-memory.md) [D18](../ui/dashboards/D18-wallets-treasury.md) | Playwright |

## 4. ToDo sets

### A. Your actions (`USER`)
- [ ] **T6.01** `USER` Set LLM budgets (monthly cap, per role) and confirm your custom endpoint details for the gateway. → R6.07
- [ ] **T6.02** `USER` Work the **D10 labelling queue** (~15 min/day while it's new). → R6.13
- [ ] **T6.03** `USER` Approve the **treasury policy** and protocol allow-list (C3); decide on HLP (only if Hyperliquid is approved). → R6.20–R6.22
- [ ] **T6.04** `USER` Decide whether to run Hummingbot, social drafts, crowd-sim (all optional). → R6.30–R6.32
- [ ] **T6.05** `USER` Approve/edit/skip social drafts and click Post yourself (if M23 is on). → R6.31

### B. Build (`BUILD`, code)
- [ ] **T6.20** `BUILD` `mt_agents` debate graph, tools, `Signal` schema, scheduler/event triggers, caching. → R6.01, R6.02
- [ ] **T6.21** `BUILD` Hindsight integration: banks, retain/recall, settlement + reflection jobs, PIT recall. → R6.04
- [ ] **T6.22** `BUILD` `mt_anomaly` detectors + explain agent. → R6.05
- [ ] **T6.23** `BUILD` LLM-signal template + post-cutoff evaluation in the lab. → R6.06
- [ ] **T6.24** `BUILD` Tier B training pipeline (PEFT `SEQ_CLS`), calibration, abstention, export; serving in `decision-svc`. → R6.10, R6.11
- [ ] **T6.25** `BUILD` Bake-off harness (all contenders, FinMMEval) and report. → R6.12
- [ ] **T6.26** `BUILD` Operating rules: state budgets, per-question thresholds, 5% shadow sampler, labelling queue API, label provenance, monthly fine-tune flow. → R6.13
- [ ] **T6.27** `BUILD` Nightly distillation flow + promotion via gates + veto threshold. → R6.14
- [ ] **T6.28** `BUILD` `mt_treasury`: allow-list, allocator, treasury split/sweeps, node/validator model, DAO monitor, earn positions. → R6.20–R6.24
- [ ] **T6.29** `BUILD` UI: D09, D10 (incl. labelling queue), D18 earn/treasury. → R6.40
- [ ] **T6.30** `BUILD` Optional: Hummingbot adapter (D11), `mt_social` drafts, crowd-sim, LightRAG. → R6.30–R6.32
- [ ] **T6.31** `BUILD` Prompt and model versioning for agents; confirm every LLM call lands in `audit.llm_call` (writer exists from P0) with model, hashes, tokens, cost, latency. → R6.03

### C. Ops & config (`OPS`)
- [ ] **T6.40** `OPS` GPU serving for tier B (vLLM pooling runner or ONNX), Hindsight slim container, Laya/Kev/Clef bake-off containers bound to `127.0.0.1` with API keys. → R6.11, R6.12 · [07 §5](../07-security-notes.md#5-network--host)
- [ ] **T6.41** `OPS` Spend panel + budget alerts in Grafana. → R6.07

### D. Verify & test (`VERIFY`)
- [ ] **T6.60** `VERIFY` Bake-off report reviewed; promotion only via gates. → R6.12, R6.14
- [ ] **T6.61** `VERIFY` Determinism: flip rate on repeated inputs; backtests reproduce on CPU ONNX FP32. → R6.11
- [ ] **T6.62** `VERIFY` Label-provenance test: shadow outputs can't become training labels; Telegram rows excluded. → R6.13
- [ ] **T6.63** `VERIFY` PIT test: memory recall in a backtest never returns later episodes. → R6.04
- [ ] **T6.64** `VERIFY` Treasury: cost gate blocks an uneconomic move; depeg auto-reduce; concentration caps. → R6.21–R6.24
- [ ] **T6.65** `VERIFY` Prompt-injection test: scraped text with instructions can't trigger commands. → [02 §9.1](../02-v1-architecture.md#91-security)

### E. Run / soak (`RUN`)
- [ ] **T6.80** `RUN` Four weeks of nightly distillation with the teacher in shadow; LLM-signal strategies on paper. → R6.14, R6.06

## 5. Deliverables

Debate graph · Hindsight memory · own decision models + bake-off · distillation loop · anomaly explanations · treasury + hold-and-earn · D09, D10, D18 earn · optional sidecars.

## 6. Exit criteria (demo)

1. Ask for an analysis of any instrument → a sourced `Signal` with provenance, visible in D09.
2. An anomaly is explained on Telegram.
3. The bake-off report names a production tier B model (or keeps SemIf) with calibration evidence.
4. Idle stables are allocated within the allow-list after the cost gate; the treasury reserve holds.

## 7. Risks & open questions

| Risk | Mitigation |
|---|---|
| Distillation copies teacher biases | Outcome-corrected labels; worst-fold promotion vs a frozen baseline |
| LLM spend creep | Per-role budgets, local fallback, event-triggered runs only |
| DeFi protocol risk | Allow-list, ≤ 20% per protocol, exploit/TVL monitors, reserve |
