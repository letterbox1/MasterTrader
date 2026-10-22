# Research methods and checklists

## Source quality (best first)

1. **Primary:** official docs, specs and standards; licence files; source code; regulator texts; vendor pricing and terms pages; peer-reviewed papers.
2. **Authoritative secondary:** maintainers' posts, release notes, reputable industry analysis.
3. **Community:** forums, Reddit, Hacker News, Discord, reviews. Use these as **signals** (pain points, reputation), never as sole evidence for a fact.

**Record every source:** title, URL, date accessed, and the fact taken from it. Facts that change (prices, limits, versions, laws) get the date in the sentence.

## Repo / open-source vetting

| Check | Look at |
|---|---|
| Licence | The licence file, licence changes in history, dual licensing, commercial-use limits |
| Activity | Last release/commit, maintainers, bus factor, issue/PR response |
| Quality | Tests, CI, docs, typed APIs, breaking-change history |
| Security | Advisories, dependency audit, secret handling |
| Code red flags | Grep for telemetry, analytics SDKs, referral/affiliate IDs, `eval`/exec of remote code, unexpected network calls, obfuscation |
| Fit | Does it do the job? Extension points; what we'd rewrite |
| Reputation | Stars and forks are weak signals; community sentiment |

## Vendor / API / data-source vetting

| Check | Look at |
|---|---|
| Free tier | Quota, rate limits, overage behaviour |
| Terms | Commercial use, redistribution, scraping, AI/training use, retention, attribution |
| Coverage | Regions, assets/formats, history depth, latency |
| Reliability | Status page, SLA, deprecation history |
| Lock-in | Export, standards, alternatives |

## Feasibility spike (time-boxed)

1. **Hypothesis:** "X can do Y within Z".
2. **Time box:** hours or days.
3. **Smallest experiment:** the least code/content that proves or refutes it.
4. **Result:** measured numbers, a decision, and what the real build should do.
5. **Throwaway** unless the decision says otherwise. The finding goes in the report, not the main branch.

## Cost model

Unit costs × expected volume, at three scales (now, 10×, 100×), plus fixed costs. Show which free tiers run out first.

## Compliance scan

1. Jurisdiction(s) and the activities that matter.
2. The rules that apply, citing the primary text.
3. What they require of us.
4. What needs a professional (a USER task for the human: lawyer, accountant, auditor).

Never present this as legal advice.

## Synthesis (deep research)

- One report per track.
- A synthesis that states the decision options with trade-offs, the recommendation, and what would change it.
- Conflicts between tracks are listed explicitly.
