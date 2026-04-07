# 076 — Eliminating open-weight licensing volatility

## Question
The Round 2 synthesis conceded that "open-weight licensing volatility is a real ongoing risk." That concession was premature. How does GSPL structurally eliminate its exposure to any single upstream model provider changing their license, via multi-backbone redundancy, a federated training collective, license-aware automatic engine migration, defensive forks, compositional retraining, and distillation insurance?

## Why it matters
Every open-weight model GSPL depends on — Flux, Stable Diffusion, Hunyuan, Mochi, LTX, SMPL-X, Whisper, Llama, Gemma, and the long tail of Gaussian splat and NeRF backbones — is released under a license that the upstream vendor can unilaterally change at any time. Stable Diffusion 3's license shifted mid-release; Meta's Llama community license has enterprise carve-outs; SMPL-X has research-only restrictions; CreativeML OpenRAIL-M has usage restrictions that can be interpreted. A creative platform that builds on these without a resilience plan is building on sand. Houdini and Unreal don't have this problem because they're closed-source — they just have a *different* set of upstream risks (vendor lock-in). GSPL has to solve this structurally or accept fragility.

## What we know from the spec
- Brief 002, 003: shipped engines.
- Brief 015, 019: gseed format and plugin ABI.
- Brief 028: per-engine spec format.
- Brief 043: federation.
- Brief 044: marketplace economics.
- Brief 046: IP rights and licensing.
- Brief 055: LLM runtime and BYO models.
- Brief 060: supply chain and dependency security.
- Brief 075: federated compute.

## Findings — the structural shape of the risk

Open-weight licensing volatility is not one risk. It is five:
1. **Retroactive license change.** A vendor releases a model under Apache 2.0, then re-releases with a restrictive clause; downstream users in the intervening window have unclear standing.
2. **Usage restrictions.** "Research only," "non-commercial," "no creators under 18," "no deepfakes" (definition unclear), "no competing models."
3. **Geographic carve-outs.** EU-only, US-only, sanctioned-country exclusions.
4. **Revenue thresholds.** Free until you hit $X revenue, then you owe royalties or re-negotiate.
5. **Vendor abandonment.** A vendor stops updating a model; users are stuck on a stale backbone.

A resilient creative substrate must address all five.

## Findings — what GSPL ships

### 1. Multi-backbone redundancy as a substrate contract (INV-218)
Every neural engine category in GSPL is served by **at least three independent backbones from different vendors under different licenses.** The substrate never hard-depends on a single model. This is declared in each engine's spec (Brief 028):

- **Image generation:** Flux (Apache 2.0 Schnell, non-commercial Dev), Stable Diffusion family (CreativeML OpenRAIL-M), Hunyuan-DiT (Tencent license), PixArt-Σ (open), Kandinsky (Apache 2.0), Würstchen (MIT).
- **Video:** Mochi, LTX-Video, Hunyuan-Video, Wan, CogVideoX, OpenSora. Multiple Apache/MIT options.
- **3D Gaussian avatars:** GaussianAvatars, HumanRF, INSTA, GaussianHead, open SMPL-X alternatives (STAR, SUPR).
- **NeRF:** Instant-NGP variants, Zip-NeRF, Nerfstudio-supported models.
- **LLM:** Llama, Gemma, Qwen, Mistral, OLMo, Phi, and the broader open ecosystem.
- **ASR/TTS:** Whisper, Parakeet, Canary, Kokoro, F5-TTS, XTTS.

At any time, at least two members of each category are under permissive licenses (Apache 2.0 or MIT equivalent) with no usage restrictions. If a vendor shifts terms, the substrate seamlessly swaps to another. **Users never have to care.**

**Concrete win:** If Black Forest Labs re-licenses Flux tomorrow, GSPL's default image engine swaps to Kandinsky-3 overnight with no user-visible change except an updated license manifest.

### 2. License-aware automatic engine migration (INV-219)
Every gseed carries a **license manifest** declaring which engines and models it depends on, their licenses, and the resulting combined usage rights. The substrate ships a **license evaluator** that, on model license changes, automatically:

1. Detects affected gseeds in the user's library.
2. Identifies an equivalent-capability engine under a permissive license.
3. **Rebuilds** the gseed on the new backbone (regenerates the outputs with the new engine), preserving parameters and lineage.
4. Notifies the user of any quality delta.

The user receives a single action: "The image engine you were using has changed terms. GSPL has rebuilt your 47 affected gseeds on Kandinsky-3. See diff."

This is impossible in Stable Diffusion forks, A1111, ComfyUI, or any other tool because they treat models as configuration, not as substrate-level dependencies with declared licenses.

**Concrete win:** A studio with 10,000 gseeds on Flux survives a license shift without a single broken project. In a traditional toolchain, they'd be manually redoing work for weeks.

### 3. Defensive fork policy
GSPL maintains **defensive forks** of every critical backbone at the moment of its most-permissive licensing. When Stable Diffusion 1.5 was released under CreativeML OpenRAIL-M, GSPL forks the checkpoint. If SAI later changes terms, the fork remains under the original license. This is legally well-established — you cannot retroactively restrict what was already granted.

The forks are hosted on the federation (Brief 043) and mirrored across multiple jurisdictions to be robust against takedown attempts. This is functionally what Hugging Face Hub already does informally; GSPL makes it a **substrate commitment** with mirrors, signed snapshots, and cryptographic attestation of the original license at fork time (INV-220).

**Concrete win:** If SAI, Meta, or Tencent pulls a model from public distribution, GSPL users still have access to the last permissively-licensed version, attested by lineage to prove its provenance.

### 4. Federated foundation training collective (INV-221)
GSPL establishes a **federated training collective** — opt-in peers contribute compute cycles (via INV-215 from Brief 075) to train open-weight foundation models jointly. The collective:

- Trains on fully-cleared datasets (CC0, CC-BY, opt-in contributions, Wikimedia Commons, LAION-Pop cleaned subsets).
- Releases weights under **Apache 2.0 with no usage restrictions whatsoever.**
- Is governed by a nonprofit or foundation structure with a mandate to never change terms.
- Uses the same substrate it serves — GSPL is dogfooded for the collective's workflow.

This is a long game. The collective will not match Flux or Sora at v1. But by v2-v3 it will provide GSPL with a **license-stable fallback** that is functionally independent of any single corporate vendor. Prior art: EleutherAI (GPT-J, Pythia), LAION (Stable Diffusion training data), OpenStreetMap (community-built alternative), Wikimedia (collective knowledge).

**Concrete win:** At v3, the GSPL substrate can be fully functional on 100% foundation-collective-trained models. Even if every commercial open-weight vendor goes closed overnight, GSPL still ships.

### 5. Compositional retraining via LoRA and small fine-tunes
Even within a single backbone, GSPL ships an **open LoRA/adapter library** trained on cleared data. These adapters reproduce much of the quality advantage of proprietary models via fine-tuning on top of permissive bases. The substrate treats LoRAs as first-class gseeds with their own lineage, authorship, and license.

**Concrete win:** A user on a permissive base model (Kandinsky, Würstchen) loads a community LoRA and matches 95% of Flux quality for their specific aesthetic.

### 6. Distillation insurance
When a permissively-licensed distilled version of a restricted model exists (SDXL Turbo, LCM, Flux Schnell), GSPL ships the distilled version as a substrate citizen. Distillation creates derivative works whose license is determined by the distillation data and process, not the teacher model's license — a legal gray area but an established practice in the ML community.

For extra safety, GSPL also ships **clean-room-distilled** variants: models distilled only from fully-cleared teachers onto fully-cleared training data. These are lower quality but legally bulletproof.

**Concrete win:** If Flux Schnell's license is later revoked or challenged, GSPL's clean-room distillation provides a drop-in replacement.

### 7. License tier segmentation in the marketplace (Brief 044)
The marketplace (Brief 044, Brief 046) already uses L1-L5 license tiers. GSPL extends this to **engine licenses**: a gseed's effective license is the *most restrictive* license in its dependency chain. The substrate computes this automatically and exposes it to the user.

A creator can filter: "Show me only engines whose outputs are safe for commercial use under CC-BY." The substrate's license evaluator resolves the dependency chain and flags conflicts before the user invests creative work on top of a risky backbone.

**Concrete win:** A studio targeting commercial release never accidentally builds on a research-only model. A creator who doesn't care picks the highest-quality model regardless.

### 8. Substrate sovereignty contract
GSPL commits — constitutionally, in the spec — that **no version of the GSPL substrate will ever require a model whose license restricts the user's commercial use or expression.** This is the same sovereignty principle as Brief 075: the commercial cloud is optional, not required. Here: the commercial open-weight vendor is optional, not required.

Every GSPL release is validated against the constraint: can a user with no access to restricted models still accomplish every workflow the release documents? If yes, ship. If no, the release is not shippable.

## What GSPL ships at each phase

### v1
- **Multi-backbone redundancy** for image (Flux Schnell + Kandinsky + Würstchen or similar trio).
- **License manifest** on every gseed.
- **Defensive fork policy** for v1 backbones.
- **License evaluator** (INV-219) with manual user action.
- **Clean-room distillation pipeline v1** for critical backbones.
- **Open LoRA marketplace** at launch.

### v1.5
- **Multi-backbone redundancy** extended to video, 3D avatars, NeRF, LLM, ASR/TTS.
- **Automatic license-aware migration** (INV-219 full automation).
- **Federated defensive fork mirrors** across jurisdictions.
- **Foundation training collective v0** — bootstrap with governance and compute commitments.

### v2
- **Foundation collective first production model** (likely image generation at modest quality).
- **Clean-room distillation at full quality parity** for image models.
- **Cross-jurisdiction license enforcement** automation.

### v3
- **Foundation collective production models across all critical categories.**
- **100% license-independent substrate** — every workflow achievable on collective models alone.

## Inventions

### INV-218: Multi-backbone redundancy as substrate contract
Every neural engine category is served by at least three independent backbones from different vendors under different licenses, with at least two under unrestricted permissive terms at all times. Declared in the engine spec. The substrate refuses to ship a single-backbone engine. Novel because no creative tool treats model redundancy as a substrate-level sovereignty commitment.

### INV-219: License-aware automatic engine migration
Every gseed carries a license manifest; the substrate ships a license evaluator that detects upstream license changes and automatically rebuilds affected gseeds on equivalent-capability engines under permissive licenses. The user's library survives vendor license shifts without manual intervention. Novel because no tool treats model dependencies as upgradable substrate dependencies with license-aware re-resolution.

### INV-220: Cryptographically-attested license snapshots
Every defensive fork is timestamped and signed, with the license in effect at fork time recorded in the snapshot. Legal provenance for the claim "this weight file was released under these terms on this date." Federated mirrors prevent takedown. Novel because Hugging Face's license tracking is informal; GSPL's is cryptographic and federated.

### INV-221: Federated foundation training collective
Opt-in peers contribute compute (via INV-215) to train open-weight foundation models on fully-cleared data under unrestricted permissive licenses. Governed by a nonprofit mandate forbidding term changes. Dogfooded on the GSPL substrate. Novel as a cross-platform-native training collective for creative models (EleutherAI is the analog for LLMs; no equivalent yet exists for image/video/3D/avatar at scale, and none are governance-bound to permanent permissive terms).

## What the closed-source competition still does at v1

Honest accounting:
- **Single-vendor quality advantage.** Flux Dev, Sora, Veo, Midjourney all have capabilities the permissive open weights don't fully match at v1.
- **Vendor support and guarantees.** Commercial customers get commercial support. GSPL ships with community support.
- **Predictable roadmap.** Closed vendors publish quarterly updates; the open ecosystem moves unpredictably.

These are real advantages. GSPL's answer: **they are advantages only for users willing to accept the underlying risk.** For users who cannot accept the risk — studios under regulatory scrutiny, creators in restricted jurisdictions, long-horizon projects that must not break — GSPL's redundancy is the only viable choice.

## Risks identified

- **Multi-backbone quality variance.** Different models produce different aesthetics. Mitigation: the substrate presents the backbone as a user-visible choice; lineage records which backbone produced each output.
- **Federated training collective is expensive.** Frontier foundation model training is $10M+ at v1 scale. Mitigation: start with smaller, more focused models (distillation targets, LoRAs, task-specific); crowdsource compute via INV-215; accept slower progress than corporate vendors.
- **License evaluator legal complexity.** License interpretation is lawyerly. Mitigation: conservative default; legal review per major jurisdiction; the evaluator reports classifications, not legal advice.
- **Defensive forks may face takedown.** DMCA, C&D letters. Mitigation: multiple jurisdictional mirrors; legal defense fund via marketplace fees; commitment to fair-use/archival arguments.
- **Clean-room distillation quality gap.** May lag commercial distillations for years. Mitigation: ship both (commercial-distilled and clean-room-distilled); user picks based on their risk tolerance.
- **Collective governance capture.** A collective can be co-opted. Mitigation: constitutional charter with amendment thresholds; multi-stakeholder board; transparent ledger.

## The strategic claim

Every creative tool building on open weights is **one license change away from a platform crisis**. A1111, ComfyUI, Civitai, Pinokio — they all assume the underlying weights stay permissively available. They have no contingency. GSPL is the first creative substrate where **license changes are expected, routine, and structurally absorbed**. This is not a niche guarantee; it is the difference between a tool you can bet a studio on and a tool you cannot. GSPL is the bettable one.

## Recommendation

1. **Reverse the "open-weight licensing volatility is a risk" concession.** GSPL ships multi-backbone, license-aware, defensively-forked, and long-term collective-trained.
2. **Mandate INV-218 (multi-backbone redundancy)** as a substrate contract at v1.
3. **Implement INV-219 (license-aware migration)** manual-action version at v1; full automation at v1.5.
4. **Launch defensive forks (INV-220)** at v1 for all critical backbones.
5. **Start the foundation training collective** as a v1.5 governance initiative, v2 first model.
6. **Ship license manifest + evaluator in every gseed** at v1.
7. **Engage LAION, EleutherAI, OpenSora, Hunyuan, Black Forest Labs** as collective partners.
8. **Legal review per major jurisdiction** on the defensive fork strategy and license evaluator classifications.
9. **Marketing language:** "Every other creative tool bets on a vendor. GSPL never has to."

## Confidence
**3.5/5.** The technical pieces are feasible; the uncertainty is governance and economics of the foundation training collective, which depends on community adoption that cannot be fully predicted. Multi-backbone redundancy, license evaluator, and defensive forks are all high-confidence. The collective is a 3/5 bet that pays off only in the long run.

## Spec impact

- `architecture/license-resilience.md` — new doc.
- `architecture/foundation-training-collective.md` — new doc.
- Update Brief 019 (plugin ABI) to require license manifest on every engine.
- Update Brief 028 (per-engine spec) to require multi-backbone declaration.
- Update Brief 046 (IP rights) to include the license evaluator and migration flow.
- Update Brief 055 (LLM runtime) to reflect the multi-backbone contract.
- Update Brief 060 (supply chain) to include defensive fork mirror architecture.
- New ADR: `adr/00NN-multi-backbone-redundancy-contract.md`.
- New ADR: `adr/00NN-foundation-training-collective.md`.
- Remove the "open-weight licensing volatility" concession from `round-2-synthesis.md`.

## Open follow-ups

- Legal review of defensive fork policy per major jurisdiction.
- Pick v1 backbone trios for each engine category.
- Design the foundation training collective governance charter.
- Engage EleutherAI and LAION as founding partners.
- Build INV-219 prototype against real license manifest cases.
- Assess clean-room distillation quality deltas per category.
- Plan collective compute bootstrapping via INV-215.

## Sources

- CreativeML OpenRAIL-M license text.
- Llama Community License text and Meta's subsequent amendments.
- Flux family license texts (Apache 2.0 Schnell vs Dev Non-Commercial).
- SAI's Stable Diffusion 3 licensing controversy timeline.
- EleutherAI governance and Pythia release notes.
- LAION dataset and training collaboration history.
- Hugging Face model licensing metadata conventions.
- Various model card analyses.
- Internal: Briefs 002, 003, 015, 019, 028, 043, 044, 046, 055, 060, 075.
