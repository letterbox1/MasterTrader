---
id: P8-B011
kind: gap
title: `mcp` container's network and ingress aren't specified
phase: 8
type: DOC
status: backlog
priority: medium
size: XS
severity: S3
owner: agent
claimed_by: ""
depends_on: []
requirements: [R8.02]
roadmap_todos: [T8.40]
modules: [M20]
dashboards: []
branch: p8/P8-B011-mcp-container-network-placement
pr: ""
doc_sync: [docs/02-v1-architecture.md, docs/07-security-notes.md, docs/roadmap/phase-8-mcp.md]
doc_sync_status: n/a
found_in: docs/02-v1-architecture.md §3.1/§3.2
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P8-B011 · `mcp` container's network and ingress aren't specified

## Goal / expected outcome

The docs agree and are specific about this point, so the P8 tasks that depend on it can be built and tested without guessing. Proposed resolution: add `mcp` to the `edge` network row (members: caddy, mt-api, mcp); Caddy route `/mcp` on the Tailscale listener; note that stdio clients run on the client machine and call mt_api via Tailscale.

## Context & references

- Spec: [02 §3.1](../../../docs/02-v1-architecture.md#31-networks) · [02 §3.2](../../../docs/02-v1-architecture.md#32-containers) · [07 §5](../../../docs/07-security-notes.md#5-network--host)
- Implementing task: P8-T015

## Requirements

- **Steps to reproduce:** Read 02 §3.1: no network lists `mcp` as a member; 02 §3.2 lists the container. 07 §5 says no published ports except via Tailscale.
- **Expected:** 02 §3.1 states which network `mcp` joins and how a remote client reaches it (e.g. `edge`, via Caddy on the Tailscale interface; stdio clients reach mt_api directly over Tailscale).
- **Actual:** Unspecified.
- **Impact:** Risk of attaching `mcp` to `core` (giving it DB/NATS reach, breaking the thin-adapter boundary) or publishing a port (S3)
- **Suggested fix:** add `mcp` to the `edge` network row (members: caddy, mt-api, mcp); Caddy route `/mcp` on the Tailscale listener; note that stdio clients run on the client machine and call mt_api via Tailscale.

## ToDo

- [ ] Confirm the proposed resolution (with the user if it changes behaviour)
- [ ] Edit the listed docs so they agree with each other
- [ ] Write or point to the test in the implementing P8 task that pins the behaviour
- [ ] Note the resolution in the Progress log

## Verification

### Tests
- Regression: the implementing task's test (named in Context) pins the documented behaviour.

### Scenarios
- Given the docs are fixed, when a developer reads only the linked sections, then they implement the same behaviour as the P8 task describes.

### Stress / failure injection
- n/a: documentation gap.

## Acceptance criteria

- [ ] Docs updated and mutually consistent
- [ ] Implementing task test exists and passes
- [ ] Resolution noted in the Progress log

## Exceptions & edge cases

- If the user rejects the proposal, record the alternative here and update the implementing task before it starts.

## Cardinal rules (do NOT)

- Do NOT close without the docs actually agreeing.
- Do NOT edit WORM records to "fix" data; append a correction instead.
- Do NOT expose withdrawals, API-key management or wallet mandate signing through MCP, in any form (R8.06).

## Doc sync on completion

- `docs/02-v1-architecture.md`: as described in the suggested fix.
- `docs/07-security-notes.md`: as described in the suggested fix.
- `docs/roadmap/phase-8-mcp.md`: note the clarified behaviour if it changes a requirement's wording.

## Branch & PR

- Branch: `p8/P8-B011-mcp-container-network-placement`
- PR title: `P8-B011: fix `mcp` container's network and ingress aren't specified`
- PR checklist: docs consistent · implementing test referenced · `./kanban done P8-B011` run

## Progress log

- 2026-10-21 00:00 · planner · opened
