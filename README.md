# NAMHub Data Models

This repository holds the canonical data models implemented in [NAMHub](https://namhub.synapse.org/), the NAMs Data Hub and Coordinating Center for the [NIH Complement-ARIE program](https://commonfund.nih.gov/complementarie). It also stores and automates data management operations associated with deploying these models across the Synapse ecosystem.

* **`/portal_schemas`** holds the YAML files defining all components of the NAMHub data model. These files are used to generate all derivative formats for this information, including **Curator** and **auto-generated documentation**.

## Setup

This repository (loosely) follows the [LinkML conventional environment](https://github.com/linkml/linkml-project-copier). The only prerequisite is **`uv`, a Python package manager and environment management tool**. [Installing this](https://docs.astral.sh/uv/getting-started/installation/) locally should enable all other dependencies to be managed automatically. The `sync` command pulls dependencies from `pyproject.toml`:

```sh
git clone git@github.com:sagebio-ada/nam-hub-models.git
cd nam-num-models
uv sync
# TODO: Add note about how to activate environment if needed
```

(If you're not using `uv`, Python >3.10 should also be able to run via `pip install .`)

One dependency installed here is `just`, a command runner in the `make` tradition. There are many [installation options](https://github.com/casey/just#installation) if you want the tool available outside of this repo, but **it will be downloaded automatically within the project's environment.**

### Dependencies

Running `uv sync` once will install what is needed to **edit and lint the schemas in `portal_schemas/`**. Other operations require heavier dependency chains and will be installed on-demand. See "Manual dependency installation" below.

## Development

### Data model

| Command | Consequence |
| --- | --- |
| `just lint` | Reports LinkML lint findings. |
| `just lint-py` | Reports `ruff` findings for the Python scripts and `tests/`. |
| `just test` | Lints the Python, then runs the integration tests in `tests/` — these regenerate the artifacts and validate the example corpus. |
| `just gen-model` | Rewrites `namhub.model.csv` and the seven schemas in `json_schemas/` from the LinkML sources in `portal_schemas/`. |

### Documentation

| Command | Consequence |
| --- | --- |
| `just installdocs` | Re-runs `uv sync` to include dependencies for generating and deploying documentation |
| `just gen-doc` | Regenerates `docs/elements/` and the merged schema at `docs/schema/namhub.yaml`. |
| `just testdoc` | Rebuilds the docs, then serves them at http://127.0.0.1:8000 until interrupted. |

### Housekeeping

| Command | Consequence |
| --- | --- |
| `just install` | Syncs dev dependencies into `.venv`. |
| `just clean` | Everything `clean-generated` does, plus `docs/elements/*.md`. |

### Helpers

These will generally not need to be run directly, but are available as utilities.

| Command | Consequence |
| --- | --- |
| `just gen-csv` | Rewrites `namhub.model.csv` from the LinkML sources in `portal_schemas/`. |
| `just gen-json` | Rewrites the seven schemas in `json_schemas/` from `namhub.model.csv`. |
| `just clean-generated` | **Deletes** `namhub.model.csv` and `json_schemas/*.json`. |

### Manual dependency installation
| Group | Install | Covers |
| --- | --- | --- |
| *(base)* | `just install` | Editing `portal_schemas/*.yaml`, `just lint`, `just gen-doc` |
| `docs` | `just installdocs` | Building and serving the documentation site (`just testdoc`) |
| `deploy` | `just installdeploy` | Generating the CSV model and portal JSON schemas (`just gen-model`) |
| `dev` | *(synced on demand)* | Linting and testing (`just lint-py`, `just test`) |
