# Phase 6 · AI Decision Layer, Memory, Models, Anomalies & Treasury

| | |
|---|---|
| **Goal** | Ask for an analysis of any instrument and get a sourced signal; agents learn from settled outcomes; own decision models are trained, benchmarked and promoted only through gates; anomalies are explained; idle capital earns under the cost gate. |
| **Duration** | Weeks 24–28 |
| **Depends on** | P2 (lab, tier A, gates), P4 (text, RAG, SemIf), P5 (signer, cost gate, wallet view) |
| **Unlocks** | P7 (LLM-signal strategies can enter the paper → live path), P8 (agents callable from MCP) |
| **Modules** | M8 agents, M9 Hindsight memory, M21 tier B stage 2 + bake-off + distillation, M10 anomaly, M22 hold-and-earn + treasury, M0 LLM-signal template, **M14 scenario & crowd simulator** (`mt-crowdsim` + the scenario twin); optional M13 Hummingbot, M23 social drafts, LightRAG |
| **Containers** | `agents` (`mt-agents`, Rust), `hindsight`, `decision-svc`, `anomaly` (`mt-anomaly`, Rust), `treasury` (`mt-treasury`, Rust), `crowdsim` (`mt-crowdsim`, Rust) and `scenario-twin` (a second paper engine on simulated venues), optional `hummingbot` (driven by `mt-mm-adapter`, Rust), `social` (`mt-social`, Rust) ([18 §2](../18-platform-and-deployment.md#2-language-split-rust-first-python-where-necessary)) |
| **Dashboards** | [D09](../ui/dashboards/D09-agents.md) Agents & Decisions, [D10](../ui/dashboards/D10-models-memory.md) Models & Memory, [D11](../ui/dashboards/D11-market-making.md) Market Making (optional), [D18](../ui/dashboards/D18-wallets-treasury.md) Wallets & Treasury (earn), [D13](../ui/dashboards/D13-tasks-curation.md) social drafts, [D14](../ui/dashboards/D14-journal.md) scenario-twin report, [D06](../ui/dashboards/D06-risk.md) Stress (simulated scenarios, used in P7) |
| **Primary docs** | [18 §2.1](../18-platform-and-deployment.md#21-rust-cargo-workspace-crates) · [18 §2.4](../18-platform-and-deployment.md#24-scenario--crowd-simulator-m14-a-go-live-tool) · [16 §2.14b](../16-configuration-and-safety-model.md#214b-scenario--crowd-simulator-m14) · [03 M8](../03-build-spec.md#m8-ai-decision-layer--mt_agents) · [03 M9](../03-build-spec.md#m9-memory--rag--mt_memory) · [03 M21](../03-build-spec.md#m21-decision-one--model-serving--mt_models) · [03 M10](../03-build-spec.md#m10-anomaly-monitor--mt_anomaly) · [03 M22](../03-build-spec.md#m22-wallets-treasury--hold-and-earn--mt_treasury) · [03 M23](../03-build-spec.md#m23-social-participation--mt_social) · [10](../10-memory-rag-and-models.md) · [13 §4](../13-wallets-treasury-and-onchain.md#4-hold-and-earn-module-m22-mt_treasury) · [13 §5](../13-wallets-treasury-and-onchain.md#5-treasury) · [13 §8](../13-wallets-treasury-and-onchain.md#8-social-participation-m23-mt_social) · [03 §7](../03-build-spec.md#7-llm-cost-control) · [02 F4](../02-v1-architecture.md#8-end-to-end-flows) |

## 1. Scope

**In:** the debate graph and `Signal` with provenance; Hindsight memory with settlement and reflection; own tier B decision-model heads, the bake-off (incl. Kev), operating rules (shadow checks, labelling queue, thresholds, monthly fine-tune) and the distillation loop; anomaly detectors + explain agent; LLM-signal template; LLM cost controls; hold-and-earn, yield allocator, treasury split and sweeps, DAO monitoring; D09, D10, D18 earn; the **scenario & crowd simulator** and the **scenario twin** that runs during the paper period (M14, a go-live tool, [17 §H](../17-decisions-register.md#h-rust-max-borrowed-code-rebuilt-in-rust-scenario-simulator-copyleft-register-2026-11-20)). **Optional:** Hummingbot, social drafts, LightRAG.

**Out:** live money (P7), MCP (P8).

## 2. Entry criteria

- P4 text + RAG + SemIf running ≥ 4 weeks (teacher/label data accumulating).
- P5 signer and cost gate passing their test suites.

## 3. Requirements

### Agents, memory, anomalies
| ID | Requirement | Source | Verified by |
|---|---|---|---|
| R6.01 | Debate graph in **`mt-agents`** (Rust on `rig-core`: explicit state-machine graph with Postgres checkpoints; the TradingAgents design rebuilt, prompts adapted with NOTICE): analysts → bull/bear → research manager → trader → risk debate → PM, with the **valuation desk** (FinRobot-style DCF/WACC/comps as deterministic Rust, LLM only for narrative), `pit` tools, memory recall → structured `Signal` with provenance (fields per 03 M8: id, ts, as_of, instrument, horizon, direction, edge, calibrated confidence, rationale summary, sources[], model/prompt versions, run id) | [03 M8](../03-build-spec.md#m8-ai-decision-layer--mt_agents), [18 §2.1](../18-platform-and-deployment.md#21-rust-cargo-workspace-crates), [17 §D](../17-decisions-register.md#d-other-decisions) | Sample runs |
| R6.02 | Agents run on cadence or events (anomaly, calendar, big news), **never per tick**; tool outputs cached per (instrument, as_of) | [03 §7](../03-build-spec.md#7-llm-cost-control) | Scheduler tests |
| R6.03 | Prompts/models versioned; **every LLM call audited** (model, hashes, text, tokens, cost, latency) in `audit.llm_call`, whose writer exists from P0 (R0.13); P6 adds prompt/model versioning | [03 M17](../03-build-spec.md#m17-observability--audit--mt_obs) | Audit check |
| R6.04 | Hindsight (slim, `hindsight` schema, TEI, LLM via gateway); banks `decisions`, `strategies`, `market-regimes`, `user`, `ops`; point-in-time recall: every memory carries `observed_at`/`ingested_at`; consolidated/reflection memories carry the **latest** source time and are excluded when later than `as_of`; if Hindsight can't enforce this, backtests run with memory disabled or from a frozen per-`as_of` snapshot; settlement + reflection | [10 §1](../10-memory-rag-and-models.md#1-hindsight-self-hosted-agent-memory), [03 M9](../03-build-spec.md#m9-memory--rag--mt_memory), [17 §A](../17-decisions-register.md#a-s2-items-all-resolved) | PIT recall test |
| R6.05 | Anomaly detectors in `mt-anomaly` (Rust: robust z, IsolationForest, change points, correlation breaks) + explain agent on `mt-agents` → Telegram | [03 M10](../03-build-spec.md#m10-anomaly-monitor--mt_anomaly) | Seeded anomaly |
| R6.06 | LLM-signal template (M0) consuming M8 signals; LLM strategies evaluated on **post-training-cutoff data** | [03 §8 item 4](../03-build-spec.md#8-promotion-gates-per-strategy-configurable) | Gate check |
| R6.07 | LLM spend: monthly cap (default US$40) and daily per-role budgets (defaults: debate $1.00, strategy-gen $0.50, explain $0.30, memory $0.30, chat $0.40, shadow $0.30; configurable, [16 §2.10](../16-configuration-and-safety-model.md#210-models-tier-b-and-llm-budgets)); local model fallback when exhausted; spend panel | [03 §7](../03-build-spec.md#7-llm-cost-control), [10 §5](../10-memory-rag-and-models.md#5-model-gateway-research-chat--debate-routing-m21) | Budget test |
| R6.08 | **Research workflows** adapted from Anthropic's financial-services skills (Apache-2.0, NOTICE kept): earnings preview and analysis, catalyst calendar, thesis tracker (per strategy/position, with invalidation conditions), morning note; DCF/comps via the FinRobot valuation desk. They run on `mt-agents`, with the skill files kept as prompts in `crates/mt-agents/skills/`. Plus optional **investor-persona lenses** (idea from ai-hedge-fund) as debate viewpoints, off by default and enabled only if they improve shadow results. All through the gateway and `pit` tools | [01 §8](../01-repo-vetting-report.md#8-addendum-2026-11-19-eleven-more-repositories), [17 §F](../17-decisions-register.md#f-vetted-additions-2026-11-19) | Workflow tests + shadow comparison |

### Decision One tier B stage 2 (M21)
| ID | Requirement | Source | Verified by |
|---|---|---|---|
| R6.10 | Own **Qwen3-0.6B/1.7B + LoRA + classification head** (or joint schema head), trained in `mt_research` (Python); distilled from M8 decisions and **corrected against outcomes**; CE + λ·Brier; temperature/isotonic calibration; abstention thresholds | [10 §4.3](../10-memory-rag-and-models.md#43-design) | Calibration report |
| R6.11 | Serving via vLLM `/classify` or ONNX; ~2–12 ms per decision on GPU (0.6B), **p95 SLO < 50 ms**; CPU 100–400 ms; CPU ONNX FP32 for reproducible backtests; determinism controls | [10 §4.3](../10-memory-rag-and-models.md#43-design), [02 §9.2](../02-v1-architecture.md#92-observability--slos) | Benchmark |
| R6.12 | **Bake-off:** own head vs fine-tuned Laya vs Clef-flash vs **Kev-4B/9B** and **Trading-R1** (each only if a public, licence-compatible release exists that runs locally; otherwise dropped (U)) vs SemIf vs JSON generation, on our data + FinMMEval; Brier/ECE per regime, coverage at target precision, latency, flip rate | [10 §4.3](../10-memory-rag-and-models.md#43-design) | Bake-off report |
| R6.13 | **Operating rules:** no Telegram text; ~320-token state budget; per-question thresholds (defaults: auto-decide coverage at ≥ 0.75 precision, ECE ≤ 0.05, flip rate ≤ 0.1%, [16 §2.10](../16-configuration-and-safety-model.md#210-models-tier-b-and-llm-budgets)); **5% shadow checks**; labels from outcomes, agent silver labels (`source: silver`) or you (`models.label.add`, optional), never shadow outputs; monthly fine-tune; social battery questions | [10 §4.3 operating rules](../10-memory-rag-and-models.md#43-design) | Rule tests |
| R6.14 | Distillation loop (nightly): teacher log + outcomes → tier A / tier B candidates → calibration → **gated promotion** (default ≥ 14 days in shadow meeting the thresholds), teacher in shadow; direct veto only at ≥ 0.90 precision (default, configurable) | [02 F4](../02-v1-architecture.md#8-end-to-end-flows), [03 M21](../03-build-spec.md#m21-decision-one--model-serving--mt_models) | Promotion audit |

### Treasury & hold-and-earn (M22 part 2)
| ID | Requirement | Source | Verified by |
|---|---|---|---|
| R6.20 | Hold-and-earn on **allow-listed** protocols only (LSTs, core Aave/Spark/Kamino, Pendle PTs, HLP if Hyperliquid is approved, capped at ≤ 10% of stablecoins and ≤ 5% of total portfolio, whichever is smaller); warm-wallet actions need your approval | [13 §4](../13-wallets-treasury-and-onchain.md#4-hold-and-earn-module-m22-mt_treasury) | Policy tests |
| R6.21 | Yield allocator on net `apyBase` minus amortised gas and risk haircut; ≤ 20% per protocol, per-chain/per-stablecoin caps; DefiLlama yields from the official free API (`yields.llama.fi`; no site scraping) cached hourly | [13 §4](../13-wallets-treasury-and-onchain.md#4-hold-and-earn-module-m22-mt_treasury) | Allocator tests |
| R6.22 | Treasury: floats per sleeve, daily profit sweep to vault, stablecoin concentration limits, **20–40% reserve** (default, configurable) | [13 §5](../13-wallets-treasury-and-onchain.md#5-treasury) | Sweep test |
| R6.23 | Node/validator net-earnings model (start only if positive; retire after two negative months); DAO proposal monitoring with drafted votes | [13 §4](../13-wallets-treasury-and-onchain.md#4-hold-and-earn-module-m22-mt_treasury) | Model review |
| R6.24 | Every treasury move passes the **on-chain cost gate** (in the `mt-onchain` crate) and M11 and signs only via the policy service; treasury loosening is C3 | [13 §7](../13-wallets-treasury-and-onchain.md#7-on-chain-cost-gate--dex-execution-extends-m12--m16), [D18](../ui/dashboards/D18-wallets-treasury.md) | Gate tests |

### Scenario & crowd simulator (M14, a go-live tool)
| ID | Requirement | Source | Verified by |
|---|---|---|---|
| R6.32 | **Scenario & crowd simulator** (`mt-crowdsim`, clean-room Rust on the OASIS/MiroFish idea; no MiroFish or OASIS code). It turns a headline or event into a simulated crowd reaction: a population of LLM persona agents (retail, funds, market makers, media, bots; default 200 agents, 10 rounds), seeded and recorded so runs replay. The output is a **scenario**: a sentiment path plus price, volatility, spread and liquidity shocks, capped by `crowdsim.max_shock` (default price ±15%, volatility ×3, spread ×5, liquidity ÷5). LLM calls use `local-advisor` by default, inside the LLM budget. Replaces the earlier optional MiroFish/OASIS experiment | [18 §2.4](../18-platform-and-deployment.md#24-scenario--crowd-simulator-m14-a-go-live-tool), [16 §2.14b](../16-configuration-and-safety-model.md#214b-scenario--crowd-simulator-m14), [17 §H](../17-decisions-register.md#h-rust-max-borrowed-code-rebuilt-in-rust-scenario-simulator-copyleft-register-2026-11-20), [03 M14](../03-build-spec.md#m14-crowd-simulation-optional) | Seeded replay test |
| R6.33 | **Scenario twin:** a second paper engine runs the same bots on replayed live data with injected scenarios (default 3 a week: the week's top events plus one tail scenario, `crowdsim.scenarios_per_week`) while `crowdsim.scenario_twin.enabled` is on (default: during the paper period and before live). It produces a weekly report per bot that goes into the P7 weekly review pack (R7.03), and its scenarios join the pre-live stress tests (R7.16). An extra input, not a gate unless 16 says so | [18 §2.4](../18-platform-and-deployment.md#24-scenario--crowd-simulator-m14-a-go-live-tool), [16 §2.14b](../16-configuration-and-safety-model.md#214b-scenario--crowd-simulator-m14) | Twin dry run |
| R6.34 | **Simulator boundaries:** it never trades the real paper or live accounts; it holds no venue keys and has no route to the signer; its data is flagged `synthetic = true` and never enters features, model training or RAG, whatever the settings say | [18 §2.4](../18-platform-and-deployment.md#24-scenario--crowd-simulator-m14-a-go-live-tool), [16 §2.14b](../16-configuration-and-safety-model.md#214b-scenario--crowd-simulator-m14) | Isolation and provenance tests |

### Optional
| ID | Requirement | Source | Verified by |
|---|---|---|---|
| R6.30 | Hummingbot MM sidecar (run unmodified, telemetry off, broker IDs stripped), driven by `mt-mm-adapter` (Rust client of the Hummingbot API) as a venue behind M11; must beat HLP on the same capital | [03 M13](../03-build-spec.md#m13-market-making-sidecar), [14 §3](../14-strategy-evidence-and-validation.md#3-strategy-catalogue-evidence-ranked-templates), [D11](../ui/dashboards/D11-market-making.md) | Paper P&L |
| R6.31 | M23 social drafts (`mt-social`, Rust): drafts in your voice → your approval → **web intent** from your account; disclosure line; credibility scoring; shill-burst posture | [13 §8](../13-wallets-treasury-and-onchain.md#8-social-participation-m23-mt_social), [D13](../ui/dashboards/D13-tasks-curation.md) | Flow test |
| R6.35 | LightRAG graph over filings (research path only) | [03 M9](../03-build-spec.md#m9-memory--rag--mt_memory) | Experiment notes |

### UI
| ID | Requirement | Source | Verified by |
|---|---|---|---|
| R6.40 | D09 Agents (runs, debate turns, consensus, provenance), D10 Models & Memory (registry, questions, bake-off, gateway spend, memory, RAG, **labelling queue** tab on the labels endpoint / `models.label.add`, shadow disagreement), D18 earn/treasury, the **scenario-twin report** view in D14 (weekly reviews) | [D09](../ui/dashboards/D09-agents.md) [D10](../ui/dashboards/D10-models-memory.md) [D18](../ui/dashboards/D18-wallets-treasury.md) [D14](../ui/dashboards/D14-journal.md) | Playwright |

### Non-functional
| ID | Requirement | Source | Verified by |
|---|---|---|---|
| R6.N1 | Prompt-injection resistance: scraped or untrusted text, wrapped and marked as untrusted, can't trigger commands | [02 §9.1](../02-v1-architecture.md#91-security) | Injection test |
| R6.N2 | Local inference servers (tier B, Hindsight, bake-off containers) bind to `127.0.0.1` and require an API key | [07 §5](../07-security-notes.md#5-network--host) | Port check |
| R6.N3 | Tier B latency: p95 < 50 ms on GPU (~2–12 ms typical for 0.6B), CPU 100–400 ms; never on the order path | [02 §9.2](../02-v1-architecture.md#92-observability--slos), [17 §B](../17-decisions-register.md#b-cross-doc-conflicts-one-canonical-answer) | Benchmark |

## 4. ToDo sets

### A. Your actions (`USER`)
- [ ] **T6.01** `BUILD` Seed the LLM budgets from 16 §2.10 (US$40/month cap, per-role daily budgets); you change them in settings any time and review them in the go-live pack. The custom endpoint URL and key come from T0.13 (P0-T007). → R6.07
- [ ] **T6.02** `USER` *Optional:* work the **D10 labelling queue** (~15 min/day while it's new). Agent silver labels are the default; yours improve them and nothing waits on them. → R6.13
- [ ] **T6.03** `USER` Approve the **treasury policy** and protocol allow-list (C3); decide on HLP (only if Hyperliquid is approved; default cap ≤ 10% of stables and ≤ 5% of portfolio). → R6.20–R6.22
- [ ] **T6.04** `OPS` Record the optional-module defaults (Hummingbot, social drafts, credibility, LightRAG: all **off**, [16 §2.14a](../16-configuration-and-safety-model.md#214a-optional-modules)); you switch any of them on in settings when you want them. The scenario & crowd simulator is not optional ([16 §2.14b](../16-configuration-and-safety-model.md#214b-scenario--crowd-simulator-m14)). → R6.30, R6.31, R6.35
- [ ] **T6.05** `USER` Approve/edit/skip social drafts and click Post yourself (if M23 is on). → R6.31

### B. Build (`BUILD`, code)
- [ ] **T6.20** `BUILD` `mt-agents` runtime (Rust, `rig-core`, explicit state-machine graph, Postgres checkpoints, every model call through the LiteLLM gateway) + debate graph, valuation desk, tools, `Signal` schema (03 M8 fields), `mt-scheduler`/event triggers, caching. → R6.01, R6.02
- [ ] **T6.21** `BUILD` Hindsight integration: banks, retain/recall, settlement + reflection jobs, PIT recall (`observed_at`/`ingested_at` on every memory; consolidated memories excluded when later than `as_of`; memory-off / frozen-snapshot backtest mode). → R6.04
- [ ] **T6.22** `BUILD` `mt-anomaly` detectors (Rust) + explain agent on `mt-agents`. → R6.05
- [ ] **T6.23** `BUILD` LLM-signal template + post-cutoff evaluation in the lab. → R6.06
- [ ] **T6.24** `BUILD` Tier B training pipeline in `mt_research` (Python, PEFT `SEQ_CLS`, run as `mt-scheduler` jobs), calibration, abstention, ONNX export; serving in `decision-svc`, runtime client in `mt-models` (Rust). → R6.10, R6.11
- [ ] **T6.25** `BUILD` Bake-off harness (all contenders, FinMMEval) and report. → R6.12
- [ ] **T6.26** `BUILD` Operating rules: state budgets, per-question thresholds (16 §2.10 defaults), 5% shadow sampler, labelling queue API, label provenance, monthly fine-tune job. → R6.13
- [ ] **T6.27** `BUILD` Nightly distillation job (`mt-scheduler`) + promotion via gates + veto threshold. → R6.14
- [ ] **T6.28** `BUILD` `mt-treasury` (Rust): allow-list, allocator (DefiLlama official API, the `mt-onchain` cost gate, signing via the policy service), treasury split/sweeps, node/validator model, DAO monitor, earn positions. → R6.20–R6.24
- [ ] **T6.29** `BUILD` UI: D09, D10 (incl. labelling queue), D18 earn/treasury. → R6.40
- [ ] **T6.30** `BUILD` `mt-crowdsim` (Rust, clean-room, no MiroFish/OASIS code): persona population and rounds (16 §2.14b defaults), seeded and recorded runs, scenario output (sentiment path + price/volatility/spread/liquidity shocks capped by `crowdsim.max_shock`), `local-advisor` route inside the LLM budget; scenarios picked from the week's top events plus one tail scenario. → R6.32, R6.34
- [ ] **T6.31** `BUILD` Prompt and model versioning for agents; confirm every LLM call lands in `audit.llm_call` (writer exists from P0) with model, hashes, tokens, cost, latency. → R6.03
- [ ] **T6.32** `BUILD` LLM budget enforcement in the gateway: monthly cap + daily per-role budgets (incl. shadow), local fallback when exhausted, spend events. → R6.07
- [ ] **T6.33** `BUILD` Research workflows (earnings preview/analysis, catalyst calendar, thesis tracker, morning note) as agent workflows feeding the debate and the morning brief. → R6.08
- [ ] **T6.34** `BUILD` Optional investor-persona lenses as debate viewpoints, off by default, evaluated in shadow before use. → R6.08
- [ ] **T6.35** `BUILD` Optional: Hummingbot adapter (`mt-mm-adapter`, Rust; D11), `mt-social` drafts (Rust), LightRAG. → R6.30, R6.31, R6.35
- [ ] **T6.36** `BUILD` Scenario twin: a second paper engine (simulated venues, no keys) running the same bots on replayed live data with injected `mt-crowdsim` scenarios; a weekly report per bot stored for the P7 weekly review pack; scenarios exported in the format `risk.stress.run` reads (T7.27); every output flagged `synthetic = true`. → R6.33, R6.34
- [ ] **T6.37** `BUILD` UI: scenario-twin report view in D14 (weekly reviews; per bot and per scenario, labelled Simulated) and a list of recent simulator runs. → R6.40, R6.33 · [D14](../ui/dashboards/D14-journal.md)

### C. Ops & config (`OPS`)
- [ ] **T6.40** `OPS` Tier B serving per `models.gpu_profile: auto` (vLLM pooling runner when a GPU is present, otherwise ONNX on CPU), Hindsight slim container, Laya/Kev/Clef bake-off containers bound to `127.0.0.1` with API keys. → R6.11, R6.12, R6.N2 · [07 §5](../07-security-notes.md#5-network--host)
- [ ] **T6.41** `OPS` Spend panel + budget alerts in Grafana. → R6.07
- [ ] **T6.42** `OPS` `crowdsim` and `scenario-twin` containers, digest-pinned, on an isolated network with no route to the signer or venue keys; `local-advisor` route inside the LLM budget; `crowdsim.*` settings seeded from 16 §2.14b. → R6.32–R6.34

### D. Verify & test (`VERIFY`)
- [ ] **T6.60** `VERIFY` Bake-off report reviewed; promotion only via gates. → R6.12, R6.14
- [ ] **T6.61** `VERIFY` Determinism: flip rate on repeated inputs; backtests reproduce on CPU ONNX FP32. → R6.11
- [ ] **T6.62** `VERIFY` Label-provenance test: shadow outputs can't become training labels; Telegram rows excluded. → R6.13
- [ ] **T6.63** `VERIFY` PIT test: memory recall in a backtest never returns later episodes. → R6.04
- [ ] **T6.64** `VERIFY` Treasury: cost gate blocks an uneconomic move; depeg auto-reduce; concentration caps. → R6.21–R6.24
- [ ] **T6.65** `VERIFY` Prompt-injection test: scraped text with instructions can't trigger commands. → R6.N1 · [02 §9.1](../02-v1-architecture.md#91-security)
- [ ] **T6.66** `VERIFY` Sample debate runs on three instruments: each returns a `Signal` with every 03 M8 field and its provenance. → R6.01
- [ ] **T6.67** `VERIFY` Scheduler test: agents run on cadence or events only, never per tick; tool outputs are cached per (instrument, as_of). → R6.02
- [ ] **T6.68** `VERIFY` Seeded anomaly → detector fires → explanation arrives on Telegram. → R6.05
- [ ] **T6.69** `VERIFY` LLM-signal gate check: strategies are evaluated only on post-training-cutoff data. → R6.06
- [ ] **T6.70** `VERIFY` Budget test: exhausting a role's daily budget (and the monthly cap) falls back to the local model instead of failing; every call still lands in `audit.llm_call`. → R6.07, R6.03
- [ ] **T6.71** `VERIFY` Tier B latency benchmark: p95 < 50 ms on GPU (runs when a GPU is present); CPU figures always recorded. → R6.11, R6.N3
- [ ] **T6.72** `VERIFY` Kev-4B/9B and Trading-R1 check (U): does a public, licence-compatible, locally runnable release exist? Record the answer before the bake-off; drop either if not. → R6.12
- [ ] **T6.73** `VERIFY` Local inference port check: tier B, Hindsight and bake-off servers listen on `127.0.0.1` only and refuse calls without the API key. → R6.N2
- [ ] **T6.74** `VERIFY` Research workflows: PIT-only inputs, outputs carry sources; persona lenses compared in shadow against the debate without them. → R6.08
- [ ] **T6.75** `VERIFY` Simulator isolation and provenance: `synthetic = true` rows are refused by features, training and RAG; the twin can't reach the signer, venue keys or the real paper/live accounts; the same seed replays the same scenario. → R6.34, R6.32
- [ ] **T6.76** `VERIFY` Scenario twin dry run on replayed data: one week produces a report for every bot, with every injected shock inside `crowdsim.max_shock`. → R6.33

### E. Run / soak (`RUN`)
- [ ] **T6.80** `RUN` Four weeks of nightly distillation with the teacher in shadow; LLM-signal strategies on paper. → R6.14, R6.06
- [ ] **T6.81** `RUN` Scenario twin runs every week alongside the paper bots, from the moment it lands until go-live (`crowdsim.scenario_twin.enabled`); its reports feed the P7 weekly reviews. → R6.33

## 5. Deliverables

Debate graph · Hindsight memory · own decision models + bake-off · distillation loop · anomaly explanations · treasury + hold-and-earn · scenario & crowd simulator + scenario twin · D09, D10, D18 earn, D14 twin report · optional sidecars.

## 6. Exit criteria (demo)

1. Ask for an analysis of any instrument → a sourced `Signal` with provenance, visible in D09.
2. An anomaly is explained on Telegram.
3. The bake-off report names a production tier B model (or keeps SemIf) with calibration evidence.
4. Idle stables are allocated within the allow-list after the cost gate; the treasury reserve holds.
5. The scenario twin produces its first weekly report per bot on replayed data, visible in D14.

## 7. Risks & open questions

| Risk | Mitigation |
|---|---|
| Distillation copies teacher biases | Outcome-corrected labels; worst-fold promotion vs a frozen baseline |
| LLM spend creep | Per-role budgets, local fallback, event-triggered runs only |
| DeFi protocol risk | Allow-list, ≤ 20% per protocol, exploit/TVL monitors, reserve |
| Simulated shocks read as evidence | The twin report and simulated stress results are an extra input, never a gate (16 §2.14b); synthetic data never enters features, training or RAG |
