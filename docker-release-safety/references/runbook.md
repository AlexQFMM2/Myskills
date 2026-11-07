# Release guard runbook

## Scope and exits

Run `python3 /path/to/docker-release-safety/scripts/release_guard.py --help` with Python 3.9+. No third-party Python packages are needed. JSON reports go to stdout; invalid command syntax uses argparse's stderr.

| Exit | Meaning | Next step |
| --- | --- | --- |
| 0 | Check passed, fingerprint computed, match found, or cleanup completed | Continue only the corresponding authorized operation |
| 1 | Insufficient disk space | Pause allocation/deployment; report shortfall and scoped recovery |
| 2 | Invalid input, inaccessible storage/Docker, or cleanup failure | Resolve the error; do not treat it as a cache miss |
| 3 | `find-image` found no matching local image | Build with normal cache after space checks |

The helper does not deploy, build, contact a registry, reserve disk, or scan every host automatically. Each check describes only the supplied locations and the selected Docker daemon. The agent/release entrypoint owns complete destination discovery, immutable input resolution, application acceptance and the protection set. Labels are provenance claims from trusted build workflows, not signatures.

## Space gate

Identify the daemon using the active Docker context/environment. For a local Linux daemon, `--docker` includes its actual `DockerRootDir`. Remote TCP/SSH daemons and Docker Desktop are rejected by this shortcut: execute checks on their host/VM instead. A forwarded Unix socket is not proof of locality; confirm the socket belongs to this host. Docker-in-Docker, Kubernetes and multi-node BuildKit require checks on the actual worker storage.

Inspect the selected builder with `docker buildx inspect` (without `--bootstrap`, which may allocate space). Include its real backing store, separate containerd image/snapshot storage if enabled, temporary directory, workspace, export destination and deployment-host import store. `DockerRootDir` alone does not cover independent containerd/BuildKit storage. In a VM also check the backing disk's host filesystem and the guest's available capacity. If a storage root is unreadable, run the read-only check with appropriate authorized access; do not substitute the current directory.

Example variables below are supplied by the project's release entrypoint; `GUARD` is the installed helper's absolute path. Peak values are estimates, not universal defaults:

```bash
# Check BEFORE copying a build context, pulling, building or saving an archive.
if python3 "$GUARD" space --docker \
    --path "$BUILD_CONTEXT" --path "$RELEASE_TMP" --peak-gib "$BUILD_PEAK_GIB"; then
    docker build --platform "$PLATFORM" -t "$CANDIDATE" "$BUILD_CONTEXT"
else
    guard_status=$?
    exit "$guard_status"
fi
```

This illustrates failure propagation; use the provenance labels below for a managed build. Paths must already exist (check their existing parent before creating a new destination). The gate requires **20 GiB + `--peak-gib`** free on each checked filesystem. Duplicate paths on one filesystem are reported together. Supply the combined peak for paths sharing a filesystem; the same conservative peak is used for every listed filesystem. For materially different estimates, use separate invocations with explicit success dependencies. A successful check on one host cannot authorize writing to another host.

Recheck on the target host before loading/pulling and before replacing the service. A reuse-only deployment may have a smaller peak but still needs room for container writable layers/logs. Do not stop the current service while the disk gate is unresolved. Recheck after cleanup, and report actual measured free-space change.

## Fingerprint, reuse and managed builds

Use a frozen build context with all actual build inputs. The helper hashes **every file, file/directory mode, and internal symlink target** in that directory, plus Dockerfile contents and declared build inputs. It intentionally does not reimplement Docker's `.dockerignore`. This may cause conservative misses, but must not omit dirty/untracked files. Avoid hashing a repository containing huge caches: first check staging capacity, then use the project's existing context-preparation procedure to create a small, complete snapshot. Do not put fingerprint/output reports inside the context, and do not stage secrets or deployment data into it.

Supply every external base and `COPY --from=<image>` input by resolved digest, every effective build argument, build target and canonical platform (such as `linux/amd64`). Pin the actual build to these same digests/arguments. For local-only source images without registry digests, either use existing verifiable build provenance or skip full-image reuse and use normal build cache. `scratch` is accepted for a scratch-only base. The script does not parse Dockerfiles, resolve tags, verify dependency lock completeness or discover external named contexts. Additional contexts, frontend/network options or secret-derived build outputs must be represented by the existing build system's provenance; otherwise do not claim equivalence with this helper. Mutable package downloads and a requested base/security refresh require a rebuild even when local inputs match.

```bash
python3 "$GUARD" fingerprint --project "$PROJECT" \
    --context "$BUILD_CONTEXT" --platform "$PLATFORM" \
    --base-image "$PINNED_BASE" --build-arg "BASE_IMAGE=$PINNED_BASE"

# FINGERPRINT is the fingerprint field from that successful JSON response.
if python3 "$GUARD" find-image --project "$PROJECT" \
    --fingerprint "$FINGERPRINT" --platform "$PLATFORM"; then
    : # Reuse a returned immutable image ID after checking its acceptance evidence.
else
    guard_status=$?
    if [ "$guard_status" -ne 3 ]; then
        exit "$guard_status"
    fi
    # Space check must succeed immediately before the build below.
    if python3 "$GUARD" space --docker --path "$RELEASE_TMP" \
        --peak-gib "$BUILD_PEAK_GIB"; then
        docker build --platform "$PLATFORM" \
            --build-arg "BASE_IMAGE=$PINNED_BASE" \
            --label "io.myskills.release.project=$PROJECT" \
            --label "io.myskills.release.fingerprint=$FINGERPRINT" \
            --label io.myskills.release.gc=eligible \
            -t "$CANDIDATE" "$BUILD_CONTEXT"
    else
        guard_status=$?
        exit "$guard_status"
    fi
fi
```

`BASE_IMAGE` here is an example Dockerfile argument; use the actual Dockerfile's names and pass exactly the same values when fingerprinting and building. Add `--dockerfile`/`--target` to fingerprinting when used, and corresponding `-f`/`--target` build options. For multiple base images repeat `--base-image`. Canonical platform names must match Docker inspect (e.g. `arm64`, not `aarch64`). Do not pass credentials via build arguments.

The `gc=eligible` label is an explicit retention opt-in; omit it for images outside managed retention. Every managed build must overwrite project/fingerprint labels rather than inherit another image's claims. `find-image` checks project/fingerprint labels and actual platform, and returns image IDs, not mutable tags. Preserve the frozen context until the build finishes and record the resulting image ID with its fingerprint/test evidence. Do not retag or rebuild it between verification and deployment. Compose's existing fixed image plus `up -d --no-build` can consume the accepted artifact.

## Image cleanup

Inventory the actual daemon's images and running **and stopped** containers. Assemble immutable protection IDs for current/candidate images, all retained rollback releases (including releases on other hosts), and Dockerfile/multi-stage/local build dependencies. Where a rollback artifact exists only remotely, record that fact and protect any local copy used for recovery. The helper requires at least one `--protect`; every supplied reference must resolve locally or the entire operation fails. The newest-image rule supplements this explicit list; it does not identify successful releases.

```bash
# Read-only preview; add one --protect per required image actually present here.
python3 "$GUARD" cleanup-images --project "$PROJECT" --repository "$IMAGE_REPOSITORY" \
    --protect "$CURRENT_IMAGE_ID" --protect "$ROLLBACK_IMAGE_ID" \
    --protect "$BUILD_SOURCE_IMAGE_ID"

# Run the same command with --apply only within authorized cleanup/retention scope.
```

Default candidates must be at least seven days old, carry matching `project` and `gc=eligible` labels, have exactly one tag in the specified repository, and be outside the latest three managed images, all container references and the explicit protection set. Tagged aliases/multiple tags, dangling images, missing labels and other repositories are retained for separate investigation. This deliberately leaves legacy/unclassified disk usage visible rather than guessing ownership. Do not adopt old images into automatic cleanup without checking provenance and dependencies.

The helper previews all candidates and, with `--apply`, reinspects the daemon identity, protections and inventory before each deletion. The original protection IDs stay protected even if a supplied tag moves; newly resolved protection IDs are checked too. It uses immutable IDs, `docker image rm --no-prune`, and never `--force`; implicit parent deletion is disabled. A failure stops further deletion and reports IDs already removed. Do not run concurrent builds/releases/cleanup on the same worker while applying retention: inspection cannot atomically lock other Docker clients. `--keep-latest` and `--older-than-days` can express an established project retention policy (positive integers); always retain explicitly required recovery artifacts regardless of these values.

## Cache and temporary files

Images and BuildKit cache are different stores. `docker system df` and `docker buildx du --builder "$BUILDER"` help identify the actual source of pressure; shared/reclaimable sizes are estimates, not guarantees.

For an **existing, verified project-dedicated builder** with no active builds and authorized cleanup, inspect `docker buildx prune --help`. On versions supporting these flags, an example bounded cleanup is:

```bash
docker buildx prune --builder "$BUILDER" --filter 'until=168h' --max-used-space 30gb
```

The seven-day age and 30 GB cache cap are a starting example, not the filesystem safety reserve. Use the project's measured working set; configure the builder's native GC to maintain its accepted cache budget between releases. Retention filters may leave usage above the budget, and GC cannot guarantee free space when other stores consume the disk. Do not add `--all` or `--force` by default. If these options are unsupported, use that builder's documented GC configuration; never fall back to global pruning. A shared default builder is **not** project-scoped by merely passing a project name; report its usage and arrange an explicit shared-cache policy before pruning it.

For exports/staging, prefer an already-supported verified stream or a single owned temporary archive. Record exact temporary paths and lifecycle in the release procedure. Check both ends before transfer; verify destination load/digest and needed diagnostics before removing the temporary copy. Clean failed-run leftovers owned by this release once active processes have stopped. Never remove the last rollback artifact, release evidence, backups, mounted data or an arbitrary directory based only on age. The helper intentionally does not implement recursive filesystem deletion or global cache pruning.

## Verification

From the skill directory:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v
```

Tests use temporary contexts and a fake Docker command boundary; they do not delete real images. They exercise insufficient space and failure propagation, fingerprint invalidation, platform/provenance matching, protected/stopped-container images, retention boundaries and revalidation before mutation. For live integration, use a disposable daemon and explicit test repository; do not validate deletion against a shared development/production daemon.
