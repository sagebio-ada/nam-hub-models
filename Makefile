CSV := namhub.model.csv
DATA := Landscape

all: collate generate-json

collate:
	@echo "Collating module components..."
	head -1 modules/dataLandscape/annotationProperty.csv > ${CSV}
	tail -n +2 -q modules/*/annotationProperty.csv >> ${CSV}

generate-json:
	python create_json_from_model.py