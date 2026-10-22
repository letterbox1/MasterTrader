# CeraNova PM skills

The skills are written in the open **Agent Skills** format (`SKILL.md` with `name` + `description` frontmatter; optional `references/` and `assets/`). The source is `skills/pm-*/` in the kit; `install.py` copies them into:
- **`.claude/skills/`** for Claude Code (OpenCode reads it too);
- **`.agents/skills/`** for Codex, Gemini CLI and other agents that read the open-standard location.

Choose with `--agents claude,agents`. Agents load a skill when its description matches the task, or when you name it ("use pm-reconcile"). Agents without skill support can read the same files as step-by-step playbooks; `AGENTS.md` points to them.

| Skill | Use when | Produces |
|---|---|---|
| **pm-lifecycle** | You're unsure where you are; "set up project management" | Routes to the right skill |
| **pm-doctor** | Something misbehaves; "what's next?"; after cloning or moving machines | `./kanban doctor --fix` repairs; ordered next lifecycle steps |
| **pm-bootstrap** | No `tracking/kanban.config.json` yet; kit just copied in | Config, phases folder, merged hooks and protocol blocks, first board |
| **pm-intake** | No clear goal/spec; joining an existing codebase; the human describes the project | GOAL, SPEC, ARCHITECTURE (+ configuration) docs from templates; open questions |
| **pm-doc-ingest** | The human hands over other docs/specs/research | Review doc (dropped / added / conflicts / not adopted); merged docs |
| **pm-research** | A decision needs outside facts (tools, repos, vendors, licences, prices, regulation) | `docs/research/<topic>.md` with dated sources, (U) flags, recommendation |
| **pm-scope** | An area needs a detailed contract (UI screens + design system, API, data, pipeline) | `docs/<area>/` index + per-unit scope docs |
| **pm-roadmap** | No roadmap, or re-phasing | `docs/roadmap/` phase docs with R/T IDs, index with timeline and registers; `tracking/phase-N/` |
| **pm-plan** | A phase needs its tasks | `PHASE.md`, task files, gap items |
| **pm-delegate** | Work spans phases or many docs | Parallel agents with disjoint scopes; merged, validated result |
| **pm-reconcile** | Gaps need decisions; the human answers or questions open issues | Configuration doc, decisions register, doc + task alignment waves, closed gaps |
| **pm-execute** | "Next task", "execute phase N", resume after a crash | Implemented, verified items with evidence |
| **pm-review** | An item is in review or about to be marked done; "check P2-T014 is really done" | Independent pass/fail verdict with findings (`./kanban reviewed`) |
| **pm-triage** | A bug report or request arrives; CI or a review fails; stale or blocked items | Deduplicated, classified, linked items; groomed board |
| **pm-doc-sync** | Stop hook asks; `DOC_SYNC.md` has items; phase completed | Docs matching reality; roadmap ToDos ticked |
| **pm-status** | "Where are we?", "show the board", handoff, switching machines | Progress summary; board; handoff log |

## Skills an agent writes for itself

The kit doesn't assign skills to tasks. Each task lists what it needs to **run** (`tools`, `mcp`, `env`, `services`; checked by `./kanban preflight`), and agents pick skills by description. When a task repeats a non-obvious procedure (a release recipe, a data migration routine), the agent may write a small project skill in `.agents/skills/<project>-<name>/SKILL.md`; `./kanban doctor --fix` mirrors it into `.claude/skills/`. Most tasks need none.

## Agent briefs used by the skills

These live in `tracking/briefs/`:
- `PLANNING_BRIEF.md`
- `EXECUTION_BRIEF.md`
- `DOC_INGEST_BRIEF.md`
- `DOC_ALIGNMENT_BRIEF.md`
- `TASK_ALIGNMENT_BRIEF.md`

Each is self-contained, so a sub-agent with no chat history can do its part.

## Templates

`docs/pm/templates/`:
- `GOAL.md`, `SPEC.md`, `ARCHITECTURE.md`
- `configuration.md`, `decisions-register.md`
- `doc-review.md`, `runbook.md`
- `scope-unit.md`, `research-note.md`
- `agent-blocks/` (the CLAUDE/AGENTS/GEMINI blocks `install.py` and `doctor --fix` merge)
- `roadmap/README.md`, `roadmap/phase.md`

`tracking/templates/`:
- `task.md`, `bug.md`, `phase.md`

`<!-- pm:fill … -->` markers say what to write. `pm-doc-sync`'s stale sweep reports any left behind.
