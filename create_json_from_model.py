"""Generate JSON Schema files from namhub.model.csv.

Run after linkml_to_csv.py has regenerated the CSV from LinkML sources.
Two build routes are available via --route:

  curator (default) — synapseclient.extensions.curator.generate_jsonschema.
    Requires the CSV in Curator format (linkml_to_csv.py --format curator)
    and a Synapse login.

  schematic — the original schematicpy pipeline (DataModelParser,
    DataModelGraph, DataModelGraphExplorer, create_json_schema). Requires
    the CSV in schematic format (linkml_to_csv.py --format schematic).

Both routes title each property after the underlying LinkML slot's camelCase
name (e.g. "datasetAssay"); restore_titles() converts that back to a
human-readable label (e.g. "Dataset Assay") before the schema is written.

Usage:
    python create_json_from_model.py [--route curator|schematic]
"""

import argparse
import json
import os
import re

DATA_MODEL_SOURCE = "namhub.model.csv"
DATA_TYPES = [
    "Landscape",
    "Studies",
    "Datasets",
    "People",
    "Grants",
    "NAMs",
    "Publications",
]
OUTPUT_DIRECTORY = "./json_schemas"


def camel_case_to_title(name: str) -> str:
    """Convert a camelCase slot name into a human-readable Title Case label.

    A trailing "Id" word becomes "_id" (e.g. "landscapeId" -> "Landscape_id"),
    matching the source data model's identifier-naming convention.
    """
    spaced = re.sub(r"(?<=[a-z0-9])(?=[A-Z])", " ", name)
    title = spaced[:1].upper() + spaced[1:]
    if title.endswith(" Id"):
        title = title[: -len(" Id")] + "_id"
    return title


def restore_titles(schema: dict) -> None:
    """Replace each property's camelCase title with a Title Case label, in place."""
    for prop in (schema.get("properties") or {}).values():
        title = prop.get("title")
        if title:
            prop["title"] = camel_case_to_title(title)


def write_schema(schema: dict, output_path: str) -> None:
    with open(output_path, "w") as f:
        json.dump(schema, f, indent=2, sort_keys=True)


def build_with_curator(data_model_source: str, data_types: list[str], output_directory: str) -> None:
    from synapseclient import Synapse
    from synapseclient.extensions.curator import generate_jsonschema

    syn = Synapse()
    syn.login()

    schemas, file_paths = generate_jsonschema(
        data_model_source=data_model_source,
        output=output_directory,
        data_types=data_types,
        synapse_client=syn,
    )

    for schema, output_path in zip(schemas, file_paths):
        restore_titles(schema)
        write_schema(schema, output_path)


def build_with_schematic(data_model_source: str, data_types: list[str], output_directory: str) -> None:
    from schematic.schemas.data_model_parser import DataModelParser
    from schematic.schemas.data_model_graph import DataModelGraph, DataModelGraphExplorer
    from schematic.schemas.create_json_schema import create_json_schema

    print(f"Parsing {data_model_source}...")
    parser = DataModelParser(data_model_source)
    parsed = parser.parse_model()

    print("Building graph...")
    graph = DataModelGraph(parsed)
    dmge = DataModelGraphExplorer(graph.graph)

    print("Generating JSON schemas...")
    for dt in data_types:
        output_path = os.path.join(output_directory, f"{dt}.json")
        try:
            schema = create_json_schema(
                dmge=dmge,
                datatype=dt,
                schema_name=dt,
                write_schema=False,
            )
            restore_titles(schema)
            write_schema(schema, output_path)
            n_props = len(schema.get("properties", {}))
            print(f"  {dt:<15} → {output_path}  ({n_props} properties)")
        except Exception as e:
            print(f"  {dt:<15} ERROR: {e}")


ROUTES = {
    "curator": build_with_curator,
    "schematic": build_with_schematic,
}


def main():
    parser = argparse.ArgumentParser(description="Generate JSON Schema files from a data model CSV.")
    parser.add_argument("--route", choices=sorted(ROUTES), default="curator",
                         help="Build route to use (default: curator)")
    parser.add_argument("--source", default=DATA_MODEL_SOURCE)
    parser.add_argument("--output", default=OUTPUT_DIRECTORY)
    args = parser.parse_args()

    os.makedirs(args.output, exist_ok=True)

    ROUTES[args.route](args.source, DATA_TYPES, args.output)


if __name__ == "__main__":
    main()
