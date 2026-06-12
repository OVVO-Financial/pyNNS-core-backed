from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path
from typing import Any, cast

import pytest

SCRIPT_DIR = Path(__file__).with_name("r_scripts")


@pytest.mark.parity
@pytest.mark.parametrize(
    "script_name",
    [
        "generate_partial_moments.R",
        "generate_central_tendencies.R",
        "generate_regression.R",
    ],
)
def test_optional_r_fixture_regeneration_scripts_emit_json(script_name: str) -> None:
    if shutil.which("Rscript") is None:
        pytest.skip("Rscript is unavailable; committed fixtures are used instead")

    completed = subprocess.run(
        ["Rscript", str(SCRIPT_DIR / script_name)],
        check=True,
        capture_output=True,
        text=True,
    )
    payload = cast(dict[str, Any], json.loads(completed.stdout))

    assert isinstance(payload, dict)
    assert "source" in payload
