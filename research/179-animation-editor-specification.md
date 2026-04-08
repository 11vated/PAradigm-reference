# 179 — Animation editor specification

## Question
What is the creator-facing animation editor surface that authors `animation.clip`, `animation.blend_tree`, and `animation.skeleton` (Brief 161) gseeds with timeline scrubbing, IK rigging, and deterministic preview?

## Why it matters (blast radius)
Animation is the bridge between sprite/mesh authoring and runtime motion. If the editor's preview does not match the runtime sampler, every animator ships visual bugs they can't see until export. If the timeline does not commit atomically, scrubbing produces lineage spam. If 2D sprite, 3D skeletal, and IK rig editing are three different surfaces, the substrate looks fragmented at the highest-stakes creator surface.

## What we know from the spec
- Brief 161 — `animation.clip`, `animation.blend_tree`, `animation.skeleton`, root motion, retargeting, IK.
- Brief 021 — sprite engine deep dive.
- Brief 177 — modifier-surface contract.
- Brief 052 — lineage time machine.
- Round 2 IK briefs (FABRIK / CCD).

## Findings
1. **Unified timeline.** A single typed `animation.timeline` editor view edits 2D sprite clips, 3D skeletal clips, and any other Brief 161 animation primitive. The timeline is parameterized over the channel type (sprite-frame, transform, blend-shape, material-property, event) and the editor swaps the keyframe widget per channel type. There is no separate "sprite animator" and "skeletal animator" surface.
2. **Keyframe as typed mutation.** Adding/moving/deleting a keyframe is one signed mutation per commit boundary. Mouse-drag scrubbing of a key emits one mutation on mouse-up. Curve editing (tangent handles) is one mutation per handle drag.
3. **Curve types.** v0.1 ships seven curve types per Brief 161: step / linear / cubic-hermite / bezier / catmull-rom / quaternion-slerp / cubic-spline-quaternion. Each curve type is a typed enum on the channel; the editor renders the appropriate widget.
4. **Preview = runtime.** The animation preview uses the same sampler the runtime uses. Scrubbing the timeline calls the runtime sampler at the displayed time, with the same fixed-tick semantics from Brief 152. There is no editor approximation.
5. **Skeleton rigging.** A `animation.skeleton` gseed is edited via a hierarchical bone tree view. Adding a bone is a typed mutation; setting parent, length, rest pose, and IK chain attachment are typed mutations. Bone limits (per Brief 161 IK constraints) are sign-time validated.
6. **IK editor.** IK chains are edited as a typed `animation.ik_chain` gseed referencing root and effector bone IDs and the solver type (FABRIK/CCD/analytic-2bone). The editor lets creators drag the effector and previews the resolved chain. Solver iteration count and tolerance are channel-level parameters with documented defaults.
7. **Blend tree editor.** `animation.blend_tree` gseeds are edited as a node graph (1D blend, 2D blend, additive, layered, state machine). Each node has typed parameter inputs (e.g., a 1D blend node binds to a `blend_speed: float` parameter). Sign-time validation: blend tree must be acyclic, all referenced clips must exist, all parameter names must resolve.
8. **Sprite sheet packing.** The editor packs sprite frames into atlases via the universal pipeline (Brief 089). Atlas layout is deterministic per the canonical packer in Brief 021. Re-pack is a one-click operation that produces a new signed atlas gseed and updates the clip's frame UV references in one batch.
9. **Skeleton retargeting.** Brief 161's retargeting is exposed as a typed `animation.retarget_map` gseed mapping bone names between two skeletons. The editor produces an automatic mapping from name heuristics + bone-length similarity, then lets the creator override per-bone mappings. Sign-time validation rejects retarget maps with disconnected bone references.
10. **Root motion.** Root motion extraction is a per-clip flag with a typed `root_motion_axes` field declaring which axes (x/y/z/yaw) are extracted to entity transform vs baked into the animation. The editor renders the extracted root motion as a path overlay on the preview viewport.
11. **Event channel.** Animation clips can carry typed `animation.event` keyframes that emit signed events to the runtime (e.g., footstep audio cue, attack hitbox enable per Brief 167). Events are first-class lineage entries — they aren't "side data."
12. **Onion skinning.** For sprite clips, the editor renders prior/next frames at reduced opacity. This is editor-runtime overlay, not signed.
13. **Sample-rate decoupling.** Animation clips store keys in canonical time (seconds) and sample rate is a runtime concern. The editor preview rate is independent of the runtime fixed tick — Brief 152's fixed-tick determinism is preserved because the sampler interpolates at runtime tick boundaries.

## Risks identified
- **Sprite atlas re-pack invalidating clip references.** Re-packing can move frames. Mitigation: clip frame references are by atlas frame *name* (Brief 021), not by UV. The packer guarantees name stability across re-packs.
- **IK solver determinism across editor/runtime.** FABRIK/CCD iteration counts must be identical or solved poses diverge. Mitigation: iteration count and tolerance are part of the `animation.ik_chain` gseed and frozen at sign time.
- **Retargeting over distinctly different skeletons.** Auto-mapping fails when bone names diverge. Mitigation: editor surfaces unmapped bones as warnings and refuses to commit a retarget map with required bones unmapped.
- **Blend tree complexity explosion.** Deep blend trees can be hard to debug. Mitigation: sign-time validation caps blend tree depth at 8 (matching Unity Mecanim's practical limit) and requires every leaf clip to exist.
- **Event keyframe ordering ambiguity.** Two events on the same frame with no defined order. Mitigation: events on the same frame are resolved by stable sort on the event's typed `priority` field, with sign-time validation that no two events on the same frame share a priority.

## Recommendation
Specify the animation editor as a unified timeline over Brief 161 channels with sampler-equals-runtime preview, signed atomic keyframe mutations, IK chain editing with frozen solver parameters, and sprite/skeletal/IK/blend-tree all in one tool. Ship the seven curve types, eight brush primitives, and the retarget editor at v0.1. Defer 3D skeletal editing and blend tree authoring runtime to v0.4 per Brief 156's 3D-physics defer, but ship the schemas at v0.1 so the editor surface is parity from day one.

## Confidence
**4.5 / 5.** The unified timeline pattern is well-precedented (Spine, DragonBones, Aseprite, Unity Animation, Blender NLA). The novelty is the runtime-equals-editor sampler binding and the lineage-tracked keyframe mutations. Lower than 5 because IK solver parameter determinism across editor/runtime needs Phase-1 measurement.

## Spec impact
- New spec section: **Animation editor surface specification**.
- Adds `animation.timeline` editor view contract.
- Adds `animation.event.priority` field to break same-frame ordering ambiguity.
- Adds the per-clip `root_motion_axes` field.
- Cross-references Briefs 161, 152, 177, and Round 2 IK briefs.

## New inventions
- **INV-729** — Unified timeline over typed channel kinds: one editor surface edits sprite, skeletal, blend-shape, material, and event channels with per-channel keyframe widgets.
- **INV-730** — Sampler-equals-preview contract for animation: the editor preview sampler is literally the runtime sampler, so scrubbing produces frame-exact runtime motion.
- **INV-731** — Frozen-IK-parameters gseed: solver iteration count and tolerance are part of the IK chain gseed and signed at edit time, guaranteeing editor/runtime/replay determinism.
- **INV-732** — Atlas-re-pack with frame-name stability: sprite re-packing moves frame UVs but preserves frame names; clips reference frames by name, not UV, so re-packs don't invalidate clips.
- **INV-733** — Auto-retarget with override surface: retarget maps are produced from name + length heuristics, surfaced for creator override, and sign-time validated against bone connectivity.

## Open follow-ups
- Mocap import pipeline (deferred to v0.4 with 3D skeletal runtime).
- Auto-keyframing (record-mode authoring) — deferred to v0.2.
- Physics-based secondary motion (cloth/jiggle bones) — deferred to v0.4 (Brief 156 3D physics defer).
- Curve baking and key reduction passes — deferred to v0.2 as an optimization tool.
- Multi-creator simultaneous animation editing — deferred to v0.3.

## Sources
1. Brief 021 — Sprite engine deep dive.
2. Brief 089 — Universal anything-to-gseed pipeline.
3. Brief 152 — Game loop and tick model.
4. Brief 156 — Physics integration 2D and 3D.
5. Brief 161 — Animation runtime namespace.
6. Brief 177 — Scene and level editor specification.
7. Round 2 IK briefs (FABRIK and CCD).
8. Spine User Guide — esotericsoftware.com/spine-user-guide.
9. Unity Animation Window and Animator Controller documentation.
