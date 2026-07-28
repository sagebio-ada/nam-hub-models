# ============ Shell configuration for Windows ============

# On Windows the "bash" shell from Git for Windows is used.
# If Git is installed in a non-standard location, edit the path below.
set windows-shell := ["C:/Program Files/Git/bin/bash", "-cu"]

# ============ Variables used in recipes ============

# Load environment variables from config.public.mk or specified file
set dotenv-load := true
set dotenv-filename := x'${LINKML_ENVIRONMENT_FILENAME:-config.public.mk}'

# Environment variables with defaults
schema_name := env_var_or_default("LINKML_SCHEMA_NAME", "_no_schema_given_")
source_schema_dir := env_var_or_default("LINKML_SCHEMA_SOURCE_DIR", "")
gen_doc_args := env_var_or_default("LINKML_GENERATORS_DOC_ARGS", "")

# Directory variables
source_schema_path := source_schema_dir / schema_name + ".yaml"
docdir := "docs/elements"  # Directory for generated documentation
distrib_schema_path := "docs/schema"  # Directory for publishing schema artifacts

# Portal data model artifacts (see gen-model)
model_csv := "namhub.model.csv"  # Intermediate CSV data model
json_schema_dir := "json_schemas"  # Directory for generated portal JSON schemas
# Must stay in sync with DATA_TYPES in create_json_from_model.py
json_schema_names := "Landscape Studies Datasets People Grants NAMs Publications"

# ============== Project recipes ==============

# List all commands as default command. The prefix "_" hides the command.
_default: _status
    @just --list

# Install project dependencies
[group('project management')]
install:
  uv sync --group dev

# Upgrade LinkML runtime and LinkML to the latest versions
[group('project management')]
update:
  uv lock --upgrade-package linkml-runtime --upgrade-package linkml

# Clean all generated files
[group('project management')]
clean: clean-generated
  rm -rf {{docdir}}/*.md

# Remove the generated CSV data model and portal JSON schemas
[group('project management')]
clean-generated:
  rm -f {{model_csv}}
  rm -f {{ prepend(json_schema_dir / "", append(".json", json_schema_names)) }}

# Run linting
[group('model development')]
lint:
  uv run linkml-lint {{source_schema_dir}}

# Generate md documentation for the schema
[group('model development')]
gen-doc: _gen-yaml
  uv run gen-doc {{gen_doc_args}} -d {{docdir}} {{source_schema_path}}

# Build the docs and run a local preview server
[group('model development')]
testdoc: gen-doc _serve

# Regenerate the CSV data model and the portal JSON schemas
[group('model development')]
gen-model: gen-csv gen-json

# Convert the LinkML schemas to the CSV data model
[group('model development')]
gen-csv:
  uv run python linkml_to_csv.py \
    --schema {{source_schema_path}} \
    --enums {{ source_schema_dir / "enums.yaml" }} \
    --output {{model_csv}}

# Generate the portal JSON schemas from the CSV data model
[group('model development')]
gen-json:
  uv run python create_json_from_model.py \
    --source {{model_csv}} \
    --output {{json_schema_dir}}

# Deploy documentation site to Github Pages
[group('deployment')]
deploy: gen-doc
  mkd-gh-deploy # NOTE: This doesn't currently work and probably won't

# ============== Hidden internal recipes ==============

# Show current project status
_status: _check-config
  @echo "Project: {{schema_name}}"
  @echo "Source: {{source_schema_path}}"

# Fail early if the schema name is not configured
_check-config:
  @if [ -z "${LINKML_SCHEMA_NAME:-}" ]; then \
    echo "**Project not configured**: see 'config.public.mk'"; \
    exit 1; \
  fi

# Add the merged model to docs/schema.
_gen-yaml:
  -mkdir -p {{distrib_schema_path}}
  uv run gen-yaml {{source_schema_path}} > {{distrib_schema_path}}/{{schema_name}}.yaml

# Run documentation server
_serve:
  uv run mkdocs serve
