---
name: pm-doc-ingest
description: Vet and merge documents the human hands over (another project's spec, research, briefs, vendor docs, notes) into this project's docs - drop direct overlap, merge new specs and systematic approaches where they fit, resolve conflicts, and write a review doc. Use when the user says "review these docs", "does this overlap with ours", "add anything we haven't covered".
compatibility: Any Agent Skills-compatible agent (Claude Code, Codex, Gemini CLI, Cursor, OpenCode and others) working in a git repository with python3 >= 3.9; uses the ./kanban CLI from CeraNova PM.
metadata:
  author: CeraNova
  product: CeraNova PM
  version: "1.3"
---

# pm-doc-ingest

Follow `tracking/briefs/DOC_INGEST_BRIEF.md`. In short:

1. **Read** the provided material and this project's goal/spec/architecture/roadmap/decisions docs.
2. **Vet:** flag unverified, outdated, contradictory or risky claims. Mark anything unconfirmed **(U)**. Respect the project's constraints and non-goals.
3. **Classify** each section:
   - **overlap:** drop it, citing where it's already covered;
   - **new:** merge it where it fits, or into a new numbered doc;
   - **conflict:** decide, or list it as a decision for the human;
   - **not adopted:** give the reason.
4. **Write the review** from `docs/pm/templates/doc-review.md`.
5. **Update** the target docs, keeping existing headings.
6. **If work was added:**
   - new requirement/ToDo IDs in the roadmap phase docs;
   - then **pm-plan** for affected phases, or gap items if planning comes later.
7. **Report to the human:**
   - what was dropped;
   - what was added, and where;
   - the conflicts and how they were resolved;
   - the decisions they need to make.

   If a decision is needed now, hand over to **pm-reconcile**.

**Large inputs:** split the work by target doc and use **pm-delegate**, with one agent per doc set and no shared files.
