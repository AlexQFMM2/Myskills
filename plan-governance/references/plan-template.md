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

## Decisions and constraints

- Chosen approach:
- Rejected alternatives and why:
- Compatibility, security, privacy, or data constraints:
- Dependencies:

## Schedule and ownership

| Milestone | Owner | Target | Exit evidence |
|---|---|---|---|

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
- Depends on:
- Acceptance:
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
- Depends on: T-001
- Acceptance:
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
