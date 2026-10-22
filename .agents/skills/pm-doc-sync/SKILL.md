---
name: pm-doc-sync
description: Keep documentation true to the work - clear the DOC_SYNC queue when items complete (spec, architecture, roadmap ToDo ticks, UI/user docs), record phase completion in the roadmap/plan docs, and sweep stale docs. Use when the Stop hook asks for doc sync, when tracking/DOC_SYNC.md lists items, when a phase completes, or for "update the docs to match", "docs are stale".
compatibility: Any Agent Skills-compatible agent (Claude Code, Codex, Gemini CLI, Cursor, OpenCode and others) working in a git repository with python3 >= 3.9; uses the ./kanban CLI from CeraNova PM.
metadata:
  author: CeraNova
  product: CeraNova PM
  version: "1.3"
---

# pm-doc-sync

## Item completed (Stop hook prompt or `tracking/DOC_SYNC.md` entry)

1. Open the item and read its **Doc sync on completion** section and `doc_sync` list.
2. **Update each listed doc** to describe what was actually built: behaviour, names, numbers, interfaces, limits, file paths. Keep existing headings (anchors are linked) and link configurable values to the configuration doc.
3. **Tick the roadmap ToDo(s)** in `roadmap_todos` in the roadmap phase doc (`- [x] **T2.22** …`).
4. `./kanban docsync <ID> --done --note "<what changed>"`, then commit with the item ID.

## Phase completed (`PHASE.md` → `status: done`, `doc_sync_status: pending`)

1. In `docs/roadmap/README.md` (outside the generated marker blocks) and the plan/summary docs, mark the phase done with the date and a link to its exit-demo evidence.
2. Update the spec/README if the phase changed the project's capabilities.
3. `./kanban docsync P<N> --done`.

## Stale-doc sweep (periodically, or before a release)

1. **Mechanical checks:**
   - relative links and anchors (every `](path#anchor)` resolves);
   - docs that mention removed modules or renamed commands;
   - numbers that contradict the configuration doc;
   - `<!-- pm:fill` markers left behind.
2. **Fix small issues directly.** File bigger ones as gap items (`./kanban new --kind gap …`) and reconcile them later (**pm-reconcile**).

## Don't

- Don't edit generated files or marker-block contents.
- Don't document intentions as facts. Docs describe what exists; the roadmap describes what's planned.
