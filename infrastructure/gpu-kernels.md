# GPU Kernels

## Why GPU

A handful of operations in Paradigm are too expensive to run on CPU at the rates we need:

- **Marching Cubes** on 256³ scalar fields for sculpt/voxel/terrain engines.
- **Particle simulation** for the Particles, Weather, and Fluids engines (>100K particles).
- **Image-space style transfer** and OKLab color operations on 4K atlases.
- **Vector similarity** for archive nearest-neighbor queries in MAP-Elites and AURORA.
- **Convolutional encoders** for AURORA descriptor learning.
- **Verlet physics** for hair, cape, and cloth.

These run as **WGSL compute shaders** dispatched via `wgpu` (Rust) or WebGPU (browser preview). Both backends consume the *same* WGSL source — we never fork shaders per platform.

## Determinism on GPU

GPU execution is the **only** place in the deterministic stack where we tolerate floating-point reordering. Even there, we constrain it:

1. **No atomic floats.** Atomic accumulation introduces order-dependence on `f32`. When summation is needed (e.g., reductions), we use parallel-prefix-sum patterns with explicit barriers.
2. **Workgroup sizes are fixed in source.** No dynamic dispatch sizing.
3. **Same driver version → same output.** We pin Mesa, Vulkan loader, and the wgpu adapter selection in CI. Production runs only on a known set of GPUs (NVIDIA A10G / L4 / L40S, or CPU fallback via lavapipe).
4. **CPU validation pass.** Every GPU kernel has a reference CPU implementation in Rust used in tests; outputs must match within `1e-6` relative error.
5. **Hashing the output.** Engine outputs that pass through GPU stages have their final hash computed *after* a deterministic CPU normalization pass (e.g., quantize positions to `f32` with fixed rounding).

The result: GPU kernels are deterministic *as a black box*, even though their internals reorder operations.

## Kernel inventory

| Kernel | Engines | Workgroup | Approx cost (A10G) |
|---|---|---|---|
| `marching_cubes` | Sculpt, Voxel, Terrain | 4×4×4 | ~5ms for 128³, ~40ms for 256³ |
| `verlet_step` | Physics, Cloth, Hair | 64 | ~0.2ms for 10K particles |
| `particle_advect` | Particles, Weather, Fluids | 64 | ~0.3ms for 100K particles |
| `oklab_recolor` | Sprite, Texture | 8×8 | ~1ms for 1024² |
| `style_blend` | Sprite, Animation | 8×8 | ~3ms for 2048² |
| `vector_topk` | Archive query | 64 | ~0.5ms for 100K vectors |
| `conv_encoder` | AURORA | 16×16 | ~8ms for 64×64 input |
| `cloth_constraint` | Cloth | 64 | ~0.4ms for 32×32 cloth |

## Marching Cubes on WebGPU

The reference WGSL kernel for the Marching Cubes algorithm described in `algorithms/marching-cubes.md`. The kernel runs in two passes:

1. **Pass 1: cube classification.** For each cube, compute the 8-corner classification index and emit a triangle count (look up in `tri_count_table`).
2. **Prefix sum** over triangle counts to get global write offsets.
3. **Pass 2: triangle generation.** Each cube writes its triangles into the global vertex buffer at its prefix-sum offset.

### Bindings

```wgsl
struct Params {
    grid_dim:    vec3<u32>,
    iso:         f32,
    cell_size:   f32,
    origin:      vec3<f32>,
    _pad:        f32,
};

@group(0) @binding(0) var<uniform> params: Params;
@group(0) @binding(1) var<storage, read>  field:        array<f32>;
@group(0) @binding(2) var<storage, read>  edge_table:   array<u32, 256>;
@group(0) @binding(3) var<storage, read>  tri_table:    array<i32, 4096>;   // 256 * 16
@group(0) @binding(4) var<storage, read>  tri_count_table: array<u32, 256>;
@group(0) @binding(5) var<storage, read_write> tri_counts: array<atomic<u32>>;
@group(0) @binding(6) var<storage, read_write> vertices:   array<vec4<f32>>;
@group(0) @binding(7) var<storage, read_write> normals:    array<vec4<f32>>;
@group(0) @binding(8) var<storage, read>  cube_offsets:   array<u32>;       // prefix sum from CPU
```

### Pass 1: classify

```wgsl
@compute @workgroup_size(4, 4, 4)
fn classify(@builtin(global_invocation_id) gid: vec3<u32>) {
    if (any(gid >= params.grid_dim - vec3<u32>(1u))) { return; }
    let cube_idx = gid.x + gid.y * params.grid_dim.x +
                   gid.z * params.grid_dim.x * params.grid_dim.y;
    let v = sample_corners(gid);
    var classification: u32 = 0u;
    for (var i: u32 = 0u; i < 8u; i = i + 1u) {
        if (v[i] < params.iso) { classification = classification | (1u << i); }
    }
    let count = tri_count_table[classification];
    atomicStore(&tri_counts[cube_idx], count);
}
```

`sample_corners` reads the eight scalar values at the cube's eight corners from the `field` storage buffer. The exact corner ordering matches the CPU reference (see `algorithms/marching-cubes.md`).

### Pass 2: generate

After CPU computes the prefix sum of `tri_counts` into `cube_offsets`, pass 2 emits triangles:

```wgsl
@compute @workgroup_size(4, 4, 4)
fn generate(@builtin(global_invocation_id) gid: vec3<u32>) {
    if (any(gid >= params.grid_dim - vec3<u32>(1u))) { return; }
    let cube_idx = gid.x + gid.y * params.grid_dim.x +
                   gid.z * params.grid_dim.x * params.grid_dim.y;
    let v        = sample_corners(gid);
    let p        = corner_positions(gid);
    var classification: u32 = 0u;
    for (var i: u32 = 0u; i < 8u; i = i + 1u) {
        if (v[i] < params.iso) { classification = classification | (1u << i); }
    }
    if (classification == 0u || classification == 255u) { return; }

    let edges = edge_table[classification];
    var verts: array<vec3<f32>, 12>;
    for (var e: u32 = 0u; e < 12u; e = e + 1u) {
        if ((edges & (1u << e)) != 0u) {
            let a = EDGE_CORNERS[e].x;
            let b = EDGE_CORNERS[e].y;
            verts[e] = vertex_interp(params.iso, p[a], p[b], v[a], v[b]);
        }
    }

    let base = cube_offsets[cube_idx];
    var local: u32 = 0u;
    for (var i: u32 = 0u; i < 16u; i = i + 3u) {
        let i0 = tri_table[classification * 16u + i];
        if (i0 < 0) { break; }
        let i1 = tri_table[classification * 16u + i + 1u];
        let i2 = tri_table[classification * 16u + i + 2u];
        let v0 = verts[i0];
        let v1 = verts[i1];
        let v2 = verts[i2];
        let n  = normalize(cross(v1 - v0, v2 - v0));
        vertices[(base + local + 0u)] = vec4<f32>(v0, 1.0);
        vertices[(base + local + 1u)] = vec4<f32>(v1, 1.0);
        vertices[(base + local + 2u)] = vec4<f32>(v2, 1.0);
        normals[(base + local + 0u)]  = vec4<f32>(n, 0.0);
        normals[(base + local + 1u)]  = vec4<f32>(n, 0.0);
        normals[(base + local + 2u)]  = vec4<f32>(n, 0.0);
        local = local + 3u;
    }
}
```

`vertex_interp` is the linear interpolation between cube corners; it must use the *same* arithmetic order as the CPU reference to satisfy bit-for-bit equivalence under fixed inputs.

## Verlet step

```wgsl
struct Particle {
    pos:     vec3<f32>,
    inv_mass: f32,
    prev:    vec3<f32>,
    pinned:  u32,
};

@group(0) @binding(0) var<storage, read_write> particles: array<Particle>;
@group(0) @binding(1) var<uniform> params: VerletParams;

@compute @workgroup_size(64)
fn verlet_step(@builtin(global_invocation_id) gid: vec3<u32>) {
    let i = gid.x;
    if (i >= arrayLength(&particles)) { return; }
    var p = particles[i];
    if (p.pinned == 1u) { return; }
    let velocity = (p.pos - p.prev) * params.damping;
    let new_pos  = p.pos + velocity + params.gravity * params.dt * params.dt;
    p.prev = p.pos;
    p.pos  = new_pos;
    particles[i] = p;
}
```

Constraint solving runs in a separate kernel and is iterated `params.iterations` times (default 8).

## Particle advection

For the Particles engine and Weather engine. Particles are stored in a flat array; the kernel updates position from velocity and an external force field.

```wgsl
@compute @workgroup_size(64)
fn particle_advect(@builtin(global_invocation_id) gid: vec3<u32>) {
    let i = gid.x;
    if (i >= arrayLength(&particles)) { return; }
    var p = particles[i];
    if (p.life <= 0.0) { return; }
    let force = sample_force_field(p.pos);
    p.vel = p.vel + (force * p.inv_mass) * params.dt;
    p.vel = p.vel * params.drag;
    p.pos = p.pos + p.vel * params.dt;
    p.life = p.life - params.dt;
    particles[i] = p;
}
```

## OKLab recolor

Used by Sprite and Texture engines for palette swaps that preserve perceptual brightness.

```wgsl
@compute @workgroup_size(8, 8)
fn oklab_recolor(@builtin(global_invocation_id) gid: vec3<u32>) {
    let dim = textureDimensions(input);
    if (gid.x >= dim.x || gid.y >= dim.y) { return; }
    let rgba = textureLoad(input, vec2<i32>(gid.xy), 0);
    let oklab = linear_srgb_to_oklab(rgba.rgb);
    let shifted = vec3<f32>(oklab.x, oklab.y * params.chroma_scale, oklab.z + params.hue_shift);
    let out = oklab_to_linear_srgb(shifted);
    textureStore(output, vec2<i32>(gid.xy), vec4<f32>(out, rgba.a));
}
```

`linear_srgb_to_oklab` and its inverse follow Björn Ottosson's published reference equations exactly. We do not vary the matrix coefficients.

## Vector top-k

Brute-force k-NN for archives below 100K vectors. Above that, we switch to HNSW (CPU-side, via pgvector or Qdrant).

```wgsl
@compute @workgroup_size(64)
fn vector_topk(@builtin(global_invocation_id) gid: vec3<u32>) {
    let i = gid.x;
    if (i >= params.archive_size) { return; }
    let v = archive[i];
    let q = query;
    var sum: f32 = 0.0;
    for (var d: u32 = 0u; d < params.dim; d = d + 1u) {
        let diff = v[d] - q[d];
        sum = sum + diff * diff;
    }
    distances[i] = sum;
}
```

A second CPU pass partial-sorts `distances` and returns the top-k indices. We chose this two-stage approach because GPU partial-sort is bounded by workgroup size and would require multiple dispatches; the partial sort on CPU after a fast GPU distance pass is a good Pareto point up to ~1M vectors.

## Cloth constraint solver

Iterative constraint relaxation. Each constraint is a spring; constraints are partitioned into 4 colors so each color can be solved in parallel without write conflicts.

```wgsl
@compute @workgroup_size(64)
fn cloth_constraint(@builtin(global_invocation_id) gid: vec3<u32>) {
    let i = gid.x;
    if (i >= params.constraint_count) { return; }
    let c = constraints[i];
    if (c.color != params.current_color) { return; }
    var pa = particles[c.a].pos;
    var pb = particles[c.b].pos;
    let delta = pb - pa;
    let dist = length(delta);
    if (dist < 1e-6) { return; }
    let correction = ((dist - c.rest) / dist) * 0.5 * delta;
    if (particles[c.a].inv_mass > 0.0) { particles[c.a].pos = pa + correction; }
    if (particles[c.b].inv_mass > 0.0) { particles[c.b].pos = pb - correction; }
}
```

Each iteration dispatches the kernel four times (once per color).

## Convolutional encoder (AURORA)

The autoencoder used by AURORA to learn descriptors. We compile a small fixed-architecture CNN to WGSL via a custom transpiler. The encoder is 4 conv layers + 2 dense layers, total ~0.5M params, runs on the GPU as 6 dispatches per forward pass.

```wgsl
@compute @workgroup_size(16, 16)
fn conv_layer(@builtin(global_invocation_id) gid: vec3<u32>) {
    let oy = gid.y;
    let ox = gid.x;
    let oc = gid.z;
    if (oy >= params.out_h || ox >= params.out_w || oc >= params.out_c) { return; }
    var sum: f32 = bias[oc];
    for (var ic: u32 = 0u; ic < params.in_c; ic = ic + 1u) {
        for (var ky: u32 = 0u; ky < params.kernel; ky = ky + 1u) {
            for (var kx: u32 = 0u; kx < params.kernel; kx = kx + 1u) {
                let iy = oy * params.stride + ky;
                let ix = ox * params.stride + kx;
                let in_idx     = ((iy * params.in_w) + ix) * params.in_c + ic;
                let weight_idx = (((oc * params.in_c) + ic) * params.kernel + ky) * params.kernel + kx;
                sum = sum + input[in_idx] * weights[weight_idx];
            }
        }
    }
    let act = max(sum, 0.0);   // ReLU
    let out_idx = ((oy * params.out_w) + ox) * params.out_c + oc;
    output[out_idx] = act;
}
```

Backpropagation is **CPU-side** in Rust using `burn` — the encoder is small enough that retraining the AURORA encoder on CPU is acceptable, and avoiding GPU backprop avoids a large class of nondeterminism.

## Pipeline cache

WGSL modules are compiled once at engine start and cached in a `wgpu::PipelineCache`. The cache key is the SHA-256 of the WGSL source plus the wgpu version. Cache hits skip shader compilation entirely; this drops engine cold-start from ~400ms to ~20ms.

## Fallback path

If the host has no GPU (CI runners, edge nodes), the engine falls back to a CPU implementation of every kernel. The CPU paths are slower (typically 20-50×) but produce *bit-identical* output. This guarantees we can always reproduce a seed regardless of hardware.

The dispatch decision is made at engine init:

```rust
let backend = if has_compatible_gpu() && !env::var("PARADIGM_FORCE_CPU").is_ok() {
    Backend::Gpu(init_wgpu().await?)
} else {
    Backend::Cpu
};
```

## References

- *Marching Cubes: A High Resolution 3D Surface Construction Algorithm* — Lorensen & Cline 1987
- *A Simple Time-Corrected Verlet Integration Method* — Jakobsen 2001
- Björn Ottosson, *A perceptual color space for image processing* (OKLab)
- *wgpu* — https://wgpu.rs (Rust WebGPU implementation)
- WebGPU specification — https://www.w3.org/TR/webgpu/
- WGSL specification — https://www.w3.org/TR/WGSL/
