CSV     := namhub.model.csv
SCHEMAS := portal_schemas/namhub.yaml portal_schemas/enums.yaml

# curator (default) or schematic — must match between the two steps, since
# each expects the CSV format the other produces.
FORMAT  := curator
ROUTE   := curator

all: generate-csv generate-json

# Convert LinkML portal_schemas/ → CSV data model (--format curator|schematic)
generate-csv: $(SCHEMAS)
	@if [ "$(FORMAT)" = "schematic" ]; then \
		python -c "import schematic" >/dev/null 2>&1 || { \
			echo "schematic (schematicpy) is not available in this environment — cannot use FORMAT=schematic. Activate an environment with schematicpy installed and try again." >&2; \
			exit 1; \
		}; \
	fi
	@echo "Converting LinkML schemas to CSV ($(FORMAT) format)..."
	python linkml_to_csv.py --format $(FORMAT) --output $(CSV)

# Generate JSON Schema from the CSV (--route curator|schematic)
generate-json: $(CSV)
	@if [ "$(ROUTE)" = "schematic" ]; then \
		python -c "import schematic" >/dev/null 2>&1 || { \
			echo "schematic (schematicpy) is not available in this environment — cannot use ROUTE=schematic. Activate an environment with schematicpy installed and try again." >&2; \
			exit 1; \
		}; \
	fi
	@echo "Generating JSON schemas ($(ROUTE) route)..."
	python create_json_from_model.py --route $(ROUTE)

clean:
	rm -f $(CSV)
	rm -f json_schemas/Studies.json json_schemas/Datasets.json json_schemas/People.json \
	       json_schemas/Grants.json json_schemas/NAMs.json json_schemas/Publications.json \
	       json_schemas/Landscape.json

.PHONY: all generate-csv generate-json clean
