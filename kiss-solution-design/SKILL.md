---
name: kiss-solution-design
description: Apply KISS reasoning to new features, architecture, workflows, data models, APIs, configuration, and cross-platform plans. Use while planning or reviewing a solution whose scope or complexity is still negotiable; do not use to remove confirmed requirements, visual fidelity, security, data integrity, auditability, or recovery safeguards.
---

# KISS Solution Design

Find the simplest complete solution to the confirmed problem at the current stage. Simplicity means fewer concepts, states, facts, and maintenance paths—not transferring complexity to users or omitting a necessary business or operational loop.

## Required Questions

Before implementation or when reviewing a proposal, answer:

1. **Is it necessary?** Name the real user, situation, problem, evidence, and acceptance outcome.
2. **Must this system own it?** Check whether an existing module, upstream platform, shared primitive, or operational process already owns the responsibility.
3. **Is it necessary now?** Separate first-release requirements, confirmed near-term needs, and speculative future ideas.
4. **What is the simpler complete path?** Prefer reuse of existing data, state, permissions, components, and workflows over a new subsystem.
5. **Is it simple for the user?** Do not make operators coordinate hidden steps, enter technical values, or repair consistency manually to keep the implementation small.
6. **Is there one source of truth?** Make ownership, failure, recovery, and observability explicit. Eliminate duplicated configuration or synchronized copies where possible.
7. **Where can it extend later?** Preserve a clear seam for a likely next step without building the future system today.

## Complexity Budget

Challenge every new service, table, queue, state, permission, configuration flag, abstraction, plugin point, or synchronization path:

- Which confirmed behavior requires it now?
- Why can the existing model not express that behavior safely?
- What failure mode and maintenance obligation does it add?
- How will its necessity and correctness be tested?

Remove elements without concrete answers. Prefer a direct implementation with a stable boundary over a generic engine, speculative framework, many switches, or premature distribution.

## Completeness Guardrail

KISS does not justify removing:

- Confirmed user or visual requirements.
- Authorization, validation, privacy, security, or compliance controls.
- Data consistency, concurrency protection, idempotency, audit, backup, recovery, or failure feedback when the risk requires them.
- Real loading, empty, error, retry, and terminal states.
- A necessary business handoff or operational owner.

Additional complexity is justified when a concrete risk or confirmed near-term use requires it. Record the reason and its acceptance check.

## Decision Output

Use [references/review-template.md](references/review-template.md) for a formal plan or review. At minimum state:

- What this iteration will do.
- What it explicitly will not do.
- Why the proposed solution is sufficient and complete.
- Which existing capability it reuses.
- The single source of truth and responsibility boundaries.
- The future extension seam, if a likely one exists.
- Any retained complexity and the concrete reason for it.

If the core user, problem, ownership, or acceptance result cannot be established without major assumptions, pause design and request that missing product decision before coding.
