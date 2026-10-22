# Doc Ingest Brief (vetting docs the human hands you)

Use this brief when the human provides external material: another project's spec, research, a brief, vendor docs, meeting notes.

## Steps

1. **Read everything** the human provided, plus this project's goal/spec/architecture/roadmap/decisions docs.

2. **Vet it:**
   - flag claims that are unverified, outdated, contradictory or legally or commercially risky;
   - mark anything you couldn't confirm **(U)**;
   - don't adopt anything that breaks the project's constraints (budget, licences, non-goals).

3. **Classify each section:**
   - **Direct overlap:** already covered here → drop it, noting where it's covered.
   - **New spec or systematic approach** not yet here → merge it into the right existing doc, or a new numbered doc if it's large.
   - **Conflict:** decide which wins and why. If it's the human's call, list it under "Decisions needed".
   - **Not adopted:** say why.

4. **Write the review** from `docs/pm/templates/doc-review.md` as a numbered doc (e.g. `docs/NN-<source>-review.md`), and link it from the docs index.

5. **Update the docs** where merged items land. Don't rename existing headings, because anchors are linked.

6. **Update the roadmap** if the merge adds work: new requirement/ToDo IDs in the right phase docs. Then plan or align tasks per the planning or task-alignment brief, or file gap items if planning comes later.

7. **Report:** what was dropped, what was added (where), the conflicts and how they were resolved, and the decisions needed from the human.
