# Roadmap

This directory describes the build order for Paradigm — what gets built, in what order, with what dependencies, and what milestones gate the next phase. It is the file Gemini (or any other agent) should read first to understand *how to actually construct* the system from the ground up.

## Files

| File | Topic |
|---|---|
| [`build-order.md`](build-order.md) | Topological build order from Layer 0 to Layer 6 |
| [`phase-1-kernel.md`](phase-1-kernel.md) | Months 1-2: Kernel + Seed System + signing |
| [`phase-2-language.md`](phase-2-language.md) | Months 3-4: GSPL compiler and one reference engine |
| [`phase-3-engines.md`](phase-3-engines.md) | Months 5-7: First 6 domain engines + evolution |
| [`phase-4-intelligence.md`](phase-4-intelligence.md) | Months 8-10: GSPL Agent + Studio MVP |
| [`phase-5-marketplace.md`](phase-5-marketplace.md) | Months 11-12: Marketplace + federation + launch |

## Principles

1. **Bottom-up.** Lower layers are built before higher layers depend on them. Layer 6 (Marketplace) is the *last* thing built, not the first.
2. **Vertical slices for validation.** At each phase boundary, a thin end-to-end vertical slice is built and demoed to prove the layers below work.
3. **Each phase is shippable.** Even if work stops at Phase 3, what exists is a working creative tool, not a half-built foundation.
4. **No skipping.** Tempting shortcuts (e.g., "let's start with the Studio because that's what users see") are rejected. The dependency graph is not negotiable.

## Total timeline

**12 months from cold start to v1.0 launch with one engineer.** The phasing is aggressive but achievable because:

- Every layer's spec is written before any code (this repo is the spec).
- Boring tech is used everywhere (Postgres, Fastify, Rust, React) to minimize learning overhead.
- Third-party libraries do the heavy lifting where they exist (wgpu, c2pa-rs, kysely, etc.).
- The Studio MVP is intentionally minimal — the bulk of polish ships post-v1.0.

A two-engineer team would shave roughly 3 months off this timeline. A three-engineer team gains less because of coordination overhead at this stage.

## Critical path

The single longest sequential chain in the dependency graph:

```
Kernel (1mo)
   ↓
Seed system + signing (1mo)
   ↓
GSPL parser + type checker (1mo)
   ↓
GSPL → IR → first engine (1mo)
   ↓
Sprite engine pipeline (1mo)
   ↓
Evolution (MAP-Elites) (1mo)
   ↓
GSPL Agent v1 (2mo)
   ↓
Studio MVP (1mo)
   ↓
Marketplace + Stripe Connect (1mo)
   ↓
Federation (1mo)
   ↓
Launch (1mo: hardening, polish, docs)
```

12 months. Anything that can be parallelized is, but the critical path is fully sequential by design.

## Risk mitigations

- The riskiest unknown is **GSPL Agent quality** — whether the 5-stage pipeline produces good seeds at usable latency. Mitigation: build a "puppet" agent in Phase 2 that uses fixed templates instead of LLMs, so the engines can be developed against a stable interface; swap in the real LLM-driven agent in Phase 4.
- The second riskiest unknown is **GPU determinism** in the Marching Cubes / particle kernels. Mitigation: every GPU kernel has a CPU reference from day one. We can ship with CPU-only if GPU determinism turns out to be intractable.
- The third risk is **scope creep** in the engine catalog — wanting all 26 engines for v1. Mitigation: only 6 engines ship in v1 (Sprite, Music, Texture, Sculpt, Particles, Animation), the rest are post-launch.
