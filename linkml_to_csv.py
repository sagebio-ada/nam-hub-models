"""Convert NAMHub LinkML schemas to a schematic-compatible CSV data model.

Reads portal_schemas/namhub.yaml and portal_schemas/enums.yaml and writes
namhub.model.csv in the format expected by schematic 25.x (schematicpy).

Required schematic headers (v25):
    Attribute, Description, Valid Values, DependsOn, DependsOn Component,
    Required, Parent, Validation Rules, Properties, Source

Mapping from LinkML:
    class             → template row: DependsOn = slot list, Parent = empty
    slot              → attribute row: Parent = all classes using it,
                        Required = TRUE if required in any class slot_usage
    multivalued: true → (informational; schematic uses Valid Values for arrays)
    range: <Enum>     → Valid Values = comma-separated permissible_values
    required: true    → Required = TRUE

Usage:
    python linkml_to_csv.py [--output namhub.model.csv]
"""

import argparse
import csv
import re
from pathlib import Path
from collections import defaultdict

import yaml

SCHEMA_DIR = Path("portal_schemas")

HEADERS = [
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


# ── Main conversion ────────────────────────────────────────────────────────────

def convert(namhub_schema: dict, enums_schema: dict) -> list[dict]:
    enum_lookup = build_enum_lookup(enums_schema, namhub_schema)
    all_slots: dict[str, dict] = namhub_schema.get("slots") or {}
    all_classes: dict[str, dict] = namhub_schema.get("classes") or {}

    # Build reverse map: slot_name → [class_name, ...]
    slot_parents: dict[str, list[str]] = defaultdict(list)
    for class_name, class_def in all_classes.items():
        for slot_name in (class_def.get("slots") or []):
            slot_parents[slot_name].append(class_name)

    # Build required map: slot_name → TRUE/FALSE
    # A slot is required if the base definition or any class slot_usage marks it required.
    slot_required: dict[str, str] = {}
    for slot_name, slot_def in all_slots.items():
        if slot_def.get("required"):
            slot_required[slot_name] = "TRUE"
    for class_def in all_classes.values():
        for slot_name, usage in (class_def.get("slot_usage") or {}).items():
            if usage.get("required"):
                slot_required[slot_name] = "TRUE"

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

            base_def = dict(all_slots.get(slot_name) or {})
            # Merge all slot_usage entries across classes for this slot
            merged = dict(base_def)
            for cd in all_classes.values():
                usage = (cd.get("slot_usage") or {}).get(slot_name, {})
                if usage:
                    merged.update(usage)

            desc = normalise_text(merged.get("description", ""))
            valid_vals = get_valid_values(merged, enum_lookup)
            required = slot_required.get(slot_name, "FALSE")
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


def main():
    parser = argparse.ArgumentParser(description="Convert LinkML schemas to schematic CSV.")
    parser.add_argument("--output", default="namhub.model.csv")
    parser.add_argument("--schema", default=str(SCHEMA_DIR / "namhub.yaml"))
    parser.add_argument("--enums", default=str(SCHEMA_DIR / "enums.yaml"))
    args = parser.parse_args()

    namhub_schema = load_yaml(Path(args.schema))
    enums_schema = load_yaml(Path(args.enums))

    rows = convert(namhub_schema, enums_schema)

    with open(args.output, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=HEADERS)
        writer.writeheader()
        writer.writerows(rows)

    templates = sum(1 for r in rows if not r["Parent"] and r["DependsOn"])
    slots = sum(1 for r in rows if r["Parent"])
    print(f"Wrote {len(rows)} rows ({templates} templates, {slots} slots) → {args.output}")


if __name__ == "__main__":
    main()
