# 085 — Biology and anatomy library

## Question
What biology and anatomy data must GSPL ship at v1 so that any character, creature, plant, organ, cell, or microbe can be rendered, animated, and simulated with anatomical accuracy?

## Why it matters
A user asks for "a wolf running," "a dancer's spine in motion," "a beating human heart," "a cell dividing," "a bird's wing in slow motion," "a tree growing." Each is an anatomy and biology problem. GSPL must ship the **structural truth of every common life form** so creators are never inventing biology from scratch. This is also the foundation for the photoreal humans work (Brief 073).

## What we know from the spec
- Brief 073: photoreal humans.
- Brief 081: chemistry (biochemistry).
- Brief 083: materials (skin primitive).
- Brief 088: character canon.

## Findings — what GSPL ships at v1

### 1. Skeletal systems
**Full skeletal models** for:

- **Human:** 206 bones, named, with measured length distributions, joint types, ROM (range of motion) limits, and rigging weights. Sourced from BodyParts3D, Visible Human Project, OpenAnatomy, Z-Anatomy.
- **Mammals (50 species):** wolf, dog, cat, lion, tiger, bear, deer, elk, moose, horse, cow, pig, sheep, goat, rabbit, mouse, rat, squirrel, raccoon, fox, otter, seal, whale, dolphin, elephant, giraffe, hippopotamus, rhinoceros, zebra, kangaroo, koala, opossum, bat, hedgehog, primates (chimpanzee, gorilla, orangutan, gibbon, baboon, macaque, lemur), and 12 more.
- **Birds (20 species):** eagle, hawk, owl, falcon, sparrow, robin, crow, raven, parrot, hummingbird, ostrich, penguin, duck, swan, chicken, turkey, dove, woodpecker, kingfisher, flamingo.
- **Reptiles (15 species):** snake (multiple), lizard, gecko, iguana, crocodile, alligator, turtle, tortoise, dragon-equivalent (Komodo).
- **Fish (20 species):** shark, salmon, trout, tuna, swordfish, marlin, eel, koi, goldfish, anglerfish, octopus (cephalopod skeleton), squid.
- **Insects (20 species):** ant, bee, butterfly (multiple), beetle, dragonfly, mantis, grasshopper, spider, scorpion, crab, lobster, shrimp.
- **Mythological creatures** as composable rigs: dragon (theropod + bat wings), unicorn (horse + horn), griffin (eagle + lion), centaur (human + horse), phoenix (bird + flame), kraken (octopus + scale).

Each rig is a signed gseed with stable IK chains, named bone hierarchy, ROM constraints, and pose libraries (idle, walk, run, jump, attack, sleep, etc.).

**Source:** BodyParts3D, Visible Human Project (NLM), Z-Anatomy, OpenAnatomy (Brigham Women's), Mixamo (rigging conventions), Smithsonian 3D digitization, MorphoBank, DigiMorph, FishBase.

### 2. Muscular systems
- **Human:** 600+ named muscles with origin, insertion, function, antagonist pairs, fiber direction.
- **Mammals:** comparable detail for top 20 species (wolf, horse, cat, dog, primate variants).
- **Mocap-friendly muscle activation maps** linking joint motion to muscle contraction patterns.

Used by the differentiable rigger (Brief 073 INV-208) for physically-plausible motion.

**Source:** Gray's Anatomy (public domain), Visible Human Project, OpenSim biomechanics models, BodyParts3D.

### 3. Organ systems
- **Human:** all major organs (brain, heart, lungs, liver, kidneys, stomach, intestines, spleen, pancreas, bladder, reproductive) with 3D meshes, vasculature, innervation, and animatable functional models.
- **Cardiovascular:** beating heart with electrical conduction (SA node, AV node, Purkinje fibers), full arterial and venous trees from peer-reviewed cardiovascular models.
- **Respiratory:** breathing lungs with airway tree (Weibel model), gas exchange.
- **Nervous:** brain regions (Allen Brain Atlas), spinal cord, peripheral nerve trees.
- **Digestive:** full GI tract with peristalsis simulation primitive.

**Source:** Visible Human, BodyParts3D, OpenAnatomy, Allen Brain Atlas, Weibel respiratory model, Heart of the Matter cardiac models.

### 4. Cellular and microbial
- **Common cell types:** epithelial, neuron, muscle (smooth/skeletal/cardiac), red and white blood cells, stem, fibroblast, adipocyte, hepatocyte, beta cell, melanocyte, photoreceptor.
- **Cell organelles:** nucleus, mitochondria (with cristae), ER, Golgi, ribosomes, lysosomes, cytoskeleton (actin, microtubules, intermediate filaments).
- **Microbes:** common bacteria (E. coli, Staph, Strep, Mycobacterium tuberculosis, Lactobacillus, etc.), archaea, common fungi, common protists.
- **Viruses:** SARS-CoV-2, influenza, HIV, herpes, adenovirus, bacteriophage T4 — accurate capsid structures.

Used for biology educational visualization, scientific illustration, and any creative work that depicts microscopic life.

**Source:** RCSB PDB, EM Data Bank, Allen Cell Explorer, NCBI Taxonomy.

### 5. Plants
- **Tree species (50):** oak, maple, pine, birch, elm, beech, willow, palm, baobab, sequoia, redwood, juniper, fir, spruce, cherry, apple, mango, banana, eucalyptus, etc. Each with growth model parameters (L-system rules), leaf morphology, bark texture, age-to-size curves.
- **Flowering plants (100):** rose, lily, sunflower, tulip, orchid, daisy, etc.
- **Grasses, mosses, ferns, mushrooms, seaweeds.**
- **Crop plants:** wheat, rice, corn, potato, tomato, etc.
- **L-system grammars** for procedural generation.
- **Phyllotaxis parameters** for accurate leaf arrangement.

**Source:** Encyclopedia of Life (EOL), Tree of Life Web Project, USDA PLANTS, Kew Gardens, peer-reviewed botany.

### 6. Locomotion and behavior libraries
For each major species, the library ships **canonical motion patterns**:

- **Gaits:** walk, trot, canter, gallop, leap, slither, swim, fly (flap, glide, soar).
- **Behaviors:** idle, alert, hunt, eat, drink, sleep, fight, flee, mate, communicate.
- **Expressions and signals:** species-appropriate facial and body expressions.

These are **gseeds** that the user can apply to a rig with one drag, or compose with custom motion via breeding.

**Source:** Mixamo, mocap libraries, biomechanics literature, ethology references.

### 7. Aging and growth
Every biological gseed accepts an **age parameter** (0 = newborn → 1 = death) that drives:

- Skeletal proportions (juvenile → adult → elderly).
- Muscle mass distribution.
- Skin material aging (wrinkles, pigmentation shift, loss of elasticity).
- Hair density and color.
- Posture and ROM changes.

This is the substrate's answer to "draw this character at every age" without manual rework.

## Findings — biology gseed structure

```
bio://human/skeleton/female@v1.0
bio://wolf/full-rig@v1.0
bio://heart/beating@v1.0
bio://cell/neuron@v1.0
bio://tree/oak/quercus-robur@v1.0
bio://gait/wolf/gallop@v1.0
bio://expression/human/smile@v1.0
```

Each is signed by GSPL Foundation, immutable, forkable, and lineage-tracked.

## Inventions

### INV-320: Composable rigs as signed substrate primitives
Skeletal, muscular, and organ rigs are signed gseeds with stable joint hierarchies, ROM constraints, and pose libraries. Mythological creatures are composable (dragon = theropod skeleton + bat wings + crocodile head). Novel because no creative tool ships rigs as composable substrate-level primitives — they're project-specific assets in every other tool.

### INV-321: Biology age-parameter as substrate primitive
Every biological gseed accepts an age parameter that drives skeletal, muscular, and skin changes via measured growth and aging models. "Draw my character at age 8, 25, 70" becomes a single parameter sweep. Novel as a substrate-level temporal-state for biology.

## Phase 1 deliverables

- **Human full rig** (skeletal, muscular, organ) at v1.
- **50 mammal rigs** at v1.
- **20 bird rigs, 15 reptile rigs, 20 fish rigs, 20 insect/arthropod rigs** at v1.
- **6 mythological composite rigs** at v1.
- **50 plant species** with L-system growth at v1.
- **Canonical gait and behavior libraries** for top 20 species at v1.
- **Cellular and microbial** primitives for science visualization at v1.

## Risks

- **3D mesh licensing.** Many anatomy resources are restricted. Mitigation: BodyParts3D, OpenAnatomy, Visible Human, Z-Anatomy are open; commission additional captures via federation if needed.
- **Library size.** All rigs together ≈ several GB. Mitigation: lazy load from federation knowledge graph; ship core 20 species locally.
- **Cultural sensitivity for mythological creatures.** Mitigation: source mythologies are documented and attributed (Brief 086E).

## Recommendation

1. **Lock the v1 species list** to the inventory above.
2. **Sign all rigs** under GSPL Foundation Identity.
3. **Build the composability protocol** for mythological creatures.
4. **Ship the age parameter** as a substrate-level rig contract.
5. **Engage BodyParts3D, OpenAnatomy, Z-Anatomy** as upstream partners.

## Confidence
**4.5/5.** The data exists and is mostly open; engineering effort is curation, rigging, and standardizing the schema.

## Spec impact

- `inventory/biology.md` — new doc.
- `inventory/anatomy-schema.md` — new doc.
- Update Brief 073 to consume biology library for human anatomy.
- New ADR: `adr/00NN-composable-rigs-as-substrate.md`.

## Open follow-ups

- 3D mesh sourcing pipeline.
- Rigging convention standardization.
- L-system grammar curation for plants.
- Behavior library mocap sourcing.

## Sources

- BodyParts3D (Database Center for Life Science, Japan).
- Visible Human Project (NLM, NIH).
- OpenAnatomy (Brigham Women's Hospital).
- Z-Anatomy.
- Allen Brain Atlas.
- Allen Cell Explorer.
- RCSB PDB.
- EM Data Bank.
- Mixamo rigging conventions.
- Smithsonian 3D digitization.
- MorphoBank, DigiMorph, FishBase.
- Encyclopedia of Life, Tree of Life Web Project.
- USDA PLANTS database.
- Kew Gardens.
- OpenSim biomechanics models.
- Gray's Anatomy (public domain).
- Internal: Briefs 073, 081, 083, 088.
