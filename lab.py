"""Trusted source bootstrap; no install or third-party runtime dependencies."""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from semver_lab.cli import main

if __name__ == "__main__":
    raise SystemExit(main())
