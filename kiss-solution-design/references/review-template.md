# KISS Review Template

Use only the sections needed for the decision; keep each answer concrete.

## Problem

- Target user and situation:
- Confirmed problem and evidence:
- Acceptance outcome:

## Scope Now

- Must deliver:
- Explicitly not delivering:
- Confirmed near-term need:
- Speculative future idea:

## Simplest Complete Solution

- User flow:
- Existing capabilities reused:
- New concepts introduced:
- Source of truth:
- Responsibility boundaries:
- Failure and recovery path:

## Complexity Review

| Added element | Confirmed need | Why reuse is insufficient | Added failure/maintenance cost | Acceptance check |
| --- | --- | --- | --- | --- |

Delete unjustified rows from the design, not merely from the table.

## Necessary Safeguards

Record any required authorization, validation, privacy, consistency, concurrency, audit, observability, or recovery behavior. These are part of the complete solution rather than optional polish.

## Extension Seam

Name only likely extensions and the stable boundary that lets them be added later. Do not implement unused states, flags, engines, or providers solely to demonstrate extensibility.

## Decision

- Why this is sufficient now:
- Why it is simpler than the alternatives:
- Retained complexity and reason:
- Open product decisions that block implementation:
