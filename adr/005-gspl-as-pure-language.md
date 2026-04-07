# ADR-005: Make GSPL a Pure Functional Language with Algebraic Effects

**Status:** Accepted
**Date:** 2024-09-02
**Layer:** Layer 2 (Language)

## Context

GSPL is the language users write to author seeds, define new domains, and compose existing ones. We have to choose its evaluation model, type system, and effect model. The choice cascades through everything: the engines below it, the studio above it, and the agent that synthesizes it.

The language must satisfy:

1. **Determinism by construction.** A program with no side effects is automatically reproducible. We do not want to retrofit reproducibility on a language that allows it to leak.
2. **Composability.** Domains, engines, and seeds must compose without surprise. Pure functional code is famously composable.
3. **Explicit side effects.** Network access, randomness, time, and GPU dispatch are all effects we want users to *see* in function signatures, not have hidden.
4. **Familiar enough that users can write it.** Hindley-Milner with type inference; ML-family syntax; not Haskell-pure (no monad transformer stack).
5. **GPU-targetable.** Pure functions are easy to compile to WGSL/SPIR-V; impure ones aren't.

## Decision

GSPL is a **pure functional language with algebraic effects**:

- All functions are pure unless they declare effects in their type signature: `fn fetch(url: String) -> String effects { Network }`.
- Effects are *handled* at the call site by an effect handler — the same `fetch` call can be intercepted to return mocked data, replayed from a recording, or actually executed.
- The 8 effect types are: `Read`, `Write`, `Random`, `Time`, `Network`, `GPU`, `Log`, `Sign`.
- The type system is Hindley-Milner with refinement types and effect-row polymorphism.
- Functions annotated with `@gpu` must be effect-free (no Network/Read/Write/Time/Sign/Log; only `Random` and `GPU` are allowed) so they can be compiled to WGSL.

See [`language/grammar.ebnf`](../language/grammar.ebnf), [`language/type-system.md`](../language/type-system.md), and [`language/keywords.md`](../language/keywords.md).

## Consequences

**Positive:**

- A function with no declared effects is *guaranteed* to be deterministic by the type system. The compiler enforces this; users cannot accidentally call `Date.now()` from a pure function.
- Effect handlers give us replay, mocking, and time-travel debugging for free.
- GPU compilation is a straightforward syntactic check: walk the function body, reject if any non-GPU effect appears.
- Pure functional code is parallelizable by default; the evolution stack can shard work freely.
- Users learn one effect model that handles all I/O — no monad confusion, no callback hell.

**Negative:**

- Users coming from imperative languages have to internalize "effects in signatures." We mitigate this with the GSPL Agent and the studio's auto-completion.
- Hindley-Milner inference with effect rows is non-trivial to implement correctly. We allocate a full quarter of engineering to the type checker.
- Some patterns (long-lived stateful objects) are awkward in a pure language. We provide an explicit `State` effect that wraps mutable state with handler-based access.
- Algebraic effects are still a relatively niche feature; we have to write good documentation and tutorials.

## Alternatives Considered

- **Embedded DSL in TypeScript:** Easier to ship; users already know TypeScript. Rejected because TypeScript's type system cannot enforce purity, and we cannot retrofit determinism.
- **Lua/JavaScript with sandboxing:** Familiar to game developers. Rejected for the same reason — sandboxing prevents *most* non-determinism but not all (Math.random, Date.now), and the user has to remember not to use them.
- **Rust as the user language:** Compiled, safe, deterministic. Rejected because compile times kill interactive iteration in the studio, and the borrow checker is too steep for non-engineer creators.
- **Lisp/Scheme:** Pure, simple, composable. Rejected for ergonomic reasons (parens, syntactic minimalism scares non-programmers).
- **Haskell:** The right choice technically but unapproachable for non-experts. We adopted Haskell's effect philosophy without its monadic surface syntax.
- **Koka / Effekt:** Languages with first-class algebraic effects. Strongly inspired the design but too research-y to bet a startup on.

## References

- Plotkin & Pretnar, *Handlers of Algebraic Effects* (ESOP 2009)
- Leijen, *Koka: Programming with Row-Polymorphic Effect Types* (MSFP 2014)
- Brachthäuser, Schuster, Ostermann, *Effects as Capabilities: Effect Handlers and Lightweight Effect Polymorphism* (OOPSLA 2020)
