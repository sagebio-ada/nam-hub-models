# nam-hub-models

LinkML data models for NAMHub curation: the Synapse portal tables and the Landscape data
collection form.

## Repository structure

* [src/namhub/schema/](src/namhub/schema) - the LinkML schema
  * `namhub.yaml` - classes and slots
  * `enums.yaml` - shared enumerations, imported by `namhub.yaml`

Everything else is derived from those two files by
[linkml-to-curator](https://github.com/sagebio-ada/linkml-to-curator).

## Working with the schema

Recipes are run with [just](https://github.com/casey/just/) and
[uv](https://docs.astral.sh/uv/). `just` alone lists them.

```bash
just install          # install dependencies
just test             # run linkml-lint and curator-lint
just lint             # linkml-lint alone, with the rules in .linkmllint.yaml
just gen-curator      # write one Curator JSON schema per class to project/curator
just register-curator NAMhub --dry-run   # have Synapse validate the generated schemas
just register-curator NAMhub             # register them under the model's version
```

Registration names the Synapse organization explicitly, reads a token from
`SYNAPSE_AUTH_TOKEN` or `~/.synapseConfig`, and refuses to reuse a version.

CI runs `just test` and `just gen-curator` on every pull request.

## Releasing

The generated Curator JSON schemas are release artifacts, attached to GitHub releases rather than tracked in git. Every push to main replaces the `latest` release, which the repository homepage shows, with schemas generated from that commit.

1. Bump `version:` in `namhub.yaml` and merge to main.
2. Check the schemas with `just register-curator NAMhub --dry-run`.
3. Publish a GitHub release from main tagged `v` plus that version, such as `v3.0.0`. The release workflow checks the tag against `version:`, runs the tests, and attaches one JSON schema per class to the release.
4. Register the same version with Synapse: `just register-curator NAMhub`.

Main's schemas are at `https://github.com/sagebio-ada/nam-hub-models/releases/latest/download/<Class>.json`, and a version's at `.../releases/download/v3.0.0/<Class>.json`.
