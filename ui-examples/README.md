# UI examples (Stitch, v1)

These are reference mock-ups generated in Stitch for MasterTrader. They're **design references, not production code**:
- static HTML;
- Tailwind loaded from the `cdn.tailwindcss.com` runtime (needs internet);
- Google Fonts and Material Symbols;
- small cosmetic scripts (countdowns, pulse effects, auto-scroll).

There's no network/data access and no `eval`; reviewed 2026-10-21.

The authoritative spec is **[../DESIGN.md](../DESIGN.md) (v2)**. It supersedes [stitch-DESIGN.original.md](stitch-DESIGN.original.md). Where a mock-up differs from DESIGN.md v2, **DESIGN.md wins**.

## Screens

| # | Screen | Module(s) | Form factor | Screenshot | Code |
|---|---|---|---|---|---|
| 1 | Autonomous Command Cockpit | M15 shell, M8, M11, M12, M16 | Desktop | [png](screenshots/autonomous-command-cockpit-quant-terminal.png) | [html](code/autonomous-command-cockpit-quant-terminal.html) |
| 2 | Multi-Agent Debate & Consensus | M8, M9, M21 | Desktop | [png](screenshots/multi-agent-debate-consensus-terminal.png) | [html](code/multi-agent-debate-consensus-terminal.html) |
| 3 | Cross-Asset Terminal & Free Liquidity Matrix | M1, M6 | Desktop only (no breakpoints) | [png](screenshots/cross-asset-terminal-free-liquidity-matrix.png) | [html](code/cross-asset-terminal-free-liquidity-matrix.html) |
| 4 | Strategy Lab (NautilusTrader simulation) | M0, M7 | Desktop | [png](screenshots/strategy-lab-nautilustrader-simulation.png) | [html](code/strategy-lab-nautilustrader-simulation.html) |
| 5 | Risk Governor & Kill-Switch Hub | M11 | Desktop | [png](screenshots/autonomous-risk-governor-kill-switch-hub.png) | [html](code/autonomous-risk-governor-kill-switch-hub.html) |
| 6 | Hummingbot Pure MM Terminal | M13 | Desktop | [png](screenshots/hummingbot-high-frequency-market-making-pure-mm-terminal.png) | [html](code/hummingbot-high-frequency-market-making-pure-mm-terminal.html) |
| 7 | Free Data Pipeline & Feed-Quality Sentinel | M1, M16 | Desktop | [png](screenshots/live-free-data-pipeline-feed-quality-sentinel.png) | [html](code/live-free-data-pipeline-feed-quality-sentinel.html) |
| 8 | Social Sentiment, Macro & Geopolitical Firehose | M2, M3, M5 | Desktop | [png](screenshots/social-sentiment-macro-geopolitical-firehose.png) | [html](code/social-sentiment-macro-geopolitical-firehose.html) |
| 9 | Order Execution Hub & Smart Routing | M12, M16 (TCA) | Desktop | [png](screenshots/order-execution-hub-smart-routing-engine.png) | [html](code/order-execution-hub-smart-routing-engine.html) |
| 10 | Vetted Launch Radar & AU EOFY Tax Ledger | M4, M19, M18 | Desktop | [png](screenshots/vetted-launch-radar-au-eofy-tax-ledger.png) | [html](code/vetted-launch-radar-au-eofy-tax-ledger.html) |
| 11 | Claude MCP Control | M20 (Phase 8) | Desktop | [png](screenshots/claude-mcp-sovereign-autonomous-node-control.png) | [html](code/claude-mcp-sovereign-autonomous-node-control.html) |
| 12 | Mobile Quant Terminal | M15 mobile | Phone only (no breakpoints) | [png](screenshots/mobile-autonomous-quant-terminal.png) | [html](code/mobile-autonomous-quant-terminal.html) |
| 13 | Mobile Multi-Agent Debate | M8 mobile | Phone only, `max-w-[412px]` | [png](screenshots/mobile-multi-agent-debate-consensus.png) | [html](code/mobile-multi-agent-debate-consensus.html) |

**Brand boards:**
- [Recommended Signal M](screenshots/brand/recommended-signal-m.png)
- [Three directions](screenshots/brand/three-directions.png)
- [App icon & small sizes](screenshots/brand/app-icon-small-sizes.png)

Vector source: [../brand/](../brand/).

**Viewing:** open any `code/*.html` in a browser with internet access. The Tailwind CDN is required, and it was blocked from the review sandbox, so the audit below is static.

## Review (2026-10-21)

### What's strong (keep)
- **The look.** It matches the brand: Ink/Graphite surfaces, Mint/Cobalt/Flare semantics, Space Grotesk + JetBrains Mono, tabular numerics.
- **Information architecture.** The 10-module navigation maps cleanly onto the build spec (cockpit, agents, cross-asset, lab, risk, MM, data pipeline, firehose, airdrops, tax/audit).
- **Domain patterns worth keeping:**
  - the persistent **Emergency Halt** and a **status bar** (kernel, audit trail, MCP, kill-switch armed);
  - **dead-man's heartbeat** countdown;
  - **manual social task queue** (airdrops);
  - lot-disposal ledger with holding period;
  - agent consensus with per-agent latency.
- **The Signal M decision node is echoed in the charts.**

### Responsive audit (static, from the code)

Count of Tailwind responsive prefixes per screen:

| Screen | sm | md | lg | xl | 2xl | `h-screen` | Verdict vs DESIGN.md §6 |
|---|---|---|---|---|---|---|---|
| Cockpit | 18 | 4 | 5 | 5 | 1 | 1 | Partial; tab strip overflows; primary button label clipped |
| Risk Governor | 4 | 6 | 9 | 7 | 0 | 3 | Partial; fixed status bar overlaps content; sidebar ends mid-page |
| MCP Control | 2 | 6 | 2 | 4 | 0 | 1 | Partial; same status-bar overlap |
| **Cross-Asset** | **0** | **0** | **0** | 2 | 0 | 3 | **Desktop-only**, won't reflow below ~1280 |
| Hummingbot MM | 1 | 2 | 1 | 6 | 0 | 0 | Mostly desktop; 19 grid-cols uses |
| Data Pipeline | 5 | 7 | 9 | 3 | 0 | 2 | Partial |
| Firehose | 2 | 3 | 3 | 8 | 0 | 2 | Partial |
| Order Execution | 4 | 1 | 6 | 1 | 0 | 0 | Partial; 18 grid-cols uses |
| Strategy Lab | 0 | 4 | 1 | 3 | 0 | 3 | Partial |
| Launch Radar & Tax | 2 | 1 | 4 | 4 | 0 | 2 | Partial; status bar overlaps the tax tiles; ledger table clipped on the right |
| Debate (desktop) | 4 | 2 | 5 | 1 | 0 | 0 | Partial |
| **Mobile Terminal** | **0** | **0** | **0** | **0** | **0** | 2 | **Phone-only**; no tablet/desktop or landscape path |
| **Mobile Debate** | **0** | **0** | **0** | **0** | **0** | 2 | **Phone-only**, capped at 412px |

**Cross-cutting fixes required by DESIGN.md v2:**
1. **Breakpoints:** replace Tailwind default breakpoints with the v2 set (240 → 2560 + `landscape-short`, `tablet-portrait`, `touch`).
2. **Viewport height:** replace `h-screen` with `min-h-dvh`.
3. **Grids:** add mobile-first prefixes to every unprefixed multi-column grid (`grid-cols-12/6/5/4`).
4. **Fixed bars:** the status bar and top bar must not overlap content (sticky, or fixed + spacer). The sidebar must be full height.
5. **Desktop/mobile parity:** merge each desktop/mobile pair into one responsive layout per module. Desktop screens need ph/sm/xs/xxs and landscape-short layouts; mobile screens need md+ layouts.
6. **Wide tables:** convert to card lists ≤ ph, and scroll inside their own box above that.
7. **Small text:** raise 9–10px labels to ≥ 11px and dim greys to ≥ `#8B95A5`.
8. **Native dialogs:** replace `alert()`/`confirm()` (kill switch) with an in-app confirm sheet.
9. **Production build:** compile Tailwind locally (no CDN script).

### Content corrections

Some mock-up copy doesn't match the build spec. Fix it when implementing (DESIGN.md §10).

| Where | Mock-up shows | Spec |
|---|---|---|
| Cockpit | Feed "TradingEconomics & FedWire" | Trading Economics is paid → excluded. Use FRED release dates + ForexFactory weekly JSON. |
| Cockpit, Debate | Model "Llama-3-Quant-70B" | Claude via the LiteLLM gateway (research/debate); local decision models (tier B); compiled trees (tier A) |
| Cockpit, Pipeline | "0.00ms delay", "0.12ms" everywhere | Show measured latencies with correct units |
| Risk Governor, MCP | "Binance VIP3 Colo Tokyo", "Direct Tokyo AWS HFT gateway" | Single self-hosted box; no colocation |
| MCP Control | "Claude 3.5 Sonnet"; execution/Hummingbot tools marked "Autonomous" | Current Claude model via the gateway; MCP orders default to **approve mode**; MCP is Phase 8 (built last) |
| Launch Radar | "Autonomous Sybil Task Pipeline", "Sybil-resistant task flow", auto testnet pings | No sybil/farming automation. Social and quest tasks go to the manual queue; auto-claims need an eligible hot wallet + simulation + mandate. |
| Tax Ledger | "HIFO (Tax minimised)", rulings "TR 2019/1", "TR 2014/26", "118-20" | Specific identification → FIFO fallback; cite only verified ATO references; label FY correctly; add a "not tax advice" note |
| All | Fake hashes, keys and balances | Fine as placeholders; never real keys |
