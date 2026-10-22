---
id: P4-T067
kind: task
title: Live check of keyed sources with your keys (FIRMS, ACLED, Finnhub, CryptoPanic, Myfxbook)
phase: 4
type: VERIFY
status: backlog
priority: high
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P4-T005, P0-T010, P4-T016, P4-T017, P4-T033, P4-T034, P4-T039]
requirements: [R4.01, R4.08, R4.11]
roadmap_todos: [T4.66]
modules: [M2, M3, M6]
dashboards: [D07, D08]
tools: [uv, sops, git]
mcp: []
env: [FINNHUB_API_KEY, CRYPTOPANIC_API_KEY, FIRMS_MAP_KEY, ACLED_EMAIL, ACLED_API_KEY, MYFXBOOK_EMAIL, MYFXBOOK_PASSWORD]
services: [finnhub, cryptopanic, nasa-firms, acled, opensanctions, myfxbook, ig-demo, oanda-practice]
branch: p4/P4-T067-live-check-of-keyed-sources-with-your-keys-firms
pr: ""
doc_sync: [docs/06-aggregators-and-market-providers.md, docs/roadmap/phase-4-intel.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-22
updated: 2026-10-22
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
review_result: ""
---

# P4-T067 · Live check of keyed sources with your keys (FIRMS, ACLED, Finnhub, CryptoPanic, Myfxbook)

## Goal / expected outcome

With your real free keys in the stack, each keyed or licence-bound P4 source delivers live data for 24 h within its quota and carries the right provenance tags: Finnhub and CryptoPanic news, NASA FIRMS fires, ACLED events (if access was granted), OpenSanctions (per your licence decision), and the positioning inputs Myfxbook / IG sentiment / OANDA books (practice credentials). This is the 'keys last' step for connectors that were built on fixtures.

## Context & references

- Roadmap: [R4.01, R4.08, R4.11](../../../docs/roadmap/phase-4-intel.md#3-requirements) · ToDo [T4.66](../../../docs/roadmap/phase-4-intel.md#4-todo-sets) (live check after T0.10, T4.06)
- Decisions: [17 §E](../../../docs/17-decisions-register.md#e-ratification-2026-10-22) (build first, keys last) · [17 §D](../../../docs/17-decisions-register.md#d-other-decisions) (P4-B008: FIRMS/ACLED keys + OpenSanctions licence are a USER task) · P1-B008 (practice accounts use their normal credentials)
- Your inputs (`depends_on`): P0-T010 (T0.10: Finnhub, CryptoPanic, Myfxbook keys), P4-T005 (T4.06: FIRMS/ACLED keys, OpenSanctions licence, terms decisions)
- Built on fixtures in: P4-T016 (Finnhub), P4-T017 (CryptoPanic), P4-T033 (FIRMS), P4-T034 (ACLED, OpenSanctions), P4-T039 (Myfxbook, IG, OANDA)
- Provenance: [12 §5](../../../docs/12-policy-and-compliance.md#5-data-provenance-tagging-one-mechanism-for-all-data-terms) (seven columns).

## Requirements

- Keys are only in the sops file outside the repo; the stack reads them from `/run/secrets/<service>/`; the env names above are exported only for this check session via `sops exec-env` and are never printed.
- For each source: ≥ 1 successful live cycle immediately, then a 24-h run with zero over-quota responses (Finnhub budget 50/min, Myfxbook ≤ 100 calls/day, others per their free tier), `feed_status = ok` in D07.
- Every stored row's provenance matches `source_terms.yaml` (e.g. Finnhub `model_input_ok` per your ML-clause decision, OpenSanctions/ACLED `commercial_ok = false`, CryptoPanic attribution present).
- Sources you declined or that were refused (e.g. ACLED) are recorded as disabled with the reason, not as failures.

## ToDo

- [ ] Confirm masked key metadata (names + ages only) in D16 for every listed key
- [ ] Enable each keyed source and run one live cycle; fix and re-run any failure
- [ ] Run 24 h; collect quota usage, item counts and provenance-flag samples per source
- [ ] Record results (no secrets) in this file's progress log and in 06
- [ ] File bugs for any source that fails

## Verification

### Tests
- Provenance assertion script over the last 24 h of rows per source (flags vs `source_terms.yaml`).
- Quota report from the P1 quota tracker: no source above its configured budget.

### Scenarios
- Given ACLED declined your account, then ACLED is disabled with the reason and UCDP + GDELT cover conflict events.
- Given Finnhub returns 401 (key revoked), then the source goes `bad` with one alert and the others continue.
- Given Myfxbook's session expires mid-run, then it re-logs in once and alerts.

### Stress / failure injection
- The 24-h run under real quotas is the stress test; no synthetic load against third-party APIs.

## Acceptance criteria

- [ ] Each enabled keyed source delivered live data for 24 h with zero over-quota responses
- [ ] Provenance flags match `source_terms.yaml` on sampled rows for every source
- [ ] Results recorded (no secret values anywhere)

## Exceptions & edge cases

- A provider changed its free tier: disable with reason, file a bug, never switch to an unofficial endpoint.
- IG/OANDA practice outages: retry the next day; not a phase blocker if the endpoint is gone (disabled with reason).

## Cardinal rules (do NOT)

- Do NOT print, log or commit any key; use the sops file outside the repo.
- Do NOT create extra accounts to raise quotas.
- Do NOT commit secrets or paste them into chats, issues or logs; they live only in the sops/age file outside the repo ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Do NOT add paid data/APIs, scraping that breaks a site's terms, self-bots/user tokens, or any sybil/fake engagement.
- Do NOT touch live money (P7 gates); keys stay trade-only, IP-locked, withdrawals disabled.
- Do NOT let Telegram text (or any `model_input_ok = false` row) reach a model, RAG index or training set ([12 §4–5](../../../docs/12-policy-and-compliance.md#4-per-platform-data--automation-rules)).
- Do NOT skip, weaken or delete a test to get green.

## Doc sync on completion

- `docs/06-aggregators-and-market-providers.md`: record live-check results per keyed source (date, pass/fail, quotas)
- `docs/roadmap/phase-4-intel.md`: tick T4.66

## Branch & PR

- Branch: `p4/P4-T067-live-check-of-keyed-sources-with-your-keys-firms`
- PR title: `P4-T067: Live check of keyed sources with your keys (FIRMS, ACLED, Finnhub, CryptoPanic, Myfxbook)`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P4-T067` run

## Progress log

- 2026-10-22 00:00 · aligner · created for docs/16–17 (T4.66 keys-last live check per 17 §E; FIRMS/ACLED/OpenSanctions per 17 §D P4-B008)
