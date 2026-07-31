"""Generate the portal JSON schemas through the legacy schematicpy pathway.

Temporary. This exists only to cross-check the curator pathway in
create_json_from_model.py while that migration is in progress, and is meant to be deleted
afterwards: `rm schematic_route.py`, then drop the gen-json-schematic recipe and
schematic_schema_dir from the justfile and json_schemas_schematic/ from .gitignore.
Nothing imports this module.

It cannot share an environment with the curator pathway. Every release of schematicpy
pins synapseclient to 4.8.0 or older, and 4.8.0 has no "curator" extra at all, while
create_json_from_model.py needs >=4.13.0. `just gen-json-schematic` therefore runs this
in a throwaway environment instead of the project venv.

Both pathways read the same namhub.model.csv -- synapseclient's curator extension is a
fork of schematic's parser, and a superset of it -- so shim_csv() only has to reconcile
the two respects in which schematic's parser is stricter. Everything after generation is
shared: the same load_model(), apply_enum_values(), apply_required() and restore_titles()
run here, so the two routes differ only in which generator produced the raw schema.

Two things this route cannot reproduce. The CSV's Format, Pattern, Minimum and Maximum
columns are curator-only additions -- schematic derives those from validation rules
instead -- so the schemas written here carry no "format", "pattern", "minimum" or
"maximum". And schematic names properties after the slot verbatim where curator
upper-cases the first character ("landscapeId" vs "LandscapeId"), so this writes to its
own directory rather than over the committed json_schemas/.

Usage:
    python schematic_route.py [--source namhub.model.csv] [--output json_schemas_schematic]
"""

import argparse
import csv
import os
import tempfile

from create_json_from_model import (
    apply_enum_values,
    apply_required,
    load_model,
    restore_titles,
    write_schema,
)

DATA_MODEL_SOURCE = "namhub.model.csv"
OUTPUT_DIRECTORY = "./json_schemas_schematic"

# Headers schematic's parser requires but the curator CSV does not carry. Both can stay
# empty: the only structural check is that a template row's DependsOn resolves to
# something, which the IsTemplate rows already satisfy.
REQUIRED_EMPTY_HEADERS = ["DependsOn Component", "Parent"]

LIST_SUFFIX = "_list"


def shim_csv(source: str, dest: str) -> None:
    """Copy the curator CSV to dest, reconciling schematic's two stricter expectations.

    Its required-header check is a subset test, so the curator-only columns pass through
    untouched and only REQUIRED_EMPTY_HEADERS have to be added.

    Its allowed columnType values are the four JSON Schema scalars, with no "_list"
    variants, so a multivalued slot moves onto the "list" validation rule instead. The
    base scalar stays behind in columnType -- schematic reads array-ness solely from the
    rule -- which is what keeps the element type on the generated array.
    """
    with open(source, newline="") as f:
        reader = csv.DictReader(f)
        headers = list(reader.fieldnames or []) + REQUIRED_EMPTY_HEADERS
        rows = list(reader)

    for row in rows:
        row.update(dict.fromkeys(REQUIRED_EMPTY_HEADERS, ""))
        if row["columnType"].endswith(LIST_SUFFIX):
            row["columnType"] = row["columnType"][: -len(LIST_SUFFIX)]
            row["Validation Rules"] = "::".join(
                filter(None, [row["Validation Rules"], "list"])
            )

    with open(dest, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)


def build(data_model_source: str, output_directory: str) -> None:
    from schematic.schemas.create_json_schema import create_json_schema
    from schematic.schemas.data_model_graph import (
        DataModelGraph,
        DataModelGraphExplorer,
    )
    from schematic.schemas.data_model_parser import DataModelParser

    model = load_model()

    with tempfile.TemporaryDirectory() as workdir:
        shimmed = os.path.join(workdir, "schematic.model.csv")
        shim_csv(data_model_source, shimmed)
        parsed = DataModelParser(shimmed).parse_model()

    dmge = DataModelGraphExplorer(DataModelGraph(parsed).graph)

    for data_type in model.data_types:
        output_path = os.path.join(output_directory, f"{data_type}.json")
        schema = create_json_schema(
            dmge=dmge,
            datatype=data_type,
            schema_name=data_type,
            write_schema=False,
        )
        apply_enum_values(schema, model)
        apply_required(schema, model)
        restore_titles(schema)
        write_schema(schema, output_path)
        print(f"  {data_type:<15} → {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Generate JSON Schema files from a data model CSV via schematicpy."
    )
    parser.add_argument("--source", default=DATA_MODEL_SOURCE)
    parser.add_argument("--output", default=OUTPUT_DIRECTORY)
    args = parser.parse_args()

    os.makedirs(args.output, exist_ok=True)

    build(args.source, args.output)


if __name__ == "__main__":
    main()
