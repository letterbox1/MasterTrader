---
id: P0-T056
kind: task
title: Scan images (trivy/grype) and verify nothing is exposed outside Tailscale
phase: 0
type: VERIFY
status: backlog
priority: high
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P0-T019, P0-T021, P0-T023, P0-T015, P0-T020]
requirements: [R0.N2, R0.N3, R0.N5]
roadmap_todos: [T0.65]
modules: [ops]
dashboards: []
branch: p0/P0-T056-image-scan-and-external-port-scan
pr: ""
doc_sync: [docs/07-security-notes.md, docs/roadmap/phase-0-foundations.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P0-T056 · Scan images (trivy/grype) and verify nothing is exposed outside Tailscale

## Goal / expected outcome

CI scans every image in `images.lock` with trivy and grype (fail on fixable CRITICAL/HIGH) and produces an SBOM; a host-side check shows no TCP/UDP port reachable from the LAN or internet, everything reachable only over Tailscale, and the scrape-network probe still cannot reach Postgres/signer.

## Context & references

- [Roadmap P0 R0.N2, R0.N3, R0.N5](../../../docs/roadmap/phase-0-foundations.md#3-requirements)
- [Roadmap P0 T0.65](../../../docs/roadmap/phase-0-foundations.md#4-todo-sets)
- [07 §5 network & host](../../../docs/07-security-notes.md#5-network--host)
- [07 §7 supply chain](../../../docs/07-security-notes.md#7-supply-chain)
- [02 §3.1 networks](../../../docs/02-v1-architecture.md#31-networks)
- Related: P0-T019 checklist, P0-T021 probe
- Depends on: P0-T019, P0-T021, P0-T023, P0-T015, P0-T020

## Requirements

- CI `images` job: for each digest in `images.lock` run `trivy image --severity CRITICAL,HIGH --ignore-unfixed --exit-code 1` and `grype --fail-on high --only-fixed`; generate CycloneDX SBOM (`syft`) as artifact; allow-list file with CVE id, reason and expiry only.
- Vendored-code check: `third_party/` grep for telemetry/referral/`eval`/`exec`/network calls (07 §7) — empty in P0 but the job exists.
- External scan: from a machine on the LAN, `nmap -Pn -p- <LAN IP>` and `nmap -sU --top-ports 100` → nothing open; from a tailnet device, only 22 and 443 open.
- Internet exposure: confirm no router port-forward / UPnP mapping (router UI) and `tailscale funnel status` off.
- Re-run `infra/host/checklist.sh` and the `scrape` netprobe; record results and scan date for D16 Security posture.

## ToDo

- [ ] Write the CI `images` job and allow-list format.
- [ ] Run the external scans and record outputs (redact IPs).
- [ ] Store `last_scan` date in `ops.setting` for D16.
- [ ] File bugs for findings.

## Verification

### Tests
- CI job fails on a fixture image with a known fixable CRITICAL (e.g. an old pinned alpine digest).
- Host scans as above.

### Scenarios
- Given a new image digest introduces a fixable CRITICAL CVE, when the PR runs, then CI fails naming the CVE.
- Given someone enables Tailscale Funnel, then the checklist marks FAIL.

### Stress / failure injection
- n/a: scanning; runtime ≤ 6 min in CI with caching.

## Acceptance criteria

- [ ] trivy + grype + SBOM in CI, failing on fixable CRITICAL/HIGH
- [ ] LAN nmap: 0 open ports; tailnet: only 22/443
- [ ] Netprobe and checklist re-run PASS
- [ ] Results recorded for D16 posture
- [ ] CI green (ruff, mypy, pytest, gitleaks, `pit` check)

## Exceptions & edge cases

- Unfixed CVEs with no patch: tracked in the allow-list with expiry ≤ 30 days and re-reviewed.

## Cardinal rules (do NOT)

- Do NOT allow-list CVEs without an expiry and reason.
- Do NOT enable Funnel, UPnP or port-forwarding.
- Pin every image by digest (no `:latest` or floating tags); no telemetry or referral IDs in vendored code.
- Do NOT skip, weaken or delete a test to get CI green.

## Doc sync on completion

- `docs/07-security-notes.md` §7: link the CI scan job and allow-list policy.
- `docs/roadmap/phase-0-foundations.md`: tick T0.65 when every item mapped to it is done.

## Branch & PR

- Branch: `p0/P0-T056-image-scan-and-external-port-scan`
- PR title: `P0-T056: Scan images (trivy/grype) and verify nothing is exposed outside Tailscale`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P0-T056` run

## Progress log

- 2026-10-21 00:00 · planner · created
