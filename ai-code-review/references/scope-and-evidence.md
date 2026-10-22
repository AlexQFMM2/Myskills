# Review Scope and Evidence

Read the sections relevant to the requested comparison or verification problem.

## Select the Comparison

| Requested review | Evidence boundary |
| --- | --- |
| PR / feature branch | Actual target and head, ordinarily merge-base → head for the branch's changes; inspect integration with a newer target separately when relevant. |
| Exact commit | Parent → commit; for a merge commit establish which parent or merge result is intended. A root commit has no parent. |
| Explicit revision range | Preserve the user's endpoint or three-dot semantics; do not silently substitute another base. |
| Staged changes | Index relative to HEAD; unstaged content is a separate state and must not be used as if committed. |
| Working changes | Inspect staged, unstaged, and relevant untracked files; distinguish the staged snapshot from the combined working result. |
| Existing module audit | Named module and the dependency paths needed to assess it; distinguish current defects from optional redesign. |
| Pasted patch / partial checkout | Review the available material and state context limits. Do not claim a guard or dependency is absent merely because it was not provided. |

For a branch review, resolve the target and head from the task or PR metadata, then use their exact revisions. Example commands below assume `review_target` and `review_head` have already been assigned verified revisions; they are not guessed branch names:

```bash
review_base=$(git merge-base "$review_target" "$review_head")
git diff --no-ext-diff --no-textconv --stat "$review_base" "$review_head" --
git diff --no-ext-diff --no-textconv --name-status "$review_base" "$review_head" --
git diff --no-ext-diff --no-textconv "$review_base" "$review_head" --
```

Check that revision resolution and merge-base succeeded before using the result. When history is shallow, a base is missing, or there are multiple merge bases, establish the intended comparison rather than quietly falling back to HEAD or another branch. Use a suitable read-only comparison when the workspace is not a Git repository.

For local work, inventory first and inspect the requested state:

```bash
git status --short
git diff --no-ext-diff --no-textconv --cached --
git diff --no-ext-diff --no-textconv --
git ls-files --others --exclude-standard -z
```

For a repository with HEAD, `git diff --no-ext-diff --no-textconv HEAD --` shows the combined tracked working result. It does not include untracked files and can hide staged changes that unstaged edits undo. Read relevant untracked text files separately; handle NUL-delimited paths without splitting on whitespace. In an unborn repository, inspect the index and working files without assuming HEAD exists.

Read source at the reviewed revision or index when the checkout differs. Examples: `git show "${review_head}:path/to/file"` for a revision and `git show :path/to/file` for the index. Use those contents for line locations and evidence. Working-tree tests do not validate a different index or commit: use a permitted isolated copy/worktree, or limit conclusions to static inspection of the requested state.

Preserve user edits and unresolved conflicts. A review does not require checkout, reset, stash, cleanup, or applying a fix to the target tree. If files change during review, reassess affected evidence rather than reporting old line numbers as current.

## Build Context Without Expanding the Assignment

- Follow the changed operation to its callers and side effects. An unchanged helper can become unsafe for newly accepted inputs; establish the changed caller or input contract causing the regression.
- Check accepted requirements and existing tests, then challenge whether the tests actually encode the intended behavior. Neither old behavior nor a new test automatically defines the correct contract.
- Inspect middleware, database constraints, serializers, upstream validation, and UI state ownership before claiming a local check is missing.
- Treat search matches as navigation. A guard matters only if it runs on the affected path with the needed data and identity.
- Use manifests, lockfiles, configuration, and authoritative version-specific documentation to resolve uncertain library behavior. Do not impose the latest framework idiom on an older supported project.
- Follow caller or schema changes beyond the diff when necessary, but keep unrelated historical defects separate. Do not silently broaden a PR review into a whole-system audit.

## Prove or Reject a Candidate

Use the least expensive method that settles the material uncertainty:

| Method | What establishes the finding | Common false proof |
| --- | --- | --- |
| Static control/data-flow trace | Reachable inputs, all relevant guards, violated contract, and concrete result are accounted for. | A missing check in one function despite enforcement in its caller. |
| Focused reproduction | Real affected path fails the agreed behavior in a controlled environment. | A copied implementation, unrealistic fixture, or setup error fails. |
| Baseline comparison | The same scenario under comparable conditions distinguishes baseline from reviewed behavior. | Comparing different dependency versions or mislabeling an old defect as new. |
| Concurrency reproduction or schedule | A feasible ordering bypasses the actual transaction, lock, or uniqueness protections. | Assuming races merely because two async functions exist. |
| Performance observation/model | Relevant input sizes, operation count or measurements, and consequential resource impact. | Calling a nested loop a bottleneck without knowing collection bounds. |

Baseline execution is helpful when attribution is uncertain; it is not mandatory if the changed path proves causality. An existing defect newly exposed or made worse by the change can still be a regression: explain exactly what changed.

For a reproduction:

1. Identify the expected behavior and its source before writing the assertion.
2. Exercise the actual changed path, including relevant authorization, transactions, serialization, and error handling. A helper-only test does not prove endpoint behavior if middleware changes the outcome.
3. Keep data and side effects isolated. Use existing local fixtures or a temporary harness; avoid adding permanent tests to a review-only assignment.
4. Inspect the actual failure. Connection failures, missing packages, import errors, or bad mocks are verification limits until linked to the change.
5. Record the command, relevant state, observed result, and what it proves. Include enough information for another developer to repeat it without copying secrets or large logs.

If a test cannot run, a complete static argument can still confirm a finding. If a critical fact remains unknown, report the specific question and consequence instead of presenting it as confirmed or discarding the concern.

## Stop When the Evidence Is Sufficient

Resolve each material candidate as confirmed, disproved, optional, or unresolved. Once requested coverage and appropriate checks are complete, deliver the review. Broaden testing only for changed evidence, a new failure, or a remaining material uncertainty. State incomplete coverage and recurring environment blockers; do not enter an unbounded repair-and-retest loop during a review.
