"""Generate JSON Schema files from namhub.model.csv using Curator.

Run after linkml_to_csv.py has regenerated the CSV from LinkML sources.
"""

import os
from synapseclient import Synapse
from synapseclient.extensions.curator import generate_jsonschema

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

syn = Synapse()
syn.login()

schemas, file_paths = generate_jsonschema(
    data_model_source=DATA_MODEL_SOURCE,
    output=OUTPUT_DIRECTORY,
    data_types=DATA_TYPES,
    synapse_client=syn,
)
