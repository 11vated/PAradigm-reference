# 067 — Creator platforms: Roblox, Dreams (PS), Inworld

## Question
Roblox, Sony's Dreams, and Inworld are *creator platforms* — environments where users make games and interactive experiences inside a hosted ecosystem. They're the closest analogs to GSPL's "make a whole game from a conversation" ambition. How does GSPL relate, what does it absorb, and what is structurally different?

## Why it matters
Creator platforms have proven that millions of non-technical users *will* make interactive content if the tooling is right. They've also each hit a ceiling — Roblox is locked to its own engine and IP terms; Dreams was beautiful but trapped on PS4/PS5; Inworld is character-AI-as-a-service. GSPL must learn from each: what they got right, where they hit a wall, and how a sovereignty-first generative substrate clears that wall.

## What we know from the spec
- Brief 029-034: agent and conversational interface.
- Brief 044: marketplace.
- Brief 048: studio is a desktop tool, not a hosted platform.
- Brief 047: anonymous publication mode.
- Brief 014: cross-engine breeding.

## Findings — competitor profiles

### Roblox
**Operator:** Roblox Corporation; hosted platform.
**Architecture:** Roblox Studio (desktop authoring tool, free) + Roblox Player (hosted multiplayer runtime). Lua scripting. Marketplace for assets. In-experience economy with Robux.
**Strengths:**
- 70M+ daily active users.
- Lowered the barrier to interactive creation enormously — kids ship games.
- Marketplace with millions of assets and ongoing creator revenue.
- Multiplayer-first; networking is solved.
- Cross-platform deploy (mobile, console, desktop, VR).
- Built-in monetization with Robux.
- Mature creator economy with payouts in real currency.

**Weaknesses:**
- Locked to Roblox engine; no export.
- IP terms heavily favor Roblox; creator content lives on Roblox servers.
- 30% platform fee; effective cut higher after Robux conversion.
- Aesthetic constrained by Roblox engine.
- AI features are nascent and centrally controlled (Code Assist, Material Generator).
- Content moderation is centralized and inconsistent.
- No sovereignty whatsoever.
- Child safety controversies and labor critiques.

### Dreams (Media Molecule, Sony)
**Operator:** Sony / Media Molecule; PlayStation exclusive; abandoned 2024.
**Architecture:** PlayStation-only creation tool with sculpting, animation, logic, audio, music — all inside one application. "Imp" cursor as the universal pointer. Visual scripting.
**Strengths:**
- Most ambitious creation platform ever shipped to consumers.
- Multi-modal creation in one tool: sculpt + paint + animate + script + sound design.
- Beautiful UI with low floor and high ceiling.
- Strong community of remixers; remix counts visible.
- Free-form aesthetic; users built everything from realistic environments to abstract music.
- Tight integration of creation and play.

**Weaknesses:**
- PS4/PS5 only; no PC, no export.
- Controller-driven; no mouse/keyboard support meaningfully.
- Sales were disappointing; Sony abandoned the project.
- No marketplace beyond in-game discovery.
- No external IP; everything stays in Dreams.
- Content was siloed and is now at risk as servers wind down.

### Inworld
**Operator:** Inworld AI; hosted SaaS for AI characters.
**Architecture:** AI character creation platform. Define personality, voice, knowledge, goals; deploy as NPC in games via SDK.
**Strengths:**
- Best-in-class AI character behavior for game NPCs.
- Integrations with Unity, Unreal, web.
- Voice synthesis, emotion, memory, goals all built-in.
- Used by indie and AA studios for NPC dialog and behavior.

**Weaknesses:**
- Hosted; per-conversation API cost.
- Closed model under the hood.
- Limited to character behavior; not a full creation platform.
- Subscription-locked.
- No sovereignty; characters live on Inworld's infrastructure.

## Axis-by-axis comparison

| Axis | Roblox | Dreams | Inworld | GSPL |
|---|---|---|---|---|
| Local execution | partial (Studio) | console-only | ❌ | ✅ |
| Open architecture | ❌ | ❌ | partial | ✅ |
| Multi-modal creation | partial | ✅ | ❌ | ✅ |
| Conversational AI authoring | ❌ | ❌ | ❌ | ✅ |
| Lineage of creation | ❌ | partial (remix tree) | ❌ | ✅ |
| Provenance / signed identity | ❌ | ❌ | ❌ | ✅ |
| Marketplace with royalties | ✅ (Roblox cut) | ❌ | ❌ | ✅ (no platform cut) |
| Cross-engine export | ❌ | ❌ | partial (SDK) | ✅ |
| Sovereignty | ❌ | ❌ | ❌ | ✅ |
| Federation | ❌ | ❌ | ❌ | ✅ |
| Built-in monetization | ✅ | ❌ | ❌ | ✅ via marketplace |
| Aesthetic ceiling | mid | high | n/a | high |
| Multiplayer runtime | ✅ | ✅ (peer-to-peer in-app) | n/a | ❌ (substrate, not engine) |
| AI character behavior | basic | basic | ✅ | ✅ |
| First-time user wow | high | high | mid | targeted high |
| Audience size | massive | small | dev-only | TBD |

## What GSPL absorbs

### From Roblox
- **Lowered the floor for non-technical creation.** GSPL's conversational interface (Brief 049) is the spiritual successor.
- **Creator economy with real-money payouts.** GSPL marketplace (Brief 044) has this without the platform-gatekeeper cut.
- **Templates as starting points.** Brief 051 ships six default templates; the Roblox Library is the model.
- **Cross-platform deploy mindset.** GSPL exports to multiple engines instead of running its own platform.

### From Dreams
- **Multi-modal in one tool.** This is the thesis. Dreams proved it's possible; GSPL takes it further with AI generation and sovereignty.
- **Imp cursor → conversational interface.** Both are universal-pointer abstractions; conversation is the new universal pointer.
- **Remix tree → lineage DAG.** Dreams had a remix counter; GSPL has the full graph (Brief 052).
- **Beautiful, opinionated UI for creation.** Brief 049 is heavily inspired.
- **High-ceiling/low-floor balance.** The hardest UX problem; Dreams cracked it on console; GSPL targets it on desktop.

### From Inworld
- **AI characters as first-class authoring objects.** GSPL ships dialog (Brief 002) and the agent supports persona authoring at v1.5.
- **Integration via SDK to game engines.** GSPL exports characters as engine-importable assets.
- **Voice + emotion + memory + goals as the character bundle.** v1.5 character engine.

## What is structurally impossible for them to copy

### Sovereignty
Roblox runs on Roblox servers. Dreams ran on PSN. Inworld runs on Inworld's API. None can become local-first without abandoning their business model.

### Federation
None of them federate. Roblox is one company; Dreams was one company; Inworld is one company. GSPL's federation (Brief 043) means no single entity can shut it down.

### Cross-engine export
Roblox has no export. Dreams had no export. Inworld has SDK integrations but the brain is hosted. GSPL exports everything (Brief 065).

### No platform cut
Roblox takes ~30% (effective rate higher with Robux conversion). GSPL marketplace has no platform cut at v1 (Brief 044). This is a constitutional commitment.

### Lineage as data
None of them have first-class lineage. Dreams had a remix counter; that's not lineage.

### IP ownership stays with creator
Roblox's IP terms are infamous. GSPL ships c2pa attestations and signed identity from day one (Brief 008, 042); IP is bound to the creator's signature.

## Strategic positioning

GSPL is the **anti-Roblox**: same ambition (millions of non-technical creators making interactive content), opposite values (sovereignty over hosting, no platform cut over Roblox's 30%, cross-engine export over lock-in, federation over centralization).

GSPL is the **fulfillment of Dreams**: same multi-modal-creation thesis, opposite distribution (PC + Mac + Linux desktop instead of console exclusive, open weights instead of proprietary, marketplace instead of in-app discovery only).

GSPL is the **substrate Inworld should have been**: same AI-character ambition, opposite architecture (local + signed instead of hosted SaaS).

## Risks identified

- **Roblox-scale audience requires multiplayer runtime.** GSPL doesn't have one. Mitigation: GSPL is a substrate; the multiplayer runtime is the engine (Unity/Unreal/Godot per Brief 065). Users export to a runtime that already has multiplayer.
- **Dreams' lesson: creator platforms can fail commercially even if they're loved.** Mitigation: GSPL doesn't depend on a single platform's economics; it's open-source and federated.
- **Inworld's lesson: AI characters as a service has a margin problem.** Mitigation: GSPL runs locally; no per-conversation API cost.
- **Network effect gap:** Roblox has 70M DAU; GSPL starts at 0. Mitigation: federated marketplace lowers the network-effect requirement; users don't need a single huge platform to find each other.
- **Content discovery:** Roblox's discovery is centralized and effective. GSPL's federation is harder to discover in. Mitigation: federated indexers (Brief 043); reputation as discovery primitive.
- **Onboarding:** Roblox got kids creating in 30 minutes. GSPL has to match that. Mitigation: Brief 051's first-wow target.

## Recommendation

1. **Position GSPL as the anti-Roblox / fulfillment of Dreams.** Public messaging acknowledges these as ancestors.
2. **No platform fee** in the marketplace. Constitutional. (Brief 044.)
3. **Cross-engine export from day one.** (Brief 065.)
4. **Conversational interface for low-floor entry.** (Brief 049.)
5. **AI character engine at v1.5** with persona, voice, memory, and goals.
6. **First-wow ≤5 min** matches Roblox/Dreams onboarding bar.
7. **Federated discovery** at v1.5; reputation as primary signal.
8. **Marketing language**: "What if Dreams escaped the PlayStation? What if Roblox was yours? What if you owned the IP and the server didn't exist?"

## Confidence
**3/5.** Creator platforms are the hardest competitive frame because they involve community, economy, AND tooling. The 3/5 reflects honest uncertainty about whether GSPL's federation can match centralized discovery effectiveness.

## Spec impact

- `marketing/competitive-creator-platforms.md` — public positioning.
- `architecture/character-engine.md` — v1.5 character engine spec.
- New ADR: `adr/00NN-substrate-vs-platform.md`.

## Open follow-ups

- Plan v1.5 character engine.
- Build federated discovery prototype.
- Engage Dreams creator community as early users.
- Publish "anti-Roblox manifesto" as a positioning piece.
- User research on Roblox creators about what they would want if they could leave.

## Sources

- Roblox developer documentation and creator economy reports.
- Media Molecule, *Dreams* postmortems and GDC talks.
- Inworld AI documentation.
- *Hit Makers* (Thompson) on Roblox cultural dynamics.
- Internal: Briefs 002, 008, 014, 029-034, 042-044, 047, 048, 049, 051, 052, 065.
