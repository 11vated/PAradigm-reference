# Phase 2 — GSPL Language and First Engine

**Duration:** Months 3-4 (8 weeks)
**Goal:** A working GSPL compiler that takes a `.gspl` source file and produces a deterministic seed via the Sprite engine.

## Why this is second

GSPL is the language every higher layer is written in. Without it, engines have no input format, the agent has no target language to assemble, and the marketplace has nothing to sell. The compiler must be solid before any engine can be built against it, but it can be built against a *stub* engine — and that's what Phase 2 does.

## Deliverables

| Deliverable | Acceptance |
|---|---|
| `gspl-lexer/` | Tokenizes the full grammar in `language/grammar.ebnf` |
| `gspl-parser/` | Produces AST for every example program in `examples/` |
| `gspl-resolve/` | Name resolution + module imports |
| `gspl-typeck/` | Hindley-Milner with refinements; rejects ill-typed programs |
| `gspl-effects/` | Effect inference + checking |
| `gspl-ir/` | Lowering from AST to IR |
| `gspl-codegen/` | Codegen to Rust for engine targets |
| `gspl-stdlib/` | The Std.* modules listed in `language/stdlib.md` |
| `gspl-driver/` | CLI compiler with diagnostics |
| First reference engine | Stub Sprite engine that consumes IR and emits a deterministic seed |
| Diagnostic test suite | At least 50 negative tests with expected error messages |

## Week-by-week plan

### Week 1: Lexer

- Implement the lexer using `chumsky`
- Handle: identifiers, keywords, numeric literals (int / float / hex), string literals with escapes, operators, delimiters, comments (line + block), whitespace, newlines
- Position tracking for diagnostics
- Test against 30 sample tokens

### Week 2: Parser → AST

- Define the AST types in `gspl_ast`
- Implement the parser top-down following `language/grammar.ebnf`
- Productions: module, import, type decl, function decl, expr, pattern, match arms, let bindings
- Pretty-printer for AST (used in golden tests)
- Test: parse all `examples/*.gspl` files cleanly

### Week 3: Name resolution

- Build symbol tables per module
- Resolve identifiers to definitions
- Handle imports and aliasing
- Detect: unresolved name, duplicate definition, shadowing
- Module dependency graph + cycle detection

### Week 4: Type checker (Hindley-Milner core)

- Implement type variables, unification, generalization, instantiation
- Type the simply-typed core: literals, lambda, application, let
- Tuples, records, ADTs (sum types), pattern matching
- Implement the standard error messages from `language/typeck.md`
- Test: 30 positive and 30 negative tests

### Week 5: Type checker (refinements + dependent slices)

- Refinement types: `Int { x | x >= 0 }`, `String { s | len(s) <= 80 }`
- Solve refinements via SMT (start with `z3.rs`, may swap to native solver later)
- Dependent slice types: `Vec<T, N>`
- Test: refinement tests from `language/refinements.md`

### Week 6: Effect checker + IR lowering

- Effect inference: every function gets an effect row
- Effect checking: pure functions cannot call effectful ones; effects propagate
- Lower AST → IR: explicit closures, monomorphized generics, eliminate sugar
- IR pretty-printer

### Week 7: Codegen + stdlib + driver

- Codegen: IR → Rust source for engine targets
- Stub Sprite engine: takes IR, runs a simple deterministic computation, returns a seed
- Implement `Std.*` modules (math, collections, strings)
- CLI driver: `gspl build`, `gspl check`, `gspl run`
- Diagnostics rendering with `ariadne`

### Week 8: Hardening + golden tests + first end-to-end

- Run the full example suite end-to-end: `.gspl` → compile → execute against stub engine → produce signed `.gseed`
- Verify the resulting `.gseed` round-trips through Phase 1's reader
- Golden tests: 50 small programs with expected outputs
- Negative tests: 50 ill-typed programs with expected error messages
- Tag `gspl-0.2.0`

## Risks and mitigations

**Risk:** Hindley-Milner with refinements is the most complex single piece of work in the entire roadmap.
**Mitigation:** Start with vanilla HM. Add refinements behind a flag. Use SMT solver as a black box. Defer dependent types to Phase 4 if necessary; don't block other work on them.

**Risk:** Effect checking interacts with type checking and can be hard to get right.
**Mitigation:** Treat effects as a separate row variable in the type system, inferred independently. Read the Koka and Eff papers before implementing.

**Risk:** Stub engine is too stub-ish to validate the IR contract.
**Mitigation:** Include in the stub a real call to the kernel's RNG, JCS, and signing — so the stub at least exercises the determinism path end-to-end.

## What is *not* in Phase 2

- No real engines (only the stub Sprite engine)
- No evolution
- No agent
- No GPU code
- No Studio

## Done definition

1. The example program `examples/melancholy_bard.gspl` compiles, runs, and produces a deterministic signed seed.
2. The same program produces byte-identical output on Linux and macOS.
3. The compiler emits friendly errors for at least 30 common mistakes.
4. The IR is documented in `language/ir.md`.
5. Tag `gspl-0.2.0`.
