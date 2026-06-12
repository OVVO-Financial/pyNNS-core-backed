#!/usr/bin/env python
"""Regenerate or validate committed R NNS parity cache entries."""

from __future__ import annotations

import argparse
import os
from pathlib import Path

import pytest


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--tests",
        nargs="+",
        default=["tests/parity"],
        help="pytest paths to execute while exercising the R cache",
    )
    parser.add_argument(
        "--offline",
        action="store_true",
        help="validate cache-only coverage without invoking Rscript",
    )
    parser.add_argument(
        "--pytest-arg",
        action="append",
        default=[],
        help="extra argument forwarded to pytest; repeat for multiple arguments",
    )
    args = parser.parse_args()

    repo = Path(__file__).resolve().parents[1]
    os.chdir(repo)
    os.environ.pop("CI", None)
    os.environ.pop("PYNNS_R_CACHE_ONLY", None)
    os.environ.pop("PYNNS_OFFLINE", None)
    if args.offline:
        os.environ["PYNNS_R_CACHE_ONLY"] = "1"

    return pytest.main(["-q", "-n0", *args.pytest_arg, *args.tests])


if __name__ == "__main__":
    raise SystemExit(main())
