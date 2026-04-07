# 138 — Compaction cadence calibration

## Question

How often should the sleep-cycle compaction (Brief 127) actually fire, what triggers it, and what is the size and quality budget for each pass?

## Why it matters (blast radius)

Sleep-cycle compaction is the mechanism that lets a creator's session survive multi-day sustained use without unbounded context growth. Compact too rarely and the kernel runs out of context (Brief 135 violation). Compact too often and we lose nuance from prior turns, regressing the four-tier memory's episodic accuracy. The cadence is a single tunable knob with very real downstream effects.

## What we know from the spec

- Brief 127 specifies sleep-cycle compaction as a periodic process that summarizes episodic memory into semantic memory.
- Brief 127 leaves the cadence as a parameter to be calibrated.
- Brief 135 fixes the v0.1 floor context window at 32k tokens.

## Findings

1. **Three trigger types must compose: time-based, fill-based, and event-based.** Time-based: every N hours of active session. Fill-based: when working memory crosses K% of context window. Event-based: when a session crosses a creator-defined boundary (end of a Studio editing session, signed-off gseed, deliberate "save and continue").

2. **Fill-based is the primary trigger at the floor.** With a 32k context window, the natural rhythm is to fire compaction when working memory hits ~24k tokens (75%). This leaves headroom for the compaction process itself plus immediate next-turn growth. Any time-based or event-based trigger that fires when working memory is below 60% should be ignored as premature.

3. **Compaction is itself a signed gseed.** Each compaction pass produces an `episodic-compaction://<session>/<turn-range>` artifact: a summary, the source turn-range parent edge, and a confidence-bearing field. Per Brief 105, the compaction is rollback-able — if the summary loses important nuance, the user can roll back and replay with a finer-grained pass.

4. **Compaction quality budget: 8:1 ratio at floor, 4:1 in high-fidelity mode.** At the floor we compress ~24k of working memory into ~3k of summary. The compaction model is the same backbone (Qwen3-14B); quality decay across the 8:1 ratio is acceptable for routine sessions but loses detail for high-stakes sessions (legal, research). High-fidelity mode runs at 4:1 (~6k summary) and is opt-in.

5. **Compaction is incremental, not full-rewrite.** Each pass summarizes only the *oldest* third of working memory, preserving the most recent two-thirds verbatim. This avoids the "telephone game" degradation where each pass re-summarizes already-summarized material.

6. **Latency budget: ≤5 seconds at the floor.** A 24k→3k compaction with Qwen3-14B at int4 takes ~3-4 seconds in benchmark. Five seconds is the hard ceiling — anything longer interrupts the user. Latency above 5s triggers an immediate cadence backoff (less frequent compaction, larger summary ratio).

7. **Time-based fallback: every 30 minutes of active session.** This catches sessions that drift below the 75% fill threshold but accumulate stale state. 30 minutes is short enough that no individual compaction loses too much, long enough that interactive users don't see constant pauses.

8. **Event-based trigger fires immediately on signed-off gseed.** When the user explicitly signs and ships an artifact, that's a natural memory boundary. The relevant turns get compacted into a "completed work" gseed with an accept-event parent edge.

9. **Quality monitor: track compaction loss with a held-out probe set.** Each session keeps a small (~10) set of probe questions about its own state. After every compaction, the model is asked the probe questions; if accuracy drops below 90%, the next compaction backs off to 4:1 ratio.

10. **Cadence adaptive over the life of v0.1.** Initial cadence is conservative (75% fill, 30-minute time, 8:1 ratio). After two weeks of telemetry, daily router updates (Brief 132) include compaction-cadence parameter updates as part of the same daily LoRA pass.

## Risks identified

- **Probe set is itself memory overhead.** ~10 probes × 5 turns of context each ≈ 1k tokens of permanent overhead per session. Mitigation: probes are stored in episodic memory (not working memory) and only loaded during the post-compaction quality check.
- **8:1 ratio loses code/math detail.** Code and math sessions need full fidelity. Mitigation: namespace-aware compaction — code and math sessions auto-default to 4:1; lifestyle and chat sessions default to 8:1.
- **Time-based trigger interrupts long focused sessions.** Mitigation: time-based is suppressed during tool-use bursts (no compaction within 5 seconds of a tool call).

## Recommendation

**Set v0.1 sleep-cycle compaction with three composed triggers: fill-based primary at 75% of context window, time-based fallback at 30 min of active session, event-based on signed-off gseed. Default ratio 8:1; namespace-aware override to 4:1 for code/math/research; user opt-in to 4:1 high-fidelity mode for any session. Latency hard ceiling 5 seconds at floor hardware. Each compaction is a signed `episodic-compaction://` gseed with parent edge to its source turns. Quality monitor: 10-probe-question set checked post-compaction; >10% accuracy drop triggers next-pass backoff to 4:1. Cadence parameters are tunable via the daily router update LoRA after 2 weeks of telemetry.**

## Confidence

**4/5.** The trigger composition follows directly from Brief 127. The exact thresholds are conservative defaults that need empirical tuning, which is exactly what the daily LoRA cadence is for. The unknown is the probe-set construction methodology; defer to Round 7 implementation.

## Spec impact

- `gspl-reference/intelligence/compaction.md` — new file documenting the trigger composition, ratios, latency budget, and quality monitor.
- `gspl-reference/research/127-gspl-memory-and-context.md` — cross-reference at the sleep-cycle compaction line.
- `gspl-reference/research/132-router-classifier-training-data.md` — note that compaction cadence parameters share the daily LoRA with the router.

## New inventions

- **INV-568** — *Three-trigger composed compaction* (fill / time / event) with namespace-aware ratio defaults. The first compaction protocol that adapts to *what kind of work* a session is doing rather than treating all sessions identically.
- **INV-569** — *Probe-set quality monitor.* A small set of session-internal questions whose post-compaction accuracy gates the next-pass backoff. Self-supervised quality control without external labels.

## Open follow-ups

- Probe set construction methodology (Round 7).
- Whether the high-fidelity mode should be the default for paid creator tiers (Brief 106 cross-reference).
- Telemetry for cadence auto-tuning (Brief 056 cross-reference).

## Sources

1. Brief 127 — GSPL memory and context.
2. Brief 056 — Observability, telemetry, privacy.
3. Brief 132 — Router classifier training data.
4. Anthropic, *Long context summarization*, 2024 (compaction patterns).
5. Liu et al., *Recurrent Memory Transformer*, NeurIPS 2022 (incremental compaction).
