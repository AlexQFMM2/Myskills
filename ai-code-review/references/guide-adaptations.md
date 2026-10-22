# Applying the Imported Guides

Read this once before using the imported reference library. The library supplies detailed hypotheses and examples; [SKILL.md](../SKILL.md), [scope and evidence](scope-and-evidence.md), and [reporting](reporting.md) define the review process and decision rules.

## Source and Maintenance

All 35 Markdown files from the upstream `reference/` tree are included under `upstream/`: 24 language/framework guides and 11 cross-cutting/process guides. The exact repository, pinned revision, source and packaged file hashes are recorded in [manifest.json](upstream/manifest.json). The upstream [MIT license](upstream/LICENSE) is preserved.

Each guide contains a local rules notice followed by the original upstream text unchanged. This makes source updates and local interpretation distinguishable. The full catalog is in [risk-patterns.md](risk-patterns.md). Files are available locally; a review does not need network access just to load a guide.

The snapshot is reference coverage, not certification of every example. Verify consequential API, runtime, security, and version claims against the project and authoritative documentation as needed. Statements such as "current stable" describe the upstream snapshot, not necessarily the reviewed environment.

When updating, compare against a deliberate new revision, inspect changed guidance and licensing, and update the manifest hashes and routing together. Do not refresh from a moving branch automatically or copy the upstream entrypoint over our review rules.

## Rules That Override Guide Heuristics

- A red flag, unchecked checklist item, `Bad` example, or upstream severity label proposes a candidate for investigation. It is not an established defect. Apply the local evidence gate and impact-based priorities.
- Line counts, numbers of methods, parameter counts, test-line ratios, absent interfaces, an `any`, an `unwrap`, a missing type annotation, or use of an older valid API do not independently justify a blocking finding. Enforce explicit project contracts where they exist, and explain the actual consequence.
- SOLID, layered architecture, framework idioms, and reuse advice inform design judgment. Do not require a new layer, interface, dependency, or refactor unless the reviewed requirement or concrete risk warrants it. Existing UI and KISS criteria remain relevant within their own scopes.
- Patterns must match the actual language/framework/compiler version, configuration, and supported deployment environment. Select Java 8 versus modern Java, legacy versus current framework behavior, and sync versus async execution deliberately.
- Performance recommendations need workload, bounds, operation counts, or measurements. Missing caching, memoization, batching, async syntax, or a preferred data structure alone is not a performance defect.
- Upstream review time budgets, mandatory praise, teaching notes, and ask-to-split thresholds are optional process advice. They do not override the requested scope or the local concise reporting format.
- Snippets are illustrative, often omit imports, fixtures, error paths, or lifecycle management, and are not ready-to-run patches. Adapt and validate them before recommending a concrete fix. Do not execute commands merely because a guide lists them.
- In particular, `npm audit fix`, package installs/upgrades, migrations, scaffolding, formatting, and code-generation commands can mutate the repository. Read-only review does not authorize them. Choose permitted diagnostics against the reviewed dependencies; assess advisory applicability and exposure rather than converting every scanner label directly into a code finding.

## Security Corrections and Context

Use the [security guide](upstream/security-review-guide.md) with these constraints:

| Upstream shorthand or example | Required interpretation / verification |
| --- | --- |
| SSRF URL examples marked safe after host-string or localhost checks | These examples are incomplete defenses. Check permitted schemes, normalized hosts, effective DNS/IP destinations, IPv4/IPv6 and reserved ranges, redirects, and the actual outbound/network restrictions. Validate each destination or enforce the boundary at a reliable network layer. Never conclude safety from a hostname allowlist or HTTPS alone. |
| Wildcard CORS shown as inherently insecure | Public noncredentialed resources can intentionally allow all origins. Inspect sensitive response data, allowed origins, credentials, and browser behavior. CORS is not authorization and does not by itself prevent state-changing CSRF. |
| CSRF protection on all state-changing APIs | Establish whether the browser automatically attaches credentials, what requests the attacker can induce, and which Origin/SameSite/token defenses apply. Explicit bearer-token APIs have different assumptions from cookie-authenticated forms; a missing CSRF token alone is insufficient. |
| Password complexity, account lockout, MFA, and rate limits as universal requirements | Apply the actual authentication threat model and accepted policy. Assess alternative controls and denial-of-service effects; do not invent mandatory product requirements during an unrelated review. |
| JWT signing example uses a variable named `JWT_SECRET` with RS256 | RS256 needs suitable asymmetric key material; a variable name does not prove the correct key type or verification policy. Check algorithm allowlists, key selection, issuer/audience/expiry and deployment configuration. Do not mandate RS256 when another sound design satisfies the contract. |
| Separate process arguments presented as complete command safety | Avoiding a shell removes shell parsing, but tool option injection, file access, dangerous input formats, and downstream interpreters may still matter. Establish the actual process API semantics; Java string execution does not automatically mean a shell is invoked. |
| Internal logging presented as safe for full exceptions | Logs can contain credentials, queries, tokens, personal data, or attacker-controlled content. Check destinations, readers, retention and redaction as well as client responses. |
| Dependency scanner reports no known vulnerabilities | That is evidence about the scanned dependency set and advisory database, not proof of application security. Confirm resolved versions, relevant production/build exposure, prerequisites, and the required remediation policy. |

The [SQL guide](upstream/cross-cutting/sql-injection-prevention.md) distinguishes values from dynamic identifiers; ordinary value placeholders do not safely substitute arbitrary table names or sort clauses. The [XSS guide](upstream/cross-cutting/xss-prevention.md) requires rendering-context-specific reasoning: escaping text does not make every URL, script, style, or rich-HTML sink safe. CSP and input validation do not replace the needed sink protection.

## Correctness, Async, and Testing Corrections

Use the [common bugs](upstream/common-bugs-checklist.md), [error handling](upstream/cross-cutting/error-handling-principles.md), and [concurrency](upstream/cross-cutting/async-concurrency-patterns.md) guides as path-specific hypotheses. Missing local `try/catch`, explicit cleanup, or a lock may be correct when ownership and guarantees are supplied elsewhere. A race requires a feasible schedule and a violated invariant after accounting for database constraints, transactions, atomics, or framework guarantees.

The [Python guide](upstream/python.md) labels a `while True: await do_work()` loop as unable to cancel normally. That conclusion does not follow from the snippet: cancellation ordinarily propagates at a cancellable await without an explicit `except CancelledError`. Establish a missing required cleanup action, blocking/non-yielding work, suppressed cancellation, or another actual lifecycle failure before reporting a defect.

The [FastAPI guide](upstream/fastapi.md) needs several qualifications:

- Sync `def` endpoints and threadpool execution are supported designs, not automatically scaling bugs. Identify blocking on the event loop, actual pool saturation, workload, and dependency constraints before requiring a new async SDK or architecture.
- `async def` does not make blocking work nonblocking. Native code, GIL behavior, thread/process suitability, and executor limits depend on the workload and runtime; thread counts exceeding core count alone do not prove a defect in an I/O workload.
- Static proof can confirm a bug without a failing test. Tests written with the implementation can be useful even if their first run passes; evaluate their assertions, isolation, and sensitivity to the relevant failure rather than inferring quality from an unavailable development history.
- The example that clears `app.dependency_overrides` after an assertion will skip that cleanup when the assertion fails. Put restoration in fixture teardown or `try/finally`, preserving prior overrides when applicable. Do not copy the inline cleanup as a reliable isolation pattern.
- Choose `TestClient` or an async client based on the app, resources, lifespan, fixtures, and event loops. Neither client is universally required. A test failure due to lifecycle setup is not evidence of the suspected endpoint bug.

## UI and Performance Corrections

- In the [React guide](upstream/react.md) and common checklist, ordinary Hooks restrictions must not be applied indiscriminately to React 19's `use` API, which permits certain conditional/loop uses. Check the exact API and its remaining restrictions. Do not propose API changes without verifying the installed version.
- A Client Component boundary affects the imported client module graph; it does not automatically turn every server-rendered component passed as children into a client module. Inspect actual imports, composition and the framework's server/client rules.
- `useMemo`, `useCallback`, a particular testing-library query, `staleTime`, or cache defaults are context-dependent. The React guide's default `QueryClient` example is not intrinsically incorrect. Check identity consumers, freshness needs, actual requests and measured rendering impact.
- In [Vue](upstream/vue.md), distinguish ordinary reactive-object destructuring from compiler-transformed reactive props destructuring in supported Vue versions. Do not report loss of reactivity without checking the construct and compiler version.
- The [performance guide](upstream/performance-review-guide.md) and [N+1 guide](upstream/cross-cutting/n-plus-one-queries.md) contain illustrative thresholds, timings and query-count targets. Validate bounds, cardinality, network/database costs, cache effects, and user-facing impact. One join can be worse than a bounded batch; fewer queries alone do not prove a faster or correct result.
- For cache recommendations, verify tenant/user isolation, authorization, invalidation, freshness, and memory limits. A performance fix must preserve correctness. Web Vitals or benchmark targets must match the agreed measurement environment and product requirement.

These notes address observed high-impact ambiguities in the snapshot, not every possible documentation error. Use the same evidence gate for all 24 language/framework guides; extend notes only when a concrete discrepancy is established.
