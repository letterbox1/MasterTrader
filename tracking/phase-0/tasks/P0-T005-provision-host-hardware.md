---
id: P0-T005
kind: task
title: Profile the workstation and select CPU/GPU profiles
phase: 0
type: OPS
status: ready
priority: critical
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: []
requirements: [R0.02]
roadmap_todos: [T0.01]
modules: [ops, infra]
dashboards: []
tools: [git, docker, just]
mcp: []
env: []
services: []
branch: p0/P0-T005-provision-host-hardware
pr: ""
doc_sync: [docs/03-build-spec.md, docs/18-platform-and-deployment.md, docs/roadmap/phase-0-foundations.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-11-19
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
review_result: ""
---

# P0-T005 · Profile the workstation and select CPU/GPU profiles

## Goal / expected outcome

The agent profiles the machine it runs on (the workstation) and writes `infra/profile.yaml`: cores, RAM, disks and free space, GPU (if any, with VRAM), OS and Docker versions. From it the stack picks the **CPU or GPU model profiles** (`models.gpu_profile: auto`, [16 §2.15](../../../docs/16-configuration-and-safety-model.md#215-platform-deployment-and-regions)) and sizes memory limits. Nothing is bought and nothing blocks: below the [03 §2](../../../docs/03-build-spec.md#2-target-environment) recommendation the profile **warns** and heavy services fall back to CPU or smaller settings. Was a USER task (provision a host, decide on a GPU); now agent work ([17 §G](../../../docs/17-decisions-register.md#g-platform-rust-and-python-supabase-vercel-workstation-first-2026-11-19)).

## Context & references

- [Roadmap P0 T0.01](../../../docs/roadmap/phase-0-foundations.md#4-todo-sets) · [§2 entry criteria](../../../docs/roadmap/phase-0-foundations.md#2-entry-criteria) · [§7 risks](../../../docs/roadmap/phase-0-foundations.md#7-risks--open-questions)
- [18 §9 workstation-first build path](../../../docs/18-platform-and-deployment.md#9-workstation-first-build-path)
- [03 §2 target environment](../../../docs/03-build-spec.md#2-target-environment) (guide figures and the GPU row)
- [16 §2.15](../../../docs/16-configuration-and-safety-model.md#215-platform-deployment-and-regions) (`models.gpu_profile`, `deploy.mode`)
- Related: P0-T019 (workstation baseline), P0-T020/P0-T043/P0-T044 (memory limits and model profiles), P7-T071/P7-T073 (runtime host choice, LUKS and the live profile at the shift)
- Unblocks: P0-T019; sizing inputs for the Compose stack

## Requirements

- `just profile` (shell + `docker info`, no root needed) writes `infra/profile.yaml` (committed without serial numbers, hostnames or IPs): CPU model and physical/logical cores, RAM, each mounted volume's type (NVMe/SSD/HDD where detectable) and free space, GPU vendor/model/VRAM and driver/runtime (NVIDIA container toolkit present?) or `none`, OS, kernel, Docker and Compose versions.
- Selection: `models.gpu_profile: auto` → `gpu` if a supported GPU and container runtime are found, else `cpu` (the default). Compose profiles for TEI and `llm-local` follow it (P0-T043, P0-T044). Tier B speed expectations from [17 §B](../../../docs/17-decisions-register.md#b-cross-doc-conflicts-one-canonical-answer) (P6-B002): ~2–12 ms per decision on GPU, ~100–400 ms on CPU.
- Warnings, never blocks: RAM < 32 GB, free NVMe/SSD < 500 GB, no SSD, fewer than 8 cores → a WARN line in the profile and the D16 posture list, with which services get smaller limits.
- Memory plan: per-service `mem_limit` suggestions written next to the profile (Supabase Postgres, `tei-rerank`, `llm-local`, observability) so the stack fits the machine.
- Full-disk encryption: reported (`luks: true|false|unknown`) as a WARN only; required at the shift in the live profile (P7-T073).
- Re-runnable: running it again on new hardware updates the file and the selection; a change of `gpu_profile` is logged.

## ToDo

- [ ] Write `infra/scripts/profile.sh` and the `just profile` recipe.
- [ ] Generate `infra/profile.yaml` on the workstation; log the summary (no identifiers) here.
- [ ] Wire `models.gpu_profile: auto` into the compose profiles for TEI and `llm-local` (with P0-T043/P0-T044).
- [ ] Write the memory plan and hand it to P0-T020.
- [ ] Update docs listed under Doc sync.

## Verification

### Tests
- `just profile` on a CPU-only CI runner writes `gpu: none` and selects `cpu`; with a mocked `nvidia-smi` fixture it selects `gpu`.
- `nproc`, `free -g`, `lsblk` values match the profile on the workstation.

### Scenarios
- Given a machine with 16 GB RAM, when profiling, then WARN lines appear and the memory plan lowers limits; nothing fails.
- Given a GPU is added later, when `just profile` is re-run, then `gpu_profile` switches and TEI/`llm-local` use the GPU profile after `just up`.

### Stress / failure injection
- n/a: profiling.

## Acceptance criteria

- [ ] `infra/profile.yaml` written on the workstation (no serials, hostnames or IPs)
- [ ] CPU/GPU profile selected automatically and used by the model containers
- [ ] Warnings (not blocks) for anything below the 03 §2 guide; LUKS reported
- [ ] Memory plan handed to P0-T020

## Exceptions & edge cases

- Laptop that sleeps: the profile notes it; the soak (P0-T063) requires sleep off.
- Apple Silicon or another non-NVIDIA GPU: treated as `cpu` for containers unless a supported runtime is found (log it).

## Cardinal rules (do NOT)

- Do NOT block the build on hardware; warn and degrade instead.
- Do NOT commit serial numbers, hostnames, IPs or anything identifying the machine.
- Do NOT ask the human to buy hardware in Phase 0; the runtime host choice is P7-T071.
- Do NOT commit secrets or paste them into chats, issues, PRs or logs; secrets live only in the sops/age file ([07 §2](../../../docs/07-security-notes.md#2-secrets)).

## Doc sync on completion

- `docs/03-build-spec.md` §2 and `docs/18-platform-and-deployment.md` §9: link `just profile` and note the selected profile if it differs from the guide.
- `docs/roadmap/phase-0-foundations.md`: tick T0.01 when every item mapped to it is done.

## Branch & PR

- Branch: `p0/P0-T005-provision-host-hardware`
- PR title: `P0-T005: Profile the workstation and select CPU/GPU profiles`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P0-T005` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (tier-B latency per 17 §B P6-B002 (the 150–300 ms figure is retired); run fields added)
- 2026-11-19: Workstation-first (17 §G): this is no longer a USER gate. The build runs on whatever machine you run the agent on. The agent detects cores, RAM, disk and GPU, writes `infra/profile.yaml` (`models.gpu_profile: auto`), and warns (never blocks) when the machine is below the 03 §2 recommendation; heavy services fall back to CPU profiles. LUKS and the production hardware check move to the go-live shift (P7-T073).
- 2026-11-19 00:00 · aligner · re-platformed per docs/18 (body rewritten as the agent OPS profiling task: `just profile` writes `infra/profile.yaml`, `models.gpu_profile: auto`, warnings instead of hardware gates; LUKS and hardware choice moved to P7-T071/P7-T073)
