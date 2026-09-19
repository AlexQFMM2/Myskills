# Myskills

Personal, reusable Codex skills for product and interface development.

## Skills

- `maintainable-ui-engineering`: component ownership, style boundaries, design tokens, and CSS variable contracts.
- `reference-ui-reconstruction`: evidence-based screenshot and design reconstruction.
- `admin-ui-usability`: task-centered, safe, and understandable admin interfaces.
- `kiss-solution-design`: simplest complete solution design without dropping necessary safeguards.
- `plan-governance`: construction-ready implementation blueprints that turn complete business requirements into coordinated database, API, verification, and UI batches—reducing uncertainty, repeated design, rework, and unclear progress.

### Plan Governance: the general contractor

Clarify the requirements and inspect the existing system before construction begins. Integrate applicable specialist skills into a detailed implementation blueprint, then organize execution by work type rather than repeatedly building and testing each feature in isolation.

- **`README.md` — project overview:** goals, scope, architecture, key decisions, and acceptance principles.
- **`tasks.md` — construction blueprint:** Part I defines complete business requirements; Part II designs the database, API, API verification, UI, and automated UI verification batches across those requirements. Specify actual files, interfaces, processing steps, and role-based test scenarios with explicit assertions—not just objectives or file lists.
- **`taskList.md` — manager-facing progress:** one progress unit per production batch, showing its deliverable, status, remaining work, blockers, and evidence references.
- **`计划交接文档.md` — agent continuity:** initially empty; records execution evidence, issues, and recovery points between turns, sessions, or agents.

Resolve consequential design questions during planning. A full implementation plan is not ready if interfaces, data rules, routes, or test expectations are deferred to a future design batch. Once finalized, `README.md` and `tasks.md` stay frozen unless the user explicitly requests replanning; execution updates the progress ledger and handoff instead.

Database and API work is coordinated before broad UI implementation, with dependency-aware verification at batch gates and UI automation enabled by default. Applicable specialist skills supply solution simplicity, component/style boundaries, visual fidelity, and usable admin interactions. Planning does not itself authorize implementation, parallel agents, database changes, deployment, commits, or pushes.

## Installation

Each top-level skill directory is independently installable. To install from GitHub, ask Codex to use `skill-installer` with repository `AlexQFMM2/Myskills` and the desired directory paths. Installed skills become available on the next turn.

The repository copy is the source of truth. Keep credentials, private endpoints, customer data, and project-specific environment values out of every skill.
