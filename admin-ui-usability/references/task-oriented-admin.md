# Task-Oriented Admin Patterns

## Forms and Structured Editors

- Replace foreign-key input with a searchable selector showing recognizable business identity.
- Replace stable codes and slugs with system generation or derivation plus uniqueness validation.
- Use date, time, range, enum, address, user, file, image, and monetary controls that match the business value.
- Display money in the operator's normal major unit while converting safely at the system boundary.
- Replace nested JSON with repeatable rows, structured sections, sortable items, condition builders, or a step editor.
- Put errors next to the responsible field and also provide a useful summary when the form is long.
- Keep system timestamps, internal IDs, version fields, and audit columns out of ordinary edit forms.

Complex editors need completeness checks before publication, server-side validation, and a way to locate the exact invalid section. A large text area with sample JSON is not a business editor.

## Tables, Filters, and Details

- Choose columns by decisions the operator makes, not by every available response field.
- Keep filters grouped, spaced, and responsive; preserve active filters and make clearing them obvious.
- Let the table own horizontal or bounded data scrolling without creating an extra whole-page horizontal scroll.
- Use recognizable customer labels and values. Hide or demote UUIDs, raw enums, redundant timestamps, and diagnostic metadata.
- An overview should summarize conclusion, progress, risk, next step, and pending work—not repeat all fields.
- Split long detail views by real tasks or information purposes. Do not merely distribute the same field dump across tabs.

## Permissions and Data Scope

- Group permissions by business page and show its view and action permissions together.
- Basic page loading must depend only on the page's declared base access; missing optional action permission should not break the whole page.
- Keep navigation visibility, button availability, API authorization, and server enforcement aligned to one permission source.
- Treat permission and data scope separately: permission answers which action is allowed; scope answers which records are accessible.
- Return and display only fields needed by this role and task. Frontend hiding is not sensitive-data protection.

## Uploads and Long-Running Work

- Explain accepted types, count, per-file size, and total size before selection.
- Validate obvious problems client-side and enforce limits server-side.
- For batches, show per-item progress and failure; do not roll back unrelated successful items unless the operation is truly atomic.
- Represent asynchronous work as queued, running, succeeded, or failed, with controlled retry and a stable operation identity.

## Audit and Change History

Summaries should answer “who did what, when, to which object, and with what result?” Use business field names. Put before/after values in a focused comparison view and mask sensitive fields by default. Do not expose internal action names, raw snapshots, or JSON as the primary customer-facing history.

## Review Scenarios

- Role can open the page with only its documented base permission.
- Missing optional permissions affect only the corresponding operations.
- Each state exposes only its legal primary and secondary actions.
- Destructive action communicates impact and creates an audit record.
- Searchable selectors handle large candidate sets and show recognizable labels.
- Empty, failed, partial, duplicate-submit, stale-update, and success flows remain understandable.
- Long tables, long labels, and narrow viewports preserve access to the main action.
