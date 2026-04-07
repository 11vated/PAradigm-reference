# 135 — Hardware budget for v0.1 context ceiling

## Question

What is the minimum consumer hardware spec for v0.1, what context window can it sustain, and what is the corresponding latency budget for each kernel operation?

## Why it matters (blast radius)

GSPL is local-first by axiom (Round 1, 53). If v0.1 only runs on an H100, the local-first claim is dead, the moat against Gemini collapses, and the year-1 roadmap (Brief 108) is invalidated. We need a concrete hardware floor that includes the backbone, the kernel, the verifiers, and the eval battery (Brief 134) in a single envelope, *and* the context window we promise creators must be the one that fits.

## What we know from the spec

- Brief 053 specifies local-first as a Round 2 commitment.
- Brief 075 (Round 3) closes the GPU dependency hole by specifying CPU-only fallback engines, but the *intelligence layer* hardware budget was deferred.
- Brief 122 selects Qwen3-MoE-A22B as the v1 default backbone — that is a 235B-parameter MoE with 22B active per token.
- Brief 110 (Round 6) surveyed open-weight backbones; smaller alternatives were noted.

## Findings

1. **Three hardware tiers cover the v0.1 audience.**
   - **Floor:** 24GB VRAM single GPU (RTX 4090 / RTX 5090 / Mac M2/M3/M4 Pro 32GB unified). Sustains a 14B-class dense model or a 30B MoE with 3B active, at fp16 or 4-bit quantized.
   - **Mid:** 48GB VRAM (RTX 6000 Ada / dual 4090 / Mac Studio M3 Max 64GB). Sustains a 32B-class dense or 70B MoE.
   - **Ceiling:** 80GB+ (H100 / dual 6000 Ada / Mac Studio M3 Ultra 192GB). Sustains the Qwen3-MoE-A22B target.

2. **The floor is the v0.1 commitment.** Anything above the floor is upside. Local-first is meaningless if the floor is "$10k workstation."

3. **Backbone selection at the floor cannot be A22B.** The 22B-active MoE alone needs ~45GB at int4. The floor backbone for v0.1 is either Qwen3-14B-Thinking (dense, ~14GB at int8, ~7GB at int4, fits with room for kernel/verifiers/cache) or Qwen3-30B-A3B (3B active MoE, ~16GB at int4). Brief 122's A22B target is the v0.2+ ceiling, not the v0.1 floor.

4. **Context ceiling at the floor: 32k tokens reliably, 64k experimentally.** With Qwen3-14B at int4, KV cache for 32k is ~3GB, leaving headroom for the router (200M, ~400MB), the cross-encoder reranker (300M, ~600MB), the eval battery in-flight state, and the verifier subprocess pool. 64k context is achievable but pushes KV cache to ~6GB and starts to crowd the verifier pool.

5. **Mid tier sustains 128k context.** With the 32B dense at int4 and a larger KV cache, 128k is comfortable. This is the recommended *creator-preferred* tier even though the floor is 32k.

6. **Ceiling tier sustains the full A22B at 256k context.** This is the v0.2 target.

7. **Latency budgets at the floor:**

   | Operation | p50 | p99 |
   |---|---|---|
   | Router classification (200M) | 30ms | 80ms |
   | Single ReAct step (14B int4) | 600ms | 1.5s |
   | Tool dispatch (parallel, 4 calls) | 200ms | 500ms |
   | Cross-encoder rerank (300M, 50 docs) | 80ms | 200ms |
   | Symbolic verifier call (avg) | 50ms | 200ms |
   | Constitutional fence check | 20ms | 60ms |
   | LATS expansion + eval (per node) | 800ms | 2s |
   | Full canonical eval battery | 28 min | 35 min |

   These are derived from published Qwen3 inference benchmarks plus the additional kernel overhead per Round 6.

8. **Memory map at the floor (24GB VRAM):**
   - Backbone weights (Qwen3-14B int4): ~7GB
   - KV cache (32k context): ~3GB
   - Router classifier: ~400MB
   - Cross-encoder reranker: ~600MB
   - LoRA adapters (composed base + namespace + creator): ~1.5GB
   - Verifier subprocess pool (CPU, but reserves some VRAM for IPC): ~500MB
   - Activation/scratch: ~3GB
   - Headroom for spike: ~8GB

9. **CPU and RAM floor:** 8-core CPU, 32GB system RAM. The federation graph cache (Brief 101) lives in system RAM not VRAM; 32GB carries a usable per-creator working slice without constant disk fetches.

10. **Disk floor:** 200GB SSD for the v0.1 substrate snapshot (1k seeds + foundation kernel + canonical eval battery + composition history). NVMe strongly preferred — the federation graph fetch latency budget assumes p99 disk seek <100µs.

11. **Mac vs PC parity.** The unified-memory Macs (M3/M4 with 32-64GB) work well at the floor because the backbone, KV cache, and verifier pool can share the same memory pool. PC users with 24GB VRAM but only 16GB system RAM will be tighter on the federation cache.

12. **Battery-life trade-off on laptops.** Running the full kernel at int4 on a 14B model on a laptop GPU consumes ~80W steady. v0.1 ships a "battery mode" that uses the 3B-active MoE and disables LATS / Reflexion / Self-Refine, reducing draw to ~25W. Expressly degrade gracefully.

## Risks identified

- **Floor hardware changes during the year-1 roadmap.** A new generation of consumer GPUs lands every 12-18 months. Mitigation: revisit the floor every 6 months at the council review (Brief 107).
- **int4 quality degradation.** Some Qwen3 layers degrade noticeably at int4. Mitigation: use mixed precision (int8 for attention, int4 for FFN); follow the Qwen3 quantization recipe in Brief 122.
- **Federation cache thrash on 16GB-system-RAM PCs.** Mitigation: explicit warning in the v0.1 install flow that 32GB system RAM is recommended; auto-degrade graph cache size below 32GB.

## Recommendation

**Set the v0.1 floor at 24GB VRAM + 32GB RAM + 200GB NVMe SSD + 8-core CPU. Default backbone Qwen3-14B-Thinking at mixed int4/int8, 32k context window. Battery mode falls back to Qwen3-30B-A3B at int4 with 16k context and disabled tree-search strategies. Document mid (48GB) and ceiling (80GB+) tiers as upside that unlocks larger backbones and longer context. Budget the full canonical eval battery (Brief 134) to complete in ≤35 min on the floor — this is the gating constraint on the battery's size. Revisit floor every 6 months at the council review.**

## Confidence

**4/5.** The numbers are derived from published benchmarks and the Brief 134 battery sizing. The unknowns are: (a) actual int4 quality on the GSPL-specific tasks (needs Round 7 measurement), and (b) federation graph cache hit rates at the floor (needs production telemetry).

## Spec impact

- `gspl-reference/intelligence/hardware-floor.md` — new file documenting the three tiers, the memory map, the latency budget table, and the battery mode.
- `gspl-reference/research/053-local-first-storage-and-sync.md` — cross-reference.
- `gspl-reference/research/108-year-1-roadmap-and-milestones.md` — cross-reference at the v0.1 launch row.
- `gspl-reference/research/122-qwen-code-architecture-teardown.md` — clarify that A22B is v0.2+, not v0.1.

## New inventions

- **INV-563** — *Battery mode degradation envelope.* A signed configuration profile that shrinks backbone, context, and disabled-strategy set in a deterministic, rollback-able way for laptop battery operation. The degradation is itself a signed gseed so creators can audit what was disabled when.

## Open follow-ups

- Exact int4 quality measurement on GSPL tasks (Round 7).
- Whether AMD ROCm and Intel Arc are first-class at v0.1 or v0.2 (defer to Brief 149).
- The exact NVMe seek-latency requirement (the 100µs floor is conservative).

## Sources

1. Brief 053 — Local-first storage and sync.
2. Brief 075 — GSPL without a real GPU.
3. Brief 122 — Qwen Code architecture teardown.
4. Brief 134 — Substrate-native benchmark battery.
5. Qwen team, *Qwen3 Technical Report*, 2024-2025 (inference benchmarks).
6. NVIDIA RTX 4090 / 5090 product specifications.
7. Apple M3/M4 unified-memory architecture documentation.
