schema := "src/namhub/schema/namhub.yaml"
curator_dir := "project/curator"

# List recipes
_default:
  @just --list

# Install dependencies
install:
  uv sync --group dev

# Run all checks
test: lint lint-curator

# Run linkml-lint with the rules in .linkmllint.yaml
lint:
  uv run linkml-lint -c .linkmllint.yaml src/namhub/schema

# Check the model against what Curator and Synapse accept
lint-curator:
  uv run curator-lint {{schema}}

# Generate Synapse Curator JSON schemas, one per class
gen-curator:
  uv run gen-curator -d {{curator_dir}} {{schema}}

# Register the generated schemas with a Synapse organization. Pass --dry-run to validate only.
register-curator org *args:
  uv run curator-register {{curator_dir}} --org {{org}} --schema {{schema}} {{args}}

# Remove generated files
clean:
  rm -rf project
