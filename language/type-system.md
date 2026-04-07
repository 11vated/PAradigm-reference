# GSPL Type System

GSPL combines four ideas into a single coherent type system: **Hindley-Milner inference**, **refinement types**, **dependent types** (limited form), and **effect polymorphism**. Together they let the compiler catch bugs that would otherwise surface only at run time, without forcing the programmer to write annotations everywhere.

## Hindley-Milner Inference

GSPL uses Algorithm W for principal-type inference. A function written without annotations gets the most general type that fits its body:

```gspl
fn double(x) { x * 2 }
// Inferred: fn double(x: int) -> int
//          (or fn double[T: Numeric](x: T) -> T if used polymorphically)
```

Inference is global within a module but bounded by `export` annotations: an exported function's type is fixed at its declaration site.

Annotations are still encouraged for top-level public functions because they document intent and stabilize the public API.

## Base Types

```
int           — 64-bit signed integer
float         — IEEE-754 binary64
bool          — true | false
string        — Unicode string
void          — unit type (no value)
seed          — UniversalSeed
```

Plus the 17 gene types as first-class citizens:

```
scalar, categorical, vector, expression, struct, array, graph, topology,
temporal, regulatory, field, symbolic, quantum, gematria, resonance,
dimensional, sovereignty
```

Each gene type has its own operators (mutate, crossover, distance, validate, canonicalize) and is treated as a primitive by the type system.

## Composite Types

```gspl
type Pair[A, B] = (A, B);
type Maybe[T] = Some(T) | None;
type Result[T, E] = Ok(T) | Err(E);

type Character = {
    name: string,
    health: int,
    inventory: [string],
    archetype: categorical,
};
```

Records are nominal (declared) — two records with the same shape but different names are different types. Sum types (algebraic data types) are exhausted by `match`.

## Refinement Types

A refinement type narrows a base type with a predicate:

```gspl
type Probability = { x: float | x >= 0.0 && x <= 1.0 };
type NonEmptyString = { s: string | length(s) > 0 };
type EvenInt = { n: int | n % 2 == 0 };
```

The compiler checks the refinement at *every* place a value flows in. If it can prove the predicate holds, no run-time check is needed. If not, an explicit cast or `assert` is required.

```gspl
fn sqrt_safe(x: { f: float | f >= 0.0 }) -> float { ... }

let y: float = read_input();
sqrt_safe(y);  // ERROR: cannot prove y >= 0.0
sqrt_safe(if y >= 0.0 { y } else { 0.0 });  // OK
```

Refinements are the primary mechanism for catching gene-value-out-of-range bugs at compile time.

## Dependent Types (Limited Form)

GSPL supports dependent types for sizes and indices, but not arbitrary value-dependent types (the full Π/Σ machinery would make inference undecidable). The compiler tracks length-indexed arrays and bounded integers:

```gspl
type Matrix[m: int, n: int] = [[float; n]; m];

fn multiply[m, k, n](
    a: Matrix[m, k],
    b: Matrix[k, n],
) -> Matrix[m, n] { ... }
```

The shape mismatch is a compile error:

```gspl
let a: Matrix[3, 4] = ...;
let b: Matrix[5, 2] = ...;
multiply(a, b);  // ERROR: 4 != 5
```

This is enough to catch the most common matrix and tensor bugs without dragging in a full proof assistant.

## Effect Polymorphism

GSPL has algebraic effects. A function's signature can declare which effects it may perform:

```gspl
fn read_file(path: string) -> string effects(Read) { ... }
fn pure_compute(x: int) -> int { ... }   // no effects
```

Effect rows are inferred just like types. A function without an effect annotation is inferred to perform the union of effects of all functions it calls.

```gspl
fn process(path: string) -> int {
    let content = read_file(path);   // performs Read
    parse_int(content)               // pure
}
// Inferred: fn process(path: string) -> int effects(Read)
```

The 8 standard effects are: `Read`, `Write`, `Random`, `Time`, `Network`, `GPU`, `Log`, `Sign`. User code can declare new effects via the `effect` keyword.

### Handler Polymorphism

A function generic over an effect can be applied with different handlers:

```gspl
fn collect_logs[E](work: fn() -> int effects(E, Log)) -> ([string], int) effects(E) {
    let logs = [];
    let result = handle work() with {
        Log(msg) -> { logs.push(msg); resume(()) }
    };
    (logs, result)
}
```

Effect handlers are themselves first-class values. This is the same model as Eff and Koka.

## Type Inference Algorithm

The compiler uses constraint-based inference (a variant of Algorithm W with row polymorphism for effects):

1. Walk the AST, generating fresh type variables for each unannotated binding.
2. Generate equality constraints from each expression's structure.
3. Generate refinement obligations from each refinement type's predicate.
4. Solve the equality constraints via unification.
5. Discharge refinement obligations via SMT (Z3 / CVC5 in development; a small custom decision procedure in production).
6. Discharge effect-row obligations by union and subset.

Unsolvable constraints become typed compile errors with locations and suggestions.

## Why This System

The motivating goals:

1. **Catch gene-range bugs at compile time** — refinement types make `gene_value: { x: float | x in [0,1] }` enforced.
2. **Catch shape bugs at compile time** — dependent types make matrix and array dims checkable.
3. **Catch determinism violations at compile time** — effect rows make `Random` and `Time` visible in the signature so the compiler can verify that an `@deterministic` function doesn't transitively call something non-deterministic.
4. **Stay invisible when not needed** — Hindley-Milner means small scripts don't need any annotations.

The system is more powerful than mainstream gradually-typed languages but lighter than full proof assistants. It targets the sweet spot where 95% of pipeline bugs become compile errors.

## Pragmatic Notes

- Type errors are **structured**, with quick-fix suggestions where possible (e.g., "did you mean to add `as float`?").
- Refinement checks fall back to runtime asserts when the SMT solver can't decide statically (compile warning, run-time guard).
- The whole type system is **erasable**: at run time only the values exist; types are not reified. This keeps the runtime small and makes interop easy.
