"""Independent literal reports and finite laws, no upstream parser oracle."""

import copy
import hashlib
import json
from pathlib import Path
import unittest
from unittest.mock import patch

from semver_lab import evaluate, evaluate_bytes, serialize
from semver_lab.admission import preflight, Rejection

ROOT = Path(__file__).resolve().parents[1]
CASES = json.loads((ROOT / "tests/cases.json").read_text(encoding="utf-8-sig"))["cases"]


def document(left="1.0.0", right="1.0.0"):
    return {"profile": "semver-precedence/1", "synthetic": True,
            "cases": [{"id": "one", "left": left, "right": right}]}


class ModelTests(unittest.TestCase):
    def test_frozen_reports(self):
        for case in CASES:
            with self.subTest(case=case["id"]):
                self.assertEqual(evaluate(case["input"]), case["expected"])
                raw = json.dumps(case["input"]).encode("ascii")
                self.assertEqual(evaluate_bytes(raw), case["expected"])

    def test_freeze_hashes(self):
        frozen = json.loads((ROOT / "evidence/freeze.json").read_text(encoding="utf-8-sig"))
        self.assertEqual(frozen["cases"], len(CASES))
        for row in frozen["files"]:
            self.assertEqual(hashlib.sha256((ROOT / row["path"]).read_bytes()).hexdigest(), row["sha256"])

    def test_immutable_detached(self):
        value = document("1.0.0+a", "1.0.0+b")
        old = copy.deepcopy(value)
        report = evaluate(value)
        report["cases"][0]["parts_left"]["build"].append("changed")
        report["limits"]["cases"] = 0
        self.assertEqual(value, old)
        self.assertEqual(evaluate(value)["limits"]["cases"], 64)

    def test_late_common_before_unknown(self):
        value = document()
        value["profile"] = "future/1"
        value["cases"].append({"id": "two", "left": 1, "right": "x"})
        self.assertEqual(evaluate(value)["error"], {"code": "string_required", "path": "/cases/1/left"})
        self.assertIsNone(evaluate(value)["cases"])

    def test_duplicate_id_and_fields(self):
        value = document()
        value["cases"] *= 2
        self.assertEqual(evaluate(value)["error"]["code"], "duplicate_id")
        value = document()
        value["cases"][0]["extra"] = True
        self.assertEqual(evaluate(value)["error"]["code"], "object_fields")

    def test_json_decoder_controls(self):
        for raw, code in [(b'{"x":1,"x":2}', "duplicate_key"), (b'NaN', "constant_invalid"),
                          (b'{} trailing', "json_invalid"), (b'\xff', "utf8_invalid"),
                          (b'1' * 33, "numeric_limit"), (b'1.2', "ordinary_type_required")]:
            with self.subTest(code=code):
                self.assertEqual(evaluate_bytes(raw)["error"]["code"], code)
        self.assertEqual(evaluate_bytes(bytearray(b'{}'))["error"]["code"], "bytes_required")

    def test_raw_depth_boundaries(self):
        raw = b' ' * (65536 - 2) + b'{}'
        self.assertEqual(evaluate_bytes(raw)["status"], "invalid")
        self.assertEqual(evaluate_bytes(raw + b' ')["error"]["code"], "raw_limit")
        deep = b'[' * 10 + b']' * 10
        self.assertEqual(evaluate_bytes(deep)["error"]["code"], "depth_limit")
        quoted = document('1.0.0+' + 'x' * 60)
        self.assertEqual(evaluate_bytes(json.dumps(quoted).encode())["status"], "complete")

    def test_exact_type_and_cycles(self):
        class Untrusted:
            def __str__(self):
                raise RuntimeError("hook must not execute")
        class FakeDict(dict):
            def items(self):
                raise RuntimeError("hook must not execute")
        for obj in (Untrusted(), FakeDict(), 1.0, (1,), {2: "x"}):
            self.assertEqual(evaluate(obj)["error"]["code"], "ordinary_type_required")
        obj = []; obj.append(obj)
        self.assertEqual(evaluate(obj)["error"]["code"], "cycle")
        obj = {}; obj["self"] = obj
        self.assertEqual(evaluate(obj)["error"]["code"], "cycle")

    def test_alias_and_node_accounting(self):
        shared = [True]
        preflight([shared, shared])
        with patch("semver_lab.admission.LIMITS", {"nodes": 4, "depth": 8, "version_chars": 256, "numeric_digits": 32}):
            with self.assertRaises(Rejection) as caught:
                preflight([shared, shared])
            self.assertEqual(caught.exception.code, "node_limit")
        preflight([True] * 4095)
        with self.assertRaises(Rejection):
            preflight([True] * 4096)
        with patch("semver_lab.admission.LIMITS", {"nodes": 2, "depth": 8, "version_chars": 256, "numeric_digits": 32}):
            with self.assertRaises(Rejection):
                preflight({"x": True})

    def test_native_dfs_error_order(self):
        value = {"first": 1.0, 2: True}
        self.assertEqual(evaluate(value)["error"], {"code": "ordinary_type_required", "path": "/first"})
        self.assertEqual(evaluate({2: True})["error"], {"code": "ordinary_type_required", "path": "/key-0"})
        self.assertEqual(evaluate_bytes(b']' + b'[' * 20)["error"]["code"], "json_invalid")
        self.assertEqual(evaluate({"x" * 10000: True})["error"], {"code": "text_limit", "path": "/key-0"})

    def test_oracle_correction_lineage(self):
        old = json.loads((ROOT / "evidence/cases-freeze-v1.json").read_text(encoding="utf-8"))
        new = json.loads((ROOT / "tests/cases.json").read_text(encoding="utf-8-sig"))
        old_case = next(case for case in old["cases"] if case["id"] == "ascii_invalid")
        self.assertEqual(old_case["expected"]["input_profile"], "semver-precedence/1")
        old_case["expected"]["input_profile"] = None
        self.assertEqual(old, new)

    def test_native_depth_and_int(self):
        value = True
        for _ in range(8):
            value = [value]
        preflight(value)
        self.assertEqual(evaluate([value])["error"]["code"], "depth_limit")
        preflight(10**32 - 1)
        self.assertEqual(evaluate(10**32)["error"]["code"], "numeric_limit")

    def test_component_bounds(self):
        accepted = ["1" * 32 + ".0.0", "1.0.0-" + "1" * 32,
                    "1.0.0+" + "a" * 64, "1.0.0+" + ".".join(["a"] * 16)]
        for version in accepted:
            self.assertEqual(evaluate(document(version))["status"], "complete")
        value = document("x" * 256)
        self.assertEqual(evaluate(value)["error"]["code"], "version_grammar")
        value["cases"][0]["left"] += "x"
        self.assertEqual(evaluate(value)["error"]["code"], "text_limit")

    def test_case_boundaries(self):
        value = document()
        value["cases"] = [{"id": f"p{i}", "left": "1.0.0", "right": "1.0.0"} for i in range(64)]
        self.assertEqual(len(evaluate(value)["cases"]), 64)
        value["cases"].append({"id": "last", "left": "1.0.0", "right": "1.0.0"})
        self.assertEqual(evaluate(value)["error"]["code"], "case_limit")

    def test_serialization_and_output_seam(self):
        report = evaluate(document())
        raw = serialize(report)
        self.assertEqual(raw, serialize(evaluate(document())))
        self.assertTrue(raw.endswith(b'\n'))
        self.assertEqual(json.loads(raw), report)
        with patch.dict("semver_lab.model.LIMITS", output_bytes=len(raw)-1):
            with self.assertRaises(Rejection) as caught:
                serialize(report)
            self.assertEqual(caught.exception.code, "output_limit")

    def test_maximum_shape_fits_output(self):
        # An amplification fixture, not proof this is the largest possible report.
        pre = '.'.join(['abcdefghijklmno'] * 8)
        build = '.'.join(['abcdefghijklmn'] * 8)
        version = '1.0.0-' + pre + '+' + build
        self.assertEqual(len(version), 253)
        value = document()
        value["cases"] = [{"id": f"pair{i:02d}" + 'x'*26, "left": version, "right": version} for i in range(64)]
        report = evaluate(value)
        self.assertEqual(report["status"], "complete")
        self.assertLess(len(serialize(report)),1048576)

    def test_finite_algebra(self):
        domain = ["0.0.0", "1.0.0-0", "1.0.0-1", "1.0.0-9", "1.0.0-10",
                  "1.0.0-A", "1.0.0-a", "1.0.0-a.1", "1.0.0", "1.0.0+one", "2.0.0"]
        orders = {}
        for a in domain:
            for b in domain:
                row = evaluate(document(a,b))["cases"][0]
                order = {"less":-1,"equal":0,"greater":1}[row["relation"]]
                orders[a,b] = order
                if a == b:
                    self.assertEqual(order, 0)
                    self.assertTrue(row["literal_equal"])
                altered = evaluate(document(a.split('+')[0]+'+new', b.split('+')[0]+'+other'))["cases"][0]
                self.assertEqual(altered["relation"], row["relation"])
        for a in domain:
            for b in domain:
                self.assertEqual(orders[a,b], -orders[b,a])
                for c in domain:
                    if orders[a,b] <= 0 and orders[b,c] <= 0:
                        self.assertLessEqual(orders[a,c], 0)
