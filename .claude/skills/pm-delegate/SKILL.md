---
name: pm-delegate
description: Run several sub-agents in parallel on CeraNova PM work without conflicts - one agent per phase (planning, task alignment, execution) or per doc set (doc alignment, doc ingest) - with ID ranges for split phases, paused triage, merge of part files, validation and commit. Use when the user asks to "spin up agents per phase", "fan out", "parallelise", or when a job covers several phases or many docs.
compatibility: Any Agent Skills-compatible agent (Claude Code, Codex, Gemini CLI, Cursor, OpenCode and others) working in a git repository with python3 >= 3.9; uses the ./kanban CLI from CeraNova PM.
metadata:
  author: CeraNova
  product: CeraNova PM
  version: "1.4.2"
---

# pm-delegate

## Partitioning rules (no two agents write the same file)

| Job | Unit per agent | Brief |
|---|---|---|
| Plan phases | One phase → `tracking/phase-N/` | `tracking/briefs/PLANNING_BRIEF.md` |
| Big phase | Split by workstream. Part A writes `PHASE.md` + IDs `T001–T099` / `B001–B049`; part B writes `PHASE.part-b.md` + `T101–T199` / `B050–B099` | Same |
| Align docs after decisions | Disjoint **sets of doc files** (e.g. architecture; spec + top docs; security/policy; UI + design) | `tracking/briefs/DOC_ALIGNMENT_BRIEF.md` |
| Align tasks after doc alignment | One phase each | `tracking/briefs/TASK_ALIGNMENT_BRIEF.md` |
| Ingest large external docs | Disjoint target doc sets | `tracking/briefs/DOC_INGEST_BRIEF.md` |
| Execute | One phase each (only phases whose prerequisites are done), or with `phase_gating: "dependencies"` any set of ready tasks with no dependency between them | `tracking/briefs/EXECUTION_BRIEF.md` |
| Review | One item (or one phase's review queue) per reviewer, never the agent that built it; reviewers only write verdicts, logs and new bug items | **pm-review** |

## Steps

1. **Prepare:** decide the partition and write any shared decisions **first** (decisions register, configuration doc, roadmap IDs), so agents don't invent conflicting answers. Then run `./kanban pause`, so triage doesn't rewrite files mid-edit.

2. **Launch one background agent per unit, all in one message.** Each prompt contains:
   - the repo path and a one-line project description;
   - "read and follow `<brief path>` exactly";
   - its unit (folder or file list) and **"edit nothing else"**;
   - ID ranges if split;
   - phase-specific emphasis (the roadmap IDs, new requirements, special concerns);
   - "validate with `./kanban validate --phase N` (0 errors) and report in ≤ 300 words".

   Keep it under ~10 agents per wave. Two waves are normal after a reconciliation: doc alignment, then task alignment.

3. **While they run**, do non-overlapping work only. Checkpoint-commit finished units as they land, so nothing is lost if the session dies.

4. **Integrate:**
   - merge `PHASE.part-*.md` into `PHASE.md` (demote headings one level; delete the part file);
   - `./kanban validate` (all phases);
   - check relative links;
   - `./kanban pause --off && ./kanban build`;
   - view the board.

5. **Summarise** each agent's report for the human: counts, gaps by severity (S1/S2 first), uncertainties. Commit and push.

## Don't

- Don't give two agents the same file.
- Don't launch execution agents for phases whose `opens_after` prerequisites aren't done.
- Don't paste agents' internal IDs into user-facing text.
