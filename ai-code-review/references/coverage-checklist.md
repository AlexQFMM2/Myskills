# Review Coverage

Use this checklist to avoid missing entire risk categories within the requested review scope. Screen for applicability first; read specialist details only for relevant paths. A documentation-only change does not require a new security audit or runtime test suite.

## Coverage States

| State | Meaning | Record |
| --- | --- | --- |
| Checked | The relevant path has been inspected to the stated depth, and material candidates are resolved or identified separately. It may contain confirmed defects. | Source path/contract, static trace or actual check result, plus finding/open-question references when applicable. |
| Not applicable | The requested change or module does not exercise this category. | A short reason tied to the scope; absence of a filename keyword is not sufficient. |
| Unverified | The category applies, but necessary code, contract, environment, or verification is missing. This includes partially checked areas. | What is known, the missing evidence, its effect on the decision, and the next check that would settle it. |

Static inspection can support Checked when it establishes the relevant behavior. Running a test is not required to fill every row, and passing tests do not automatically mark unrelated rows Checked. Track evidence per affected path when one category spans multiple independent operations; do not hide an unverified operation behind another operation's passing result.

## Applicability and Evidence

| Category | When to inspect | Evidence to seek / edge cases |
| --- | --- | --- |
| Requirement and end-to-end behavior | A behavior, contract, state transition, or business action changes. | Accepted requirement → entry point → validation → side effects → result. Include forbidden transitions, missing resources, repeated operations, and partial failures. |
| Input, output, and arithmetic | Parsers, schemas, serialization, money/quantity, dates, IDs, or collection logic changes. | Empty/missing/null versus zero/false, boundaries, overflow/precision, timezone/DST assumptions, ordering/pagination, and old payloads. Use actual supported inputs. |
| Identity and authorization | Requests, tenant/resource queries, roles, sessions/tokens, or privileged operations change. | Which actor can reach which resource; caller/middleware/service/database guards; anonymous, own-resource, other-resource, and tenant-boundary paths as applicable. |
| Untrusted data and disclosure | SQL, markup, commands, files, URLs, uploads, logs, errors, or response models handle external data. | Source → transformations → sink; output context, effective permissions, exposed fields, path/redirect handling, secrets and dependency changes. |
| Persistence and compatibility | Schema, migrations, API/event formats, configuration, or shared dependencies change. | Old data, defaults, rollback constraints, producer/consumer versions, deployment order, required indexes/constraints, and all affected callers. |
| Concurrency and idempotency | Read-modify-write, callbacks, jobs, retries, cancellation, shared state, or concurrent UI requests exist. | Feasible interleavings; real transaction/lock/constraint boundaries; duplicate delivery, stale responses, retry after partial success, and cancellation while work is in progress. |
| Errors, lifetime, and recovery | External calls, resource acquisition, background work, or cleanup changes. | Errors propagate to the right owner; cleanup runs on exceptional paths; no swallowed cancellation, abandoned tasks, lost results, or irrecoverable partial state. |
| Performance and bounds | Data volume, query loops, rendering, caching, allocation, or concurrency changes. | Supported workload and limits, query/operation counts, cache isolation/invalidation, memory lifetime, and measured or reasoned consequential cost. |
| Architecture and maintainability | Responsibilities, dependencies, reusable operations, state ownership, or abstraction boundaries change. | Concrete coupling or duplicated-invariant problems, broken contracts, or maintenance consequences. Preserve intentional conventions; personal preference is an optional suggestion. |
| UI and interaction | Screens, navigation, forms, optimistic updates, or async UI state changes. | Target role can complete the task; loading/empty/error/disabled/retry states; stale data and duplicate submission; keyboard/accessibility and responsive/visual evidence where relevant. |
| Tests, build, and CI | A behavioral change needs validation, or test/build/dependency configuration changes. | Relevant assertions and failure paths, test isolation, genuine mock boundaries, exact reviewed revision, required check outcomes, and test gaps that affect confidence. |
| Documentation and operational handoff | Public contracts, defaults, setup, migration, or operator actions change. | Documented commands and examples match actual behavior; breaking changes and recovery instructions are consistent with the change. Mere missing prose is not automatically a defect. |

For concrete patterns and code examples, select the matching guides from [risk-patterns.md](risk-patterns.md). There is no obligation to read every guide or enumerate every example for each row.

## CI and Test Evidence

- When relevant CI results are available, inspect their revision, jobs, configuration, and failure reasons. Distinguish head checks from merge-result checks when that difference matters.
- A skipped, cancelled, pending, or unavailable job is not a pass. A failure is not automatically caused by the change; inspect whether it is a code failure, pre-existing failure, or environment/setup failure.
- Local test results apply to the source and dependency state actually executed. Do not use working-tree results as proof for a different staged snapshot or remote commit.
- Review what assertions prove. A test that only checks that a mocked method was called may miss authorization, persisted side effects, or serialization failures. Conversely, a focused unit test is sufficient for a unit-level claim; do not require endpoint tests for every helper.
- Where a risk needs reproduction, select a decisive case: unauthorized actor, boundary value, duplicate delivery, controlled interleaving, or failing dependency. Do not add permanent tests or change production behavior during review-only work.
- Treat required acceptance checks as pending until they pass or an authorized exception is recorded. Do not rerun all checks solely to fill this table; reuse evidence while its prerequisites remain valid.

## Compact Review Record

For broad reviews, use a table shaped like this, containing only actual observations:

| Area / affected path | Status | Evidence and outcome | Remaining gap |
| --- | --- | --- | --- |
| Document deletion / authorization | Checked | Route → auth dependency → service inspected; owner predicate absent; finding F1. | Endpoint execution unavailable; finding established by static trace. |
| Document deletion / concurrent requests | Unverified | Deletion transaction inspected. | External event deduplication contract unavailable; effect of duplicate delivery unresolved. |
| Browser rendering | Not applicable | Change affects only the server-side deletion path and preserves its response contract. | None. |

The example demonstrates status semantics, not assumed facts. Use finding identifiers only if the report needs them. Keep the record in the current review or existing workflow artifact; do not create an additional ledger for every review. A small review can express the same facts in a few sentences.

Before concluding, check that each applicable category has evidence or an explicit gap. Coverage is not a numeric quality score, and a checked category is not a guarantee that every possible defect has been found.
