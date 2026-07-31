"""Convert NAMHub LinkML schemas to a Curator-compatible CSV data model.

Reads portal_schemas/namhub.yaml and portal_schemas/enums.yaml and writes
namhub.model.csv in the format used by modules/dataLandscape/annotationProperty.csv,
for use with synapseclient.extensions.curator (create_json_from_model.py). Headers:

    Attribute, Description, Valid Values, DependsOn, Required, Properties,
    Validation Rules, columnType, Format, Pattern, Minimum, Maximum,
    IsTemplate, Source

Mapping from LinkML:
    class             → template row: IsTemplate = True, DependsOn = slot list
    slot              → attribute row
    range: <Enum>     → Valid Values = comma-separated permissible_values
    range: date       → columnType = string, Format = date
    range: uri        → columnType = string, Format = uri
    range: integer    → columnType = number
    range: boolean    → columnType = boolean
    multivalued: true → columnType gets a "_list" suffix (string/boolean)
    pattern           → Pattern
    minimum_value/maximum_value → Minimum/Maximum

Two things this CSV cannot represent: "Required" is one column per attribute, so it
has no way to say a slot is required by one class but not another; and "Valid Values"
is a bare comma-joined string, so a permissible value containing a comma cannot be
round-tripped. create_json_from_model.py therefore reads `required` and the enum
values straight from the LinkML source rather than back out of this file.

Usage:
    python linkml_to_csv.py [--output namhub.model.csv]
"""

import argparse
import csv
import re
from pathlib import Path

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
            column_type, fmt = get_column_type(merged)

            rows.append({
                "Attribute": slot_name,
                "Description": normalise_text(merged.get("description", "")),
                "Valid Values": get_valid_values(merged, enum_lookup),
                "DependsOn": "",
                "Required": "True" if merged.get("required") else "False",
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


def main():
    parser = argparse.ArgumentParser(description="Convert LinkML schemas to a Curator-compatible CSV.")
    parser.add_argument("--output", default="namhub.model.csv")
    parser.add_argument("--schema", default=str(SCHEMA_DIR / "namhub.yaml"))
    parser.add_argument("--enums", default=str(SCHEMA_DIR / "enums.yaml"))
    args = parser.parse_args()

    namhub_schema = load_yaml(Path(args.schema))
    enums_schema = load_yaml(Path(args.enums))

    rows = convert_curator(namhub_schema, enums_schema)

    with open(args.output, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CURATOR_HEADERS)
        writer.writeheader()
        writer.writerows(rows)

    templates = sum(1 for r in rows if r["IsTemplate"] == "True")
    slots = len(rows) - templates
    print(f"Wrote {len(rows)} rows ({templates} templates, {slots} slots) → {args.output}")


if __name__ == "__main__":
    main()
