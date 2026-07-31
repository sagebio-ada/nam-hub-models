"""Generate JSON Schema files from namhub.model.csv.

Run after linkml_to_csv.py has regenerated the CSV from LinkML sources.
Two build routes are available via --route:

  apply_enum_values() — the generator builds its enum entries from the CSV's
    comma-joined "Valid Values" cell, which strips whitespace, upper-cases the first
    letter, and splits any value that itself contains a comma. The values are taken
    from the LinkML source instead, so none of that has to be undone.

  apply_required() — the CSV has a single "Required" column per attribute, so a slot
    required by one class is marked required for every class that uses it. The
    per-class truth only exists in the LinkML slot_usage blocks.

  restore_titles() — the generator titles each property after the underlying LinkML
    slot's camelCase name (e.g. "datasetAssay"); this converts it back to a
    human-readable label (e.g. "Dataset Assay").

The first two look up slots by each property's original camelCase title, so both must
run before restore_titles() rewrites it.

One schema is written per class in portal_schemas/namhub.yaml, so adding a class there
is all that is needed to have it generated.

Usage:
    python create_json_from_model.py
"""

import argparse
import json
import os
import re
from typing import NamedTuple

import yaml

DATA_MODEL_SOURCE = "namhub.model.csv"
PORTAL_SCHEMA_DIR = "portal_schemas"
OUTPUT_DIRECTORY = "./json_schemas"


class Model(NamedTuple):
    """The parts of the LinkML source that the CSV cannot represent faithfully."""

    slots: dict[str, dict]
    """camelCase slot name -> {"range": LinkML range, "multivalued": bool}"""

    class_required: dict[str, set[str]]
    """class name -> camelCase names of the slots that class requires"""

    enum_values: dict[str, list[tuple[str, str]]]
    """LinkML enum name -> [(permissible value, description or "")], in source order"""

    @property
    def data_types(self) -> list[str]:
        """Class names in source order — one JSON schema is generated per class."""
        return list(self.class_required)


def _one_line(text: str) -> str:
    """Collapse a folded YAML description onto a single line."""
    return re.sub(r"\s+", " ", text).strip() if text else ""


def load_model(schema_dir: str = PORTAL_SCHEMA_DIR) -> Model:
    """Read the LinkML sources. Enums may be defined in either file."""
    with open(os.path.join(schema_dir, "enums.yaml")) as f:
        enums_schema = yaml.safe_load(f)
    with open(os.path.join(schema_dir, "namhub.yaml")) as f:
        namhub_schema = yaml.safe_load(f)

    all_slots: dict[str, dict] = namhub_schema.get("slots") or {}
    slots = {
        name: {"range": defn.get("range"), "multivalued": bool(defn.get("multivalued"))}
        for name, defn in all_slots.items()
    }

    # A slot is required for a class if the class's slot_usage says so, or if the base
    # slot definition does — but only for the classes that actually use that slot.
    base_required = {name for name, defn in all_slots.items() if defn.get("required")}
    class_required: dict[str, set[str]] = {}
    for class_name, class_def in (namhub_schema.get("classes") or {}).items():
        from_usage = {
            slot_name
            for slot_name, usage in (class_def.get("slot_usage") or {}).items()
            if usage.get("required")
        }
        class_required[class_name] = from_usage | (base_required & set(class_def.get("slots") or []))

    enum_values: dict[str, list[tuple[str, str]]] = {}
    for schema in (enums_schema, namhub_schema):
        for enum_name, enum_def in (schema.get("enums") or {}).items():
            enum_values[enum_name] = [
                (value, _one_line(value_def.get("description") if isinstance(value_def, dict) else ""))
                for value, value_def in (enum_def.get("permissible_values") or {}).items()
            ]

    return Model(slots, class_required, enum_values)


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


def apply_enum_values(schema: dict, model: Model) -> None:
    """Replace every generated enum with the verbatim LinkML permissible values, in place.

    The shapes mirror what the generator emits, so that only the values change: the enum
    sits under "items" for a multivalued slot, and is written as "oneOf" — the only form
    RJSF (the form renderer downstream) reads per-value metadata from — when the enum
    documents its values, otherwise as a plain "enum" list.
    """
    for prop in (schema.get("properties") or {}).values():
        slot = model.slots.get(prop.get("title"))
        values = model.enum_values.get(slot["range"]) if slot else None
        if not values:
            continue

        for holder in (prop, prop.get("items")):
            if isinstance(holder, dict):
                holder.pop("enum", None)
                holder.pop("oneOf", None)

        target = prop.setdefault("items", {}) if slot["multivalued"] else prop
        if any(description for _, description in values):
            target["oneOf"] = [
                {"const": value, "title": value, **({"description": description} if description else {})}
                for value, description in values
            ]
        else:
            target["enum"] = [value for value, _ in values]


def apply_required(schema: dict, model: Model) -> None:
    """Replace the generator's global required list with this class's own, in place."""
    required = model.class_required.get(schema.get("title"), set())
    schema["required"] = sorted(
        key
        for key, prop in (schema.get("properties") or {}).items()
        if prop.get("title") in required
    )


def restore_titles(schema: dict) -> None:
    """Replace each property's camelCase title with a Title Case label, in place."""
    for prop in (schema.get("properties") or {}).values():
        title = prop.get("title")
        if title:
            prop["title"] = camel_case_to_title(title)


def write_schema(schema: dict, output_path: str) -> None:
    with open(output_path, "w") as f:
        json.dump(schema, f, indent=2, sort_keys=True)


def build(data_model_source: str, output_directory: str) -> None:
    from synapseclient import Synapse
    from synapseclient.extensions.curator import generate_jsonschema

    model = load_model()

    schemas, file_paths = generate_jsonschema(
        data_model_source=data_model_source,
        output=output_directory,
        data_types=model.data_types,
        synapse_client=Synapse(),
    )

    for schema, output_path in zip(schemas, file_paths):
        apply_enum_values(schema, model)
        apply_required(schema, model)
        restore_titles(schema)
        write_schema(schema, output_path)
        print(f"  {schema.get('title', ''):<15} → {output_path}")


def main():
    parser = argparse.ArgumentParser(description="Generate JSON Schema files from a data model CSV.")
    parser.add_argument("--source", default=DATA_MODEL_SOURCE)
    parser.add_argument("--output", default=OUTPUT_DIRECTORY)
    args = parser.parse_args()

    os.makedirs(args.output, exist_ok=True)

    build(args.source, args.output)


if __name__ == "__main__":
    main()
