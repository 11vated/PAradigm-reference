# Paradigm GSPL Engine — Technical R&D

This directory holds the technical research that resolves the load-bearing open questions in the spec **before** any code is written. The goal is to de-risk the parts of the spec that, if wrong, would force a major rewrite during Phase 1.

## Charter

Each brief in this directory addresses **one** open question, follows a fixed template, and ends with an actionable conclusion. The audience is an AI coding agent (or a human engineer working through Phase 1) — the briefs are written to be machine-actionable, not narrative.

The briefs are **research outputs**, not normative spec. When a brief recommends a change to the spec, it's flagged in the `Spec impact` section and will be folded into the spec in a separate, traceable PR.

## Methodology

1. **Primary sources only.** RFCs, language specs, library source code, peer-reviewed papers, and authoritative documentation. Blog posts are admissible as secondary corroboration but never as the only source.
2. **Confidence ratings.** Every conclusion carries a confidence score from 1 (speculative) to 5 (verified against source code or formal spec). Anything below 3 is a red flag for further investigation.
3. **Reproducibility.** Where a finding depends on a specific tool version, library commit, or empirical measurement, that version is pinned in the brief.
4. **Conservative bias.** When sources disagree or evidence is thin, the brief recommends the more conservative path and flags the disagreement.
5. **Spec impact is explicit.** Every brief lists exactly which spec files it touches and what the proposed change is. No silent drift.

## Brief template

Every brief in this directory has these sections, in this order:

```
# NNN — <Question title>

## Question
One sentence stating the question.

## Why it matters (blast radius)
What breaks in the spec / Phase 1 plan if we get this wrong.

## What we know from the spec
Pointers to the relevant spec sections that depend on this.

## Findings
Numbered findings, each with citations to primary sources.

## Risks identified
Specific failure modes the findings revealed.

## Recommendation
Concrete, actionable. "Use X with config Y" or "Defer to Phase N because Z."

## Confidence
1-5, with rationale.

## Spec impact
List of spec files to update and the proposed change.

## Open follow-ups
Things we still don't know that the brief did not resolve.

## Sources
Numbered list of citations matching the inline references.
```

## Brief index

### Tier 1 — Foundational (Phase 1 blockers)

| # | Title | Status | Confidence |
|---|-------|--------|------------|
| 001 | GPU determinism cross-vendor | done | 3 |
| 002 | WGSL portable subset | done | 4 |
| 003 | JCS canonicalization edge cases | done | 4 |
| 004 | RFC 6979 ECDSA via p256 crate | done | 4 |
| 005 | zstd deterministic encoding | done | 4 |
| 006 | HM + refinements feasibility | done | 3 |

### Tier 2 — Compliance (cannot ship without)

| # | Title | Status | Confidence |
|---|-------|--------|------------|
| 007 | c2pa-rs library maturity | done | 4 |
| 008 | Image DCT watermark robustness | done | 3 |
| 009 | audiowmark robustness | done | 4 |
| 010 | EU AI Act 2026 application details | done | 4 |

### Tier 3 — Operational (cannot run as solo founder without)

| # | Title | Status | Confidence |
|---|-------|--------|------------|
| 011 | Agent reliability backstops | done | 3 |
| 012 | MAP-Elites convergence in our budgets | done | 3 |

### Synthesis

| Doc | Purpose |
|-----|---------|
| `synthesis.md` | Cross-brief findings, spec impact summary, Phase 1 plan deltas |

## How to read this directory

If you are a human engineer:
- Start with `synthesis.md`. It tells you what changed and why.
- Read briefs 001–006 before writing any kernel code.
- Read briefs 007–010 before designing the export pipeline.
- Read briefs 011–012 before building the agent and evolution loops.

If you are an AI coding agent:
- Each brief's `Recommendation` is your operating instruction for the relevant subsystem.
- Each brief's `Spec impact` lists files in the parent repo that take precedence over the brief if they conflict.
- Treat any finding with confidence ≤ 2 as a hard stop — surface it to the human and ask before proceeding.

## What is deliberately NOT in this directory

- **Build planning.** That belongs in `roadmap/`.
- **Architecture decisions.** Those belong in `adr/`. A brief can recommend an ADR but does not replace one.
- **Performance benchmarks against real hardware.** Those require Phase 1 infrastructure to be stood up first. The briefs cite published benchmarks where they exist and flag where empirical measurement is required.
- **Anything resolved by spec text already.** If the spec answers the question, it's not an open question.
