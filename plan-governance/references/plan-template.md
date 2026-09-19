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

## Change inventory

### DB changes

| Change ID | Source tasks | Repository/file | Symbol/target | Action | Output | Validation | Dependencies |
|---|---|---|---|---|---|---|---|

### API changes

| Change ID | Source tasks | Repository/file | Symbol/target | Action | Output | Validation | Dependencies |
|---|---|---|---|---|---|---|---|

### Integration changes

| Change ID | Source tasks | Repository/file | Symbol/target | Action | Output | Validation | Dependencies |
|---|---|---|---|---|---|---|---|

### UI changes

| Change ID | Source tasks | Repository/file | Symbol/target | Action | Output | Validation | Dependencies |
|---|---|---|---|---|---|---|---|

### Verification changes

| Change ID | Source tasks | Repository/file | Symbol/target | Action | Output | Validation | Dependencies |
|---|---|---|---|---|---|---|---|

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

## T-001 <business task>

- [ ] DB-001 修改 `repository-relative/path` 的 `table/schema`：完成具体数据库变更
- [ ] API-001 修改 `repository-relative/path` 的 `function/route/contract`：完成具体 API 变更
- [ ] TEST-001 执行具体命令或测试：记录证据路径

## T-002 <business task>

- [ ] UI-001 修改 `repository-relative/path` 的 `route/component`：完成具体页面变更
- [ ] UIV-001 执行 UI 自动核查：记录通过项、失败项和修复结果
```

`taskList.md` 初始创建时可以只有业务任务分组和待补充项；开始执行前，必须将待执行项细化为变更 ID、精确文件路径、目标符号和具体动作。

## `plan/<feature>/计划交接文档.md`

创建计划时生成一个空的 UTF-8 文件，不填充默认模板内容。只有发生跨会话、跨 Agent 或跨负责人交接时，才在此文件记录交接上下文、已完成项、变更文件、证据、未解决问题和下一步启动条件。

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
