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

# Confluence publishing. These recipes publish the docs that `just gen-doc` already
# wrote, rather than having the publisher regenerate them.
confluence_source := "--elements " + docdir

confluence_config := env_var_or_default("CONFLUENCE_CONFIG", "")
confluence_args := if confluence_config != "" { "--config " + confluence_config } else { "" }

# Portal data model artifacts (see gen-model)
model_csv := "namhub.model.csv"  # Intermediate CSV data model
json_schema_dir := "json_schemas"  # Directory for generated portal JSON schemas
# Must stay in sync with DATA_TYPES in create_json_from_model.py
json_schema_names := "Landscape Studies Datasets People Grants NAMs Publications"

# ============== Project recipes ==============

# List all commands as default command. The prefix "_" hides the command.
_default: _status
    @just --list

# Install the base dependencies needed to edit the schemas and run `just lint`
[group('project management')]
install:
  uv sync

# Add the documentation toolchain on top of the base dependencies
[group('project management')]
installdocs:
  uv sync --group docs

# Add the schema deployment toolchain on top of the base dependencies
[group('project management')]
installdeploy:
  uv sync --group deploy

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

# Move the pinned confluence-publish-linkml commit up to the head of main
[group('confluence')]
confluence-update:
  uv lock --upgrade-package confluence-publish-linkml
  uv sync --group confluence

# Show the Confluence page tree that would be published. Needs no credentials.
[group('confluence')]
confluence-plan: confluence-update gen-doc
  uv run --group confluence python -m confluence_publish_linkml --print-plan {{confluence_source}}

# Report what publishing would change, without writing anything to Confluence
[group('confluence')]
confluence-diff: confluence-update gen-doc
  uv run --group confluence python -m confluence_publish_linkml --dry-run {{confluence_source}} {{confluence_args}}

# Publish the docs to Confluence. Creates and updates real pages; never deletes.
[group('confluence')]
confluence-publish: confluence-update gen-doc
  uv run --group confluence python -m confluence_publish_linkml {{confluence_source}} {{confluence_args}}

# Rebuild the local page-id cache from Confluence, then publish
[group('confluence')]
confluence-republish: confluence-update gen-doc
  uv run --group confluence python -m confluence_publish_linkml --refresh {{confluence_source}} {{confluence_args}}

# Regenerate the CSV data model and the portal JSON schemas
[group('model development')]
gen-model: gen-csv gen-json

# Convert the LinkML schemas to the CSV data model
[group('model development')]
gen-csv:
  uv run --group deploy python linkml_to_csv.py \
    --schema {{source_schema_path}} \
    --enums {{ source_schema_dir / "enums.yaml" }} \
    --output {{model_csv}}

# Generate the portal JSON schemas from the CSV data model
[group('model development')]
gen-json:
  uv run --group deploy python create_json_from_model.py \
    --source {{model_csv}} \
    --output {{json_schema_dir}}

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
  uv run --group docs mkdocs serve
