"""Three isolated semantic mutations; original source is never modified.

Usage: python -I scripts/verify_mutations.py. Requires only stdlib; uses owned
project scratch, executes inspected copied tests and retains raw failure logs.
Each mutation must cause the designated frozen-report assertion, not a crash.
"""

import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import uuid

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "semver_lab/version.py"
MUTANTS = [
    ("build_tiebreak", '    return result(0, "equal")',
     '    return result(_order(left.build, right.build), "equal")', "build_equal"),
    ("lexical_numeric", '        order = _numeric(a, b) if numeric_a else _order(a, b)',
     '        order = _order(a, b)', "numeric_pre"),
    ("reverse_release", 'return result(-1 if left.prerelease else 1, "release_presence", None,',
     'return result(1 if left.prerelease else -1, "release_presence", None,', "release_greater")]


def main():
    original = SOURCE.read_bytes()
    digest = hashlib.sha256(original).hexdigest()
    work = ROOT / ".verification-work" / ("mutations-" + uuid.uuid4().hex)
    work.mkdir(parents=True)
    outcomes = []
    for label, before, after, target in MUTANTS:
        directory = work / label
        directory.mkdir()
        for name in ("semver_lab", "tests", "scripts", "evidence"):
            shutil.copytree(ROOT / name, directory / name, ignore=shutil.ignore_patterns("__pycache__"))
        shutil.copyfile(ROOT / "CONTRACT.md", directory / "CONTRACT.md")
        shutil.copyfile(ROOT / "lab.py", directory / "lab.py")
        text = original.decode("utf-8")
        if text.count(before) != 1:
            raise RuntimeError("Mutation anchor changed")
        (directory / "semver_lab/version.py").write_text(text.replace(before, after), encoding="utf-8")
        process = subprocess.run([sys.executable, "-I", "scripts/run_tests.py"], cwd=directory,
                                 capture_output=True, timeout=45, check=False, shell=False)
        (directory / "stdout.log").write_bytes(process.stdout)
        (directory / "stderr.log").write_bytes(process.stderr)
        stderr = process.stderr.decode("utf-8", errors="replace")
        detected = (process.returncode == 1 and "AssertionError" in stderr and
                    f"case='{target}'" in stderr and "ERROR:" not in stderr)
        outcomes.append({"mutation": label, "target": target, "exit": process.returncode,
                         "intended_assertion_detected": detected})
    unchanged = hashlib.sha256(SOURCE.read_bytes()).hexdigest() == digest
    summary = {"outcomes": outcomes, "original_unchanged": unchanged,
               "original_sha256": digest, "work": str(work)}
    print(json.dumps(summary))
    return 0 if unchanged and all(row["intended_assertion_detected"] for row in outcomes) else 1


if __name__ == "__main__":
    raise SystemExit(main())
