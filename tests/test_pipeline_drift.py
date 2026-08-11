"""Drift tests for the LinkML -> CSV -> JSON Schema pipeline.

Regenerate the artifacts and compare them against what is committed.
Any difference means either someone edited portal_schemas/
without running ``just gen-model``, or a dependency upgrade changed the output. If a
dependency bump is the cause, re-run ``just gen-model``, read the diff, and commit it.
"""

import subprocess
import sys

import linkml_to_csv

from .conftest import (
    DATA_TYPES,
    JSON_SCHEMA_DIR,
    MODEL_CSV,
    PORTAL_SCHEMA_DIR,
    REPO_ROOT,
)


def test_generated_csv_matches_committed(tmp_path):
    """`just gen-csv` reproduces namhub.model.csv exactly."""
    output = tmp_path / "namhub.model.csv"
    result = subprocess.run(
        [
            sys.executable, "linkml_to_csv.py",
            "--schema", str(PORTAL_SCHEMA_DIR / "namhub.yaml"),
            "--enums", str(PORTAL_SCHEMA_DIR / "enums.yaml"),
            "--output", str(output),
        ],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,  # returncode is asserted below, for a better failure message
    )
    assert result.returncode == 0, f"gen-csv failed:\n{result.stderr}"
    assert output.read_bytes() == MODEL_CSV.read_bytes(), (
        "namhub.model.csv is stale relative to portal_schemas/. "
        "Run `just gen-model` and commit the result."
    )


def test_generated_json_matches_committed(tmp_path):
    """`just gen-json` reproduces every schema in json_schemas/ exactly."""
    result = subprocess.run(
        [
            sys.executable, "create_json_from_model.py",
            "--source", str(MODEL_CSV),
            "--output", str(tmp_path),
        ],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,  # returncode is asserted below, for a better failure message
    )
    assert result.returncode == 0, f"gen-json failed:\n{result.stderr}"

    stale = [
        dt for dt in DATA_TYPES
        if (tmp_path / f"{dt}.json").read_bytes() != (JSON_SCHEMA_DIR / f"{dt}.json").read_bytes()
    ]
    assert not stale, (
        f"these committed schemas are stale: {', '.join(stale)}. "
        "Run `just gen-model` and commit the result."
    )


def test_committed_json_exists_for_every_data_type():
    """No data type may be missing its committed schema."""
    missing = [dt for dt in DATA_TYPES if not (JSON_SCHEMA_DIR / f"{dt}.json").exists()]
    assert not missing, f"no committed schema for: {', '.join(missing)}"


def test_committed_csv_uses_the_curator_headers():
    """namhub.model.csv is in curator format, which is what gen-json expects.

    A header mismatch means the CSV was written by something other than the current
    linkml_to_csv.py, and explains an otherwise cryptic downstream failure.
    """
    header = MODEL_CSV.read_text(encoding="utf-8").splitlines()[0]
    assert header.split(",") == linkml_to_csv.CURATOR_HEADERS, (
        "namhub.model.csv headers do not match the curator format. "
        "Regenerate with `just gen-csv`."
    )
