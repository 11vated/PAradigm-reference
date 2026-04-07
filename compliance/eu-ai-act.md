# EU AI Act Compliance

## Scope

The EU Artificial Intelligence Act (Regulation (EU) 2024/1689) entered into force in August 2024 with phased application dates running through 2027. The provision most relevant to Paradigm is **Article 50: Transparency obligations for providers and deployers of certain AI systems**, which becomes applicable on **2 August 2026**.

Article 50(2) requires that providers of AI systems generating synthetic image, audio, video, or text content "ensure that the outputs of the AI system are marked in a machine-readable format and detectable as artificially generated or manipulated."

Paradigm is squarely within scope: it generates synthetic images (sprites, textures, environments), audio (music seeds), video (animation exports), and arguably text (gene-tree explanations). It is therefore subject to Article 50(2) for all EU users, and by our compliance principle of conservative-by-default, for all users globally.

## Disclaimer

This document describes how Paradigm engineers compliance into the product. It is **not legal advice**. Paradigm Inc. retains EU AI counsel for the formal compliance posture, and the engineering compliance described here is informed by but not a substitute for that counsel.

## Article 50(2) requirements

The text of Article 50(2) imposes three concrete obligations on Paradigm as a provider:

1. **Machine-readable marking** — outputs must carry a marker that machines can detect. Recital 133 names "watermarks, metadata identifications, [or] cryptographic methods" as examples and explicitly references the work of standards bodies, including C2PA, on technical solutions.
2. **Effective and reliable** — the marking must be "as far as technically feasible" robust against removal, including by adversaries. Perfect robustness is not required, but trivial stripping (e.g., a single field that any tool would clear) is insufficient.
3. **Interoperable** — the marking should be in a standard format so downstream tools can read it without special-case handling per provider.

C2PA satisfies all three: it is machine-readable, it is cryptographically signed (so tampering is detectable even if not preventable), and it is the de-facto interoperable format.

## How Paradigm satisfies Article 50(2)

| Requirement | Paradigm response | Where implemented |
|---|---|---|
| Machine-readable mark on every synthetic output | C2PA manifest embedded in every export and `.gseed` | `compliance/c2pa.md`, `infrastructure/gseed-format.md` |
| Detectable as artificially generated | `c2pa.actions[].action == "c2pa.ai_generated"` with `digitalSourceType` of `algorithmicMedia` | `c2pa.md` §"The c2pa.actions assertion" |
| Robust against trivial stripping | ECDSA-signed manifest; tampering breaks the signature; manifests embedded in format-native metadata containers, not added as a separate file | `c2pa.md` §"Where manifests live" |
| Interoperable | Adobe, Microsoft, BBC, and other major platforms read C2PA natively | C2PA 2.0 spec |

## Article 50(4) — content disclosure to natural persons

Article 50(4) imposes an additional obligation specifically on deployers of AI image, audio, or video systems that generate or manipulate content depicting persons, objects, places, or events that "would falsely appear to a person to be authentic." For most Paradigm output (sprites, fictional characters, abstract music) this provision doesn't apply because the content is overtly stylized.

But Paradigm has a special case: the **Realistic** sprite style and the **Photoreal** texture engine. These produce output that could plausibly be mistaken for photography. For seeds tagged with these styles, Paradigm:

1. Adds a visible label to the Studio render: "AI-generated content."
2. Exports include a corner watermark by default (toggleable in Studio for the seed author, not for downstream consumers).
3. The C2PA manifest carries an additional `c2pa.actions[].action == "c2pa.deepfake_disclosure"` extension where applicable.

## Article 50(1) — interaction with chatbots

The GSPL Agent is a conversational interface; users talk to it in natural language. Article 50(1) requires that users be informed they are interacting with an AI system unless this is obvious from context.

Paradigm's Studio always shows a clear "AI Agent" header on the chat panel, and the very first message in any conversation is system-supplied: "I'm the GSPL Agent. I'll help you create and refine seeds. Everything I make is AI-generated and labeled as such."

This satisfies Art. 50(1).

## Article 50(5) — accessibility of disclosures

Article 50(5) requires that the information provided under Art. 50 be presented "in a clear and distinguishable manner at the latest at the time of the first interaction or exposure" and "shall conform to the applicable accessibility requirements." Paradigm's Studio is WCAG 2.2 AA compliant (see `compliance/wcag.md`), and the AI disclosure on first interaction is rendered with the same accessibility level as the rest of the UI.

## Risk classification

Paradigm is **not** a high-risk AI system under Annex III of the AI Act. It is general-purpose creative content generation. The applicable obligations are therefore those of Article 50 (transparency) and the general obligations on providers in Articles 53-55 to the extent the GSPL Agent constitutes a "general-purpose AI model" — which it does not, because it is built on top of third-party foundation models, not itself a foundation model. The third-party providers (Anthropic, OpenAI) carry the GPAI obligations for their models.

If future versions of Paradigm fine-tune or train models in-house at scale, this analysis would need to be revisited.

## Operational compliance

Beyond the technical marking, Paradigm maintains:

- A public **Acceptable Use Policy** that prohibits using Paradigm to generate content that would be illegal under EU law (CSAM, non-consensual intimate imagery, election disinformation depicting real people).
- A **content moderation pipeline** that rejects prompts matching known harmful patterns at the GSPL Agent intent-classification stage.
- A **transparency report** published annually documenting takedown counts and abuse categories.
- A **point of contact** in the EU (a "representative" within the meaning of Art. 22) listed at `paradigm.app/legal/eu-representative`.
- An **incident reporting** workflow into the EU AI Office should any "serious incident" within the meaning of Art. 73 occur.

## Audit trail

For every seed produced, Paradigm logs in `agent_runs`:

- The user who initiated the run
- The provider and model used
- The prompt (encrypted at rest)
- The intent classification
- The resolved spec
- The construction plan
- The output seed hash
- The exact agent version

This log is retained for at least 5 years and is the source of truth for any post-hoc compliance inquiry. It also feeds the C2PA manifest's `org.paradigm.gspl-agent` assertion.

## Open questions

These are tracked for legal review and may shift the engineering response:

1. **Transitional period** for Article 50(2): the 2 August 2026 application date is firm, but the European Commission has not yet published the implementing standards under Article 50(7). C2PA is the most likely candidate but is not formally adopted as of this writing.
2. **Watermarking requirement**: some commentators argue Article 50(2) implies a *visible* perceptual watermark in addition to metadata. Paradigm's current posture (metadata only by default, visible watermark only for photorealistic styles) is conservative but may need to expand.
3. **Cross-border enforcement**: the AI Office will publish enforcement guidelines in 2026; the engineering posture may need to track those.

These items are reviewed quarterly with EU counsel.

## References

- Regulation (EU) 2024/1689 — full text in EUR-Lex
- Article 50 — Transparency obligations for providers and deployers
- Recitals 132-134 — context for Article 50 requirements
- C2PA 2.0 Specification — https://c2pa.org
- `compliance/c2pa.md` — implementation details
- `compliance/ca-sb-942.md` — parallel California regime
