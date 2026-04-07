# Examples

This directory contains worked examples that exercise the full stack: GSPL source files, the seeds they produce, and the engine outputs they evaluate to. They are the canonical "by example" reference for anyone reading this repo.

| File | What it shows |
|---|---|
| [`melancholy_bard.gspl`](melancholy_bard.gspl) | The canonical sprite-creation example used throughout the docs |
| [`melancholy_bard.gseed.json`](melancholy_bard.gseed.json) | The signed seed JSON that `melancholy_bard.gspl` evaluates to |
| [`forest_cathedral.gspl`](forest_cathedral.gspl) | Composite scene: character + environment + ambient music |
| [`fierce_warrior.gspl`](fierce_warrior.gspl) | Variation example: same template, opposite axis |
| [`tiling_brick_wall.gspl`](tiling_brick_wall.gspl) | Texture engine example with procedural tiling |
| [`drum_loop.gspl`](drum_loop.gspl) | Music engine: 8-bar deterministic drum loop |
| [`stone_idol.gspl`](stone_idol.gspl) | Sculpt engine: SDF + Marching Cubes mesh |
| [`evolution_run.gspl`](evolution_run.gspl) | MAP-Elites loop seeded from `melancholy_bard` |
| [`functor_sprite_to_music.gspl`](functor_sprite_to_music.gspl) | Cross-domain functor application |

## How to read these

Every `.gspl` file follows the structure described in `language/`. They use the standard library prefixes (`Std.*`, `Sprite.*`, etc.) and produce typed seeds via the `seed { ... }` constructor. Comments explain *why*, not what.

Every `.gseed.json` file is the canonical JSON form of a signed seed — what the engine actually consumes, what gets hashed, and what the marketplace stores. The signature and key id at the bottom are real-shaped (P-256 ECDSA / RFC 7638 thumbprint) but use deterministic test keys, not production keys.

## Reproducibility

All examples in this directory are reproducible bit-for-bit:

```bash
gspl run examples/melancholy_bard.gspl > out.gseed
sha256sum out.gseed
# 8f3a... (matches the value embedded in the file's header comment)
```

The expected hash is recorded in a header comment in each `.gspl` file. CI verifies on every commit that the expected hash still matches the produced hash. A drift in any example means a regression somewhere in the deterministic stack.

## Adding examples

When adding a new example:

1. Write the `.gspl` source.
2. Run it through the compiler and capture the seed JSON and hash.
3. Add the hash as a header comment in the `.gspl` file.
4. Add a row to the table above with a one-line description.
5. Add a regression test in CI that re-runs the example and checks the hash.
