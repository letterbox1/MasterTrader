---
name: pm-scope
description: Deep-scope one area of the product before planning tasks - UI screens/dashboards, components and design system, API contract, data model, integration, content/media pipeline - into per-unit scope docs (purpose, layout/structure, data shown or exchanged, actions with confirmation levels, states incl. empty/loading/error, responsive or format rules, acceptance criteria, backend/data contract) that roadmap phases and tasks link to. Use for "scope out the UI / dashboards / API / pipeline", "design system", when a roadmap phase is too vague to plan, or when tasks need a shared contract.
compatibility: Any Agent Skills-compatible agent (Claude Code, Codex, Gemini CLI, Cursor, OpenCode and others) working in a git repository with python3 >= 3.9; uses the ./kanban CLI from CeraNova PM.
metadata:
  author: CeraNova
  product: CeraNova PM
  version: "1.4.1"
---

# pm-scope

**Goal:** a contract per unit (screen, endpoint group, pipeline stage, asset type). Planning agents then write tasks against it instead of guessing.

## Steps

1. **Pick the area and its units.** Base the list on the architecture doc, the roadmap and the code, and confirm it with the human if it's a product choice. Examples:
   - UI: one doc per dashboard/screen;
   - API: per resource group;
   - pipeline: per stage;
   - design: tokens, components, responsive rules.

2. **Create the area index:** `docs/<area>/README.md`. It holds the information architecture or list of units, shared rules (states, numbers/formatting, confirmation levels, accessibility, permissions), and a phase-by-unit table.

3. **Write one doc per unit** from `docs/pm/templates/scope-unit.md`:
   - purpose;
   - structure by size/format (breakpoints for UI, payload shapes for API, specs for media);
   - widgets/fields and their data sources;
   - actions, with who may do them and how they're confirmed;
   - states (empty, loading, error, degraded, permission);
   - acceptance criteria;
   - the backend/data contract (endpoints, events, files) it relies on.

4. **Shared design/system rules** (for UI):
   - tokens, typography, spacing, components;
   - a **test matrix** of viewports/devices or formats every unit must pass;
   - a content style.

   Record it in a `DESIGN.md` (or the area index) that the units reference.

5. **Cross-check** against the architecture/API docs. Mismatches become gap items or are fixed in the contract docs. Every action must exist in the command/API catalogue, and every data field must have a source.

6. **Link from the roadmap:** each phase that builds units lists them. **pm-plan** then turns units into tasks, typically one per widget group or endpoint plus a VERIFY item per unit for its acceptance criteria and test matrix.

7. **Commit** (`scope: <area>`).
