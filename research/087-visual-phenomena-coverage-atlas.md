# 087 — Visual phenomena coverage atlas

## Question
What is the **complete enumerated list** of visual phenomena GSPL must render correctly at v1, and how do we prove coverage so that no creator ever finds a "GSPL can't render this" gap?

## Why it matters
A library is only as strong as the gaps it doesn't have. Every other library brief in Round 4 ships *primitives*; this brief is the **coverage atlas** that proves the primitives compose into the full visual surface of reality. If a creator can ask for *any* visual and GSPL renders it grounded, the substrate has no escape hatches. If even one obvious phenomenon falls through ("we can't do caustics through wet glass at sunset"), the whole substrate's claim is undermined.

## What we know from the spec
- Briefs 081–086H: domain libraries.
- Brief 072: neural rendering.
- Brief 084: particles and fields.

## Findings — the visual phenomena atlas

The atlas enumerates phenomena across 12 categories. Each entry maps to (a) the substrate primitives that compose it and (b) the brief(s) that ship those primitives. This is the **substrate's coverage proof**.

### A. Light and lighting
1. Direct sunlight at all solar elevations (Brief 086 + 082)
2. Sky illumination including overcast, partly cloudy, twilight (Brief 086)
3. Moonlight at all phases (Brief 086A + 086)
4. Star illumination (Brief 086A)
5. Aurora (Brief 084 + 086)
6. Lightning illumination (Brief 084)
7. Fire / candle / hearth illumination (Brief 084 + 081)
8. Incandescent, fluorescent, LED, sodium, mercury vapor (Brief 082 + 086F)
9. Bioluminescence (Brief 081 + 085)
10. Volumetric light shafts / god rays (Brief 082 + 086)
11. Caustics through water and glass (Brief 082)
12. Dispersion / prism / rainbow (Brief 082 + 086)
13. Iridescence / thin-film / soap bubble / oil slick (Brief 082 + 083)
14. Halos, sundogs, glories, coronas (Brief 086)
15. Scattering through fog, haze, smoke, dust (Brief 084 + 086)

### B. Materials and surfaces
16. Metals (200+) at all roughness and oxidation states (Brief 083)
17. Glass and crystal at all clarity and color states (Brief 083)
18. Water (still, flowing, frozen, vapor) (Brief 084 + 081 + 086)
19. Skin across all Fitzpatrick types and ages (Brief 083 + 085)
20. Hair, fur, feathers, scales (Brief 085 + 084)
21. Fabric (1000+ types, dry/wet) (Brief 086G + 083)
22. Wood (50 species, fresh/aged/painted/wet) (Brief 083)
23. Stone (200 rocks, dry/wet/lichen-covered) (Brief 086)
24. Concrete, brick, plaster, stucco (Brief 083 + 086F)
25. Plastic, rubber, foam (Brief 083)
26. Leather (fresh, aged, oiled) (Brief 086G + 083)
27. Pottery, glazed ceramic, raw ceramic (Brief 083 + 086F)
28. Painted surfaces (matte, satin, gloss, automotive, weathered) (Brief 083)
29. Food surfaces (raw, cooked, plated) (Brief 086G)
30. Organic decay surfaces (Brief 081 + 085)

### C. Atmosphere and weather
31. Clear sky (full diurnal range) (Brief 086)
32. All 10 cloud genera + species + varieties (Brief 086 + 084)
33. Rain (drizzle → torrential, fresh / acid / monsoon) (Brief 084 + 086)
34. Snow (powder, packed, slush, blizzard) (Brief 084 + 086)
35. Hail, sleet, freezing rain (Brief 084)
36. Fog, mist, haze (Brief 084 + 086)
37. Tornado, hurricane, cyclone (Brief 086 + 084)
38. Sand and dust storms (Brief 084 + 086)
39. Volcanic ash plumes and fall (Brief 086 + 084)
40. Wildfire, smoke columns, ember storms (Brief 084 + 081)

### D. Water and fluids
41. Ocean waves (calm → storm) (Brief 086 + 084)
42. Rivers (straight, meandering, braided, rapids, waterfalls) (Brief 086)
43. Lakes, ponds, puddles (Brief 086)
44. Underwater (clear, turbid, deep) (Brief 086 + 082)
45. Wet surfaces and droplets (Brief 084 + 083)
46. Steam, vapor, breath in cold air (Brief 084 + 081)
47. Liquid pours, splashes, drips (Brief 084)
48. Foam, bubbles, suds (Brief 084 + 081)
49. Ice (clear, frosted, cracked, dirty) (Brief 086 + 083)
50. Mud, slurry, lava, lahars (Brief 084 + 086)

### E. Living things
51. Humans across all ages, genders, ethnicities (Brief 073 + 085)
52. 50 mammals at all ages and behaviors (Brief 085)
53. 20 bird species at all behaviors (Brief 085)
54. 15 reptiles, 20 fish, 20 insects (Brief 085)
55. Mythological creatures (composable rigs) (Brief 085 + 086E)
56. 50 tree species at all seasons and ages (Brief 085)
57. 100 flowering plants (Brief 085)
58. Grasses, mosses, ferns, mushrooms, seaweeds (Brief 085)
59. Microbes, cells, viruses (Brief 085 + 081)
60. Crowds of living things (Brief 085 + 088)

### F. Built world
61. Architecture from 40 traditions across periods (Brief 086F)
62. Interiors at every period and culture (Brief 086F + 086G)
63. Streets and urban patterns (Brief 086F)
64. Vehicles across all eras (Brief 086F)
65. Tools and weapons (Brief 086F)
66. Furniture and decor (Brief 086F + 086G)
67. Signage and typography in 100 languages (Brief 086D)
68. Markets, shops, stalls (Brief 086F + 086G)
69. Industrial sites, power, infrastructure (Brief 086F)
70. Sports venues and equipment (Brief 086F)

### G. Performance and human action
71. All 46 facial action units, all combinations (Brief 086H + 085)
72. Walk, run, jump, climb, swim, fly cycles (Brief 085)
73. Gestures and emblems across cultures (Brief 086H + 086E)
74. Combat (martial arts, sword, bow, gun in depiction-grade) (Brief 085 + 086F)
75. Dance across cultures (Brief 086H + 086C + 086E)
76. Working actions (cooking, building, farming, crafting) (Brief 086G + 086F)
77. Intimacy and care (with content rules per Brief 088) (Brief 086H)
78. Sleep, rest, illness, dying (Brief 086H + 085)
79. Crowds and group dynamics (Brief 086H + 088)
80. Vehicle operation and driving (Brief 086F + 086H)

### H. Color and stylization
81. Photoreal across all lighting conditions (Brief 072 + 082 + 083)
82. Cinematic looks (color grades, film emulations) (Brief 088)
83. 2D anime, manga, comic, graphic novel styles (Brief 088)
84. Watercolor, oil, gouache, ink wash painterly (Brief 088)
85. Pixel art at every common resolution (Brief 088)
86. 3D stylized (Pixar/Sony/Aardman family) (Brief 088)
87. Line art, woodcut, engraving, lithograph (Brief 088)
88. Photographic film stocks (Velvia, Portra, Tri-X, etc.) (Brief 088)
89. Historical art styles by movement (Brief 088 + 086E)
90. Children's book and editorial illustration (Brief 088)

### I. Time and motion
91. Slow motion at variable rates (Brief 071)
92. Time-lapse including growth, decay, weather (Brief 083 + 084 + 086)
93. Stop motion and frame-by-frame variants (Brief 088)
94. Motion blur (camera, subject) (Brief 082)
95. Camera shake, handheld, gimbal smoothing (Brief 088)
96. Long exposures (light trails, star trails, water silk) (Brief 086A + 084)
97. High-speed capture (bullet, droplet) (Brief 084)
98. Lens phenomena (DOF, bokeh, chromatic aberration, vignette, lens flare, dust on glass) (Brief 082 + 088)
99. Aspect ratios and aspect bars (Brief 088)
100. Time machine scrubs across history (Brief 071 + 086E)

### J. Sound coupled to visual
101. Material-acoustic-coherent reverb in any space (Brief 086C + 083)
102. Foley grounded in materials (Brief 086C + 083)
103. Voice with measured affect (Brief 086H + 086C)
104. Music in any tradition (Brief 086C + 086E)
105. Ambient soundscapes per environment (Brief 086C + 086)

### K. Special and rare
106. Black hole / accretion disk / lensing (Brief 086A + 082)
107. Microscopy (cell, virus, bacterium) (Brief 085 + 081)
108. Telescopy (planetary surface, deep sky) (Brief 086A)
109. X-ray, IR, UV, multispectral imagery (Brief 082 + 083)
110. Holograms, CRTs, screens-within-screens (Brief 086F + 088)
111. Glowing magic / fantasy effects (Brief 084)
112. Energy weapons / sci-fi VFX (Brief 084)
113. Portals, time vortices, space distortion (Brief 084 + 082)
114. Blueprints, schematics, technical drawings (Brief 088)
115. Charts, graphs, data visualizations (Brief 086B + 088)

### L. Cultural and ceremonial
116. Religious rituals across traditions (Brief 086E + 086F + 086G)
117. Festivals and celebrations (Brief 086E)
118. Funerary practices (Brief 086E + 086H)
119. Sport competitions (Brief 086F + 085)
120. Performance art and theatre (Brief 086H + 086C + 086F)

## Findings — coverage proof

Total enumerated phenomena: **120**. Each maps to a composition of substrate primitives drawn from one or more briefs. **Zero phenomena require artist invention from scratch.** Every gap closes by composing existing gseeds.

The atlas is published as a versioned substrate document at `inventory/visual-coverage-atlas.md` and updated whenever a new phenomenon is identified.

## Inventions

### INV-340: Living visual coverage atlas as substrate commitment
The atlas is a signed, versioned substrate document that enumerates every visual phenomenon GSPL guarantees coverage for, with explicit substrate-primitive composition for each. New gaps trigger new primitives via federation. Novel because no creative tool publishes a guaranteed-coverage atlas as a substrate-level commitment.

## Phase 1 deliverables

- **120-entry coverage atlas** signed at v1.
- **Composition recipe for every entry** documented at v1.
- **Gap intake protocol** for community-reported gaps at v1.

## Risks

- **Atlas creep without delivery.** Mitigation: gap intake requires composition proof before being marked covered.
- **Subjective quality threshold.** Mitigation: each entry ships with a reference render and quality acceptance criteria.

## Recommendation

1. **Publish the atlas as a versioned substrate document at v1.**
2. **Sign every entry** with composition recipe.
3. **Ship reference renders** for the top 30 entries at v1.
4. **Open a federated gap intake** for community reporting.

## Confidence
**4/5.** The atlas is the *spec* — execution is the rest of Round 4.

## Spec impact

- `inventory/visual-coverage-atlas.md` — new doc.
- New ADR: `adr/00NN-coverage-atlas-as-substrate-commitment.md`.

## Open follow-ups

- Reference render production for top 30.
- Gap intake UX design.
- Quality acceptance criteria definition.

## Sources

- Internal: All Round 4 briefs (078–086H), 071, 072, 073.
