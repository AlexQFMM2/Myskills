---
name: git-release-discipline
description: Manage a solo project owner's agent-assisted Git development in one local workspace, with task branches, versioned handoffs and reviewed merges into the sole production branch, release. Use for feature/fix implementation or merge/deployment preparation in deployed Git projects; not for read-only investigation or non-Git projects.
---

# Git Release Discipline

Serve **one project → one human owner → that owner's agent team**. Keep production independently repairable while features are unfinished or awaiting business approval. The operating constraint is one local project directory and one development environment, with Git switching the files in place. Do not import a multi-human organization or one workspace/environment per agent into this workflow.

## Single-owner coordination

- The human owner sets scope, business holds and release authorization. One coordinating agent handles Git operations, integration, handoffs and release preparation within that authorization. Development and review are phases that agents can perform sequentially in the same directory, not additional human positions to fill.
- Keep one active task branch and reuse the project's development environment. Branches preserve alternative code histories without requiring duplicated checkouts or one running environment per branch.
- Do not automatically create worktrees, extra clones, per-agent environments or a second local database to accelerate work or escape a blocked switch. Queue work in the existing workspace. A multi-workspace arrangement requires an explicit change to the owner's constraints; it is not the routine fallback.
- Use existing task/handoff records for the active task, branch, checkpoint SHA, pending checks, paused work and next action. The coordinating agent maintains this continuity; the owner should not have to manually coordinate hidden agent state. Agent roles do not themselves authorize delegation or external actions, and existing authorization must not be requested repeatedly.

## External materials and versioned agent handoffs

For new tasks, keep the project container's `plan/` and task workbench `test/` beside its single source repository. Keep handoffs inside `<repository>/docs/handoffs/<task-id>/<agent-name>.md`, tracked on the owning task branch and included in checkpoint pushes. Each participating agent maintains its own stable task file; do not create a new file per turn or overwrite another agent's history. A small task README may link multiple agent files and the current handoff without duplicating their narratives or the external plan ledger.

Resolve the actual project container and repository roots before selecting paths; do not assume a standalone repository's parent belongs to only that project. With `plan-governance`, use its external plan/test layout and update the mutable task ledger plus the acting agent's docs handoff, leaving frozen specifications intact. Do not require a full implementation plan for a small repair. Existing tasks retain their known paths until migration is explicitly requested; installing this skill does not relocate or untrack their materials.

Record the task objective/scope and branch, base version, accepted constraints and plan revision, work completed, remaining work, checks actually run and their results, known failures, business hold if any, and the next concrete action. Include actual external plan/test locations and evidence references, plus enough recovery context to remain useful without those local files. A round ending is a recovery checkpoint, not a claim that the feature or its tests are complete. No full acceptance run is required merely to preserve unfinished work.

Check that the handoff is actually tracked and included in the commit; an ignored or local-only document is not remotely backed up. When tracking is requested, keep any ignore-rule adjustment limited to the intended safe documentation. Exclude secrets, private endpoints, customer data and bulky raw test artifacts; do not force-add an entire ignored plan/log directory.

The handoff follows its branch. A feature's document may disappear from the working directory while the repair branch is checked out; that is expected and does not justify merging feature code into the repair to retrieve it. Identify the saved branch and checkpoint in the agent's completion message; resume the feature by switching back and reading that branch's document. Each resumed agent must still verify current branch/HEAD instead of relying on its earlier conversation state.

External plan/test files do not switch with Git and are not backed up by a source push. Keep tasks and runs separate; match their task/plan/test revision and candidate commit to the checked-out branch before reuse. Never apply a suspended feature's instructions or passing test results to an unrelated fix. Standard regression/CI test code stays versioned with the source; the external test workbench owns task-specific materials/helpers and raw evidence. Do not make clean-clone CI depend on unavailable sibling files.

## Repository and branch ownership

Identify actual repository boundaries, repository instructions, release entrypoints and branch conventions. A workspace may contain independent repositories; do not initialize a parent repository to impose this workflow.

**The branch literally named `release` is the only production deployment source.** Keep it limited to reviewed, release-eligible work. All new functionality and repairs follow this route:

`task branch → review and corrections → merge into release → verify the resulting release version → deploy`

- Use one branch per independently deliverable task: `feat/<feature>`, `fix/<issue>` or `hotfix/<incident>`. Reuse a suitable existing task branch when continuing its task. These branches can be committed and pushed for backup, handoff and review, including WIP checkpoints; none can deploy to production.
- Urgency does not create an exception. `main`, `dev`, maintenance branches and arbitrary tags are not alternate production entrypoints. Task branches can run local tests and validation without becoming deployable branches.
- Record the deployed commit SHA and artifact version/digest from `release`. Tags may identify those verified release versions; a tag must not bypass the `release` merge/review path or become an independent route for publishing task-branch code.
- Inspect existing CI, push/tag triggers and manual release scripts. They must not deploy other branches, and a `release` deployment must wait for its resulting candidate to pass verification. If the existing setup violates this policy, report the mismatch and stop the affected deployment; align it within the already-authorized scope before proceeding. Do not claim that writing this skill configured enforcement.

Do not add permanent dev/test/maintenance branches for this workflow. If `release` is absent, establish its verified baseline and the required deployment-entrypoint change within the authorized task; do not silently substitute another branch, rename shared history or migrate unrelated repositories. The latest `release` tip is not evidence of the version currently running in production.

## Establish the base before editing

Inspect the current branch, worktree/index, untracked files, remotes, upstream and local commits. Fetch the relevant remote successfully before claiming synchronization; cached remote refs and commit dates are insufficient evidence.

Useful checks after fetching include:

```bash
git status --short --branch
git branch -vv
git rev-parse HEAD
git rev-list --left-right --count 'HEAD...@{upstream}'
```

The last command requires a real upstream: left means local-only commits, right means upstream-only commits. Distinguish synchronized, ahead, behind and diverged. Missing upstream or failed fetch is unknown state. Inspect the intended integration/release base as well: a feature branch usually tracks its own remote feature branch.

- Start ordinary new work from the freshly fetched, verified `release` base. An obsolete local `dev` branch need not be the starting point.
- Fast-forward a clean outdated branch when appropriate. Inspect divergence before integrating; do not blindly pull, reset or force-push away commits. Do not rewrite another contributor's published history.
- Start production repairs from the actual deployed commit or a verified compatible `release` tip. Do not inherit unreleased work merely because `release` HEAD is newer. The repair must still be reviewed and merged into `release` before deployment.
- If required remote/release facts are unavailable, continue independent inspection or explicitly provisional local work, but stop dependent integration/deployment and report the missing evidence.

“Do not fall behind” means verify the intended base and reconcile its relevant remote history before delivery. It does not require all local branches to match the newest integration tip. An intentional hotfix base or rollback may be older; record that choice and its release scope.

## One workspace: save, switch, verify, resume

Create or switch to the task branch **before implementation edits**. New features and all fixes must not be developed directly on `release` for convenience, even when small or urgent. Update `release` through the reviewed merge path.

Allow only one active implementation task to mutate the shared workspace at a time; default to one writer. If same-task parallel editing is explicitly authorized, assign disjoint files on the same branch and keep Git/index operations with the coordinating agent. This does not permit different branches in the same directory. Other agents may plan or review a fixed committed diff; pause implementation for review/test runs that read the working tree. Do not claim review of a stable revision while its files are changing.

Before every resumed edit, test or Git mutation after a handoff/switch, verify the actual branch, HEAD and pending changes against the task record. An agent's remembered branch can be stale because another phase changed the same directory. On mismatch, reconcile the task state before writing. Branch switches require all workspace-dependent agents/tools to stop and hand control back; do not switch underneath them.

When interrupted by a production issue:

1. Let the current agent reach a recoverable checkpoint, then stop all workspace-dependent writers/tools. Inspect pending changes, update the versioned handoff and preserve the current feature work plus handoff on its own branch with a coherent checkpoint commit. An explicitly incomplete/WIP commit is valid backup, not release acceptance. Exclude secrets, runtime data and unrelated changes; do not sweep everything into a commit.
2. Push the task checkpoint and handoff when authorized, especially before suspension or takeover. Verify that the remote task branch contains the saved commit. A local commit preserves branch work but is not a remote backup. Inspect any push-triggered deployment before pushing. Record pending backup honestly when push is unavailable or unauthorized.
3. Verify that switching will not carry uncommitted task changes into the other branch. Do not rely on Git allowing a switch as proof of isolation. Preserve any remaining work deliberately; do not discard changes or use stash as the normal long-term storage for an unfinished feature.
4. Switch this same development directory to the repair branch at the verified production-compatible base. Verify the resulting branch/HEAD, restart/reconfigure the existing development stack as required, implement and verify the repair, then use the review/release gates below.
5. After the repair has been reviewed, merged into `release`, verified and deployed, switch back to the feature branch and merge the updated `release` into it. Resolve conflicts and verify affected behavior, then resume from the recorded checkpoint. Do not merge the unfinished feature into `release` to synchronize it.

Use the development checkout for branch switching, never a directory actively serving production. Git changes tracked code, not databases, running processes, ignored files or dependency installations. Check lockfile/generated-output changes and schema compatibility on a switch; restart/reinstall only when needed. Remove or regenerate only identified disposable outputs that would contaminate the switched version; do not indiscriminately clean ignored files that may contain configuration/data. Do not blindly reverse database migrations. Prefer compatible schema evolution. If the shared development database cannot safely support the repair, report that specific test blocker and use an already available, authorized validation path where possible; do not silently duplicate the environment or claim unperformed tests passed.

## Feature completion, review and merge

Keep task scope, acceptance checks, merge target and release holds explicit. Commit coherent checkpoints during development rather than leaving days of work only in the working tree. Integrate relevant base changes at meaningful boundaries and before merge; use the repository's existing merge/rebase convention.

For a large feature, use increments that can be reviewed coherently and identify any dependencies. Unfinished or commercially unapproved functionality stays outside the release line. Passing tests does not lift a business hold. Do not assume disabling a UI/feature flag removes migrations, background jobs or startup effects; flag-based integration needs an agreed design and release scope.

Use the existing PR/MR process if the project has one. Otherwise review the committed diff and record the outcome locally in the existing task record; a hosted PR, merge queue and another human maintainer are not prerequisites for this personal workflow. The final merge target is `release`. Before merging into it:

1. Record actual base/head commits, intended behavior, affected checks and migration/rollback implications. Run required CI and tests proportional to the change, including business acceptance paths for new functionality.
2. Perform a distinct review phase on the actual diff and affected behavior, scope, permissions/data risks and failure cases. Use a separate reviewer agent when available and authorized; it can review read-only in the same workspace while implementation is paused. Otherwise perform and label a self-review, without inventing independent approval. Respect any stronger existing repository review requirement and record it as unmet if unavailable; do not invent a requirement for another human reviewer.
3. Resolve required findings on the task branch, commit/push the corrections through the authorized path, and recheck the affected behavior and resulting diff before merging. Confirm that held/unrelated features are absent. Technical review and business release eligibility are separate decisions.
4. The coordinating agent serializes merges in the same workspace. Verify the candidate against the current target, resolve conflicts on the task branch, and rerun affected checks after changes. Successful tests on an older base do not prove the new merge result.
5. Follow the repository's merge strategy; squash is a reasonable default for an independent task if no convention exists. Verify the resulting release commit/artifact before deployment, since merging may change its SHA or tree.

Respect existing repository protection and CI. Do not add organizational approval machinery just to complete this solo workflow. Check whether merging triggers automatic deployment before treating a merge as a purely internal operation.

## Hotfix release and reintegration

Keep urgent repairs narrowly scoped and reproduce/verify the defect. Use the normal review and release gates; urgency does not silently waive traceability or deployment authorization.

Merge the reviewed fix into `release`, verify the resulting version, push through the authorized path and deploy that version from `release`. Never deploy directly from `fix/*`, `hotfix/*`, a maintenance branch or a task-branch tag. If `release` contains changes excluded from this repair's deployment scope, restore an eligible `release` through reviewed corrective work before releasing; do not bypass it. Do not merge unrelated changes into the repair merely to remove a behind count.

After deployment, bring the updated `release` into relevant continuing feature work, resolve semantic conflicts and verify there. Record unresolved reintegration so a later feature release cannot silently restore the production bug.

If unfinished or held feature work already contaminated `release`, preserve it on a task branch before recovery. Creating another branch at the same tip does not remove commits from `release`. Compare against the last releasable version and prepare the required corrective changes on a task branch, then review and merge them into `release`; avoid destructive shared-history rewrites. Verify the final release tree and the required repair together before deployment.

## Mandatory deployment gate

For a Git-managed release, require:

- **Only release can deploy:** the deployment entrypoint selects a verified version of the remote `release` branch. Check the actual source SHA and release provenance, not merely a branch-name argument or local branch label. CI may use a detached checkout of that selected SHA, but a feature/fix branch or tag cannot invoke an alternate production path.
- **Committed source:** all release source changes are committed; the release checkout has no tracked/staged modifications or untracked source inputs. Preserve unrelated development work instead of discarding it to pass the check. Select and build the release commit in the same workspace, or use an existing authorized CI/release path. A second local checkout is not required to obtain clean committed source.
- **Remote record and current comparison:** the selected commit is pushed and freshly verified in the remote `release` history, with the relevant review/merge evidence. Reconcile its upstream for a normal tip-based release. An intentionally pinned release or rollback may use an older verified version previously selected from `release`, through the same release entrypoint; verify its authorized immutable version and artifact. Remote reachability through some other branch/tag is insufficient. A moving branch name alone is not a release record.
- **Correct release scope:** inspect the delta from current production for unfinished/held/unrelated functionality. Clean Git status and zero ahead/behind counts alone do not establish eligibility.
- **Verified candidate:** required checks/review cover the resulting release source and artifact. Deploy the verified artifact; do not silently pull a newer branch tip or rebuild different inputs after validation. If the remote moves, explicitly retain the authorized pinned candidate or prepare and verify a new one.
- **Explicit non-source inputs:** handle environment configuration, secrets, dependency inputs and generated assets through the established release process. Ignored local source/build inputs invalidate an unsupported clean-source claim. Never commit secrets or runtime data just to make status look clean.
- **Authorized release and recovery:** deployment authorization covers the actual merge/push/tag/service change and any automatic publishing it triggers. Preserve the rollback version and account for database compatibility; reverting code is not automatically a safe data rollback.

Complete safe authorized preparation when a gate fails, then stop the dependent deployment and state the concrete blocker. Do not deploy first and commit/push afterward. The gate does not grant missing external-action permission or require asking again for existing authorization. An authorized restoration of an existing verified artifact previously released from `release` needs no artificial new commit and still uses the release-controlled deployment path.

## Evidence and skill boundaries

In the existing task/release record, report the repository, branch, base/candidate SHA, fresh upstream comparison, checkpoint/remote status, review/check results, merge target, release eligibility and blockers. After deployment record the actual deployed SHA/artifact, verification and rollback reference. Distinguish implementation complete, merged and deployed.

Use `ai-code-review`, `plan-governance` and `docker-release-safety` when available and relevant for review evidence, existing plan records and container resource/artifact checks. This skill owns Git isolation, synchronization and release source traceability without duplicating their policies. Skill instructions guide agents; actual enforcement belongs in branch protection, CI and release entrypoints when those changes are authorized.
