# GSPL Reserved Keywords

GSPL has exactly 26 reserved keywords. The number is fixed: any future language extension must reuse existing keywords or repurpose contextually-sensitive identifiers, not add new reserved words. This is a deliberate constraint that keeps the language small enough to learn in an afternoon.

| # | Keyword | Category | Purpose |
|---|---|---|---|
| 1 | `seed` | Declaration | Declares a seed in a domain |
| 2 | `gene` | Declaration | Assigns a gene value inside a seed |
| 3 | `fn` | Declaration | Declares a function |
| 4 | `type` | Declaration | Declares a type alias or record/sum type |
| 5 | `trait` | Declaration | Declares a trait (interface) |
| 6 | `domain` | Declaration | Declares a domain (engine schema) |
| 7 | `import` | Module | Imports symbols from another module |
| 8 | `export` | Module | Marks symbols as exported |
| 9 | `let` | Statement | Local variable binding |
| 10 | `if` | Control flow | Conditional |
| 11 | `else` | Control flow | Alternate branch |
| 12 | `match` | Control flow | Pattern matching |
| 13 | `case` | Control flow | Pattern arm in `match` |
| 14 | `return` | Control flow | Early return |
| 15 | `for` | Control flow | Iteration over a collection |
| 16 | `in` | Control flow | Iterable binder in `for` |
| 17 | `while` | Control flow | Loop while condition holds |
| 18 | `do` | Control flow | (Reserved for `do` notation in effect handlers; not yet used) |
| 19 | `true` | Literal | Boolean literal |
| 20 | `false` | Literal | Boolean literal |
| 21 | `nil` | Literal | Null/optional empty |
| 22 | `gpu` | Annotation | (Reserved as keyword; used as `@gpu` annotation) |
| 23 | `effect` | Effect system | Declares an algebraic effect |
| 24 | `handle` | Effect system | Handles an effect computation |
| 25 | `with` | Effect system | Binds handlers in `handle ... with ...` |
| 26 | `where` | Refinement | Refinement clause on types and seeds |

## Why Exactly 26

The 26 keyword budget was chosen to fit the language inside the cognitive working memory of a developer reading it for the first time. Each keyword is single-purpose and earns its place. Adding a 27th would require justifying why an existing keyword can't be repurposed.

## Contextual / Soft Keywords

These identifiers are *not* reserved but have special meaning in specific positions:

- `as` — used in `import x as y;`. Outside import statements, `as` is a normal identifier.
- `effects` — used in function signatures (`fn f() -> T effects(Read, Write)`). Outside that position, normal identifier.
- `from` — used in some import forms. Otherwise normal.

Soft keywords let the grammar avoid bloating the reserved list while still parsing unambiguously.

## Annotation Words

The `@`-prefixed annotations look like keywords but are syntactically a separate class. The standard set:

- `@gpu` — function compiles to a WGSL kernel
- `@pure` — function is provably side-effect-free (compiler verifies)
- `@deterministic` — function is determinism-required (compiler enforces)
- `@inline` — request inlining
- `@cache(by=...)` — declare a cache key
- `@deprecated(...)` — deprecation warning

Annotations are extensible by libraries; user code can declare new annotations without changing the language.
