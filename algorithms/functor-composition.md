# Cross-Domain Functor Composition Pathfinding

## What it does

Paradigm's Layer 5 functor registry exposes a directed graph where nodes are domains (`Sprite`, `Character`, `Music`, …) and edges are *functors* — structure-preserving maps that translate one domain's seed into another. This module describes the algorithm that, given a source domain `A` and a target domain `B`, finds the **best chain of functors** to compose.

The "best" chain minimizes a cost function that balances:

1. **Path length** (each functor introduces some loss).
2. **Per-functor coherence loss** (some functors lose more information than others).
3. **Direct edges first** (a single functor `A → B` always beats `A → X → B`).

The output is an ordered list of functors that, when applied in sequence, transform a source seed into a target-domain seed while propagating lineage and royalties.

## Data model

```
struct Functor:
    id: string                     // e.g., "character_to_music"
    source: Domain
    target: Domain
    cost: float                    // 0..1, lower is better
    apply: fn(Seed) -> Seed
    coherence_loss: float          // measured on validation seeds; baked in
    is_lossy: bool

struct FunctorRegistry:
    functors: [Functor]
    by_source: Map<Domain, [Functor]>      // index for outgoing edges
```

The 9 pre-registered Paradigm functors (see `architecture/cross-domain-composition.md`):

| Functor | A → B | Cost |
|---|---|---|
| `sprite_to_character` | Sprite → Character | 0.20 |
| `character_to_music` | Character → Music | 0.30 |
| `music_to_sprite` | Music → Sprite | 0.40 |
| `character_to_animation` | Character → Animation | 0.10 |
| `geometry3d_to_sprite` | Geometry3D → Sprite | 0.25 |
| `sprite_to_geometry3d` | Sprite → Geometry3D | 0.50 |
| `narrative_to_character` | Narrative → Character | 0.15 |
| `character_to_narrative` | Character → Narrative | 0.20 |
| `procedural_to_geometry3d` | Procedural → Geometry3D | 0.10 |

## Pathfinding: Dijkstra's algorithm on the functor graph

Because edge costs are non-negative and we want minimum total cost, Dijkstra is the correct algorithm. (BFS would only minimize hop count, which is wrong because hop count and total cost are correlated but not identical.)

```
struct PathNode:
    domain: Domain
    cumulative_cost: float
    path: [Functor]                // functors applied so far

fn find_path(registry: &FunctorRegistry, source: Domain, target: Domain)
    -> Option<[Functor]>:
    if source == target:
        return Some([])

    let mut queue = MinHeap::new()
    queue.push(PathNode {
        domain: source,
        cumulative_cost: 0.0,
        path: [],
    })
    let mut visited: Set<Domain> = empty_set()

    while let Some(node) = queue.pop():
        if node.domain == target:
            return Some(node.path)
        if visited.contains(&node.domain):
            continue
        visited.insert(node.domain)

        let outgoing = registry.by_source.get(&node.domain).unwrap_or(&[])
        for functor in outgoing:
            if visited.contains(&functor.target):
                continue
            let mut new_path = node.path.clone()
            new_path.push(functor.clone())
            queue.push(PathNode {
                domain: functor.target,
                cumulative_cost: node.cumulative_cost + functor.cost,
                path: new_path,
            })

    return None    // no path exists
```

## MinHeap ordering

The heap orders by `cumulative_cost`, with ties broken by `path.length` (prefer shorter), and final ties broken by lexicographic order of the `path` ids (for determinism):

```
fn compare_path_nodes(a: &PathNode, b: &PathNode) -> Ordering:
    let c = compare(a.cumulative_cost, b.cumulative_cost)
    if c != Equal: return c
    let l = compare(a.path.length, b.path.length)
    if l != Equal: return l
    return compare(path_id_string(&a.path), path_id_string(&b.path))

fn path_id_string(path: &[Functor]) -> string:
    return path.map(|f| f.id).join("→")
```

## Cycle prevention

Dijkstra's `visited` set already prevents revisiting domains, which prevents cycles. But for safety:

- We never re-enter a domain in a single path.
- Maximum path length is capped at `MAX_FUNCTOR_HOPS = 5` to bound runtime in pathological registries.

## Direct application after pathfinding

```
fn compose_seed(registry: &FunctorRegistry, source_seed: Seed, target: Domain) -> Result<Seed>:
    let path = find_path(registry, source_seed.domain(), target)
        .ok_or(Error::NoFunctorPath)?
    let mut current = source_seed
    let mut lineage_chain = []
    for functor in &path {
        let next = (functor.apply)(current)
        lineage_chain.push(LineageStep {
            functor_id: functor.id.clone(),
            input_hash: current.hash(),
            output_hash: next.hash(),
        })
        current = next
    }
    // Attach the lineage chain to the resulting seed.
    current.lineage.functor_chain = lineage_chain
    return Ok(current)
```

## Caching

Path lookups are cached because:

- The registry rarely changes (functors are added quarterly at most).
- Many users want the same `A → B` paths.

```
struct PathCache:
    cache: Map<(Domain, Domain), Option<[FunctorId]>>
    registry_version: int

fn cached_find_path(cache: &mut PathCache, registry: &FunctorRegistry,
                     source: Domain, target: Domain) -> Option<[Functor]>:
    if cache.registry_version != registry.version:
        cache.cache.clear()
        cache.registry_version = registry.version
    if let Some(cached) = cache.cache.get(&(source, target)):
        return cached.map(|ids| resolve_ids(registry, ids))
    let result = find_path(registry, source, target)
    cache.cache.insert((source, target), result.as_ref().map(|p| ids_of(p)))
    return result
```

The cache is a `(source × target) → path-of-ids` map. With ~25 domains, that's at most 625 entries; trivial.

## All shortest paths (for the studio gallery)

Sometimes the studio needs to show *every* way to get from `A` to `B`, ranked. This is a small modification of Dijkstra that yields the top-`k` paths via Yen's algorithm:

```
fn k_shortest_paths(registry: &FunctorRegistry, source: Domain, target: Domain, k: int)
    -> [Path]:
    let mut paths: [Path] = []
    let mut candidates: MinHeap<Path> = MinHeap::new()

    let first = find_path(registry, source, target)
    if first.is_none(): return []
    paths.push(first.unwrap())

    for i in 1..k:
        let prev = &paths[i - 1]
        for j in 0..prev.length:
            let spur_node = if j == 0 { source } else { prev[j - 1].target }
            // Build a temporary registry with the prev path's edges removed.
            let restricted = registry.without_edges(&prev[0..j])
            let spur_path = find_path(&restricted, spur_node, target)
            if spur_path.is_some():
                let mut total = prev[0..j].to_vec()
                total.extend(spur_path.unwrap())
                candidates.push(total)
        if candidates.is_empty(): break
        paths.push(candidates.pop().unwrap())

    return paths
```

## Determinism

- The MinHeap's strict ordering (with the lex-id tiebreak) makes Dijkstra deterministic.
- `find_path` returns the same path every time given the same registry version.
- The cache key includes the registry version, so updates invalidate cleanly.
- Pathfinding does *not* use the kernel RNG.

## Validation

After pathfinding, the result is validated:

1. Every functor in the path must be in the registry.
2. The path must form a valid chain (`functor[i].target == functor[i+1].source`).
3. The first functor's source must equal `source`; the last functor's target must equal `target`.
4. The path's total cost must equal the sum of its functors' individual costs.

These checks are performed in tests and at runtime in `cached_find_path`.

## Performance

- Registry size: ~9 functors today, target ~30 within 18 months.
- Domain count: ~25 today, ~50 in long-term roadmap.
- Dijkstra with 50 nodes and 30 edges runs in microseconds.
- Cache hit rate in production: >99.9% — only the first request for each (source, target) pair pays the pathfinding cost.

## Where it's used in Paradigm

- **Layer 5 evolution and composition** — every cross-domain seed transformation goes through this pathfinder.
- **Studio composition panel** — when the user drags a Sprite onto a Music workspace, the studio looks up the path.
- **Marketplace** — recommended derivations ("seeds you can make from this one") use `find_path` to enumerate reachable target domains.
- **Lineage propagation** — every step in the chain becomes a lineage edge with proper royalty attribution.

## References

- Dijkstra, *A Note on Two Problems in Connexion with Graphs* (Numerische Mathematik 1959)
- Yen, *Finding the K Shortest Loopless Paths in a Network* (Management Science 1971)
- Mac Lane, *Categories for the Working Mathematician* — for the category-theoretic backdrop on functors
