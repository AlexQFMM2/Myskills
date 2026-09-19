---
name: plan-governance
description: Create and govern frozen implementation plans, file-level change inventories, approved execution batches, progress ledgers, automated verification, and handoffs. Use for confirmed engineering work needing a persistent plan; not open-ended brainstorming or unrequested implementation/deployment.
---

# Plan Governance

Turn large requirements into construction-ready blueprints that reduce execution uncertainty, repeated design, rework and opaque progress. Producing four files is NOT the completion objective. README introduces the building; tasks supplies its construction drawings and production organization; taskList shows construction progress to the manager; the handoff lets agents continue internal work without rediscovering it.

Plan by business outcome; execute compatible changes in batches. Prepare the whole approved design before construction, rather than sourcing materials, inventing interfaces and rebuilding for each feature. A precise file inventory locates work but does not explain HOW to build it. Require current behavior → target behavior → ordered modifications → concrete verification, with depth proportional to risk and uncertainty. Long useful specifications are preferable to short ambiguous summaries; repetition and irrelevant detail are not useful depth. Ordinary coding details remain with the implementer; consequential design does not.

## Modes and authority

- Draft: discuss a plan without writing files.
- Persist: write the requested plan files; planning does not authorize implementation.
- Audit: inspect without changing unless requested.

Do not start agents, change runtime code, deploy, commit, or push merely because the plan mentions those actions.

## Four artifacts and the freeze rule

```text
plan/
├── catalog/README.md
└── <feature>/
    ├── README.md
    ├── tasks.md
    ├── taskList.md
    └── 计划交接文档.md
```

Read references/plan-template.md when creating or substantially revising a plan.

- **README.md — frozen overview**: problem/evidence, summary and links to business tasks in tasks.md, scope/non-goals, architecture, ownership, key decisions, constraints, acceptance principles, rollout/rollback and risks. Do not maintain a second detailed task specification here or record live execution results.
- **tasks.md — frozen two-part implementation plan**: Part I contains the complete business tasks (requirements); Part II derives the detailed production batches from the WHOLE approved task set. It explains current/target flows, unified database/API/UI changes, exact implementation steps and executable verification scenarios. A short Output/Acceptance list or file table alone is insufficient.
- **taskList.md — mutable batch progress ledger**: one progress unit/checkbox per execution batch, with batch ID, covered change IDs, status, blockers and evidence references. Do not create separate progress indicators for functions, business features or individual files. Exact file-level actions remain in tasks.md; batch-internal progress belongs in the handoff.
- **计划交接文档.md — mutable execution and recovery record**: create as an empty UTF-8 file (no heading/template). Update between turns as well as across sessions, agents or owners. Record meaningful deltas, actual changed files, commands/results, failures and fixes, environment facts, next action and resume conditions. All narrative handoffs for this plan belong here; do not create separate per-turn HANDOFF documents. Reference large raw test artifacts instead of copying them.

Once the user finalizes the plan or authorizes execution of it, README.md and tasks.md are frozen. **Only an explicit user request to replan authorizes editing either file.** Starting/continuing execution, completing a batch, failing a test, discovering a discrepancy, updating lifecycle status or preparing a handoff does not authorize rewriting them, even just their metadata.

During execution update taskList.md and 计划交接文档.md only within the feature plan. Catalog lifecycle navigation may be synchronized from taskList.md; never from a frozen README status. Routine progress must not trigger rewriting all four files.

If execution reveals missing paths, new scope, changed dependencies or an incorrect frozen instruction, record findings and a proposed change in the handoff, mark the affected ledger item blocked, and request explicit replanning before implementing the changed scope. Continue unaffected authorized work where safe. Do not silently add/redefine tasks in the ledger as a workaround. Ordinary fixes within a planned change and its acceptance criteria do not require replanning.

When replanning is explicitly requested, revise both frozen specifications as needed, preserve stable IDs and historical evidence, reconcile the ledger, and freeze the new revision when confirmed. Never erase or empty an existing handoff file.

## Repository and plan ownership

- Single repository: use <repository>/plan/.
- Independent repositories: use an explicitly designated workspace plan or owner repository; list affected repositories and integration owner.
- Read workspace guidance and inspect actual repository boundaries and affected Git status before writing. A non-Git workspace may contain independent repositories or nested category folders; never initialize Git at its root to satisfy this skill.
- Check ignore/tracked status within the owning repository before claiming the plan is excluded from Git. Do not silently untrack files. For a non-Git plan location, Git ignore checking is not applicable; report storage/backup limitations instead of pretending it is protected.

## Planning depth and clarification gate

Prefer extra clarification during planning over repeated design and rework during execution. Read code to establish facts the repository can answer; ask the user about consequential business choices with options, impacts and a recommendation. Do not ask the user to perform code discovery for you. Resolve ambiguity about roles, workflows, data disclosure, compatibility, side effects and acceptance BEFORE finalization.

Length is not a defect when it removes uncertainty. A precise path plus 'implement the feature' is still not an implementation design. Do not hide unresolved decisions behind 'improve', 'handle appropriately', 'add necessary logic' or a short Output/Acceptance paragraph. Record unknowns and keep the affected specification draft until resolved; do not silently downgrade a full implementation-planning request to a discovery-only deliverable. Execution should not have to invent business rules, interface contracts or test expectations; ordinary coding details remain the implementer's responsibility.

## Required planning workflow and completion gate

Within authorized access, complete this workflow during planning, not as future production batches:

1. Inspect the existing schema, real API/call chains, permissions/state transitions, reusable capabilities, page/routes/components and test/authentication entry points. Gather evidence rather than guess paths.
2. Resolve questions: investigate repository facts yourself; ask the user about business choices with evidence, options, impacts and a recommendation; report concrete access/environment blockers. Do not merely file questions for a future execution agent.
3. Write the complete business requirements, then derive one holistic DB/API/UI design and production sequence across the approved scope.
4. Apply relevant professional skills during design and record their selected conclusions in the blueprint.
5. Specify exact implementation steps, dependencies and executable test scenarios. Cross-check request/response contracts, UI bindings, role transitions and tests for contradictions.
6. Review build-readiness, resolve remaining gaps, and only then present the specification for user finalization. File-writing success is not planning completion.

A full implementation request does not need a second 'continue planning' authorization for ordinary already-authorized code reading. Do not invent a B3-P/design-closeout production batch to defer finding API names, deciding fields, locating routes or designing test authentication. Discovery-only or deliberately staged planning is an exception ONLY when explicitly requested by the user; name its limited deliverable and unfinished implementation scope. Real access limits remain limits: report them, never bypass them to complete planning.

The build-readiness review must answer, with specification references:

- Are consequential business choices resolved and each requirement covered by implementation AND verification?
- Are schema changes/no-change decisions, compatibility and migration/recovery procedures settled?
- Are API actions, input/output contracts, permissions, ordered processing, state changes and error outcomes determined?
- Are UI entry points, data sources, role actions, component responsibilities and important interaction/visual requirements determined?
- Are script paths, real authentication/setup entry points, fixtures, ordered calls/actions, per-step assertions, commands and safe cleanup specified?
- Can an implementer proceed without making new business/architecture decisions, and can a manager understand batch outputs and blockers without decoding change IDs?

Unresolved required design means 'planning incomplete', not 'ready for implementation'. Explain the exact gaps and continue permitted investigation or ask the concrete questions. Do not request final approval for a blueprint that says 'action/schema/route/expected errors to be filled during execution'. These phrases are diagnostic signals, not a mechanical word ban: explicitly excluded future work may remain undesigned. Record the review in tasks while drafting; after freeze record audit results in the handoff without rewriting the specification. User execution approval does not magically resolve missing design; surface the gaps.

## Professional skill integration during planning

Load applicable skills from the current catalog before using them. Do not load every skill unconditionally or reproduce their entire instructions. In tasks record the chosen design conclusions, rationale, affected changes and verification criteria:

- kiss-solution-design: reuse, scope/complexity boundaries, and the simplest complete solution; avoid turning a small house into a skyscraper.
- maintainable-ui-engineering: component/module ownership, shared logic, style/token boundaries and integration conventions.
- admin-ui-usability: actual role journeys, business-friendly forms, permissions, safe transitions, feedback and recovery.
- reference-ui-reconstruction: when a visual reference exists, evidence-based layout and fidelity requirements.
- ui-ux-pro-max: relevant layout, interaction, responsive and accessibility decisions.

'Consult the UI skill during implementation' is not a substitute for resolving design that affects construction now. Implementation-time checks may confirm the design, not become its first creation. If a required skill is unavailable, report that limitation and resolve the required design explicitly rather than claiming it was applied.

## tasks.md Part I — complete business requirements

Use stable business IDs (T-001, etc.). This part is the authoritative detailed task specification; README summarizes or links to it. For each task explain the problem and observed current behavior, actors and their relationship to the transaction, prerequisites, target step-by-step business flow, rules, exceptions, scope/non-goals and observable acceptance outcomes.

'Abstract requirement' means business-level language, not ambiguity. For example distinguish first-time inquiry creation with required buyer details from forwarding an inquiry upstream without copying or recollecting those details. Specify what each party sees and may do, including a party acting as seller downstream and buyer upstream. Do not automatically prescribe new create/forward APIs before inspecting existing capabilities.

Complete the approved requirement set before deriving its implementation. Do NOT organize production as task 1 DB/API/UI/test, then task 2 DB/API/UI/test.

## tasks.md Part II — holistic implementation batches

Review ALL approved Part I tasks together. Resolve shared data models, contracts, pages, conflicting requirements and reusable capabilities before defining batches. This is unified design, not concatenating per-feature file lists. A batch change may serve multiple tasks; map each task to its implementation changes AND verification scenarios so no requirement disappears during aggregation.

For each applicable batch supply detailed prose/steps as well as the file inventory:

- Database: current and target tables/columns/types/nullability/defaults/indexes/relationships, shared ownership, old-data handling, exact schema/migration files, ordered migration/application procedure, authorized target, checks and recovery. Explain why unchanged database layers need no work.
- API: verified existing entry points and call chain; which to reuse/modify/add and why; exact route/action/method, request and response fields, identity/permission rules, ordered reads/writes and state transitions, transaction/idempotency behavior and defined error outcomes; exact files/functions and affected consumers. Specify field allowlists where data isolation matters. 'Reject or ignore' must be decided, not left to the executor.
- UI: current and target user journey, exact routes/components, fields to add/remove/retain, API bindings and payloads, role-specific actions, success/loading/empty/error/retry behavior and affected shared components. Aggregate multiple tasks changing the same page into one coherent implementation.
- API verification: specify the script path (existing or proposed), command, working directory, isolated environment, fixtures/accounts/authentication, safe external substitutes and cleanup; ordered role-specific API calls with concrete input and per-step response/persistence assertions. Exercise a complete workflow through real API boundaries and authorization, not only direct helper calls. Plan positive, invalid-input, unauthorized and relevant repeat/concurrency cases. State exit codes, failure output and acceptance evidence. Unit tests supplement this flow, not replace it.
- UI automated verification: define environment/accounts, routes, concrete actions and expected states, error/permission and relevant viewport checks, artifacts and rerun conditions; a vague 'UI check' is insufficient.

A representative API scenario could seed isolated buyer A, intermediary B and upstream C; authenticate each; have A create an inquiry with required details, B forward without those details, C inspect and quote, B inspect the upstream quote and issue its own downstream quote, and A read it. Specify assertions on data isolation, lineage and permissions at each step, plus negative cases and cleanup. This is an illustration, not a claim that these endpoints or actors exist in every repository; replace with inspected actual contracts.

## File-level inventory within batches

The inventory indexes the detailed batch design; it must not replace the implementation steps or test scenarios.

Group the inventory by database, API implementation, API integration, UI implementation and automated UI verification. Every executable change has:

- Stable change ID (DB-001, API-001, INT-001, UI-001, UIV-001, TEST-001).
- Source business IDs; exact repository-relative file paths; target table/function/route/component/permission/test.
- Concrete action and expected output; owner; inputs; dependencies and shared resource conflicts.
- Acceptance check and verification ID. A verification reference does NOT mean run it immediately after this row.

Inspect code before asserting existing paths or symbols. Label proposed new files explicitly. Do not invent paths for precision or use ellipses, broad directories, or 'affected APIs' as executable targets. Combine compatible edits to the same file/target across business tasks; do not split every small symbol into its own delivery gate.

Resolve file discovery as part of the current planning work before freezing implementation scope. Only for a user-explicit discovery-only/staged request may a DISC item itself be the deliverable; mark it as planning work, separate from the production progress view. Do not introduce discovery as a default escape from finishing a full blueprint. Findings never authorize automatic edits to an already frozen tasks.md.

## Execution batches, not row-by-row delivery

The approved scope is the batching boundary. Do not enter an unauthorized business wave to improve batching. Within that scope default to:

1. Database batch: enumerate and implement all related schema/migrations/local database preparation. Apply only to authorized targets, retaining data-integrity and recovery safeguards.
2. API implementation batch: complete contracts, services, permissions, consumers and composition across the approved tasks. Test code can be written alongside implementation without running full suites after each edit.
3. API verification batch: run the planned build/type checks and API business-flow tests, then integration checks against authorized isolated resources. Aggregate failures, repair by root cause, rerun affected checks and perform required batch regression.
4. UI implementation batch: enumerate and implement all related pages/components after the API gate passes.
5. UI automated verification batch: automatic by default, after UI implementation; collect failures, repair and rerun affected checks. Manual viewing is not a default prerequisite or a substitute. Any waiver requires explicit user approval and recorded coverage limitations.

A batch can include many precise file items. Document its member IDs, entry prerequisites, implementation exit condition, verification gate and authorization boundary before freezing. Business waves B0/B1/etc. express dependency/scope boundaries, not automatic per-task testing instructions. Skip inapplicable layers with a reason; do not manufacture database work for a UI-only change.

Do not reset a batch at each turn, checkbox, file, business task or agent handoff. Resume its remaining work. Serial execution means one safe stream of edits, not complete testing and handoff after every row.

## Verification scheduling and cost

Classify expected cost using the user's approximate ranges: 快 5–10, 中 10–20, 慢 20–40, 超慢 >40 minutes. These are estimates, not mandatory delays or permission to skip safety checks.

Each verification entry names the exact command/check, working directory/environment, covered change IDs, timing, prerequisites and rerun trigger:

- Immediate lightweight check: focused syntax/parse/startup or a narrowly targeted diagnostic necessary for safe continued work. Repeated auth/contracts builds, whole-API type checks and multi-file regressions are not lightweight merely because they are automated. Record the reason for an exceptional early expensive run.
- Batch gate: shared builds, type checks, targeted suites and API integration after the corresponding implementation batch. If generation/build is needed to unblock implementation, do that required prerequisite without automatically running the entire test chain.
- Final UI gate: concentrated automated checks of affected routes, interactions, errors, permissions and relevant layout states.

Run the dependency-aware verification set, collect failures where safe, group fixes by root cause, then rerun affected checks. Stop dependent checks when prerequisites fail; stop unsafe operations rather than accumulating harmful failures. Do not blindly rerun the full chain after every tiny fix.

Reuse passing evidence only when relevant source, contracts, dependencies, environment and test configuration remain valid. Record what change invalidates it. A final summary does not inherently require repeating every already-valid test; shared changes still require affected regression. Define a bounded repair pass; unresolved recurring failures become a documented blocker/decision rather than an endless green-test loop.

## Ledger and evidence semantics

Make taskList readable to the manager first: use a plain-language batch name, the usable result it delivers, status, a concise remaining-work/blocker summary, next action/owner and evidence link. Change IDs support traceability, not the primary explanation. Show planning readiness/approval separately from production progress; unfinished design is not completed construction. The manager should not need the long handoff to learn what has or has not been built.

When replanning an in-progress project, map retained historical IDs and evidence to the current understandable production batches; preserve their original scope without resetting accomplishments or upgrading partial/backend-only evidence to full completion. Keep technical historical mappings as references, not the main status language.

Use one checkbox per execution batch, not per function, business task, file or test case. Each line identifies its batch, covered change IDs, current status (pending/in progress/blocked/complete), exit condition and handoff evidence link. Merely putting file-level checkboxes under batch headings does NOT satisfy this rule. No feature-count or file-count completion percentages.

Exact file/target/action specifications stay in tasks.md. Record partial implementation, remaining change IDs, test failures and next action in 计划交接文档.md; the batch stays unchecked while incomplete. Do not split a batch into tiny batches just to obtain more checkmarks.

Separate implementation, verification and acceptance:

- An implementation-batch checkbox means all its defined implementation outputs and required immediate safeguards are complete. It does not claim the later verification batch passed.
- A verification-batch checkbox means all its required checks passed with valid evidence, or an explicit user-approved waiver is recorded.
- A business outcome is accepted only when its required implementation AND verification batches are complete.

Do not run expensive checks solely to tick an implementation batch. Do not mark implementation complete when only audit/design is done. Partial progress does not complete a batch.

taskList.md is authoritative for current lifecycle: 草稿 / 待执行 / 进行中 / 阻塞 / 已完成 / 已归档. The handoff is authoritative for detailed execution evidence and recovery facts. README/tasks remain the approved specification. Catalog is only an index and mirrors lifecycle changes from the ledger.

- 待执行 requires confirmed scope, owners, IDs, exact targets, batch schedule and acceptance.
- 进行中 requires actual authorized execution.
- 阻塞 records blocker, impact, owner and next action.
- 已完成 requires acceptance evidence, not only checkboxes.
- 已归档 requires no remaining required work/handoff; preserve history.

Update ledger progress as it changes. Between turns, add concise handoff deltas when useful for continuity; do not force a full recap or verification run each turn. At batch completion, pause or takeover, record a usable recovery point. Summarize results once in the handoff and reference them from the ledger.

## Parallel execution

Batching does not authorize parallel agents. Before proposing concurrency inspect unmet dependencies, shared files/generated artifacts/databases/environments, integration ownership and recovery paths. Same-file work, migrations, production operations and shared configuration are serial by default.

Before freezing record any proposed mapping in tasks.md: lane, change IDs, start condition, output/handoff and integration owner. Launch only after explicit user approval of that concrete scope/mapping. During execution record approval in the handoff/ledger without editing frozen tasks. Changing the planned mapping or scope requires explicit replanning and renewed concurrency approval.

Independent same-wave tasks may run together when safe; dependent later tasks wait for prerequisite exit evidence. Relay lanes are not simultaneous execution when one depends on the other's output. Cross-repository work still needs a serial shared-contract/integration gate. Keep plans independent of any specific agent API.

## Audit and delivery

Check that tasks.md contains both complete business requirements and holistic production batches, not only goals/file tables. Verify that current-to-target flows, database changes, API contracts, UI behavior and ordered test inputs/assertions are specified, all consequential questions are resolved, and every business task maps to implementation and verification. Reject plans that leave core design to the execution agent.

Check ID references across inventory, batches, lane assignments and ledger; dependency feasibility; exact path/action precision; implementation versus acceptance semantics; catalog-to-ledger status; and evidence validity. Check frozen files were not rewritten without explicit replanning and that execution did not silently expand scope.

Specifically reject 'edit → full test chain → update four documents' repeated for each inventory row. Require batch membership, verification timing/rerun rules and one narrative handoff location. Check UI automation defaults and user-approved exceptions. Handoff starts empty but may have content after any meaningful execution turn; do not require an agent switch or erase existing content.

Report affected repositories, changed plan paths, lifecycle, approval boundaries, validation and blockers. Never include credentials. Local-only files are not automatically backed up. Do not rewrite existing project plans just because this skill was updated; frozen plans require explicit user replanning.
