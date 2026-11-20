# Decisions Register (resolution of planning gaps)

When the phase planners cross-referenced the docs, they filed **150 gap/bug items** (`tracking/phase-N/bugs/`). This register records the decision for each one.
- **Configurable values** are defined in [16](16-configuration-and-safety-model.md).
- **Anything not listed with an explicit decision** adopts the *suggested fix* in its gap file, as long as it doesn't contradict this register or doc 16.

Decided 2026-10-21 with the user's input on the S2 items. A gap is closed through the kanban (`./kanban done <ID> --evidence "<docs changed>"`) once the docs carry the decision.

## A. S2 items (all resolved)

| Gap | Decision | Docs |
|---|---|---|
| P0-B001 | WORM verify mismatch → `audit.integrity` status in NATS KV; M11 reads it pre-trade. Default action `block_new_entries` (exits continue); options `alert_only` / `halt_all`. Clear with `audit.integrity.ack` (C3) after investigation; every incident and ack is a WORM row (`audit.integrity_incident`) | 16 §2.11 §3.3, 15 §2, 02 §6/§7.2, 03 M17, 07 §8 |
| P1-B001 | Data age = now − our receive time per stream. Thresholds per bot (2 s fast / 60 s slow), session-aware. **M11 checks age inline on every order.** Monitor flips status ≤ 250 ms p99 after the threshold. Replaces "detection → paused < 2 s" | 16 §2.2, 02 §9.2, 03 M16/M11, 14 §5 |
| P2-B001 | Two-stage sleeve drawdown: 10% → halve new sizes, 15% → halt (configurable; e.g. 15%/30%). System: 10% → no new entries, 25% → flatten + 30-day lock | 16 §2.1, 14 §4–§5 |
| P2-B002 | Three-layer dead-man: in-engine watchdog + **external `deadman` sidecar** (own keys/connections) + **venue-side cancel-after timers and resting stops**. Per-bot `on_system_failure` (default `flatten`). Restart flat with bots paused until you resume | 16 §3.1, 02 §3.2/F6, 03 M11/M12, 07 §9 |
| P2-B050 | Deflated Sharpe **≥ 0.95** (it's a probability). "> 0" was an error | 16 §2.4, 03 §8, 14 §6–§7 |
| P2-B051 | Personal, never-distributed use allows vendoring GPL code (03 §1). freqtrade analysers stay vendored under `third_party/` with their licence, isolated in `mt_lab`; a clean-room rewrite is needed only for a SaaS (05) | 03 M7, 01, 05 |
| P3-B001 | Crypto valuation hierarchy: fill price → VWAP of our recorded trades → on-chain pool price → aggregators as cross-check only; stored values are ours | 16 §4.1, 09 |
| P3-B002 | Snapshot price convention per asset class, recorded with source and method | 16 §4.2, 09 |
| P4-B001 | 02 F3 split: Telegram → regex extractor → postures → code/policy only. Other sources → model chain | 02 F3, 12 §4 |
| P4-B010 | Decision path: prefix caching **off**, fixed batch. Shared-prefix mode is allowed only for offline/backfill scoring (marked non-deterministic, never used for decisions or backtests). Stage-1 relevance gate latency: p95 ≤ 300 ms GPU, ≤ 3 s CPU, queued, never on the order path | 10 §4.3, 02 §9.2 |
| P5-B001 | Wallet floats, signer caps, gas budgets are configuration with defaults (16 §2.7). Signing stays disabled until you confirm them (Phase 5 USER task) | 16 §2.7, 13 §1–§2/§7 |
| P6-B016 | Every memory carries `observed_at`/`ingested_at`. Consolidated/reflection memories carry the **latest** source time and are excluded when > `as_of`. If Hindsight can't enforce this, backtests run with memory **disabled** or from a frozen per-`as_of` snapshot. A PIT recall test is mandatory | 10 §1, 03 M9 |
| P7-B003 | Clean week, step size (+25% of current allocation), step-down rules | 16 §2.5, 14 §7 |
| P7-B004 | Static AU egress via a WireGuard/Tailscale exit node with a fixed IP; only that IP allow-listed; broadband and 4G both tunnel to it. If the tunnel is down → fail-flat via venue timers + resting stops. Egress IP/country check | 16 §3.2, 07 §5, 12 §3 |
| P8-B001 | MCP can never approve; `approval.*` and `mcp.*` are never exposed. Approvals only from Telegram/web by you | 16 §2.12, 03 M20, 02 §7.4 |
| P8-B002 | MCP: C0 reads; C1 per token scope; C2 orders → always your approval card (TTL 5 min, expiry = reject); C3 → Telegram + TOTP as usual. No "skip approval" option for MCP orders (resolves P8-B010) | 16 §2.3, 03 M20 |
| P8-B003 | MCP responses pass the provenance filter like any model input: no Telegram text, no `model_input_ok = false` rows, PII (TFN, addresses, statements) redacted, untrusted text wrapped and marked | 03 M20, 12 §5 |
| P8-B004 | Tokens: opaque 256-bit, shown once, stored hashed (HMAC-SHA-256 with a server pepper), scoped, revocable instantly, last-used + client identity recorded, expiry 1d/7d/30d/1y/custom/indefinite (indefinite = warning + C3 + monthly reminder). OAuth 2.1 (PKCE, resource indicators) for clients that support MCP authorization. Transport: Streamable HTTP (JSON-RPC 2.0, SSE streaming, resumable) on Tailscale/TLS; stdio (newline-delimited JSON) locally; optional legacy HTTP+SSE endpoint for older clients. Server notifications via resource subscriptions (fills, approvals, alerts) | 16 §2.12, 03 M20, 07 §6, D17 |

## B. Cross-doc conflicts (one canonical answer)

| Gaps | Decision |
|---|---|
| P2-B053, P7-B009 | Modes are `paper` / `hitl` / `autonomous`, set **per bot** ("approve"/"auto" are retired aliases). A strategy is promoted through gates; a bot is switched between modes |
| P2-B005 | paper → HITL is **C2** everywhere |
| P5-B006, P6-B008 | Venue concentration cap: one default, 25% (range 10–30%) |
| P5-B007, P2-B010 | **Kill:** stops new trading, cancels orders, applies each bot's failure policy, freezes new treasury/earn moves, and (from P5, default on) sweeps hot trading balances to the vault address. In P2 there's no sweep yet |
| P5-B008 | Vault and warm are watch-only: the system never holds their keys. It may *prepare* unsigned transactions (QR/WalletConnect) for you to sign in your own wallet |
| P5-B017 | Autonomous claims use the chain's **airdrop identity wallet**, never the hot trading wallet |
| P3-B003, P5-B015, P6-B005 | One registry, `ops.wallets` (accounts and on-chain addresses), created in P3, extended by the P5 wallet-indexer |
| P5-B003 | The signer accepts intents only from the policy service; airdrop-exec, treasury and DEX execution all go through it |
| P5-B002 | The cost gate is a library (`mt_onchain.costgate`) used by the signer from P5; treasury uses it in P6 |
| P5-B004 | Task-type names: one canonical list in 03 M19, which D13, 08 and the roadmap use |
| P5-B009 | Depeg before P6: alert + task (no automated reduce until the treasury exists) |
| P5-B010 | Airdrop disposal before P7: a USER task (manual sale); automated via M11 only once live execution passes P7 gates |
| P5-B016 | Proof of control: you sign a one-time challenge in **your own wallet app** (EIP-4361-style text / Solana `signMessage`), or make a tiny self-transfer. The system never signs it |
| P6-B002 | Tier B latency: ~2–12 ms per decision on GPU (0.6B), p95 SLO < 50 ms; CPU 100–400 ms. The "150–300 ms" in 03 §2 is removed |
| P6-B013 | HLP cap: ≤ 10% of stablecoins and ≤ 5% of total portfolio, whichever is smaller |
| P7-B001, P7-B002, P2-B060 | Gate profile in 16 §2.4 (DSR ≥ 0.95; paper ≥ 8 weeks and ≥ 50 trades; class overrides) |
| P7-B005 | System drawdown stages in 16 §2.1 (10% no new entries; 25% flatten + lock) |
| P7-B006, P2-B011 | Decay/kill signal meanings in 16 §2.6. Built in P2 for paper; P7 extends to live with kill criteria |
| P0-B017, P1-B010, P8-B007 | Canonical audit names (singular): `audit.order`, `audit.fill`, `audit.command`, `audit.llm_call`, `audit.dq_event`, `audit.dq_ack`, `audit.cost_event`, `audit.recon`, `audit.decision_run`, `audit.seal`, `audit.integrity_incident`, `audit.mcp_call`, `audit.auth_event`, `audit.verify_run`, `audit.signer_ledger`, `audit.signal`, `audit.tierb_decision`, `audit.anomaly`. Command `source` = `web` / `telegram` / `mcp` / `system` |
| P0-B005, P4-B006 | Canonical schemas: `market`, `text`, `features`, `strategy`, `risk`, `audit`, `journal`, `curation`, `ops`, `rag`, `models`, `treasury`, `hindsight`, all created in P0 |
| P0-B006 | 03 §3 is the canonical repo layout; 02 §11 points to it |
| P0-B010 | Provenance columns: `source`, `licence`, `train_ok`, `model_input_ok`, `display_ok`, `retention_days`, `commercial_ok` |
| P0-B011 | Backups: continuous WAL archive, nightly incremental, weekly full, monthly restore test, monthly immutable WORM export |

## C. Defaults that were "N" or unspecified

All in 16:
- P1-B017, P2-B003, P7-B015: dead-man 5 s/10 s; price collar; decision deadlines; cost blow-out; downgrade triggers.
- P4-B004: blackouts.
- P3-B004: wash-sale flag window: re-acquisition within **30 days** either side of a loss disposal (flag only).
- P5-B011: Discord 7 days / ≤ 3 servers per week.
- P5-B012: EV hurdle.
- P6-B012: LLM budgets.
- P6-B015: tier-B thresholds.
- P7-B007: reconciliation.
- P7-B016: low-frequency windows.
- P2-B055: regimes.
- P3-B015: NATS buffer bound.
- P8-B013: MCP limits.

## D. Other decisions

| Gap | Decision |
|---|---|
| P0-B002, P1-B009 | Until the Telegram C3 path exists (P2), C3 commands complete through a host-only break-glass CLI (`mtctl approve <id>` + TOTP over SSH/Tailscale), audited. Retired once Telegram C3 works |
| P0-B003 | C1 = explicit confirm token from the preview call; C2 = a risk-preview hash bound to the exact command + a session re-authenticated within 12 h; C3 = C2 + Telegram approve + TOTP + cool-down |
| P0-B004 | WORM insert p99 < 5 ms; the order path never waits on seals |
| P0-B007 | Two TEI containers: `tei-embed` and `tei-rerank` |
| P0-B008 | P0 adds `llm-local` (llama-server or vLLM) serving the `local-advisor` route |
| P0-B009 | P0 USER task: obtain Anthropic and custom-endpoint API keys into the secrets file |
| P0-B012 | `system.service.restart` goes through a restricted Docker-socket proxy that allows restarting only allow-listed containers |
| P0-B018 | The encrypted sops file lives **outside** this repo (e.g. `~/.config/mastertrader/`), backed up by restic |
| P0-B013, P0-B014, P0-B015, P0-B016 | Fix in DESIGN §6.3, ui §1, roadmap source text, 04 Phase 0 |
| P1-B002 | Record L2 diffs at native speed only for bots that need order-book data (≤ 3 symbols by default); others 1 s snapshots; budget recalculated |
| P1-B005 | Email via your own mail provider's SMTP with an app password, or turn email off (Telegram + ntfy remain) |
| P1-B006 | ntfy self-hosted on the host, reachable via Tailscale only. For iOS push it uses ntfy's upstream relay, which carries only a message ID (no content) |
| P1-B007 | One fan-out: Grafana alerts → webhook → the `alert.*` consumer → Telegram/ntfy/email |
| P1-B008 | Practice/paper accounts use their normal credentials (no money at risk). Live accounts use read-only keys where offered, otherwise trade-only |
| P1-B013 | Add an `ib-gateway` container (IBC-managed) when IBKR is used |
| P1-B014 | Venue health: our own measured withdrawal times + venue status pages/feeds via the regulatory & venue watch + a quarterly AUSTRAC register check (USER task) |
| P1-B011, P1-B015 | Timeframes run tick → 1W with continuous aggregates at 1m, 5m, 15m, 1h, 4h, 1D, 1W; other sizes via `time_bucket` queries at read time. Add `recon.*` and `dq.raw.*` to the 02 §6 subject table |
| P1-B016 | ABS CPI: All groups CPI, weighted average of eight capital cities (series A2325846C (U), verify) |
| P1-B018 | Incident acknowledgement is a new WORM row (`audit.dq_ack`), never an update |
| P1-B003, P1-B004, P1-B012 | Add the missing roadmap ToDos; D02 shows "arrives in P4" states for P4-fed widgets |
| P2-B006 | Netting brokers (OANDA, IG, Alpaca, IBKR) have no STP field. The venue registry marks `stp: n/a (netting)`; one strategy per account/sub-account where netting would merge bots |
| P2-B007 | Client order ID = `{bot}-{engine_epoch}-{seq}`; a signal hash is stored separately for idempotency |
| P2-B008 | Paper/testnet orders are allowed for venues/products marked `allowed` or `read_only`; `blocked` products only if marked `paper_ok` |
| P2-B012 | Telegram `/kill` via NATS uses NATS credentials limited to publishing `kill.set`. The engine writes the kill event to WORM with source `telegram` |
| P2-B013, P2-B014, P2-B052, P2-B054, P2-B056, P2-B057, P2-B058, P2-B059 | Adopt suggested fixes. Tier A trains on forward-return / triple-barrier labels from market data until the P6 teacher exists. Commands `lab.leakage.waive` (C2) and `models.tiera.train` (C1) are added. Bulk approve isn't allowed (except the batched dynamic-selection card in 15 §1.3) |
| P2-B004, P2-B009 | Adopt suggested fixes (D06 uses the 6-rung ladder; engine control subjects `engine.cmd.*`) |
| P3-B005 | PAYG estimator: ATO instalment-amount and instalment-rate methods both computed; your notice decides (U, tax agent) |
| P3-B006, P3-B007 | Add commands `tax.fy.lock`/`unlock` (C3), `task.answer`, `journal.manual_event.add` (C2). A residency change emits `tax.residency.changed`, the venue registry recomputes, and any loosening that results is C3 |
| P3-B008 | RBA gaps: last published business day; non-F11 currencies via USD |
| P3-B009 | Envelope encryption: yearly data keys wrapped by a master key; rotation re-wraps keys in a non-WORM key table, never rows |
| P3-B010 | CARF: use venue-provided statements when available; otherwise not applicable |
| P3-B011, P3-B012 | P3 adds a minimal Accounts page (D16 settings) and a minimal `curation.task` table |
| P3-B013, P3-B014, P3-B016 | Attachments are stored content-addressed under `data/attachments/` and referenced by hash. CommSec is optional in R3.01. Perps treatment added to the tax-agent questions (default revenue (U)) |
| P4-B002, P4-B003 | D08 shows Telegram only as postures. Postures: table `text.telegram_posture`, subject `posture.telegram.*`, consumers M4/M11 rules only |
| P4-B005, P4-B007, P4-B008, P4-B009, P4-B011 | YouTube check moves to P4. Add `models.label.add` + a minimal labelling tool. FIRMS/ACLED keys + OpenSanctions licence as a USER task. Reddit stays optional. Morning-brief content is canonical in mobile-and-telegram §3 |
| P5-B005, P6-B007 | Add WS topics `wallet`, `treasury`, `alert` to 02 §7.3 |
| P5-B013 | Tenderly is not used; Anvil and `simulateTransaction` only |
| P5-B014 | Telegram task buttons include Details |
| P6-B001, P6-B011 | Add missing roadmap ToDos; update 04 Phase 6 |
| P6-B003 | Kev-4B/9B is in the bake-off only if a public, licence-compatible release exists; otherwise dropped (U) |
| P6-B004, P6-B014 | Add the labels endpoint/command and D10 queue tab. `Signal` fields defined in 03 M8: id, ts, as_of, instrument, horizon, direction, edge, calibrated confidence, rationale summary, sources[], model/prompt versions, run id |
| P6-B006 | DefiLlama: the official free API hosts (`api.llama.fi`, `yields.llama.fi`) are allowed; site scraping isn't |
| P6-B009 | MiroFish/OASIS only with a local memory backend and hardened config; no Zep Cloud. Otherwise M14 is skipped |
| P6-B010 | `audit.llm_call` is written from **P0** via the LiteLLM callback, not P6 |
| P7-B008 | Add Phase 7 API/dashboard spec (capital steps, kill state, gate reports, weekly reviews) to 02 and D06/D03 |
| P7-B010 | Windows VPS for MT5: hardened, Tailscale-only, MT5 trade-only login, no other secrets; added to 07 |
| P7-B011 | P7 opens after P3; items that need P5/P6 deliverables carry task dependencies |
| P7-B012 | P7 closes once micro-live is stable; the 12-month review is a scheduled recurring review (calendar task), not a phase item |
| P7-B013, P7-B014 | Fix the roadmap text; add "safety drills" to 03 §8 gates |
| P8-B005, P8-B006, P8-B008, P8-B009, P8-B011, P8-B012 | Never-exposed list in 16 §2.12. The old research note is superseded. Add `anomaly.explain`, `/bots`, `/approvals`, `/mcp/tokens`, `/mcp/sessions`, `source=` filters. `mcp` lives on the internal network behind Caddy on Tailscale only. Reads are logged to `audit.mcp_call` (WORM) |
| P8-B010 | MCP orders always need approval (see P8-B002) |

## E. Ratification (2026-10-22)

You reviewed and ratified this register: every decision in sections A–D stands as written.

**Changes from the review:**
- **L0 hard ceilings** are edited in the agent/bot strategy settings (the ceilings section applies to every bot), not in a host-only file. Tightening is immediate; loosening is C3 like every other loosening ([16 §1](16-configuration-and-safety-model.md#1-configuration-layers-tighten-only-inheritance)).
- **Configurable values are settings, not decisions.** Every value in [16](16-configuration-and-safety-model.md) (sizes, limits, thresholds, allocations, timers) is a default you change in settings. The starting live allocation defaults to A$2,000 and is set per bot when it goes live.

**How work runs (adopted):**
- **Parallel by dependency:** a task starts as soon as its own `depends_on` are done, in any phase (`phase_gating: "dependencies"`, switched on 2026-10-22 once task alignment had added every real cross-phase dependency). Phase 7 (go small-live) and Phase 8 (MCP) are hard-gated: they still wait for their prerequisite phases.
- **Build first, keys last:** integrations are built and tested against mocks, recorded fixtures, emulators, testnets and paper accounts without secrets; live checks needing your keys, accounts or money are separate final VERIFY tasks depending on the USER task that provides them.
- **Up to 6 agents at once**, one per independent workstream, each claiming its task with `./kanban start`.
- **Independent review is mandatory** (`require_review: true`): a separate reviewer agent passes every task before it's done.
- **Trail:** one branch and PR per task where the environment allows it (`p<N>/<ID>-<slug>`, PR `<ID>: <title>`, labelled `phase-N` + type); everywhere, commits carry the task ID and `./kanban trail` reconciles task → branch → PR → commits.
- **Unverified (U) facts** are verified by agents in research tasks before the build that relies on them; tax-law questions go to your tax agent as a USER task.
- **Alignment before build:** doc alignment, then task alignment per phase, then a short change summary for your approval, then kickoff.

## F. Vetted additions (2026-11-19)

Eleven repositories were vetted ([01 §8](01-repo-vetting-report.md#8-addendum-2026-11-19-eleven-more-repositories)); you approved adding what fits:

| Decision | Plan |
|---|---|
| **Setup odds ("time machine")**: before an entry, replay thousands of continuations from the instrument's own recent bars plus every past occurrence of the same setup, using point-in-time data only; show the odds in the lab and on HITL approval cards. Informational: never overrides the risk manager | R2.59 · P2-T077, P2-T078 |
| **Congressional trading disclosures** as a free official event source (House Clerk periodic transaction reports; the Senate eFD only if its terms allow automated personal access (U)). Delayed by law (up to 45 days), so context only, never a sole trigger | R4.17 · P4-T070, P4-T071 |
| **Research workflows** adapted from Anthropic's financial-services skills (Apache-2.0): earnings preview and analysis, catalyst calendar, thesis tracker, morning note, DCF/comps through the valuation desk | R6.08 · P6-T071, P6-T073 |
| **Investor-persona lenses** (idea from ai-hedge-fund, MIT) as optional debate viewpoints, off by default, enabled only if they improve shadow results | R6.08 · P6-T072, P6-T073 |
| **TradingAgents ≥ 0.7.1** (fixes a filing look-ahead leak); **Trading-R1** joins the bake-off only under the Kev rule (public, licence-compatible, runs locally) | P6-T007, P6-T068 · R6.12 |
| **OpenBB provenance resolved**: `openbq-org/OpenBB` is the project's own home | 01 §5 |
| Morning brief per-instrument layout borrows daily_stock_analysis's structure | P4-T047 |
| Not adopted: alpaca-mcp-server in the trading path (bypasses M11; dev/paper tool only), FinceptTerminal (AGPL, overlap), tradingview-mcp (undocumented interfaces), llm-trading-lab code (no licence; reading only) | 01 §8 |


## G. Platform: Rust and Python, Supabase, Vercel, workstation-first (2026-11-19)

You asked for a Rust backend with Python only where necessary, a Vercel-deployable frontend, Supabase Postgres run locally or in the cloud, and a workstation-first build. The full design is [18](18-platform-and-deployment.md).

| Decision | Plan |
|---|---|
| **Rust first** for every service we write: `mt-api` (axum), `mt-risk` (one crate, used by the API, the engine and the dead-man), `mt-deadman`, `mt-recorder`, `mt-monitor`, `mt-store` (`pit` with Python bindings), `mt-obs` (WORM writer, seal), `mt-signer`, `mt-journal` (lot engine, tax), `mt-events`, `mt-telegram-bot`, `mt-mcp` | [18 §2.1](18-platform-and-deployment.md#21-rust-cargo-workspace-crates) |
| **Python only where necessary:** ML training, agents/RAG, Python-only data SDKs (OpenBB, edgartools, Telethon, trafilatura), Python strategies and the research lab. Python never places orders or signs | [18 §2.2](18-platform-and-deployment.md#22-python-uv-workspace-packages-only-where-absolutely-required) |
| **Engine stays NautilusTrader** (Rust core). Rust live node where the venue's Rust adapter is production-ready (verified per venue), else the Python node with the same `mt-risk` binding | [18 §2.1](18-platform-and-deployment.md#21-rust-cargo-workspace-crates) |
| **Supabase Postgres** replaces plain Postgres + TimescaleDB, locally (CLI / self-hosted) and optionally in Supabase cloud. SQL migrations in `supabase/` replace Alembic | [18 §4](18-platform-and-deployment.md#4-database-supabase-postgres) |
| **No TimescaleDB** (deprecated on Supabase Postgres 17): native monthly partitions; the recorder writes the standard bar sizes; `date_bin` for others; old bars to Parquet | [18 §4.3](18-platform-and-deployment.md#43-bars-without-timescaledb) |
| **Supabase Auth** (password + TOTP MFA, sign-ups off) replaces the hand-built login; the browser never reads the database directly (RLS deny-all, Data API and Realtime off) | [18 §4.5–4.6](18-platform-and-deployment.md#45-access-rules) |
| **Frontend:** the same React SPA served locally or deployed to Vercel. Vercel Functions only for stateless short jobs, never in the order path | [18 §5](18-platform-and-deployment.md#5-deployment-modes) |
| **Always-on services never run on Vercel** (engine, dead-man, recorder, NATS, workers, signer): no long-lived processes, duration caps, no static egress IP for IP-locked keys | [18 §6](18-platform-and-deployment.md#6-what-cant-run-on-vercel-and-why) |
| **Workstation first:** Phases 0–6 build, test and paper-trade on your workstation; the shift to a runtime host / Vercel / Supabase cloud is a set of P7 OPS tasks before live money. Host hardware is whatever you run the agent on; GPU optional (CPU profiles default) | [18 §9](18-platform-and-deployment.md#9-workstation-first-build-path) |
| **Regions:** one region (Sydney) by default. Regional engines are allowed later only with measured benefit, a venue-permitted jurisdiction (no location masking), a static IP per region and pre-allocated risk budgets under one global risk authority. Database read replicas serve dashboards, not orders | [18 §7](18-platform-and-deployment.md#7-latency-and-regions) |
| **Tailscale** is needed only for phone access, the private API in hybrid mode and the go-live egress exit node; **the hardware key** only before live money (OS keychain until then). Both move from P0 to when they're needed | [18 §8](18-platform-and-deployment.md#8-tailscale-and-the-hardware-key-per-mode) |
| **Cloud costs are your call at shift time:** Supabase cloud needs a paid plan for a trading database (free plan: 500 MB, pauses after 7 idle days); Vercel Hobby covers personal use (U). Workstation mode is free | [18 §4.1](18-platform-and-deployment.md#41-where-it-runs) |
| **Values you'd otherwise be asked to set** (P2-T048 risk values, P2-T049 sleeves, P2-T050 manifests) are drafted by agents from the 14/16 defaults and approved once in the go-live pack ([P7-T070](../tracking/phase-7/tasks/P7-T070-approve-the-go-live-pack-risk-values-ceilings-sl.md), checked by the P7-T011 preflight), changeable any time in settings | 16 §2 |

## H. Rust-max, borrowed code rebuilt in Rust, scenario simulator, copyleft register (2026-11-20)

You set the direction: anything we adapt or build from ideas is written in Rust; Python only where absolutely required; the crowd simulator becomes a go-live tool; copyleft code is isolated and there's a release plan. Details: [18 §2](18-platform-and-deployment.md#2-language-split-rust-first-python-where-necessary) and [19](19-third-party-register.md).

| Decision | Plan |
|---|---|
| **Borrowed designs are rebuilt in Rust**: TradingAgents debate, FinRobot valuation desk, Vibe-Trading generator loop, Anthropic research workflows (skill files as prompts), persona lenses, setup-odds, congressional disclosures, freqtrade-style bias analysers (clean-room) | `mt-agents` (Rust agent runtime on `rig-core`, explicit state machine, Postgres checkpoints; replaces LangGraph), `mt-lab-core`, `mt-events` |
| **More of the stack moves to Rust**: NLP pipeline (FinBERT and entity models via ONNX/`ort`), anomaly detectors, features, airdrop discovery/scoring, curation, social, model runtime, memory/RAG client | `mt-nlp`, `mt-anomaly`, `mt-features`, `mt-airdrop`, `mt-curation`, `mt-social`, `mt-models`, `mt-memory` |
| **OpenBB, fredapi, sdmx1, edgartools, yfinance → Rust connectors**; **Prefect → `mt-scheduler`** (Postgres-backed jobs and cron) | `mt-connectors`, `mt-scheduler` |
| **Python only where absolutely required**: ML training/research (`mt_research`; promoted models run in Rust via ONNX), trafilatura extraction, Telethon reader (Rust MTProto client archived and unaudited), ccxt ledger import, MT5 bridge. Python never places orders, signs or sits on the live decision path | [18 §2.2](18-platform-and-deployment.md#22-python-uv-workspace-packages-only-where-absolutely-required) |
| **Strategies are Rust by default**; Python strategies only for ML research on paper, ported (ONNX) before live; the generator emits Rust | [18 §2.1](18-platform-and-deployment.md#21-rust-cargo-workspace-crates) |
| **Third-party services stay as they are** (LiteLLM, Hindsight, MLflow, vLLM, TEI, llama.cpp, NATS, Supabase, Grafana stack, Hummingbot, crawl4ai, rss-bridge, ntfy, Anvil): run unmodified, any language; Hummingbot is driven from Rust through its REST API | [19 §1](19-third-party-register.md#1-run-unmodified-separate-services-or-libraries-we-call) |
| **Scenario & crowd simulator (M14) is a go-live tool**, not an optional experiment: clean-room Rust (`mt-crowdsim`), no MiroFish/OASIS code; a **scenario twin** paper engine runs the same bots under simulated shocks during the 8-week paper period (weekly report) and joins the pre-live stress tests. Synthetic data never enters features, training or RAG | [18 §2.4](18-platform-and-deployment.md#24-scenario--crowd-simulator-m14-a-go-live-tool), 16 §2.14b; supersedes P6-B009's "otherwise skip" |
| **Copyleft register and release plan**: copyleft items flagged ⚑ with a per-item open-source/commercial action; vendored copyleft only under `third_party/copyleft/`; `just licence-audit`. The vendored freqtrade analysers (P2-B051) are replaced by the clean-room Rust ones | [19 §4](19-third-party-register.md#4-copyleft-register--and-the-release-plan) |
