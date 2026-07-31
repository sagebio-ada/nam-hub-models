"""Register the Landscape JSON schema with the NAMhub Synapse organization.

Reads json_schemas/Landscape.json, sets the $id to the target version, and
registers it via the Synapse async schema-creation endpoint.

Usage:
    python register_schema.py                 # bumps patch: 1.0.0 → 1.0.1
    python register_schema.py --version 1.1.0 # explicit version
    python register_schema.py --dry-run       # validate without storing
"""

import argparse
import json
import re

import synapseclient
from synapseclient.services.json_schema import JsonSchemaService

SCHEMA_PATH = "json_schemas/Landscape.json"
ORGANIZATION = "NAMhub"
SCHEMA_NAME = "Landscape"
CURRENT_VERSION = "1.0.0"


def bump_patch(version: str) -> str:
    major, minor, patch = version.split(".")
    return f"{major}.{minor}.{int(patch) + 1}"


def get_latest_version(service: JsonSchemaService) -> str:
    """Return the highest semantic version currently registered, or CURRENT_VERSION."""
    versions = list(service.list_json_schema_versions(ORGANIZATION, SCHEMA_NAME))
    sem_versions = [
        v["semanticVersion"]
        for v in versions
        if v.get("semanticVersion")
        and re.match(r"^\d+\.\d+\.\d+$", v["semanticVersion"])
    ]
    if not sem_versions:
        return CURRENT_VERSION
    return max(sem_versions, key=lambda v: list(map(int, v.split("."))))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--version", default=None, help="Semantic version to register")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate schema without storing to Synapse",
    )
    args = parser.parse_args()

    syn = synapseclient.Synapse()
    syn.login(silent=True)
    service = JsonSchemaService(synapse=syn)

    if args.version:
        new_version = args.version
    else:
        latest = get_latest_version(service)
        new_version = bump_patch(latest)

    schema_id = f"{ORGANIZATION}-{SCHEMA_NAME}-{new_version}"

    with open(SCHEMA_PATH) as f:
        schema = json.load(f)

    schema["$id"] = schema_id

    print(f"{'[dry-run] ' if args.dry_run else ''}Registering: {schema_id}")
    service.create_json_schema(schema, dry_run=args.dry_run)

    if args.dry_run:
        print("Dry-run validation passed.")
    else:
        print("Registered successfully.")
        print(f"  $id:     {schema_id}")
        print(f"  version: {new_version}")


if __name__ == "__main__":
    main()
