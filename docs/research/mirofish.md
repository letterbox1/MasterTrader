_Raw notes from the research agents. They back up [../01-repo-vetting-report.md](../01-repo-vetting-report.md). File paths refer to each upstream repo at its 2026-10-21 HEAD._

# MiroFish (666ghj/MiroFish) — AGPL-3.0 — Verdict: Reference only / walled-off experiment
- Wrapper over CAMEL-AI OASIS (Apache-2.0) + Zep Cloud (mandatory, no local fallback). Flask backend ~30.7k LOC, Vue frontend ~21k LOC.
- Flow: docs -> Zep graph (backend/app/services/graph_builder.py) -> LLM personas w/ unseeded random fields (oasis_profile_generator.py) -> simulated Twitter/Reddit ~72 rounds default (simulation_config_generator.py:88-95, scripts/run_parallel_simulation.py) -> ReportAgent (report_agent.py:925).
- No calibration/accuracy/backtest; non-deterministic (temp 0.3-0.7, no seed); backtests contaminated by LLM hindsight. README warns high token consumption, suggests <40 rounds.
- One unverified anecdote: modified fork, 338 Polymarket trades, +$4,266, edge on political not financial markets.
- LLM: any OpenAI-compatible (default qwen-plus). Replacing Zep = rewrite ~6 modules.
- Last commit 2026-10-02, ~322 commits, 68 open issues, 91 open PRs, no releases. 18 test files; CI only builds Docker.
- Security: no API auth, CORS * (backend/app/__init__.py:43), default SECRET_KEY 'mirofish-secret-key' (backend/app/config.py:21), dev servers in Docker. No eval/pickle/shell on LLM output, no hardcoded keys, no telemetry.
- ~80.9k stars/12.3k forks; star history consistent with viral news spike Mar 2026 (student Guo Hangjiang, ~10-day vibe-coded build; reported 30M RMB from Shanda's Chen Tianqiao). Coverage mostly promotional.
- Overlap: complementary (crowd-reaction modeling) to TradingAgents/FinRobot/Vibe-Trading; can sit downstream of osiris.
- Pattern: isolated private service, HTTP-only boundary, public fork for patches; or clean-room rebuild on OASIS + local LLM + own memory.
Sources: https://github.com/666ghj/MiroFish https://emelia.io/hub/mirofish-ai-swarm-prediction https://eu.36kr.com/en/p/3715147673006213 https://news.pedaily.cn/202603/561503.shtml https://www.abhs.in/blog/mirofish-1m-agents-why-trading-fails-public-opinion-wins-2026
