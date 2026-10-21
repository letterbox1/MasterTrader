---
id: P2-T116
kind: task
title: Sandbox runner and LLM strategy generator
phase: 2
type: BUILD
status: backlog
priority: high
size: L
severity: ""
owner: agent
claimed_by: ""
depends_on: [P2-T101, P2-T104, P2-T113]
requirements: [R2.45]
roadmap_todos: [T2.28]
modules: [M7, M0, M21]
dashboards: [D03, D04]
branch: p2/P2-T116-sandbox-runner-and-generator
pr: ""
doc_sync: [docs/03-build-spec.md, docs/07-security-notes.md, docs/roadmap/phase-2-strategies-risk-lab.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P2-T116 · Sandbox runner and LLM strategy generator

## Goal / expected outcome

`lab.generate_strategy` turns a natural-language description into strategy code + manifest via the gateway, runs it only inside the `sandbox` container (gVisor `runsc`, `--network none`, no secrets, read-only data mount) for static checks and a first backtest, and returns code + manifest + results for you to review before `strategy.create`.

## Context & references

- Roadmap: [R2.45](../../../docs/roadmap/phase-2-strategies-risk-lab.md#3-requirements) · ToDo T2.28 · verified by P2-T165 (escape test)
- [SPEC NN4](../../../SPEC.md#non-negotiable-requirements) · [03 M7](../../../docs/03-build-spec.md#m7-research-lab--mt_lab) · [07 security notes](../../../docs/07-security-notes.md) (gVisor/`--network none`; never run cloned bot code outside the sandbox) · [01 §3.4 Vibe-Trading in-process exec risk](../../../docs/01-repo-vetting-report.md#34-hkudsvibe-trading--research-and-strategy-generation-layer)
- Part-A prerequisites: `sandbox` container + gVisor runtime + resource limits (T2.40), manifest validator incl. never-build rules (T2.20) in part A (P2-T001–T099)
- UI: [D03 'Describe it' tab](../../../docs/ui/dashboards/D03-strategies.md), [D04 generator panel](../../../docs/ui/dashboards/D04-research-lab.md)

## Requirements

- Generation: gateway role `strategy-gen` (its own virtual key + daily budget, local fallback); prompt = your description + the M0 base-class API + template catalogue; output = `strategy.py` + `manifest.yaml`.
- Static gate before execution: AST import allow-list (`mt_strategy`, `mt_core`, numpy, pandas, talib; no `os`, `subprocess`, `socket`, `importlib`, `ctypes`, `eval/exec`, file writes outside `/tmp`), manifest schema + never-build validator (part A), max file size 200 KB.
- Sandbox run: `docker run --runtime=runsc --network none --read-only --cap-drop ALL --pids-limit 256 --memory 2g --cpus 2`, tmpfs `/tmp`, no env secrets, data mounted read-only from a pre-built dataset snapshot; wall-clock cap 10 min.
- In the sandbox: import, instantiate, run a screener backtest on the mounted snapshot; results returned as JSON over stdout only.
- Output to UI: code (read-only diff), manifest, sandbox log, first backtest, leakage review (P2-T113); banner text 'Generated code ran in an isolated sandbox with no network or secrets.'
- Saving = `strategy.create` (C1) as `draft`; generated strategies are tagged `origin=generated` and count trials against their family.

## ToDo

- [ ] Implement `mt_lab/generator/` (prompting, response parsing, retries ≤ 2)
- [ ] Implement AST static checker with allow-list
- [ ] Implement `mt_lab/sandbox/runner.py` invoking the sandbox container with the flags above; output size cap 5 MB
- [ ] Dataset snapshot export for sandbox mounts (read-only Parquet subset)
- [ ] Wire `lab.generate_strategy` command and progress on `lab.job.{id}`
- [ ] Tests (recorded LLM responses) + docs

## Verification

### Tests
- Unit: AST checker rejects each forbidden construct (one fixture per item).
- Integration: a benign recorded generation runs in the sandbox and returns a backtest JSON.
- Integration: generated code containing a sniping/copy-trading pattern is rejected by the never-build validator before running.

### Scenarios
- Given generated code that tries `socket.connect`, then the static gate rejects it; if obfuscated, the sandbox network is absent and the run fails without egress.
- Given the gateway budget is exhausted, then generation falls back to `local-advisor` and says so.
- Given the sandbox times out at 10 min, then the job fails with the sandbox log and nothing is saved.

### Stress / failure injection
- Fork bomb / memory hog fixtures are contained by pids/memory limits and the host stays healthy (asserted in P2-T165).

## Acceptance criteria

- [ ] Generated code never executes outside the `sandbox` container
- [ ] Static gate + never-build validator run before execution
- [ ] User review required before save
- [ ] CI green (lint, types, tests, `pit` check)

## Exceptions & edge cases

- gVisor unavailable on the host: generator disabled with a clear error (never falls back to plain Docker or in-process).
- Generated manifest missing counterparty/kill criteria/benchmark: shown as validation errors; cannot save until filled.

## Cardinal rules (do NOT)

- Do NOT execute generated code in `backtest-worker`, `mt-api` or `engine`.
- Do NOT mount secrets, the Docker socket or writable volumes into the sandbox.
- Do NOT commit secrets or paste them into chats/issues; secrets live only in the sops/age file (07 §2).
- Do NOT put Telegram text (or any `model_input_ok = false` / `train_ok = false` row) into a model, prompt, RAG index or training set (12 §4–5).
- Do NOT skip, weaken or delete a test to get green.

## Doc sync on completion

- `docs/03-build-spec.md` M7: generator flow and allow-list.
- `docs/07-security-notes.md`: exact sandbox flags.
- `docs/roadmap/phase-2-strategies-risk-lab.md`: tick T2.28 once every task mapped to it (part A and part B) is done.

## Branch & PR

- Branch: `p2/P2-T116-sandbox-runner-and-generator`
- PR title: `P2-T116: Sandbox runner and LLM strategy generator`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P2-T116` run

## Progress log

- 2026-10-21 00:00 · planner · created
