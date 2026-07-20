"""Generate JSON Schema files from namhub.model.csv using schematic.

Run after linkml_to_csv.py has regenerated the CSV from LinkML sources.
"""

import os
from schematic.schemas.data_model_parser import DataModelParser
from schematic.schemas.data_model_graph import DataModelGraph, DataModelGraphExplorer
from schematic.schemas.create_json_schema import create_json_schema

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

os.makedirs(OUTPUT_DIRECTORY, exist_ok=True)

print(f"Parsing {DATA_MODEL_SOURCE}...")
parser = DataModelParser(DATA_MODEL_SOURCE)
parsed = parser.parse_model()

print("Building graph...")
graph = DataModelGraph(parsed)
dmge = DataModelGraphExplorer(graph.graph)

print("Generating JSON schemas...")
for dt in DATA_TYPES:
    output_path = os.path.join(OUTPUT_DIRECTORY, f"{dt}.json")
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
