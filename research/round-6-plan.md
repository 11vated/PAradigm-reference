# Round 6 — The Intelligence Layer: Making GSPL Unsurpassable (charter)

## Directive

Rounds 1–5 built the substrate, filled it with the stuff of the world, and made it shippable. Round 6 answers a single binding question:

> **What must GSPL's intelligence layer — its reasoning kernel, memory architecture, tool-use discipline, self-improvement loop, and agent scaffolding — be, so that no frontier AI platform (Claude, Gemini, GPT, Qwen, DeepSeek, Llama, Mistral, xAI Grok) and no code-generation system (Claude Code, Qwen Code, Gemini CLI, Cursor, Aider, Cline, Continue, Copilot Workspace, Devin, SWE-agent) has a technique, framework, or architectural primitive that GSPL does not either match, absorb as a special case, or structurally surpass by virtue of its substrate-native grounding floor?**

Round 6 is the **intelligence round**. Architecture is locked at the substrate layer. The shippable foundation is planned. Round 6 asks: given all of that, what makes GSPL's agent **smarter, more grounded, more self-improving, more honest, and more capable** than anything creators can use elsewhere?

## What Round 6 must deliver

Round 6 delivers four interlocking things:

1. **Frontier teardown** — A source-level analysis of how current frontier models actually work: test-time compute scaling (o1/o3/R1), Mixture of Experts (Mixtral/DeepSeek-V3/Qwen3-MoE), long-context architectures (Mamba/RWKV/Titans/Gated DeltaNet/YOCO), diffusion language models (LLaDA/Mercury/SEDD), constitutional training (Claude's RLAIF), and neurosymbolic + world-model integration (Dreamer/Genie/V-JEPA). Not marketing — actual architectural primitives at the paper and implementation level.

2. **Agent framework comparison** — Every published planning framework (ReAct, Reflexion, Tree of Thoughts, Graph of Thoughts, LATS, Self-Consistency, Chain-of-Verification), every memory architecture (MemGPT, A-Mem, cognitive architectures), every tool-use discipline (Claude Computer Use, Gemini function calling, Qwen Agent, OpenAI Assistants API), every multi-agent orchestration pattern (AutoGen, CrewAI, LangGraph, AgentVerse, MetaGPT), every self-improvement loop (STaR, Quiet-STaR, SPIN, self-play, constitutional self-critique), and every RAG evolution (GraphRAG, HyDE, Self-RAG, CRAG, RAPTOR, Contextual Retrieval). With named strengths, named weaknesses, and named assimilation pathways into GSPL.

3. **Code-platform source analysis** — Teardown of every code-generation system that matters: Claude Code, Qwen Code, Gemini Code Assist / Gemini CLI, Cursor, Aider, Cline, Continue, GitHub Copilot Workspace, Devin, SWE-agent, OpenHands. How each one does planning, context management, tool dispatch, code application, test validation, and failure recovery. What each does better than the others. What none of them do. What GSPL can do that none of them can because of the substrate-native knowledge graph.

4. **GSPL intelligence layer design** — A concrete, coherent intelligence architecture for GSPL that: (a) uses the Round 4 knowledge graph as its grounding floor; (b) absorbs every useful technique from the teardown as a first-class primitive; (c) adds the GSPL-native primitives that no other platform has because no other platform has a signed, lineage-bearing, federated substrate underneath the agent; (d) remains honest about what it refuses to do; (e) compounds over time through self-improvement loops that are themselves substrate-native signed gseeds.

## Round 6 is research-first, not design-first

Round 4 was design-first because the substrate content had to be invented. Round 5 was operationalization-first because the architecture was locked. Round 6 is **research-first** because the frontier moves weekly and GSPL cannot ship an intelligence layer that is already six months obsolete at launch. Every brief in Tier T and Tier V is a source-level read of the strongest publicly-known work as of Q2 2026. Every brief in Tier U is a comparative analysis. Only Tier W converts research into GSPL design.

## Brief inventory

### Tier T — Frontier model architecture teardown (6 briefs)

- **109 — Test-time compute scaling.** OpenAI o1 / o3 reasoning traces, DeepSeek-R1's reinforcement-learning-from-verifiable-rewards recipe, Qwen QwQ, process reward models, speculative / tree / beam search over reasoning, budget-forced reasoning, the "thinking tokens are a free lunch" thesis, when to spend compute and when to cache. What GSPL's reasoning kernel must absorb.

- **110 — Mixture of Experts architectures.** Switch Transformer, GShard, Mixtral 8x7B / 8x22B, DeepSeek-V2 / V3 MLA + fine-grained experts + shared-expert isolation, Qwen3-MoE, DBRX, Arctic, JetMoE. Routing discipline, load-balancing auxiliary losses, expert specialization evidence, inference cost curves, training stability. Whether GSPL's agent should itself be MoE-shaped at orchestration layer.

- **111 — Long-context architectures beyond attention.** Mamba / Mamba-2 state-space models, RWKV-7, Gated DeltaNet, Titans (Google's memory-at-test-time paper), YOCO (You Only Cache Once), Jamba hybrid, Griffin, Infini-attention, hyena, Hyena-DNA. Cost curves at 1M+ tokens, retrieval accuracy, extrapolation behavior, loss of in-context-learning as we leave pure attention. What GSPL needs at the context layer.

- **112 — Diffusion and non-autoregressive language models.** LLaDA (Large Language Diffusion model), Mercury Coder, SEDD (Score Entropy Discrete Diffusion), block-diffusion, MDLM, consistency LMs, parallel decoding. Latency characteristics, quality parity with AR, editability (the killer feature for code-gen), what GSPL's code generation should inherit.

- **113 — Constitutional AI, RLAIF, DPO, IPO, KTO, and alignment training recipes.** Anthropic's Constitutional AI, Claude's character training, RLAIF, Direct Preference Optimization, Identity Preference Optimization, Kahneman-Tversky Optimization, Rejection-sampling Fine-Tuning, Iterative DPO, online DPO, process reward models vs outcome reward models. What alignment recipe keeps GSPL's agent honest at the grounding floor.

- **114 — Neurosymbolic integration and world models.** DeepMind Genie / Genie-2, OpenAI Sora, V-JEPA, Dreamer-V3, DreamerV4 trajectories, AlphaProof / AlphaGeometry neurosymbolic pattern, LeanDojo, miniF2F, Logic-LM, LLM+Solver hybrids, symbolic distillation. Which parts of the substrate should be symbolic, which should be neural, and where the binding happens.

### Tier U — Reasoning and agent framework comparison (6 briefs)

- **115 — Planning frameworks compared.** ReAct, Reflexion, Self-Refine, Tree of Thoughts, Graph of Thoughts, Skeleton-of-Thought, Algorithm of Thoughts, LATS (Language Agent Tree Search), AlphaCode search, Chain-of-Verification, Self-Consistency, Plan-and-Solve, Least-to-Most. Ranked by task type (reasoning / code / creative / grounded). Which GSPL absorbs as first-class planner primitives.

- **116 — Memory architectures.** MemGPT, A-Mem, Sparrow-style memory, Generative Agents episodic memory, Letta, mem0, zep, cognitive-architecture inspired (ACT-R, SOAR), retrieval-augmented memory, hierarchical summarization, sleep-compaction, Titans memory-as-test-time. What GSPL's memory system must look like given that its substrate already is a content-addressed graph.

- **117 — Tool-use and action-space design.** Claude Computer Use, Anthropic MCP, OpenAI Assistants v2 tools, Gemini function calling, Qwen Agent, Toolformer, Gorilla, ToolBench, ReAct tool loop, HuggingGPT, function-calling fine-tune recipes, structured output grammars (JSON schema, regex, Lark grammars, xgrammar, Outlines, Guidance). The action space GSPL's agent should offer and how each action is itself a signed gseed.

- **118 — Multi-agent orchestration.** AutoGen, CrewAI, LangGraph, MetaGPT, AgentVerse, ChatDev, Camel, SWE-agent's agent-computer interface, Devin's multi-agent loops, OpenAI Swarm, Anthropic's agent patterns doc. When multiple agents help, when they hurt, how GSPL uses subagents without losing the grounding floor.

- **119 — Self-improvement loops.** STaR (Self-Taught Reasoner), Quiet-STaR, V-STaR, SPIN (Self-Play Fine-Tuning), rStar-Math, self-rewarding language models, iterative DPO, self-consistency-as-reward, weak-to-strong generalization, debate-as-training-signal. The safe self-improvement loop GSPL runs on its own federation data.

- **120 — Retrieval-augmented generation evolution.** Naive RAG, HyDE, Self-RAG, Corrective RAG (CRAG), RAPTOR hierarchical summary trees, GraphRAG, Contextual Retrieval (Anthropic), Late Chunking, ColBERT / ColBERTv2, DRAGON, Matryoshka embeddings, reranking with cross-encoders, RAG-fusion, fusion-in-decoder. How GSPL's federation graph makes all of these a special case of substrate-native retrieval.

### Tier V — Code generation platform source analysis (5 briefs)

- **121 — Claude Code architecture teardown.** Published system design, slash-commands, skills, subagent model, tool discipline, plan mode, MCP integration, hooks, settings hierarchy, session management. What Claude Code does that GSPL's studio must match or exceed. What Claude Code deliberately does not do that GSPL can safely do because the substrate grounds it.

- **122 — Qwen Code architecture teardown.** Qwen-Agent, Qwen-Code, Qwen3-Coder, the Qwen Agent loop, tool-call format, context packing strategy, multi-file edit handling, agentic RL training recipe (Qwen-Agent-RL), published benchmarks. Techniques GSPL should absorb.

- **123 — Gemini Code Assist and Gemini CLI teardown.** Gemini CLI's reasoning loop, 1M+ context strategy, tool integration, Google Cloud integration patterns, the Code Assist Enterprise feature set, AIDA, PaLM-Coder heritage, the shift to Gemini 2.5 Pro's deep-think mode. What the 1M-context advantage really buys in practice.

- **124 — Cursor, Aider, Cline, Continue, Roo Code, OpenHands teardown.** Cursor's composer + tab-complete + agent mode, Aider's repo-map + git-commit discipline + edit formats (whole/diff/udiff/architect), Cline's plan-and-act separation, Continue's index-and-retrieve, Roo Code's forked refinements, OpenHands' sandboxed runtime. The best single idea from each.

- **125 — Copilot Workspace, Devin, SWE-agent, Augment, Cognition-class autonomous systems.** Task-level vs step-level autonomy, benchmark performance on SWE-bench Verified, how each handles long-horizon tasks, how each handles failure recovery, the agent-computer interface (ACI) insight from SWE-agent, GitHub's task-centric Copilot Workspace, how Devin packages everything into a tracked task. The autonomy ladder GSPL climbs.

### Tier W — GSPL intelligence layer design (6 briefs)

- **126 — The GSPL reasoning kernel.** Ties Tier T and Tier U into a single reasoning architecture with: a deliberation loop (o1/R1-style) that cites the knowledge graph at every step, a critic ensemble trained on substrate-native contradictions, a process reward model grounded in graph truth, a test-time compute budget that honors the query envelope from Brief 101, and a refusal discipline that is itself a first-class reasoning move.

- **127 — GSPL memory and context architecture.** Working memory, episodic memory, semantic memory, procedural memory — each mapped onto substrate-native gseed namespaces. Context packing that uses the composition graph as the retrieval spine. Hybrid long-context (attention + SSM + test-time memory) with a budget the grounding floor can audit.

- **128 — GSPL tool-use and modifier-surface intelligence.** Every tool call is a signed gseed. Every tool is described by a schema that is itself a gseed. Every error is a lineage-tracked recovery opportunity. The modifier surface from Brief 023 becomes the substrate-native action space — more expressive than any function-calling API because it carries differentiable modifier semantics rather than opaque JSON.

- **129 — GSPL self-improvement and evolution loop.** Self-play on substrate-native tasks, novelty-search over the knowledge graph, Reflexion with signed critique gseeds, STaR-style bootstrapping where every successful reasoning trace becomes a signed training gseed, weak-to-strong bootstrapping inside the consultancy network, and the constitutional safety fence that prevents self-improvement from drifting.

- **130 — GSPL neurosymbolic substrate binding.** Chemistry equations, physics constants, math axioms, cultural attributions, and power-system mechanics are already symbolic in the substrate. The neural reasoning kernel calls the symbolic substrate as a tool rather than hallucinating physics. Binding protocol, round-trip verifier, symbolic-confidence score propagation into natural-language response.

- **131 — GSPL as a differentiable reasoning substrate.** The culminating brief. GSPL is not an LLM with a RAG bolted on. GSPL is a reasoning substrate where every reasoning step is signed, lineage-bearing, and composable with every other reasoning step across every creator in the federation. The substrate-native moat: techniques the competition cannot copy without first building a signed substrate underneath.

**23 briefs + 1 synthesis = 24 total for Round 6.**

## Invention numbering

Round 6 invention numbers start at **INV-482** (continuing from Round 5's INV-481).

## How Round 6 composes

```
        FRONTIER TEARDOWN (T)            AGENT FRAMEWORKS (U)
        109  110  111  112  113  114     115  116  117  118  119  120
              │                                  │
              └──────────────┬───────────────────┘
                             ↓
              CODE-PLATFORM SOURCE ANALYSIS (V)
              121  122  123  124  125
                             │
                             ↓
            GSPL INTELLIGENCE LAYER DESIGN (W)
            126 (reasoning kernel)
            127 (memory + context)
            128 (tool-use + modifier-surface)
            129 (self-improvement loop)
            130 (neurosymbolic binding)
            131 (differentiable reasoning substrate)
                             │
                             ↓
                   ROUND 6 SYNTHESIS
```

Tier T tells us what the frontier is. Tier U tells us what the research community has discovered about using frontier models well. Tier V tells us how to ship a studio that creators actually want. Tier W converts all of that into the GSPL intelligence architecture — tethered at every step to the Round 4 substrate and the Round 5 operational layer.

## Round 6 non-goals (explicitly)

- **No new substrate primitives.** If Tier W discovers the need for a new `xyz://` scheme, it goes into Round 7 as a proposal, not into Round 6.
- **No new constitutional commitments.** Honesty, grounding, non-hallucination, and credit lineage from Round 4 are load-bearing and must be preserved by any Tier W design.
- **No architectural changes to locked Round 4 systems.** The knowledge graph, the edge ontology, the refusal envelope, and the canonical seed armory are untouchable. Round 6 plugs into them.
- **No copying of model weights, proprietary prompts, or closed training data.** Tier V is source-level reading where source is public and interface-level reading where it is not. We absorb techniques, not IP.
- **No marketing claims.** A claim is either cited to a paper, a published blog post, a public repo, a public benchmark, or it is marked "unknown / private."

## Round 6 confidence target

**4/5 per brief minimum. 4.5/5 for Round 6 as a whole.**

The frontier will continue to move after Round 6 ships. The design must remain strong under that motion by being **absorptive-by-architecture**: any new frontier technique should be a special case of GSPL's reasoning substrate rather than a retrofit. The confidence rating should measure the absorptive architecture, not the specific techniques absorbed.

## How Round 6 ends

Round 6 ends when:

1. All 23 briefs are written and cross-referenced.
2. The Round 6 synthesis captures the intelligence-layer posture as a single readable artifact with the full INV-482..NNN catalog.
3. The README is updated to reflect 131 total briefs and the Round 6 set.
4. Every named frontier technique is either absorbed as a GSPL primitive, noted as already-covered by substrate architecture, or explicitly refused with a constitutional reason.
5. The culminating Brief 131 states — in plain, defensible language — why GSPL's intelligence layer is unsurpassable by construction, not by assertion.

After Round 6, GSPL is not merely a ship-ready foundation with world-grade content. GSPL is **a reasoning substrate whose agent cannot be caught up to by any frontier model that does not also build a signed, lineage-bearing, federated substrate underneath it** — because the moat is not in the weights, it is in the graph.
