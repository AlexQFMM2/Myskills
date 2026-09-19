---
name: plan-governance
description: Create and govern implementation plans with cataloging, task waves, explicit concurrency approval, execution tracking, acceptance, and archival. Use for confirmed product or engineering work that needs a persistent handoff plan; do not use for open-ended brainstorming, KISS architecture review, or unrequested code/deployment changes.
---

# Plan Governance

Manage the plan as an auditable execution record. This skill governs where the plan lives, how work is handed off, when parallel work is allowed, and how completion is proved. It does not decide whether a solution is over-designed; use `kiss-solution-design` for that separate question.

## Operating modes

Choose the least mutating mode that satisfies the request:

- **Draft**: produce or revise a plan in the conversation without writing files.
- **Persist**: create or update the requested `plan/` files after the user asks for a persistent plan.
- **Audit**: inspect an existing plan, catalog, task state, ignore rules, dependencies, and evidence without changing them unless requested.

Do not start agents, edit runtime code, change deployment state, commit, or push merely because a plan mentions those actions.

## Locate the plan

- For a single-repository change, use `<repository>/plan/`.
- For a change spanning independent repositories, use a clearly designated workspace-level `plan/` or an explicitly chosen owner repository. Record that ownership in the plan.
- Inspect repository boundaries and current status before writing. In a multi-repository workspace, never treat the workspace root as one Git repository unless it actually is one.
- Verify that the plan path is ignored with `git check-ignore` before claiming it is local-only. If an existing plan is already tracked, report that fact; do not silently untrack it.

## Execution model: task view plus workstream view

Keep two views of the same work:

1. **Business task view**: what the user needs, such as `T-001 user management` and `T-002 audit log`. This view is the source for scope and final acceptance.
2. **Execution workstream view**: how to perform the work efficiently across all tasks. Group compatible changes instead of repeatedly taking each task from database to API to UI to final testing.

For ordinary feature work, use this default workstream order unless a concrete dependency requires another order:

1. **Database change plan**: enumerate all schema, migration, seed, index, and local-database changes across the tasks; implement them together and run database-level checks.
2. **API change plan**: enumerate all new or changed APIs, contracts, services, and errors; implement them together, then run a structural/API smoke check.
3. **API integration**: exercise the real business flows through the API layer, without depending on the UI. Fix cross-API, data, permission, and state-transition problems here.
4. **UI implementation**: enumerate affected pages and components, then implement the UI after the API flow is sufficiently stable.
5. **UI verification**: run the automated UI checks as the default final quality gate after the UI workstream. Do not repeat the expensive full UI check after every business task. If failures are found, record the failure set, fix it in a bounded repair pass, and rerun the relevant automated checks.

The workstream order is a default, not a license to ignore dependencies. Record exceptions and the reason. The API integration gate should pass before broad UI implementation begins unless the plan explicitly documents a safe mock/contract seam.

### Operation cost

Classify execution items by expected feedback and recovery cost, not only wall-clock duration:

- **Fast (快)**: roughly 5–10 minutes; examples include a focused schema/API edit or local database update.
- **Medium (中)**: roughly 10–20 minutes; examples include API flow checks or a focused UI change.
- **Slow (慢)**: roughly 20–40 minutes; usually a repair loop or a change with meaningful integration risk.
- **Very slow (超慢)**: over 40 minutes or with long feedback latency; UI automation and broad regression checks commonly belong here.

Use cost to schedule and batch work. Do not use it to skip necessary lightweight checks. Cheap syntax, startup, route, migration, or targeted smoke checks may happen inside a workstream; expensive end-to-end or UI automation should normally run at the workstream gate.

## Required structure

Create only the structure needed by the request:

```text
plan/
├── catalog/
│   └── README.md
└── <feature-name>/
    ├── README.md
    ├── tasks.md
    └── taskList.md
```

Read [references/plan-template.md](references/plan-template.md) when creating or substantially revising a plan. Keep the catalog a quick index, not a second copy of every task.

### Plan README

Record the problem, evidence, target outcome, scope and non-goals, current architecture, affected repositories and owners, chosen decisions, constraints, dependencies, schedule, acceptance, rollout, rollback, risks, blockers, and change history. Keep runtime configuration and credentials out of the plan.

### tasks.md

Give each business task a stable ID such as `T-001`. Group tasks into dependency waves (`B0`, `B1`, `B2`, ...), where a later wave cannot start until its declared prerequisites are satisfied. For every task record its owner, repository/files, inputs, outputs, acceptance check, dependencies, shared-resource conflicts, and handoff notes. Also record the task's execution workstream mapping, for example `DB-001`, `API-001`, `INT-001`, `UI-001`, or `UIV-001`, so grouped implementation remains traceable to the original business task. Mark parallel candidates explicitly, but do not treat that mark as authorization.

Do not replace business tasks with only layer tasks. The plan must preserve the business-task view and add the workstream view. A workstream may cover many business tasks, and one business task may map to several workstream items.

### taskList.md

Keep this file as the compact progress ledger. Use `- [ ]` and `- [x]` with the stable task IDs. Do not duplicate detailed task specifications here. A checked box is not sufficient evidence for completion; link or summarize the actual test, review, deployment, or acceptance result in the plan README.

### catalog/README.md

Index plans by status, owner, update time, and relative path. Use the lifecycle `草稿`, `待执行`, `进行中`, `阻塞`, `已完成`, and `已归档`. The `Status` field in each plan README is authoritative; the catalog is the navigation surface and must be updated when lifecycle state changes. Never hide a blocked or incomplete plan under “已归档”.

## Concurrency gate

Before proposing parallel execution, inspect all candidate tasks for:

1. Unmet dependencies or ordering constraints.
2. Shared files, generated artifacts, databases, environments, or external resources.
3. Clear ownership of the merge, integration, and final acceptance.
4. A safe recovery path if one branch fails or produces incompatible output.

Write the result into `tasks.md` as “parallel candidate” or “serial”. Explicitly ask for or record the user's approval before launching multiple agents. If approval is absent, prepare handoff notes only. Database migrations, production changes, shared configuration edits, and same-file changes are serial by default.

The user may choose a multi-agent workflow. Record the chosen execution mode, but keep the plan independent of a particular agent API or invocation mechanism.

Workstream batching does not automatically authorize parallel execution. A database workstream, API workstream, UI workstream, or verification workstream can still have shared files and ordering constraints. Ask for approval only for the concrete parallel assignment, not for the existence of the workstream model.

## How to run approved parallel work

Treat `B0`, `B1`, `B2`, ... as dependency waves, not as agent names or automatic scheduling instructions. After building the task dependency graph, choose one of these patterns and write the assignment into `tasks.md`:

### Wave-parallel

Tasks in the same wave can start together when they have no unmet dependencies and no unsafe shared resource. For example:

```text
Agent A: B1/T-101, B1/T-102
Agent B: B1/T-103, B1/T-104
```

Both agents report their outputs, tests, changed files, and unresolved issues to the integration owner before the next wave begins.

### Relay or pipeline

An agent owns an early wave and another agent owns a later wave. The later agent must wait for the earlier wave's exit evidence and handoff; this is staged parallelism, not simultaneous execution. For example:

```text
Agent A: B0 → B1
  handoff: API notes, changed files, tests, decisions
Agent B: B2 → B3
  start condition: Agent A's B1 acceptance is recorded
```

The example above is invalid as simultaneous execution if B2 depends on B0 or B1. If B2 is genuinely independent, split it into an explicitly independent task and document why it can start early.

### Cross-repository split

Independent repositories may be assigned to different agents, but shared contracts, generated artifacts, deployment configuration, and final integration remain a serial gate. The plan must name the integration owner and the exact handoff artifact.

For every approved assignment, record:

```markdown
| Agent/lane | Tasks | Start condition | Handoff artifact | Integration owner |
|---|---|---|---|---|
| Agent A | B0/T-001 → B1/T-003 | plan ready | test report + changed-file list | Agent C |
| Agent B | B1/T-004 | T-001 acceptance | adapter notes | Agent C |
```

Before launching, present the concrete mapping and ask for explicit approval. Approval applies to that mapping and scope only; adding a task, changing a shared file, or changing the execution order requires a new confirmation. If approval is absent, keep the assignment as a proposal and do not launch agents.

## Lifecycle and completion

- Move from `草稿` to `待执行` only when scope, owner, task IDs, dependencies, and acceptance are present.
- Move to `进行中` only when execution has actually started and any required concurrency approval exists.
- A `阻塞` state must name the blocker, impact, owner, and next decision or action.
- Mark `已完成` only after acceptance evidence is recorded, not merely when checkboxes are checked.
- Mark `已归档` only after no required task or handoff remains. Preserve the plan for audit and recovery.

When auditing, check catalog-to-plan consistency, missing task IDs, unchecked tasks, impossible wave dependencies, missing business-task-to-workstream mappings, unauthorized parallelization, missing acceptance evidence, and whether `plan/` is truly excluded from publication. Also verify that API integration evidence exists before broad UI work, and that the default automated UI verification was either completed or has a recorded, user-approved exception.

## Delivery

When a persistent plan is requested, report the plan path, lifecycle state, affected repositories, concurrency decisions, unresolved blockers, and validation performed. Do not include secrets or assume that “not uploaded” means “backed up”; call out the storage and recovery trade-off when relevant.
