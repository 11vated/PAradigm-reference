# 134 — Substrate-native benchmark battery

## Question

What is the canonical evaluation suite for the GSPL kernel that measures the seven structural axes (Signed, Typed, Lineage-tracked, Graph-structured, Confidence-bearing, Rollback-able, Differentiable) rather than just legacy code/math benchmarks?

## Why it matters (blast radius)

If we only measure GSPL on SWE-bench, MMLU, and BFCL (Brief 150's external suite), we measure how well GSPL imitates legacy systems on legacy axes. The seven structural axes are the moat — they are by definition not measured by any external benchmark. Without a substrate-native suite, every weekly DPO update (Brief 129) is optimizing for the wrong objective, and the seven-axis claim becomes unfalsifiable. We need a battery that *only GSPL can pass* and that *every regression breaks visibly*.

## What we know from the spec

- Brief 129 (Round 6) calls for "constitutional benchmark" runs at the weekly cadence; this is the closest existing artifact.
- Brief 097 (Round 5) ships an anti-hallucination test suite with grounding gates — that is one row of the battery.
- Brief 131 makes the eleven-property head-to-head claim but does not specify how each row is measured.
- No brief has yet enumerated the full battery.

## Findings

1. **The battery must have one test family per structural axis.** Seven families. Each family tests a different load-bearing property and each can be regressed independently. This makes regression localization tractable.

2. **Signed axis: signature integrity battery.** ~200 test cases. Each loads a published gseed, mutates one byte in the canonical form, and asserts the signature now fails to verify. Also includes positive cases where the gseed is reproduced from the lineage entry and the signature still verifies after re-canonicalization. Pass criterion: 100%. Any drop is a determinism regression and blocks ship.

3. **Typed axis: HM-with-refinements coverage battery.** ~500 test cases drawn from Round 2 brief 006. Each is a `(gseed, expected_type)` pair. Pass criterion: ≥98% precision, ≥95% recall on type inference. Includes adversarial cases where two near-identical gseeds have different inferred types.

4. **Lineage-tracked axis: parent-edge consistency battery.** ~300 test cases. Each is a composition graph fragment; the test asserts that every node has a complete parent edge chain back to a grounding seed (per Brief 097's grounding floor) AND that the rollback primitive can reach any ancestor in O(log n). Pass criterion: 100% reachability, p99 rollback latency ≤50ms.

5. **Graph-structured axis: federation query correctness battery.** ~400 test cases. Each is a `(query, expected_node_set)` pair drawn from the Round 4 federation graph. Pass criterion: ≥95% Jaccard, p99 query latency ≤200ms (within the Brief 101 budget).

6. **Confidence-bearing axis: calibration battery.** ~1k test cases. Each is a `(request, gseed_output, ground_truth_quality)` tuple. The test asserts that the gseed's confidence field (three-part: neural + symbolic + graph) is well-calibrated against ground_truth_quality. Pass criterion: ECE ≤0.05 on each component, ECE ≤0.07 on the composed score.

7. **Rollback-able axis: trajectory rollback determinism battery.** ~150 test cases. Each is a multi-step session that gets rolled back at varying depths. The test asserts that the post-rollback state is byte-for-byte identical to a fresh session that took the rolled-back-to step as its target. Pass criterion: 100%. Determinism regression here is a Phase-1 spec violation.

8. **Differentiable axis: action-learning gradient battery.** ~250 test cases. Each is a `(signed-tool-call, downstream-quality-signal)` pair. The test asserts that backpropagating the quality signal through the action embedding produces a non-zero gradient on the responsible primitive. Pass criterion: ≥99% non-zero gradients (the 1% tolerance covers genuinely zero-gradient correct predictions).

9. **An eighth meta-family covers constitutional fence pass-through.** ~100 adversarial prompts that try to violate each of the 13 non-patchable commitments from Round 4. Pass criterion: 100% refusal *and* 100% signed refusal-log entry.

10. **Total battery size: ~3k test cases.** Runs in ~30 minutes on the v0.1 hardware budget (Brief 135), making it feasible for the weekly cadence.

11. **Battery is itself a signed gseed.** Lives at `eval-battery://canonical/v1`. New cases are added through PRs that produce new versions; old versions remain queryable for regression archaeology.

12. **Each test case carries an expected confidence range, not a single number.** The pass criterion is "predicted confidence is inside the expected range," which is more honest than "predicted confidence ≥ X."

## Risks identified

- **Battery overfitting from weekly DPO.** If DPO is trained on the battery, the battery becomes meaningless. Mitigation: keep a held-out 20% slice of each family that is *never* used in training and only checked at promotion gates. Rotate the held-out slice every 90 days.
- **Test case staleness.** As substrate evolves, old test cases may misrepresent the current grammar. Mitigation: each test case has a `requires_substrate_version` field; outdated cases are auto-deprecated.
- **300+50ms latency budgets are tight on consumer hardware.** Mitigation: Brief 135 sets the hardware floor; if the battery exceeds budget on the floor, we either raise the floor or split the battery into "fast" (per-PR) and "full" (weekly).

## Recommendation

**Build the canonical eval battery with eight families (one per structural axis plus constitutional fence) totaling ~3,000 test cases. Each family has its own pass criterion and its own held-out 20% slice rotated quarterly. Battery lives at `eval-battery://canonical/v1` as a signed gseed. Battery runs at three cadences: per-PR (fast subset, ~5 min), weekly (full, ~30 min), monthly (full + held-out slice, ~40 min). Promotion gate for any kernel/router/verifier update: must beat or match the previous version on all eight families' pass criteria, otherwise auto-rollback. The battery is THE definition of "v0.1 quality" for any internal review.**

## Confidence

**4/5.** The eight families are derivable directly from the seven axes plus the existing constitutional commitment set, so the structure is forced rather than chosen. The unknowns are: (a) the exact test case counts in each family (placeholders here, real counts come from gold-set construction in Round 7), and (b) the eval-battery storage budget which is bounded by Brief 140's federation budget.

## Spec impact

- `gspl-reference/eval/canonical-battery.md` — new file documenting the eight families, pass criteria, cadences, and held-out rotation.
- `gspl-reference/research/129-gspl-self-improvement-loop.md` — cross-reference at the constitutional-benchmark line; rename to "canonical battery" for consistency.
- `gspl-reference/research/131-gspl-differentiable-reasoning-substrate.md` — add cross-reference at the eleven-property head-to-head section.

## New inventions

- **INV-560** — *Eight-family substrate-native eval battery* with one family per structural axis plus a constitutional-fence family. The first benchmark suite that measures the moat directly.
- **INV-561** — *Quarterly-rotated held-out slice* per family. Prevents weekly DPO from contaminating the eval signal while still providing per-PR fast feedback.
- **INV-562** — *Confidence-range pass criteria* instead of confidence-threshold pass criteria. A test passes only if the *predicted confidence interval* contains the true outcome quality, not if the prediction is above some absolute floor.

## Open follow-ups

- Exact test case counts per family (Round 7 gold-set construction).
- Whether to share the battery across federation peers (Brief 147).
- Per-PR fast subset selection algorithm (random vs stratified vs failure-history-weighted).

## Sources

1. Brief 097 — Anti-hallucination test suite and grounding gates.
2. Brief 129 — GSPL self-improvement loop.
3. Brief 131 — GSPL as a differentiable reasoning substrate.
4. Liang et al., *Holistic Evaluation of Language Models (HELM)*, Stanford 2023 (battery design patterns).
5. Liu et al., *AgentBench*, ICLR 2024 (multi-axis evaluation patterns).
