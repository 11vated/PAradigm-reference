# 112 — Diffusion and non-autoregressive language models: LLaDA, Mercury, SEDD, block-diffusion

## Question

What does diffusion-based text generation buy GSPL that autoregressive generation cannot, and where in the agent should GSPL use it?

## Why it matters (blast radius)

Diffusion LMs parallel-decode hundreds of tokens per forward pass, giving 5–20× latency wins on code and structured output. If GSPL's studio ships a conversational AR model only, the edit-mode experience (where latency is felt most) will lose to Mercury-class competitors on feel alone. Worse, autoregressive generation is *bad* at editing: every local change is an expensive prefix-plus-regenerate. Diffusion edits are local by construction.

## What we know from the spec

- Brief 049 (compose and conversational UX) assumes AR generation.
- Brief 048 (studio IDE architecture) assumes edit operations are full-regen.
- Brief 022 (image engine) is diffusion-aware but text generation is not.

## Findings

### 1. The autoregressive monopoly is ending

From GPT-1 through Llama 3, text generation has been autoregressive: one token at a time, left-to-right, with a KV cache. Every major open model released 2020–2024 is AR. Starting in 2024, diffusion and non-AR approaches began producing competitive results on coding and structured output, with LLaDA (2025) matching Llama 3 8B perplexity on standard benchmarks at a fraction of per-token decode cost. [1]

### 2. SEDD: score entropy discrete diffusion

Lou et al. (2024) introduced SEDD, a principled discrete diffusion recipe using score entropy loss. SEDD matches GPT-2 quality with 32× fewer network evaluations, and unlike earlier discrete diffusion attempts, it extends cleanly to larger scales. [2]

### 3. LLaDA: large-scale diffusion LM

LLaDA (Large Language Diffusion Model, 2025) scaled masked diffusion to 8B parameters and showed competitive performance with Llama 3 8B on standard benchmarks. LLaDA trains with a variable-mask-ratio objective: at training time a random fraction of tokens is masked, and the model learns to denoise. At inference, it starts from a fully-masked sequence and iteratively unmasks in parallel. [1]

Key practical finding: LLaDA's quality-vs-steps curve saturates around 16–32 steps for most tasks, giving 20–40× parallelism over AR at target quality.

### 4. Mercury Coder (Inception Labs): diffusion-native code generation

Mercury Coder (2025) is the first commercially competitive diffusion code model. Published benchmarks show ~5× throughput at HumanEval parity vs Llama-class AR baselines. [3] The killer feature is editability: because diffusion updates happen in parallel across positions, edits to one region don't force regeneration of downstream tokens. This is exactly the interaction model a code studio needs.

### 5. Block diffusion

MDLM and block-diffusion variants hybridize: the sequence is chunked into blocks; diffusion runs within a block, AR runs between blocks. This gives the context-coherence of AR with the parallelism of diffusion. [4] It is the likeliest shipping compromise for most production use cases.

### 6. Where diffusion wins, where it loses

**Wins:**
- Code generation with edits (Mercury's sweet spot)
- Structured output (JSON, tool-call grammars, configs)
- Parallel decoding latency
- Infilling and gap-filling (the masked objective is literally this)
- Constrained decoding (grammar constraints integrate naturally with the unmask step)

**Loses:**
- Open-ended creative writing (AR is still better at narrative coherence)
- Reasoning traces (AR's left-to-right causality matches deliberation)
- Very-long-context generation (diffusion memory is still weaker)
- Fine-grained sampling control (temperature/top-p mean less in diffusion)

### 7. Diffusion + grounding

An under-appreciated diffusion property: the denoising process can be *guided* at every step by an external classifier or constraint. For image diffusion this is classifier-free guidance. For text diffusion, this means the GSPL knowledge graph can act as a guidance function during decoding — every step pulls the output distribution toward graph-grounded answers.

AR models can only do post-hoc grounding (generate, then cite). Diffusion models can do *co-generative* grounding: the tokens emerge already consistent with the graph. This is a substantial grounding-floor advantage no AR-only system can match. [5]

### 8. Diffusion and the substrate modifier surface

Brief 023's modifier surface — the differentiable knobs creators pull on — is architecturally a constraint. Diffusion generation under constraint is natural: each modifier is a guidance term added to the score function. AR generation under the same constraint has to fall back on rejection sampling or controlled decoding, both of which are worse.

This is the GSPL-specific observation: **diffusion is the natural generation modality for a substrate with signed, differentiable modifiers.** AR is the generation modality for a "just the prompt" world. GSPL is not that world.

## Inventions to absorb

Tier W hooks:

- **Dual generation modality.** The reasoning kernel is AR (Brief 109). The code and structured-output generation is diffusion. The decision is task-namespace-conditional (matching Brief 110's MoE routing pattern).
- **Graph-guided denoising.** Every unmask step during diffusion decoding is guided by a graph-consistency score. This is GSPL's native "grounding floor during generation" technique.
- **Modifier-surface-as-guidance.** Brief 023's differentiable modifiers attach naturally to the diffusion score function; AR generation cannot do this as cleanly.
- **Block-diffusion for long outputs.** Blocks give coherence; intra-block diffusion gives parallelism.
- **Editability as first-class interaction.** The studio's edit mode (Brief 048) uses diffusion update in place of re-roll; a creator touching a sprite's face does not regenerate the rest of the sprite.

## Risks identified

- **Diffusion LMs are immature compared to AR.** Mitigation: AR remains the default for reasoning and creative; diffusion is scoped to code, structured output, and edit-mode.
- **Open-weight diffusion LMs are behind closed (Mercury).** Mitigation: train a minimal open diffusion code model post-launch, or license Mercury-class capability.
- **Diffusion inference requires different runtime than AR.** Mitigation: Brief 055 runtime supports two model types; this is feasible.
- **Graph-guided decoding has no published recipe at scale yet.** Mitigation: GSPL publishes the recipe as a research note post-launch; the v1 kernel uses post-hoc grounding as fallback.
- **Users do not know what diffusion is and expect AR behavior.** Mitigation: the UX hides the distinction; the difference is felt only as latency wins.

## Recommendation

1. **Dual generation modalities in the kernel.** AR (Brief 109's reasoning-trained model) for deliberation and creative writing; diffusion (Mercury-class or open successor) for code, structured output, and edit-mode.
2. **Namespace-conditional modality selection.** Code namespaces → diffusion. Chat/creative → AR. Mixed → AR primary, diffusion for code blocks.
3. **Graph-guided denoising** is the GSPL-native technique. Publish as an open research note after launch.
4. **Modifier surface binds to the diffusion score function** naturally. Brief 128 owns this design.
5. **Block-diffusion** for any output longer than 2K tokens where structure matters (code files, configs, specs).
6. **v1 ships with diffusion limited to code and edit mode.** Full dual-modality across all tasks is v2.

Feeds Brief 128 (tool-use and modifier-surface intelligence) and Brief 126 (reasoning kernel).

## Confidence

**3.5/5.** Diffusion LM architecture findings are strong; the GSPL-specific applications (graph-guided denoising, modifier-as-guidance) are novel and lightly tested. The productization risk is real. If we commit to AR-only for v1 and diffusion for v1.5, the confidence rises to 4/5.

## Spec impact

- Brief 048 (studio IDE) needs edit-mode diffusion integration.
- Brief 055 (LLM runtime) needs dual-modality runtime support.
- Brief 049 (compose UX) needs the namespace-conditional modality decision surface.

## Open follow-ups

- Whether to license Mercury-class capability or wait for an open-weight diffusion LM matching it.
- Graph-guided denoising experimental timeline.
- Block-diffusion block size vs reasoning coherence trade-off.

## Sources

1. Nie et al., "LLaDA: Large Language Diffusion Model," 2025. arXiv:2502.09992.
2. Lou et al., "Score Entropy Discrete Diffusion," ICML 2024. arXiv:2310.16834.
3. Inception Labs, "Mercury Coder," 2025.
4. Arriola et al., "Block Diffusion: Interpolating Between Autoregressive and Diffusion Language Models," 2025.
5. Li et al., "Diffusion-LM Improves Controllable Text Generation," 2022.
