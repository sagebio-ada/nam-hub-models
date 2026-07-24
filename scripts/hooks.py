from os import makedirs
from os.path import isfile, join

import yaml

# --- Configuration ---

SCHEMA_DIR = "portal_schemas"
MODEL_FILE = join(SCHEMA_DIR, "namhub.yaml")
ENUMS_FILE = join(SCHEMA_DIR, "enums.yaml")

MODEL_DOCS_DIR = join("docs", "model")
TERMS_DOCS_DIR = join("docs", "valid_values")
NAVIGATION_FILENAME = "nav.yml"

# Class -> docs page filename (also drives the order pages are listed in).
CLASS_PAGES = {
    "Landscape": "landscape",
    "Studies": "studies",
    "Datasets": "datasets",
    "People": "people",
    "Grants": "grants",
    "NAMs": "nams",
    "Publications": "publications",
}

# Enum -> display title for the Standard Terms nav section.
ENUM_TITLES = {
    "AssayEnum": "Assay",
    "SpeciesEnum": "Species",
    "FileFormatEnum": "File Format",
    "DataCategoryEnum": "Data Category",
    "ProcessLevelEnum": "Process Level",
    "NamContextEnum": "NAM Context",
    "RepositoryEnum": "Repository",
    "AccessTypeEnum": "Access Type",
    "DevelopmentStatusEnum": "Development Status",
    "RoleEnum": "Role",
}

FIELD_COLUMNS = ["Attribute", "Description", "Required", "Multivalued", "Range", "Pattern"]
TERMS_COLUMNS = ["Value", "Description", "Ontology Term"]


# --- Helper functions ---
def _load_schema():
    with open(MODEL_FILE) as f:
        model = yaml.safe_load(f)
    with open(ENUMS_FILE) as f:
        enums = yaml.safe_load(f)
    return model, enums


def _render_table(rows, columns):
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join(["---"] * len(columns)) + " |"
    body = [
        "| " + " | ".join(str(row.get(c, "")).replace("|", "\\|") for c in columns) + " |"
        for row in rows
    ]
    return "\n".join([header, sep] + body)


def _expand_curie(curie, prefixes):
    """Expand a CURIE (e.g. "NCIT:C12345") into a full URL using the enums
    schema's own prefixes: block, which already includes the trailing
    separator (e.g. "NCIT: http://purl.obolibrary.org/obo/NCIT_")."""
    if not curie or ":" not in curie:
        return None
    prefix, local = curie.split(":", 1)
    base = prefixes.get(prefix)
    return base + local if base else None


def _slot_row(slot_name, slot_def, required, default_range, enums):
    range_ = slot_def.get("range") or default_range
    if range_ in enums.get("enums", {}):
        range_display = f"[{range_}](../valid_values/{range_}.md)"
    else:
        range_display = range_
    return {
        "Attribute": slot_name,
        "Description": (slot_def.get("description") or "").strip().replace("\n", " "),
        "Required": "True" if required else "False",
        "Multivalued": "True" if slot_def.get("multivalued") else "False",
        "Range": range_display,
        "Pattern": slot_def.get("pattern") or "_None_",
    }


# --- Core logic functions ---
def generate_model_pages(model, enums):
    """Generate one docs page per class, listing its slots as a field
    reference table (attribute, description, required, multivalued, range,
    pattern) sourced directly from portal_schemas/namhub.yaml."""
    global_slots = model.get("slots", {})
    default_range = model.get("default_range", "string")
    makedirs(MODEL_DOCS_DIR, exist_ok=True)

    for class_name, class_def in model.get("classes", {}).items():
        page_slug = CLASS_PAGES.get(class_name, class_name.lower())
        slot_usage = class_def.get("slot_usage") or {}

        rows = [
            _slot_row(
                slot_name,
                global_slots.get(slot_name, {}),
                (slot_usage.get(slot_name) or {}).get("required", False),
                default_range,
                enums,
            )
            for slot_name in class_def.get("slots", [])
        ]

        lines = [f"# {class_name}\n"]
        description = (class_def.get("description") or "").strip()
        if description:
            lines.append(description + "\n")
        see_also = class_def.get("see_also")
        if see_also:
            links = ", ".join(f"[{url}]({url})" for url in see_also)
            lines.append(f"**See also:** {links}\n")
        lines.append("## Field Reference\n")
        lines.append(_render_table(rows, FIELD_COLUMNS))
        lines.append("")

        with open(join(MODEL_DOCS_DIR, f"{page_slug}.md"), "w") as f:
            f.write("\n".join(lines))


def generate_enum_pages(enums):
    """Generate one docs page per enum, listing its permissible values as a
    standard-terms table (value, description, ontology term) sourced
    directly from portal_schemas/enums.yaml."""
    prefixes = enums.get("prefixes", {})
    makedirs(TERMS_DOCS_DIR, exist_ok=True)

    for enum_name, enum_def in enums.get("enums", {}).items():
        rows = []
        for value, value_def in (enum_def.get("permissible_values") or {}).items():
            value_def = value_def or {}
            meaning = value_def.get("meaning")
            url = _expand_curie(meaning, prefixes)
            if meaning and url:
                term_display = f"[{meaning}]({url})"
            else:
                term_display = meaning or "_None_"
            rows.append({
                "Value": value,
                "Description": (value_def.get("description") or "").strip().replace("\n", " "),
                "Ontology Term": term_display,
            })

        lines = [f"# {ENUM_TITLES.get(enum_name, enum_name)}\n"]
        description = (enum_def.get("description") or "").strip()
        if description:
            lines.append(description + "\n")
        lines.append('<div style="max-height:650px; overflow-x: hidden; overflow-y: auto;">\n')
        lines.append(_render_table(rows, TERMS_COLUMNS))
        lines.append("\n</div>\n")

        with open(join(TERMS_DOCS_DIR, f"{enum_name}.md"), "w") as f:
            f.write("\n".join(lines))


# --- MkDocs event hooks ---
def on_pre_build(config):
    """Generate the model reference pages and standard-terms pages from
    portal_schemas/ before the site is built."""
    model, enums = _load_schema()
    generate_model_pages(model, enums)
    generate_enum_pages(enums)


def on_files(files, config):
    """Rebuild config.nav from nav.yml, appending a Standard Terms entry for
    each enum page generated by generate_enum_pages()."""
    with open(NAVIGATION_FILENAME) as f:
        nav_mapping = yaml.safe_load(f)

    _, enums = _load_schema()
    nav_mapping["Standard Terms"] = [
        {ENUM_TITLES.get(enum_name, enum_name): join("valid_values", f"{enum_name}.md")}
        for enum_name in enums.get("enums", {})
        if isfile(join(TERMS_DOCS_DIR, f"{enum_name}.md"))
    ]

    config["nav"] = nav_mapping
    return files
