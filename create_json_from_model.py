"""Generate JSON Schema files from namhub.model.csv.

Run after linkml_to_csv.py has regenerated the CSV from LinkML sources.
Two build routes are available via --route:

  curator (default) — synapseclient.extensions.curator.generate_jsonschema.
    Requires the CSV in Curator format (linkml_to_csv.py --format curator)
    and a Synapse login.

  schematic — the original schematicpy pipeline (DataModelParser,
    DataModelGraph, DataModelGraphExplorer, create_json_schema). Requires
    the CSV in schematic format (linkml_to_csv.py --format schematic).

Usage:
    python create_json_from_model.py [--route curator|schematic]
"""

import argparse
import os

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


def build_with_curator(data_model_source: str, data_types: list[str], output_directory: str) -> None:
    from synapseclient import Synapse
    from synapseclient.extensions.curator import generate_jsonschema

    syn = Synapse()
    syn.login()

    generate_jsonschema(
        data_model_source=data_model_source,
        output=output_directory,
        data_types=data_types,
        synapse_client=syn,
    )


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
                write_schema=True,
                schema_path=output_path,
            )
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
