# Project workspace, plans, tests and handoffs

Use this layout for new tasks and explicitly authorized migrations. It keeps a single source checkout while plans and test materials remain available across Git branch switches.

```text
<project-root>/
├── <repository>/                    # The only source checkout; contains .git
│   ├── docs/handoffs/<task-id>/
│   │   ├── <agent-name>.md          # Each participating agent owns its file
│   │   └── README.md                # Small handoff index when several agents participate
│   └── ...                         # Application and versioned regression/CI test code
├── plan/
│   ├── catalog/README.md
│   └── <task-id>/
│       ├── README.md               # Frozen overview
│       ├── tasks.md                # Frozen implementation specification
│       └── taskList.md             # Mutable execution ledger
└── test/<task-id>/
    ├── ...                         # Task test plans, fixtures, local helpers
    └── runs/<run-id>/              # Reports, logs, screenshots and other raw evidence
```

`<repository>` means the actual directory name, not a mandatory folder named `git`. Do not rename or move repositories to make the example literal. Do not create the optional index, test directories or agent files until there is an actual need.

## Resolve roots before writing

- Identify the real Git root with Git and the owning project container from workspace guidance and actual structure. If the project already has a container such as `<project-name>/<repository>`, its `plan/` and `test/` are siblings of that repository.
- Do not blindly use the repository's parent: some repositories live directly in a multi-project workspace. If no owning project container is established, resolve the intended external location before creating a shared `plan/` or `test/`; do not move the repository or initialize a parent Git repository automatically.
- Record project root, repository root, task ID, task branch, base SHA and plan revision in the task's records. Name the root when specifying a path: repository-relative for source/docs, project-relative for external plan/test files. Generate actual relative links from their containing documents; do not rely on a fixed number of `../` components.
- Multiple repositories may share an explicitly designated project plan/test area; identify each repository, affected branch and integration responsibility. This is not permission to create extra checkouts.

## Ownership and branch behavior

- `plan/<task-id>/` owns the approved design and live batch ledger. Existing freeze/replanning rules still apply even though the files are outside Git.
- `test/<task-id>/` owns task-level test specifications, local verification helpers and raw evidence. It is not an independent source checkout or environment.
- `<repository>/docs/handoffs/<task-id>/<agent-name>.md` owns that agent's narrative execution history and recovery facts. Use stable names agreed for the task, not a new file per turn. Do not overwrite another agent's history; an explicitly transferred role may continue its existing file with attribution.
- For multiple agents, the task's `docs/handoffs/.../README.md` only links agent files and identifies the current handoff/next action. It must not duplicate the full external task ledger or maintain competing status histories. For one agent, its file is sufficient.
- Put a concise, self-contained recovery summary in tracked handoffs: task objective/scope, branch/base, accepted constraints and plan revision, changed code, actual checks/results and coverage limits, blockers, and next action. Include external plan/test locations and evidence references, but not only a link that becomes useless on another machine. Record enough to identify missing material honestly; do not invent an absent approved specification.
- Handoffs are committed and pushed with their owning task branch when authorized. `docs/` existing on disk does not prove its new files are tracked; check Git and staged content. Keep secrets, private endpoints, customer data and bulky evidence out of committed handoffs.
- External plan/test files do not switch with Git and are not backed up by a source push. Keep tasks separate, associate their content with branches and explicit plan/test revisions, and do not overwrite a suspended feature's material while repairing production. Report actual backup status; do not automatically add another Git repository or upload these materials elsewhere.
- Before resuming or testing after a branch switch, match the active branch/commit and task against the handoff and external plan/test version. External progress/checkmarks are not proof that the checked-out code contains the completed work.

## Test placement and reproducibility

The external `test/` is the task workbench, including business acceptance matrices, exploratory/browser scripts, local fixtures and raw reports/screenshots. Source-owned unit, integration and regression tests required by the repository's standard commands or CI remain versioned with the implementation, wherever the repository already locates them. Do not move all files named `test` or `tests` outside Git or remove CI coverage to satisfy a folder convention.

For each external test run, record task/plan revision, repository and branch, tested commit (and any dirty-state delta), the tested service/artifact when different from the local checkout, script/test-spec revision or hash, command/working directory, relevant nonsecret setup, outcomes and coverage gaps. Separate runs by run ID; do not overwrite old evidence or carry a passing result across a changed candidate without checking validity.

External helpers must select the actual repository explicitly through a documented argument/configuration or verified root mapping. Check relative imports, dependency resolution, executable paths, fixtures and report destinations. Do not guess a repository by assuming a fixed number of parent directories. Reuse the project's existing test/runtime tools rather than create a second checkout/environment just to run an external script. Repository CI must not silently depend on an unversioned sibling directory that a fresh clone does not contain.

An external helper that becomes a required, repeatable regression/CI gate needs its reproducible test code and safe fixtures versioned with the source, or another explicitly established versioned delivery mechanism. Its large run artifacts can remain external. Merely moving a script into a sibling directory does not establish its portability or backup.

## Existing projects and later migration

Updating this skill changes the convention for new work; it does not authorize bulk relocation, untracking files, rewriting frozen plans or reorganizing every existing repository. Existing tasks retain their known authoritative paths until their migration is explicitly requested; do not fork a second live copy of their plan/handoff just to match the new layout.

For an authorized migration, first inventory tracked/ignored/untracked files, pending edits, live consumers, script path assumptions, docs links and CI/package commands. Being listed in `.gitignore` does not make an already tracked file untracked. Preserve a recoverable copy and the task's current state before moving. Transfer narrative handoffs into the chosen docs ownership structure without discarding history; preserve original attribution and evidence, and leave no competing active handoff. Update callers/navigation and validate affected entrypoints before claiming migration complete. Do not force-add entire ignored directories, silently remove tracked tests, or treat a folder move as acceptance of the underlying feature.
