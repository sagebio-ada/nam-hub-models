"""Shared paths for the NAMHub integration tests."""

from pathlib import Path

import create_json_from_model

REPO_ROOT = Path(__file__).resolve().parent.parent
PORTAL_SCHEMA_DIR = REPO_ROOT / "portal_schemas"
JSON_SCHEMA_DIR = REPO_ROOT / "json_schemas"
MODEL_CSV = REPO_ROOT / "namhub.model.csv"
EXAMPLE_DATA_DIR = Path(__file__).resolve().parent / "data"

VALID_DIR = EXAMPLE_DATA_DIR / "valid"
INVALID_DIR = EXAMPLE_DATA_DIR / "invalid"

# One schema is generated per class in namhub.yaml; create_json_from_model derives the
# list from the schema itself, so there is no separate constant to drift from it.
DATA_TYPES = create_json_from_model.load_model(str(PORTAL_SCHEMA_DIR)).data_types
