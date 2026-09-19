# Plan Governance Template

Use applicable sections only. README.md and tasks.md freeze on user finalization/execution approval; edit them thereafter only on an explicit user request to replan. Execution updates taskList.md and 计划交接文档.md, not the frozen specification. Catalog mirrors the ledger lifecycle.

## `plan/<feature>/README.md` — frozen design

```markdown
# <Feature>

## Baseline and ownership
- Plan revision:
- Owner and affected repositories:
- Repository boundaries and plan location:
- Baseline reviewed:
- Freeze/approval reference:
- Live progress: taskList.md
- Execution evidence and recovery: 计划交接文档.md

## Problem, evidence and target outcomes

Summarize the overall problem and outcome here. Link to tasks.md Part I for the authoritative detailed business tasks; do not maintain a duplicate requirement specification.

- Business task index and links:
- Overall acceptance principles:

## Scope and non-goals
- Approved work:
- Explicitly excluded work:
- Database/deployment/parallel authorization boundaries:

## Existing system and decisions
- Existing capabilities to reuse:
- Responsibility boundaries and source of truth:
- Chosen approach and rejected alternatives:
- Contracts, security and data-integrity constraints:

## Planned execution
- Default: database → API implementation → API verification → UI implementation → automated UI verification
- Approved batching scope:
- Dependencies and justified exceptions:
- API gate before UI:
- UI automatic verification is default; no manual pre-check requirement.

## Acceptance and release requirements
- Required verification coverage:
- Rollout and separate authorizations:
- Rollback/recovery safeguards:
- Known risks and dependencies:

## Replanning history
Only update this section when the user explicitly requests replanning, not for execution progress.
| Revision | User request | Scope/decision change |
|---|---|---|
```

## `plan/<feature>/tasks.md` — frozen execution specification

Deliver construction drawings, not a list of future design work. Resolve current code facts, ask consequential business questions, apply relevant design skills, and finish implementation/test design in this planning round before requesting finalization. Label proposed new files and never invent existing paths. A discovery-only/staged deliverable is allowed only when explicitly requested by the user; do not substitute it for a requested full plan. Missing authorized access is a reported blocker, not permission to guess or bypass controls.

A completed document template is not necessarily a completed plan. Required interfaces, schemas, routes, test setup and assertions must not say 'decide during implementation'. Preserve the detailed design sections below; do not compress them into a few Output/Acceptance sentences.

```markdown
# Execution specification

## Scope and ownership
- Plan revision:
- Approved business IDs:
- Owner/integration owner:
- Execution mode and authorization boundary:
- Shared files/resources:
- Cost estimates: 快 5–10 / 中 10–20 / 慢 20–40 / 超慢 >40 minutes

## Part I — Business tasks: what must be achieved

### T-001 <business requirement>
- Problem and inspected current behavior/evidence:
- Actors and transaction-specific roles:
- Preconditions:
- Current business flow (ordered steps):
- Target business flow (ordered steps):
- Business rules, data visibility and allowed actions:
- Exceptions and expected outcomes:
- Scope and explicitly unchanged behavior:
- Observable acceptance outcomes:

Repeat for T-002 and every approved requirement. Do not stop at a short Output/Acceptance paragraph. Do not attach a separate DB→API→UI execution loop to each task.

### Planning questions and decisions
| Question affecting implementation | Code evidence / user decision needed | Options and impacts | Confirmed decision / reference |
|---|---|---|---|

Unresolved consequential choices keep the plan draft. For repository facts continue permitted investigation now; for business choices ask the user with options/impacts/recommendation; for access/environment limitations report the actual blocker. Listing questions is not resolving them. No 'reject or ignore, decide later' in an executable plan and no production design-closeout batch to postpone this work.

## Part II — Production batches: unified design and implementation order

First review ALL Part I tasks together. Explain common data ownership, reusable interfaces/components, overlapping file changes and resolved conflicts. Derive the batches from this unified design rather than concatenating isolated feature plans.

### Professional design decisions
Load only applicable available skills during planning; write their selected conclusions rather than 'consult during UI implementation'.

| Applicable skill / discipline | Evidence and selected design | Reason / reuse boundary | Affected change IDs | Acceptance criterion |
|---|---|---|---|---|

Cover relevant KISS scope, component/style ownership, admin role/form/feedback design, reference fidelity and UX/layout/accessibility. If a discipline does not apply, do not manufacture work.

### Requirement coverage
| Business task | Implementation change IDs / batches | Verification scenario IDs |
|---|---|---|

### Batch schedule
Batch membership determines execution order; inventory rows are not independent edit-test-report cycles.
Only include applicable batches. Reuse existing IDs instead of introducing unnecessary numbering systems.

| Batch ID | Work type | Covered change IDs | Entry prerequisites | Implementation exit / verification gate | Owner | Cost |
|---|---|---|---|---|---|---|
| B1 | Database | DB-001… | Approved database scope | All planned schema/migration outputs and required immediate safety checks | | |
| B2 | API implementation | API-001… and planned test-code preparation | B1 required outputs | All approved API/contract/consumer wiring implemented | | |
| B3 | API verification | TEST-001…, INT-001… | B2 implementation ready | Planned builds, type checks and business-flow/integration checks pass | | |
| B4 | UI implementation | UI-001… | B3 gate passed | All affected pages/components implemented | | |
| B5 | UI automated verification | UIV-001… | B4 implementation ready | Automated checks pass; repairs and affected regression complete | | |

### Detailed batch implementation design

Complete the applicable sections below with inspected repository facts and confirmed decisions. Text may be long when necessary: execution must not have to redesign the workflow. Mark an inapplicable layer unchanged with a reason, not invented work. Replace all placeholders before freezing.

#### Database batch — unified data changes
- Related tasks and shared data ownership:
- Current versus target schema:

| Table/column/relation | Current definition | Target type/default/nullability/index/constraint | Reason and affected readers/writers |
|---|---|---|---|

- Ordered implementation steps with exact schema/migration files:
- Existing-data handling and compatibility decision:
- Migration/application commands, prerequisites and authorized database target:
- Structure/data checks and recovery procedure:

#### API batch — interfaces and processing steps
Repeat the following for each affected API, merging shared work across tasks:
- Change ID and source task IDs:
- Existing entry point/call chain and evidence:
- Reuse/modify/add decision and reason:
- Exact method/route/action and files/functions:
- Request fields: required/optional, validation and trusted source:
- Response fields and role-dependent visibility:
- Authentication, actual-party permissions and forbidden operations:
- Ordered processing: reads → validations → writes → state transitions → result:
- Transaction, idempotency and relevant side-effect boundaries:
- Error outcomes (decide rejection versus ignoring explicitly):
- Consumers/contracts to update, with exact paths and steps:

#### API verification batch — executable workflow scripts
- Script ID and exact existing/proposed script path:
- Run command, working directory, server startup and prerequisites:
- Isolated target and guard against business/production data:
- Seed data and role-specific accounts; authentication method:
- External service substitutes and prohibited real side effects:

| Step | Acting role | API method/route/action | Concrete request / prior-step output used | Expected status and response assertion | Persistence / permission / side-effect assertion |
|---|---|---|---|---|---|

Define the entire business journey, not only individual endpoint smoke tests. Include positive paths, missing/invalid inputs, unauthorized access, data leakage and applicable retries/concurrency. Each negative case states the exact expected rejection/ignore behavior and unchanged data.

- Test cleanup/isolation teardown, including failure paths:
- Failure step reporting, nonzero exit behavior and evidence location:
- Supplementary unit/regression cases (not a substitute for authenticated API flow):
- Coverage mapping to Part I tasks:

#### UI batch — unified page and component changes
Repeat for each affected page/component, combining related tasks:
- Task/change IDs, exact route/component/file:
- Current versus target user journey:
- Fields/sections/actions to add, remove or retain:
- Role visibility and operation permissions:
- API binding, submitted payload and displayed response fields:
- Ordered code changes and shared component reuse:
- Loading/empty/error/retry/success/navigation behavior:

#### UI automated verification batch — explicit interactions
- Script/test paths, environment, accounts, commands:

| Scenario | Role and initial data | Route and ordered actions | Expected visible/result states | Error/permission checks | Evidence |
|---|---|---|---|---|---|

- Relevant viewport/refresh/back-navigation checks:
- Failure collection, repair and affected rerun procedure:

### Aggregated file-level change inventory
Index the detailed designs above; a short table cannot replace them. These are specifications, not taskList progress checkboxes. Group compatible changes across business tasks; do not repeat the same file edit under each feature.

### Database
| ID | Source business IDs | Exact repository/file | Table/symbol | Action and output | Dependencies | Verification ID |
|---|---|---|---|---|---|---|

### API implementation and test-code preparation
| ID | Source business IDs | Exact repository/file | Route/function/contract | Action and output | Dependencies | Verification ID |
|---|---|---|---|---|---|---|

### UI implementation
| ID | Source business IDs | Exact repository/file | Route/component | Action and output | Dependencies | Verification ID |
|---|---|---|---|---|---|---|

## Verification schedule
Validation references above do not require an immediate run after each edit.

| Verification ID | Covered change IDs | Exact command/check and working directory | Environment/prerequisites | Timing: immediate / batch / final UI | Rerun trigger | Evidence destination |
|---|---|---|---|---|---|---|

- Immediate checks are narrowly necessary for safe continued implementation; full build/type/regression chains are not automatically lightweight.
- Test code may be written during implementation without running all suites after every file change.
- Run dependency-aware batch checks → collect safe-to-collect failures → group fixes by root cause → rerun affected checks → required batch regression.
- If a prerequisite fails, do not run dependent checks against invalid artifacts.
- Reuse passing evidence only while relevant source/contracts/environment remain valid.
- Final reporting does not itself require rerunning all previously valid tests.
- Recurring failures: bounded repair pass, then explicit blocker/decision rather than an endless loop.

## Proposed lanes (only if needed)
| Lane | Batch/change IDs | Start condition | Shared conflicts | Handoff output | Integration owner |
|---|---|---|---|---|---|

Concrete parallel mapping requires explicit approval; record execution approval in handoff/ledger. A changed frozen mapping requires explicit replanning.

## Construction-readiness review — before finalization
Complete with references to the actual design above, not merely 'yes' because a heading exists.

| Check | Specification / inspected evidence / confirmed user decision | Pass or unresolved gap |
|---|---|---|
| Complete requirements and resolved consequential choices | | |
| Unified database design, compatibility, migration/no-change decision and recovery | | |
| Real API entries, fields, permissions, ordered writes/state transitions and errors | | |
| UI routes, data/action binding, component and relevant visual/interaction decisions | | |
| Test authentication/setup, data, exact calls, per-step assertions and cleanup | | |
| Cross-task coverage, shared-resource dependencies and actual production batches | | |
| Executor can implement without new core design; manager can understand progress | | |

- Remaining planning gaps and action to resolve them now:
- Result: planning incomplete / construction-ready for user review.
- User finalization reference (only after readiness and actual confirmation):

A gap in required design prevents construction-ready status. Do not call a full plan complete because the files were created, or replace missing design with a future Bx-P batch. User-explicit discovery-only plans must be labeled limited research deliverables, not full implementation plans. Runtime execution approval remains separate from blueprint completeness.

## Stop and recovery boundaries
- Stop unsafe or out-of-scope operations; continue unaffected authorized work where safe.
- Missing files/scope/dependencies: record findings and proposed revision in handoff, request replanning; do not rewrite this file automatically.
- Required preservation, database target and external-side-effect safeguards:
```

## `plan/<feature>/taskList.md` — mutable batch ledger

One checkbox per batch. Do NOT put file-level/feature-level checkboxes beneath batch headings. Match actual batch IDs and members from tasks.md; the examples below are placeholders to replace before finalization.

```markdown
# Batch progress

- Status: 草稿（定稿且满足门槛后才转待执行）
- Plan revision:
- Planning readiness: 规划中 / 待用户澄清 / 图纸完整待确认 / 已定稿
- Current production batch and usable result:
- Current authorization:
- Blocker/owner/next action:
- Evidence and within-batch recovery: 计划交接文档.md

One checkbox per actual production batch; readable outputs come first, technical IDs are references.

- [ ] 数据库准备（B1）：交付本批统一结构与迁移准备；状态：未开始；已完成/剩余：；阻塞/下一步：；索引：DB-001…；证据：
- [ ] API制作（B2）：交付本批业务接口、权限及消费接线；状态：未开始；已完成/剩余：；阻塞/下一步：；索引：API-001…；证据：
- [ ] API流程验证（B3）：证明各角色完整业务流程及异常处理正确；状态：未开始；已完成/剩余：；阻塞/下一步：；索引：TEST-001…、INT-001…；证据：
- [ ] 页面制作（B4）：交付本批可操作的页面与组件；状态：未开始；已完成/剩余：；阻塞/下一步：；索引：UI-001…；证据：
- [ ] 页面自动核查（B5）：证明页面操作、权限和恢复场景通过；状态：未开始；已完成/剩余：；阻塞/下一步：；索引：UIV-001…；证据：

For an in-progress replan, map historical IDs/evidence into these batch results without resetting work or claiming broader acceptance. Keep original IDs when practical; explain historical mappings in the handoff. Do not present unfinished planning as production progress. Short remaining-work summaries belong here; detailed internal steps and logs stay in the handoff.

## Acceptance
- Implementation-batch completion is not verification or business acceptance.
- Partial progress keeps the batch unchecked; remaining item IDs and results go into the handoff.
- Final acceptance evidence / approved exceptions:
```

## `plan/<feature>/计划交接文档.md` — initially empty

Create a zero-byte UTF-8 file, without even a title. Never erase an existing file. It can be updated between execution turns, not only when agents/sessions change. All narrative handoff notes for the plan go here.

When there is meaningful execution progress, record concise dated deltas and a current recovery point:

- Current batch, authorized scope, completed and remaining change IDs.
- Actual changed files and implementation facts, without copying the full frozen specification.
- Commands, environment, outcomes, evidence references and coverage limits.
- Failure set, root causes, repair progress and which evidence remains valid.
- Next action/resume conditions, blockers and proposed changes awaiting user replanning.

Do not force tests or a full recap merely because a turn ends. At a batch exit/pause/takeover, ensure the recovery point is usable. Ledger references these results; README/tasks do not receive execution logs.

## `plan/catalog/README.md`

```markdown
# Plan catalog

Status comes from each plan's taskList.md, not frozen README metadata.

| Plan | Lifecycle | Owner | Updated | Path |
|---|---|---|---|---|
```

Lifecycle: 草稿 / 待执行 / 进行中 / 阻塞 / 已完成 / 已归档. Never archive incomplete required work to hide it.
