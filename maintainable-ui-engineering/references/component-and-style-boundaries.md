# Component and Style Boundaries

Read this reference when a task changes UI structure, styling ownership, reusable components, or CSS custom properties.

## Choose Component Boundaries

Extract a component when at least one of these is true:

- It represents an independently understandable product or visual concept.
- It owns meaningful state, interaction, accessibility behavior, or asynchronous feedback.
- It repeats or is expected to repeat with the same contract.
- It is complex enough to review and test independently.
- Its internal layout should be protected from page-level changes.

Keep markup local when extraction would only create a pass-through wrapper, obscure the reading order, or introduce configuration larger than the duplicated markup.

Use composition for structural variation. Use variants for a small, explicit set of supported appearances. Avoid a universal component with many boolean switches and unrelated modes.

## Styling Ownership

| Layer | Owns | Must not own |
| --- | --- | --- |
| Global | reset, fonts, root defaults, semantic token scales | feature layout or component internals |
| Page | page grid, section order, placement, page-level responsive composition | selectors coupled to child internals |
| Component | internal layout, variants, states, overflow, local responsiveness | unrelated page positioning |
| Utility | one documented, predictable concern | hidden component-specific exceptions |

Follow the repository's established mechanism—CSS Modules, scoped styles, CSS-in-JS, utility classes, native styles, or another system—while preserving these ownership boundaries.

## Variable Taxonomy

Use names that reveal scope and purpose:

```css
:root {
  --color-surface: #fff;
  --color-text: #16181d;
  --space-3: 0.75rem;
  --radius-control: 0.5rem;
}

.profile-card {
  --profile-card-avatar-size: 3rem;
  --profile-card-gap: var(--space-3);
}

.account-page {
  --account-page-sidebar-width: 18rem;
}
```

- Global tokens use a controlled semantic namespace and one definition source.
- Component variables start with the component name.
- Page variables start with the page or feature name.
- Add a part segment only when it disambiguates meaning: `--data-table-header-height`.
- Prefer semantic purpose over incidental implementation: `--dialog-max-width`, not `--big-width`.
- Do not create aliases that merely rename another token without establishing a real boundary.

## Public Styling Contract

A component's public variables are an API. Keep the set small, document non-obvious units or constraints, provide safe defaults, and avoid exposing values whose independent modification would break the component.

The parent may override an exposed variable:

```css
.dashboard-page .summary-card {
  --summary-card-media-size: 4rem;
}
```

The parent must not target private descendants:

```css
/* Avoid: coupled to private markup. */
.dashboard-page .summary-card .summary-card__media img { width: 4rem; }
```

When several descendants depend on one dimension, calculate them from the component-owned variable. Do not repeat the same literal across selectors.

## Review Checklist

- Can a reader identify who owns each layout decision?
- Are shared components reused through their documented contract?
- Do global styles contain only global concerns?
- Can variable names coexist across many pages without collision?
- Does changing a component default avoid page-specific regressions?
- Are responsive, overflow, long-text, empty, loading, error, and disabled states handled where they are owned?
