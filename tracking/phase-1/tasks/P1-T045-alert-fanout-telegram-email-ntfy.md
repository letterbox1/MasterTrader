---
id: P1-T045
kind: task
title: Fan out alerts to Telegram, ntfy and email through one consumer
phase: 1
type: BUILD
status: backlog
priority: critical
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P1-T004, P1-T044, P0-T023, P0-T045]
requirements: [R1.14]
roadmap_todos: [T1.31]
modules: [M17, M15]
dashboards: [D16]
tools: [git, uv, docker]
mcp: []
env: []
services: [nats, ntfy, alertmanager]
branch: p1/P1-T045-alert-fanout-telegram-email-ntfy
pr: ""
doc_sync: [docs/roadmap/phase-1-data-and-monitoring.md, docs/02-v1-architecture.md, docs/07-security-notes.md, docs/03-build-spec.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-22
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
review_result: ""
---

# P1-T045 · Fan out alerts to Telegram, ntfy and email through one consumer

## Goal / expected outcome

One notifier consumes `alert.{severity}.{kind}` and delivers to Telegram (alerts-only bot), ntfy and email (your provider's SMTP with an app password, or off) with routing by severity, dedupe and rate limits; Grafana/Alertmanager alerts reach it by webhook (one fan-out; nothing sends to a channel directly), and every notification lands in `ops.notification` for the UI.

## Context & references

- Roadmap: requirements [R1.14](../../../docs/roadmap/phase-1-data-and-monitoring.md#3-requirements) · ToDo [T1.31](../../../docs/roadmap/phase-1-data-and-monitoring.md#4-todo-sets)
- Spec: [03 M15](../../../docs/03-build-spec.md#m15-ui--alerts--mt_ui-calls-mt_api) (Telegram bot: alerts and digests) · [07 §9](../../../docs/07-security-notes.md#9-monitoring--incident-response) (alert list; Telegram + email + ntfy) · subjects [02 §6](../../../docs/02-v1-architecture.md#6-messaging-nats) (`alert.{severity}.{kind}`)
- Telegram rules: [12 §4](../../../docs/12-policy-and-compliance.md#4-per-platform-data--automation-rules) (Bot API ≤ 30 msg/s, minimal data) · P2 adds commands (R2.52)
- Decisions: [17 §D](../../../docs/17-decisions-register.md#d-other-decisions) P1-B007 (one fan-out: Grafana alerts → webhook → `alert.*` consumer → Telegram/ntfy/email), P1-B005 (email via your provider's SMTP with an app password, or off; USER task P1-T068); network placement is interim per gap P1-B020
- Build first, keys last: built and tested keyless against a fake Telegram API, a fake SMTP server and the real ntfy container; delivery to your real Telegram, phone and inbox is P1-T060
- Cross-phase prerequisites (depends_on): P0-T023 (Alertmanager), P0-T045 (P0 routes Alertmanager straight to Telegram; this task replaces that route with the webhook so there is one path)
- Depends on (this phase): P1-T004, P1-T044

## Requirements

- `mt_ui.telegram` alerts-only bot (python-telegram-bot, pinned): sends to your chat ID (`TELEGRAM_BOT_TOKEN`, `TELEGRAM_ALERT_CHAT_ID` from the secrets file at runtime); ignores and does not store incoming messages except `/start` from the configured chat
- Email via your mail provider's SMTP (TLS required; `SMTP_HOST`, `SMTP_PORT`, `SMTP_USERNAME`, `SMTP_APP_PASSWORD`, `ALERT_EMAIL_FROM`, `ALERT_EMAIL_TO` from the secrets file), or `alerts.email.enabled: false` (P1-T068); ntfy via HTTP publish with `NTFY_NOTIFIER_TOKEN`
- Routing: `critical` → all three; `warning` → Telegram + ntfy; `info` → notification centre + daily digest; configurable defaults in `config/alerts.yaml` (loosening routing = C3 via the break-glass CLI (`mtctl approve <id>` + TOTP) until Telegram C3 lands in P2; tightening C1)
- Dedupe key (kind + subject) with a 5 min window and escalation if still open after 15 min (defaults, configurable); global rate limit ≤ 1 msg/s per channel, never above Telegram's 30 msg/s
- Alertmanager webhook receiver → publishes `alert.*` so Grafana alerts reach all channels through one path; remove P0-T045's direct `telegram_configs` route in the same PR (test: Alertmanager has exactly one receiver, the webhook)
- Every alert also written to `ops.notification` (for the notification centre) and channel delivery results recorded (delivered/failed, latency)
- If one channel fails, the others still deliver; a failed channel raises `alert.warning.channel_down` on the remaining ones

## ToDo

- [ ] Implement the notifier service (in `telegram-bot` container or `monitor`) with three channel adapters
- [ ] Implement Alertmanager webhook bridge and `config/alerts.yaml`
- [ ] CLI `mt-alerts test --channel <c>` used by P1-T003/T060
- [ ] Migration for `ops.notification` delivery fields
- [ ] Write the tests listed under Verification
- [ ] Update the docs listed under Doc sync and tick the roadmap ToDo box(es)

## Verification

### Tests

- Unit: routing matrix; dedupe and escalation timers; message formatting with no secrets/account numbers beyond last 4 chars
- Integration: fake Telegram API, fake SMTP (aiosmtpd) and real ntfy container receive one alert each; Alertmanager webhook sample → all channels

### Scenarios

- Given email is off, when a critical alert fires, then Telegram and ntfy deliver and email is recorded as `disabled`, not `failed`
- Given Telegram API is unreachable, when a critical alert fires, then email and ntfy deliver, Telegram retries with backoff, and `channel_down` is raised
- Given 200 alerts in 1 s (alert storm), when processed, then they are grouped into a summary per kind and no channel exceeds its rate limit

### Stress / failure injection

- Storm: 10k alerts in 60 s; delivery stays within rate limits, summaries sent, memory bounded
- Fault: kill each channel in turn; the other two always deliver

## Acceptance criteria

- [ ] A test alert reaches all three channels in the keyless integration test (fake Telegram/SMTP, real ntfy); delivery latency recorded per channel; email `disabled` handled cleanly
- [ ] Grafana-originated alerts arrive through the same path
- [ ] CI green (ruff, mypy, pytest, `pit` bypass check, gitleaks)

## Exceptions & edge cases

- Telegram text from incoming messages is never stored, logged in full or passed to any model
- mt-api down: notifier still runs (consumes NATS directly) per 02 §9.3

## Cardinal rules (do NOT)

- Do NOT put Telegram text into any model input, RAG index or training set ([12 §4–5](../../../docs/12-policy-and-compliance.md#4-per-platform-data--automation-rules)); the bot only sends alerts.
- Do NOT commit secrets or paste them into chats, issues, logs or test fixtures; credentials come only from the sops/age secrets file (kept outside the repo) mounted on tmpfs ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Do NOT skip, weaken or delete a test (or widen a tolerance) to get CI green.
- Do NOT let any path loosen DQ thresholds, risk or alert routing without C3 (Telegram + TOTP + cool-down; in P1 via the break-glass CLI `mtctl approve` + TOTP); tightening is C1.
- Do NOT add an image without pinning it by digest, or vendored code that carries telemetry or referral IDs.

## Doc sync on completion

- `docs/roadmap/phase-1-data-and-monitoring.md`: tick T1.31 once every task traced to it in PHASE.md is done; note P1-T045 next to it.
- `docs/02-v1-architecture.md` §6: `alert.*` consumers include email + ntfy + notification centre
- `docs/07-security-notes.md` §9: routing table by severity
- `docs/03-build-spec.md` §M15: note the alerts-only bot from P1

## Branch & PR

- Branch: `p1/P1-T045-alert-fanout-telegram-email-ntfy`
- PR title: `P1-T045: Fan out alerts to Telegram, ntfy and email through one consumer`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P1-T045` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (one fan-out via webhook replacing P0 direct route (P1-B007); email via own SMTP app password or off (P1-B005); keyless build, live in P1-T060; P0 deps)
