# MasterTrader

A **private, proprietary, personal-use** AI quant trading platform built from open-source parts. Currently in the **planning / research stage**.

MasterTrader will combine what the best open-source trading projects do well into one system:
- NautilusTrader's execution engine;
- Hummingbot's market making;
- TradingAgents' multi-agent decision-making;
- FinRobot's valuation tools;
- Vibe-Trading's strategy lab and safety rails.

On top of that it adds free data pipelines, social/news and global-event scrapers, RAG memory and anomaly detection, across crypto, forex, commodities, metals, stocks, ETFs, bonds and more.

## Documents

| File | Contents |
|---|---|
| [GOAL.md](GOAL.md) | What we're building and why |
| [SPEC.md](SPEC.md) | v1 specification and core decisions |
| [docs/01-repo-vetting-report.md](docs/01-repo-vetting-report.md) | Vetting of 10 open-source repos: licenses, code audit, reputation, overlap and redundancy, verdicts, and the supporting free data/memory/quant ecosystem |
| [docs/02-v1-architecture.md](docs/02-v1-architecture.md) | v1 modules, asset coverage, phased roadmap, acceptance gates |
| [docs/03-build-spec.md](docs/03-build-spec.md) | **Build spec (personal-use edition):** stack, repo layout, data model, module specs, interfaces, guardrails |
| [docs/04-plan-of-action.md](docs/04-plan-of-action.md) | Phased plan of action with checklists and a demo per phase |
| [docs/05-saas-legal-and-licensing.md](docs/05-saas-legal-and-licensing.md) | What would change licence-, data- and regulation-wise if this ever became a SaaS |
| [docs/research/](docs/research/) | Raw per-repo research notes with file-level evidence |

## Licensing stance

This is a private project for personal use only. GPL obligations start only when software is distributed, and AGPL obligations only when others use it over a network. Neither happens here, so GPL/AGPL code may be used directly. The verdicts below reflect what is **best**, not just what is licence-safe. See [docs/05](docs/05-saas-legal-and-licensing.md) for the SaaS picture. **Keep this repo private.**

## Repos vetted

| Repo | License | Verdict |
|---|---|---|
| nautechsystems/nautilus_trader | LGPL-3.0 | Adopt as core engine |
| hummingbot/hummingbot | Apache-2.0 | Adopt as a module (market making, DEX) |
| TauricResearch/TradingAgents | Apache-2.0 | Borrow its pattern and components (AI decision layer) |
| HKUDS/Vibe-Trading | MIT | Borrow components (research lab, order guard) |
| AI4Finance-Foundation/FinRobot | Apache-2.0 | Borrow components (valuation) |
| freqtrade/freqtrade | GPL-3.0 | Reference only (redundant as an engine) |
| NoFxAiOS/nofx | AGPL-3.0 | Avoid the code; borrow ideas |
| VibeTradingLabs/vibetrading | No LICENSE file | Avoid (redundant) |
| 666ghj/MiroFish | AGPL-3.0 | Reference only / experiment |
| simplifaisoul/osiris | MIT | Reference only |

> Nothing here is financial advice. No reviewed system has shown durable, cost-adjusted, out-of-sample profitability.
