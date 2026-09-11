# Analysis and Validation Contract

## Theme and Style Definition

Record only decisions that affect implementation:

- Page purpose, target user, primary task, and content priority.
- Dominant visual language and any region-specific exceptions.
- Background, surface, text, accent, and status color roles.
- Typeface category, size/weight hierarchy, and line-height character.
- Spacing rhythm, information density, separators, radius, shadow, gradient, and transparency.
- Image, illustration, icon, texture, logo, and video-cover style; aspect ratio; crop mode; likely source strategy.
- Visual rhythm and module boundaries.
- Unobservable interaction, animation, sticky behavior, loading, error, empty, and modal states.

## Component Layout Tree

For each meaningful node, capture:

```text
Region name
- Evidence: observed / inferred / unknown
- Layout: row flex / column flex / grid / normal flow / overlay
- Relationship: parent, siblings, order, grouping
- Alignment: start / end / center / baseline / space distribution
- Positioning: normal, sticky, fixed, or anchored overlay; name the containing block
- Sizing: fixed, intrinsic, flexible, min/max, aspect ratio
- Spacing and boundaries: margin, gap, padding, clipping, wrapping, truncation, scroll owner
- Responsive behavior: preserve, wrap, reflow, resize, change columns, or scroll
└─ Child regions
```

Prefer normal flow, flex, and grid for primary structure. Use absolute positioning only when the evidence shows an overlay or anchored decoration, and identify its containing block and stacking relationship.

When exact dimensions cannot be measured reliably, specify proportions and relationships rather than invented pixel precision.

## Evidence Capture

When an existing product can be inspected, collect the smallest evidence set that covers the requested scope:

- Route and state inventory, including protected and modal states when relevant.
- Desktop and mobile references using recorded viewport sizes.
- DOM or accessibility structure when available.
- Successful network assets and fonts rather than broken or guessed substitutes.
- Representative content volume, long labels, and data density.
- Separate user-requested additions from reference-derived behavior.

Never persist credentials in screenshots, plans, logs, or fixtures.

## Fidelity Matrix

For each route or state, record:

| Area | Reference evidence | Implementation | Status | Remaining difference |
| --- | --- | --- | --- | --- |
| Skeleton | regions and order | observed result | match/partial/missing | concrete delta |
| Geometry | width, height, proportion | observed result | match/partial/missing | concrete delta |
| Assets | source, crop, ratio | observed result | match/partial/missing | concrete delta |
| Density | fields, cards, rows, labels | observed result | match/partial/missing | concrete delta |
| Styling | type, color, space, effects | observed result | match/partial/missing | concrete delta |
| States | responsive and interaction | observed result | match/partial/unknown | concrete delta |

Use “unknown” when the reference lacks evidence. Do not silently label a guessed state as matched.

## Acceptance

- Compare all in-scope representative routes, not only the landing page.
- Cover the supplied desktop/mobile sizes and material states.
- Verify long content, overflow, fixed elements, and scroll ownership.
- Distinguish faithful reconstruction, authorized change, unresolved difference, and missing source evidence.
- Require visual inspection in addition to build, type, route, and functional checks.
