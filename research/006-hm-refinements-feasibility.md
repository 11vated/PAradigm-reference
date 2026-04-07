# 006 — Hindley-Milner + refinements feasibility for a solo founder

## Question
Is it feasible for a single engineer to implement, ship, and maintain a Hindley-Milner type inferencer extended with refinement types (in the Liquid Types tradition) for the GSPL DSL within Phase 1, and what compromises does the budget force?

## Why it matters (blast radius)
The GSPL DSL is the user-facing surface. Its type system promises both ergonomic inference (no annotations needed for typical seeds) and refinement-checked invariants (e.g., "this color channel is in [0,1]", "this kernel size is a power of two"). If the type system is too ambitious, Phase 1 slips and the DSL never ships. If it is too weak, the spec's safety claims do not hold and the kernel layer has to re-check everything at runtime — losing the entire ergonomic and performance argument for having types at all. This brief gates `dsl/types.md`, `dsl/inference.md`, and the entire Phase 1 timeline.

## What we know from the spec
- `dsl/types.md` calls for HM-style let-polymorphism with no required annotations.
- `dsl/types.md` separately calls for refinement predicates over a small theory (linear arithmetic, equality, basic uninterpreted functions).
- `dsl/inference.md` is mostly empty pending this brief.

## Findings

1. **Vanilla Hindley-Milner is small, well-understood, and feasible for a single engineer in days, not weeks.** [1, 2, 3] The classical Algorithm W (or Algorithm J for efficiency) implementation is on the order of 500-1500 lines in a high-level language. Multiple high-quality tutorials and reference implementations exist. The hard part is not the inference algorithm; it is the testing and the error messages.

2. **HM with let-generalization is decidable in DEXPTIME but practically near-linear on real programs.** [1] The pathological cases (`let x1 = fn ... in let x2 = (x1, x1) in let x3 = (x2, x2) in ...` blowing up types exponentially) do not occur in human-written code. The textbook implementation is fast enough for any plausible GSPL seed.

3. **Refinement types on top of HM are *not* a small extension.** [4, 5, 6, 7] Type checking (let alone inference) is undecidable in the presence of even simple linear arithmetic refinements [4]. Practical implementations rely on:
   - **Predicate abstraction** (Liquid Types) to keep refinement inference decidable by restricting refinements to a finite set of templates [5].
   - **An external SMT solver** (almost always Z3) to discharge the verification conditions [4, 6].
   - **A constraint generation pass** that turns typing derivations into systems of constrained Horn clauses [4].

4. **The smallest published Liquid-Types-style implementation is on the order of 5,000-10,000 lines** plus a Z3 dependency, plus a substantial test corpus, plus a substantial doc corpus to teach users how to write refinements that the inferencer can actually solve. [5, 6]

5. **Refinement type *checking* (with annotations) is far easier than refinement type *inference*.** [4, 5] If the user writes the refinement explicitly, the system only needs to generate verification conditions and ship them to Z3 — a tractable engineering task on the order of 1,000-2,000 lines plus the Z3 binding.

6. **The 1991 Freeman-Pfenning paper** [8] established that *datasort refinements* (a restricted form: refinements drawn from a finite lattice of subtypes of a base type) preserve ML-style decidable inference. This is the most ergonomic refinement system that fits on top of HM without requiring an SMT solver, but it is much weaker than Liquid Types — it cannot express arithmetic constraints.

7. **All known production refinement type systems** (LiquidHaskell, Stainless for Scala, F*, Dafny, Refinement Reflection, etc.) are multi-person, multi-year projects. None has shipped from a solo founder in under a year as a side concern of a larger system.

## Risks identified

- **The Liquid Types path is a year-long project on its own,** competing with every other Phase 1 deliverable. Pursuing it directly will sink the timeline.
- **The "we'll just call Z3" instinct underestimates the work** of constraint generation, predicate template design, error reporting, and proving that the SMT calls actually terminate within a budget on real GSPL programs.
- **Datasort refinements alone are too weak** to cover the spec's stated invariants (numeric range checks, power-of-two checks, length-equal-to-N checks).
- **A bad refinement system is worse than no refinement system,** because users will write refinements that the inferencer rejects for opaque reasons and lose trust in the entire DSL.
- **A `// trust me` escape hatch** undermines the safety claim if it is the path of least resistance for users.

## Recommendation

**Phase the type system in three explicit milestones:**

### v1 (Phase 1, ships with the engine)

- **Vanilla Hindley-Milner with let-polymorphism.** Algorithm J implementation, Damas-Milner generalization, sound and complete for the base type system.
- **No refinements at the language level.** Range and shape constraints are checked at the *kernel boundary* by runtime asserts that abort with a clear error if violated. The DSL does not have refinement syntax yet — this avoids committing to a syntax we will regret.
- **Effort estimate:** 2-4 weeks for one engineer including parser, inferencer, error messages, and a thorough test suite. This is the well-trodden path.

### v1.5 (between Phase 1 and Phase 2)

- **Add datasort refinements (Freeman-Pfenning style).** Finite lattices of subtypes — e.g., `Nat <: Int`, `PowerOfTwo <: Nat`, `UnitInterval <: Float`. Inference remains decidable. No SMT solver.
- **Datasorts are declared by the standard library**, not by user code, at v1.5. User-declared datasorts come later.
- **Effort estimate:** 4-8 weeks. Substantial but bounded.

### v2 (separate release, potentially after a co-founder or grant)

- **Liquid-Types-style refinements with Z3.** Linear arithmetic, equality, uninterpreted functions over the existing datasort lattice. User-written refinement annotations on function signatures.
- **Inference is local** — refinements are checked, not inferred, except in trivially propagatable cases.
- **Effort estimate:** 3-6 months. This is the project that needs justification, prototyping, and dedicated focus.

### What this means for the spec right now

- The spec must stop promising "refinement-inferred safety" at v1.
- The spec must explicitly say what is checked at compile time vs at the kernel boundary at v1.
- The spec must reserve syntax for refinements without committing to it. Do not bake `{x: Int | x > 0}` into v1 syntax.
- The spec must say which invariants are runtime-checked at v1 and migrate them to compile-time at v1.5/v2.

## Confidence
**3/5.** The vanilla HM portion is 5/5 confident. The "refinements are a year of work" portion is 4/5 confident based on the published track record of every existing system. The 3/5 overall reflects genuine uncertainty about whether *datasort refinements* (the v1.5 path) really are as cheap as Freeman-Pfenning's 1991 paper suggests for our specific lattice — that needs a prototype before committing.

## Spec impact

- **`dsl/types.md` — REWRITE.** Drop the implication that refinements are a v1 feature. Add the three-milestone phasing explicitly. List the v1 invariants that are runtime-checked rather than statically refined.
- **`dsl/inference.md`** — fill in the empty file with the Algorithm J / Damas-Milner approach for v1.
- **`dsl/runtime-checks.md`** — new file listing every invariant that is runtime-checked at v1 because it is not yet expressible in the type system.
- **`roadmap/phase-1.md`** — adjust scope to reflect the v1 type system, not the v2 type system.
- **`roadmap/phase-2.md`** — add the v1.5 datasort milestone and the v2 Liquid-Types milestone with explicit effort estimates and triggers.
- New ADR: `adr/00NN-type-system-phasing.md` — capture this decision and the reasoning.

## Open follow-ups

- Build a one-week prototype of vanilla HM for a GSPL subset to validate the 2-4 week v1 estimate. Phase 1 task.
- Build a two-week datasort prototype to validate the 4-8 week v1.5 estimate before promising it to anyone. Phase 1 task.
- Survey LiquidHaskell, Stainless, and F* error messages to learn what *not* to do for v2.
- Decide whether the v2 Z3 dependency is acceptable under the spec's "boring tech, minimal deps" rule. Z3 is heavy and stateful; this needs an explicit ADR.

## Sources

1. Hindley-Milner type system overview. https://en.wikipedia.org/wiki/Hindley%E2%80%93Milner_type_system
2. Implementing a Hindley-Milner Type System (tutorial). https://blog.stimsina.com/post/implementing-a-hindley-milner-type-system-part-1
3. Damas-Hindley-Milner inference two ways. https://bernsteinbear.com/blog/type-inference/
4. Data Flow Refinement Type Inference (PACMPL). https://dl.acm.org/doi/10.1145/3434300
5. Refinement type — overview. https://en.wikipedia.org/wiki/Refinement_type
6. Refinement Type Refutations (PACMPL). https://dl.acm.org/doi/10.1145/3689745
7. Refinement Types lecture notes (Northeastern). https://prl.khoury.northeastern.edu/blog/static/refinement_types_lecture.pdf
8. Freeman & Pfenning, Refinement Types for ML (PLDI 1991). https://www.cs.cmu.edu/~fp/papers/pldi91.pdf
