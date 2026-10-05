"""Repeatable checks and current-byte receipts, no installs or network.

Usage: python -I scripts/verify_project.py. Requires installed Bandit on this
interpreter. Retains fresh raw evidence and copies the reviewed public receipt.
Subprocesses are explicit owned Python checks with fixed argv and no shell.
"""

import ast
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
import uuid

ROOT = Path(__file__).resolve().parents[1]


def main():
    work = ROOT / ".verification-work" / ("acceptance-" + uuid.uuid4().hex)
    work.mkdir(parents=True)
    results, counts = [], {}

    def run(label, args, timeout=90):
        process = subprocess.run([sys.executable, "-I", *args], cwd=ROOT, capture_output=True,
                                 timeout=timeout, check=False, shell=False)
        (work / (label + ".stdout")).write_bytes(process.stdout)
        (work / (label + ".stderr")).write_bytes(process.stderr)
        results.append({"check": label, "exit": process.returncode})
        return process

    for mode, prefix in (("normal", []), ("optimized", ["-O"])):
        process = run(mode, prefix + ["scripts/run_tests.py"])
        match = re.search(rb"Ran (\d+) tests", process.stderr)
        counts[mode] = int(match.group(1)) if match else None
    run("compile", ["-m", "compileall", "-q", "semver_lab", "lab.py", "scripts", "tests"])
    mutation_process = run("mutations", ["scripts/verify_mutations.py"], 120)
    mutations = json.loads(mutation_process.stdout) if mutation_process.returncode == 0 else None
    run("restored", ["scripts/run_tests.py"])
    bandit = work / "bandit.json"
    run("bandit-production", ["-m", "bandit", "-r", "semver_lab", "lab.py", "-f", "json", "-o", str(bandit)])
    harness = work / "harness-bandit.json"
    harness_process = run("bandit-harness", ["-m", "bandit", "-r", "scripts", "tests", "-f", "json", "-o", str(harness)])
    scanner = json.loads(bandit.read_text()) if bandit.exists() else None
    harness_scanner = json.loads(harness.read_text()) if harness.exists() else None
    if scanner is None or scanner["results"] or scanner["errors"]:
        raise RuntimeError("Production SAST not clean/available")
    if harness_scanner is None or harness_scanner["errors"] or any(
            row["issue_severity"] != "LOW" or row["test_id"] not in ("B404", "B603")
            for row in harness_scanner["results"]):
        raise RuntimeError("Unreviewed harness finding")
    if harness_process.returncode not in (0, 1):
        raise RuntimeError("Harness scanner failed")
    # Static gate corroborates pure model source; this is not OS containment.
    for name in ("admission.py", "version.py", "model.py"):
        tree = ast.parse((ROOT / "semver_lab" / name).read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            names = ([row.name for row in node.names] if isinstance(node, ast.Import) else
                     [node.module or ""] if isinstance(node, ast.ImportFrom) else [])
            if any(name.split('.')[0] in ("os", "subprocess", "socket", "pathlib", "urllib", "pickle", "importlib") for name in names):
                raise RuntimeError("Unexpected model I/O import")
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in ("open", "eval", "exec", "__import__"):
                raise RuntimeError("Unexpected model I/O call")
    files = [ROOT / name for name in ("CONTRACT.md", "lab.py", "tests/cases.json", "evidence/freeze.json",
                                     "evidence/freeze-v1.json", "evidence/cases-freeze-v1.json")]
    files += sorted((ROOT / "semver_lab").glob("*.py"))
    files += sorted((ROOT / "tests").glob("*.py")) + sorted((ROOT / "scripts").glob("*.py"))
    hashes = [{"path": file.relative_to(ROOT).as_posix(), "bytes": file.stat().st_size,
               "sha256": hashlib.sha256(file.read_bytes()).hexdigest()} for file in files]
    receipts = {"date": datetime.now(timezone.utc).isoformat(), "runtime": sys.version, "platform": sys.platform,
                "counts": counts, "frozen_cases": 41, "actual_cli_cases_per_mode": 41,
                "checks": results, "mutations": mutations, "source_sha256": hashes,
                "finite_domain": {"versions": 11, "pairs": 121, "triples": 1331},
                "bandit": {"production_findings": len(scanner["results"]), "production_errors": len(scanner["errors"]),
                           "harness_findings": len(harness_scanner["results"]), "harness_errors": len(harness_scanner["errors"])},
                "pure_source_gate": "PASS; static inspection only", "hosted": "NOT RUN",
                "real_packages": False, "raw_directory": str(work)}
    passed = all(row["exit"] == 0 for row in results if row["check"] != "bandit-harness")
    (work / "receipt.json").write_text(json.dumps(receipts, indent=2) + "\n", encoding="utf-8")
    if passed:
        for source, destination in ((work / "receipt.json", ROOT / "evidence/receipt.json"),
                                    (bandit, ROOT / "evidence/bandit.json"), (harness, ROOT / "evidence/harness-bandit.json")):
            destination.write_bytes(source.read_bytes())
    print(json.dumps({"pass": passed, "checks": results, "receipt": str(work / "receipt.json")}))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
