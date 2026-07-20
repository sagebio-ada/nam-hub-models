CSV     := namhub.model.csv
SCHEMAS := portal_schemas/namhub.yaml portal_schemas/enums.yaml

all: generate-csv generate-json

# Convert LinkML portal_schemas/ → schematic-compatible CSV
generate-csv: $(SCHEMAS)
	@echo "Converting LinkML schemas to schematic CSV..."
	python linkml_to_csv.py --output $(CSV)

# Generate JSON Schema from the CSV via synapseclient curator
generate-json: $(CSV)
	@echo "Generating JSON schemas..."
	python create_json_from_model.py

clean:
	rm -f $(CSV)
	rm -f json_schemas/Studies.json json_schemas/Datasets.json json_schemas/People.json \
	       json_schemas/Grants.json json_schemas/NAMs.json json_schemas/Publications.json \
	       json_schemas/Landscape.json

.PHONY: all generate-csv generate-json clean
