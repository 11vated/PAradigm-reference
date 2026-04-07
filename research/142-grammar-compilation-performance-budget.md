# 142 — Grammar compilation performance budget

## Question

What is the startup-time performance budget for compiling the xgrammar tool-call grammars (Brief 128, INV-518) on the v0.1 floor hardware, and is per-tool grammar precompilation feasible at scale?

## Why it matters (blast radius)

Brief 128 specifies that every tool call passes through an xgrammar-class structured-output grammar enforced at decode time. Grammar enforcement is what makes tool calls *typed*-by-construction (the second of the seven axes). If grammar compilation takes too long at startup, kernel boot is unacceptable. If grammars cannot be precompiled and cached, every session pays the compilation cost at first call. Either failure mode degrades the typed-axis claim and slows the user-visible loop.

## What we know from the spec

- Brief 128 lists xgrammar grammars as primitive infrastructure for the action-space layer.
- The primitive tool catalog has ~10 tools at v0.1; the meta tool catalog has ~6; external tools (file/shell/web/MCP) have ~10. ~25-30 grammars total.
- Brief 135 sets the floor at 24GB VRAM, 32GB RAM, 8-core CPU, NVMe SSD.

## Findings

1. **xgrammar compilation has two phases.** *Schema parsing* (parse the JSON schema or the EBNF grammar into an internal automaton) and *FSM construction* (build the token-level finite-state machine the constrained decoder steps through). Schema parsing is microseconds; FSM construction is the dominant cost.

2. **FSM construction time scales with grammar size and tokenizer vocabulary.** For Qwen3's 152k vocabulary, a moderate-complexity grammar (~50 production rules) takes ~80-200ms to compile on a single CPU core. A very complex grammar (Brief 023 modifier-surface DSL, hundreds of rules) takes 500-800ms.

3. **v0.1 grammar inventory: ~30 grammars.** Worst case: 30 × 500ms serial = 15 seconds. This is unacceptable for cold start. Best case: 30 × 100ms parallel on 8 cores = 400ms. Acceptable but tight.

4. **Precompilation + serialization is the right answer.** xgrammar supports serializing compiled FSMs to disk. Build the grammars at GSPL install time (or on first launch), serialize to `~/.gspl/grammar-cache/<grammar-id>-<vocab-hash>.bin`, load from disk on subsequent boots. Disk-load latency: ~5-15ms per grammar = ~150-450ms total at the floor with NVMe.

5. **Vocab-hash invalidates the cache on backbone change.** When the user changes backbone (e.g., upgrade Qwen3-14B → Qwen3-32B), the vocabulary may differ. The cache key includes a hash of the tokenizer; cache misses trigger recompilation in parallel.

6. **Cold-boot budget at floor: ≤500ms grammar load + 200ms backbone load + 100ms KV cache init = ~800ms total.** Within the 1-second cold-boot budget set by the Brief 104 first-ten-minutes UX.

7. **Hot-reload during session: free.** Grammars are loaded once at session start; tool calls reuse the already-loaded FSM. No per-call compilation cost.

8. **Grammar size on disk: ~100-500KB each.** Total grammar cache footprint: ~10MB. Negligible against the 200GB SSD floor.

9. **Per-creator custom grammars are first-class.** When a creator adds a custom tool (per Brief 128 plugin extension), its grammar is compiled on first use and cached identically. The cache directory is content-addressed by grammar source hash, so reusing a published custom tool across creators reuses the cached FSM.

10. **Compilation is itself signed.** The compiled FSM cache file is content-addressed, the cache index is signed by the GSPL install (`grammar-cache-index://<install-id>`), and rollback works on the cache the same way it works on any other gseed. If a compiled FSM is corrupted (e.g., disk error), the verification fails and the kernel forces recompile.

## Risks identified

- **Tokenizer drift across model versions.** Qwen3-14B → Qwen3-30B → Qwen3-32B may all have slightly different vocabularies. Mitigation: vocab-hash in cache key catches this; full recompile takes ~1 second on 8 cores in parallel.
- **Custom grammar quality is creator-dependent.** A creator can write a malformed grammar that takes seconds to compile or silently produces wrong constraints. Mitigation: plugin loader runs a 100ms compile-time budget check before accepting a custom grammar; over-budget grammars are rejected with a clear error.
- **xgrammar library is young.** The library is well-maintained (NVIDIA/xgrammar) but has fewer production deployments than llama.cpp's grammar mode. Mitigation: pin to a known-good xgrammar release; ship llama.cpp grammar fallback for the smaller grammar set if xgrammar regresses.

## Recommendation

**Adopt xgrammar as the v0.1 grammar engine. Precompile all ~30 v0.1 grammars at install time, serialize to `~/.gspl/grammar-cache/<grammar-id>-<vocab-hash>.bin`. Cold-boot grammar load budget: ≤500ms at the floor with NVMe. Per-creator custom grammars are content-addressed and cached identically; plugin loader enforces a 100ms compile-time budget check on submission. Grammar cache index is a signed gseed with rollback. Pin to a known-good xgrammar release; ship llama.cpp grammar fallback for the core 10-tool primitive set as a redundancy mechanism.**

## Confidence

**4/5.** xgrammar's published benchmarks support these numbers. The unknowns are: (a) actual cold-boot timing on the full v0.1 grammar set (Round 7 measurement), and (b) creator custom-grammar pathological cases.

## Spec impact

- `gspl-reference/intelligence/grammar-cache.md` — new file documenting precompilation, cache layout, vocab-hash invalidation, custom grammar loading.
- `gspl-reference/research/128-gspl-tool-use-and-modifier-surface.md` — cross-reference at the xgrammar primitive infrastructure line.
- `gspl-reference/research/104-first-user-experience-first-ten-minutes.md` — cross-reference; cold-boot ≤1s is a Brief 104 commitment.

## New inventions

- **INV-576** — *Vocab-hashed precompiled grammar cache* with content-addressed FSM artifacts, signed cache index, and creator-custom grammar reuse across creators. Eliminates per-session compilation cost while preserving the typed-by-construction guarantee.

## Open follow-ups

- Actual cold-boot timing on the full grammar set (Round 7 measurement).
- Whether to publish the precompiled grammar cache as a downloadable artifact for fresh installs (avoids first-launch compile entirely).
- Long-term: whether to switch to grammar JIT inside the kernel for more flexibility.

## Sources

1. NVIDIA, *xgrammar: Flexible and Efficient Structured Generation Engine*, 2024.
2. ggerganov, *llama.cpp grammar mode*, GitHub.
3. Brief 023 — Modifier-surface DSL.
4. Brief 104 — First-user experience.
5. Brief 128 — GSPL tool-use and modifier-surface intelligence.
6. Brief 135 — Hardware budget for v0.1.
