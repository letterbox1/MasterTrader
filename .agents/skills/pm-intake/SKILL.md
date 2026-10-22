---
name: pm-intake
description: Build or refresh a project's foundation docs (goal, spec, architecture, docs index) from the codebase, existing docs and the human's input, using the CeraNova PM templates, and record unknowns as gaps. Use after pm-bootstrap, when a project has no clear goal/spec, when joining an existing codebase, or when the human describes what they want built.
compatibility: Any Agent Skills-compatible agent (Claude Code, Codex, Gemini CLI, Cursor, OpenCode and others) working in a git repository with python3 >= 3.9; uses the ./kanban CLI from CeraNova PM.
metadata:
  author: CeraNova
  product: CeraNova PM
  version: "1.3"
---

# pm-intake

**Goal:** the project's intent and shape written down, so a roadmap can be phased from it. **Infer first, ask second:** only ask the human what the code and docs can't tell you.

## Steps

1. **Inventory:**
   - README, `docs/`, ADRs, issue templates, CI config, package manifests;
   - entry points, modules, tests, data/asset folders;
   - deployment files, licences;
   - anything the human attached.

   For media projects: asset types, formats, tools, pipelines, naming, review flow.

2. **Draft from the templates** in `docs/pm/templates/`:
   - `GOAL.md`: what, for whom, why; capabilities; non-goals; constraints.
   - `SPEC.md`: core decisions + numbered non-negotiables.
   - `ARCHITECTURE.md`: components or pipeline stages, data/assets, interfaces, flows, failure handling, layout.
   - `configuration.md` (if the project has tunable behaviour): layers + defaults. **Nothing that users may want to change is hard-coded.**

   **Placement:**
   - Existing docs with the same purpose → **update them in place** (keep their headings and anchors) instead of duplicating.
   - New docs → `GOAL.md`/`SPEC.md` at the root (or wherever the project keeps top-level docs), others under `docs/` numbered in reading order (`docs/01-…`).

   Replace every `<!-- pm:fill … -->` marker with real content, or a clearly marked `(U)` unknown.

3. **Ask the human, in one batch,** only for what's still unknown and matters for phasing:
   - goals, constraints, deadlines, budget;
   - what's off-limits;
   - who does what (USER items).

   Offer your best guess for each so they can just confirm.

4. **Record gaps:** each unresolved inconsistency or unknown becomes a gap item once phases exist (`./kanban new --phase N --kind gap --severity S? --title …`). Before phases exist, list them at the end of the spec under "Open questions", and pm-roadmap converts them.

5. **Docs index:** make sure the project README (or `docs/README.md`) lists every doc with a one-line purpose.

6. **Facts and contracts:** check the type with `./kanban detect`.
   - **Greenfield projects (built from scratch)** get a research pass first: prior art, build-vs-buy, stack, feasibility.
   - **Existing codebases** get dependency/upgrade research.
   - **Media, data, game, docs and research projects** each have their own agenda (**pm-research**).

   Beyond that: if a decision needs outside facts, use **pm-research**. If an area (UI, API, pipeline) needs a detailed contract before phasing, use **pm-scope**.

7. **Commit** (`docs: intake`), then continue with **pm-roadmap**, or **pm-doc-ingest** if the human gave you external material.

## Don't

- Don't invent requirements the human didn't ask for and the code doesn't imply. Mark them as suggestions.
- Don't rename existing headings: other docs and tasks link to their anchors.
