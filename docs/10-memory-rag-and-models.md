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
| Fast advisor, **Decision One tier B** | **Qwen3.5-4B** (alternatives: Gemma 4 E4B, Phi-4-mini) on **vLLM** (GPU) or **llama.cpp server** (CPU), strict JSON schema, temperature 0, hard timeout | Apache-2.0 | GPU ~150–300 ms per decision (est.); CPU: seconds |
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

## 4. Decision One: fast, accurate, concurrent decisions

**Honest framing:** no language model is "near-zero latency". Even a 0.6B model on a GPU costs tens of milliseconds, and on CPU hundreds of ms to seconds. So Decision One is **two tiers**, and only the first is in the order path.

### Tier A: microsecond engine (in the order path)

**Model:** gradient-boosted trees (LightGBM/XGBoost/CatBoost), logistic/linear, or a small MLP, trained on M6 features.

**Compilation and loading:**
- Compiled to **ONNX Runtime** (MIT), **Treelite** (Apache-2.0) or **lleaves** (LLVM-compiled LightGBM).
- Loaded **in-process** in the Nautilus strategy/actor. **No network hop**; a NATS round-trip alone is ~50–200 µs.

**Latency:**
- Published single-row benchmarks: ~10–50 µs per prediction (indicative).
- Concurrency is trivially high (pure CPU functions, one per strategy instance).

**Output:** a **calibrated probability / expected edge** (isotonic or Platt calibration on a time-ordered holdout; Brier and ECE tracked). Deterministic sizing (M11) consumes it, never the raw model.

**Features:** computed incrementally (Nautilus indicators), plus **cached tier-B flags** read from NATS KV.

### Tier B: millisecond advisor (asynchronous, never blocks an order)

**Model:** **Qwen3.5-4B** (Apache-2.0, strongest under 5B per Artificial Analysis).
- Alternatives: **Gemma 4 E4B** (now Apache-2.0), Phi-4-mini (MIT), Granite 4 (Apache-2.0).
- **9B** where there's GPU headroom.

**Serving:**
- **vLLM** (Apache-2.0; continuous batching, automatic prefix caching, xgrammar/guidance JSON) on a GPU.
- **llama.cpp server** (MIT; `--parallel` slots, `json_schema`/GBNF) on CPU.
- SGLang is an equivalent alternative to vLLM.

**Contract:**
- Fixed system prompt (prefix-cached).
- Strict JSON schema: an `action` enum (`regime`, `veto`, `annotate`) plus `confidence` and `reason_codes`.
- `temperature=0`.
- **Hard timeout.** On timeout or invalid output the result is ignored and tier A carries on.

**Uses:**
- Regime and veto flags refreshed per bar or per event.
- News/event reaction classification (seconds-scale).
- Fast pre-screening for M8.

**Latency (est.):**
- GPU (RTX 4090-class): ~20–60 ms time-to-first-token for 1k-token prompts; ~150–300 ms per ~30-token JSON decision.
- CPU-only: seconds. So **tier B is practical for bars ≥ 1 s, or as precomputed flags.** Scalpers rely on tier A alone.

### Teacher → student distillation (how "high accuracy" is earned)

1. **Log the teacher.** Every M8 debate decision (Claude via the gateway) is logged with its exact point-in-time feature snapshot, prompt hash, rationale and later **realised outcome**.
2. **Distil into tier A** nightly/weekly. Train LightGBM on features with teacher outputs as soft labels **plus realised forward returns**, using purged walk-forward CV with an embargo.
3. **Optionally fine-tune tier B.** LoRA/SFT on (context → teacher JSON) so the 4B advisor imitates the debate cheaply.
4. **Promote by gate only.** A student replaces anything only after matching the teacher's out-of-sample P&L and risk (build spec §8). The teacher keeps running in shadow for disagreement audits.

### Hardware note

- Tier A needs only CPU.
- Tier B with low latency wants **one consumer GPU** (e.g. 16–24 GB VRAM). Without a GPU, tier B runs on CPU at seconds-scale and is used only for slower flags.
- Hindsight retain, LightRAG and debate agents all benefit from the GPU too, or go via the gateway to Claude/your endpoint.

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
| M7 Lab | Trains, calibrates, compiles and benchmarks tier-A models; distillation jobs; registers models in MLflow |
| M8 Agents | Run via the gateway; their decisions are the teacher log |
| M9 Memory & RAG | Hindsight (agent memory) + `rag` schema hybrid retrieval, sharing one TEI embedder/reranker |
| **M21 Decision One & model serving** | Tier A runtime (in-strategy), tier B advisor service, LiteLLM gateway, TEI, model registry, benchmarks |
| M17 Observability | Latency histograms per tier, timeout and fallback counts, LLM spend |
