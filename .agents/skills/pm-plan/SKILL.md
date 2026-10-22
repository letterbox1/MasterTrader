---
name: pm-plan
description: Plan a roadmap phase into ready-to-work kanban items - every task as a Markdown spec (goal, references, requirements, ToDo, tests/scenarios/stress verification, acceptance, exceptions, cardinal do-not rules, doc sync, branch/PR, progress log) - plus PHASE.md traceability and gap/bug items for inconsistencies found. Use when a phase has no tasks yet, when re-planning a phase, or for "scope every task", "break this phase down".
compatibility: Any Agent Skills-compatible agent (Claude Code, Codex, Gemini CLI, Cursor, OpenCode and others) working in a git repository with python3 >= 3.9; uses the ./kanban CLI from CeraNova PM.
metadata:
  author: CeraNova
  product: CeraNova PM
  version: "1.4.1"
---

# pm-plan

Follow `tracking/briefs/PLANNING_BRIEF.md` exactly. This skill is the single-phase version; for several phases at once use **pm-delegate**.

## Steps

1. **Pause triage while writing many files:** `./kanban pause`.

2. **Read:**
   - the brief;
   - `tracking/SCHEMA.md`;
   - the templates;
   - the roadmap phase doc and everything it links to;
   - the relevant code.

3. **Write `tracking/phase-N/PHASE.md`:**
   - summary, entry/exit criteria;
   - workstreams, critical path;
   - **full traceability** (every R and T ID → tasks);
   - risks, cross-phase prerequisites.

4. **Write the tasks.**
   - **Create:** `./kanban new --phase N --title "…" --type BUILD|USER|… [--depends P2-T003]` creates each from the template with the next ID. Then fill every heading with specific content. Sizes XS–L. Each task is one branch and one PR.
   - **Dependencies:** `depends_on` within the phase only.
   - **USER tasks:** human-only steps with exact instructions.
   - **VERIFY tasks:** dedicated items for the roadmap checks, end-to-end scenarios, stress/failure injection, and **one final phase exit-demo** item.
   - **Parallel by default:** `depends_on` holds only real preconditions, so independent tasks run side by side (and across phases when `phase_gating` is `"dependencies"`).
   - **Build first, keys last:** integrations are built and tested against mocks, fixtures, emulators or sandboxes without secrets; the live check that needs real keys, accounts or money is a separate late VERIFY task depending on the USER task that provides them.
   - **Scope what each task needs to run**, in its front matter:
     - `tools`: CLIs that must be on PATH (`[git, node>=20, docker]`);
     - `mcp`: MCP servers the agent will call (`[github, postgres]`);
     - `env`: environment variable **names** for keys and settings (`[STRIPE_API_KEY]`), never values;
     - `services`: external services or accounts to confirm (`[staging-db]`).
     Put project-wide needs in `requires_defaults` in `tracking/kanban.config.json` instead of repeating them. For anything the human must provide (an account, a key, a paid plan), add a USER task and make the task depend on it. Don't list skills: agents pick skills by description, and write their own only when a task needs one (see **pm-execute**).

5. **Write gaps:** `./kanban new --phase N --kind gap --severity S1–S4 --title "…"` for each inconsistency or unknown found, with wrong / expected / suggested fix.

6. **Validate:** `./kanban validate --phase N` must show 0 errors and 0 warnings.

7. **Resume:** `./kanban pause --off && ./kanban build`. Check the phase board (`tracking/phase-N/BOARD.md`) and `kanban.html`.

8. **Commit** (`plan: phase N (<x> tasks, <y> gaps)`).

9. **Report:** counts by type, coverage, gaps by severity, cross-phase prerequisites. If there are S1/S2 gaps, offer **pm-reconcile**.

## Quality bar

- Specific beats generic: real file paths, modules, endpoints, assets, numbers.
- Every BUILD/OPS task carries its own tests.
- Every task lists the tools, MCP servers, env var names and services it needs, so `./kanban preflight` can check them before anyone starts.
- Configurable values point at the configuration doc instead of hard-coding them.
