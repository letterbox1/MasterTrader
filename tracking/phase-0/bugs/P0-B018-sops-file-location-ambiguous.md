---
id: P0-B018
kind: gap
title: 07 §2 doesn't say whether the encrypted sops file may live in git
phase: 0
type: DOC
status: done
priority: low
size: XS
severity: S4
owner: agent
claimed_by: ""
depends_on: []
requirements: [R0.N1]
roadmap_todos: [T0.43]
modules: []
dashboards: []
tools: []
mcp: []
env: []
services: []
branch: p0/P0-B018-sops-file-location-ambiguous
pr: ""
doc_sync: [docs/07-security-notes.md]
doc_sync_status: done
found_in: docs/07-security-notes.md §2
created: 2026-10-21
updated: 2026-10-22
started: ""
completed: 2026-10-22
blocked_reason: ""
checkpoint: ""
review_result: ""
---

# P0-B018 · 07 §2 doesn't say whether the encrypted sops file may live in git

## Goal / expected outcome

The docs agree and the implementing tasks have one unambiguous answer. Suggested fix: Document the P0 choice (P0-T022): encrypted file lives at `/etc/mastertrader/secrets.sops.yaml` outside the repo, encrypted copy off-site via restic; the repo holds only `.sops.yaml` and an example with key names.

## Context & references

- Found in: `docs/07-security-notes.md §2`
- Related: P0-T022
- [07 §2 secrets](../../../docs/07-security-notes.md#2-secrets)

## Requirements

- **Steps to reproduce:** Read 07 §2 ('Never in git', sops+age file) and R0.N1 ('no secret in git').
- **Expected:** An explicit location rule for the encrypted file.
- **Actual:** Ambiguous: sops files are commonly committed encrypted, but R0.N1 says no secret in git.
- **Impact:** Low: someone may commit the encrypted file (and its metadata: key names, dates) to the repo.
- **Suggested fix:** Document the P0 choice (P0-T022): encrypted file lives at `/etc/mastertrader/secrets.sops.yaml` outside the repo, encrypted copy off-site via restic; the repo holds only `.sops.yaml` and an example with key names.

## ToDo

- [x] Decision taken: 17 §D P0-B018 (ratified in 17 §E)
- [x] Docs updated so they agree: 07 §2 Location bullet (outside the repo, e.g. `~/.config/mastertrader/`, backed up by restic; repo holds only `.sops.yaml` + example); 04 Phase 0; D16 Backups; roadmap P0 R0.N1/T0.43
- [x] Affected P0 task files reference the resolution: P0-T001–P0-T010, P0-T013, P0-T022, P0-T039, P0-T060
- [x] Regression check owned: P0-T022 `secrets-lint` + gitleaks full-history scan

## Verification

### Tests
- Doc check: grep the listed docs for the conflicting statements; none remain after the fix.

### Scenarios
- Given a developer reads any of the listed docs, then they reach the same answer.

### Stress / failure injection
- n/a: documentation gap.

## Acceptance criteria

- [x] Listed docs carry the 17 §D P0-B018 decision and agree (checked in the alignment wave, 2026-10-22)
- [x] Implementation owned by: P0-T022
- [x] Root cause noted in the progress log

## Exceptions & edge cases

- If the user decides differently from the suggestion, the affected tasks are updated before they start.

## Cardinal rules (do NOT)

- Do NOT close without updating every listed doc.
- Do NOT edit WORM records to 'fix' data; append a correction instead.

## Doc sync on completion

- `docs/07-security-notes.md`: reconcile as described.

## Branch & PR

- Branch: `p0/P0-B018-sops-file-location-ambiguous`
- PR title: `P0-B018: fix 07 §2 doesn't say whether the encrypted sops file may live in git`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P0-B018` run

## Progress log

- 2026-10-21 00:00 · planner · opened
- 2026-10-22 00:00 · aligner · resolved by 17 §D P0-B018; docs checked: 07 §2 Location bullet (outside the repo, e.g. `~/.config/mastertrader/`, backed up by restic; repo holds only `.sops.yaml` + example); 04 Phase 0; D16 Backups; roadmap P0 R0.N1/T0.43. Root cause: 07 §2 said 'never in git' without saying where the encrypted file lives. Implementation owned by P0-T022.
- 2026-10-22 02:05 · cloud:vm:be04b6ae61f8 · verified: decided in docs/17 (17 §D P0-B018); docs updated: 07 §2 Location bullet (outside the repo, e.g. `~/.config/mastertrader/`, backed up by restic; repo holds only `.sops.yaml` + example); 04 Phase 0; D16 Backups; roadmap P0 R0.N1/T0.43; implementation owned by P0-T022
- 2026-10-22 02:05 · cloud:vm:be04b6ae61f8 · done
- 2026-10-22 02:05 · cloud:vm:be04b6ae61f8 · doc sync done: docs updated in the alignment wave
