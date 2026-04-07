# 111 — Long-context architectures beyond attention: Mamba, RWKV, Titans, Gated DeltaNet, YOCO, Jamba

## Question

Which long-context architecture — pure attention, pure SSM, hybrid, or test-time memory — gives GSPL's reasoning kernel the best cost/quality/grounding-auditability trade-off at 128K–10M token horizons?

## Why it matters (blast radius)

GSPL's knowledge graph is the grounding floor; the knowledge graph will routinely deliver 50K–200K tokens of supporting context for a single grounded query. If attention cost scales quadratically, the per-query budget from Brief 101 blows up immediately at scale. If we pick the wrong alternative architecture, we trade cost for retrieval fidelity and the grounding floor suffers.

## What we know from the spec

- Brief 055 (LLM runtime) is silent on attention alternatives.
- Brief 101 (query budget) assumes a context-token cost axis but does not specify the underlying architecture.
- Round 4's graph (Brief 091) is content-addressable, so we can theoretically assemble any sub-context needed — the question is whether the model can reason over it efficiently once assembled.

## Findings

### 1. Quadratic attention is the default and has known limits

Vanilla transformer attention is O(n²) in sequence length. At 128K context this is expensive but tractable. At 1M it becomes the dominant cost on most hardware. FlashAttention-3, sliding window + global attention (Longformer, BigBird), Ring Attention, and Ring-Flash hybrids push the practical limit but do not change the asymptote. [1]

Empirical finding from "Lost in the Middle" and subsequent work: dense attention at 128K+ degrades significantly in *recall* from the middle of the context, not just in cost. [2] The model technically sees everything but preferentially attends to the start and end. This is a **retrieval quality** problem, not a throughput problem, and it is fatal for the grounding floor.

### 2. State-space models: Mamba, Mamba-2

Mamba (Gu & Dao, 2023) and Mamba-2 (Dao & Gu, 2024) replace attention with selective state-space models (SSMs). Cost is O(n) in sequence length. Long-range retrieval is limited by the fixed-size state, but in practice Mamba-2 at 130M params matches 1.3B attention on language modeling perplexity at 16K+ context. [3][4]

Weakness: SSMs are notably worse at multi-hop retrieval than attention because the state compresses. Benchmarks like RULER and LongBench show Mamba trails pure attention at copy-paste and multi-needle-in-haystack tasks but matches or beats at long-range language modeling. [5][6]

**Implication:** pure SSM is the wrong choice for GSPL. The grounding floor *needs* high-fidelity retrieval from arbitrary positions in the assembled context.

### 3. RWKV-7: attention-free with improving retrieval

RWKV-7 (released 2025) is an RNN variant with linear cost and strong long-context retrieval — closing much of the gap to attention on RULER. [7] Training stability and community momentum are real advantages. Commercial deployment remains niche.

RWKV-7 is a plausible fallback for GSPL's low-resource path (Brief 075) but not the primary kernel.

### 4. Hybrid attention + SSM: Jamba, Griffin, Zamba

Jamba (AI21, 2024) interleaves attention layers and Mamba layers in a 1:7 ratio and achieves dense-attention-like retrieval at SSM-like cost. Griffin (DeepMind, 2024) does a similar interleave with gated linear recurrences. Zamba is an open variant. [8][9]

**This is the dominant pattern.** Empirical retrieval quality matches pure attention on RULER within 2 points while cutting cost by ~60% at 32K and ~75% at 128K. [8]

### 5. Gated DeltaNet and the linear-attention-with-updates family

DeltaNet and its gated variant (2024–2025) use linear attention with learned delta-rule updates, giving dense-attention-grade retrieval at O(n) cost for certain task classes. [10] Published results are still narrow — strong on retrieval, weak on reasoning chains longer than the delta rule can track — but the trajectory is promising.

### 6. Titans: memory at test time

Google's Titans paper (Feb 2025) introduces a three-tier memory: short-term attention, long-term neural memory module updated at test time, and persistent memory. The neural memory learns to store surprising information and retrieves via content similarity. Reported SOTA on needle-in-haystack at 2M+ tokens while beating pure attention at 32K as well. [11]

This is the most architecturally interesting 2025 paper for GSPL because the test-time-updated memory parallels GSPL's substrate concept: the graph is already a test-time-updatable memory. Titans provides the *neural* interface to the same idea.

### 7. YOCO (You Only Cache Once)

Microsoft's YOCO (2024) decodes once through a full transformer to build a KV cache, then switches to a lightweight decoder that only cross-attends to the cached KV. Memory savings of 3–10× at long context. [12]

YOCO is a pure efficiency win with no quality loss, and is orthogonal to everything above.

### 8. Retrieval augmentation as an architectural bypass

A different school of thought: don't push the context window at all. Use retrieval (Brief 120) to assemble small context windows on demand. GSPL is already committed to this via the knowledge graph. But retrieval alone is fragile on long-chain reasoning and multi-hop questions where the model needs to *reason across* the retrieved set. [13]

**The right answer:** retrieval is the floor, long context is the ceiling, and both are needed. This is exactly what Titans-class architectures provide.

### 9. What the frontier labs actually use

As of Q2 2026 (public knowledge): Gemini 2.5 Pro's 1M context uses an undisclosed hybrid (likely Ring Attention + sparse + some cache compression). Claude's extended context uses optimized attention with caching. Qwen3 uses a hybrid window+global attention. DeepSeek-V3 uses MLA (Brief 110) to compress KV. [14]

No frontier lab has publicly committed to pure SSM or pure test-time memory as the primary architecture. The consensus is hybrid.

## Inventions to absorb

None are substrate primitives. Tier W hooks for Brief 127:

- **Hybrid attention + SSM base.** A Jamba- or Griffin-style hybrid is the default context backbone. This gives GSPL dense-attention-grade retrieval at SSM-grade cost.
- **MLA KV compression** (from Brief 110) stacks on top.
- **Test-time memory as substrate binding.** A Titans-style test-time memory module where the "memory" IS the knowledge graph. Writing to memory = signing a new gseed. Reading from memory = graph query. This is the GSPL-native Titans generalization.
- **YOCO for long-decode paths.** Stacks on top of the hybrid.
- **Retrieval-augmented by default, long-context as ceiling.** Brief 120 retrieval is the primary grounding path; long context is for reasoning over the retrieved set.
- **Context is a budget envelope, not a fixed size.** Matches Brief 101's budget discipline.

## Risks identified

- **Hybrid models are harder to fine-tune than pure attention.** Mitigation: LoRA/QLoRA adapters only; no full fine-tune pre-launch.
- **SSM layers degrade at copy-paste tasks.** Mitigation: verbatim citation from graph goes through an attention layer or a dedicated copy head.
- **Titans-style test-time memory is new and unstable.** Mitigation: treat it as v2 research and ship v1 on hybrid + retrieval.
- **Long-context benchmarks are unreliable.** Mitigation: build a substrate-native benchmark (citation-multi-hop from the graph) and measure internally.
- **The 1M-context marketing claim is often stickier than the reality.** Mitigation: publish the actual recall curve and the grounding-audit recall curve separately.

## Recommendation

1. **Default kernel:** hybrid attention + SSM (Jamba / Griffin / Zamba class) with MLA KV compression.
2. **Primary grounding path:** retrieval from the substrate knowledge graph (Brief 120). Context is assembled, not forced into a 1M window.
3. **Long-context ceiling:** 128K as the shipping default; the architecture supports 1M+ but the envelope budget caps it at 128K unless the user has a Professional/Studio subscription (Brief 106).
4. **v2 research direction:** Titans-class test-time memory where the memory IS the graph. Publish as an open research note after launch.
5. **Substrate-native long-context benchmark.** A "grounded multi-hop" benchmark built from the knowledge graph becomes the internal quality bar. Publish the recall curve as a transparency artifact.

These feed Brief 127 (memory + context architecture).

## Confidence

**4/5.** The hybrid-attention-plus-SSM consensus is well-published. The Titans-as-substrate-binding idea is novel (GSPL-specific) and is 3.5/5 — the analogy is sound but no public result yet proves it works in production. The retrieval-as-floor commitment is 5/5 because GSPL has the graph.

## Spec impact

- Brief 055 needs the hybrid kernel choice added.
- Brief 101 needs the context-budget envelope extended with recall-curve targets.
- Brief 127 owns the final architecture.

## Open follow-ups

- Specific hybrid model at launch (Jamba-class vs Griffin-class vs a 2026 successor).
- Substrate-native benchmark construction details.
- Titans-as-substrate experiment timeline.

## Sources

1. Dao, "FlashAttention-3," 2024.
2. Liu et al., "Lost in the Middle: How Language Models Use Long Contexts," 2023. arXiv:2307.03172.
3. Gu & Dao, "Mamba: Linear-Time Sequence Modeling with Selective State Spaces," 2023. arXiv:2312.00752.
4. Dao & Gu, "Mamba-2," 2024. arXiv:2405.21060.
5. Hsieh et al., "RULER: What's the Real Context Size of Your Long-Context Language Models?" 2024. arXiv:2404.06654.
6. Bai et al., "LongBench," 2023.
7. BlinkDL, "RWKV-7," 2025.
8. Lieber et al., "Jamba: A Hybrid Transformer-Mamba Language Model," AI21, 2024. arXiv:2403.19887.
9. De et al., "Griffin," DeepMind, 2024. arXiv:2402.19427.
10. Yang et al., "Gated Delta Networks," 2024.
11. Behrouz et al., "Titans: Learning to Memorize at Test Time," Google, 2025. arXiv:2501.00663.
12. Sun et al., "You Only Cache Once: Decoder-Decoder Architectures for Language Models," Microsoft, 2024. arXiv:2405.05254.
13. Lewis et al., "Retrieval-Augmented Generation," 2020.
14. Various technical reports, 2024–2026.
