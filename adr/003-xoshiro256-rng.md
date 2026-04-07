# ADR-003: Use xoshiro256** + splitmix64 for the Kernel RNG

**Status:** Accepted
**Date:** 2024-08-15
**Layer:** Layer 0 (Kernel)

## Context

Every Paradigm engine needs random numbers, but the random numbers must be:

1. **Deterministic** — same seed → same sequence on every machine.
2. **Portable** — bit-identical across CPU architectures, OSes, and language runtimes.
3. **Statistically excellent** — must pass BigCrush, PractRand, and TestU01.
4. **Fast** — millions of calls/second on commodity hardware (engines call RNG inner-loop).
5. **Splittable** — derived sub-streams for parallel work without correlation.
6. **Small** — easy to serialize as part of seed state.

The default OS RNG fails (1) and (5). Mersenne Twister is slow and notoriously hard to split. PCG is a strong candidate but its variants have evolved confusingly. Java's `Random` is too weak statistically. ChaCha20 is overkill (cryptographic guarantees we don't need at our hot-path cost).

## Decision

We will use `xoshiro256**` as the workhorse PRNG and `splitmix64` for seeding and substream derivation. Both are standardized in modern languages (Java 17 `RandomGeneratorFactory`, Rust `rand` crate, etc.) and well-vetted.

See [`algorithms/xoshiro256.md`](../algorithms/xoshiro256.md) for full pseudocode and references.

For substream derivation we use `splitmix64(parent_state.s0 ^ fnv1a(label))` where `label` is a stable string like `"stage:morphogenesis"`. Same parent + same label → same substream; different labels → statistically independent streams.

## Consequences

**Positive:**

- 256-bit state is trivially serializable as part of seed state.
- ~2 ns per call on modern x86 (4× faster than Mersenne Twister).
- Passes all known statistical tests including 32 GB of PractRand.
- Substream derivation is `O(1)` and lock-free, perfect for parallel evolution islands.
- Library implementations exist in TypeScript, Rust, Go, Python, C++, and Java; cross-validated by RFC-style test vectors.

**Negative:**

- `xoshiro256**` is *not* cryptographically secure. We do not use it where cryptographic randomness is required (key generation, nonces). For those, we use OS getrandom/CSPRNG.
- The substream derivation via FNV-1a + splitmix64 is *our* convention, not a standard. We must document and test it carefully (see the determinism test suite).
- Mistakes in implementation are subtle: a single sign error in `rotl` produces a working-looking but incorrect generator. Test against known seed → known sequence vectors at every implementation.

## Alternatives Considered

- **Mersenne Twister (MT19937):** Slow, 2.5 KB state, splitting is hard, fails BigCrush.
- **PCG (Permuted Congruential Generator):** Strong contender. Faster than MT, smaller state. Rejected because the PCG family has multiple variants (PCG-XSH-RR, PCG-DXSM, etc.) with non-obvious tradeoffs, and we want one canonical choice that won't be questioned in two years.
- **ChaCha20:** Cryptographically secure, deterministic, well-supported. Rejected because it's 5-10× slower than xoshiro256** in hot loops, which adds up over millions of evaluations per generation.
- **Lehmer128:** Even faster than xoshiro256**. Rejected because it has weaker statistical properties on the low bits.
- **OS getrandom:** Not deterministic. Use only for key generation.

## References

- Blackman & Vigna, *Scrambled Linear Pseudorandom Number Generators* (2018)
- Steele, Lea, Flood, *Fast Splittable Pseudorandom Number Generators* (OOPSLA 2014)
- Vigna, *xoshiro / xoroshiro generators and the PRNG shootout*: https://prng.di.unimi.it
