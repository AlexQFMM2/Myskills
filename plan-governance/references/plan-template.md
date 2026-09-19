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

| Business ID | Confirmed problem | Target outcome | Acceptance criteria |
|---|---|---|---|
| T-001 | | | |
| T-002 | | | |

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

Resolve existing paths by inspection before freezing. Label proposed new files. Do not use illustrative placeholders as executable targets. Discovery-only plans require explicit replanning before implementation can be added.

```markdown
# Execution specification

## Scope and ownership
- Plan revision:
- Approved business IDs:
- Owner/integration owner:
- Execution mode and authorization boundary:
- Shared files/resources:
- Cost estimates: 快 5–10 / 中 10–20 / 慢 20–40 / 超慢 >40 minutes

## Batch schedule
Batch membership determines execution order; inventory rows are not independent edit-test-report cycles.
Only include applicable batches. Reuse existing IDs instead of introducing unnecessary numbering systems.

| Batch ID | Work type | Covered change IDs | Entry prerequisites | Implementation exit / verification gate | Owner | Cost |
|---|---|---|---|---|---|---|
| B1 | Database | DB-001… | Approved database scope | All planned schema/migration outputs and required immediate safety checks | | |
| B2 | API implementation | API-001… and planned test-code preparation | B1 required outputs | All approved API/contract/consumer wiring implemented | | |
| B3 | API verification | TEST-001…, INT-001… | B2 implementation ready | Planned builds, type checks and business-flow/integration checks pass | | |
| B4 | UI implementation | UI-001… | B3 gate passed | All affected pages/components implemented | | |
| B5 | UI automated verification | UIV-001… | B4 implementation ready | Automated checks pass; repairs and affected regression complete | | |

## Aggregated file-level change inventory
These are specifications, not taskList progress checkboxes. Group compatible changes across business tasks; do not repeat the same file edit under each feature.

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

## Stop and recovery boundaries
- Stop unsafe or out-of-scope operations; continue unaffected authorized work where safe.
- Missing files/scope/dependencies: record findings and proposed revision in handoff, request replanning; do not rewrite this file automatically.
- Required preservation, database target and external-side-effect safeguards:
```

## `plan/<feature>/taskList.md` — mutable batch ledger

One checkbox per batch. Do NOT put file-level/feature-level checkboxes beneath batch headings. Match actual batch IDs and members from tasks.md; the examples below are placeholders to replace before finalization.

```markdown
# Batch progress

- Status: 待执行
- Plan revision:
- Current batch:
- Current authorization:
- Blocker/owner/next action:
- Evidence and within-batch recovery: 计划交接文档.md

- [ ] B1 数据库批次：DB-001…；状态：未开始；退出：本批结构/迁移准备及必要安全检查完成
- [ ] B2 API实现批次：API-001…；状态：未开始；退出：本批API、契约、权限和消费者接线完成
- [ ] B3 API集中验证批次：TEST-001…、INT-001…；状态：未开始；退出：集中验证与受影响复验通过
- [ ] B4 UI制作批次：UI-001…；状态：未开始；退出：本批页面及组件制作完成
- [ ] B5 UI自动核查批次：UIV-001…；状态：未开始；退出：自动核查与必要修复复验通过

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
