# Self-Bootstrapping Loop

**Status:** canonical
**License:** GSPL Open Specification License (GSPL-OSL-1.0)
**Materializes:** `agent/bootstrap/loop.py`, `agent/manifest.yaml#bootstrap_loop`

The self-bootstrapping loop is the mechanism by which the GSPL agent
grows its own training corpus and improves CodeSmith without relying
on any external annotator, labelling service, or closed dataset. The
loop is deterministic, auditable, and fully air-gap capable.

## Phase A — Gold corpus seeding

A curator script walks `seed_commons/`, `spec/`, and `language/` and
emits the initial gold corpus as ShareGPT-format conversations. Every
example is a tuple:

    (intent_prompt, expected_envelope, expected_source, expected_hash)

The minimum gold-corpus size is 5000 examples (declared in
`manifest.yaml#bootstrap_loop.gold_corpus_minimum_size`). Below that
threshold, the loop refuses to fine-tune.

## Phase B — Continuous loop

For every cycle (default 1000 prompts per cycle):

1. `SyntheticPromptGenerator` samples a domain, archetype, and
   adjective bundle from `intelligence/intent-taxonomy.md` and emits
   a natural-language prompt. The RNG seed is deterministic in the
   cycle index so the prompt stream is exactly reproducible.
2. The full six-stage pipeline runs on the prompt.
3. If Stage 4 passes, the `(prompt, envelope, source, hash)` tuple
   is archived to `agent/bootstrap/corpus/gold/` with provenance
   `fully_agentic`.
4. If Stage 4 fails after all configured retries, the defect set is
   archived to `agent/bootstrap/corpus/negative/` as a contrastive
   example.
5. Every cycle emits a manifest fragment to
   `agent/bootstrap/corpus/manifest.json` summarizing the delta.

Cycles are idempotent: re-running with the same `(synthetic seed,
cycle_index)` produces byte-identical corpus additions.

## Phase C — Fine-tune trigger

When the gold corpus has grown by
`fine_tune_threshold_new_examples` (default 50_000) since the last
fine-tune, the loop calls
`SelfFineTuneTriggerTool.trigger(opt_in_confirmed=operator_flag)`.

The new adapter is evaluated against a held-out set of
`held_out_size` (default 10_000) examples using the four canonical
metrics defined in `agent/fine_tune/eval_harness.py`. If every metric
is >= `required_pass_rate` (default 0.995), the adapter is promoted
to production and signed by the SovereignSigner. Otherwise it is
archived for inspection and the previous adapter remains in use.

## Phase D — Federated adapter governance (optional)

Operators may publish promoted adapters to a federated registry.
Every published adapter is signed and carries its gold-corpus
manifest so downstream forks can audit the exact examples used in
training. Federation is optional and never a prerequisite for running
the agent.

## Sovereignty guarantees

- Every synthetic prompt, every Stage receipt, every gold-corpus
  addition, every fine-tune event is recorded in the lineage ledger.
- No example in the gold corpus may claim human authorship; the
  provenance field is always `fully_agentic` or `agent_assisted`.
- The sovereignty gene on the agent's identity seed is mutated on
  exactly zero occasions. It is immutable.
- The loop is byte-reproducible given the same RNG seed prefix.

## Determinism invariants

The following must hold for every cycle:

- `RNG seed = SHA-256("gspl.bootstrap:" || manifest_version || cycle_index)`
- The ordered list of prompts emitted in cycle N is a pure function of
  that RNG seed.
- Every resulting seed hash is a pure function of the grown payload.
- Re-running cycle N from the same state produces byte-identical gold
  and negative corpus additions.

Violation of any of these invariants is a Stage 4 error and blocks
fine-tune promotion.
