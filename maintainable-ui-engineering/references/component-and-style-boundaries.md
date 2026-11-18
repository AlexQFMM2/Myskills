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
| Global | reset, font registration, root defaults, authoritative theme tokens and variants | feature layout or component internals |
| Page | page grid, section order, placement, page-level responsive composition | selectors coupled to child internals |
| Component | internal layout, variants, states, overflow, local responsiveness | unrelated page positioning |
| Utility | one documented, predictable concern | hidden component-specific exceptions |

Follow the repository's established mechanism—CSS Modules, scoped styles, CSS-in-JS, utility classes, native styles, or another system—while preserving these ownership boundaries.

## Fixed Theme File and Variable Naming

For CSS-based UI, use `<application-root>/src/styles/theme.css` as the single definition source. Declare defaults in `:root` and supported theme overrides in that same file. Import it from the application entry point; feature and component stylesheets consume it without redefining `--app-theme-*` variables.

Use `--app-theme-<category>-<purpose-or-level>` with lowercase, hyphen-separated names. The file path, reserved prefix, and category prefixes below are fixed; suffixes and the number of variables follow the product's needs. The examples are not an exhaustive or mandatory token list. Values follow the project's approved design.

| Category | Required prefix | Example suffixes, freely extensible |
| --- | --- | --- |
| Colors | `--app-theme-color-` | `primary`, `primary-hover`, `primary-active`, `on-primary`, `selected`, `focus-ring`, `background`, `surface`, `text`, `text-muted`, `border`, `success`, `error` |
| Font families | `--app-theme-font-family-` | `body`, `heading`, `mono` |
| Font sizes | `--app-theme-font-size-` | `xs`, `sm`, `md`, `lg`, `xl`, `2xl`, or semantic roles such as `body`, `heading`, `caption` |
| Font weights | `--app-theme-font-weight-` | `regular`, `medium`, `bold`, or semantic roles such as `body`, `heading` |
| Line heights | `--app-theme-line-height-` | `tight`, `normal`, `relaxed`, or semantic roles such as `body`, `heading` |
| Spacing | `--app-theme-space-` | `1`, `2`, `3`, or semantic roles such as `section` |
| Corner radii | `--app-theme-radius-` | `sm`, `md`, `lg`, or semantic roles such as `control`, `card` |
| Shadows | `--app-theme-shadow-` | `card`, `popover`, `dialog` |
| Motion duration | `--app-theme-duration-` | `fast`, `normal`, `slow` |
| Motion easing | `--app-theme-easing-` | `standard`, `enter`, `exit` |

For example, a project may start with `--app-theme-font-size-sm`, `--app-theme-font-size-md`, and `--app-theme-font-size-lg`, then add `--app-theme-font-size-xl` or a named display size when needed. Do not cap the number of sizes or require every size to have separate weight and line-height variables. Keep the chosen scale coherent; semantic typography aliases are useful when they establish a shared role.

Reuse an existing variable for the same purpose instead of adding synonymous names. Distinguish different meanings: for example, `primary-active` describes a pressed action, while `selected` describes a persistent selection. Document non-obvious additions in the theme file. A genuinely new shared category may extend the same structure; component-specific values remain owner-prefixed local variables. Temporary legacy aliases must point to canonical tokens, not the reverse, and new code must use the canonical names.

## Variable Taxonomy

The following excerpt illustrates the fixed naming contract and ownership boundaries. Its values are examples, not a prescribed palette or type scale.

```css
/* src/styles/theme.css — loaded from the application entry point */
:root {
  --app-theme-color-primary: #3155c6;
  --app-theme-color-primary-active: #24429f;
  --app-theme-color-on-primary: #fff;
  --app-theme-color-background: #f5f6fa;
  --app-theme-color-surface: #fff;
  --app-theme-color-text: #16181d;
  --app-theme-color-text-muted: #596170;
  --app-theme-color-border: #d8dce5;
  --app-theme-font-family-body: system-ui, sans-serif;
  --app-theme-font-family-heading: var(--app-theme-font-family-body);
  --app-theme-font-size-body: 1rem;
  --app-theme-font-size-heading: 1.5rem;
  --app-theme-font-size-caption: 0.875rem;
  --app-theme-font-weight-body: 400;
  --app-theme-font-weight-heading: 600;
  --app-theme-font-weight-caption: 400;
  --app-theme-line-height-body: 1.5;
  --app-theme-line-height-heading: 1.25;
  --app-theme-line-height-caption: 1.4;
  --app-theme-space-3: 0.75rem;
  --app-theme-radius-control: 0.5rem;
}

body {
  color: var(--app-theme-color-text);
  background: var(--app-theme-color-background);
  font-family: var(--app-theme-font-family-body);
  font-size: var(--app-theme-font-size-body);
  font-weight: var(--app-theme-font-weight-body);
  line-height: var(--app-theme-line-height-body);
}

/* ProfileCard's locally scoped stylesheet */
.profile-card {
  --profile-card-avatar-size: 3rem;
  gap: var(--app-theme-space-3);
  color: var(--app-theme-color-text);
  background: var(--app-theme-color-surface);
}

.profile-card__title {
  font-family: var(--app-theme-font-family-heading);
  font-size: var(--app-theme-font-size-heading);
  font-weight: var(--app-theme-font-weight-heading);
  line-height: var(--app-theme-line-height-heading);
}

/* ActionButton owns its state selectors; the theme owns their colors. */
.action-button {
  color: var(--app-theme-color-on-primary);
  background: var(--app-theme-color-primary);
  border-radius: var(--app-theme-radius-control);
}

.action-button:active {
  background: var(--app-theme-color-primary-active);
}

/* AccountPage's locally scoped stylesheet */
.account-page {
  --account-page-sidebar-width: 18rem;
}
```

- Global tokens use the reserved `--app-theme-*` namespace and the category naming convention above.
- Component variables start with the component name.
- Page variables start with the page or feature name.
- Add a part segment only when it disambiguates meaning: `--data-table-header-height`.
- Prefer semantic purpose over incidental implementation: `--dialog-max-width`, not `--big-width`.
- Do not create aliases that merely rename another token without establishing a real boundary.

For utility-first styling or CSS-in-JS on the web, map shared utilities and theme properties to `var(--app-theme-...)` from `src/styles/theme.css`. When a UI library needs separate token names, map them through its supported configuration instead of copying literal values. Genuinely non-CSS native UI uses its platform theme facility with the same semantic roles, without an unused CSS file. These integrations must not create additional independent palettes or typography scales.

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
- Is `src/styles/theme.css` loaded at the application root, with the required `--app-theme-*` naming structure and no component-local definitions in that namespace?
- Do affected pages and controls use these tokens for shared colors and typography, including active/selected states?
- If shared tokens changed, do representative consumers across pages and supported themes remain consistent without local overrides masking the change?
- Can variable names coexist across many pages without collision?
- Does changing a component default avoid page-specific regressions?
- Are responsive, overflow, long-text, empty, loading, error, and disabled states handled where they are owned?
