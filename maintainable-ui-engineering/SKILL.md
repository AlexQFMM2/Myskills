---
name: maintainable-ui-engineering
description: Build or refactor web and app interfaces with consistent application themes, clear component ownership, scoped styles, and collision-resistant CSS variables. Use for substantial UI implementation, component extraction, design-system integration, or stylesheet architecture; do not trigger for copy-only edits or non-visual backend work.
---

# Maintainable UI Engineering

Produce UI code that remains understandable and safe to change as pages and features grow. Preserve the repository's framework, styling approach, design system, and established conventions unless the task explicitly changes them.

## Workflow

1. Inspect the relevant page, nearby components, shared UI package, global tokens, and styling configuration before proposing new structure.
2. Map ownership: the page owns page composition; a component owns its internal layout, states, and behavior; global styles own only true application-wide foundations.
3. Extract components at meaningful responsibility or reuse boundaries. Do not turn every wrapper or one-line fragment into a component.
4. Define the smallest stable styling interface a parent needs. Keep implementation details private to the component.
5. Implement responsive behavior and all applicable loading, empty, error, disabled, and overflow states.
6. Verify representative viewports and check that changing one component or page does not leak into unrelated UI.

## Invariants

- Do not grow a monolithic page or stylesheet when sections have independent responsibilities, state, or reuse value.
- Do not create wrapper-component or abstraction layers without a concrete responsibility.
- Page styles may place and size components but must not reach into a child's private DOM or class names to repair its internals.
- A reusable component owns its internal layout, proportions, variants, state styles, and scrolling behavior.
- Prefer the project's existing primitives and shared components; do not duplicate a near-equivalent component merely to avoid understanding it.
- Keep reset, font registration, root layout, and shared semantic tokens global. Keep feature and component styling locally owned.
- Treat responsiveness as component behavior, not as a late collection of page-specific overrides.
- A visual fallback must not hide broken data, resource resolution, or layout logic.

## Global Theme Contract

- For CSS-based applications, the authoritative global theme file is fixed at `src/styles/theme.css`, relative to each application's root (the UI package root in a monorepo), and loaded through its application entry point. Shared token definitions belong in this file; do not substitute `global.css`, `variables.css`, or another theme filename.
- Reserve the exact `--app-theme-*` prefix for global theme variables. Follow `--app-theme-<category>-<purpose-or-level>` and the category prefixes in [references/component-and-style-boundaries.md](references/component-and-style-boundaries.md#fixed-theme-file-and-variable-naming). Add variables and typography levels as the product needs; the naming structure is fixed, not the token inventory. Reuse an existing token for the same purpose. Page and component variables retain their owner prefixes and must not use the reserved theme prefix.
- Define the shared visual language there: primary/brand color, active/selected interaction colors, surface/text/border and status colors, font families, typography roles (size, weight, line height), and shared spacing, radius, shadow, and motion scales as needed by the product. Keep distinct semantic roles separate even when their current values match.
- Pages and components must consume these tokens through variables, theme APIs, or theme-backed utilities. Do not independently hard-code or redefine shared colors, typography, or other established theme decisions. Component state styles select the appropriate global semantic token; they do not invent a separate palette.
- Keep internal layout, component-specific dimensions, and exceptional decorative details local, with owner-prefixed variables where useful. Use global tokens directly unless a local alias establishes an intentional styling contract or a meaningful derived value. Do not promote every component detail into the global theme.
- Keep supported theme variants in `src/styles/theme.css`, overriding the same token names in theme selectors. Configure framework utilities and third-party UI themes from these tokens through supported APIs; their configuration must not become a second source of shared values.
- For existing projects, preserve approved visual values while consolidating the shared definitions needed by the task into the fixed file and naming convention. Legacy names may temporarily alias the canonical tokens for untouched consumers. Do not turn a local UI task into an unsolicited project-wide visual migration.
- For genuinely non-CSS native UI, use the platform's theme facility and preserve the same semantic roles; report its actual location instead of creating an unused CSS file. CSS-capable frameworks follow the fixed CSS contract above.

## CSS Variables and Tokens

Read [references/component-and-style-boundaries.md](references/component-and-style-boundaries.md) when creating or changing component APIs, CSS variables, design tokens, or stylesheet organization.

At minimum:

- Follow the Global Theme Contract for shared visual decisions; keep page and component implementation variables local.
- Prefix page-local and component-local variables with their owner: `--<owner>-<property>` or `--<owner>-<part>-<property>`.
- Expose only variables a parent is intentionally allowed to override.
- Derive internal dimensions from owned variables instead of scattering duplicate magic numbers.
- Do not use broad selectors or generic variable names that can silently affect unrelated UI.

## Delivery Check

Report the authoritative theme source and the component boundaries or public styling contracts that materially changed. Verify the fixed file path and `--app-theme-*` naming convention, that the theme is loaded, and that representative affected pages and controls consume the same semantic tokens (including interaction states). Check that styles are locally owned and no parent depends on a child's private markup. When shared theme values change, verify representative consumers across pages for consistency and regressions.
