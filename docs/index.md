# NAMHub Data Models Explorer

**Welcome!** This site documents the data schemas behind [NAMHub](https://namhub.synapse.org/), a Synapse-hosted portal for cataloging New Approach Methods (NAMs) and the studies, datasets, and publications associated with them.

The schemas are defined in [LinkML](https://linkml.io/) at `portal_schemas/namhub.yaml` and `portal_schemas/enums.yaml`, and back the portal's Synapse tables (project [syn74360399](https://www.synapse.org/Synapse:syn74360399)) as well as the Landscape data collection form used by Technology Development Center (TDC) teams. NAM type classification uses the [New Approach Methods Ontology (NAMO)](https://github.com/monarch-initiative/namo), developed by the Monarch Initiative.

## Data Model

| Table | Description |
|---|---|
| **Landscape** | Preliminary information about datasets intended to be shared through NAM Hub, used by TDC teams to declare expected data uploads. |
| **Studies** | One row per TDC study in the NAMHub program. |
| **Datasets** | One row per dataset — Synapse-hosted or external (e.g. GEO) — linked to Studies and NAMs. |
| **People** | Investigators and contributors associated with NAMHub studies. |
| **Grants** | Backend grant records linked to Studies. |
| **NAMs** | One row per New Approach Method, classified using NAMO. |
| **Publications** | Publications associated with NAMHub studies, grants, or NAMs. |

Use the navigation above to browse the full field reference for each table, or look up controlled-vocabulary terms under **Standard Terms**.

## Found an Error?

If you notice any issues with the schemas or documentation, please [open an issue](https://github.com/sagebio-ada/nam-hub-models/issues).
