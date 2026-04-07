# xoshiro256** + splitmix64 RNG

## Why these two

Paradigm needs an RNG that is:

- **Deterministic and portable** — same output on every CPU and OS.
- **Fast** — millions of calls per second on a modern CPU.
- **Statistically excellent** — passes BigCrush, PractRand, and TestU01 batteries.
- **Splittable** — substreams derivable from a parent state for parallel work.
- **Small** — minimal state, easy to serialize.

`xoshiro256**` (256-bit state, 4× faster than Mersenne Twister, passes all known statistical tests) is the workhorse. `splitmix64` is a 64-bit-state stateless integer hash used to seed `xoshiro256**` and to derive substreams. The combination is the same one used by Java 17's `RandomGeneratorFactory` and is well-vetted.

## State

```
struct Xoshiro256ssState:
    s0: u64
    s1: u64
    s2: u64
    s3: u64
```

256 bits total. Trivially serializable.

## Constants

```
ROTATIONS: rotl(x, k) = (x << k) | (x >> (64 - k))   (over u64)
```

## next() — produce one u64

```
fn next(state: &mut Xoshiro256ssState) -> u64:
    let result = rotl(state.s1 * 5, 7) * 9
    let t = state.s1 << 17
    state.s2 ^= state.s0
    state.s3 ^= state.s1
    state.s1 ^= state.s2
    state.s0 ^= state.s3
    state.s2 ^= t
    state.s3 = rotl(state.s3, 45)
    return result
```

This is the standard `xoshiro256**` step. The "**" variant is the strongest of the xoshiro family for general-purpose use.

## Seeding via splitmix64

A user provides a 64-bit seed. We must expand it to 256 bits to initialize `xoshiro256**`. We use four `splitmix64` steps to do so:

```
fn splitmix64(state: &mut u64) -> u64:
    state = state + 0x9E3779B97F4A7C15
    let z = state
    z = (z ^ (z >> 30)) * 0xBF58476D1CE4E5B9
    z = (z ^ (z >> 27)) * 0x94D049BB133111EB
    return z ^ (z >> 31)

fn seed_xoshiro256ss(seed: u64) -> Xoshiro256ssState:
    let mut sm = seed
    return Xoshiro256ssState {
        s0: splitmix64(&mut sm),
        s1: splitmix64(&mut sm),
        s2: splitmix64(&mut sm),
        s3: splitmix64(&mut sm),
    }
```

The constants `0x9E3779B97F4A7C15`, `0xBF58476D1CE4E5B9`, and `0x94D049BB133111EB` are the canonical splitmix64 magic numbers (Steele, Lea, Flood, 2014).

## Seeding from a seed hash

In Paradigm we typically seed from a 32-byte SHA-256 of canonical seed JSON. We fold the 256 bits down to 64:

```
fn seed_from_hash(hash: bytes32) -> u64:
    let mut acc: u64 = 0
    for i in 0..4:
        acc ^= u64_le(hash[i*8..(i+1)*8])
    return acc
```

Then call `seed_xoshiro256ss(acc)`.

## Substream derivation

When work is split across stages, gene types, or parallel evolution islands, each sub-task needs an independent stream that's deterministically derived from the parent. We use `splitmix64` of `(parent_seed XOR fnv1a(label))`:

```
fn fnv1a_64(s: string) -> u64:
    let mut h: u64 = 0xCBF29CE484222325
    for byte in s.bytes():
        h ^= byte
        h = h * 0x100000001B3
    return h

fn substream(parent: &Xoshiro256ssState, label: string) -> Xoshiro256ssState:
    let mix = parent.s0 ^ fnv1a_64(label)
    let mut sm = mix
    return Xoshiro256ssState {
        s0: splitmix64(&mut sm),
        s1: splitmix64(&mut sm),
        s2: splitmix64(&mut sm),
        s3: splitmix64(&mut sm),
    }
```

The label is a stable string like `"stage:morphogenesis"` or `"gene:palette"`. The same parent + same label always produces the same substream. Different labels produce statistically independent streams (verified by the fact that fnv1a + splitmix64 are good hashes; collisions are negligible at the bit level).

## Higher-level distributions

```
fn uniform_int(rng: &mut Rng, lo: int, hi: int) -> int:
    let range = hi - lo
    return lo + (next(rng) as int) % range    // for unbiased: rejection sample

fn uniform_float(rng: &mut Rng, lo: float, hi: float) -> float:
    // 53-bit mantissa, multiply into [0, 1), scale into [lo, hi)
    let bits = next(rng) >> 11
    let f = (bits as float) * (1.0 / (1u64 << 53))
    return lo + f * (hi - lo)

fn normal(rng: &mut Rng, mean: float, stddev: float) -> float:
    // Box-Muller. Cache the second sample.
    if rng.has_cached_normal:
        rng.has_cached_normal = false
        return mean + stddev * rng.cached_normal
    let u1 = uniform_float(rng, 1e-300, 1.0)
    let u2 = uniform_float(rng, 0.0, 1.0)
    let r = sqrt(-2.0 * ln(u1))
    let theta = 2.0 * pi * u2
    let z0 = r * cos(theta)
    let z1 = r * sin(theta)
    rng.cached_normal = z1
    rng.has_cached_normal = true
    return mean + stddev * z0
```

The Box-Muller transform is exact (no rejection). We cache the second sample to amortize the cost across two calls.

## Determinism Notes

- `xoshiro256**` is portable: bit operations are well-defined in every modern language.
- `splitmix64` and `fnv1a` use only 64-bit unsigned arithmetic.
- The Box-Muller normal uses `sqrt`, `ln`, `cos`, `sin` — these must be IEEE-754 compliant. On x86 builds, compile with `--no-x87` to force SSE2 binary64.
- Cached normal state is part of the serialized RNG state; pause/resume must preserve it.

## Tests

The reference test suite for any RNG implementation:

1. **Known seed → known sequence.** Seed with 0; first 16 outputs must match a published vector.
2. **Substream isolation.** Two substreams derived from the same parent must have outputs whose pairwise distance from parent state is statistically uniform.
3. **Cross-language byte-equality.** A TypeScript implementation and a Rust implementation seeded identically must produce bit-identical sequences.
4. **PractRand 32 GB pass.** Generate 32 GB of output and run PractRand; no failures expected.

## References

- Blackman & Vigna, *Scrambled Linear Pseudorandom Number Generators* (2018) — the xoshiro family
- Steele, Lea, Flood, *Fast Splittable Pseudorandom Number Generators* (OOPSLA 2014) — splitmix64
- Box & Muller, *A Note on the Generation of Random Normal Deviates* (1958)
