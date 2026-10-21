# D10 · Models & Memory

| | |
|---|---|
| **Route** | `/models` (tabs: Registry · Decision questions · Bake-off · Gateway · Memory · RAG) |
| **Modules** | M21 Decision One + serving, M9 Hindsight & RAG, M7 training/distillation |
| **Phase** | 6 (Gateway tab from 0; Decision questions from 4) |
| **Mock-up reference** | None (new) |

## Purpose

Govern every model that influences decisions:
- what's deployed, how accurate and calibrated it is, and how fast;
- how much LLM budget is used;
- what the agents remember.

## Layout by tier

| Tier | Layout |
|---|---|
| ≥ xl | Tabs; each tab: table + detail panel |
| md | Tabs; detail as a drawer |
| ≤ ph | Tabs as a select; cards; charts full width |

## Tabs & widgets

| Tab | Shows | Source |
|---|---|---|
| **Registry** | Models by tier: **Tier A** (GBDT/linear/MLP: version, features, training range, calibration method, Brier/ECE, latency p50/p99 µs, status: candidate / shadow / production / retired), **Tier B** (SemIf readout, own Qwen-LoRA heads, Laya/Clef-flash benchmarks), **Gateway models** (Claude, custom endpoint, local). Detail: reliability diagram, feature importance (tier A), confusion matrix, drift (Evidently), lineage (teacher runs + outcomes used). | `/models/registry` |
| **Decision questions** | Question registry: id, type (choice/score/yes-no), options, version, model serving it, abstention threshold, calibration status, traffic/day, abstain rate, flip rate (determinism). Detail: recent decisions with inputs (truncated) and probabilities. | `/models/questions`, `/models/tierb/decisions` |
| **Bake-off** | Benchmark runs comparing decision models (own head vs Laya vs Clef-flash vs SemIf vs JSON generation) and tier-A candidates. Metrics: accuracy, log-loss, Brier, ECE per regime, coverage at target precision, latency p50/p95, flip rate; plus the FinMMEval Buy/Hold/Sell external check. | `/models/benchmarks` |
| **Gateway** | LiteLLM spend by role (debate, strategy-gen, explain, memory, chat) vs daily budget; requests, errors, fallbacks to local, latency; provider status | `/models/gateway/spend` |
| **Memory** | Hindsight banks (decisions, strategies, market-regimes, user, ops): counts, recent memories, search (point-in-time `as_of` option), delete a memory (C1; audited) | `/memory/search`, `/memory/banks` |
| **RAG** | Document search playground: query → hybrid results (vector + keyword, RRF, reranked) with scores, `as_of` filter, chunk source; index stats | `/rag/search` |

## Actions

| Control | Command | Level |
|---|---|---|
| Promote model (candidate → shadow → production) | `models.promote` | C2 (shows gate results: calibration, OOS, latency SLO); production for tier A/B used by **auto** strategies = **C3** |
| Roll back model | `models.rollback` | C1 |
| Run bake-off | `models.bakeoff.run` | C1 |
| Run distillation / retrain | `lab.validate.run` (kind = distill) | C1 |
| Edit question (options, threshold) | `models.question.update` | C1 (new version) |
| Adjust gateway budget | `system.settings.update` (budgets) | Raise = C3, lower = C1 |
| Delete memory item | `memory.delete` | C1 |

## Acceptance criteria

1. **Model metadata:** every production model shows calibration and latency against its SLO. Models out of SLO are flagged red.
2. **Promotion:** impossible without passing gates; the reason is shown.
3. **Budgets:** gateway budgets can only be raised via C3.

## Backend contract

- **Queries:** `/models/registry`, `/models/questions`, `/models/tierb/decisions`, `/models/benchmarks`, `/models/gateway/spend`, `/memory/search`, `/memory/banks`, `/rag/search`.
- **WebSocket topics:** `tierb`, `lab.job`.
- **Commands:**
  - `models.promote|rollback`, `models.bakeoff.run`, `models.question.update`, `memory.delete`;
  - `lab.validate.run`, `system.settings.update`.

_New relative to architecture §7.2 (added there): `models.question.update`, `memory.delete`, `/memory/banks`._
