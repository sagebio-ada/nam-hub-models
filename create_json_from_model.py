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

import yaml

DATA_MODEL_SOURCE = "namhub.model.csv"
PORTAL_SCHEMA_DIR = "portal_schemas"
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


def _strip_ws(s: str) -> str:
    """Remove whitespace the same way the curator/schematic routes do when they turn a
    permissible value name into an enum entry (e.g. "Level 1" -> "Level1")."""
    return re.sub(r"\s+", "", s)


def load_enum_value_descriptions(schema_dir: str = PORTAL_SCHEMA_DIR) -> dict[str, dict[str, str]]:
    """LinkML enum name -> {enum entry (whitespace-stripped): description}.

    Only includes values that actually have a description. Reads both YAML files
    since enums can be defined in either.
    """
    descriptions: dict[str, dict[str, str]] = {}
    for filename in ("enums.yaml", "namhub.yaml"):
        with open(os.path.join(schema_dir, filename)) as f:
            schema = yaml.safe_load(f)
        for enum_name, enum_def in (schema.get("enums") or {}).items():
            values: dict[str, str] = {}
            for value, value_def in (enum_def.get("permissible_values") or {}).items():
                desc = value_def.get("description") if isinstance(value_def, dict) else None
                if desc:
                    values[_strip_ws(value)] = re.sub(r"\s+", " ", desc).strip()
            if values:
                descriptions[enum_name] = values
    return descriptions


def load_slot_ranges(schema_dir: str = PORTAL_SCHEMA_DIR) -> dict[str, str]:
    """camelCase slot name -> LinkML range, merged with class slot_usage overrides."""
    with open(os.path.join(schema_dir, "namhub.yaml")) as f:
        namhub_schema = yaml.safe_load(f)

    ranges: dict[str, str] = {
        name: defn["range"] for name, defn in (namhub_schema.get("slots") or {}).items() if defn.get("range")
    }
    for class_def in (namhub_schema.get("classes") or {}).values():
        for slot_name, usage in (class_def.get("slot_usage") or {}).items():
            if usage.get("range"):
                ranges[slot_name] = usage["range"]
    return ranges


def _expand_enum(values: list, value_descriptions: dict) -> list:
    return [
        {
            "const": value,
            "title": value,
            **(
                {"description": value_descriptions[_strip_ws(value)]}
                if _strip_ws(value) in value_descriptions
                else {}
            ),
        }
        for value in values
    ]


def restore_enum_descriptions(schema: dict, slot_ranges: dict, enum_value_descriptions: dict) -> None:
    """Attach permissible-value descriptions to enum properties, in place.

    Both routes emit a raw enum list with no way to carry per-value metadata. The curator
    route puts it directly on the property (or under "items" for multivalued slots). The
    schematic route wraps it in "oneOf" instead — as its lone entry for a required slot,
    or alongside a {"type": "null"} branch for an optional one — so the enum-bearing
    branch has to be located by scanning rather than assumed to be the only one. RJSF (the
    form renderer downstream) only recognizes per-value metadata on "oneOf" entries with a
    "const", so that's the shape used here regardless of which raw shape came in. Must run
    before restore_titles(), since it keys off each property's original camelCase title.
    """
    for prop in (schema.get("properties") or {}).values():
        slot_name = prop.get("title")
        if not slot_name:
            continue
        value_descriptions = enum_value_descriptions.get(slot_ranges.get(slot_name))
        if not value_descriptions:
            continue

        one_of_wrapper = prop.get("oneOf")
        enum_index = None
        if isinstance(one_of_wrapper, list):
            enum_index = next(
                (i for i, branch in enumerate(one_of_wrapper) if isinstance(branch, dict) and "enum" in branch),
                None,
            )

        if enum_index is not None:
            expanded = _expand_enum(one_of_wrapper[enum_index]["enum"], value_descriptions)
            prop["oneOf"] = one_of_wrapper[:enum_index] + expanded + one_of_wrapper[enum_index + 1 :]
        elif "items" in prop and "enum" in prop["items"]:
            prop["items"]["oneOf"] = _expand_enum(prop["items"]["enum"], value_descriptions)
            del prop["items"]["enum"]
        elif "enum" in prop:
            prop["oneOf"] = _expand_enum(prop["enum"], value_descriptions)
            del prop["enum"]


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

    slot_ranges = load_slot_ranges()
    enum_value_descriptions = load_enum_value_descriptions()

    for schema, output_path in zip(schemas, file_paths):
        restore_enum_descriptions(schema, slot_ranges, enum_value_descriptions)
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
    slot_ranges = load_slot_ranges()
    enum_value_descriptions = load_enum_value_descriptions()

    for dt in data_types:
        output_path = os.path.join(output_directory, f"{dt}.json")
        try:
            schema = create_json_schema(
                dmge=dmge,
                datatype=dt,
                schema_name=dt,
                write_schema=False,
            )
            restore_enum_descriptions(schema, slot_ranges, enum_value_descriptions)
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
