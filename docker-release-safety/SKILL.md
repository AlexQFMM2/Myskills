---
name: docker-release-safety
description: Guard disk space before Docker builds, pulls, image exports and deployments; reuse verified images and retire scoped build artifacts. Use for container build/release work or Docker disk-pressure cleanup, not unrelated application changes.
---

# Docker Release Safety

Prevent repeated agent builds and retained artifacts from exhausting development or deployment disks. Use the existing Docker/Compose release path. This skill owns resource checks and retention, not deployment authorization or application acceptance.

## Before allocating space

1. Identify the actual Docker daemon, BuildKit worker(s), build context, temporary/export directories and destination host. Inspect disk usage (`docker system df`, builder-specific `docker buildx du`, and filesystem free space) before attributing pressure to images. Logical image sizes share layers and are not additive reclaim estimates.
2. Identify the candidate, current release, retained rollback versions and build-source images. Record immutable IDs/digests; a stopped container still references its image. Multi-stage `COPY --from` sources and images used by other projects remain dependencies even without containers.
3. Check for a reusable candidate using the input fingerprint procedure in [the runbook](references/runbook.md). Same tag or Git commit alone is insufficient: include dirty/untracked build inputs, Dockerfile, dependency locks, build arguments/target, resolved base digests and platform. Missing provenance means rebuild with normal cache. Do not default to `--no-cache`.
4. Run `scripts/release_guard.py space` on **every filesystem that will receive data**, before building, pulling, staging a context, exporting, transferring or loading. Run it on each actual host/worker; a local `df` cannot validate a remote daemon or VM disk. Recheck before service replacement and after cleanup.

The default safety reserve is **20 GiB (20 × 1024³ bytes)**. Required free space is the reserve **plus the estimated peak additional allocation**, including overlapping old/new images, unpacking, cache and export files. `--peak-gib` is mandatory; estimate from similar builds/actual artifacts, and explain uncertainty. Zero is appropriate only for an operation known not to allocate materially. Shared-filesystem estimates must cover the combined peak. Unknown paths, daemon errors or unsupported storage layouts are failed checks, not permission to proceed.

If a check fails, stop dependent build/release commands and report host, affected filesystem/path, free and required space, and scoped cleanup options. Do not override the result with `|| true`, silently lower the reserve, or retry allocations. An already-authorized cleanup can proceed within its scope; resume only after a fresh successful check. For large or poorly bounded builds, use a bounded worker/cache and monitor space during execution; a preflight is not a disk reservation. Serialize competing builds/cleanup on a shared worker or account for their combined allocation.

## Reuse and deployment

Build from a stable context and add the script-generated project/fingerprint labels. Pin base inputs by digest and record other artifact-affecting inputs. Mutable network downloads or unresolved build inputs invalidate an equivalence claim. Fingerprinting is conservative and does not implement `.dockerignore`; see the runbook before using it on a large repository.

`find-image` returns immutable matching image IDs. Verify candidate acceptance evidence against that ID; reuse never waives required tests. Deploy that verified artifact (for Compose, use the existing fixed release image and `--no-build`) instead of rebuilding between testing and deployment. For multi-platform images, remote caches or external named contexts not covered by the helper, use the existing build system's provenance and apply the same gates; do not pretend the single-platform helper proved equivalence.

## Retention and cleanup

- Default to preview. Execute cleanup when already authorized by the task or established retention policy; do not repeatedly ask for authorization already given. Implementing this skill does not itself authorize cleaning a user's machine.
- `cleanup-images` acts only on explicitly opted-in images with the exact project label and repository. It retains the newest three managed images by default, all container references, and every explicitly protected candidate/rollback/build-source image. Age defaults to seven days. Release records, not age alone, determine rollback protection.
- Supply the complete protection set. Docker cannot infer arbitrary Dockerfile dependencies or releases on other hosts. Resolve protection references successfully before deleting anything; unclassified or unlabelled historical images require inspection, not retroactive bulk opt-in.
- Never use broad `docker system prune -a --volumes`, force image removal, volume pruning, or delete Docker/BuildKit storage directories. Persistent data, backups and unrelated projects are outside build-artifact cleanup.
- Build cache needs its own bound. Use worker-native GC/retention on an established dedicated builder; on shared builders preserve other workloads and do not automatically prune. Read the runbook for the scoped cache procedure. Preserve useful recent cache to avoid costly rebuilds.
- Keep staging/export files in an owned, per-release temporary directory. Remove the exact temporary files after transfer/load verification, and failed-run leftovers after recording diagnostics. Retain release manifests, test/deployment evidence and required rollback artifacts. Do not recursively clean arbitrary `/tmp`, workspace or release roots.

After success or failure, finish safe temporary-resource cleanup and report the retained image IDs, cleanup performed, actual free-space change and any remaining block. Never promise reclaimed bytes by summing image sizes.

## Helpers and integration

Read [references/runbook.md](references/runbook.md) for commands, labels, exit codes, cleanup scope and limitations. The helper uses Python 3's standard library and Docker CLI; checks are read-only, and image deletion requires `--apply`.

Wire the check into the actual build/deploy entrypoint using an explicit successful-exit dependency. Skill instructions alone cannot intercept arbitrary shell commands. For a remote host, run/copy the helper there or use an equivalent verified host-side gate. `plan-governance`, when available, references this skill for release gates instead of maintaining another threshold or retention policy.
