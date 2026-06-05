from synapseclient import Synapse
from synapseclient.extensions.curator import generate_jsonschema

DATA_MODEL_SOURCE = "namhub.model.csv"
DATA_TYPE = ["Landscape"]
OUTPUT_DIRECTORY = "./json_schemas"

syn = Synapse()
syn.login()

schemas, file_paths = generate_jsonschema(
    data_model_source=DATA_MODEL_SOURCE,
    output=OUTPUT_DIRECTORY,
    data_types=DATA_TYPE,
    synapse_client=syn,
)
