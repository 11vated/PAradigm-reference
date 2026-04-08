# 161 — Animation runtime namespace

## Question

How does GSPL equip the universal animation runtime — skeletal, sprite, blend trees, IK, root motion, retargeting — as a typed substrate namespace where every clip, blend, and pose is a signed gseed and animation events drive Brief 159 state transitions deterministically?

## Why it matters (blast radius)

Animation is the largest visual surface in a game and the largest source of "feels broken" bugs. Wrong root motion = floaty character. Wrong IK = foot through ground. Wrong blend = pop. Animation events firing in the wrong order = state stuck. Without a typed substrate runtime, every game writes its own animation state machine, IK solver, and event dispatcher, and bugs propagate through every Tier C tooling brief and every Tier E genre. Brief 161 equips the canonical runtime once.

## What we know from the spec

- Round 2 Brief 021 — sprite engine deep dive (the v0.1 default for character animation).
- Round 4 Brief 088 — character canon (Round 4 already specified character data; Brief 161 specifies how it animates at runtime).
- Brief 152 — fixed/variable tick split; animation runs on variable update with sampling at fixed-tick boundaries for events.
- Brief 153 — ECS animator component.
- Brief 159 — `behavior.animation_link` ties animation events to state transitions.
- Brief 131 — seven-axis claim; animation state is signed.

## Findings

1. **Three animation backbones ship at v0.1: sprite, 2D-skeletal, 3D-skeletal.** Sprite (frame-by-frame, sprite atlases) is the v0.1 default for the 2D-first scope. 2D-skeletal (Spine/DragonBones-class bone hierarchy) ships substrate. 3D-skeletal (mesh + skeleton) ships substrate but only Godot/Unity/Unreal export targets surface it at v0.1.

2. **Common abstraction: clips, blend trees, animator state.** Regardless of backbone, animation is authored as `animation.clip` gseeds (a sequence of poses + duration + events), composed via `animation.blend_tree` gseeds (parametric blending across clips), and stepped by an `animation.animator` ECS component (current state, blend weights, time, speed, layers).

3. **Animation events as signed gseeds.** A clip carries a list of `animation.event` markers at signed time offsets. Examples: `footstep_left`, `footstep_right`, `attack_hit`, `attack_recover`, `dialogue_continue`, `effect_spawn`, `state_exit`. When the animator's playhead crosses an event time, the event fires as a signed `animation.event.fired` gseed at the next fixed-tick boundary. Brief 159's `behavior.animation_link` subscribes.

4. **Blend trees are typed and parametric.** A blend tree node is `(type, parameters[], children[])` where type is `1d`, `2d_freeform`, `2d_directional`, or `additive`. Parameters reference ECS component values (e.g., `velocity.length`, `aim.angle`). Same-input determinism is preserved because parameters are read at fixed-tick boundaries.

5. **Root motion is opt-in per clip.** Default: animation does not move the entity (the gameplay code sets velocity, animation visualizes it). Opt-in: a clip can declare `root_motion = true`, and the animator extracts per-tick translation from the root bone and writes it to the entity's transform. Required for animation-driven games (Dark Souls-style melee, cinematic platformers).

6. **IK solvers ship as a substrate primitive.** Two solvers at v0.1: FABRIK (Forward And Backward Reaching Inverse Kinematics) for arbitrary chains, two-bone analytic for arms/legs. 3D-only at v0.1 (2D-skeletal can technically use FABRIK but the v0.1 sprite-default scope rarely needs it). Round 2 already covered IK at the substrate primitive level; Brief 161 binds it to the animator.

7. **Animation layers compose poses additively.** A character can have a base locomotion layer plus an upper-body action layer (e.g., walk while shooting). Layers blend with weights and masks (which bones each layer affects). Up to 4 layers per animator at v0.1. This is the consensus pattern from Unity Mecanim and Unreal anim graphs.

8. **Sprite atlas packing is signed.** The Tier C Brief 179 animation editor authors the atlas; the runtime reads a signed `animation.sprite_atlas` gseed mapping clip frames to atlas regions. Pack changes invalidate the gseed, propagating per Brief 147 federation review.

9. **Animation retargeting at v0.1 (2D-skeletal only) and v0.4 (3D).** A `animation.retarget_map` gseed lets a clip authored for one skeleton play on another with compatible bone roles. v0.1 ships retargeting for 2D-skeletal so creators can swap sprite skins on shared rigs. 3D retargeting (humanoid skeleton → humanoid skeleton) ships at v0.4.

10. **Animation determinism across replays.** Per Brief 152, variable-update animation interpolates between fixed-tick samples using the deterministic accumulator. Same input + same fixed-tick state = same animator state every frame. Variable-rate refresh changes interpolation count but not state-at-tick-boundary.

11. **Performance.** v0.1 budgets animation at 2ms variable + 1ms fixed for: 200 active animators on the hardware floor for 2D sprite, 50 for 2D-skeletal, 20 for 3D-skeletal. Brief 134 canonical battery validates.

12. **Animation cancel windows are typed.** A clip can declare `cancel_windows[]` — time ranges during which a state transition is allowed (e.g., the recovery frames of an attack are cancelable into a dodge). The behavior layer (Brief 159) reads the windows when evaluating transition conditions. This is the structural fighting-game / character-action substrate.

13. **Differentiable animation parameters.** Blend tree parameter weights, IK solver settings, layer mask configurations tuned by creators and accepted via the drift detector become genre-default suggestions. Per-archetype animation starter packs propagate via federation. Brief 143 axis at the animation layer.

## Risks identified

- **3D-skeletal animation is hard and v0.1's 2D-first scope leaves it under-tested.** Mitigation: v0.1 ships substrate but documents that 3D animation is "preview"; full QA at v0.4.
- **Root motion conflicts with kinematic-physics character controllers.** Mitigation: explicit opt-in per clip; conflict surfaced in scene-compile when both are enabled on the same entity.
- **Animation events fired across slow ticks can fire multiple times.** Mitigation: scheduler tracks `last_event_index` per layer; on tick catch-up, intermediate events fire in order; signed.
- **Blend tree parameters can become high-dimensional and hard to author.** Mitigation: ship `1d`, `2d_freeform`, `2d_directional` as the canonical types; higher-dimensional blends are deferred to Round 8.
- **Sprite atlas packing changes invalidate every dependent gseed (cascade).** Mitigation: atlas changes propagate as a single signed `atlas.repack` event; downstream gseeds reference the atlas by hash, not by frame index.

## Recommendation

**GSPL ships an `animation` namespace at v0.1 with three backbones (sprite-default / 2D-skeletal / 3D-skeletal-preview), unified abstraction over clips, blend trees, animator components, and animation events; signed event firing on fixed-tick boundaries; parametric blend tree types (1d / 2d_freeform / 2d_directional / additive); opt-in root motion; FABRIK + two-bone IK from Round 2 substrate; up to 4 additive layers per animator with bone masks; signed sprite atlas packing; 2D-skeletal retargeting at v0.1 and 3D at v0.4; deterministic variable-update interpolation against fixed-tick samples; ~200/50/20 animator capacity on the hardware floor by backbone; signed cancel windows on clips for fighting-game / character-action transitions; and creator-tuned animation parameters propagating via the Differentiable axis.**

## Confidence

**4/5.** The architecture is the synthesis of Unity Mecanim, Unreal anim graph, Spine 2D, Godot AnimationTree, and Spine/DragonBones runtime patterns. All proven. The 5th confidence point waits on Brief 134 measuring 200-active-sprite-animator throughput on the hardware floor.

## Spec impact

- `gspl-reference/namespaces/animation.md` — new namespace
- `gspl-reference/research/152-game-loop-tick-model-namespace.md` — variable-update animation interpolation
- `gspl-reference/research/153-ecs-substrate-binding.md` — `animator` component
- `gspl-reference/research/159-state-machines-and-behavior-trees.md` — animation_link integration
- `gspl-reference/research/021-sprite-engine-deep-dive.md` — sprite backbone implementation
- `gspl-reference/research/088-character-canon.md` — character canon data feeds animator
- `gspl-reference/research/134-substrate-native-benchmark-battery.md` — animation battery
- Tier C Brief 179 — animation editor authors clips/atlases
- Tier D Brief 195 — Spine/DragonBones runtime export

## New inventions

- **INV-640** — *Three-backbone unified animation runtime* (sprite/2D-skel/3D-skel) under one signed namespace with shared event/blend/layer semantics.
- **INV-641** — *Signed cancel windows on clips* — fighting-game and character-action transition timing equipped as substrate, not per-game scripting.
- **INV-642** — *Bone-masked additive layers up to 4 deep* with signed weights — locomotion + upper-body + face + facial-emotion compositions out of the box.
- **INV-643** — *Animation event determinism on tick catch-up* — intermediate events fire in order even when the scheduler catches up multiple ticks per render frame, preserving Brief 152's fairness contract.
- **INV-644** — *Sprite atlas packing as signed gseed with hash-stable references* — atlas repack changes one root signature, downstream gseeds remain valid via content-addressed reference.

## Open follow-ups

- Whether facial blendshapes ship at v0.1 (sprite-only at v0.1; 3D facial defer to v0.4 with character canon expansion).
- Procedural animation primitives (cloth, hair, secondary motion) — defer to Round 8; substrate already has Verlet primitives from Round 2.
- Animation compression formats — defer to Tier D export pipeline briefs.

## Sources

- Brief 131 — seven-axis structural claim
- Brief 134 — substrate-native benchmark battery
- Brief 143 — differentiable action learning recipe
- Brief 147 — federation-wide adapter review protocol
- Brief 152 — game loop and tick model namespace
- Brief 153 — ECS substrate binding
- Brief 159 — state machines and behavior trees
- Round 2 Brief 021 — sprite engine deep dive
- Round 4 Brief 088 — character canon
- Spine animation runtime documentation
- DragonBones runtime documentation
- Unity Mecanim documentation (animator state machines, blend trees, layers)
- Unreal Anim Graph / Anim Blueprint documentation
- Aristidou & Lasenby, "FABRIK: A fast, iterative solver for the Inverse Kinematics problem"
