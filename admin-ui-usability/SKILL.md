---
name: admin-ui-usability
description: Design, implement, or review admin panels and operational back offices for task clarity, safe state transitions, business-friendly data entry, permissions, feedback, and auditability. Use for administrator, staff, moderation, review, configuration, and operations interfaces; do not trigger for public marketing pages.
---

# Admin UI Usability

Design an operational workspace around the target user's job, not around database columns or API shapes. A successful admin page makes the current situation, next action, result, and responsibility clear without developer explanation.

## Start From the Task

Identify:

- Target role and the job they came to complete.
- Current state, business conclusion, risk, and next responsible role.
- The one primary action available in each state.
- Required evidence, permissions, validation, confirmation, and audit trail.
- What belongs on the first screen versus details, history, or advanced settings.

If this task model is unclear, do not compensate by placing every field and endpoint action on one page.

## Page Hierarchy

- Lead with page purpose, current state, business conclusion, next step, and one primary action.
- Demote low-frequency actions; move raw source material, full history, diagnostics, and secondary configuration into clearly named detail areas.
- Use customer or operator language. Do not expose internal action names, schema terminology, stack traces, or transport errors.
- Keep one main vertical scroll owner. Bound independent scrolling for a large table, report, or code/data viewer rather than nesting uncontrolled same-direction scrolling.
- Use drawers and dialogs for focused tasks. Move long-running or multi-stage editing to a dedicated page or workspace.

## Actions and State

- Derive available actions from an explicit state machine. Show only legal actions for the current state, and validate the transition again on the server.
- Emphasize one primary action per state. Explain why unavailable actions are hidden or disabled when that information helps the operator.
- State copy should explain both the present condition and what happens next, including the next responsible role in cross-role workflows.
- Destructive or high-impact actions require clear confirmation, affected scope, and a reason when the business process needs one.
- Prevent duplicate submission and stale concurrent updates. Preserve actor, time, target, outcome, and necessary reason for auditable operations.

## Business-Friendly Input

Read [references/task-oriented-admin.md](references/task-oriented-admin.md) when building forms, tables, filters, upload flows, permissions, logs, or complex configuration editors.

Never make ordinary operators type or edit:

- Foreign keys, UUIDs, resource keys, permission keys, idempotency keys, stable codes, or internal enum values.
- JSON, YAML, SQL, regular expressions, request bodies, templates, or database-shaped objects.
- Raw numeric ordering values, storage paths, or minor currency units.

Generate these values, derive them from business input, or provide a constrained selector/editor. Advanced technical controls, when genuinely required, belong in a separately permissioned expert area with validation and risk explanation.

## Feedback and Recovery

Cover loading, empty, partial, error, retry, disabled, submitting, queued, processing, success, and failure states as applicable. Put validation near the field or action. Translate failures into a business-readable cause and next step. After success, refresh the relevant truth and make the resulting state visible.

## Acceptance

Test with the actual target role and permissions. The user must be able to find the entry, understand the state, complete the main task, confirm the result, and know the next responsible party without developer guidance. Also inspect density, scroll ownership, empty/error states, destructive flows, long content, and narrow-screen reachability.
