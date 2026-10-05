"""Strict bounded grammar and SemVer precedence; build stays literal only."""

from dataclasses import dataclass
import re

from .admission import reject, LIMITS

GRAMMAR = re.compile(
    r"(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)"
    r"(?:-([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?"
    r"(?:\+([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?", re.ASCII)


@dataclass(frozen=True)
class Version:
    """Internal immutable parts; construction alone does not validate a string."""

    original: str
    core: tuple
    prerelease: tuple
    build: tuple

    def parts(self):
        return {"core": list(self.core), "prerelease": [
            {"value": item, "kind": "numeric" if item.isdigit() else "text"}
            for item in self.prerelease], "build": list(self.build)}


def grammar(text, path):
    match = GRAMMAR.fullmatch(text)
    if match is None:
        reject("version_grammar", path)
    major, minor, patch, pre, build = match.groups()
    prerelease = tuple(pre.split(".")) if pre is not None else ()
    if any(item.isdigit() and len(item) > 1 and item[0] == "0" for item in prerelease):
        reject("version_grammar", path)
    return Version(text, (major, minor, patch), prerelease,
                   tuple(build.split(".")) if build is not None else ())


def caps(version, path):
    for item in version.core:
        if len(item) > LIMITS["numeric_digits"]:
            reject("core_limit", path, "limit")
    for group in (version.prerelease, version.build):
        if len(group) > LIMITS["identifiers"]:
            reject("identifier_count_limit", path, "limit")
        for item in group:
            if len(item) > LIMITS["identifier_chars"]:
                reject("identifier_limit", path, "limit")
            if group is version.prerelease and item.isdigit() and len(item) > LIMITS["numeric_digits"]:
                reject("numeric_prerelease_limit", path, "limit")


def _order(left, right):
    return (left > right) - (left < right)


def _numeric(left, right):
    return _order((len(left), left), (len(right), right))


def compare(left, right):
    """Return precedence relation and first decisive rule for admitted parts."""
    def result(order, rule, index=None, a=None, b=None):
        return ("less" if order < 0 else "greater" if order > 0 else "equal",
                {"rule": rule, "index": index, "left": a, "right": b})

    for index, (a, b) in enumerate(zip(left.core, right.core)):
        order = _numeric(a, b)
        if order:
            return result(order, ("core_major", "core_minor", "core_patch")[index], index, a, b)
    if bool(left.prerelease) != bool(right.prerelease):
        return result(-1 if left.prerelease else 1, "release_presence", None,
                      bool(left.prerelease), bool(right.prerelease))
    for index, (a, b) in enumerate(zip(left.prerelease, right.prerelease)):
        if a == b:
            continue
        numeric_a, numeric_b = a.isdigit(), b.isdigit()
        if numeric_a != numeric_b:
            return result(-1 if numeric_a else 1, "numeric_vs_text", index, a, b)
        rule = "prerelease_numeric" if numeric_a else "prerelease_text"
        order = _numeric(a, b) if numeric_a else _order(a, b)
        return result(order, rule, index, a, b)
    if len(left.prerelease) != len(right.prerelease):
        return result(_order(len(left.prerelease), len(right.prerelease)), "prerelease_prefix",
                      None, len(left.prerelease), len(right.prerelease))
    return result(0, "equal")
