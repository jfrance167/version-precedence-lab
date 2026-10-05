"""Pure whole-input evaluation with no rows on incomplete admission."""

import json

from .admission import common, decode, LIMITS, PROFILE, Rejection, reject
from .version import caps, compare, grammar


def _report(profile, rows=None, error=None):
    status = error.status if error is not None else "complete"
    return {"schema": "semver-precedence-report/1", "input_profile": profile,
            "status": status, "evaluation": "complete" if status == "complete" else "incomplete",
            "limits": dict(LIMITS), "assumptions": {
                "standard": "SemVer 2.0.0 bounded syntax/precedence", "package_existence": "unknown",
                "authenticity": "unknown", "compatibility": "unknown", "security": "unknown"},
            "cases": rows if status == "complete" else None,
            "error": None if error is None else {"code": error.code, "path": error.path}}


def evaluate(value):
    """Validate all common fields, then all grammar, then all caps, before comparing."""
    profile = None
    try:
        profile = common(value)
        if profile != PROFILE:
            reject("profile_unsupported", "/profile", "unsupported")
        parsed = []
        for index, case in enumerate(value["cases"]):
            parsed.append(tuple(grammar(case[field], f"/cases/{index}/{field}") for field in ("left", "right")))
        for index, pair in enumerate(parsed):
            for field, version in zip(("left", "right"), pair):
                caps(version, f"/cases/{index}/{field}")
        rows = []
        for index, (case, pair) in enumerate(zip(value["cases"], parsed)):
            left, right = pair
            relation, evidence = compare(left, right)
            rows.append({"index": index, "id": case["id"], "left": left.original, "right": right.original,
                         "parts_left": left.parts(), "parts_right": right.parts(), "relation": relation,
                         "literal_equal": left.original == right.original, "build_ignored": True, "evidence": evidence})
        return _report(profile, rows)
    except Rejection as error:
        return _report(profile, error=error)


def evaluate_bytes(raw):
    """Exact UTF-8 bytes entry point with bounded predecode guards."""
    try:
        value = decode(raw)
    except Rejection as error:
        return _report(None, error=error)
    return evaluate(value)


def serialize(report):
    """Encode the whole model report before opening output or writing bytes."""
    encoded = (json.dumps(report, ensure_ascii=True, sort_keys=True, separators=(",", ":"),
                          allow_nan=False) + "\n").encode("ascii")
    if len(encoded) > LIMITS["output_bytes"]:
        reject("output_limit", status="limit")
    return encoded
