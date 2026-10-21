_Raw notes from the research agents (2026-10-21). They back up [../10-memory-rag-and-models.md](../10-memory-rag-and-models.md) §4. Many sites (HF, arXiv, Cloudflare) were unreachable from the sandbox, so (U) = taken from search summaries. **Almost all benchmarks are vendor-reported. No finance/trading evaluation or market-data calibration study exists for any of these models.**_

# "System One" / decision models

**The category:** models that don't generate text. You give them a **state** (text/JSON/image) plus typed questions:
- **choice:** pick one option;
- **score:** an ordinal value;
- **noul:** yes/no.

They return probabilities over the allowed options in a single forward pass. TypeSafe AI coined the term with Jev (2026-09-15). No model is literally called "DecisionOne"; the closest is **Microsoft-Decision-1**.

| Model | Who | Open? | Base | Latency (as reported) | Accuracy notes | Cost |
|---|---|---|---|---|---|---|
| **Jev** | TypeSafe AI | Closed, hosted only | — | Vendor 70–500 ms; OpenRouter p50 0.17 s; Cloudflare median 524 ms (U) | Banking77 0.870 acc (one paper) / 79.74 macro-F1 (Cloudflare). ECE 0.157 in a CSS study; "calibrated pooled, not within benchmark". Cisco: a fine-tuned 1B encoder beat it on 5/6 safety sets | **Paid** ($0.042/M input) → excluded |
| **Microsoft-Decision-1** | Microsoft | Closed | Qwen3.5-9B | 85/125 ms vendor; 0.19 s OpenRouter (U) | Card: not for sole automated high-stakes decisions | **Paid** → excluded |
| **Laya** | Convai Innovations (`NandhaKishorM/laya`) | **Apache-2.0** | ModernBERT-large 421M / mmBERT 322M encoder | T4 33–40 ms per question, ~7 ms batched; MLX 7–14 ms; CPU ~453 ms per 4-question call | Zero-shot typed decisions 0.362 (< majority 0.461); fine-tuned 0.766; over-confident as shipped; noul label bias. Context 512–1024 | Free; `pip install laya`, ONNX, server, MCP |
| **Clef / Clef-flash** | Cloudflare (2026-10-01) | **Apache-2.0** weights | Qwen3.8-27B / **Qwen3.5-9B** + rank-256 LoRA + **joint schema head** | Vendor: flash 38.8 ms median (Workers AI). Local: ~0.43 s on an RTX 3090 (NF4) | Vendor: best on 7/10 decision benchmarks; Banking77 F1 94.2. No published calibration comparison | Self-host free (flash: FP8 ~11.5 GB / NF4 8 GB / BF16 ~24 GB; 27B ~60 GB); hosted is paid |
| **SemIf** (formerly OpenJev) | Independent (`theoleecj/semif`) | MIT | **No training**: reads next-token logits of the option tokens on stock Qwen3.5-4B / Qwen3-0.6B / MiniCPM5-2B | 3090 + 4B: 21 binary criteria in 1.02 s vs 5.33 s for JSON generation; 2.3/s fresh, 20/s with prefix reuse | Balanced accuracy 0.813 (4B), 0.686 (2B), 0.440 (0.6B, worse than chance); agrees with Jev 0.845. **No calibration published**; prefix reuse flipped 5–6/777 decisions (BF16 nondeterminism) | Free |
| Others (U) | — | Mostly Apache | H2O-Lightning-4B (Qwen3.5-4B, plain vLLM); Liquid d1-3B / d1-omni-600M (~8 ms on 4090, GGUF); Vela (ModernBERT 0.3B–9B, ONNX); Intern-Decision 0.8/2/4B; Juspay xor (LoRA on Qwen3.6-35B-A3B) | — | — | — |

**Ecosystem:**
- https://github.com/raullenchai/awesome-system-one
- https://systemonemodels.org/
- **Benchmarks:** JevBench, Artificial Analysis Decision Index, jev-ood-calibration.
- **External finance benchmark worth using:** CLEF-2026 FinMMEval Buy/Hold/Sell task (unrelated to Cloudflare's Clef). https://arxiv.org/pdf/2602.10886

**Fine-tuning tooling:**
- `MersivMedia/clef-finetune`: LoRA + head, with a CE + λ·Brier loss and ECE / auto-decide coverage reports. **Never run on real Clef weights.**
- HF `Qwen3ForSequenceClassification` + PEFT (`task_type=SEQ_CLS`, `modules_to_save=["score"]`).
- vLLM pooling runner `/classify` (`--convert classify`).
- **TEI doesn't support Qwen3 classification yet** (issue #643).
- Qwen3.5's hybrid Gated-DeltaNet layers may not export to ONNX cleanly (U), so prefer a dense Qwen3 backbone for ONNX.

**Sources:**
- https://openrouter.ai/typesafe/jev-1.13
- https://blogs.cisco.com/ai/jev-decision-models-on-trial
- https://arxiv.org/pdf/2609.24574
- https://github.com/NandhaKishorM/laya
- https://blog.cloudflare.com/clef-decision-models/ (U)
- https://github.com/MersivMedia/clef-finetune
- https://github.com/turlockmike/clef-flash-local
- https://github.com/theoleecj/semif
- https://www.infoworld.com/article/4234290/microsoft-separates-decision-making-from-generative-ai-with-a-new-model (U)
- https://docs.vllm.ai/en/stable/models/pooling_models/classify/
- https://github.com/huggingface/text-embeddings-inference/issues/643
