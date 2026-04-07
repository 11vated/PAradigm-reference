# 038 — POET: open-ended co-evolution

## Question
What is POET (Paired Open-Ended Trailblazer), how does it apply to GSPL's simulation and game engines, and what makes it tractable at solo-founder budgets?

## Why it matters
Most evolution stacks converge — they find a local optimum and stop being interesting. POET *doesn't converge by design*. It produces an indefinitely growing collection of (environment, agent) pairs where each pair is meaningful only because the others exist. This is the only known recipe for *open-ended creativity at scale*. For GSPL's simulation engines and FullGameEngine, POET is the headline feature.

## What we know from the spec
- Brief 035 named POET as Layer 6 of the evolution stack.
- Brief 023 (interactive engines) and Brief 025 (simulation engines) are the consumers.

## Findings — POET in one paragraph

POET maintains a population of *(environment, agent)* pairs. Each pair is co-evolved: the environment is mutated to be more challenging, the agent is mutated to better solve its environment. New environments are spawned by mutating existing ones, and an environment is admitted to the active set only if it's *novel* (different from existing environments) and *just barely solvable* by some agent. Periodically, agents from one pair are *transferred* to other pairs to test whether they generalize. The result is an unbounded curriculum: each pair only exists because of the agents and environments that came before it.

## How it maps to GSPL

### What's an environment in GSPL?

Different things in different engines:
- **GameEngine**: a level, a rule set, a difficulty configuration.
- **PhysicsEngine**: a world layout (terrain, gravity, obstacles).
- **EcosystemEngine**: an initial biome configuration.
- **ALifeEngine**: a starting world + selection pressure.
- **FullGameEngine**: a full game spec (rare; expensive).

In all cases the environment is itself a sub-seed of the appropriate engine. Mutating an environment is just mutating its seed.

### What's an agent in GSPL?

An agent is a seed in an engine that can be *evaluated against* an environment. Most often this is a CharacterEngine seed with a BehaviorGene + RuleGene action set, or a small ALife genome.

### The fitness function

For GSPL, POET fitness is **reachable & interesting**: the agent must reach a meaningful state in the environment (solving the puzzle, surviving N steps, scoring above a floor) and the environment must be different from existing ones in BC space.

### The transfer mechanism

Periodically, take agent A from pair (E_a, A) and run it in environment E_b. If A outperforms B in B's own environment, A *replaces* B. This is how POET generalizes: agents that work in many environments survive.

## Solo-founder constraints

Standard POET runs are *enormous* (Wang et al.'s original ran for days on hundreds of CPUs). GSPL adapts:

1. **Bounded population**: 32 active pairs at v1, 128 at v2. Capped not unbounded.
2. **Bounded generations per session**: a POET session has a hard step budget (e.g., 10K steps total) and resumes from checkpoint next session.
3. **Surrogate-assisted evaluation**: use a learned surrogate (Brief 012) to pre-screen environments for "is this just-barely-solvable?" before paying for a full rollout.
4. **GPU rollouts**: physics and game rollouts on the fixed-point GPU kernel (Brief 001) are batched.
5. **Checkpointing**: every N steps the entire POET state is checkpointed and resumable.
6. **Asymmetric compute**: agents get more compute than environments. Most rollouts are agent-improvement, not environment-creation.

## When POET is the right tool

- **Long-running creative loops** where the user wants to "let it run overnight" and come back to a curated archive.
- **Engines where novelty is the entire point** (ALife, Procedural, FullGame).
- **When the user has zero idea what they want** and is exploring open-ended.

## When POET is the wrong tool

- **Quick interactive sessions**: too slow.
- **Engines with no environment/agent split**: most static asset engines.
- **Cost-sensitive users**: POET burns compute by design.

## Risks identified

- **Compute cost dominates**: POET is the most expensive thing in the evolution stack. Mitigation: opt-in only, hard budgets, surrogate pre-screening.
- **Open-ended drift**: a POET archive can drift into uninteresting regions. Mitigation: periodic critic-based pruning to remove pairs whose agents and environments both fail to advance.
- **Niche collapse**: all environments converge to one shape. Mitigation: explicit BC-space coverage requirement on the active set.
- **Transfer regressions**: a transferred agent damages the source pair. Mitigation: transfer is non-destructive to source by default.
- **Determinism in long runs**: floating-point drift over millions of steps. Mitigation: fixed-point kernel (Brief 001) + checkpointing with hash chains.

## Recommendation

1. **Adopt POET as a v1 *opt-in* algorithm** for simulation and FullGame engines.
2. **Active pair cap** at 32 (v1), 128 (v2).
3. **Hard step budget per session** with checkpoint resume.
4. **Surrogate-assisted environment pre-screening** is mandatory.
5. **Asymmetric compute split**: 70% agent improvement, 30% environment creation.
6. **Explicit BC coverage requirement** on the active set to prevent niche collapse.
7. **Determinism on the fixed-point kernel** with hash-chain checkpoints.
8. **POET sessions are first-class artifacts**: checkpointable, signable, shareable.

## Confidence
**3/5.** POET works in research but is hard to tame for production. The 3/5 reflects honest uncertainty about whether the solo-founder adaptations preserve the open-ended-ness or accidentally collapse the algorithm.

## Spec impact

- `algorithms/evolution/poet.md` — full POET pseudocode with GSPL adaptations.
- `architecture/poet-budgets.md` — pair caps and step budgets.
- `algorithms/poet-surrogate.md` — surrogate-assisted pre-screening.
- New ADR: `adr/00NN-poet-as-opt-in.md`.

## Open follow-ups

- Build a POET prototype against the GameEngine in Phase 2.
- Empirically test surrogate pre-screening accuracy.
- Decide on the BC coverage metric (probably entropy of cell occupancy).
- Investigate whether POET can produce shareable "challenge sets" that other users can run.

## Sources

- Wang et al., *Paired Open-Ended Trailblazer (POET)*.
- Wang et al., *Enhanced POET: Open-Ended Reinforcement Learning through Unbounded Invention of Learning Challenges and their Solutions*.
- Internal: Briefs 001 (kernel), 012 (surrogate), 035, 023, 025.
