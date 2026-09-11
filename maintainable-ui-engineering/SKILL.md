---
name: maintainable-ui-engineering
description: Build or refactor web and app interfaces with clear component ownership, scoped styles, stable design tokens, and collision-resistant CSS variables. Use for substantial UI implementation, component extraction, design-system integration, or stylesheet architecture; do not trigger for copy-only edits or non-visual backend work.
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

## CSS Variables and Tokens

Read [references/component-and-style-boundaries.md](references/component-and-style-boundaries.md) when creating or changing component APIs, CSS variables, design tokens, or stylesheet organization.

At minimum:

- Use global tokens only for genuinely shared semantic decisions such as surface, text, spacing, radius, and motion scales.
- Prefix page-local and component-local variables with their owner: `--<owner>-<property>` or `--<owner>-<part>-<property>`.
- Expose only variables a parent is intentionally allowed to override.
- Derive internal dimensions from owned variables instead of scattering duplicate magic numbers.
- Do not use broad selectors or generic variable names that can silently affect unrelated UI.

## Delivery Check

Report the component boundaries and public styling contracts that materially changed. Verify that styles are locally owned, shared tokens have one source of truth, and no parent depends on a child's private markup.
