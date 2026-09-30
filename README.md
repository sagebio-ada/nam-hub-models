# nam-hub-models

LinkML data models for NAMHub curation: the Synapse portal tables and the Landscape data
collection form.

## Repository structure

* [src/namhub/schema/](src/namhub/schema) - the LinkML schema
  * `namhub.yaml` - classes and slots
  * `enums.yaml` - shared enumerations, imported by `namhub.yaml`

Everything else is derived from those two files by
[linkml-curator](https://github.com/sagebio-ada/linkml-curator).

## Working with the schema

Recipes are run with [just](https://github.com/casey/just/) and
[uv](https://docs.astral.sh/uv/). `just` alone lists them.

```bash
just install          # install dependencies
just test             # run linkml-lint and curator-lint
just lint             # linkml-lint alone
just gen-curator      # write one Curator JSON schema per class to project/curator
just register-curator NAMhub --dry-run   # have Synapse validate the generated schemas
just register-curator NAMhub             # register them under the model's version
```

Registration names the Synapse organization explicitly, reads a token from
`SYNAPSE_AUTH_TOKEN` or `~/.synapseConfig`, and refuses to reuse a version, so a release
starts with a bump of `version:` in `namhub.yaml`.

CI runs `just test` on every pull request.
