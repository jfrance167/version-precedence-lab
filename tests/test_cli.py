"""Actual CLI pipes and owned files plus narrow deterministic I/O seams."""

import io
import json
import os
from pathlib import Path
import subprocess
import sys
import uuid
import unittest
from unittest.mock import patch

from semver_lab.cli import main
from test_model import CASES, ROOT, document


class Sink:
    def __init__(self, mode):
        self.mode = mode
    def write(self, data):
        if self.mode == "dirty":
            raise OSError("dirty")
        return len(data)-1 if self.mode == "short" else len(data)
    def flush(self):
        if self.mode == "flush":
            raise OSError("flush")


class CloseFailure(io.BytesIO):
    def __exit__(self, *_args):
        raise OSError("close")


class CLITests(unittest.TestCase):
    def setUp(self):
        self.root = ROOT / ".verification-work" / ("cli-" + uuid.uuid4().hex)
        self.root.mkdir(parents=True)
        self.input = self.root / "input.json"
        self.input.write_text(json.dumps(document()), encoding="utf-8")

    def command(self, *args):
        return [sys.executable, "-I", *(["-O"] if sys.flags.optimize else []), str(ROOT / "lab.py"), *map(str,args)]

    def run_cli(self, *args):
        return subprocess.run(self.command(*args), capture_output=True, timeout=10, check=False, shell=False)

    def test_actual_all_frozen(self):
        for case in CASES:
            with self.subTest(case=case["id"]):
                self.input.write_text(json.dumps(case["input"]), encoding="utf-8")
                process = self.run_cli(self.input)
                self.assertEqual(process.returncode, {"complete":0,"invalid":2,"unsupported":3,"limit":4}[case["expected"]["status"]])
                self.assertEqual(process.stderr, b"")
                self.assertEqual(json.loads(process.stdout), case["expected"])

    def test_fresh_existing_empty_directory(self):
        output = self.root / "out.json"
        self.assertEqual(self.run_cli(self.input,"--output",output).returncode, 0)
        before = output.read_bytes()
        for path in (output,"",self.root,self.root / "missing" / "out.json"):
            result = self.run_cli(self.input,"--output",path)
            self.assertEqual(result.returncode,5)
            self.assertEqual(result.stdout,b"")
            self.assertEqual(result.stderr,b'{"error":"output_failure"}\n')
        self.assertEqual(output.read_bytes(),before)

    def test_missing_usage_help(self):
        self.assertEqual(self.run_cli(self.root / "missing").returncode,5)
        self.assertEqual(self.run_cli().returncode,2)
        process = self.run_cli("--help")
        self.assertEqual(process.returncode,0)
        self.assertEqual(process.stderr,b"")
        self.assertIn(b"Synthetic",process.stdout)
        self.assertEqual(self.run_cli("--unknown").returncode,2)

    def test_dirty_short_flush_and_both_sinks(self):
        for mode in ("dirty","short","flush"):
            for args in ([str(self.input)],["--help"]):
                err = io.BytesIO()
                self.assertEqual(main(args,stdout=Sink(mode),stderr=err),5)
                self.assertEqual(err.getvalue(),b'{"error":"output_failure"}\n')
                self.assertEqual(main(args,stdout=Sink(mode),stderr=Sink("dirty")),5)
        self.assertEqual(main([],stdout=io.BytesIO(),stderr=Sink("flush")),5)

    def test_close_and_output_cap_seams(self):
        real_open = open
        def failing_open(path,mode):
            return CloseFailure() if mode == "xb" else real_open(path,mode)
        with patch("semver_lab.cli.open",side_effect=failing_open):
            self.assertEqual(main([str(self.input),"--output","fresh"],stdout=io.BytesIO(),stderr=io.BytesIO()),5)
        with patch.dict("semver_lab.model.LIMITS",output_bytes=1):
            self.assertEqual(main([str(self.input)],stdout=io.BytesIO(),stderr=io.BytesIO()),4)
            self.assertEqual(main([str(self.input)],stdout=io.BytesIO(),stderr=Sink("dirty")),5)

    def test_actual_closed_pipes_shutdown(self):
        for args in ([str(self.input)],["--help"],[str(self.root / "missing")],[]):
            process = subprocess.Popen(self.command(*args),stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=False)
            # Readers close before child startup completes; no output sink remains.
            process.stdout.close()
            process.stderr.close()
            self.assertEqual(process.wait(timeout=10),5)

    def test_nonlocal_paths(self):
        for value in ("//server/file", "\\\\server\\file"):
            result = self.run_cli(value)
            self.assertEqual(result.returncode,5)
            self.assertNotIn(value.encode(),result.stderr)
