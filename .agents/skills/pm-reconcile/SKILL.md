---
name: pm-reconcile
description: Human-in-the-loop gap and decision reconciliation - gather open gaps/bugs (S1/S2 first), explain each plainly with a recommendation, take the human's answers in chat, record them in the decisions register and configuration doc (defaults, not hard-coded), then run doc alignment and task alignment so docs, tasks and the kanban all update and gaps close with evidence. Use when planning surfaced gaps, when the human answers or questions open issues, or for "what do you need from me", "let's discuss the gaps", "update everything to match".
compatibility: Any Agent Skills-compatible agent (Claude Code, Codex, Gemini CLI, Cursor, OpenCode and others) working in a git repository with python3 >= 3.9; uses the ./kanban CLI from CeraNova PM.
metadata:
  author: CeraNova
  product: CeraNova PM
  version: "1.3"
---

# pm-reconcile

This is the loop that keeps docs, tasks and boards true to what the human decided.

## 1. Gather

```
./kanban list --kind gap --include-bugs            # every gap and bug, all phases
./kanban list --kind gap --include-bugs --severity S2
```

The board shows open bugs by severity (`KANBAN.md` "Open S1/S2"). Read each gap's *Requirements*: what's wrong, expected, suggested fix.

## 2. Present to the human (chat)

- **S1/S2 first**, grouped by theme (e.g. "undefined numbers", "conflicts between docs", "design holes").
- For each: one or two plain sentences on what's wrong and why it matters, then **your recommendation**.
- **Distinguish** what's a configurable default (propose a value and say it's changeable), what's a genuine design choice, and what needs an external check (U).
- If the human pushes back or asks "why", explain, correct any misunderstanding kindly and precisely, and keep it short.
- **Ask only for what you can't decide.** Never re-ask what they already answered.

## 3. Record decisions (before touching other docs)

- **Configuration doc** (`docs/pm/templates/configuration.md` → the project's numbered config doc):
  - layers (tighten-only);
  - every default with range and layer;
  - failure behaviour;
  - live inputs.

  **Nothing that a user may want to change is hard-coded.**
- **Decisions register** (`docs/pm/templates/decisions-register.md` → the project's numbered register):
  - one row per gap ID: decision + docs to change;
  - S1/S2 explicitly, then cross-doc conflicts, then other decisions;
  - "adopt the suggested fix" as the default for minor items.

  Verify **every** gap ID appears:

  ```
  for f in tracking/phase-*/bugs/*.md; do id=$(basename $f|cut -d- -f1-2); grep -q $id <register> || echo MISSING $id; done
  ```
- **Roadmap:** add requirement/ToDo IDs for genuinely new work (e.g. a new safety mechanism), in the right phase docs.

Commit this step on its own.

## 4. Doc alignment wave

- **pm-delegate** with `tracking/briefs/DOC_ALIGNMENT_BRIEF.md`.
- Use disjoint doc sets per agent (they must not rename headings). For a small change, do it yourself.

## 5. Task alignment wave (after the docs are done)

- `./kanban pause`, then **pm-delegate** one agent per phase with `tracking/briefs/TASK_ALIGNMENT_BRIEF.md`, listing that phase's new roadmap IDs.
- Agents:
  - update tasks;
  - create tasks for new IDs;
  - close gaps with `./kanban done <ID> --evidence "decided in <register row>; docs updated: …"` and `./kanban docsync <ID> --done`;
  - leave (U) items open, owned by a task.

## 6. Integrate

`./kanban validate`, link check, `./kanban pause --off && ./kanban build`, commit, push.

Report to the human:
- gaps closed and still open (why);
- new tasks;
- what changed in which docs;
- anything still needing their input.

## Don't

- Don't close a gap without the decision being in the docs.
- Don't hard-code a value the human said should be configurable.
- Don't make product decisions silently: recommend, then record what the human chose.
