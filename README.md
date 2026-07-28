# NAMHub Data Models

Launching operations with `just`:

Run `just` with no arguments for the full list. The common operations:

**Generating artifacts**

| Command | Consequence |
| --- | --- |
| `just gen-model` | Rewrites the seven schemas in `json_schemas/` from the LinkML sources in `portal_schemas/`. |
| `just gen-doc` | Regenerates `docs/elements/` and the merged schema at `docs/schema/namhub.yaml`. |

**Checking your work**

| Command | Consequence |
| --- | --- |
| `just lint` | Reports LinkML lint findings. |
| `just testdoc` | Rebuilds the docs, then serves them at http://127.0.0.1:8000 until interrupted. |

**Housekeeping**

| Command | Consequence |
| --- | --- |
| `just install` | Syncs dev dependencies into `.venv`. |
| `just update` | Upgrades `linkml` and `linkml-runtime` in `uv.lock`. |
| `just clean-generated` | **Deletes** `namhub.model.csv` and `json_schemas/*.json`. |
| `just clean` | Everything `clean-generated` does, plus `docs/elements/*.md`. |
| `just deploy` | **Publishes** the documentation site to GitHub Pages. |

**Helpers**

| Command | Consequence |
| --- | --- |
| `just gen-csv` | Rewrites `namhub.model.csv` from the LinkML sources in `portal_schemas/`. |
| `just gen-json` | Rewrites the seven schemas in `json_schemas/` from `namhub.model.csv`. |


## Generate docs

Testing locally:

```
git clone git@github.com:sagebio-ada/nam-hub-models.git
uv sync
just gen-doc
just testdoc
```

http://127.0.0.1:8000/nam-hub-models/elements/datasetProcessingLevel/

### Editing

Templates can be edited in `docs/templates-limkml`. If the template you need to modify isn't already there, the defaults can be found in [the LinkML repository](https://github.com/linkml/linkml/tree/main/packages/linkml/src/linkml/generators/docgen/).
