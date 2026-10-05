"""Owned-file transport and checked delivery, including interpreter shutdown."""

import argparse
import json
import os
import stat
import sys

from .admission import LIMITS, Rejection
from .model import evaluate_bytes, serialize

HELP = b"Usage: python -I lab.py INPUT [--output FRESH_FILE]\nSynthetic bounded SemVer precedence only.\n"
EXIT = {"complete": 0, "invalid": 2, "unsupported": 3, "limit": 4}


def _silence(stream):
    # Stop CPython's shutdown flush from replacing controlled exit5 with exit120.
    try:
        fd = stream.fileno()
        with open(os.devnull, "wb") as sink:
            os.dup2(sink.fileno(), fd)
    except (OSError, ValueError, AttributeError):
        return


def _write(stream, data):
    try:
        count = stream.write(data)
        if type(count) is not int or count != len(data):
            raise OSError("short_write")
        stream.flush()
    except (OSError, ValueError):
        _silence(stream)
        raise


def _diagnostic(stream, code):
    try:
        _write(stream, (json.dumps({"error": code}, separators=(",", ":")) + "\n").encode("ascii"))
        return True
    except (OSError, ValueError):
        return False


class Parser(argparse.ArgumentParser):
    def error(self, _message):
        raise Rejection("usage")


def _path(value):
    if value.startswith(("\\\\", "//", "\\?", "\\.")):
        raise OSError("nonlocal_path")
    if os.name == "nt" and ":" in os.path.splitdrive(value)[1]:
        raise OSError("alternate_stream")
    return value


def main(argv=None, *, stdout=None, stderr=None):
    """Return checked evaluation/delivery status; never echo user filenames."""
    out = sys.stdout.buffer if stdout is None else stdout
    err = sys.stderr.buffer if stderr is None else stderr
    parser = Parser(prog="semver-lab", add_help=False)
    parser.add_argument("input", nargs="?")
    parser.add_argument("--output")
    parser.add_argument("--help", action="store_true")
    try:
        args = parser.parse_args(argv)
        if args.help:
            _write(out, HELP)
            return 0
        if args.input is None:
            raise Rejection("usage")
    except Rejection:
        return 2 if _diagnostic(err, "usage") else 5
    except (OSError, ValueError):
        _diagnostic(err, "output_failure")
        return 5
    try:
        with open(_path(args.input), "rb") as stream:
            if not stat.S_ISREG(os.fstat(stream.fileno()).st_mode):
                raise OSError("ordinary_file_required")
            raw = stream.read(LIMITS["raw_bytes"] + 1)
    except (OSError, ValueError):
        _diagnostic(err, "input_failure")
        return 5
    report = evaluate_bytes(raw)
    try:
        payload = serialize(report)
    except Rejection:
        return 4 if _diagnostic(err, "output_limit") else 5
    try:
        if args.output is not None:
            with open(_path(args.output), "xb") as stream:
                _write(stream, payload)
        else:
            _write(out, payload)
    except (OSError, ValueError):
        _diagnostic(err, "output_failure")
        return 5
    return EXIT[report["status"]]
