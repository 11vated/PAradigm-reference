# Cross-Domain Composition

The 26 domain engines are siblings, not nested. When a user wants a *character with a theme song and a level designed around them*, no single engine produces it. Instead, the platform composes seeds across domains using **functor bridges** — typed, category-theoretic mappings from one domain's seed space into another.

This document specifies the functor system, the registry, the pathfinding algorithm that finds composition routes, and the laws every functor must obey.

## The Problem

A naive approach to cross-domain generation has each engine call into others:

```
characterEngine.grow(seed) -> calls musicEngine.grow(theme_song_seed)
                            -> calls fullGameEngine.grow(level_seed)
```

This breaks layering (Layer 4 calling Layer 4), creates implicit dependencies, makes determinism harder to reason about, and forces every engine to know about every other engine. It does not scale to 26 domains.

The category-theoretic approach instead **lifts composition out of the engines into Layer 5** and treats each engine as a pure functor from `Seed[domain] -> Artifact[domain]`. Cross-domain mappings are then *separate* functors `Seed[A] -> Seed[B]` that are composed externally.

## The `Functor` Interface

```ts
interface Functor<A extends Domain, B extends Domain> {
  readonly source: A;
  readonly target: B;
  readonly name: string;                    // e.g., "character_to_music"
  readonly version: string;

  apply(seed: UniversalSeed & { $domain: A }): UniversalSeed & { $domain: B };

  // Optional: a fitness-aware variant for use inside an evolution loop
  applyWithContext?(
    seed: UniversalSeed & { $domain: A },
    ctx: CompositionContext,
  ): UniversalSeed & { $domain: B };
}
```

A functor is a pure, deterministic function. Given the same input seed it produces the same output seed bit-for-bit. Like an engine, it never reads global state or the wall clock.

## The Nine Pre-Registered Functors

Paradigm ships with nine bridges covering the most common composition routes:

| Source → Target | Purpose | Approach |
|---|---|---|
| `character → sprite` | Render a character's 2D form from its 3D morphology | Project mesh silhouette, sample texture, derive palette |
| `character → music` | Compose a theme song matching personality | Map personality vector to mode/tempo/instrumentation |
| `character → fullgame` | Spawn a playable game starring the character | Use character as protagonist seed, generate level around their abilities |
| `procedural → fullgame` | Wrap a procedural world in a playable game | Use procgen output as environment, add objectives and mechanics |
| `music → ecosystem` | Drive an ecosystem simulation by music structure | Map harmonic complexity to species count, tempo to interaction rate |
| `physics → fullgame` | Build a physics-puzzle game from a physics simulation | Lift physics params, add goals and level layout |
| `visual2d → animation` | Animate a static 2D image | Detect rig points, apply skeletal motion |
| `narrative → fullgame` | Generate a game from a story | Each story beat becomes a level, characters become NPCs |
| `terrain → fullgame` | Build an open-world game on a procedural terrain | Wrap terrain in nav mesh, add quests and POIs |

Each functor lives in its own file under `intelligence/functors/<source>_to_<target>.md` with a full pseudocode specification.

## The Functor Registry

The registry is a directed graph where nodes are domains and edges are registered functors:

```ts
class FunctorRegistry {
  private functors: Map<`${Domain}->${Domain}`, Functor<Domain, Domain>>;

  register<A extends Domain, B extends Domain>(f: Functor<A, B>): void;
  get<A extends Domain, B extends Domain>(source: A, target: B): Functor<A, B> | undefined;
  outgoing(source: Domain): Functor<Domain, Domain>[];
  incoming(target: Domain): Functor<Domain, Domain>[];
}
```

The registry is populated at startup. Third parties can register additional functors at runtime (subject to validation that they obey the laws below).

## Composition Pathfinding

When the user asks to compose `character` with `fullgame`, a direct functor exists, so `apply` runs once. When the user asks to compose `narrative` with `music`, no direct functor exists, but the registry can find a path:

```
narrative -> fullgame -> [no edge to music]
narrative -> [no other outgoing]
```

In this case, no path exists and the system reports it. When a path *does* exist (e.g., `procedural -> fullgame -> ...`), the system finds the shortest one via BFS:

```
fn find_path(source: Domain, target: Domain) -> Option<Vec<Functor>>:
    if source == target:
        return Some(vec![identity_functor(source)])
    visited = HashSet::from([source])
    queue = VecDeque::from([(source, vec![])])
    while let Some((node, path)) = queue.pop_front():
        for f in registry.outgoing(node):
            if f.target == target:
                return Some([path, f].concat())
            if !visited.contains(&f.target):
                visited.insert(f.target)
                queue.push_back((f.target, [path, f].concat()))
    return None
```

When multiple paths exist, the BFS returns the *shortest*. If two paths have the same length, ties are broken by lexicographic ordering of the functor names — keeping pathfinding deterministic.

## Composition Application

Once a path is found, applying it is a left-fold:

```
fn compose(seed: Seed, path: Vec<Functor>) -> Seed:
    let mut current = seed;
    for f in path:
        assert!(current.$domain == f.source);
        current = f.apply(current);
    return current
```

The intermediate seeds along the way are not artifacts — they are still seeds. Only at the *end* of the composition path does the user typically call `grow(final_seed, target_engine)` to materialize an artifact. This means a long composition path is cheap (no engine work happens until the end) and the entire composition is a single deterministic transformation of the original seed.

## MultiDomainSeed and Coherence

A common need is producing a *bundle* of related artifacts (e.g., character + theme music + signature level) that share a coherent identity. Rather than apply functors and discard the intermediate seeds, the platform tracks them in a `MultiDomainSeed`:

```ts
interface MultiDomainSeed {
  readonly $primary: UniversalSeed;
  readonly $derived: Map<Domain, UniversalSeed>;
  readonly $coherence: number;  // [0, 1]
}
```

The **coherence score** is a measure of how well the derived seeds reflect the primary. It's computed by:

1. Apply the inverse functor (when one exists) and measure distance to the primary in its native gene space.
2. Compare the QualityVector dimensions of the derived artifacts; high coherence ↔ similar style and novelty axes.
3. Average over all derived domains.

A coherence score of 1.0 means every derived seed perfectly reflects the primary; 0.0 means the derived seeds are unrelated. A typical "good" composition scores ≥ 0.7. The score is informational — the user may accept lower coherence if the resulting bundle is creatively interesting.

## The Functor Laws

Every registered functor must obey these laws, which are verified by property-based tests on every CI build:

### Law 1: Determinism

```
forall seed. f.apply(seed) == f.apply(seed)
```

A functor produces the same output for the same input, every time. (This is just the determinism guarantee of Layer 5 inherited.)

### Law 2: Hash Consistency

```
forall seed. f.apply(seed).$hash == hash(canonicalize(f.apply(seed)))
```

The output seed's `$hash` is correctly computed from its canonical form. Functors must not forget to recompute the hash; the registry rejects functors that produce malformed seeds.

### Law 3: Lineage Propagation

```
forall seed. f.apply(seed).$lineage.parents includes seed.$hash
forall seed. f.apply(seed).$lineage.operation == "compose:" + f.name
```

The output seed records the input seed as a parent and identifies the functor used. This is what makes royalty propagation work across compositions.

### Law 4: Identity (when applicable)

For `identity_functor(D): D -> D`,

```
forall seed in D. identity_functor(D).apply(seed) == seed (modulo lineage)
```

The identity functor changes lineage but otherwise leaves the seed alone. This is required for the BFS pathfinding's `source == target` early-out to be sound.

### Law 5: Associativity (when paths overlap)

For functors `f: A -> B`, `g: B -> C`, `h: C -> D`,

```
forall seed in A. h.apply(g.apply(f.apply(seed))) == compose([f, g, h]).apply(seed)
```

Composition is associative — the order in which functors are applied along a path is determined entirely by the path order and not by grouping. The category-theoretic phrasing: the registry forms a category whose objects are domains and whose morphisms are functors.

### Law 6: No Information Fabrication

A functor must not invent gene values that have no basis in the source seed. Every gene in the output must be either (a) computed deterministically from source genes or (b) a default value declared in the target domain's schema. This is a soft law enforced by code review rather than property testing, but it's essential to make compositions feel principled rather than hallucinated.

## Worked Example: Character → Music

```
fn character_to_music(char_seed: Seed { $domain: "character" }) -> Seed { $domain: "music" }:
    let personality = char_seed.genes["personality"]   // vector gene
    let archetype   = char_seed.genes["archetype"]     // categorical gene

    // Map personality dimensions to musical parameters
    let aggression  = personality["aggression"]        // [0, 1]
    let warmth      = personality["warmth"]            // [0, 1]
    let complexity  = personality["complexity"]        // [0, 1]

    let tempo = lerp(60, 180, aggression)              // bpm
    let mode = if warmth > 0.5 { "major" } else { "minor" }
    let instruments = if archetype == "warrior" {
        ["timpani", "brass", "low_strings"]
    } else if archetype == "rogue" {
        ["pizzicato_strings", "woodwinds", "harp"]
    } else {
        ["full_orchestra"]
    }
    let harmonic_density = lerp(0.2, 0.9, complexity)

    let music_seed = UniversalSeed {
        $gst: char_seed.$gst,
        $domain: "music",
        $name: char_seed.$name + " - Theme",
        $lineage: Lineage {
            parents: [char_seed.$hash],
            operation: "compose:character_to_music",
            generation: char_seed.$lineage.generation + 1,
        },
        genes: {
            tempo: scalar_gene(tempo),
            mode: categorical_gene(mode),
            instruments: array_gene(instruments),
            harmonic_density: scalar_gene(harmonic_density),
            scale: derive_scale_from_archetype(archetype),
            structure: default_song_structure(),
        },
        $sovereignty: inherit_sovereignty(char_seed.$sovereignty),
        $metadata: {},
    }
    music_seed.$hash = sha256(canonicalize(music_seed))
    return music_seed
```

The output is a seed in the `music` domain. The user can now grow it into a WAV+MIDI artifact by calling the music engine, or further compose it (e.g., `music -> ecosystem`) by walking another functor.

## Why Category Theory

The functor framing is not just academic. It buys three concrete things:

1. **Compositionality.** The user can extend a composition by adding one functor at a time without rewriting upstream stages. A new `music -> visual2d` functor (e.g., album art generator) immediately enables `character -> music -> visual2d` without touching the existing `character -> music` functor.
2. **Reasoning at the type level.** The compiler knows that `character_to_music: character -> music`, so a programmer cannot accidentally apply it to a sprite seed. Type errors catch composition bugs before they run.
3. **Auditability.** The lineage of every composed artifact is a *path through the functor graph*. A regulator (or a curious user) can trace exactly which functors were involved, in what order, and verify each one independently.

The 9 pre-registered functors are the seed of an open ecosystem. Third parties can publish their own bridges, and the marketplace can pay royalties to functor authors when their bridges are used in profitable compositions.

## Performance and Caching

Functor application is typically cheap — milliseconds for most functors, since they are small pure transformations of gene tables. But long composition paths in evolution loops can add up, so the registry caches functor outputs by `(input.$hash, functor.name, functor.version)`. The cache is content-addressed and shared across runs.

Functors that are themselves expensive (e.g., a rare functor that runs a small DSP pass) should declare so in their metadata; the scheduler avoids placing them inside hot evolution inner loops when possible.
