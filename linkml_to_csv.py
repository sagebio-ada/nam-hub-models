"""Convert NAMHub LinkML schemas to a schematic-compatible CSV data model.

Reads portal_schemas/namhub.yaml and portal_schemas/enums.yaml and writes
namhub.model.csv in the format expected by the Synapse Data Curator /
schematic (CSV or JSON-LD only; YAML not supported).

Usage:
    python linkml_to_csv.py [--output namhub.model.csv]

Mapping:
    LinkML class       → IsTemplate=TRUE row; Properties = slot list
    LinkML slot        → attribute row with columnType, Valid Values, etc.
    LinkML enum range  → Valid Values (comma-separated permissible_values)
    multivalued: true  → columnType = string_list
    required: true     → Required = TRUE
    pattern:           → Pattern column
"""

import argparse
import csv
import re
import sys
from pathlib import Path

import yaml

SCHEMA_DIR = Path("portal_schemas")
HEADERS = [
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
    """Collapse whitespace/newlines from multi-line YAML strings."""
    if not s:
        return ""
    return re.sub(r"\s+", " ", s).strip()


def build_enum_lookup(enums_schema: dict, namhub_schema: dict) -> dict[str, list[str]]:
    """Return {enum_name: [permissible_value, ...]} from both schema files."""
    lookup: dict[str, list[str]] = {}
    for schema in (enums_schema, namhub_schema):
        for name, defn in (schema.get("enums") or {}).items():
            pv = defn.get("permissible_values") or {}
            lookup[name] = list(pv.keys())
    return lookup


def linkml_range_to_col_type(slot_def: dict, enum_lookup: dict) -> tuple[str, str]:
    """Return (columnType, format) for a slot definition."""
    range_ = slot_def.get("range", "string")
    multivalued = slot_def.get("multivalued", False)

    if range_ == "integer":
        return ("int", "")
    if range_ == "boolean":
        return ("boolean", "")
    if range_ == "date":
        return ("date", "date")
    if range_ in ("float", "double"):
        return ("float", "")
    # uri → plain string in schematic
    if multivalued or range_ in enum_lookup and multivalued:
        return ("string_list", "")
    # enum ranges that are multivalued are handled above; single-value enums → string
    return ("string", "")


def get_valid_values(slot_def: dict, enum_lookup: dict) -> str:
    range_ = slot_def.get("range", "string")
    if range_ in enum_lookup:
        return ", ".join(enum_lookup[range_])
    return ""


def is_required(slot_name: str, slot_def: dict, slot_usages: list[dict]) -> str:
    """Return 'TRUE' if the slot is required in the base definition or any class."""
    if slot_def.get("required"):
        return "TRUE"
    for usage in slot_usages:
        if usage.get("required"):
            return "TRUE"
    return ""


# ── Main conversion ────────────────────────────────────────────────────────────

def convert(namhub_schema: dict, enums_schema: dict) -> list[dict]:
    enum_lookup = build_enum_lookup(enums_schema, namhub_schema)
    all_slots: dict[str, dict] = namhub_schema.get("slots") or {}
    all_classes: dict[str, dict] = namhub_schema.get("classes") or {}

    rows: list[dict] = []
    emitted_slots: set[str] = set()

    for class_name, class_def in all_classes.items():
        class_slots: list[str] = class_def.get("slots") or []
        slot_usage_map: dict[str, dict] = class_def.get("slot_usage") or {}

        # Template row
        rows.append({
            "Attribute": class_name,
            "Description": normalise_text(class_def.get("description", "")),
            "Valid Values": "",
            "DependsOn": "",
            "Required": "",
            "Properties": ", ".join(class_slots),
            "Validation Rules": "",
            "columnType": "",
            "Format": "",
            "Pattern": "",
            "Minimum": "",
            "Maximum": "",
            "IsTemplate": "TRUE",
            "Source": "",
        })

        # Slot rows (emit each slot only once globally)
        for slot_name in class_slots:
            if slot_name in emitted_slots:
                continue
            emitted_slots.add(slot_name)

            base_def = dict(all_slots.get(slot_name) or {})
            usage = dict(slot_usage_map.get(slot_name) or {})

            # Collect slot_usage for this slot across all classes for required check
            all_usages = [
                (c.get("slot_usage") or {}).get(slot_name, {})
                for c in all_classes.values()
            ]

            # Merge: slot_usage overrides base for range/multivalued
            merged = {**base_def, **usage}

            col_type, fmt = linkml_range_to_col_type(merged, enum_lookup)
            valid_vals = get_valid_values(merged, enum_lookup)
            required = is_required(slot_name, merged, all_usages)
            pattern = merged.get("pattern", "")
            desc = normalise_text(merged.get("description", base_def.get("description", "")))

            rows.append({
                "Attribute": slot_name,
                "Description": desc,
                "Valid Values": valid_vals,
                "DependsOn": "",
                "Required": required,
                "Properties": "",
                "Validation Rules": "",
                "columnType": col_type,
                "Format": fmt,
                "Pattern": pattern,
                "Minimum": "",
                "Maximum": "",
                "IsTemplate": "",
                "Source": "",
            })

    return rows


def main():
    parser = argparse.ArgumentParser(description="Convert LinkML schemas to schematic CSV.")
    parser.add_argument("--output", default="namhub.model.csv", help="Output CSV path.")
    parser.add_argument(
        "--schema", default=str(SCHEMA_DIR / "namhub.yaml"), help="Path to namhub.yaml."
    )
    parser.add_argument(
        "--enums", default=str(SCHEMA_DIR / "enums.yaml"), help="Path to enums.yaml."
    )
    args = parser.parse_args()

    namhub_schema = load_yaml(Path(args.schema))
    enums_schema = load_yaml(Path(args.enums))

    rows = convert(namhub_schema, enums_schema)

    with open(args.output, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=HEADERS)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {len(rows)} rows ({sum(1 for r in rows if r['IsTemplate'] == 'TRUE')} templates, "
          f"{sum(1 for r in rows if not r['IsTemplate'])} slots) → {args.output}")


if __name__ == "__main__":
    main()
