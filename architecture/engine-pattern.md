# The Domain Engine Pattern

Every one of the 26 domain engines conforms to the same interface and the same staged-pipeline pattern. This is what makes the platform extensible: a third party can ship a new domain engine in a day if they understand this pattern.

## The `DomainEngine` Interface

```ts
interface DomainEngine {
  readonly domain: Domain;                  // e.g., "character"
  readonly version: string;                 // semver, e.g., "1.2.3"
  readonly geneSchema: GeneSchema;          // declared genes + types
  readonly stages: Stage[];                 // ordered developmental pipeline
  readonly outputType: ArtifactType;        // mesh | image | audio | game | ...

  validate(seed: UniversalSeed): Result<void, ValidationError>;
  grow(seed: UniversalSeed, ctx: GrowContext): Promise<Artifact>;

  // Optional capabilities
  readonly renderHints?: RenderHints;       // how the studio should preview
  readonly exportHints?: ExportHints;       // which export formats are supported
  readonly fitnessHints?: FitnessHints;     // which QualityVector axes are meaningful
}
```

### `Stage`

A stage is a pure function from the previous stage's output (plus the seed) to a new intermediate state. Each stage is named, deterministic, side-effect-free, and may be cached.

```ts
interface Stage<In, Out> {
  readonly name: string;                    // e.g., "morphogenesis"
  readonly inputType: TypeOf<In>;
  readonly outputType: TypeOf<Out>;
  run(input: In, seed: UniversalSeed, rng: DeterministicRng): Out;
}
```

The first stage takes the seed itself; the last stage produces the final artifact.

### `GrowContext`

```ts
interface GrowContext {
  readonly kernel: Kernel;
  readonly rng: DeterministicRng;           // pre-seeded from seed.$hash
  readonly logger: StructuredLogger;
  readonly cache?: StageCache;              // optional intermediate cache
  readonly cancellation?: CancellationToken;
}
```

The context is immutable for the duration of `grow`. The engine never reaches outside it. This is what makes engines deterministic and safely embeddable in any host (browser, Node, edge runtime).

## Pipeline Discipline

Every engine's pipeline must follow these rules:

1. **Stages are ordered.** No re-ordering, no skipping. The order is part of the engine spec.
2. **Stages are typed.** The output type of stage `i` is the input type of stage `i+1`. The compiler / type checker enforces this.
3. **Stages are pure.** A stage is a function `(input, seed, rng) → output`. No global state, no I/O, no wall clock.
4. **Stages are deterministic.** Given the same `(input, seed, rng)`, a stage produces the same output bit-for-bit.
5. **Stages may use sub-RNG streams.** Each stage gets its own sub-stream via `rng.substream(stage.name)` so adding or removing a stage in the middle doesn't shift the RNG state for later stages.
6. **Stages may cache.** If a stage is expensive and idempotent, it can be cached by `(seed.$hash, stage.name)`. The cache is content-addressed.
7. **Stages may emit warnings.** Non-fatal issues (e.g., a gene value at the edge of its valid range) flow through `ctx.logger` as structured warnings without failing the grow.

## Stage Catalog (recurring stages across engines)

Many engines share stage names. The names are not mandatory but are strongly conventional, so an external observer can read any engine and understand it without studying the implementation.

| Stage name | Meaning |
|---|---|
| `extract`        | Read genes off the seed and convert to working types |
| `morphogenesis`  | Generate base form (mesh, layout, structure) from genes |
| `populate`       | Fill the form with content (limbs, instruments, rooms, characters) |
| `parameterize`   | Compute derived parameters from base genes |
| `simulate`       | Run a simulation step (physics, ecosystem, narrative grammar) |
| `pose`           | Apply animation, transforms, or arrangement |
| `texture`        | Generate or apply textures, materials, palettes |
| `light`          | Compute lighting, IBL, ambient |
| `compose`        | Combine layers, tracks, or sub-objects |
| `render`         | Produce the final pixel/audio/binary output |
| `export`         | Wrap in a target format envelope (PNG, glTF, WAV, HTML5) |

A typical pipeline draws 4–8 stages from this catalog plus 0–4 engine-specific stages.

## Worked Example: The Sprite Engine

The Sprite engine is the largest implemented engine in the existing codebase (3,673 LOC, 8 stages). Its pipeline:

```
1. extract        : pull color, body_template, animation_set, palette, size genes
2. morphogenesis  : compose body parts from the body_template field
3. parameterize   : compute joint positions, eye positions, weapon attachment points
4. texture        : generate the per-pixel palette using OKLab color science
5. pose           : compute frames for each animation in the animation_set
6. compose        : combine frames into a sprite atlas
7. render         : rasterize to PNG with alpha
8. export         : emit PNG bytes + JSON metadata (frame map, hitboxes)
```

Output: a `SpriteArtifact` containing the PNG, the metadata, and a manifest of supported animations.

## Worked Example: The Music Engine

```
1. extract        : pull scale, tempo, instrument_set, mood, genre genes
2. parameterize   : compute key signature, time signature, song structure
3. morphogenesis  : generate the harmonic progression (theory-driven)
4. populate       : compose melodies for each instrument under voice-leading rules
5. render         : synthesize WAV via DSP (oscillators + envelopes + effects)
6. export         : emit WAV bytes + MIDI bytes + JSON metadata
```

Output: a `MusicArtifact` containing the WAV, the MIDI, and the structural metadata.

## Worked Example: The FullGame Engine

```
1. extract        : pull theme, mechanics, level_seeds, character_seeds, narrative_seeds genes
2. morphogenesis  : generate world layout from procedural rules
3. populate       : place characters, items, hazards via the level_seeds
4. parameterize   : compute game balance numbers (HP, damage, cooldowns)
5. simulate       : run a balance pass — play the game with a stub AI to verify completability
6. compose        : assemble HTML5 bundle (engine.js, assets, index.html)
7. render         : minify and pack into a single deployable archive
8. export         : emit .zip bytes + manifest
```

Output: a `FullGameArtifact` containing a self-contained HTML5 game.

The full per-engine specs live in [`engines/`](../engines/).

## Engine Registration

Engines register themselves with the kernel at startup:

```ts
kernel.engineRegistry.register(spriteEngine);
kernel.engineRegistry.register(characterEngine);
kernel.engineRegistry.register(musicEngine);
// ...
```

The registry is the only place that knows the full set of engines. Looking up an engine by domain:

```ts
const engine = kernel.engineRegistry.get("character");
const artifact = await engine.grow(seed, ctx);
```

## Adding a New Engine

The minimum work to add a new domain engine to Paradigm:

1. Choose a domain name (kebab-case discouraged: use `vehicle`, not `vehicle-engine`).
2. Declare the gene schema — which named genes does this domain need, and what type is each? Pull from the 17-type system.
3. Design the pipeline — which stages, in what order, with what types between?
4. Implement each stage as a pure function.
5. Implement `validate` and `grow` on the `DomainEngine` interface.
6. Register with the kernel.
7. Optionally provide `renderHints`, `exportHints`, `fitnessHints`.
8. Optionally register a functor bridge from another domain into this one (or vice versa).
9. Write determinism tests (self-replay, cross-platform, browser parity, mutation determinism).
10. Document in `engines/<domain>.md` following the engine template.

The whole process should take 1–3 days for a simple domain, 1–3 weeks for a complex one. The 26-domain target is achievable for a small team because the pattern is uniform.

## Anti-Patterns

These are forbidden:

- **Calling another engine inside `grow`.** If you need cross-domain composition, do it via Layer 5 (functor bridges), not by directly calling another engine. Engines must be siblings, not nested.
- **Mutating the seed inside `grow`.** Engines are read-only on their input. If you need a derived seed, create a new one via the seed operations.
- **Reading global state.** No globals, no env vars, no filesystem reads outside the `Read` effect.
- **Reading the system clock.** Use `ctx.kernel.time` (which can be mocked) if you absolutely must.
- **Skipping stages conditionally based on seed values.** Stages run unconditionally; conditional behavior lives *inside* a stage. This keeps the pipeline shape stable for caching and reasoning.
- **Stateful stages.** A stage cannot remember anything between calls.
