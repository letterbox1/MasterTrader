_Raw notes from the research agents. They back up [../06-aggregators-and-market-providers.md](../06-aggregators-and-market-providers.md)._

# listeningkit & log (matthewdonsemail-lab) — B2B lead-gen social listening, not market aggregators
## listeningkit = GitHub fork of obris-dev/openmagpie (v0.8.0, 2026-07-23)
- Fork 9★/3 forks/279 commits; upstream 70★/6/283. README/CHANGELOG (113+ links)/release-please package-name "openmagpie"/packages/openmagpie-schema all upstream. Fork addition (U): X connector apps/core/sources/connectors/twitter/* (~570 LOC, twikit cookies, "ported from listeningkit").
- License: Apache-2.0 (Copyright Obris LLC) except `ee/` (reserved, ee/LICENSE absent) — open-core.
- Python 3.13 Django+Postgres (apps/core), Typer CLI `magpie`, Next.js web; ~51k LOC. Feed(sources)->poll->FeedItem; Watch -> semantic_filter (LLM vs NL criterion) -> webhook/log/extract. Sources: Reddit RSS, HN Algolia, GitHub, any RSS/Atom, X (twikit); FlareSolverr sidecar. BYO OpenAI-compatible LLM (Ollama). Fully self-hostable.
- Quality: CI ruff/ty/shellcheck/tests, 63 test files, release-please, SSRF-pinned client (common.safe_http).
- Flags: PostHog telemetry default-on with baked key (apps/core/conf/settings/base.py:530) -> set POSTHOG_API_KEY empty / DO_NOT_TRACK; unpinned twikit from git fork (unclecode/twikit); `curl openmagpie.ai | sh` installer; flaresolverr:latest. No eval/obfuscation.
- Verdict: Reference only (use upstream openmagpie). Patterns: Feed->Watch->action chain, connector registry, LLM semantic_filter as cheap relevance gate before FinBERT.
## log ("Log by ListeningKit") — Convex "All Gas" hackathon entry (hackathon.md, SUBMISSION.md)
- MIT, "ListeningKit Contributors"; credits Matthew Dons, PACER1, deepmroot, john11099 (README.md:341); 25★/6 forks/164 commits; last commit 2026-10-19.
- TS: Convex backend, React/Vite/Clerk dashboard, Hono bridge, MV3 Chrome extension, Python Camoufox/Playwright helpers; ~60k LOC.
- Sources: Reddit (OAuth/RSS/Arctic Shift mirror, convex/reddit.ts:6), X & Facebook via logged-in session browser automation + mandatory residential proxy (convex/lib/proxy.ts).
- Hosted deps: Convex cloud, OpenAI gpt-4o-mini (convex/lib/scoring.ts), Firecrawl, AgentMail, Clerk, Bark, R2, Vercel.
- Flags: extension takes cookies permission for reddit/x/facebook and uploads session cookies (apps/extension/manifest.json); clients/x_push.py "Use an account you can afford to lose"; FB group auto-join; leftover debug scripts; no CI; twikit engine broken.
- Verdict: Avoid.
Sources: github.com/matthewdonsemail-lab/listeningkit, github.com/obris-dev/openmagpie, github.com/matthewdonsemail-lab/log
