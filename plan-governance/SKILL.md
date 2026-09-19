---
name: plan-governance
description: Create and govern frozen implementation plans, file-level change inventories, approved execution batches, progress ledgers, automated verification, and handoffs. Use for confirmed engineering work needing a persistent plan; not open-ended brainstorming or unrequested implementation/deployment.
---

# Plan Governance

Plan by business outcome; execute compatible changes in batches. A precise file inventory describes WHAT to change, not a requirement to run a complete edit-test-report cycle for each row. Use kiss-solution-design for solution complexity review.

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

- **README.md — frozen design**: problem/evidence, business task IDs and outcomes, scope/non-goals, architecture and ownership, decisions, constraints, acceptance criteria, rollout/rollback and risks. It contains planned requirements, not live execution results.
- **tasks.md — frozen execution specification**: aggregate all approved business tasks into workstreams, exact change inventories, dependency batches, verification schedule, ownership and parallel proposals. It explains exactly which files/symbols change and what each batch must deliver.
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

## Business view and file-level inventory

Preserve stable business IDs (T-001, etc.) and acceptance outcomes in README; tasks.md maps changes back to these IDs. Do not duplicate a full end-to-end business workflow beneath every business task as the execution order.

Group the inventory by database, API implementation, API integration, UI implementation and automated UI verification. Every executable change has:

- Stable change ID (DB-001, API-001, INT-001, UI-001, UIV-001, TEST-001).
- Source business IDs; exact repository-relative file paths; target table/function/route/component/permission/test.
- Concrete action and expected output; owner; inputs; dependencies and shared resource conflicts.
- Acceptance check and verification ID. A verification reference does NOT mean run it immediately after this row.

Inspect code before asserting existing paths or symbols. Label proposed new files explicitly. Do not invent paths for precision or use ellipses, broad directories, or 'affected APIs' as executable targets. Combine compatible edits to the same file/target across business tasks; do not split every small symbol into its own delivery gate.

Resolve file discovery before freezing implementation scope. If discovery is itself the only approved work, give it a DISC ID and a bounded search/output; implementation remains blocked until the user explicitly requests replanning with the findings. A discovery task cannot authorize automatic edits to frozen tasks.md.

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

Check ID references across inventory, batches, lane assignments and ledger; dependency feasibility; exact path/action precision; implementation versus acceptance semantics; catalog-to-ledger status; and evidence validity. Check frozen files were not rewritten without explicit replanning and that execution did not silently expand scope.

Specifically reject 'edit → full test chain → update four documents' repeated for each inventory row. Require batch membership, verification timing/rerun rules and one narrative handoff location. Check UI automation defaults and user-approved exceptions. Handoff starts empty but may have content after any meaningful execution turn; do not require an agent switch or erase existing content.

Report affected repositories, changed plan paths, lifecycle, approval boundaries, validation and blockers. Never include credentials. Local-only files are not automatically backed up. Do not rewrite existing project plans just because this skill was updated; frozen plans require explicit user replanning.
