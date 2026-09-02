"""Data model package for nam-hub-models."""

from pathlib import Path
from .namhub import *  # noqa: F403

THIS_PATH = Path(__file__).parent

SCHEMA_DIRECTORY = THIS_PATH.parent / "schema"
MAIN_SCHEMA_PATH = SCHEMA_DIRECTORY / "namhub.yaml"
