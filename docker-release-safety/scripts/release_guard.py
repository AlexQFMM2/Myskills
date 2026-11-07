#!/usr/bin/env python3
"""Conservative disk, provenance and image-retention helpers. Python 3.9+."""

import argparse
from datetime import datetime, timedelta, timezone
from decimal import Decimal, InvalidOperation, ROUND_CEILING
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import socket
import stat
import subprocess
import sys

GIB = 1024 ** 3
RESERVE_BYTES = 20 * GIB
LABEL = "io.myskills.release."


class GuardError(Exception):
    pass


def docker(*args):
    # Raw daemon errors may contain credentials; never echo them.
    try:
        result = subprocess.run(["docker", *args], capture_output=True, text=True,
                                timeout=60, check=False)
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise GuardError("Docker command unavailable or timed out; no passing check.") from exc
    if result.returncode:
        raise GuardError("Docker command failed; check daemon access and the supplied references.")
    return result.stdout.strip()


def docker_json(*args):
    try:
        return json.loads(docker(*args))
    except (ValueError, TypeError) as exc:
        raise GuardError("Invalid Docker response; no passing check.") from exc


def project_name(value):
    if not re.fullmatch(r"[a-z0-9][a-z0-9_.-]{0,127}", value):
        raise argparse.ArgumentTypeError("Use a lowercase project identifier (letters, digits, ._-).")
    return value


def digest(value):
    if not re.fullmatch(r"[a-f0-9]{64}", value):
        raise argparse.ArgumentTypeError("Expected a lowercase SHA-256 fingerprint.")
    return value


def gib_bytes(value):
    try:
        amount = Decimal(value)
        if not amount.is_finite() or amount < 0:
            raise InvalidOperation
        return int((amount * GIB).to_integral_value(rounding=ROUND_CEILING))
    except (InvalidOperation, ValueError, OverflowError) as exc:
        raise argparse.ArgumentTypeError("GiB must be a finite, nonnegative number.") from exc


def positive_integer(value):
    number = int(value)
    if number < 1:
        raise argparse.ArgumentTypeError("Must be at least 1.")
    return number


def local_docker_root():
    # DOCKER_CONTEXT overrides DOCKER_HOST, as it does in Docker CLI.
    context = os.environ.get("DOCKER_CONTEXT")
    if context or not os.environ.get("DOCKER_HOST"):
        args = ["context", "inspect"] + ([context] if context else [])
        host = docker_json(*args, "--format", "{{json .Endpoints.docker.Host}}")
    else:
        host = os.environ["DOCKER_HOST"]
    if not isinstance(host, str) or not host.startswith("unix://"):
        raise GuardError("Docker is remote or its locality is unknown; run space checks on its host.")
    info = docker_json("info", "--format", "{{json .}}")
    if "docker desktop" in info.get("OperatingSystem", "").lower():
        raise GuardError("Docker Desktop uses a VM disk; check inside the VM/worker as well as its host.")
    root = info.get("DockerRootDir")
    if not root or not Path(root).is_absolute():
        raise GuardError("Docker data directory could not be determined.")
    return root


def space_report(paths, peak_bytes):
    filesystems = {}
    for raw in paths:
        path = Path(raw).resolve(strict=True)
        device = path.stat().st_dev
        if device not in filesystems:
            free = shutil.disk_usage(path).free
            required = RESERVE_BYTES + peak_bytes
            filesystems[device] = {
                "device": device, "paths": [], "free_bytes": free,
                "required_bytes": required, "shortfall_bytes": max(0, required - free),
                "free_gib": round(free / GIB, 3), "required_gib": round(required / GIB, 3),
                "passed": free >= required,
            }
        filesystems[device]["paths"].append(str(path))
    return {"host": socket.gethostname(), "reserve_bytes": RESERVE_BYTES,
            "peak_bytes": peak_bytes, "filesystems": list(filesystems.values()),
            "passed": all(item["passed"] for item in filesystems.values())}


def check_space(args):
    paths = list(args.path)
    if args.docker:
        paths.append(local_docker_root())
    if not paths:
        raise GuardError("Supply --path and/or --docker for actual allocation destinations.")
    report = space_report(paths, args.peak_gib)
    return (0 if report["passed"] else 1), report


def add_record(hasher, record):
    encoded = json.dumps(record, sort_keys=True, separators=(",", ":")).encode()
    hasher.update(len(encoded).to_bytes(8, "big"))
    hasher.update(encoded)


def file_hash(path):
    before = path.stat()
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    after = path.stat()
    fields = ("st_dev", "st_ino", "st_size", "st_mtime_ns", "st_ctime_ns")
    if any(getattr(before, field) != getattr(after, field) for field in fields):
        raise GuardError("A build input changed during hashing; freeze the context and retry.")
    return h.hexdigest()


def context_hash(root):
    root = Path(root).resolve(strict=True)
    if not root.is_dir():
        raise GuardError("Build context must be a directory.")
    h = hashlib.sha256()

    def visit(directory):
        for path in sorted(directory.iterdir(), key=lambda entry: entry.name):
            info = path.lstat()
            record = [str(path.relative_to(root)), stat.S_IMODE(info.st_mode)]
            if stat.S_ISLNK(info.st_mode):
                target = path.resolve(strict=True)
                if root != target and root not in target.parents:
                    raise GuardError("External context symlink; stage its input explicitly before hashing.")
                record += ["symlink", os.readlink(path)]
            elif stat.S_ISREG(info.st_mode):
                record += ["file", file_hash(path)]
            elif stat.S_ISDIR(info.st_mode):
                record += ["directory"]
            else:
                raise GuardError("Unsupported special file in build context.")
            add_record(h, record)
            if stat.S_ISDIR(info.st_mode):
                visit(path)

    visit(root)
    return h.hexdigest()


def fingerprint(args):
    values = {}
    for item in args.build_arg:
        key, separator, value = item.partition("=")
        if not separator or not key or key in values:
            raise GuardError("Build arguments need unique explicit KEY=VALUE pairs.")
        values[key] = value
    for base in args.base_image:
        if base != "scratch" and not re.fullmatch(r"[^\s@]+@sha256:[a-f0-9]{64}", base):
            raise GuardError("Every base input must be scratch or an image reference pinned by SHA-256 digest.")
    dockerfile = Path(args.dockerfile) if args.dockerfile else Path(args.context) / "Dockerfile"
    inputs = {"version": 1, "context": context_hash(args.context),
              "dockerfile": file_hash(dockerfile), "platform": args.platform,
              "target": args.target, "base_images": sorted(set(args.base_image)),
              "build_args": values}
    h = hashlib.sha256()
    add_record(h, inputs)
    value = h.hexdigest()
    return 0, {"fingerprint": value,
               "labels": {LABEL + "project": args.project, LABEL + "fingerprint": value}}


def image_ids(project):
    output = docker("image", "ls", "--all", "--quiet", "--no-trunc", "--filter",
                    "label=" + LABEL + "project=" + project)
    return sorted(set(output.split()))


def inspect_image(reference):
    items = docker_json("image", "inspect", reference)
    if not isinstance(items, list) or len(items) != 1:
        raise GuardError("Expected one inspectable image for each reference.")
    return items[0]


def image_labels(item):
    return (item.get("Config") or {}).get("Labels") or {}


def image_platform(item):
    result = item["Os"] + "/" + item["Architecture"]
    return result + ("/" + item["Variant"] if item.get("Variant") else "")


def find_image(args):
    matches = []
    for identifier in image_ids(args.project):
        item = inspect_image(identifier)
        labels = image_labels(item)
        if (labels.get(LABEL + "project") == args.project
                and labels.get(LABEL + "fingerprint") == args.fingerprint
                and image_platform(item) == args.platform):
            matches.append(item["Id"])
    return (0 if matches else 3), {"reusable": bool(matches), "image_ids": matches}


def container_images():
    result = set()
    # Include stopped containers. Any inspect/list failure fails the whole check.
    for identifier in docker("container", "ls", "--all", "--quiet", "--no-trunc").split():
        items = docker_json("container", "inspect", identifier)
        result.add(items[0]["Image"])
    return result


def created_at(item):
    # Docker emits nanoseconds; Python 3.9/3.10 accept only millisecond/microsecond fractions.
    stamp = re.sub(r"\.(\d+)(?=Z|[+-]\d\d:\d\d$)",
                   lambda match: "." + match[1][:6].ljust(6, "0"), item["Created"])
    value = datetime.fromisoformat(stamp.replace("Z", "+00:00"))
    if value.tzinfo is None:
        raise GuardError("Image creation timestamp lacks timezone.")
    return value


def cleanup_snapshot(args):
    protected = {inspect_image(ref)["Id"] for ref in args.protect}
    used = container_images()
    images = [inspect_image(identifier) for identifier in image_ids(args.project)]
    managed = [item for item in images
               if image_labels(item).get(LABEL + "project") == args.project
               and image_labels(item).get(LABEL + "gc") == "eligible"
               and len(item.get("RepoTags") or []) == 1
               and item["RepoTags"][0].rsplit(":", 1)[0] == args.repository]
    recent = {item["Id"] for item in sorted(managed, key=created_at, reverse=True)[:args.keep_latest]}
    cutoff = datetime.now(timezone.utc) - timedelta(days=args.older_than_days)
    candidates, retained = [], []
    for item in images:
        identifier = item["Id"]
        reason = None
        if item not in managed:
            reason = "not opted in, different repository, or not exactly one tag"
        elif identifier in protected:
            reason = "explicitly protected release or build dependency"
        elif identifier in used:
            reason = "referenced by a running or stopped container"
        elif identifier in recent:
            reason = "retained recent version"
        elif created_at(item) >= cutoff:
            reason = "within retention age"
        if reason:
            retained.append({"id": identifier, "reason": reason})
        else:
            candidates.append(identifier)
    return {"candidates": candidates, "retained": retained, "protected_ids": sorted(protected)}


def cleanup_images(args):
    daemon_id = docker_json("info", "--format", "{{json .ID}}")
    if not daemon_id:
        raise GuardError("Cannot identify Docker daemon for cleanup.")
    report = cleanup_snapshot(args)
    # A movable protection tag must never unprotect its original image mid-run.
    recheck_args = argparse.Namespace(**vars(args))
    recheck_args.protect = list(args.protect) + report["protected_ids"]
    report.update({"daemon_id": daemon_id, "project": args.project,
                   "repository": args.repository, "applied": args.apply, "removed": []})
    if args.apply:
        for identifier in list(report["candidates"]):
            try:
                if docker_json("info", "--format", "{{json .ID}}") != daemon_id:
                    raise GuardError("Docker daemon changed during cleanup; stopped.")
                if identifier not in cleanup_snapshot(recheck_args)["candidates"]:
                    report["retained"].append({"id": identifier, "reason": "state changed before removal"})
                    continue
                # Do not implicitly delete untagged parents outside this project's scope.
                docker("image", "rm", "--no-prune", identifier)
                report["removed"].append(identifier)
            except (GuardError, OSError, ValueError, KeyError, TypeError) as exc:
                report.update({"error": str(exc), "stopped_at": identifier})
                return 2, report
    return 0, report


def parser():
    root = argparse.ArgumentParser(description=__doc__)
    commands = root.add_subparsers(dest="command", required=True)
    space = commands.add_parser("space", help="Check actual allocation filesystems; exit 1 if insufficient.")
    space.add_argument("--path", action="append", default=[], help="Existing allocation path; repeat per filesystem.")
    space.add_argument("--docker", action="store_true", help="Include the local Unix-socket daemon's data root.")
    space.add_argument("--peak-gib", type=gib_bytes, required=True, help="Estimated additional peak GiB per filesystem.")
    space.set_defaults(handler=check_space)

    build = commands.add_parser("fingerprint", help="Hash stable context and declared immutable inputs.")
    build.add_argument("--project", type=project_name, required=True)
    build.add_argument("--context", required=True)
    build.add_argument("--dockerfile")
    build.add_argument("--platform", required=True, help="Canonical os/architecture[/variant].")
    build.add_argument("--target", default="")
    build.add_argument("--base-image", action="append", required=True)
    build.add_argument("--build-arg", action="append", default=[])
    build.set_defaults(handler=fingerprint)

    find = commands.add_parser("find-image", help="Find matching local images; exit 3 when none match.")
    find.add_argument("--project", type=project_name, required=True)
    find.add_argument("--fingerprint", type=digest, required=True)
    find.add_argument("--platform", required=True)
    find.set_defaults(handler=find_image)

    clean = commands.add_parser("cleanup-images", help="Preview scoped images; --apply enables deletion.")
    clean.add_argument("--project", type=project_name, required=True)
    clean.add_argument("--repository", required=True, help="Exact repository without tag, e.g. registry:5000/team/app.")
    clean.add_argument("--protect", action="append", required=True, help="Current/candidate/rollback/base image ID or ref; repeat.")
    clean.add_argument("--keep-latest", type=positive_integer, default=3)
    clean.add_argument("--older-than-days", type=positive_integer, default=7)
    clean.add_argument("--apply", action="store_true")
    clean.set_defaults(handler=cleanup_images)
    return root


def main(argv=None):
    args = parser().parse_args(argv)
    try:
        status, report = args.handler(args)
    except (GuardError, OSError, ValueError, KeyError, TypeError, RuntimeError) as exc:
        status, report = 2, {"error": str(exc), "passed": False}
    print(json.dumps(report, indent=2, sort_keys=True))
    return status


if __name__ == "__main__":
    sys.exit(main())
