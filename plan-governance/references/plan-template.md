# Plan Governance Template

Use only the sections that apply, but do not omit the fields needed to execute and verify the work.

## `plan/<feature>/README.md`

```markdown
# <Feature name>

## Metadata

- Owner:
- Status: 草稿
- Created:
- Last updated:
- Repositories:
- Plan location:

## Problem and outcome

- User or operator:
- Confirmed problem and evidence:
- Target outcome:
- Acceptance result:

## Scope

### In scope

### Explicitly out of scope

## Current system

- Relevant flow:
- Existing capabilities to reuse:
- Responsibility boundaries:
- Source of truth:

## Execution model

- Business-task summary:
- Execution workstream order: database → API → API integration → UI implementation → UI automated verification
- Operation cost assumptions: 快 / 中 / 慢 / 超慢
- API integration gate before broad UI work:
- UI automated verification gate: 默认执行；集中在 UI 制作完成后，不按每个业务任务重复执行
- Exceptions to the default order and reason:

## Decisions and constraints

- Chosen approach:
- Rejected alternatives and why:
- Compatibility, security, privacy, or data constraints:
- Dependencies:

## Schedule and ownership

| Milestone | Workstream | Owner | Cost | Target | Exit evidence |
|---|---|---|---|---|---|
| Database change plan | DB |  | 快 |  |  |
| API change plan | API |  | 快/中 |  |  |
| API integration | INT |  | 中/慢 |  |  |
| UI implementation | UI |  | 中/慢 |  |  |
| UI automated verification | UIV |  | 超慢 |  |  |

## Verification and release

- Tests:
- Observability:
- Rollout:
- Rollback:
- Recovery or cleanup:

## Risks and blockers

| Item | Impact | Owner | Next action |
|---|---|---|---|

## Change log

| Date | Change | Reason | Author |
|---|---|---|---|
```

## `plan/<feature>/tasks.md`

```markdown
# Task breakdown

## Execution notes

- Execution mode:
- Concurrency approval:
- Integration owner:

| Agent/lane | Tasks | Start condition | Handoff artifact | Integration owner |
|---|---|---|---|---|

## B0: prerequisites and blockers

### T-001 <Task>

- Owner:
- Repository/files:
- Goal:
- Inputs:
- Outputs:
- Execution workstream: DB / API / INT / UI / UIV
- Operation cost: 快 / 中 / 慢 / 超慢
- Depends on:
- Acceptance:
- Verification mode: lightweight check / workstream gate / final automated UI verification
- Parallel candidate: no
- Execution lane:
- Handoff:

## B1: unlocked work

### T-002 <Task>

- Owner:
- Repository/files:
- Goal:
- Inputs:
- Outputs:
- Execution workstream: DB / API / INT / UI / UIV
- Operation cost: 快 / 中 / 慢 / 超慢
- Depends on: T-001
- Acceptance:
- Verification mode: lightweight check / workstream gate / final automated UI verification
- Parallel candidate: yes/no
- Execution lane:
- Shared resources or conflicts:
- Handoff:
```

## `plan/<feature>/taskList.md`

```markdown
# Execution checklist

- [ ] T-001 <short task name>
- [ ] T-002 <short task name>
```

## `plan/catalog/README.md`

```markdown
# Plan catalog

## 草稿

| Plan | Owner | Updated | Path |
|---|---|---|---|

## 待执行

| Plan | Owner | Updated | Path |
|---|---|---|---|

## 进行中

| Plan | Owner | Updated | Path |
|---|---|---|---|

## 阻塞

| Plan | Owner | Blocker | Updated | Path |
|---|---|---|---|---|

## 已完成

| Plan | Owner | Completed | Path |
|---|---|---|---|

## 已归档

| Plan | Owner | Archived | Path |
|---|---|---|---|
```
