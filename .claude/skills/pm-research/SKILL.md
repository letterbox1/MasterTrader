---
name: pm-research
description: Research for any project type, out of the box - picks the right research spectrum from what the project is (greenfield build, existing codebase, data/ML, media/film/audio, game, docs/course, academic research, design) and produces cited, dated reports - landscape and prior art, build-vs-buy, stack/tool/vendor/repo vetting, feasibility spikes, licences and compliance, costs and free tiers, audience/market, standards and delivery specs. Use whenever a decision needs outside facts, for "research X", "compare options", "vet these repos/tools", "is this feasible / allowed / free", "deep research", or when pm-intake, pm-roadmap or pm-reconcile hits an unknown.
compatibility: Any Agent Skills-compatible agent (Claude Code, Codex, Gemini CLI, Cursor, OpenCode and others) working in a git repository with python3 >= 3.9; uses the ./kanban CLI from CeraNova PM. Web research needs the agent's web/search tools; without them the skill produces a question list for the human.
metadata:
  author: CeraNova
  product: CeraNova PM
  version: "1.3"
---

# pm-research

**Goal:** every decision that depends on the outside world rests on current, cited facts, kept as reports in the repo rather than lost in chat. Research adapts to the project: a greenfield app, a film edit and a PhD thesis need different questions.

## 1. Identify the project type (seconds)

Run `./kanban detect`. It reads the repo (manifests, file types, engines, notebooks, media) plus `project_type` in `tracking/kanban.config.json`, and prints the type and the signals it used. Confirm it against GOAL/SPEC. If it's wrong, set `"project_type"` in the config.

Types:
- `greenfield` (empty or nearly empty repo)
- `software`
- `data-ml`
- `media-video`, `media-audio`
- `game`
- `docs` (docs/books/courses)
- `research` (academic/R&D)
- `design`
- `mixed`

## 2. Pick the research spectrum

Open [references/research-agendas.md](references/research-agendas.md) and take the agenda for the type. Each agenda lists the standard research tracks for that kind of project, with the decision each track feeds. For example:
- **greenfield:** problem and prior art → build-vs-buy → stack → architecture patterns → feasibility spikes → cost and hosting → licences;
- **media:** formats/codecs and delivery specs → toolchain → rights and clearances → distribution platforms → accessibility.

Select only the tracks that feed open decisions. Ask the human only about scope, budget, jurisdiction and taste.

## 3. Choose the depth

| Depth | When | Output |
|---|---|---|
| **Quick scan** | One factual question, low stakes | 3–5 sources, a short note in `docs/research/` |
| **Standard report** | A real decision (tool, vendor, approach) | Report from [assets/report-template.md](assets/report-template.md) |
| **Deep research** | Many tracks or high stakes (stack choice for a new build, legal/compliance, big spend) | Research plan ([assets/research-plan.md](assets/research-plan.md)) → one agent per track via **pm-delegate** → per-track reports → a synthesis report |

**Long research becomes kanban work:** create `RESEARCH` tasks (`./kanban new --phase N --type RESEARCH --title "…"`). The task's deliverable is the report path, and its acceptance criterion is "decision doc updated with link".

**New builds:** pm-roadmap should start with a **Discovery & research** phase holding these tasks plus time-boxed **feasibility spikes**. Spikes are `BUILD` tasks whose acceptance is a written finding.

## 4. Do it properly

Follow [references/methods.md](references/methods.md):
- **Sources:** prefer primary sources; date every source; repeat the key facts verbatim.
- **(U)** marks anything unverified.
- **Checklists** for repos/vendors (licence, activity, security, telemetry, terms), feasibility spikes, cost models and compliance.
- **Without web tools:** write the questions for the human and stop.

## 5. Land it

1. Save reports in `docs/research/<topic>.md` (or `docs/research/<track>/…` for deep research).
2. Link them from the docs index.
3. Update the doc the decision belongs in (SPEC core decisions, configuration defaults, decisions register, roadmap) with a one-line conclusion and the link.
4. Open questions become gap items or questions for the human (**pm-reconcile**).

## Don't

- Don't cite what you didn't read, and don't present (U) claims as facts.
- Don't recommend options the project's constraints exclude (budget, licence, jurisdiction, non-goals). List them as "excluded because …".
- Don't let research sprawl: every track must name the decision it feeds.
