---
id: P2-T165
kind: task
title: Verify sandbox containment (escape, egress, secrets, resource abuse)
phase: 2
type: VERIFY
status: backlog
priority: critical
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P2-T116]
requirements: [R2.45]
roadmap_todos: [T2.28]
modules: [M7]
dashboards: [D04]
branch: p2/P2-T165-verify-sandbox-escape
pr: ""
doc_sync: [docs/07-security-notes.md, docs/roadmap/phase-2-strategies-risk-lab.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P2-T165 · Verify sandbox containment (escape, egress, secrets, resource abuse)

## Goal / expected outcome

Evidence that hostile generated code cannot reach the network, secrets, the host or other containers, and cannot exhaust host resources — the 'Escape test' for R2.45 / SPEC NN4.

## Context & references

- Roadmap: [R2.45](../../../docs/roadmap/phase-2-strategies-risk-lab.md#3-requirements) · ToDo T2.28 · [SPEC NN4](../../../SPEC.md#non-negotiable-requirements) · [07](../../../docs/07-security-notes.md)
- Sandbox container + gVisor from T2.40 in part A (P2-T001–T099); runner from P2-T116

## Requirements

- Hostile fixtures (bypassing the static gate via a test flag): DNS lookup, TCP connect to postgres/nats/litellm and to 1.1.1.1, read `/proc/1/environ`, read `/run/secrets`, write outside `/tmp`, fork bomb, 8 GB allocation, 100% CPU loop, attempt `docker.sock`, ptrace, mount.
- Expected: every network attempt fails (no interface but loopback), no secrets present, writes fail (read-only FS), fork bomb stopped at pids-limit 256, memory killed at 2 GB, CPU limited to 2, wall-clock cap 10 min; host and other containers unaffected.
- `runsc` confirmed as the runtime (`docker inspect`) on every sandbox run; a run without gVisor is refused.

## ToDo

- [ ] Write `tests/security/sandbox_escape/` fixtures
- [ ] Run on the host; capture outputs
- [ ] Record results; file S1 bugs for any escape

## Verification

### Tests
- Security integration suite above (runs on the host in CI-self-hosted or manual with evidence).

### Scenarios
- Given a fixture that sleeps then exfiltrates via DNS, then no DNS resolution is possible and the attempt is logged.

### Stress / failure injection
- Fork bomb + memory hog simultaneously: host load stays < 80% on other cores; engine heartbeat uninterrupted.

## Acceptance criteria

- [ ] All hostile fixtures contained
- [ ] gVisor runtime verified
- [ ] Engine/monitor heartbeats unaffected during the test

## Exceptions & edge cases

- Kernel/gVisor upgrade: re-run this suite as part of the upgrade checklist.

## Cardinal rules (do NOT)

- Do NOT run these fixtures outside the sandbox.
- Do NOT relax sandbox flags to make legit generations work; extend the allow-list instead.
- Do NOT commit secrets or paste them into chats/issues; secrets live only in the sops/age file (07 §2).
- Do NOT skip, weaken or delete a test to get green.

## Doc sync on completion

- `docs/07-security-notes.md`: sandbox test results and re-run trigger.
- `docs/roadmap/phase-2-strategies-risk-lab.md`: tick T2.28 once every task mapped to it (part A and part B) is done.

## Branch & PR

- Branch: `p2/P2-T165-verify-sandbox-escape`
- PR title: `P2-T165: Verify sandbox containment (escape, egress, secrets, resource abuse)`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P2-T165` run

## Progress log

- 2026-10-21 00:00 · planner · created
