# Task Alignment Brief (wave 2, after the 2026-10-21 decisions)

The docs now carry the decisions in [`docs/16`](../docs/16-configuration-and-safety-model.md) (configuration layers, defaults, failure safety, valuation, live inputs) and [`docs/17`](../docs/17-decisions-register.md) (the decision for each planning gap). Your job is to bring **one phase's** kanban items in line with them.

The kanban hooks and CLI triage are **paused** during this wave (`tracking/.state/paused`). `./kanban` commands still work, but don't rebuild boards. Don't run `./kanban build` or `./kanban pause --off`; the main agent does that.

## Steps

1. **Read** `docs/16`, `docs/17`, `tracking/SCHEMA.md`, `tracking/PLANNING_BRIEF.md` and your roadmap phase doc (`docs/roadmap/phase-N-*.md`). The roadmap doc has new requirement and ToDo IDs (listed in your prompt).

2. **Update existing tasks** in `tracking/phase-N/tasks/` wherever a decision changes them:
   - **Numbers become configurable defaults** with a link to the 16 section (no hard-coded limits). Modes are `paper`/`hitl`/`autonomous`. Use the canonical audit/table names, `ops.wallets`, venue cap 25%, DSR ≥ 0.95, two-stage drawdowns, the three-layer dead-man, the MCP rules, etc.
   - Fix any task that contradicts a decision. Keep each task's ID, file name and structure; edit content and front matter (`requirements`, `roadmap_todos`, `depends_on`, `doc_sync`). Add a progress-log line: `- 2026-10-21 00:00 · aligner · updated for docs/16–17 (<what changed>)`.

3. **Create new tasks** for the new roadmap ToDos/requirements in your phase. Use the next free IDs in your phase (`./kanban new --phase N --title "…" --type …` creates the file from the template, then fill it in fully per the planning brief). Include tests, scenarios, stress/failure injection, exceptions and cardinal rules. Wire `depends_on` within the phase, and add the new tasks as dependencies of the phase exit-demo task where they're part of the exit.

4. **Close resolved gaps** in `tracking/phase-N/bugs/`. A gap is resolved when 17 records its decision **and** the aligned docs now carry it (check the doc text).
   - Edit the gap's `## ToDo` / `## Acceptance criteria` so they describe the spec-level resolution, and tick them.
   - If the gap still implies implementation work, make sure an existing or new **task** owns it, and name that task ID in the gap's progress log.
   - Then run `./kanban done <ID> --evidence "decided in docs/17 (<row>); docs updated: <files/sections>; implementation owned by <task IDs or n/a>"`, then `./kanban docsync <ID> --done --note "docs already updated in this wave"`.
   - If the aligned docs **don't** yet carry the decision, leave the gap open, add a progress-log line saying what's missing, and report it.
   - Gaps that need a real-world check marked (U) (e.g. a series ID to verify) stay open, become S3/S4 if they were S2, and get owned by a task.

5. **Update `PHASE.md`:** traceability (new requirements/ToDos → tasks), exit criteria if the roadmap's changed, workstreams and critical path. Keep the front matter as is (except `updated`).

6. **Validate:** `python3 tools/kanban/kanban.py validate --phase N` must show **0 errors and 0 warnings** for your phase.

## Rules

- Edit only `tracking/phase-N/`. Report doc problems; don't fix them.
- Don't delete items. If a task is obsolete, run `./kanban cancel <ID> --reason "…"`.
- Every gap you close must cite its evidence (doc + section).

## Report (≤ 250 words)

- Tasks updated (count + notable).
- New task IDs.
- Gaps closed (IDs).
- Gaps left open (IDs + why).
- Any doc that still contradicts 16/17.
