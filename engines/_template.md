# Engine Spec Template

> Copy this file when adding a new domain engine. Replace every `<placeholder>` with real content. Delete sections that don't apply but keep the section headings so all engine specs are uniformly navigable.

## Overview

A one-paragraph description of what the engine produces, who it's for, and what makes it different from a generic generator. Include the canonical artifact type (PNG, glTF, WAV, HTML5 zip, etc.).

## Gene Schema

| Gene Name | Type | Range / Constraint | Required | Description |
|---|---|---|---|---|
| `<gene_1>` | scalar | [0, 1] | yes | <what it controls> |
| `<gene_2>` | categorical | enum {a, b, c} | yes | <what it controls> |
| `<gene_3>` | vector(3) | each [0, 1] | yes | <what it controls> |
| `<gene_4>` | array | length 1..16 | no | <what it controls> |
| ... | ... | ... | ... | ... |

The full TypeScript schema lives in `engines/<domain>/schema.ts`.

## Stage Pipeline

```
1. extract        : <input type>  -> <output type>
2. <stage_2>      : <input type>  -> <output type>
3. <stage_3>      : <input type>  -> <output type>
...
N. export         : <input type>  -> Artifact
```

Total: N stages. The pipeline is fixed; stages are not skipped or reordered conditionally.

## Stage Details

### Stage 1 — `extract`

Read the gene table off the seed and convert to engine-internal working types.

```
fn extract(seed):
    return Working {
        <field_1>: seed.genes["<gene_1>"].value,
        <field_2>: seed.genes["<gene_2>"].value,
        ...
    }
```

### Stage 2 — `<stage_name>`

<one-paragraph description of what the stage does>

```
fn <stage_name>(input, seed, rng):
    <pseudocode>
    return <output>
```

(Repeat for each stage.)

### Stage N — `export`

Wrap the final intermediate state in the target format envelope.

```
fn export(state, seed, rng):
    return <artifact format wrapper>(state)
```

## Render Hints

```ts
const renderHints: RenderHints = {
  viewportMode: '<2d | 3d | audio | game | text>',
  defaultCamera: <camera config or null>,
  thumbnailSize: { width: 256, height: 256 },
  supportsAnimation: <true | false>,
};
```

## Export Hints

```ts
const exportHints: ExportHints = {
  formats: ['<format_1>', '<format_2>', ...],
  recommendedFormat: '<format>',
  containerOptions: { ... },
};
```

## Fitness Hints

```ts
const fitnessHints: FitnessHints = {
  meaningfulAxes: ['geometry', 'texture', '...'],  // QualityVector dimensions
  defaultDescriptors: ['<descriptor_1>', '<descriptor_2>'],  // for MAP-Elites
};
```

## Determinism Notes

- <Engine-specific determinism budget; cite spec/07-determinism.md per-engine table>
- <Floating-point hot spots and how they're handled>
- <GPU vs CPU parity tests>

## Validation Rules

`validate(seed)` checks:

- All required genes present.
- All gene values within declared ranges.
- <Engine-specific cross-gene constraints, e.g., "if gene_3 > 0.5 then gene_4 must be non-empty">
- <Output size bounds, e.g., "the resulting mesh must have ≤ 100k vertices">

## Anti-Patterns

- <Engine-specific things to avoid, e.g., "don't try to combine two body templates in morphogenesis — use cross-domain composition instead">

## References

- <Paper / library / prior art>
- <Paper / library / prior art>
