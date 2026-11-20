# MasterTrader — Third-party register (language, licence, use, open-source plan)

Every outside component, what it's written in, how we use it, and what would change if MasterTrader were ever open-sourced or sold.
- Decisions: [17 §H](17-decisions-register.md#h-rust-max-borrowed-code-rebuilt-in-rust-scenario-simulator-copyleft-register-2026-11-20).
- Stack: [18 §2](18-platform-and-deployment.md#2-language-split-rust-first-python-where-necessary).
- Licence background: [05](05-saas-legal-and-licensing.md) and [01 §2](01-repo-vetting-report.md#2-license-matrix--what-you-can-actually-do).
- Facts marked (U) are checked by an agent before release work starts (P0-T074 audit).

**How to read it.** MasterTrader is private and single-user. Copyleft obligations (GPL, AGPL, LGPL) are triggered by **distributing** the software, or (AGPL) by letting **other people** use a modified version over a network. Private use triggers neither. The register still marks every copyleft item, so that a release later is a known checklist rather than an audit.

---

## 1. Run unmodified (separate services or libraries we call)

Their language is irrelevant to the Rust-first rule: we run them as they are and talk to them over HTTP, NATS, SQL or a library API. **None of them needs porting.** "Release action" says what an open-source or commercial release would need.

| Component | Language | Licence | How we use it | Release action |
|---|---|---|---|---|
| **NautilusTrader** | **Rust** core + Python API | **LGPL-3.0** ⚑ | Trading engine (library) | Keep. Publish any changes we make to Nautilus itself; Rust links statically, so ship relinkable objects or release under an LGPL-compatible licence. No port: it's already Rust |
| Supabase (Postgres, Auth, Storage, Studio) | C (Postgres), Go (Auth), TypeScript (Storage, Studio) | PostgreSQL licence, Apache-2.0, MIT (U per component) | Database, login, file storage | None |
| NATS JetStream | Go | Apache-2.0 | Event bus, KV | None |
| Caddy | Go | Apache-2.0 | Reverse proxy, TLS | None |
| LiteLLM | Python | MIT (its `enterprise/` folder is under a separate licence and isn't used) | LLM gateway, budgets; our `audit.llm_call` callback is a small Python plugin file mounted into the unmodified container | None. A Rust gateway (e.g. TensorZero, Apache-2.0 (U)) is an optional swap, not needed |
| MLflow | Python + TypeScript UI | Apache-2.0 | Experiments, model registry (training side) | None |
| TEI (text-embeddings-inference) | **Rust** | Apache-2.0 | Embeddings, rerank | None |
| llama.cpp (`llama-server`) | C/C++ | MIT | Local advisor model | None |
| vLLM | Python + C++/CUDA | Apache-2.0 | GPU model serving (SemIf, tier B) | None |
| Hindsight | Python | MIT (U: PyPI lists Apache-2.0) | Agent memory service | None |
| LightRAG | Python | MIT | Optional filings graph (off by default, 16 §2.14a), unmodified container | None |
| Hummingbot + Hummingbot API | Python/Cython | Apache-2.0 | Optional market-making sidecar; our Rust `mt-mm-adapter` drives its REST API | None |
| crawl4ai | Python | Apache-2.0 (attribution request (U)) | JS-page extraction fallback | Keep attribution |
| yt-dlp | Python (standalone CLI) | Unlicense | Subtitles for earnings calls, optional YouTube source | None |
| Farcaster hub (Hubble) | TypeScript + Rust | MIT (U) | Optional: a public hub's HTTP API, or self-hosted | None |
| rss-bridge | PHP | Unlicense (U) | Feeds for sites without RSS | None |
| Anvil (Foundry) | **Rust** | MIT / Apache-2.0 | Mainnet-fork simulation | None |
| Prometheus, Alertmanager | Go | Apache-2.0 | Metrics, alert routing | None |
| **Grafana, Loki** | Go + TypeScript | **AGPL-3.0** ⚑ | Dashboards, logs (unmodified, separate containers) | Unmodified use is fine even in a release. Never patch them. For a hosted product, optionally swap to Perses + VictoriaLogs (Apache-2.0) |
| Vector | **Rust** | MPL-2.0 | Log shipping | None (file-level copyleft only if modified) |
| ntfy | Go | Apache-2.0 / GPL-2.0 dual | Push alerts | Use under Apache-2.0 |

## 2. Python libraries we keep (only where absolutely required, [18 §2.2](18-platform-and-deployment.md#22-python-uv-workspace-packages-only-where-absolutely-required))

| Library | Licence | Why it stays | Rust path if ever wanted |
|---|---|---|---|
| PyTorch, LightGBM, scikit-learn, Optuna, Qlib | BSD-3 / MIT | Training and research only; promoted models run in Rust via ONNX | Not worth it: training ecosystem |
| **vectorbt** | Apache-2.0 **+ Commons Clause** ⚑ | Research exploration only, never in the runtime | Drop from any commercial build; our Rust `mt-lab-core` harness covers validation |
| trafilatura | Apache-2.0 (U: changed from GPL in v1.8) | Article extraction quality | A Rust readability crate once its quality matches on our fixtures |
| Telethon | MIT | MTProto reader; the Rust client (grammers) was archived in Feb 2026, unaudited | Swap when a maintained, audited Rust MTProto client exists |
| ccxt (ledger import only) | MIT | Statement history across many exchanges | Per-venue Rust importers for the venues you use |
| MetaTrader5 package | Proprietary (MetaQuotes) ⚑ (U) | Only way to drive MT5 | Ship as an optional adapter you install yourself; or use the cTrader route (Rust) |

## 3. Borrowed designs, rebuilt in Rust (no third-party code in the runtime)

Since we rewrite anyway, these are rebuilt in Rust from their published designs. Where we copy text from an MIT/Apache source (prompts, skill files, formulas), we keep its copyright notice in `NOTICE`.

| Source | Licence | What we take | Our Rust home |
|---|---|---|---|
| TradingAgents | Apache-2.0 | Debate graph design: analysts → bull/bear → trader → risk → PM; prompts adapted. Its ≥ 0.7.1 filing look-ahead fix is covered by `pit` | `mt-agents` |
| FinRobot | Apache-2.0 + trademark policy | Valuation desk design (DCF/WACC/DDM/comps, SEC XBRL); don't use the FinRobot name | `mt-agents` (valuation desk), `mt-connectors` (XBRL) |
| HKUDS/Vibe-Trading | MIT | Research → strategy-generation loop; generator emits **Rust** strategies against our templates, compiled and tested in the sandbox | `mt-agents`, `mt-lab-core` |
| anthropics/financial-services | Apache-2.0 | Skill files (earnings preview/analysis, catalyst calendar, thesis tracker, morning note, DCF/comps) used as prompts | `mt-agents` (prompts in `crates/mt-agents/skills/`, NOTICE kept) |
| freqtrade | GPL-3.0 | **Ideas only**: look-ahead and recursive-formula analysers, clean-room. Replaces the earlier vendored copy (P2-B051) | `mt-lab-core` |
| day-trader-skill | MIT | Setup-odds "time machine"; congressional-trade source | `mt-lab-core`, `mt-events` |
| ai-hedge-fund | MIT | Investor-persona lenses (off by default) | `mt-agents` |
| daily_stock_analysis | MIT | Per-instrument brief layout | `mt-agents` (morning brief), web |
| osiris | MIT | Event-map ideas, small pieces | `mt-events`, web |
| nofx | AGPL-3.0 | Idea only ("frontier mode"); no code | — |
| MiroFish / CAMEL-AI OASIS | AGPL-3.0 / Apache-2.0 | **Idea only**: LLM persona crowd simulation, clean-room | `mt-crowdsim` ([18 §2.4](18-platform-and-deployment.md#24-scenario--crowd-simulator-m14-a-go-live-tool)) |

**Not used at all:** vibetrading (unsafe, redundant), FinceptTerminal (AGPL, overlap), tradingview-mcp (undocumented interfaces), llm-trading-lab (no licence; reading only), alpaca-mcp-server (bypasses the risk manager; dev tool against paper only).

## 4. Copyleft register ⚑ and the release plan

| ⚑ Item | Today (private) | If open-sourced | If sold / hosted |
|---|---|---|---|
| NautilusTrader (LGPL-3.0, linked) | Fine | Fine with an LGPL-compatible project licence; publish Nautilus changes | Comply with LGPL relinking (dynamic linking or relinkable objects), or a commercial arrangement with Nautech |
| Grafana, Loki (AGPL-3.0, separate) | Fine | Fine unmodified | Fine unmodified; optional swap to Perses + VictoriaLogs |
| vectorbt (Commons Clause) | Fine (research) | Fine as an optional research extra | Remove |
| MetaTrader5 package (proprietary) | Fine | Optional adapter the user installs | Same |
| Vendored freqtrade analysers (GPL-3.0) | Being replaced by the clean-room Rust analysers | Must be gone: the release checklist fails if `third_party/` holds GPL code | Same |

**Rules from now on:**
- Any copyleft code that's ever vendored goes under `third_party/copyleft/<name>/` with its licence and a line in this table.
- `just licence-audit` (cargo-deny + pip-licenses + a scan of `third_party/`) reports every ⚑ item.
- A release starts with that audit and this table; nothing else needs porting for licence reasons.
