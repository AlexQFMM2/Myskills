import argparse
from contextlib import redirect_stdout
from datetime import datetime, timedelta, timezone
import importlib.util
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "release_guard.py"
SPEC = importlib.util.spec_from_file_location("release_guard", SCRIPT)
guard = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(guard)


def make_image(number, days=30, repository="example/app", project="example", gc=True):
    labels = {guard.LABEL + "project": project, guard.LABEL + "fingerprint": "a" * 64}
    if gc:
        labels[guard.LABEL + "gc"] = "eligible"
    return {"Id": "sha256:" + format(number, "064x"),
            "Created": (datetime.now(timezone.utc) - timedelta(days=days)).isoformat(),
            "RepoTags": [repository + ":v" + str(number)],
            "Config": {"Labels": labels}, "Os": "linux", "Architecture": "amd64"}


class FakeDocker:
    """Stateful Docker command boundary: real selection/deletion logic still runs."""

    def __init__(self, images):
        self.images = {item["Id"]: item for item in images}
        self.containers = {}
        self.calls = []
        self.info_count = 0
        self.before_recheck = None
        self.fail_remove = None
        self.daemon = "test-daemon"

    def __call__(self, *args):
        self.calls.append(args)
        if args[:1] == ("info",):
            self.info_count += 1
            if self.info_count == 2 and self.before_recheck:
                self.before_recheck()
            return json.dumps(self.daemon)
        if args[:2] == ("image", "ls"):
            project = args[-1].split("=", 2)[-1]
            return "\n".join(key for key, item in self.images.items()
                             if guard.image_labels(item).get(guard.LABEL + "project") == project)
        if args[:2] == ("image", "inspect"):
            for item in self.images.values():
                if args[2] == item["Id"] or args[2] in (item.get("RepoTags") or []):
                    return json.dumps([item])
            raise guard.GuardError("Missing image")
        if args[:2] == ("container", "ls"):
            return "\n".join(self.containers)
        if args[:2] == ("container", "inspect"):
            return json.dumps([{"Image": self.containers[args[2]]}])
        if args[:2] == ("image", "rm"):
            if args != ("image", "rm", "--no-prune", args[-1]):
                raise AssertionError("Deletion must disable parent pruning and must not force")
            if args[-1] == self.fail_remove:
                raise guard.GuardError("Removal refused")
            if args[-1] in self.containers.values():
                raise guard.GuardError("Image is used")
            del self.images[args[-1]]
            return args[-1]
        raise AssertionError("Unexpected Docker command: " + repr(args))


class SpaceTests(unittest.TestCase):
    def test_floor_and_peak_are_both_enforced(self):
        with tempfile.TemporaryDirectory() as directory:
            for free, peak, passed in [(20 * guard.GIB - 1, 0, False),
                                       (20 * guard.GIB, 0, True),
                                       (21 * guard.GIB, 10 * guard.GIB, False),
                                       (30 * guard.GIB, 10 * guard.GIB, True)]:
                with self.subTest(free=free, peak=peak), patch.object(
                        guard.shutil, "disk_usage", return_value=SimpleNamespace(free=free)):
                    report = guard.space_report([directory], peak)
                    self.assertEqual(report["passed"], passed)
                    self.assertEqual(report["filesystems"][0]["shortfall_bytes"],
                                     max(0, 20 * guard.GIB + peak - free))

    def test_duplicate_mount_paths_are_grouped(self):
        with tempfile.TemporaryDirectory() as directory:
            child = Path(directory) / "child"
            child.mkdir()
            report = guard.space_report([directory, str(child)], 0)
            self.assertEqual(len(report["filesystems"]), 1)
            self.assertEqual(len(report["filesystems"][0]["paths"]), 2)

    def test_different_mounts_are_each_checked(self):
        paths = [SimpleNamespace(resolve=lambda strict: SimpleNamespace(
            stat=lambda: SimpleNamespace(st_dev=1), __str__=lambda: "one")),
            SimpleNamespace(resolve=lambda strict: SimpleNamespace(
                stat=lambda: SimpleNamespace(st_dev=2), __str__=lambda: "two"))]
        with patch.object(guard, "Path", side_effect=paths), patch.object(
                guard.shutil, "disk_usage", side_effect=[SimpleNamespace(free=99 * guard.GIB),
                                                         SimpleNamespace(free=19 * guard.GIB)]):
            report = guard.space_report(["one", "two"], 0)
        self.assertFalse(report["passed"])
        self.assertEqual(len(report["filesystems"]), 2)

    def test_missing_path_fails_instead_of_using_parent(self):
        with tempfile.TemporaryDirectory() as directory, redirect_stdout(io.StringIO()) as output:
            status = guard.main(["space", "--path", str(Path(directory) / "missing"), "--peak-gib", "0"])
            self.assertEqual(status, 2)
            self.assertFalse(json.loads(output.getvalue())["passed"])

    def test_nonfinite_and_negative_estimates_are_rejected(self):
        for value in ["nan", "inf", "-1", "not-a-number"]:
            with self.subTest(value=value), self.assertRaises(argparse.ArgumentTypeError):
                guard.gib_bytes(value)

    def test_remote_docker_is_not_checked_with_local_df(self):
        with patch.dict(os.environ, {"DOCKER_HOST": "ssh://example"}, clear=True):
            with self.assertRaises(guard.GuardError):
                guard.local_docker_root()

    def test_explicit_context_overrides_docker_host(self):
        with patch.dict(os.environ, {"DOCKER_CONTEXT": "remote", "DOCKER_HOST": "unix:///run/docker.sock"}, clear=True), patch.object(
                guard, "docker_json", return_value="tcp://remote:2376") as cli:
            with self.assertRaises(guard.GuardError):
                guard.local_docker_root()
            self.assertEqual(cli.call_args.args[:3], ("context", "inspect", "remote"))

    def test_desktop_vm_is_not_checked_as_host_storage(self):
        with patch.dict(os.environ, {}, clear=True), patch.object(guard, "docker_json", side_effect=[
                "unix:///run/docker.sock", {"OperatingSystem": "Docker Desktop", "DockerRootDir": "/var/lib/docker"}]):
            with self.assertRaises(guard.GuardError):
                guard.local_docker_root()

    def test_failed_cli_gate_prevents_dependent_shell_command(self):
        with tempfile.TemporaryDirectory() as directory:
            env = dict(os.environ, TEST_PYTHON=sys.executable, TEST_GUARD=str(SCRIPT), TEST_DIR=directory)
            result = subprocess.run(["bash", "-c", '''
if "$TEST_PYTHON" "$TEST_GUARD" space --path "$TEST_DIR" --peak-gib 100000000000; then
    touch "$TEST_DIR/allocated"
else
    guard_status=$?
    exit "$guard_status"
fi
'''], env=env, capture_output=True, text=True)
            self.assertEqual(result.returncode, 1, result.stderr)
            self.assertFalse(json.loads(result.stdout)["passed"])
            self.assertFalse((Path(directory) / "allocated").exists())


class FingerprintTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.context = Path(self.temp.name)
        (self.context / "Dockerfile").write_text("FROM scratch\nCOPY payload /payload\n")
        (self.context / "payload").write_text("one")
        self.args = guard.parser().parse_args(["fingerprint", "--project", "example", "--context", str(self.context),
                                              "--platform", "linux/amd64", "--base-image", "scratch"])

    def fingerprint(self):
        return guard.fingerprint(self.args)[1]["fingerprint"]

    def test_stable_content_does_not_depend_on_timestamp(self):
        before = self.fingerprint()
        os.utime(self.context / "payload", (100, 100))
        self.assertEqual(self.fingerprint(), before)

    def test_dirty_untracked_and_permission_changes_invalidate(self):
        previous = self.fingerprint()
        for change in [lambda: (self.context / "payload").write_text("two"),
                       lambda: (self.context / "untracked").write_text("new input"),
                       lambda: (self.context / "payload").chmod(0o755)]:
            change()
            current = self.fingerprint()
            self.assertNotEqual(current, previous)
            previous = current

    def test_build_parameters_all_affect_fingerprint(self):
        original = self.fingerprint()
        for field, value in [("platform", "linux/arm64"), ("target", "runtime"),
                             ("build_arg", ["FEATURE=enabled"]),
                             ("base_image", ["base@sha256:" + "b" * 64])]:
            with self.subTest(field=field):
                before = getattr(self.args, field)
                setattr(self.args, field, value)
                self.assertNotEqual(self.fingerprint(), original)
                setattr(self.args, field, before)

    def test_argument_order_is_irrelevant_and_values_are_not_reported(self):
        self.args.build_arg = ["SECOND=private-value", "FIRST=1"]
        before = guard.fingerprint(self.args)[1]
        self.args.build_arg.reverse()
        self.assertEqual(before, guard.fingerprint(self.args)[1])
        self.assertNotIn("private-value", json.dumps(before))

    def test_mutable_base_and_duplicate_arguments_fail(self):
        self.args.base_image = ["python:latest"]
        with self.assertRaises(guard.GuardError):
            self.fingerprint()
        self.args.base_image = ["scratch"]
        self.args.build_arg = ["A=1", "A=2"]
        with self.assertRaises(guard.GuardError):
            self.fingerprint()

    def test_external_symlink_fails(self):
        with tempfile.TemporaryDirectory() as outside:
            (Path(outside) / "input").write_text("outside")
            (self.context / "link").symlink_to(Path(outside) / "input")
            with self.assertRaises(guard.GuardError):
                self.fingerprint()

    def test_external_dockerfile_contents_are_hashed(self):
        with tempfile.TemporaryDirectory() as outside:
            path = Path(outside) / "Dockerfile"
            path.write_text("FROM scratch\n")
            self.args.dockerfile = str(path)
            before = self.fingerprint()
            path.write_text("FROM scratch\nENV SETTING=changed\n")
            self.assertNotEqual(before, self.fingerprint())


class ImageTests(unittest.TestCase):
    def test_docker_nanosecond_creation_timestamp(self):
        value = guard.created_at({"Created": "2026-01-01T00:00:00.123456789Z"})
        self.assertEqual(value.microsecond, 123456)
        self.assertEqual(value.tzinfo, timezone.utc)

    def setUp(self):
        self.images = [make_image(number, days=20 + number) for number in range(1, 9)]
        self.images += [make_image(9, days=1), make_image(10, days=2), make_image(11, days=3)]
        self.images[5]["Config"]["Labels"].pop(guard.LABEL + "gc")  # not opted in
        self.images[6]["RepoTags"] = ["other/app:v7"]
        self.images[7]["RepoTags"].append("example/app:another-tag")
        self.fake = FakeDocker(self.images)
        self.fake.containers["stopped-container"] = self.images[3]["Id"]
        self.patch = patch.object(guard, "docker", side_effect=self.fake)
        self.patch.start()
        self.addCleanup(self.patch.stop)
        self.args = guard.parser().parse_args([
            "cleanup-images", "--project", "example", "--repository", "example/app",
            "--protect", self.images[0]["Id"], "--protect", self.images[1]["Id"],
            "--protect", self.images[2]["Id"]])

    def test_preview_protects_releases_dependencies_containers_and_recent_versions(self):
        code, report = guard.cleanup_images(self.args)
        self.assertEqual(code, 0)
        self.assertEqual(report["candidates"], [self.images[4]["Id"]])
        self.assertEqual(len(report["retained"]), 10)
        self.assertEqual(report["removed"], [])
        self.assertFalse(any(call[:2] == ("image", "rm") for call in self.fake.calls))

    def test_apply_removes_only_candidate_without_parent_prune_or_force(self):
        self.args.apply = True
        code, report = guard.cleanup_images(self.args)
        self.assertEqual(code, 0)
        self.assertEqual(report["removed"], [self.images[4]["Id"]])
        self.assertNotIn(self.images[4]["Id"], self.fake.images)
        self.assertEqual(len(self.fake.images), 10)

    def test_unresolved_protection_stops_before_any_deletion(self):
        self.args.protect.append("missing:rollback")
        self.args.apply = True
        with self.assertRaises(guard.GuardError):
            guard.cleanup_images(self.args)
        self.assertFalse(any(call[:2] == ("image", "rm") for call in self.fake.calls))

    def test_new_container_reference_between_preview_and_delete_is_retained(self):
        self.args.apply = True
        self.fake.before_recheck = lambda: self.fake.containers.update({"new-container": self.images[4]["Id"]})
        code, report = guard.cleanup_images(self.args)
        self.assertEqual(code, 0)
        self.assertEqual(report["removed"], [])

    def test_retagged_candidate_is_rechecked_before_removal(self):
        self.args.apply = True
        self.fake.before_recheck = lambda: self.images[4]["RepoTags"].append("other/app:shared")
        code, report = guard.cleanup_images(self.args)
        self.assertEqual(code, 0)
        self.assertEqual(report["removed"], [])

    def test_protection_added_after_preview_is_respected(self):
        tag = "example/app:rollback"
        self.images[0]["RepoTags"].append(tag)
        self.args.protect.append(tag)
        self.args.apply = True

        def move_tag():
            self.images[0]["RepoTags"].remove(tag)
            self.images[4]["RepoTags"] = [tag]

        self.fake.before_recheck = move_tag
        code, report = guard.cleanup_images(self.args)
        self.assertEqual(code, 0)
        self.assertEqual(report["removed"], [])
        self.assertIn(self.images[0]["Id"], report["protected_ids"])

    def test_daemon_switch_stops_deletion(self):
        self.args.apply = True
        self.fake.before_recheck = lambda: setattr(self.fake, "daemon", "different-daemon")
        code, report = guard.cleanup_images(self.args)
        self.assertEqual(code, 2)
        self.assertEqual(report["removed"], [])

    def test_partial_failure_reports_prior_deletions(self):
        extra = make_image(12, days=60)
        self.fake.images[extra["Id"]] = extra
        self.fake.fail_remove = extra["Id"]
        self.args.apply = True
        code, report = guard.cleanup_images(self.args)
        self.assertEqual(code, 2)
        self.assertEqual(report["removed"], [self.images[4]["Id"]])
        self.assertEqual(report["stopped_at"], extra["Id"])

    def test_dangling_images_and_other_projects_are_not_deleted(self):
        dangling = make_image(12)
        dangling["RepoTags"] = None
        other = make_image(13, project="other")
        self.fake.images[dangling["Id"]] = dangling
        self.fake.images[other["Id"]] = other
        _, report = guard.cleanup_images(self.args)
        self.assertNotIn(dangling["Id"], report["candidates"])
        self.assertNotIn(other["Id"], report["candidates"])

    def test_age_rule_applies_even_when_recent_count_is_lower(self):
        self.args.keep_latest = 1
        _, report = guard.cleanup_images(self.args)
        self.assertEqual(report["candidates"], [self.images[4]["Id"]])

    def test_reuse_requires_matching_fingerprint_and_platform(self):
        args = guard.parser().parse_args(["find-image", "--project", "example",
                                          "--fingerprint", "a" * 64, "--platform", "linux/amd64"])
        code, report = guard.find_image(args)
        self.assertEqual(code, 0)
        self.assertEqual(len(report["image_ids"]), 11)
        args.platform = "linux/arm64"
        self.assertEqual(guard.find_image(args)[0], 3)
        args.platform = "linux/amd64"
        args.fingerprint = "b" * 64
        self.assertEqual(guard.find_image(args)[0], 3)

    def test_docker_failure_is_not_a_reuse_miss(self):
        with patch.object(guard, "docker", side_effect=guard.GuardError("unavailable")), redirect_stdout(io.StringIO()) as out:
            code = guard.main(["find-image", "--project", "example", "--fingerprint", "a" * 64, "--platform", "linux/amd64"])
        self.assertEqual(code, 2)
        self.assertIn("error", json.loads(out.getvalue()))


if __name__ == "__main__":
    unittest.main()
