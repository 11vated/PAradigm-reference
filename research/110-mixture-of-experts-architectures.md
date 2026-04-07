# 110 — Mixture of Experts: Mixtral, DeepSeek-V3, Qwen3-MoE, and the sparsity frontier

## Question

What architectural techniques from the 2023–2026 MoE wave must GSPL absorb — at the base-model layer, at the agent-orchestration layer, or both?

## Why it matters (blast radius)

MoE is the dominant architectural pattern for capable open-weight models at 2026 inference cost. Mixtral, DeepSeek-V3, Qwen3-MoE, and the Llama 4 Scout/Maverick family all ship with active-parameter counts 3–8× smaller than their total parameter counts, giving near-dense quality at sparse cost. If GSPL's base model choice ignores MoE, inference cost at 10K+ users (Brief 101) blows up by 3–8×.

Beyond the base model, there's a second-order question: should GSPL's agent orchestration itself be MoE-shaped? A routing layer that dispatches chemistry queries to a chem expert, culture queries to a culture expert, code queries to a code expert, can amortize context costs and preserve specialization without a 400B dense model.

## What we know from the spec

- Brief 055 (LLM runtime and BYO models) commits to open-weight support but is silent on MoE routing overhead.
- Brief 101 (query budget) assumes dense-model cost curves; MoE changes those curves materially.
- Brief 091 (federated knowledge graph) has an implicit routing shape — namespace-keyed queries — that parallels MoE expert routing.

## Findings

### 1. MoE as a quality-per-FLOP win

Mixtral 8x7B showed an 8-expert top-2 routing design at 47B total / 13B active parameters matching Llama 2 70B dense quality at ~4× lower inference FLOPs. [1] DeepSeek-V2 introduced fine-grained experts (64 routed + 2 shared out of 160) with Multi-head Latent Attention, pushing the ratio further: 236B total / 21B active. DeepSeek-V3 extended this to 671B total / 37B active with 256 routed + 1 shared expert, and released the full training recipe. [2][3]

Qwen3-MoE (A3B and A22B) ships 30B/3B and 235B/22B active-parameter variants with a similar fine-grained-expert + shared-expert pattern. [4] Llama 4 Scout (109B/17B) and Maverick (400B/17B) shipped in April 2025 with 16-expert and 128-expert configurations respectively. [5]

**Meta-finding:** the 2024–2026 frontier shifted from "big dense expert" to "hundreds of small fine-grained experts + 1–2 always-on shared experts." Fine-grained expert counts give better specialization at constant active-parameter budget.

### 2. Routing discipline

Every MoE design has to solve: which token goes to which expert, and how do we prevent experts from collapsing to the mean?

- **Top-k routing:** each token is routed to k experts (k=2 in Mixtral, k=8 in DeepSeek-V3 with finer experts). The top-k trade-off is capacity-vs-noise: higher k means more capacity per token but less expert specialization. [1][2][3]
- **Load-balancing auxiliary losses:** auxiliary loss terms that penalize expert underuse, typically hurting quality slightly. DeepSeek-V3 introduced **auxiliary-loss-free load balancing** using a per-expert bias term updated online, recovering the quality cost. [3]
- **Expert parallelism vs tensor parallelism:** expert parallelism places each expert on a separate device; tensor parallelism shards each expert. At 256 experts and 8 GPUs, expert parallelism dominates. [3]
- **Router temperature and noise:** training uses noisy routing to prevent lock-in; inference uses deterministic routing for reproducibility (GSPL determinism contract from Brief 020 requires this).

### 3. Fine-grained vs coarse-grained experts

The published evidence favors fine-grained experts (256 experts of smaller size) over coarse experts (8 experts of larger size) for constant active-parameter budget. [3][4] Specialization is more measurable: you can probe experts and find reliable per-domain firing patterns. DeepSeek's paper shows experts that specialize in code, math, Chinese, English, and specific syntactic patterns. [3]

**Implication for GSPL:** an MoE base model with fine-grained experts will naturally specialize along namespace boundaries when fine-tuned on substrate-native tasks. The namespace becomes a soft expert label.

### 4. Multi-head Latent Attention (MLA)

DeepSeek-V2 introduced MLA: a low-rank compression of the KV cache that cuts KV memory by 93% at minimal quality cost. [2][3] This is not MoE per se but ships with the DeepSeek MoE line and is load-bearing for the long-context claims.

MLA matters for GSPL because the reasoning-kernel budget from Brief 109 depends on KV-cache cost scaling linearly in context. A 93% KV reduction turns a 32K context from "expensive" into "cheap."

### 5. Shared expert isolation

DeepSeek-V2 / V3 ships with 1–2 **shared experts** always active alongside the routed top-k. The insight: generic capabilities (basic grammar, factual recall, common sense) should not have to be duplicated across routed experts. Isolating them into always-on experts frees routed experts to specialize further. [2][3]

This pattern applies directly to GSPL orchestration: a shared "grounding floor" reasoning kernel + routed "namespace experts."

### 6. Training stability

MoE training is famously unstable — expert collapse, router dead-ends, loss spikes. DeepSeek-V3's paper documents the stabilization tricks: auxiliary-loss-free balancing, FP8 mixed precision with tile-level scaling, DualPipe pipeline parallelism to hide communication. [3] These are expensive engineering pieces a solo founder cannot replicate.

**Implication:** GSPL must consume MoE models, not train them from scratch. Fine-tuning a released MoE model on substrate tasks is feasible; pretraining one is not.

### 7. MoE at inference: routing overhead vs quality gain

MoE routing adds latency per token (~5–15% overhead vs dense at same active-parameter count). [1][3] But for equivalent quality, MoE is 3–5× faster because the dense baseline is that much bigger. At GSPL's scale, the latency math works out only if we host the MoE model on hardware with enough memory to hold all experts (since routing dynamically selects).

For creator laptops (Brief 075) this is a problem: DeepSeek-V3 needs ~450GB to hold all experts. The published workaround is **expert offloading**: keep inactive experts on SSD, stream in on demand. This adds 200–500ms latency but works on 64GB consumer hardware. [6]

### 8. The agent-orchestration MoE analogy

Here is the GSPL-specific observation. An agent that dispatches "chemistry query → chem expert subagent" is architecturally a top-1 MoE router. The same load-balancing questions apply: how to prevent expert specialization collapse, how to handle queries that span experts (multi-expert routing), how to share common reasoning across experts (shared agent = grounding floor).

**This is an under-exploited lever.** Frameworks like AutoGen and CrewAI treat multi-agent orchestration as an *engineering* problem. MoE literature treats it as a *learning* problem. The latter is more principled.

GSPL's agent orchestration layer (Brief 126) should adopt MoE discipline: a router trained on namespace signals, fine-grained expert agents, shared grounding floor, load-balancing via auxiliary signals (Brief 101 cost accounting doubles as auxiliary signal).

## Inventions to absorb

None are new substrate primitives. Tier W hooks:

- **MoE base model as default backbone.** Qwen3-MoE-235B-A22B or DeepSeek-V3 variant.
- **Namespace-keyed expert routing at orchestration layer.** The agent itself is an MoE — router + fine-grained expert subagents + shared grounding floor.
- **MLA-compressed context buffer** for the reasoning kernel.
- **Auxiliary-loss-free load balancing** applied to agent orchestration: cost accounting from Brief 101 provides the balancing signal.
- **Shared-expert isolation:** the grounding floor (INV-357) is the shared expert; domain-specific reasoning kernels are routed.
- **Expert offloading for on-device.** SSD-streamed experts with sub-500ms swap budgets for creator laptops.

## Risks identified

- **MoE models need hardware the typical creator laptop lacks.** Mitigation: expert offloading + tiered-cloud fallback from Brief 101 degradation ladder.
- **Router decisions are hard to explain.** Mitigation: router decisions are themselves signed gseeds in a lineage-only namespace (`router-decision://`), matching the open-trace commitment from Brief 109.
- **MoE fine-tuning is more fragile than dense.** Mitigation: use LoRA/QLoRA adapters per expert rather than full fine-tune; substrate fine-tuning becomes per-expert delta.
- **Expert drift over time.** Mitigation: periodic rebalancing against the substrate evaluation grid (Brief 096) and cost accounting (Brief 101).
- **Licensing on open-weight MoE models.** Mitigation: Brief 076 (open-weight licensing resilience) already covers this.

## Recommendation

1. **Default backbone:** Qwen3-MoE-A22B (or successor) with DeepSeek-V3 as alternate BYO path.
2. **Adopt MLA** in the context buffer for the reasoning kernel (Brief 109 budget feasibility depends on it).
3. **Adopt MoE discipline at the agent orchestration layer.** The agent is a router + fine-grained expert agents + shared grounding floor. Routing is trained on namespace signals; load-balancing auxiliary signal is cost accounting from Brief 101.
4. **Expert offloading** is the default strategy for on-device creator hardware; cloud fallback kicks in when the swap latency budget is exceeded.
5. **Router decisions are signed gseeds.** Every routing decision is auditable, forkable, and reusable.

These choices feed directly into Brief 126 (reasoning kernel) and Brief 127 (memory + context).

## Confidence

**4/5.** MoE architectural findings are mature and well-published. The application of MoE discipline to agent orchestration is novel and 3.5/5 — the analogy is principled but no one has published results proving it beats engineered multi-agent systems yet. GSPL would be publishing the first rigorous result on this if it ships.

## Spec impact

- Brief 055 needs MoE routing overhead added to the cost model.
- Brief 075 (GSPL without a real GPU) needs the expert-offloading escape hatch.
- Brief 101 needs the MoE auxiliary-balancing signal added to cost accounting.
- Defer to Brief 126 for the full architectural commitment.

## Open follow-ups

- Final base model choice pending Q2 2026 open-weight landscape.
- Router training data (substrate-native namespaced queries).
- Expert-offloading latency budget vs creator laptop hardware variance.
- Whether GSPL publishes the first "agent-as-MoE" result as a research note.

## Sources

1. Mistral AI, "Mixtral of Experts," 2024. arXiv:2401.04088.
2. DeepSeek-AI, "DeepSeek-V2: A Strong, Economical, and Efficient Mixture-of-Experts Language Model," 2024. arXiv:2405.04434.
3. DeepSeek-AI, "DeepSeek-V3 Technical Report," Dec 2024. arXiv:2412.19437.
4. Qwen Team, "Qwen3 Technical Report," 2025.
5. Meta AI, "Llama 4 technical blog," Apr 2025.
6. Eliseev & Mazur, "Fast Inference of Mixture-of-Experts Language Models with Offloading," 2023. arXiv:2312.17238.
