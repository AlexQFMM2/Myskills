# Reference Catalog and Routing

The local library includes every Markdown guide in the pinned upstream `reference/` tree: 24 language/framework guides and 11 cross-cutting/process guides. Use this index to select what the current review needs. Read [guide-adaptations.md](guide-adaptations.md) before applying imported guidance; [SKILL.md](../SKILL.md) owns scope, evidence, and decisions.

## Select References

1. Screen the requested behavior with [coverage-checklist.md](coverage-checklist.md), including error and boundary paths. Do not limit review only to issues the author calls out.
2. Identify languages, frameworks, runtime/compiler versions, dependencies and deployment roles from the reviewed source and manifests. A filename extension alone does not establish the framework or its version.
3. Select the applicable language/framework guides and cross-cutting topics below. Navigate headings or search for the affected API/pattern; read enough surrounding explanation to interpret it correctly. Do not load all 35 guides or every section of a long guide.
4. Use examples to generate candidates, trace the actual implementation and counterevidence, then apply the evidence gate. Deduplicate the same root cause encountered in several guides.
5. Record coverage and gaps. If an API/version is outside these guides, use actual source and authoritative documentation rather than forcing a newer framework idiom onto it.

Examples: a FastAPI authorization change may need the relevant FastAPI, security and test-verification sections; a Vue watcher change may need Vue plus cancellation/async guidance; a React text-only change may need neither a database nor a concurrency review. Java 8/Spring Boot 2 work normally uses the legacy Java guide, not modern Java requirements.

## Language and Framework Guides — 24

| Reviewed stack / trigger | Guide | Focus when relevant |
| --- | --- | --- |
| React, React 19 APIs, RSC, Next.js, TanStack Query | [React](upstream/react.md) | Hooks/effects, stale responses, server/client boundaries, actions, forms, Suspense, query identity/invalidation. |
| Vue 3, Composition API, Vue 3.5 features | [Vue](upstream/vue.md) | Reactivity, props/emits, watchers and cleanup, composables, keys, compiler-version distinctions. |
| Angular 17+, Signals, standalone components, RxJS | [Angular](upstream/angular.md) | Change detection, subscriptions, dependency injection, routing, interceptors, template behavior. |
| Svelte 5 / SvelteKit | [Svelte](upstream/svelte.md) | Runes, derived state, load functions, form actions, SSR/client state isolation and migrations. |
| TypeScript / JavaScript, including Node.js code | [TypeScript/JavaScript](upstream/typescript.md) | Runtime boundaries versus static types, narrowing, async/error flow, mutation, module resolution, tests. |
| CSS / Less / Sass | [CSS](upstream/css-less-sass.md) | Cascade, variable ownership, specificity, responsive layout, compatibility, measured rendering cost. |
| Python | [Python](upstream/python.md) | Mutable defaults/class state, exceptions, iteration, typing contracts, resource ownership, async and tests. |
| Django / Django REST Framework | [Django](upstream/django.md) | Query scoping, serializers, viewsets, CSRF, ORM behavior, N+1, async boundaries and transactions. |
| FastAPI / Pydantic | [FastAPI](upstream/fastapi.md) | Dependency/authorization paths, validation and response models, sessions, async execution, endpoint verification. |
| Java 17/21+, Spring Boot 3 | [Modern Java](upstream/java.md) | Records/patterns where supported, streams, Spring contracts, JPA, concurrency and virtual-thread constraints. |
| Java 8, Spring Boot 2, legacy javax stacks | [Java 8](upstream/java8.md) | Supported syntax/APIs, streams/Optional, time handling, bounded executors, CompletableFuture and legacy Spring/JPA. |
| NestJS | [NestJS](upstream/nestjs.md) | Module/DI scope, DTO validation, guards, interceptors, exception handling, request lifecycle and testing. |
| PHP | [PHP](upstream/php.md) | Runtime type/coercion behavior, PDO/ORM, input/output boundaries, Composer and PHPUnit/static-analysis evidence. |
| Ruby / Rails | [Ruby/Rails](upstream/ruby.md) | Ruby value semantics, Active Record scopes/transactions, jobs, security, version-dependent Rails behavior. |
| Go | [Go](upstream/go.md) | Error handling, goroutine/channel lifetime, context cancellation, shared state, interfaces and resources. |
| Rust | [Rust](upstream/rust.md) | Ownership/lifetimes, unsafe invariants, cancellation safety, blocking/locks across await, error handling. |
| C# / .NET / ASP.NET Core | [C#/.NET](upstream/csharp.md) | Task/cancellation flow, disposal, EF Core tracking/queries, LINQ evaluation, request/DI lifetimes. |
| Kotlin / Android / Jetpack Compose | [Kotlin](upstream/kotlin.md) | Coroutine scopes/cancellation, Flow, lifecycle, state/recomposition, nullability and resource retention. |
| Swift / SwiftUI | [Swift](upstream/swift.md) | Optionals, ARC/capture lifetimes, value/reference behavior, actors/Sendable, task and UI state ownership. |
| Dart / Flutter | [Dart/Flutter](upstream/dart.md) | Widget identity/rebuilds, async lifecycle, disposal, isolates, null safety, state and platform channels. |
| C | [C](upstream/c.md) | Bounds, pointers, integer/undefined behavior, resource cleanup, allocation failures and portability. |
| C++ | [C++](upstream/cpp.md) | RAII, ownership, lifetime/move semantics, exceptions, iterator invalidation and supported standard features. |
| Zig | [Zig](upstream/zig.md) | Allocators, defer/errdefer, slices/pointers, error unions, comptime and C interoperability. |
| Qt / QML | [Qt](upstream/qt.md) | QObject ownership/thread affinity, signals/slots, model/view contracts, QML binding and Qt-version differences. |

A framework guide complements its language guide where relevant; it does not require reading both in full. For polyglot changes, cover each affected runtime and the shared protocol/schema between them.

## Cross-Cutting and Process Guides — 11

| Trigger / review question | Guide | Evidence to establish |
| --- | --- | --- |
| Changed responsibilities, dependencies, layers, extension boundaries | [Architecture](upstream/architecture-review-guide.md) | An actual contract, ownership, coupling, or change-propagation problem; file size/pattern preference alone is insufficient. |
| New helper, duplicated operation, redundant state, broad updates, TOCTOU | [Universal quality](upstream/code-quality-universal.md) | Existing complete operations, divergent invariants, unnecessary writes, actual race windows or maintainability consequences. |
| Boundary logic, nulls, numbers, mutation, error or resource paths | [Common bugs](upstream/common-bugs-checklist.md) | A reachable failing case in the reviewed version; distinguish unsupported assumptions and stylistic advice. |
| Identity, resource access, untrusted data, secrets, API/dependency changes | [Security](upstream/security-review-guide.md) | Attacker/caller capability, full data/control path, effective defenses, concrete exposure and affected scope. |
| SQL values, dynamic identifiers, raw ORM queries | [SQL injection](upstream/cross-cutting/sql-injection-prevention.md) | Untrusted input reaches SQL syntax after considering parameter binding, identifier restrictions and actual driver semantics. |
| HTML, template, DOM, URL, script or style output | [XSS](upstream/cross-cutting/xss-prevention.md) | Rendering context, trust source, encoding/sanitization, framework escape hatches and realistic browser behavior. |
| Input size, query volume, rendering, caching, allocation or I/O changes | [Performance](upstream/performance-review-guide.md) | Supported workload/bounds, operation counts or measurements, consequential cost and correctness of proposed optimization. |
| ORM relationships, query loops, GraphQL resolvers or serializers | [N+1 queries](upstream/cross-cutting/n-plus-one-queries.md) | Queries actually executed under meaningful cardinality, existing batching/loading, and latency/memory effects. |
| Exceptions, retries, partial failures, external APIs or cleanup | [Error handling](upstream/cross-cutting/error-handling-principles.md) | Error ownership/propagation, observable failure, safe retry, resource recovery and disclosure boundaries. |
| Tasks/threads, shared state, cancellation, channels, locks or async callbacks | [Async and concurrency](upstream/cross-cutting/async-concurrency-patterns.md) | Feasible interleaving/lifetime failure after checking transactions, constraints, runtime guarantees and cancellation ownership. |
| User explicitly requests review communication or team process guidance | [Review best practices](upstream/code-review-best-practices.md) | Useful communication/process choices for this team; local report semantics and user authorization remain authoritative. |

The detailed guides are available offline with their [MIT license](upstream/LICENSE) and [source manifest](upstream/manifest.json). The catalog covers the pinned upstream library; it does not imply that every possible language, defect, or framework version is covered.
