# Memory, RAG & Model Serving (M9, M21)

_Research date 2026-10-21. (U) = unverified; "est." = estimated from hardware first principles. Latencies must be benchmarked on the actual box._

## Summary

| Area | Pick | Licence | Latency |
|---|---|---|---|
| Agent memory | **Hindsight 1.0.0**, self-hosted: **slim** image, our Postgres 16 in its own schema, local embedder + reranker via TEI, LLM via the LiteLLM gateway | MIT | Recall 100–600 ms with a CPU reranker (vendor figure); retain is LLM-bound (seconds) |
| Embedder | **bge-small-en-v1.5** (384-d) now. **Qwen3-Embedding-0.6B** (Matryoshka 512/1024) once a GPU is available | MIT (U) / Apache-2.0 (U) | ~2–5 ms / ~40–100 ms per query on CPU (est.) |
| Embedding/rerank server | **HF Text Embeddings Inference (TEI)**, CPU image; **fastembed** (ONNX) for in-process use | Apache-2.0 | ~900–2,000 texts/s (Hindsight's measurement) |
| Reranker | **bge-reranker-v2-m3** or **mxbai-rerank-base-v2**; ms-marco-MiniLM-L-6 if CPU is tight. **Avoid Jina rerankers** (CC-BY-NC) | Apache-2.0 | Tens to hundreds of ms for 30–50 pairs on CPU (U) |
| Document RAG | Postgres: **pgvector HNSW (halfvec) + native tsvector/`ts_rank_cd` + pg_trgm**, fused with **Reciprocal Rank Fusion**, then cross-encoder rerank, recency decay and a **point-in-time filter** | PostgreSQL | ms-level retrieval + rerank |
| Hot-path decision, **Decision One tier A** | **LightGBM** (or XGBoost/linear/small MLP) compiled to **ONNX Runtime / Treelite / lleaves**, run **in-process** inside the Nautilus strategy | MIT / Apache-2.0 | **~10–50 µs per prediction** (published benchmarks, indicative) |
| Text/context decisions, **Decision One tier B** | A **decision model** ("System One" class, no text generation). Phase 1: **SemIf**-style logit readout on Qwen3.5-4B (no training). Phase 2: our own **Qwen3 0.6B/1.7B + LoRA + classification head** (Clef pattern), distilled and calibrated. Benchmarked against **Laya** and **Clef-flash** (both Apache-2.0) | Apache-2.0 / MIT | ~2–12 ms GPU for 0.6B (est.); ~15–40 ms for 4B; Clef-flash ~0.4 s local |
| Research / chat / debate routing | **LiteLLM proxy** (≥ 1.83, pinned by hash or image digest): Claude API → your custom endpoint → local model fallback; per-role budgets | MIT core | A few ms of overhead (U); **never on the hot path** |

## 1. Hindsight: self-hosted agent memory

**Role:** episodic and agent memory. It covers decisions, outcomes, reflections, lessons, and the user's preferences and mental models. It is **not** the document store (that's §3).

**Deployment:**

| Setting | Value |
|---|---|
| Image | `ghcr.io/vectorize-io/hindsight` **slim** variant (~500 MB; the full image is ~9 GB with bundled models), pinned by digest |
| Database | Our Postgres 16: `HINDSIGHT_API_DATABASE_URL`, `HINDSIGHT_API_DATABASE_SCHEMA=hindsight`; `VECTOR_EXTENSION=pgvector`; `TEXT_SEARCH_EXTENSION=native` |
| Embeddings | `HINDSIGHT_API_EMBEDDINGS_PROVIDER=tei` → our TEI container running bge-small-en-v1.5. The **same embedder as document RAG**, so one model serves both. |
| Reranker | `HINDSIGHT_API_RERANKER_PROVIDER=tei` → TEI reranker. Lower the candidate count (default 300) to cut recall time. |
| LLM (retain / consolidate / reflect) | `HINDSIGHT_API_LLM_PROVIDER=litellm` → our gateway. Spend is metered and capped, and the provider can be switched (Claude, custom endpoint, local Qwen) without touching Hindsight. For small local models: set `HINDSIGHT_API_LLM_STRICT_SCHEMA=true` and `RETAIN_MAX_COMPLETION_TOKENS` (> 3000). |
| Access | API :8888 and UI :9999, internal network only. Built-in **MCP endpoint** per memory bank (`/mcp/{bank_id}/`) is available for Phase 8. |
| Telemetry | No phone-home was found. OpenTelemetry and Prometheus are opt-in. |
| Footprint | API ~1–1.5 GB RAM (slim: 0.5–1 GB) + Postgres |

> ⚠️ **The embedding dimension is fixed once memories exist.** Changing it means re-embedding everything. Choose 384-d (bge-small) now. If we later move to Qwen3-Embedding, do a planned re-embed migration.

**Memory banks:**
- `decisions`: every M8 decision, its settlement and the reflection.
- `strategies`: per-strategy lessons.
- `market-regimes`
- `user`: your preferences and standing instructions.
- `ops`: incidents and what fixed them.

**Point-in-time recall** in backtests filters by memory creation time ≤ `as_of`, so backtests can't "remember the future".

**Alternatives considered:**
- **mem0** (Apache-2.0): telemetry is ON by default.
- **Graphiti** (Apache-2.0): needs Neo4j/FalkorDB, and its MCP server has no auth.
- **LightRAG** (MIT): Postgres-capable, but extraction needs a ~30B-A3B-class model.

LightRAG is kept as an **optional, offline** graph layer over filings (§3.7).

## 2. Local embedders & rerankers

| Model | Size | Dims | Max tokens | Licence | Use |
|---|---|---|---|---|---|
| **bge-small-en-v1.5** | 33M (U) | 384 | 512 | MIT (U) | **Default** (CPU, fast) |
| **Qwen3-Embedding-0.6B** | 0.6B | 32–1024 (MRL) | 32K | Apache-2.0 (U) | **Upgrade** with a GPU (MMTEB 64.3) |
| nomic-embed-text-v1.5 / v2-moe | 137M / 475M | 768 (MRL) | 8192 / 512 | Apache-2.0 | Alternative (needs prefixes) |
| snowflake-arctic-embed-s/m, m-v2.0 | 33M–305M | 384–768 | 512–8192 | Apache-2.0 | Alternative |
| mxbai-embed-large-v1 | 335M | 1024 | 512 | Apache-2.0 | Alternative |
| bge-m3 | 568M | 1024 + sparse | 8192 | MIT (U) | Multilingual; heavier |
| EmbeddingGemma-300M | 308M | 768 (MRL) | 2048 | Gemma ToU (U) | Avoid (licence) |
| all-MiniLM-L6-v2 | 22M | 384 | 256 | Apache-2.0 | Fallback only |

**Finance:**
- FinBERT stays as the sentiment classifier; it isn't an embedder.
- Research (FinMTEB) shows **keyword (BM25-style) search beats dense embeddings on financial text similarity**. That's why hybrid retrieval is mandatory.
- Later option: fine-tune bge-small on our own filing/news pairs.

**Serving:**
- **TEI** (Apache-2.0; embeddings, `/rerank`, dynamic batching) as a shared container.
- **fastembed** (ONNX, Apache-2.0) for in-process embedding in Python services.
- Ollama is **not** used for embeddings under load (`OLLAMA_NUM_PARALLEL` defaults to 1).

## 3. Document RAG design (Postgres)

1. **Table:** `rag.doc_chunk(id, doc_id, source, tickers[], published_at, ingested_at, valid_from, section, text, tsv tsvector GENERATED, emb halfvec(384))`.
   - Never update a chunk in place; a revision is a new row.
2. **Point-in-time filter on every query:** `ingested_at <= :as_of AND published_at <= :as_of`.
3. **Indexes:**
   - HNSW on `emb` (`halfvec_cosine_ops`, m=16, ef_construction=64);
   - GIN on `tsv`;
   - GIN trigram on tickers/entities;
   - B-tree on `ingested_at` and `(ticker, published_at)`.
   - For filtered queries, set `hnsw.iterative_scan = relaxed_order` and `ef_search` 100–200.
4. **Retrieval:**
   1. Vector top-50 and keyword top-50.
   2. **RRF** in SQL (`Σ 1/(60+rank)`).
   3. Cross-encoder rerank of the top 30–50.
   4. Recency decay.
   5. Return chunks with source ids, for provenance.
5. **Chunking:**
   - **Filings:** split by Item/section (1A Risk Factors, 7 MD&A…), then 512–800 tokens with ~15% overlap. Tables become separate markdown chunks. Each chunk gets a context header `{ticker} {form} {period} {section}`.
   - **News:** one chunk per article (paragraph windows if long). Dedupe wire copies with MinHash or cosine > 0.95.
6. **Caching:**
   - embedding cache keyed by `sha256(model||text)`;
   - retrieval cache keyed by `(query, as_of bucket, filters)`;
   - Anthropic prompt caching via LiteLLM;
   - vLLM/SGLang prefix caching locally.
7. **Graph RAG (optional, later):** LightRAG over filings (supplier/customer/subsidiary/litigation links), run offline in batch for the research path only, once plain hybrid retrieval is benchmarked.
8. **Extensions:**
   - **Not used:** `pg_textsearch` (needs PG17+); VectorChord (AGPL/ELv2).
   - **Optional:** ParadeDB `pg_search` (AGPL, fine privately) if true BM25 is ever needed.
   - **Scale-up:** `pgvectorscale` only above ~10M vectors.

## 4. Decision One: decision models + microsecond engine

_Evidence: [research/decision-models-system-one.md](research/decision-models-system-one.md)._

### 4.1 What "decision models" are (and the candidates)

**What they are:**
- A new model class (Sep–Oct 2026), usually called **"System One" / decision models**.
- They **don't generate text**. Given a *state* (text, JSON, image) and typed questions, they return **probabilities over a fixed option set in one forward pass**:
  - `choice`: pick one;
  - `score`: an ordinal value;
  - `noul`: yes/no.
- There's no decoding, parsing or JSON repair, and no sampling: the same input gives the same scores, apart from the GPU caveats below.

| Candidate | Licence / access | Fit for MasterTrader |
|---|---|---|
| **Jev** (TypeSafe AI) | Closed, hosted only, **paid** | ❌ Excluded (free-only, no self-hosting). Kept as a published reference point. |
| **Microsoft-Decision-1** (closest to "DecisionOne") | Closed, **paid** | ❌ Excluded |
| **Laya** (Convai) | Apache-2.0, ModernBERT encoder 322–421M | ⚠️ Fast (~7 ms/question batched on a T4) but **weak zero-shot** (below the majority baseline), over-confident, 512–1024-token context. Only useful **after fine-tuning**, for short text. Benchmark candidate. |
| **Clef / Clef-flash** (Cloudflare) | Apache-2.0 weights; Qwen3.5-9B / Qwen3.8-27B + LoRA + joint schema head | ✅ **Reference architecture** and benchmark baseline. Self-hosted Clef-flash is ~0.4 s on a 3090 (8–24 GB VRAM), so it's a "rich context" option, not the fast path. |
| **SemIf** (formerly OpenJev) | MIT; no training, reads option-token logits on stock Qwen3.5-4B | ✅ **Use where it logically applies:** zero-shot boolean/categorical checks over text when no labels exist yet. ~5× faster than JSON generation. 4B is good (0.81 balanced accuracy); 0.6B is worse than chance. Uncalibrated. |
| Liquid d1 (~8 ms on a 4090), Vela (ONNX), H2O-Lightning-4B, Intern-Decision (U) | Mostly Apache | Optional extra benchmark candidates |

**Evidence gaps:**
- **No public evaluation of any decision model on trading/finance decisions, or calibration on market data.**
- Benchmarks are mostly vendor-reported, and independent tests show shipped models are **miscalibrated for a new domain**.
- So we *build and calibrate our own* (the Clef pattern on a small Qwen), and adopt only what beats the baseline in our own walk-forward tests.

### 4.2 Verdict: decision models vs trees

| Input / job | Winner | Why |
|---|---|---|
| Numeric, tabular, microstructure features; sub-millisecond; bit-exact backtests | **Tier A: compiled GBDT/linear** | ~10–50 µs, bit-deterministic on CPU, easy isotonic calibration. No decision model has been shown to beat trees on numeric time series. |
| News, filings, transcripts, social posts, debate rationales, charts (images) | **Tier B: decision model** | Reads text natively. One forward pass instead of decoding (~5× faster than JSON generation, with no parse failures). Outputs real option probabilities, not a generated number. |
| Brand-new criteria with no labels yet | **SemIf readout** (Qwen3.5-4B) | Zero-shot and runtime-defined, but uncalibrated, so flags and vetoes only |
| Final trade decision + sizing | **Tier A**, or a small stacker over tier A features + decision-model scores | Keeps determinism and calibration in one place |

So the current approach (trees) **stays authoritative for numeric decisions**. **Decision models replace JSON-generating LLMs** for every text and context judgement. Their calibrated scores become **features for tier A**.

### 4.3 Design

**Tier A: microsecond engine (order path, authoritative)**
- **Model and runtime:**
  - LightGBM/XGBoost/linear/small MLP;
  - compiled to **ONNX Runtime / Treelite / lleaves**;
  - **in-process** in the Nautilus strategy (no network hop).
- **Latency:** ~10–50 µs.
- **Calibration:** isotonic/Platt on a time-ordered holdout, tracking Brier/ECE.
- **Inputs:** M6 numeric features + **cached tier B scores** (from NATS KV).

**Tier B: decision models (asynchronous, event-driven, never on the tick path)**
- **Questions are typed and versioned in a registry**, e.g.:
  - `news_direction{bull,bear,neutral}`;
  - `event_type{guidance_cut, M&A, hack, listing, regulation, …}`;
  - `regime{trend,range,crisis}`;
  - `veto{yes,no}`;
  - `relevance{yes,no}`;
  - `rug_risk_text{low,med,high}`;
  - `debate_quality{sound, stale_data, contradictory}`.
- **Stage 1 (Phase 4, no training):**
  - **SemIf-style logit readout** on Qwen3.5-4B for relevance gating (replaces the planned LLM gate) and first-pass flags;
  - shared-prefix mode for many criteria per document.
- **Stage 2 (Phase 6): our own decision models.**
  - **Base:** **Qwen3-0.6B or 1.7B (dense, ONNX-exportable)**.
  - **LoRA and head:** LoRA (rank 8–64) + **classification head** (`Qwen3ForSequenceClassification` + PEFT `SEQ_CLS`) or a Clef-style joint schema head scoring several questions in one pass.
  - **Training labels:** distilled from M8 debate decisions (the teacher), then **corrected against realised outcomes** (forward returns / barrier hits) so it doesn't just copy the debate's biases.
  - **Validation:** purged, embargoed walk-forward CV; option shuffle/rename augmentation.
  - **Loss:** CE + λ·Brier.
  - **Calibration:** post-hoc temperature/isotonic on a walk-forward holdout.
  - **Abstention:** thresholds set at a target precision ("auto-decide coverage"), with abstain as the default.
  - **Serving:** vLLM pooling runner (`/classify`) on GPU, or ONNX Runtime on CPU (FP32 for reproducible backtests).
  - **Expected latency:**
    - **~2–12 ms per decision on a consumer GPU (0.6B)**;
    - ~15–40 ms for 4B;
    - 0.6B ONNX int8 on CPU ~100–400 ms (est.; benchmark it).
- **Benchmark bake-off before adopting anything:**
  - **Contenders:** our Qwen-LoRA head vs fine-tuned Laya vs self-hosted Clef-flash vs **Kev-4B/9B** (challenger, from the CryptoTrader review) vs SemIf zero-shot vs the old JSON-generation baseline.
  - **Data:** our own data, plus the **CLEF-2026 FinMMEval Buy/Hold/Sell** task as an external check.
  - **Metrics:** accuracy, log-loss, **Brier, ECE per regime**, coverage at target precision, latency p50/p95, determinism (flip rate).
  - **Promotion:** only via the §8 gates, with the teacher in shadow.
- **How outputs are used:**
  - Scores go to NATS KV as tier-A features.
  - A direct **veto** is allowed only above a calibrated high-precision threshold.
  - Scores also feed M4 (airdrop/rug text risk), M2 (relevance), M10 (anomaly explanations) and M8 (pre-screening).

**Operating rules (adopted from the CryptoTrader review):**
- **Inputs:** Telegram text is **never** a model input (Telegram API ToS §1.5). Rows with `model_input_ok = false` are refused at the question boundary ([12 §5](12-policy-and-compliance.md#5-data-provenance-tagging-one-mechanism-for-all-data-terms)).
- **Question shape:** binary or low-option questions only; each question gets a **state budget of ~320 tokens** (compact, structured state, not raw documents).
- **Thresholds per question** come from measured disagreement with the teacher and with outcomes, not one global cut-off.
- **Shadow checks:** ~5% of tier B decisions are re-asked of the teacher (M8 / gateway model) in shadow; disagreement rate is tracked per question in D10.
- **Labels come from outcomes or from you (D10 labelling queue), never from shadow-model outputs**, so models don't train on each other's mistakes.
- **Retraining cadence:** monthly fine-tune, promoted only through the gates.
- **Social battery** (for X/Bluesky/Discord/Farcaster text, never Telegram): `organic`, `bot_like`, `scam_language`, `narrative`, `stance`, `conviction`.
- **Laya serving:** bind to `127.0.0.1` with `LAYA_API_KEY`; on CPU each question is ~0.7 s and independent, so batch by question. Laya has no ROCm build: on an AMD GPU (e.g. 7900 XTX) use llama.cpp with Vulkan for the Qwen-based models instead.

**Determinism controls (GPU):**
- **Precision and model:** FP32 head, pinned model revision.
- **Batching:** batch size 1 (or fixed padded batch) on the decision path.
- **Prefix caching:** off on the decision path (SemIf saw 5–6/777 flips from prefix reuse in BF16).
- **Audit:** `prompt_hash`, `model_revision` and `question_version` logged on every decision (M17).
- **Backtests:** run on CPU ONNX FP32 so they reproduce exactly.

**Hardware:**
- Tier A: CPU only.
- Tier B at ~10 ms: one consumer GPU (16–24 GB also covers Clef-flash FP8 and the Hindsight/LightRAG LLM work). Without a GPU, tier B runs on CPU at hundreds of ms and serves slower flags only.

## 5. Model gateway: research, chat & debate routing (M21)

**The trading hot path (tiers A and B) never calls a remote API**, and the engine has no dependency on the gateway.

Everything else (M8 debate agents, M7 strategy generator, M10 explain agent, Hindsight's LLM, chat via UI/Telegram/MCP) calls **one OpenAI-compatible gateway: LiteLLM proxy** (MIT core).

```yaml
model_list:
  - model_name: research-primary      # Claude (Anthropic API, prompt caching on)
  - model_name: research-custom       # your custom OpenAI-compatible endpoint
  - model_name: local-advisor         # vLLM / llama-server Qwen3.5-4B (or 9B)
  - model_name: local-embed           # TEI bge-small (embeddings)
router_settings:
  routing_strategy: latency-based-routing
  fallbacks: [{research-primary: [research-custom, local-advisor]}]
  context_window_fallbacks: [{local-advisor: [research-primary]}]
```

- **Budgets:**
  - a virtual key per role (debate, strategy-gen, explain, memory, chat) with `max_budget` + `budget_duration: 1d`;
  - a global provider budget.
  - **When the budget is exhausted it falls back to local models** instead of failing.
  - Spend goes to Grafana.
- **Endpoints:** any OpenAI-compatible endpoint (your own server, OpenRouter for research only, another box) is just another `model_list` entry, so routing is a config change.
- **⚠️ Supply chain:**
  - LiteLLM releases **1.82.7 and 1.82.8 were malicious** (PyPI compromise, March 2026).
  - Use ≥ 1.83, pinned by hash or by official image digest.
  - Give it only the API keys it needs; keep it on the internal network.

## 6. Where this lands in the build

| Module | Change |
|---|---|
| M6 Features | Feature snapshots logged per decision (for distillation) |
| M7 Lab | Trains, calibrates, compiles and benchmarks tier-A models and tier-B decision models (LoRA + head); runs the decision-model bake-off; distillation jobs; registers models in MLflow |
| M8 Agents | Run via the gateway; their decisions are the teacher log |
| M9 Memory & RAG | Hindsight (agent memory) + `rag` schema hybrid retrieval, sharing one TEI embedder/reranker |
| **M21 Decision One & model serving** | Tier A runtime (in-strategy), tier B decision-model service (SemIf readout → own Qwen-LoRA head), question registry, LiteLLM gateway, TEI, model registry, benchmarks |
| M17 Observability | Latency histograms per tier, timeout and fallback counts, LLM spend |
