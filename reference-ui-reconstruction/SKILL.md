---
name: reference-ui-reconstruction
description: Analyze screenshots, mockups, design files, or existing pages as visual evidence and reconstruct their structure and appearance faithfully. Use when implementing or auditing a UI against a visual reference; do not trigger for open-ended design without a reference or for purely functional changes.
---

# Reference UI Reconstruction

Translate visual evidence into an executable layout model before coding, then validate the result against the same evidence. Fidelity is the first objective unless the user explicitly authorizes a redesign.

## Evidence Rules

Classify every material conclusion as one of:

- **Observed:** directly visible or measurable in the supplied reference.
- **Inferred:** a likely responsive, structural, or interaction rule supported by visible evidence.
- **Unknown:** cannot be established from the available state or viewport.

Do not present inferred pixels, behavior, hidden states, animation, or responsive rules as observed facts. Ask for more evidence when an unknown would materially change the architecture; otherwise preserve it as an explicit assumption and continue with the stable skeleton.

## Required Analysis

Before implementation, produce:

1. A concise theme and style definition covering purpose, audience, content priority, visual language, color roles, typography hierarchy, density, spacing, radius, borders, shadows, imagery, and icon treatment.
2. A component layout tree from the page root through every visually or interactively meaningful region.
3. A list of distinctive details that must not be simplified, including overlays, badges, unusual composition, grouped controls, textures, asymmetric whitespace, and content density.
4. A list of unknowns and permitted assumptions.

For the exact analysis fields and validation matrix, read [references/analysis-and-validation.md](references/analysis-and-validation.md).

## Implementation Order

1. Preserve the reference route, viewport, state, and content density as the comparison baseline.
2. Build the page skeleton, region order, shared edges, proportions, and overflow ownership.
3. Place real or appropriately sourced assets with the observed aspect ratios and cropping behavior.
4. Match typography, color, border, radius, shadow, spacing, and alignment.
5. Implement supported responsive changes and interaction states without inventing unseen product behavior.
6. Extract shared structure only after the visual baseline works; revalidate after extraction.
7. Optimize or redesign only after fidelity is established and the requested differences are explicit.

Do not use KISS, component reuse, or personal aesthetic preference as a reason to remove visible content or distinctive detail. Those principles reduce accidental engineering complexity; they do not override the user's visual requirements.

## Validation

Compare reference and implementation at the same viewport, zoom, route, content, and state. Use side-by-side screenshots and, when useful, an overlay or difference image. Fix in this order:

1. Missing regions, incorrect hierarchy, content density, and assets.
2. Container geometry, grid/flex behavior, alignment, and proportions.
3. Typography and spacing rhythm.
4. Color, border, shadow, radius, and decorative details.
5. Responsive and interactive states.

A rendered page, passing build, correct route, or rough stylistic similarity is not evidence of visual fidelity. Report remaining differences honestly.
