# Phase Execution Brief (for build agents)

Give this to an agent (Claude Code cloud or local, or any CLI agent) that should **execute** a phase's tasks. One agent per phase. Several phases can run at once when their `opens_after` prerequisites are met.

## Prompt template

> You are the execution agent for **Phase N** of MasterTrader. Read `AGENTS.md`, `tracking/README.md`, `tracking/phase-N/PHASE.md` and `docs/roadmap/phase-N-*.md`. Then loop:
> 1. `./kanban resume`. If a Phase-N item is `in_progress`, finish it first (read its checkpoint and progress log; check out its branch).
> 2. Otherwise `./kanban next --phase N --owner agent`, then `./kanban start <ID> --git`. `start` runs the **preflight** (the `tools`, `mcp`, `env` names and `services` the item lists). If something only the user can provide is missing (keys, accounts, money), block the item (`./kanban block <ID> --reason "needs …"`), make sure a USER task covers it, and pick another.
> 3. Implement exactly what the item file specifies. Use the skills you have; write a project skill (`.agents/skills/mastertrader-<name>/`, then `./kanban doctor --fix`) only for a procedure you'll repeat. Tick ToDo boxes as you go and `./kanban checkpoint <ID> "…"` after each step. Commit and push with the item ID in the message.
> 4. Run every test, scenario and stress check listed under *Verification*. Paste the commands and results into the progress log.
> 5. File any defect you find (search first: `./kanban list --grep "…"`; **pm-triage**) with `./kanban new --phase N --kind bug …`. Fix it only if it's in scope.
> 6. Open a PR (title `<ID>: <title>`), then `./kanban review <ID> --pr <url>`. Get an independent review (**pm-review**, a separate agent: `./kanban reviewed <ID> --pass|--fail --note "…"`); risk, `pit`, WORM, tax and money-path items always get one. After merge, `./kanban done <ID> --evidence "…"`.
> 7. Do the doc sync the Stop hook asks for (spec, roadmap, architecture, UI docs; **tick the roadmap ToDo**), then `./kanban docsync <ID> --done`.
> 8. Repeat until nothing is ready for agents in Phase N. Then list what's waiting on the user (`./kanban next --phase N --owner user`) and stop with a handoff (`./kanban session handoff --note "…"`, commit, push).
>
> Never do `owner: user` items yourself. Never bypass the cardinal rules in `AGENTS.md`. If you hit a limit or the session is about to end, checkpoint and push first.

## Rules of engagement for parallel agents

- **One claim per item:** `start` records `claimed_by`. Don't take an item another session claimed in the last 24 h unless its progress log says it was handed off.
- **Phase boundaries:** only Phase-N files, plus the code those items touch. A cross-phase change becomes a gap item in the other phase.
- **Shared files** (spec, architecture, roadmap README): keep edits small and focused on the item; pull and rebase before pushing.
- **Generated files** (`KANBAN.md`, `kanban.html`, `BOARD.md`, `DOC_SYNC.md`): never hand-edit. On a merge conflict, take either side and run `./kanban build`.

## Phase completion

When the last item is done, tick the `PHASE.md` exit criteria from the evidence in the exit-demo item's log, then run `./kanban build`. The phase flips to `done` and the next phase opens. Do the phase doc sync (`./kanban docsync P<N> --done`) and report.
