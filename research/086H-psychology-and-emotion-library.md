# 086H — Psychology, emotion, and behavior library

## Question
What psychology, emotion, behavior, expression, and personality data must GSPL ship at v1 so that any character a creator invokes has access to validated emotion, expression, personality, and behavior primitives — and so that performance is grounded in real psychological science rather than caricature?

## Why it matters
A character is *a person*. They feel, decide, react, perform. Their face moves in measurable ways. Their voice carries measurable affect. Their personality has measurable structure. If GSPL ships only "happy / sad / angry," every character is a cartoon. If it ships **FACS-grade facial action coding, vocal affect parameters, validated personality models, and behavior libraries from peer-reviewed psychology**, performance becomes a substrate creators compose — and AI-driven characters become believable rather than uncanny.

## What we know from the spec
- Brief 073: photoreal humans.
- Brief 085: biology and anatomy (facial muscles, vocal tract).
- Brief 086C: audio (vocal affect).

## Findings — what GSPL ships at v1

### 1. Facial expression — FACS-grade
- **All 46 Action Units (AUs)** from Ekman's Facial Action Coding System with measured muscle activation patterns mapping to Brief 085 facial musculature.
- **AU intensities** (A → E, trace → max).
- **Compound expressions** (Du, Tao, Martinez 2014 — 22 validated compound expressions: happily surprised, sadly fearful, angrily disgusted, etc.).
- **Microexpressions** with timing parameters from Ekman's research.
- **Cultural display rules** documented per culture (consumes Brief 086E).
- **Subtle expressions** (cheek raise, eyebrow flash, lip press) for nuanced performance.

**Source:** Ekman & Friesen FACS Manual, Du et al. *Compound Facial Expressions of Emotion* (PNAS 2014), peer-reviewed affective science literature.

### 2. Body language and posture
- **Posture taxonomy:** open, closed, expansive, contractive, leaning, mirroring, oriented toward/away.
- **Gesture libraries:** emblematic (culture-specific), illustrative (beat, deictic, iconic, metaphoric), affective, regulators, adaptors.
- **Cultural gesture variants** with source-culture attribution (Brief 086E).
- **Proxemics** (Hall's intimate, personal, social, public distances with cultural variants).
- **Walking gait variants** by mood, age, situation (consumes Brief 085 gait library).

**Source:** McNeill *Hand and Mind*, Hall *The Hidden Dimension*, Eibl-Eibesfeldt *Human Ethology*, peer-reviewed nonverbal communication literature.

### 3. Vocal affect
- **Prosodic affect parameters:** F0 (mean, range, variability), intensity, speech rate, jitter, shimmer, voice quality (modal, breathy, creaky, falsetto, harsh).
- **Affective vocal templates** for joy, sadness, anger, fear, disgust, surprise, contempt — peer-reviewed and cross-culturally validated.
- **Cultural prosody variants.**
- **Laugh, cry, sigh, gasp, scream** vocal primitives.
- **Speech disfluencies** (filled pauses, repairs, restarts) for naturalistic dialogue.

**Source:** Scherer affect bursts research, Banse & Scherer vocal expression studies, IEMOCAP, RAVDESS emotion corpora.

### 4. Emotion models
- **Discrete emotion model** (Ekman's 6 basic + Plutchik's 8 + extended set with cultural validation).
- **Dimensional model:** Russell's circumplex (valence × arousal), PAD (pleasure-arousal-dominance), Watson-Tellegen.
- **Appraisal models:** OCC (Ortony, Clore, Collins), Scherer's component process model.
- **Cultural emotion variants** (e.g., amae, saudade, hygge, sisu, schadenfreude, mono no aware) — with source culture attribution.
- **Mixed and conflicting** emotions.

**Source:** Ekman, Plutchik, Russell, OCC, Scherer literature; Affective Norms for English Words (ANEW); WordNet-Affect.

### 5. Personality models
- **Big Five (OCEAN)** with measured trait facets (NEO-PI-R-style).
- **HEXACO** model.
- **MBTI** (with documentation that it is popular but not psychometrically rigorous — for legacy compatibility, not as a recommended substrate).
- **Dark Triad / Tetrad** (with restraint — for villain depiction, not for real-person profiling).
- **Attachment styles** (secure, anxious, avoidant, disorganized).
- **Temperament models** (Thomas-Chess, Rothbart).
- **Personality → behavior priors** for character animation: trait scores bias gait, posture, gesture frequency, prosody, expression baseline.

**Source:** Costa & McCrae NEO literature, HEXACO publications, peer-reviewed personality psychology.

### 6. Cognition and decision
- **Cognitive bias library:** anchoring, availability, confirmation, hindsight, dunning-kruger, attribution, framing, etc. — for writing realistic decision-making.
- **Memory models:** sensory, working, long-term (episodic, semantic, procedural), forgetting curves.
- **Attention models** for visualization of focus.
- **Theory of mind** primitives for multi-character scenes.
- **Moral foundations** (Haidt: care, fairness, loyalty, authority, sanctity, liberty) for character belief modeling.

**Source:** Kahneman *Thinking Fast and Slow*, peer-reviewed cognitive psychology; Moral Foundations Theory (Haidt et al.).

### 7. Mental states and clinical (depiction-grade only)
- **Mood states:** elated, content, neutral, low, dysphoric.
- **Stress and fatigue** parameter axes.
- **Sleep/wake cycle** parameters.
- **Clinical conditions** (depiction-grade only): anxiety, depression, PTSD, bipolar, schizophrenia, ADHD, autism — each with **mandatory care contract**:
  - Substrate ships *respectful, validated* depiction parameters drawn from lived-experience consultants.
  - Substrate refuses to ship *diagnostic* tools or *self-diagnosis* affordances.
  - Stigmatizing tropes are documented as such and flagged for creator awareness.
  - Source consultants attributed in lineage.

**Source:** APA DSM-5 (depiction reference only, not diagnostic substrate), lived-experience consultancies, mental health advocacy organizations.

### 8. Social and group dynamics
- **Relationship taxonomies** (kin, friend, colleague, acquaintance, romantic, mentor, rival, enemy).
- **Group dynamics** templates (in-group/out-group, hierarchy, conformity, leadership styles).
- **Conversation primitives:** turn-taking, repair, backchannel, alignment.

## Findings — psychology gseed structure

```
psy://au/AU12@v1.0          → lip corner puller (zygomaticus major)
psy://expression/joy@v1.0   → AU6 + AU12 with intensity profile
psy://prosody/sadness@v1.0
psy://emotion/discrete/disgust@v1.0
psy://personality/big-five/(O80,C40,E60,A70,N30)@v1.0
psy://gesture/emblem/yoruba/respect-bow@v1.0
psy://state/depiction/anxiety-mild@v1.0  [care_contract:true, consultants:[...]]
```

A "tense conversation between an anxious teenager and her authoritative father in 2025 Tokyo" composes psy://personality/teen, psy://state/anxiety-mild, psy://emotion/conflicting/(fear+resentment), gestures from culture://japan, prosody from audio://japanese, AU sequences for the facial performance — every parameter measured, attributed, and lineage-tracked.

## Inventions

### INV-338: FACS-grade performance substrate
Facial action units, body posture, prosodic affect, and personality priors are signed substrate primitives that compose into validated character performance. The differentiable rigger (Brief 085 INV-208) consumes them directly. Novel because no creative tool ships psychological primitives at this granularity as substrate — they live in proprietary mocap pipelines or per-project hacks.

### INV-339: Mental health depiction care contract
Clinical mental state gseeds carry mandatory care contracts: lived-experience consultant attribution, stigma-trope flagging, and refusal to function as diagnostic tools. Novel as a substrate-level care contract for sensitive psychological depiction.

## Phase 1 deliverables

- **All 46 FACS AUs + 22 compound expressions** at v1.
- **Body language, gesture, proxemics** primitives with cultural variants at v1.
- **Vocal affect parameters** wired to Brief 086C synthesis at v1.
- **Discrete + dimensional + appraisal emotion models** at v1.
- **Big Five + HEXACO + attachment + temperament** personality models at v1.
- **Cognitive bias + memory + theory-of-mind** primitives at v1.
- **Depiction-grade clinical states** with care contracts at v1.
- **Personality → behavior prior wiring** to the differentiable rigger at v1.

## Risks

- **Stigma harm in clinical depiction.** Mitigation: care contract is non-negotiable; lived-experience consultants attributed.
- **Cross-cultural validity.** Mitigation: cultural variants documented; not all models claim universality.
- **Misuse for real-person profiling.** Mitigation: substrate refuses to map gseeds onto identified real persons (Brief 088 enforces).

## Recommendation

1. **Lock v1 to FACS + compound + Big Five + OCC + cultural variants.**
2. **Sign all gseeds** under GSPL Foundation Identity.
3. **Build the mental-health care contract** as a v1 substrate commitment.
4. **Engage Ekman Group, lived-experience consultancies, peer reviewers** as upstream partners.
5. **Wire personality priors** into the differentiable rigger.

## Confidence
**4/5.** Source science is mature; the care work is non-trivial.

## Spec impact

- `inventory/psychology.md` — new doc.
- `inventory/performance-schema.md` — new doc.
- New ADR: `adr/00NN-mental-health-depiction-care-contract.md`.

## Open follow-ups

- Lived-experience consultant engagement plan.
- FACS implementation in differentiable rigger.
- Cross-cultural emotion validation audit.

## Sources

- Ekman & Friesen *Facial Action Coding System*.
- Du, Tao, Martinez *Compound Facial Expressions of Emotion* (PNAS 2014).
- Plutchik *Emotion: A Psychoevolutionary Synthesis*.
- Russell circumplex model literature.
- Ortony, Clore, Collins *The Cognitive Structure of Emotions*.
- Scherer component process model literature.
- Costa & McCrae NEO-PI-R.
- Lee & Ashton HEXACO publications.
- Haidt *The Righteous Mind* and Moral Foundations.
- Kahneman *Thinking, Fast and Slow*.
- McNeill *Hand and Mind*.
- Hall *The Hidden Dimension*.
- IEMOCAP, RAVDESS emotion corpora.
- Affective Norms for English Words (ANEW).
- WordNet-Affect.
- APA DSM-5 (depiction reference only).
- Internal: Briefs 073, 085, 086C, 086E, 088.
