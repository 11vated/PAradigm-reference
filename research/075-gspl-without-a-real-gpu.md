# 075 — GSPL without a real GPU

## Question
The Round 2 synthesis conceded that GSPL "depends on a real GPU for the best engines." That concession was premature. How does GSPL run — at usable quality — on machines without a discrete GPU, via federation, tiered execution, quantization, distillation, cloud burst, WebGPU, and lineage-attested remote compute?

## Why it matters
Most of the world does not have a discrete GPU. Laptops, Chromebooks, older desktops, school machines, and the entire mobile install base run on integrated graphics, Apple Silicon, or commodity NPUs. If GSPL's best engines require a high-end NVIDIA card, GSPL is a tool for the already-equipped — which is exactly the AAA ceiling GSPL was built to escape. Houdini and Unreal need *your* GPU. GSPL needs *some* GPU *somewhere* on the federation — and ideally, for most workflows, none at all.

## What we know from the spec
- Brief 026: deterministic kernel (CPU-path mandatory).
- Brief 027: reproducibility test harness (CPU reference).
- Brief 043: federation transport (libp2p/QUIC).
- Brief 044: marketplace economics (credits, settlement).
- Brief 054: three-tier rendering (deterministic / native fast / differentiable).
- Brief 055: LLM runtime and BYO models (quantization, hybrid cloud).
- Brief 057: release engineering (per-platform builds).
- Brief 071, 072, 073, 074: differentiable/neural/multiplayer substrate.

## Findings — the structural shape of the problem

"Need a GPU" is not one problem. It is four:
1. **Inference for neural engines** (diffusion, NeRF, neural avatars, neural shaders). High VRAM, high FLOPS, latency-tolerant.
2. **Training and fine-tuning** (neural riggers, critic fine-tunes, shader fine-tunes). Very high VRAM, very high FLOPS, batch-tolerant.
3. **Real-time rendering** (studio preview, playback). Latency-critical, modest FLOPS, low VRAM.
4. **Simulation** (differentiable physics, large particle counts). High FLOPS, moderate VRAM, latency-tolerant.

GSPL answers each with a different substrate primitive. None of them require the user to own a discrete GPU.

## Findings — what GSPL ships

### 1. Lineage-attested federated compute (INV-215)
Federation (Brief 043) is not just a content transport; it is a compute transport. Any GSPL peer can offer compute cycles — CPU, GPU, NPU — priced in marketplace credits. A peer requests a job by sending a **lineage hash**: `hash(input_gseed || engine_version || parameters || seed)`. The lender runs the job on its hardware, produces the output gseed, and signs an attestation: "I ran engine E at version V on inputs hashed as H and produced output hashed as O."

The borrower verifies the attestation in two ways:
- **Cheap:** the lender's signature on the output hash chains back to the deterministic kernel contract. If the engine is deterministic (Brief 020, 026), the borrower can spot-check by re-running a single frame on local CPU and comparing hashes.
- **Strong (optional):** a second peer runs the same job and both results must match. Disagreement is Byzantine-resolved by a third peer.

This is cryptographically stronger than any corporate render farm because the attestation travels with the output forever — an auditor years later can verify "this frame was produced by this engine at this version on these inputs."

**Concrete win:** A creator on a Chromebook renders a 3D Gaussian splat scene by leasing 10 minutes of GPU time from a peer with a 4090. The result is signed, verifiable, and cheaper than any cloud service because there is no middleman.

### 2. Tiered-quality execution gradient (INV-216)
Every GSPL engine ships **at least three execution tiers** declared in its engine manifest:
- **T0 — CPU fallback.** Single-thread or lightly threaded CPU path. Always present. Slow but functional. Enables the deterministic kernel contract on any machine.
- **T1 — Integrated/Apple/NPU path.** Runs on integrated graphics, Apple Silicon Neural Engine, or commodity NPUs via WebGPU, Metal, or ONNX Runtime. Quantized (INT8/FP16), distilled where possible. Sufficient for previews, iteration, and most creator workflows.
- **T2 — Discrete GPU path.** Full-quality native CUDA/ROCm/Vulkan. For finals and heavy neural workloads.
- **T3 (optional) — Federated / cloud.** Same as T2 but runs on a remote peer with INV-215 attestation.

The runtime picks the tier that matches the user's hardware and the job's quality requirement. **Previews are always local; finals can be federated.** This is the critical workflow ergonomic: nothing stalls waiting on the network because preview-grade output is always available on-machine.

**Concrete win:** A user on an M2 MacBook Air iterates on a scene in real time at T1 quality, then fires "render final" and GSPL automatically routes the job to a federated T3 peer, pays them in marketplace credits, and returns a signed final in minutes. In Unreal this workflow doesn't exist; the user either has the hardware or doesn't.

### 3. Quantization and distillation as first-class engine citizens
Every neural engine in GSPL ships alongside **distilled small variants** and **quantized variants**. The substrate treats these as sibling gseeds: a full-fat Flux-Dev gseed and a Flux-Schnell-Distilled-INT8 gseed share lineage and parameter semantics. Switching is a gseed swap, not a reconfiguration.

Distillation is an ongoing process: GSPL ships a **distillation pipeline** (Brief 055) so the community can re-distill models when new quantization methods arrive (AWQ, GPTQ, SpinQuant, SmoothQuant, and successors). Distilled models live in the marketplace with their own lineage and authorship.

**Concrete win:** A user with 8 GB of unified memory runs a 4-bit-quantized Flux-Schnell variant at 3 sec/image on an M1. MetaHuman won't even open on that machine.

### 4. WebGPU + WASM for in-browser execution
GSPL's CPU path and T1 path compile to **WASM + WebGPU** for in-browser execution. This is not a toy demo; it is a real execution tier. A user can open `studio.gspl.dev` in any modern browser, load a gseed from federation, and iterate on it without installing anything. Federation transport runs over WebTransport/libp2p-js. Finals can still be routed to a federated peer.

**Concrete win:** A school student on a locked-down Chromebook creates and publishes a gseed from the browser. Unity, Unreal, Houdini, MetaHuman, Roblox Studio are all installable-only or require accounts and credit cards; GSPL runs from a URL.

### 5. Cloud burst mode as an opt-in, not a requirement
For users who don't want to federate with peers, GSPL offers **opt-in cloud burst** (Brief 055 hybrid path). The substrate treats the cloud as just another federation peer — the same INV-215 attestation applies, the same lineage is produced. Providers are interchangeable (GSPL ships adapters for the major cloud GPU providers and community-run gsplcompute.org-style collectives).

**Crucially, cloud burst is never mandatory.** GSPL's sovereignty principle forbids a runtime that cannot function without a commercial cloud. Cloud is an accelerant, not a dependency.

**Concrete win:** A user who doesn't want to join the peer federation pays a flat per-minute rate to a cloud provider for T3 compute. A user who wants zero dollars pays zero dollars by using federation credits earned from offering their own idle cycles.

### 6. Compute marketplace economics
Compute is priced in marketplace credits (Brief 044). A peer offering their GPU during idle hours earns credits that can be spent on finals, or converted through the marketplace. **This creates a non-extractive compute economy**: nobody's value is being taken by a middleman cloud provider.

Reputation and attestation chain through Brief 042 identity. Bad actors who sign bogus outputs are detected by spot-checks and blocklisted.

**Concrete win:** A user with a 4090 who games three hours a night earns enough compute credits during the other 21 to pay for their entire creative workflow. No subscription, no cloud bill.

### 7. CPU-competent engines by design
Several of GSPL's core engines are **CPU-competent by design** — they don't need a GPU at all for acceptable quality:
- **Sprite engine** (Brief 021): CPU-only at full quality. Always runs on any hardware.
- **Modifier-surface DSL** (Brief 023): CPU evaluation, no GPU needed.
- **Lineage walker, gseed crypto, federation, marketplace**: all CPU.
- **CRDT collaborative editing** (Brief 074 INV-212): all CPU.
- **Most of the studio IDE** (Brief 048): CPU.
- **Deterministic lockstep multiplayer** (Brief 074 INV-211): CPU (by construction — the kernel is bit-exact on CPU).

The GPU is only needed for the neural and heavy-render tiers. A massive fraction of real GSPL work — sprite creation, collaborative editing, parameter tuning, federation, marketplace activity, replays, lineage navigation, multiplayer async — runs on a 2015 laptop.

### 8. Automatic tier negotiation
The studio observes the user's hardware, the job's requirements, and available federation capacity, and picks the tier automatically. The user sees a single status: "Rendering final — estimated 2m (local T1) or 12s (federated T3, 0.04 credits)." The user chooses; the substrate routes.

## What GSPL ships at each phase

### v1
- **T0 CPU fallback** mandatory for every engine.
- **T1 integrated-GPU path** for the image engine (quantized Flux Schnell), sprite engine, and critic ensemble.
- **Federated compute v1** with direct-invite peers (Brief 043).
- **Cloud burst opt-in** for one or two cloud providers.
- **INV-215 lineage-attested attestation** for remote jobs.
- **Distilled model marketplace** from day one.
- **WebGPU studio preview** (limited feature set, proof-of-concept).

### v1.5
- **T1 path for neural avatars, NeRF, 3DGS** (quantized, preview quality).
- **DHT-based compute discovery** (find idle GPU peers in the federation).
- **Byzantine spot-checking** via second-peer verification.
- **Full WebGPU studio** with federated finals.
- **Compute marketplace v1** (credit pricing, settlement).

### v2
- **Production distillation pipeline** for community-driven quantization.
- **Byzantine triple-peer verification** for high-stakes renders.
- **Federated training pools** (share idle compute for collective model fine-tuning).
- **Mobile studio** (iOS/Android) with T1 local + T3 federated.

### v3
- **Federated foundation-model training collective** (cross-reference Brief 076).
- **On-device neural rendering at AAA quality** on commodity NPUs as distillation catches up.

## Inventions

### INV-215: Lineage-attested federated compute
Any peer can lease compute cycles to any other peer over federation. Each job is identified by a lineage hash `hash(input_gseed || engine_version || parameters || seed)`. The lender signs an attestation on the output hash. Verification is (a) signature-chain to deterministic kernel contract, (b) optional Byzantine spot-check via a second peer. Attestation travels with the output forever. Novel because no cloud GPU service has cryptographically verifiable-in-perpetuity output attestation; no peer-to-peer compute service has gseed-grained lineage verification.

### INV-216: Tiered-quality preview-to-final execution gradient
Every engine ships with at least T0 (CPU), T1 (iGPU/NPU), T2 (dGPU), and optionally T3 (federated). The runtime auto-routes jobs to the appropriate tier based on user hardware and job quality requirements. Previews are always local; finals can be federated. Novel because no creative tool makes tiered execution a first-class substrate property — most tools either run or don't on a given machine.

### INV-217: CPU-reference kernel as the substrate contract
The deterministic kernel contract (Brief 026) requires every engine to ship a CPU reference implementation that produces bit-identical output to the GPU path. This is not a fallback; it is the contract. GPU implementations are optimizations the substrate verifies against the CPU reference. Novel because no production creative tool treats CPU as the reference implementation for GPU correctness.

## What the dGPU-required competition still does at v1

Honest accounting:
- **AAA neural rendering at 60fps on your own machine** if you have a 4090. GSPL's local T1 on an M2 is maybe 10-20% of that quality; the federated T3 path restores parity but with network latency.
- **Zero-network offline rendering at full quality.** If you have the dGPU you don't need the federation. GSPL doesn't take this away; federation is additive.
- **Deterministic local iteration latency at AAA quality.** Only dGPU owners get this with or without GSPL.

These are real advantages for dGPU-owning users. GSPL does not strip them — it just doesn't require them. The architectural ledger favors GSPL because **everyone else's runtime breaks on non-dGPU hardware**; GSPL's runtime degrades gracefully across four orders of magnitude of hardware capability.

## Risks identified

- **Federation latency for interactive finals.** Lockstep multiplayer and real-time preview need local compute. Mitigation: T0/T1 always run locally; federation is for batch-tolerant finals.
- **Compute market chicken-and-egg.** No lenders, no borrowers. Mitigation: v1 launches with curated compute partners and cloud burst; organic federation grows as the ecosystem scales.
- **Byzantine attestation complexity.** Second-peer verification adds cost. Mitigation: single-peer attestation is the default; Byzantine verification is opt-in for high-stakes renders.
- **Quantization quality loss.** Distilled/quantized models are not pixel-perfect replicas. Mitigation: users can always choose T2/T3 for finals; T1 is for iteration.
- **Provider monopoly risk in cloud burst.** If one cloud dominates, the sovereignty claim is hollow. Mitigation: GSPL ships multiple adapters and forbids any runtime hard-dependency on a single cloud.
- **Idle-peer availability at global scale.** Federation compute needs enough lenders. Mitigation: marketplace pricing adapts; scarce compute costs more credits, which incentivizes more lenders to join.
- **Cheating lenders.** A peer could fake outputs. Mitigation: signature + optional Byzantine spot-check + blocklisting via Brief 061.

## The strategic claim

Every other creative tool says: "Get better hardware." GSPL says: "Hardware is negotiable." The substrate runs on any machine with any degree of acceleration, and the federation provides the rest. **This is a structural advantage as decisive as any invention in the spec because it determines the addressable market.** Unity, Unreal, Houdini, Maya, and MetaHuman are tools for the already-equipped. GSPL is the first professional creative substrate that works from a Chromebook to a 4090 without compromising sovereignty, provenance, or lineage.

## Recommendation

1. **Reverse the "depends on a real GPU" concession.** GSPL runs on any hardware; the federation provides the rest.
2. **Mandate T0 CPU fallback** for every engine as a substrate contract (INV-217).
3. **Ship T1 iGPU/NPU path** for the image engine, sprite engine, and critic ensemble at v1.
4. **Ship INV-215 federated compute v1** with direct-invite peers and one or two cloud burst adapters.
5. **Launch the distilled-model marketplace** at v1 so the community can ship quantized variants.
6. **Ship WebGPU studio proof-of-concept** at v1; full studio at v1.5.
7. **Engage quantization research community** (AWQ, GPTQ, SpinQuant authors) as advisors.
8. **Position as "the creative tool that runs on any computer"** in marketing.
9. **Marketing language:** "Unreal needs your GPU. GSPL needs some GPU, somewhere, or none at all."

## Confidence
**4/5.** The execution-tier architecture is well-understood; federated compute is the newer piece and the risk lives in the economics of the compute market, not the cryptography. 4/5 reflects honest uncertainty about how fast the federation reaches self-sustaining lender density.

## Spec impact

- `architecture/tiered-execution.md` — new doc.
- `architecture/federated-compute.md` — new doc.
- Update Brief 026 to make CPU reference the substrate contract (INV-217).
- Update Brief 054 to add the tiered-execution gradient explicitly.
- Update Brief 055 to reflect cloud burst as opt-in, federation as primary.
- New ADR: `adr/00NN-lineage-attested-federated-compute.md`.
- New ADR: `adr/00NN-cpu-reference-as-substrate-contract.md`.
- Remove the "depends on a real GPU" concession from `round-2-synthesis.md`.

## Open follow-ups

- Design the compute marketplace pricing mechanism in detail.
- Pick WebGPU runtime (wgpu-web, Dawn, or browser-native).
- Build INV-215 prototype with two-peer Byzantine spot-check.
- Engage quantization research community on v1 distillation pipeline.
- Benchmark T1 quality vs T2 quality for the image engine on Apple M-series.
- Legal review of peer-to-peer compute liability per jurisdiction.

## Sources

- WebGPU specification (W3C).
- wgpu Rust implementation.
- ONNX Runtime documentation.
- Apple Core ML and Neural Engine documentation.
- AWQ, GPTQ, SpinQuant, SmoothQuant quantization papers.
- Stable Diffusion distillation literature (SDXL Turbo, LCM, Flux Schnell).
- BOINC / Folding@home peer compute architectures (prior art for volunteer compute).
- Render-network and akash compute marketplaces (prior art for crypto-denominated GPU markets).
- libp2p specification.
- Internal: Briefs 020, 026, 027, 043, 044, 054, 055, 057, 061, 071, 072, 073, 074.
