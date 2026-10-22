---
name: pm-roadmap
description: Turn a project's goal/spec/architecture into a phased roadmap - one doc per phase with requirement IDs (R), typed ToDos (T: USER/BUILD/OPS/VERIFY/RUN/DOC), exit criteria and risks, plus the roadmap index with timeline, dependencies, fixed dates, user-action register and traceability - and create the matching kanban phases. Use when there's no roadmap yet, when re-phasing, or when the user asks "scope each phase", "plan of action", "roadmap".
compatibility: Any Agent Skills-compatible agent (Claude Code, Codex, Gemini CLI, Cursor, OpenCode and others) working in a git repository with python3 >= 3.9; uses the ./kanban CLI from CeraNova PM.
metadata:
  author: CeraNova
  product: CeraNova PM
  version: "1.4.2"
---

# pm-roadmap

## Steps

1. **Read** goal/spec/architecture/configuration/decisions docs, the codebase state and any existing plan.

2. **Choose phases.**
   - **Platform/foundations first, risky unknowns early.**
   - Each phase ends with a usable demo.
   - Optional work comes last.
   - Typically 4–10 phases; name them by outcome.
   - Decide each phase's prerequisites (`opens_after`).
   - **New builds and big unknowns:** start with a **Discovery & research** phase. It holds `RESEARCH` tasks (one per track from **pm-research**) and time-boxed feasibility spikes, and its exit criterion is "decisions recorded in SPEC/configuration".

3. **Create them:** `./kanban init --phases "Foundations,Core,…" --roadmap` for a new project, or `./kanban phase-add --title "…" --roadmap [--opens-after 2,3]` per phase. This creates `tracking/phase-N/PHASE.md` and `docs/roadmap/phase-N-<slug>.md` from the templates, plus `docs/roadmap/README.md` if missing.

4. **Fill each roadmap phase doc** (`docs/pm/templates/roadmap/phase.md` structure):
   - Header table: goal, duration, depends/unlocks, components, primary docs.
   - **Scope in/out**, **entry criteria**.
   - **Requirements** table: `R<N>.<nn>` with source link and "verified by"; non-functional as `R<N>.N<n>`.
   - **ToDo sets** A–F by type, each line `- [ ] **T<N>.<nn>** \`TYPE\` text → R<N>.xx · link`.
     - USER items: everything only the human can do (accounts, credentials, purchases, approvals, decisions, reviews, external advice), with deadlines.
     - VERIFY: tests, drills, reviews proving the requirements.
     - RUN: elapsed-time items. Anything that outlasts the phase is "start X" here and checked later.
   - **Deliverables**, **Exit criteria** (observable), **Risks**.

5. **Fill the roadmap index** (`docs/roadmap/README.md`):
   - phase table with indicative dates;
   - how to read;
   - the work-mix and user-register **marker blocks** (auto-filled by `./kanban build`; don't edit their contents);
   - timeline (Mermaid gantt + dependency flowchart);
   - critical path and parallel tracks;
   - fixed external dates;
   - cross-phase tracks;
   - traceability (spec non-negotiables → R IDs; goal capabilities → phases; components → phases; docs → phases);
   - definition of done.

6. **Copy** each phase's exit criteria into `tracking/phase-N/PHASE.md`.

7. **Build and verify:** `./kanban build`. The roadmap status, counts and user register blocks fill in. Check the links resolve.

8. **Checkpoint with the human:** show the phase list, the `USER` action register (what they'll need to do, and when) and the fixed dates. Adjust if needed.

9. **Commit** (`roadmap: phases 0–N`), then **pm-plan** (or **pm-delegate** to plan all phases in parallel).
