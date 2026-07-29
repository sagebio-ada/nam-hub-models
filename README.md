# NAMHub Data Models

This repository holds the canonical data models implemented in [NAMHub](https://namhub.synapse.org/), the NAMs Data Hub and Coordinating Center for the [NIH Complement-ARIE program](https://commonfund.nih.gov/complementarie). It also stores and automates data management operations associated with deploying these models across the Synapse ecosystem.

* **`/portal_schemas`** holds the YAML files defining all components of the NAMHub data model. These files are used to generate all derivative formats for this information, including **Curator** and **auto-generated documentation**.

## Setup

This repository (loosely) follows the [LinkML conventional environment](https://github.com/linkml/linkml-project-copier). The only prerequesite is **`uv`, a Python package manager and environment management tool**. [Installing this](https://docs.astral.sh/uv/getting-started/installation/) locally should enable all other dependencies to be managed automatically. The `sync` command pulls dependencies from `pyproject.toml`:

```sh
git clone git@github.com:sagebio-ada/nam-hub-models.git
cd nam-num-models
uv sync
# TODO: Add note about how to activate environment if needed
```

One dependency installed here is `just`, a command runner in the `make` tradition. There are many [installation options](https://github.com/casey/just#installation) if you want the tool available outside of this repo, but **it will be downloaded automatically within the project's environment.**

## Development

### Data model

| Command | Consequence |
| --- | --- |
| `just lint` | Reports LinkML lint findings. |
| `just gen-model` | Rewrites `namhub.model.csv` and the seven schemas in `json_schemas/` from the LinkML sources in `portal_schemas/`. |

### Documentation

Templates can be edited in `docs/templates-limkml`. If the template you need to modify isn't already there, the defaults can be found in [the LinkML repository](https://github.com/linkml/linkml/tree/main/packages/linkml/src/linkml/generators/docgen/).

| Command | Consequence |
| --- | --- |
| `just installdocs` | Re-runs `uv sync` to include dependencies for generating and deploying documentation |
| `just gen-doc` | Regenerates `docs/elements/` and the merged schema at `docs/schema/namhub.yaml`. |
| `just testdoc` | Rebuilds the docs, then serves them at http://127.0.0.1:8000 until interrupted. |


### Housekeeping

| Command | Consequence |
| --- | --- |
| `just install` | Syncs dev dependencies into `.venv`. |
| `just update` | Upgrades `linkml` and `linkml-runtime` in `uv.lock`. |
| `just clean` | Everything `clean-generated` does, plus `docs/elements/*.md`. |

### Helpers

These will generally not need to be run directly, but are available as utilities.

| Command | Consequence |
| --- | --- |
| `just gen-csv` | Rewrites `namhub.model.csv` from the LinkML sources in `portal_schemas/`. |
| `just gen-json` | Rewrites the seven schemas in `json_schemas/` from `namhub.model.csv`. |
| `just clean-generated` | **Deletes** `namhub.model.csv` and `json_schemas/*.json`. |
