# Research agendas by project type

Each track names the decision it feeds. Select the tracks for open decisions only; order roughly by dependency.

## Universal tracks (any project)

| Track | Feeds |
|---|---|
| Constraints check: budget, free-tier-only, licences allowed, jurisdiction, deadlines | GOAL constraints, SPEC non-negotiables |
| Legal & compliance for the jurisdiction (privacy, consumer law, sector rules, accessibility law) | SPEC, configuration, USER tasks (advice) |
| Costs & quotas of every external service | Configuration defaults, roadmap risks |
| Security & supply chain of dependencies | SPEC, security doc |

## greenfield (new build from scratch)

| Track | Feeds |
|---|---|
| Problem & prior art: who already solves this, how, what users complain about | GOAL, non-goals, differentiation |
| Build-vs-buy-vs-adapt: open-source projects to reuse or fork (licence, health, fit) | SPEC core decisions |
| Stack selection: language, framework, data store, hosting; ecosystem maturity, hiring, cost | SPEC, ARCHITECTURE |
| Architecture patterns & reference designs for this problem class | ARCHITECTURE |
| Feasibility spikes: time-boxed prototypes for the riskiest assumptions | Roadmap phase 0, risks |
| Data sources / APIs / vendors: free tiers, terms, rate limits | SPEC, configuration |
| Cost model: hosting, services and licences at expected scale | GOAL constraints, roadmap |
| Delivery: CI/CD, environments, release channels, app stores | Roadmap ops tasks |

## software (existing codebase)

| Track | Feeds |
|---|---|
| Dependency health: outdated or abandoned packages, licences, advisories | Gap items, upgrade tasks |
| Upgrade paths for frameworks/runtimes (breaking changes, migration guides) | Roadmap, tasks |
| Alternatives for pain points (performance, cost, maintainability) | Decisions register |
| Benchmarks / profiling references for SLOs | Configuration, VERIFY tasks |
| Observability & operations tooling | ARCHITECTURE, ops tasks |

## data-ml

| Track | Feeds |
|---|---|
| Datasets: availability, licence, provenance, bias, PII | SPEC, data terms in configuration |
| Model options (open/closed, size, licence, serving cost, latency) | SPEC, ARCHITECTURE |
| Evaluation: benchmarks, metrics, leakage risks, baselines | VERIFY tasks, gates |
| Compute & cost (GPU, cloud credits, free tiers) | Configuration, roadmap |
| Privacy, consent and regulation for data use and AI | SPEC non-negotiables |

## media-video / media-audio (film, video, podcast, music)

| Track | Feeds |
|---|---|
| Delivery specs per platform (resolution, codec, bitrate, loudness LUFS, captions, aspect ratios) | Configuration, VERIFY checklists |
| Toolchain & pipeline (NLE/DAW, proxies, colour, versioning, Git LFS) | ARCHITECTURE (pipeline) |
| Rights & clearances (music, footage, fonts, likeness, locations), licence terms | USER tasks, SPEC |
| Distribution & monetisation platform rules | Roadmap release phase |
| Accessibility (captions, audio description, transcripts) | Requirements, VERIFY |
| Audience & comparable titles | GOAL |

## game

| Track | Feeds |
|---|---|
| Engine choice (licence/royalties, platforms, tooling) | SPEC |
| Platform certification and store requirements | Roadmap, VERIFY |
| Performance budgets per platform | Configuration, VERIFY |
| Asset store/licensing, middleware | SPEC, USER tasks |
| Monetisation rules (loot boxes, age ratings, regional law) | SPEC non-negotiables |
| Comparable games & player expectations | GOAL |

## docs (documentation, books, courses)

| Track | Feeds |
|---|---|
| Audience & existing material (gaps, competitors) | GOAL |
| Publishing platforms/formats (static site, LMS, print/ePub specs) | ARCHITECTURE |
| Style guides, accessibility (WCAG), localisation | Configuration, VERIFY |
| Rights for quoted/third-party material | USER tasks |

## research (academic / R&D)

| Track | Feeds |
|---|---|
| Literature review & state of the art | GOAL, SPEC (hypotheses) |
| Methods & experimental design, pre-registration | Roadmap, VERIFY |
| Datasets, instruments and tools | SPEC |
| Ethics approvals, consent, data management plans | USER tasks, SPEC |
| Publication venues & deadlines | Roadmap fixed dates |

## design (brand, product, UX)

| Track | Feeds |
|---|---|
| Users & jobs-to-be-done (desk research, existing studies) | GOAL |
| Competitor/pattern audit | Scope docs (**pm-scope**) |
| Design systems & component libraries (licence, accessibility) | DESIGN, ARCHITECTURE |
| Accessibility standards | Requirements, VERIFY |
| Font/asset licensing | USER tasks |
