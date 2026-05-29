"""Backward-compatible Chapter 01 validator CLI/import shim.

The canonical implementation lives in `harness_lab.validators.chapter01`.
"""

from __future__ import annotations

from harness_lab.validators.chapter01 import *  # noqa: F401,F403
from harness_lab.validators.chapter01 import main


if __name__ == "__main__":
    raise SystemExit(main())
