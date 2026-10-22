# Findings and Review Output

Use the user's language and any required output schema. The shape below is a default, not a reason to override a host's structured review format. Omit empty sections and keep detail proportional to the change.

## Priority Is Impact, Not Confidence

| Priority | Meaning | Evidence needed for that priority |
| --- | --- | --- |
| P0 — critical | An immediate release/operation blocker, such as unavoidable catastrophic data loss or broad compromise in normal supported operation. | Established broad impact; do not use for a worst-case scenario with unproven assumptions. |
| P1 — high | A serious reachable security, integrity, availability, or core-workflow failure that should be fixed before the affected change ships. | Name the affected users, conditions, and consequence. |
| P2 — normal | A concrete correctness or contract defect under supported conditions with more limited impact or a practical workaround. | Explain the trigger and observable wrong result. |
| P3 — low | A confirmed low-impact defect worth fixing. | Still needs a real consequence; not a bucket for taste or uncertainty. |

Repository-specific severity definitions take precedence when provided; map the evidence to those definitions and explain material differences. Whether a defect blocks a merge also depends on the agreed release criteria. An optional naming/refactoring preference is not automatically P3, and an unverified security suspicion is not automatically P1.

## Finding Content

Keep one root cause per finding. Include:

- A short priority-tagged title that identifies the failure or required correction.
- A precise file and line location in the reviewed state. For a diff review, anchor to the changed lines responsible for the regression where possible; cite unchanged supporting code as context. Do not invent line numbers for unavailable source.
- The reachable trigger, violated expectation, and concrete impact in direct prose.
- The evidence: relevant control/data flow or a reproduction with its actual result. Distinguish observed results from reasoned consequences.
- A proportionate repair direction. Do not require a broad refactor when a local fix preserves the contract, or prescribe a library/pattern merely by preference.

Example of a confirmed finding with static evidence:

> **[P1] Check document ownership before deletion — `api/documents.py:84`**
>
> An authenticated user who supplies another user's document ID reaches the new delete route. Its dependency establishes login only, and the service loads by document ID without an owner or tenant condition. Deletion therefore violates the documented owner-only contract. Scope the lookup or enforce ownership before mutation. This conclusion follows the route → authentication dependency → delete service path; no endpoint test was run.

This example assumes all named guards and service behavior have actually been inspected. If the dependency or policy implementation is unavailable, report that missing evidence instead of copying the conclusion.

Example of a material unresolved question:

> The retry path sends the payment request again, but the provider's idempotency contract is unavailable. Confirm whether this key is honored before deciding whether duplicate charging is possible. No duplicate-charge defect is established by the available code alone.

Example of an optional suggestion:

> Two formatters implement the same display rule. Sharing the existing formatter could reduce future drift; current outputs agree, so this is an optional maintenance improvement.

## Default Report Shape

1. **Confirmed findings**, ordered by impact, with evidence and repair direction.
2. **Material open questions**, only when an unresolved fact changes the review decision; identify what would settle it.
3. **Optional suggestions**, only when useful to the requested scope and clearly separated from defects.
4. **Coverage and verification:** reviewed comparison/module, checks actually run, relevant outcomes, and material gaps or skipped areas. Use the evidence-backed Checked / Not applicable / Unverified states in [coverage-checklist.md](coverage-checklist.md); a broad review can include its compact table, while a small review can summarize the same information in prose.
5. **Recommendation:** address the established defects, resolve a named blocker, or proceed within the reviewed scope. Do not present a local recommendation as a submitted PR approval or completed acceptance gate.

For a short review, combine these into a few paragraphs. A full template is unnecessary when there is one finding or none. Do not report a numeric quality score or fabricate review time.

If no defect is established, use a bounded statement such as:

> No confirmed defects were found in the reviewed changes. Reviewed the handler and affected callers; the focused unit checks passed. Database integration was not exercised, so migration behavior remains unverified.

Use only the checks and gaps that actually apply. If major areas remain unreviewed, label the result partial instead of implying a complete review. Missing verification is not automatically a code defect, but it can prevent a confident recommendation when an important risk remains unsettled.
