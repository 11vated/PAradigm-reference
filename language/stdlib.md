# GSPL Standard Library

The GSPL standard library is the set of modules every GSPL program can `import` without external dependencies. It is intentionally small — large enough to write any pipeline without reaching outside, small enough to learn in an afternoon.

## Module Index

| Module | Purpose |
|---|---|
| `std::core` | Built-in types, basic operations, the prelude (auto-imported) |
| `std::math` | Mathematical functions and constants |
| `std::vec` | Vector and matrix operations |
| `std::seed` | UniversalSeed operations (canonicalize, hash, sign, verify, mutate, breed, distance) |
| `std::gene` | The 17 gene type operators (mutate, crossover, distance, validate, canonicalize) |
| `std::evolve` | Population evolution algorithms |
| `std::engine` | Engine registration and grow operations |
| `std::compose` | Cross-domain functor composition |
| `std::rng` | Deterministic RNG (xoshiro256, splitmix64, normal, uniform) |
| `std::color` | OKLab, RGB, HSL color science |
| `std::geom` | Geometry primitives, SDF helpers, mesh operations |
| `std::audio` | DSP primitives, oscillators, envelopes, filters |
| `std::io` | File and stdio (effects: Read, Write) |
| `std::http` | HTTP client (effects: Network) |
| `std::time` | Clock and timing (effect: Time) |
| `std::log` | Structured logging (effect: Log) |
| `std::test` | Property-based and unit testing primitives |

## std::core (auto-imported prelude)

Always available without `import`:

```
// Types
int, float, bool, string, void, seed, scalar, categorical, vector, ...

// Constructors
some(x), none, ok(x), err(e), pair(a, b), tuple(...)

// Combinators
map, filter, fold, reduce, scan, zip, unzip, range, repeat
identity, const, compose, flip, curry

// Predicates
is_some, is_none, is_ok, is_err, is_empty, all, any

// Conversions
to_string, parse_int, parse_float, to_int, to_float

// Assertions
assert(cond), require(cond, msg), unreachable()
```

## std::math

```
pi, e, tau, sqrt2, ln2, deg, rad
abs, sign, min, max, clamp, lerp, smoothstep
sqrt, cbrt, pow, exp, log, log2, log10
sin, cos, tan, asin, acos, atan, atan2
floor, ceil, round, trunc, frac
gcd, lcm
hypot, fma
```

All `std::math` functions are `@deterministic` and `@pure`.

## std::vec

```
type Vec2 = (float, float);
type Vec3 = (float, float, float);
type Vec4 = (float, float, float, float);
type Mat3 = [[float; 3]; 3];
type Mat4 = [[float; 4]; 4];

fn add[N], sub[N], mul[N], div[N], dot[N], cross, length, normalize, distance, lerp[N];
fn matmul[m, n, p](a: Matrix[m, n], b: Matrix[n, p]) -> Matrix[m, p];
fn transpose[m, n](m: Matrix[m, n]) -> Matrix[n, m];
fn invert(m: Mat3) -> Maybe[Mat3];
fn invert(m: Mat4) -> Maybe[Mat4];
```

## std::seed

```
fn canonicalize(s: seed) -> seed;
fn hash(s: seed) -> bytes32;
fn sign(s: seed, key: PrivKey) -> seed effects(Sign);
fn verify(s: seed) -> bool;

fn mutate(s: seed, rate: { f: float | f in [0,1] }, rng: Rng) -> seed effects(Random);
fn breed(a: seed, b: seed, rng: Rng) -> seed effects(Random);
fn compose(s: seed, target: domain) -> seed;
fn distance(a: seed, b: seed) -> float;

fn grow(s: seed) -> Artifact;
```

## std::gene

For each of the 17 gene types, the standard set:

```
fn <T>::mutate(g: T, rate: float, rng: Rng) -> T effects(Random);
fn <T>::crossover(a: T, b: T, rng: Rng) -> T effects(Random);
fn <T>::distance(a: T, b: T) -> float;
fn <T>::validate(g: T) -> Result[void, ValidationError];
fn <T>::canonicalize(g: T) -> T;
```

`T` ranges over `scalar`, `categorical`, `vector`, `expression`, `struct`, `array`, `graph`, `topology`, `temporal`, `regulatory`, `field`, `symbolic`, `quantum`, `gematria`, `resonance`, `dimensional`, `sovereignty`.

## std::evolve

```
type EvolveAlgo = GA | MAPElites | CMAES | NoveltySearch | AURORA | DQD | POET;

type EvolveConfig = {
    algorithm: EvolveAlgo,
    population_size: int,
    generations: int,
    fitness: fn(seed) -> QualityVector,
    descriptors: [fn(seed) -> float],   // for MAP-Elites
    elitism: int,
    mutation_rate: float,
    rng: Rng,
};

fn evolve(initial: [seed], cfg: EvolveConfig) -> EvolveResult effects(Random);
```

## std::compose

```
fn compose(s: seed, target: domain) -> seed;
fn find_path(source: domain, target: domain) -> Maybe[[Functor]];
fn register_functor(f: Functor) -> void;
```

## std::rng

```
type Rng = ...;     // opaque

fn from_seed(s: seed) -> Rng;
fn from_bytes(b: bytes32) -> Rng;
fn substream(r: Rng, name: string) -> Rng;

fn uniform_int(r: Rng, lo: int, hi: int) -> int effects(Random);
fn uniform_float(r: Rng, lo: float, hi: float) -> float effects(Random);
fn normal(r: Rng, mean: float, stddev: float) -> float effects(Random);
fn choose[T](r: Rng, options: [T]) -> T effects(Random);
fn shuffle[T](r: Rng, items: [T]) -> [T] effects(Random);
```

## std::color

```
type RGB = (float, float, float);
type OKLab = (float, float, float);
type HSL = (float, float, float);

fn rgb_to_oklab(c: RGB) -> OKLab;
fn oklab_to_rgb(c: OKLab) -> RGB;
fn rgb_to_hsl(c: RGB) -> HSL;
fn oklab_lighten(c: OKLab, amount: float) -> OKLab;
fn oklab_darken(c: OKLab, amount: float) -> OKLab;
fn palette_distance(a: [OKLab], b: [OKLab]) -> float;
fn palette_coherence(p: [OKLab]) -> float;   // [0, 1]
```

## std::geom

```
type SDF = fn(p: Vec3) -> float;

// Primitives
fn sphere(radius: float) -> SDF;
fn box(half_extents: Vec3) -> SDF;
fn cylinder(radius: float, half_height: float) -> SDF;
fn torus(major: float, minor: float) -> SDF;

// Operations
fn union(a: SDF, b: SDF) -> SDF;
fn intersect(a: SDF, b: SDF) -> SDF;
fn subtract(a: SDF, b: SDF) -> SDF;
fn smooth_union(a: SDF, b: SDF, k: float) -> SDF;

// Transforms
fn translate(s: SDF, t: Vec3) -> SDF;
fn rotate(s: SDF, axis: Vec3, angle: float) -> SDF;
fn scale(s: SDF, factor: float) -> SDF;

// Extraction
fn marching_cubes(s: SDF, bounds: BBox, resolution: int) -> Mesh;
```

## std::audio

```
fn sine(freq: float, t: float) -> float;
fn square(freq: float, t: float, duty: float) -> float;
fn triangle(freq: float, t: float) -> float;
fn saw(freq: float, t: float) -> float;
fn noise_white(rng: Rng) -> float effects(Random);
fn noise_pink(rng: Rng) -> float effects(Random);

type Envelope = ...;
fn adsr(attack: float, decay: float, sustain: float, release: float) -> Envelope;
fn apply_envelope(samples: [float], env: Envelope, sample_rate: int) -> [float];

fn lowpass(samples: [float], cutoff: float, sample_rate: int) -> [float];
fn highpass(samples: [float], cutoff: float, sample_rate: int) -> [float];
fn reverb(samples: [float], room_size: float, damping: float) -> [float];
```

## std::io

```
fn read_text(path: string) -> string effects(Read);
fn write_text(path: string, content: string) -> void effects(Write);
fn read_bytes(path: string) -> bytes effects(Read);
fn write_bytes(path: string, content: bytes) -> void effects(Write);
fn print(msg: string) -> void effects(Write);
fn println(msg: string) -> void effects(Write);
```

## std::test

```
fn assert(cond: bool, msg: string);
fn assert_eq[T: Eq](a: T, b: T);
fn property[T](name: string, gen: Gen[T], pred: fn(T) -> bool);

type Gen[T] = ...;
fn gen_int(lo: int, hi: int) -> Gen[int];
fn gen_float(lo: float, hi: float) -> Gen[float];
fn gen_seed(domain: domain) -> Gen[seed];
```

## Determinism Notes

Every function in the standard library that doesn't declare an effect is `@deterministic` and produces bit-identical outputs across machines. Functions that declare `Random` use a deterministic RNG passed in by the caller — no hidden global RNG anywhere.

The `std::time` module is the one explicit source of wall-clock non-determinism, and it's quarantined behind the `Time` effect so deterministic runs can refuse to call it.
