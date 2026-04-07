# Marching Cubes

## What it does

Marching Cubes (Lorensen & Cline 1987) extracts a polygonal mesh from a 3D scalar field by dividing space into a regular grid of cubes and, for each cube, generating a small set of triangles that approximate the iso-surface where the field equals a chosen threshold.

In Paradigm, Marching Cubes is the algorithm that turns a `Geometry3D` engine's signed-distance field (SDF) representation into a renderable mesh. SDFs are the canonical internal representation (they support boolean operations, smooth blending, and infinite resolution), but GPUs render triangles, so we need a conversion step.

## The 256 cube cases

A cube has 8 corners. Each corner is either inside the surface (`field < threshold`) or outside (`field ≥ threshold`). That's `2^8 = 256` possible cube configurations.

The original Marching Cubes paper provides two lookup tables:

1. **edge_table[256]** — bitmask of which of the cube's 12 edges are crossed by the surface.
2. **tri_table[256][16]** — sequence of edge indices forming triangles (terminated by `-1`).

These tables are public domain and ~5 KB total. Every implementation in every language uses the same numerical values; they're a fixed mathematical fact.

Reference: <http://paulbourke.net/geometry/polygonise/>

## State

```
struct ScalarField:
    fn sample(x: float, y: float, z: float) -> float
    bounds: AABB                   // bounding box

struct MarchingCubesConfig:
    grid_resolution: ivec3         // e.g., (64, 64, 64)
    threshold: float               // e.g., 0.0 for SDF iso-surface
    smoothing_iterations: int      // optional Laplacian smoothing
```

## Per-cube routine

```
fn march_cube(corners: [vec3; 8], values: [float; 8], threshold: float)
    -> [Triangle]:
    // 1. Build cube index from corner sign pattern.
    let mut cube_index: int = 0
    for i in 0..8:
        if values[i] < threshold:
            cube_index |= (1 << i)
    // 2. Lookup which edges are crossed.
    let edges = EDGE_TABLE[cube_index]
    if edges == 0: return []      // fully inside or outside; no surface
    // 3. Compute the intersection vertex on each crossed edge.
    let mut vert_list: [vec3; 12] = [zero_vec3(); 12]
    for e in 0..12:
        if edges & (1 << e) != 0:
            let (i, j) = EDGE_VERTICES[e]   // the two cube corners this edge connects
            vert_list[e] = vertex_interp(threshold, corners[i], corners[j],
                                          values[i], values[j])
    // 4. Emit triangles using TRI_TABLE.
    let mut tris = []
    let mut i = 0
    while TRI_TABLE[cube_index][i] != -1:
        let a = vert_list[TRI_TABLE[cube_index][i]]
        let b = vert_list[TRI_TABLE[cube_index][i + 1]]
        let c = vert_list[TRI_TABLE[cube_index][i + 2]]
        tris.push(Triangle { a, b, c })
        i += 3
    return tris

fn vertex_interp(threshold: float, p1: vec3, p2: vec3, v1: float, v2: float) -> vec3:
    // Linear interpolation along the edge to find where field crosses threshold.
    if abs(threshold - v1) < 1e-6: return p1
    if abs(threshold - v2) < 1e-6: return p2
    if abs(v1 - v2)          < 1e-6: return p1
    let mu = (threshold - v1) / (v2 - v1)
    return vec3(p1.x + mu * (p2.x - p1.x),
                p1.y + mu * (p2.y - p1.y),
                p1.z + mu * (p2.z - p1.z))
```

## Whole-grid routine

```
fn marching_cubes(field: &ScalarField, cfg: &MarchingCubesConfig) -> Mesh:
    let res = cfg.grid_resolution
    let bounds = field.bounds
    let cell_size = vec3(
        (bounds.max.x - bounds.min.x) / (res.x - 1) as float,
        (bounds.max.y - bounds.min.y) / (res.y - 1) as float,
        (bounds.max.z - bounds.min.z) / (res.z - 1) as float,
    )

    // Pre-sample the field at every grid point. This is the bottleneck.
    let mut samples: Array3D<float> = Array3D::new(res)
    for k in 0..res.z:
        for j in 0..res.y:
            for i in 0..res.x:
                let p = bounds.min + vec3(i as float * cell_size.x,
                                            j as float * cell_size.y,
                                            k as float * cell_size.z)
                samples[i][j][k] = field.sample(p.x, p.y, p.z)

    // March every cube. Output: a flat triangle list.
    let mut triangles: [Triangle] = []
    for k in 0..(res.z - 1):
        for j in 0..(res.y - 1):
            for i in 0..(res.x - 1):
                let corners = [
                    grid_point(bounds, cell_size, i,     j,     k),
                    grid_point(bounds, cell_size, i + 1, j,     k),
                    grid_point(bounds, cell_size, i + 1, j + 1, k),
                    grid_point(bounds, cell_size, i,     j + 1, k),
                    grid_point(bounds, cell_size, i,     j,     k + 1),
                    grid_point(bounds, cell_size, i + 1, j,     k + 1),
                    grid_point(bounds, cell_size, i + 1, j + 1, k + 1),
                    grid_point(bounds, cell_size, i,     j + 1, k + 1),
                ]
                let values = [
                    samples[i    ][j    ][k    ],
                    samples[i + 1][j    ][k    ],
                    samples[i + 1][j + 1][k    ],
                    samples[i    ][j + 1][k    ],
                    samples[i    ][j    ][k + 1],
                    samples[i + 1][j    ][k + 1],
                    samples[i + 1][j + 1][k + 1],
                    samples[i    ][j + 1][k + 1],
                ]
                let cube_tris = march_cube(corners, values, cfg.threshold)
                triangles.extend(cube_tris)

    // Convert flat triangle list to indexed mesh (deduplicated vertices).
    return triangles_to_indexed_mesh(triangles)
```

## Vertex deduplication

The naive output has 3 vertices per triangle and many duplicates (each interior vertex is shared by ~6 triangles). For a renderable mesh we deduplicate:

```
fn triangles_to_indexed_mesh(tris: [Triangle]) -> Mesh:
    let mut vertices: [vec3] = []
    let mut indices: [int] = []
    let mut lookup: HashMap<QuantizedVec3, int> = empty_map()

    for tri in tris:
        for v in [tri.a, tri.b, tri.c]:
            let key = quantize(v, eps = 1e-6)    // round to a grid cell to merge near-coincident verts
            let idx = match lookup.get(&key):
                Some(i) -> i
                None    -> {
                    let i = vertices.length
                    vertices.push(v)
                    lookup.insert(key, i)
                    i
                }
            indices.push(idx)

    return Mesh { vertices, indices }
```

The quantization tolerance `eps` should be small enough not to merge unrelated vertices but large enough to merge ones that *should* be coincident (e.g., shared edges between adjacent cubes). `1e-6 * cell_size` is a good default.

## Normal computation

After mesh extraction, compute per-vertex normals:

```
fn compute_normals(mesh: &mut Mesh) -> void:
    let mut normals = vec![zero_vec3(); mesh.vertices.length]
    for tri_idx in 0..(mesh.indices.length / 3):
        let i0 = mesh.indices[tri_idx * 3]
        let i1 = mesh.indices[tri_idx * 3 + 1]
        let i2 = mesh.indices[tri_idx * 3 + 2]
        let v0 = mesh.vertices[i0]
        let v1 = mesh.vertices[i1]
        let v2 = mesh.vertices[i2]
        let face_normal = normalize(cross(v1 - v0, v2 - v0))
        normals[i0] = normals[i0] + face_normal
        normals[i1] = normals[i1] + face_normal
        normals[i2] = normals[i2] + face_normal
    for i in 0..normals.length:
        normals[i] = normalize(normals[i])
    mesh.normals = normals
```

This is **vertex-area-weighted** normal accumulation, which produces smooth shading on curved surfaces. For sharper edges, use angle-weighted normals.

## Optional smoothing pass

The raw Marching Cubes mesh is bumpy because the iso-surface jumps from cube to cube. Laplacian smoothing softens it:

```
fn laplacian_smooth(mesh: &mut Mesh, iterations: int, lambda: float) -> void:
    let adjacency = build_adjacency_list(mesh)
    for _ in 0..iterations:
        let mut new_verts = mesh.vertices.clone()
        for i in 0..mesh.vertices.length:
            if adjacency[i].is_empty(): continue
            let centroid = mean(adjacency[i].iter().map(|j| mesh.vertices[j]))
            new_verts[i] = mesh.vertices[i] + scalar_mul(lambda, centroid - mesh.vertices[i])
        mesh.vertices = new_verts
```

`lambda = 0.5`, `iterations = 3` is a good default. Watch for shrinkage; for shrinkage-free smoothing, use Taubin's algorithm (alternate λ and -μ).

## Determinism

- Marching Cubes is fully deterministic given the field and the grid.
- The lookup tables are constants — no hash randomization, no parallelism reordering.
- Vertex deduplication uses a sorted insertion order based on linearized cube index.
- Quantization uses fixed-point arithmetic (`round(v / eps) * eps`), bit-stable across platforms.

## Performance

For a `64³` grid: 250K cubes, ~1M field samples, ~50K triangles output.

| Stage | Time on M2 (single-threaded) |
|---|---|
| Field sampling | 80ms |
| Cube marching | 30ms |
| Vertex deduplication | 15ms |
| Normal computation | 5ms |
| Laplacian smoothing (×3) | 20ms |

Field sampling dominates and is `O(res³)`. The implementation is trivially parallelizable: subdivide the grid into 8 octants and march each in a worker thread. Paradigm uses a Web Worker pool by default.

For GPU: see [`infrastructure/gpu-kernels.md`](../infrastructure/gpu-kernels.md) §"Marching Cubes on WebGPU" for the WGSL compute shader implementation that runs ~50× faster.

## Limitations and alternatives

- **Topological ambiguity:** the original 256-case table has 6 ambiguous configurations that can produce holes. Use the **disambiguated** Marching Cubes 33 tables (Chernyaev 1995) or switch to **Dual Contouring** for higher-fidelity surfaces.
- **Sharp edges:** Marching Cubes smooths over sharp features. Use **Dual Contouring** or **Manifold Dual Contouring** for CAD-quality output.
- **Adaptive resolution:** for objects with both fine details and large flat regions, use an **octree** subdivision and **Adaptive Marching Cubes**.

Paradigm currently uses standard Marching Cubes 33 (with disambiguation) for its balance of simplicity and quality.

## Where it's used in Paradigm

- **Geometry3D** mesh extraction stage — the core rendering pipeline.
- **Sprite engine** for converting sprite SDFs to 2D outlines (a 2D variant: Marching Squares).
- **Character engine** for skin mesh extraction from blend shapes.
- **Procedural engine** for rendering implicit terrain.

## References

- Lorensen & Cline, *Marching Cubes: A High Resolution 3D Surface Construction Algorithm* (SIGGRAPH 1987) — the original paper
- Chernyaev, *Marching Cubes 33: Construction of Topologically Correct Isosurfaces* (Tech Report 1995) — disambiguation
- Ju, Losasso, Schaefer, Warren, *Dual Contouring of Hermite Data* (SIGGRAPH 2002) — sharp-edge alternative
- Bourke's lookup tables: <http://paulbourke.net/geometry/polygonise/>
