"""Convert NAMHub LinkML schemas to a schematic/Curator-compatible CSV data model.

Reads portal_schemas/namhub.yaml and portal_schemas/enums.yaml and writes
namhub.model.csv. Two output formats are supported via --format:

  curator (default) — the format in modules/dataLandscape/annotationProperty.csv,
    for use with synapseclient.extensions.curator (create_json_from_model.py
    --route curator). Headers:
        Attribute, Description, Valid Values, DependsOn, Required, Properties,
        Validation Rules, columnType, Format, Pattern, Minimum, Maximum,
        IsTemplate, Source

  schematic — the original format expected by schematicpy's DataModelParser
    (create_json_from_model.py --route schematic). Headers:
        Attribute, Description, Valid Values, DependsOn, DependsOn Component,
        Required, Parent, Validation Rules, Properties, Source

Mapping from LinkML (shared):
    class             → template row: DependsOn = slot list
    slot              → attribute row: Required = True if required in the
                        base slot definition or any class slot_usage
    range: <Enum>     → Valid Values = comma-separated permissible_values

curator-only mapping:
    class             → IsTemplate = True
    range: date       → columnType = string, Format = date
    range: uri        → columnType = string, Format = uri
    range: integer     → columnType = number
    range: boolean     → columnType = boolean
    multivalued: true  → columnType gets a "_list" suffix (string/boolean)
    pattern            → Pattern
    minimum_value/maximum_value → Minimum/Maximum

schematic-only mapping:
    slot              → Parent = all classes using it

Usage:
    python linkml_to_csv.py [--format curator|schematic] [--output namhub.model.csv]
"""

import argparse
import csv
import re
from pathlib import Path
from collections import defaultdict

import yaml

SCHEMA_DIR = Path("portal_schemas")

CURATOR_HEADERS = [
    "Attribute",
    "Description",
    "Valid Values",
    "DependsOn",
    "Required",
    "Properties",
    "Validation Rules",
    "columnType",
    "Format",
    "Pattern",
    "Minimum",
    "Maximum",
    "IsTemplate",
    "Source",
]

SCHEMATIC_HEADERS = [
    "Attribute",
    "Description",
    "Valid Values",
    "DependsOn",
    "DependsOn Component",
    "Required",
    "Parent",
    "Validation Rules",
    "Properties",
    "Source",
]

# ── Helpers ────────────────────────────────────────────────────────────────────

def load_yaml(path: Path) -> dict:
    with open(path) as f:
        return yaml.safe_load(f)


def normalise_text(s: str) -> str:
    if not s:
        return ""
    return re.sub(r"\s+", " ", s).strip()


def build_enum_lookup(enums_schema: dict, namhub_schema: dict) -> dict[str, list[str]]:
    lookup: dict[str, list[str]] = {}
    for schema in (enums_schema, namhub_schema):
        for name, defn in (schema.get("enums") or {}).items():
            pv = defn.get("permissible_values") or {}
            lookup[name] = list(pv.keys())
    return lookup


def get_valid_values(slot_def: dict, enum_lookup: dict) -> str:
    range_ = slot_def.get("range", "string")
    if range_ in enum_lookup:
        return ", ".join(enum_lookup[range_])
    return ""


def get_column_type(slot_def: dict) -> tuple[str, str]:
    """Return (columnType, Format) for a slot based on its LinkML range."""
    range_ = slot_def.get("range", "string")
    multivalued = bool(slot_def.get("multivalued"))

    if range_ == "date":
        base, fmt = "string", "date"
    elif range_ == "uri":
        base, fmt = "string", "uri"
    elif range_ == "integer":
        base, fmt = "number", ""
    elif range_ == "boolean":
        base, fmt = "boolean", ""
    else:
        # plain string range, or an enum range (valid values carry the constraint)
        base, fmt = "string", ""

    if multivalued and base in ("string", "boolean"):
        return f"{base}_list", fmt
    return base, fmt


def build_slot_required(namhub_schema: dict) -> dict[str, bool]:
    """slot_name → True if required in the base slot definition or any class slot_usage."""
    all_slots: dict[str, dict] = namhub_schema.get("slots") or {}
    all_classes: dict[str, dict] = namhub_schema.get("classes") or {}

    slot_required: dict[str, bool] = {}
    for slot_name, slot_def in all_slots.items():
        if slot_def.get("required"):
            slot_required[slot_name] = True
    for class_def in all_classes.values():
        for slot_name, usage in (class_def.get("slot_usage") or {}).items():
            if usage.get("required"):
                slot_required[slot_name] = True
    return slot_required


def merge_slot_def(slot_name: str, namhub_schema: dict) -> dict:
    """Base slot definition merged with slot_usage overrides from every class that uses it."""
    all_slots: dict[str, dict] = namhub_schema.get("slots") or {}
    all_classes: dict[str, dict] = namhub_schema.get("classes") or {}

    merged = dict(all_slots.get(slot_name) or {})
    for class_def in all_classes.values():
        usage = (class_def.get("slot_usage") or {}).get(slot_name, {})
        if usage:
            merged.update(usage)
    return merged


# ── Curator format ──────────────────────────────────────────────────────────────

def convert_curator(namhub_schema: dict, enums_schema: dict) -> list[dict]:
    enum_lookup = build_enum_lookup(enums_schema, namhub_schema)
    all_classes: dict[str, dict] = namhub_schema.get("classes") or {}
    slot_required = build_slot_required(namhub_schema)

    rows: list[dict] = []
    emitted_slots: set[str] = set()

    for class_name, class_def in all_classes.items():
        class_slots: list[str] = class_def.get("slots") or []

        # Template row — DependsOn lists the slots for this template
        rows.append({
            "Attribute": class_name,
            "Description": normalise_text(class_def.get("description", "")),
            "Valid Values": "",
            "DependsOn": ", ".join(class_slots),
            "Required": "",
            "Properties": "",
            "Validation Rules": "",
            "columnType": "",
            "Format": "",
            "Pattern": "",
            "Minimum": "",
            "Maximum": "",
            "IsTemplate": "True",
            "Source": "",
        })

        # Slot rows (emitted once globally)
        for slot_name in class_slots:
            if slot_name in emitted_slots:
                continue
            emitted_slots.add(slot_name)

            merged = merge_slot_def(slot_name, namhub_schema)
            desc = normalise_text(merged.get("description", ""))
            valid_vals = get_valid_values(merged, enum_lookup)
            column_type, fmt = get_column_type(merged)
            required = "True" if slot_required.get(slot_name) else "False"

            rows.append({
                "Attribute": slot_name,
                "Description": desc,
                "Valid Values": valid_vals,
                "DependsOn": "",
                "Required": required,
                "Properties": "",
                "Validation Rules": "",
                "columnType": column_type,
                "Format": fmt,
                "Pattern": merged.get("pattern", ""),
                "Minimum": merged.get("minimum_value", ""),
                "Maximum": merged.get("maximum_value", ""),
                "IsTemplate": "",
                "Source": "",
            })

    return rows


# ── schematic format ─────────────────────────────────────────────────────────────

def convert_schematic(namhub_schema: dict, enums_schema: dict) -> list[dict]:
    enum_lookup = build_enum_lookup(enums_schema, namhub_schema)
    all_classes: dict[str, dict] = namhub_schema.get("classes") or {}
    slot_required = build_slot_required(namhub_schema)

    # Build reverse map: slot_name → [class_name, ...]
    slot_parents: dict[str, list[str]] = defaultdict(list)
    for class_name, class_def in all_classes.items():
        for slot_name in (class_def.get("slots") or []):
            slot_parents[slot_name].append(class_name)

    rows: list[dict] = []
    emitted_slots: set[str] = set()

    for class_name, class_def in all_classes.items():
        class_slots: list[str] = class_def.get("slots") or []

        # Template row — DependsOn lists the slots for this template
        rows.append({
            "Attribute": class_name,
            "Description": normalise_text(class_def.get("description", "")),
            "Valid Values": "",
            "DependsOn": ", ".join(class_slots),
            "DependsOn Component": "",
            "Required": "",
            "Parent": "",
            "Validation Rules": "",
            "Properties": "",
            "Source": "",
        })

        # Slot rows (emitted once globally; Parent lists all classes that use them)
        for slot_name in class_slots:
            if slot_name in emitted_slots:
                continue
            emitted_slots.add(slot_name)

            merged = merge_slot_def(slot_name, namhub_schema)
            desc = normalise_text(merged.get("description", ""))
            valid_vals = get_valid_values(merged, enum_lookup)
            required = "TRUE" if slot_required.get(slot_name) else "FALSE"
            parents = ", ".join(slot_parents[slot_name])

            rows.append({
                "Attribute": slot_name,
                "Description": desc,
                "Valid Values": valid_vals,
                "DependsOn": "",
                "DependsOn Component": "",
                "Required": required,
                "Parent": parents,
                "Validation Rules": "",
                "Properties": "",
                "Source": "",
            })

    return rows


FORMATS = {
    "curator": (CURATOR_HEADERS, convert_curator),
    "schematic": (SCHEMATIC_HEADERS, convert_schematic),
}


def main():
    parser = argparse.ArgumentParser(description="Convert LinkML schemas to a schematic/Curator-compatible CSV.")
    parser.add_argument("--format", choices=sorted(FORMATS), default="curator",
                         help="CSV format to emit (default: curator)")
    parser.add_argument("--output", default="namhub.model.csv")
    parser.add_argument("--schema", default=str(SCHEMA_DIR / "namhub.yaml"))
    parser.add_argument("--enums", default=str(SCHEMA_DIR / "enums.yaml"))
    args = parser.parse_args()

    headers, convert = FORMATS[args.format]

    namhub_schema = load_yaml(Path(args.schema))
    enums_schema = load_yaml(Path(args.enums))

    rows = convert(namhub_schema, enums_schema)

    with open(args.output, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)

    if args.format == "curator":
        templates = sum(1 for r in rows if r["IsTemplate"] == "True")
    else:
        templates = sum(1 for r in rows if not r["Parent"] and r["DependsOn"])
    slots = len(rows) - templates
    print(f"Wrote {len(rows)} rows ({templates} templates, {slots} slots) → {args.output} [{args.format} format]")


if __name__ == "__main__":
    main()
