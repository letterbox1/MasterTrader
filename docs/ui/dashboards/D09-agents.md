# D09 · Agents & Decisions

| | |
|---|---|
| **Routes** | `/agents` (runs & signals), `/agents/runs/:id` (debate detail) |
| **Modules** | M8 debate agents, M9 memory & RAG, M21 tier B, M10 anomaly explanations |
| **Phase** | 6 (tier-B panels from 4) |
| **Mock-up references** | `multi-agent-debate-consensus-terminal.png`, `mobile-multi-agent-debate-consensus.png` (fix model labels: Claude via the gateway, local decision models) |

## Purpose

Run and inspect the AI layer:
- **multi-agent analyses:** analysts → bull/bear debate → risk debate → portfolio manager;
- the **signals** they produce, with provenance;
- **decision-model** outputs;
- **anomaly explanations**;
- how past decisions turned out (settlement + reflection).

## `/agents`

| Tier | Layout |
|---|---|
| ≥ 2xl | Left: "New analysis" (6). Centre: runs list (12). Right: latest signals + tier-B stream (6). Below: outcome scorecard. |
| xl–md | Runs list + right column stacked |
| ≤ ph | Tabs: Runs · Signals · Decisions · Scorecard; "New analysis" button → sheet |

**Widgets:**

| Widget | Shows | Source |
|---|---|---|
| New analysis | Instrument(s) or portfolio question; depth (quick / standard / deep); model route (default Claude via the gateway; local-only option); budget estimate (tokens/$); context toggles (news window, filings, memory) | `/models/gateway/spend` (budget) |
| Runs list | Time, subject, trigger (scheduled / event / manual / anomaly), status, PM decision (direction, conviction, horizon), risk outcome, cost, duration | `/agents/runs`, WS `agents.run` |
| Signals | Signals from agents + strategies + tier B: direction, probability/conviction, horizon, provenance count, risk outcome | `/signals`, WS `signals` |
| Decision stream (tier B) | Recent decision-model outputs per question (`TierBScore`), with abstentions shown | `/models/tierb/decisions`, WS `tierb` |
| Outcome scorecard | Settled decisions: hit rate, calibration (reliability diagram), Brier, P&L if traded, by agent role / model / horizon; teacher vs student agreement | `/agents/runs?settled=1&metrics=1` |
| Anomaly explanations | Latest anomalies with their explain-agent briefs | `/notifications?kind=anomaly` |

## `/agents/runs/:id`: debate detail

| Tier | Layout |
|---|---|
| ≥ xl | Header (subject, trigger, models used, tokens/cost, duration) + **stage timeline** (analysts → research debate → trader → risk debate → PM) + the selected stage's turns + evidence panel (right) |
| md–lg | Timeline as horizontal steps; evidence as a drawer |
| ≤ ph | Single thread of `AgentTurn`s grouped by stage; evidence via "Sources (n)" sheet |

**Widgets:**

| Widget | Shows |
|---|---|
| `AgentTurn` | Role (technical, sentiment, news, fundamentals, macro/events, bull, bear, research manager, trader, risk ×3, PM), stance, confidence, text, **cited sources** (documents, bars, filings, memory items), tool calls (collapsed) |
| `ConsensusBar` | Bull vs bear weight, PM decision |
| Final signal card | Direction, conviction, horizon, rationale summary, **risk manager result** (pass / veto / approval), resulting order (if any) |
| Evidence panel | `ProvenanceList` with open/preview |
| Memory used | Hindsight memories recalled (with bank + timestamp; point-in-time) |
| Settlement | When the horizon ends: realised outcome, alpha vs benchmark, reflection text, memory written |

**Actions:**

| Control | Command | Level |
|---|---|---|
| Re-run with changes | `agents.run_analysis` | C1 |
| Send signal to a strategy (LLM-signal strategies only) | `strategy.update_params` / route | C1 |
| Create order from signal | Opens `OrderTicket` pre-filled | C2 on submit |
| Flag decision as bad (feedback) | `journal.note.add` | C0 |

## Actions (global)

| Control | Command | Level |
|---|---|---|
| Start analysis | `agents.run_analysis` | C1 (shows budget) |
| Ask decision model | `models.tierb.ask` | C0 |
| Schedule recurring analysis | `system.settings.update` (schedules) | C1 |

## Acceptance criteria

1. **Provenance:** every agent claim with a number links to its source (provenance). Unsourced numbers are flagged by the server.
2. **Visibility:** cost and model are visible on every run. Budget-exhausted runs show the local fallback.
3. **Point-in-time:** settlement/reflection appears only after the horizon (it can't leak into past views).

## Backend contract

- **Queries:** `/agents/runs` (+ `/{id}`), `/signals`, `/models/tierb/decisions`, `/models/gateway/spend`, `/memory/search`, `/notifications?kind=anomaly`.
- **WebSocket topics:** `agents.run`, `signals`, `tierb`, `notifications`.
- **Commands:** `agents.run_analysis`, `models.tierb.ask`, `journal.note.add`, `system.settings.update`.
