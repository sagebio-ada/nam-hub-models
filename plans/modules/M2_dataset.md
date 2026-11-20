# M2 assay and dataset: Assay and NAMPortalDataset

**Decisions (README section 4):** D4, D11, D25a, D26, D27, D33, D34, D39, D40

## Scope

1. Add the `Assay` record (D34). One Assay is one planned data contribution
   of one Study that realizes one NAM.
2. Make `NAMPortalDataset` the only dataset record (D39). Retire the
   `Datasets` table.
3. Make the dataset record hold the FAIR fields once (M0 FAIR field map).

`NAMPortalDataset` is the set of annotations on the Synapse Dataset entity.
Every dataset has a Synapse Dataset entity, external datasets too. The
`dataset_id` links of other records (files, assessment results, in silico
models) name this entity.

## Starting point

`Datasets` (syn75404713) has these slots: `dataset_id` (Synapse Dataset ID,
pattern `^syn\d+$`, blank for external datasets), `title`, `description`,
`study_id`, `study_name`, `assay`, `data_type`, `species`, `format`,
`repository`, `external_link`, `doi`, `release_date`, `dataset_item_count`,
`dataset_size_in_bytes`, `has_croissant_metadata`, `croissant_metadata_url`,
`access_type`, `nam_id` (multivalued).

`NAMPortalDataset` has the NF-OSI PortalDataset fields, with NAMHub
vocabularies:

- `nam_id`, `study_id`, `creator` (required), `funder` (`FunderEnum`).
- `license` (`LicenseEnum`, required) and `data_use_modifiers`
  (`DataUseModifierEnum`).
- `hosting` (Synapse, external cloud, external download, external access,
  mixed, unavailable), `repository`, `external_repository_uri` (a CURIE,
  for example `geo:GSE274451`) and `external_url`.
- `format` and `measurement_technique` are calculated from the files of the
  dataset.
- Its slots have `exact_mappings` or `close_mappings` to the equivalent
  `Datasets` slots. Example: `measurement_technique` = `assay`.

## Changes

One PR. The Curator output changes (major version: columns and a table are
removed).

### `Assay` (new; study-scoped `study_id` + `assay_id`)

The FUSION (NDHCC) LinkML model, version 1.2.0-wave2r4, has an Assay class
with the same meaning. `class_uri` `OBI:0000070`. Exact mappings:
`ndhcc:Assay` and `isa:assay`.

| Slot | Required | Range | Description | Anchor / FUSION slot |
|---|---|---|---|---|
| `study_id` | yes | key part; link → Studies | | `study` |
| `assay_id` | yes | key part | Study-scoped ID of the assay. | `source_identifier` |
| `assay_name` | yes | text | Name of the assay. | `title` |
| `description` | no | text | (existing slot) | `description` |
| `nam_id` | yes | link → NAMs | The NAM that the assay realizes. | `nam` (BFO realizes) |
| `context_of_use_id` | no | link → ContextOfUse | The context of use that the assay serves. | `context_of_use` |
| `assay` | yes | `AssayEnum` (existing slot; OBI `meaning`, D5) | The assay technology. Moved from Datasets. | `technology_type` |
| `species` | yes | `SpeciesEnum`, multivalued (existing slot) | Species of the material that the assay measures. Moved from Datasets. | `species` |
| `model_system_id` | no | multivalued; link → ModelSystem | The model system types that the assay runs on. | `runs_on` |
| `device_id` | no | multivalued; link → MicrophysiologicalDevice | The device types that the assay runs on. | `runs_on` |
| `landscape_id` | no | link → Landscape (existing slot) | The Landscape plan row that the assay fulfils. | Assay `landscape_id` |

The Assay has no protocol slot. Each Level 1 file and each Biospecimen row
names the protocol that made it (D24). The FUSION Assay `protocol_version`
slot has a close mapping to that `protocol_id`. The Assay has no slot for
the applicable standards or the contribution lead. The Assay reaches them
through `landscape_id`.

### `NAMPortalDataset` (the only dataset record)

Keep the current slots, with these changes:

| Change | Anchor (candidate) |
|---|---|
| Add `assay_id`. With `study_id`, it names the Assay. Required for data that a NAMHub study produced. Blank for external reference datasets. | FUSION Dataset `assay` |
| Add `dataset_processing_level`. Reuse the Landscape slot and its `ProcessLevelEnum`. A dataset holds data of one processing level. | FUSION `processing_level` |
| Add `dataset_item_count` and `dataset_size_in_bytes` (moved from `Datasets`). They are calculated from the files of the dataset, as `format` is. | FUSION `dataset_item_count`, `dataset_size_in_bytes` |
| Remove `nam_id` and `species`. The dataset reaches them through `assay_id` (D27). `measurement_technique` stays (calculated from the files). | — |
| Remove `funder`. The dataset reaches it through `study_id` → Studies `grant_id` → Grants `funding_agency`. | — |
| Remove `disease_focus`. The dataset reaches it through `study_id` → Studies `disease_focus`. | — |
| Keep `study_id`. It is part of the Assay key. | — |

Mappings: `date_published` → FUSION `release_date`. `external_url` →
FUSION `external_locator`. `croissant_file_s3_object` → FUSION
`croissant_metadata_url` (close).

### Retire `Datasets` (D39)

Retire the `Datasets` table (syn75404713). Alternatively, keep it as a
portal view that a process generates from the Dataset entities. Do this
only after the portal-page check (Assumptions).

These `Datasets` fields are not carried over:

- `dataset_id`: the Synapse Dataset entity ID is the key.
- `study_name`: repeats Studies (D27).
- `assay`, `species`, `nam_id`: reached through `assay_id`.
- `external_link`: the same as `external_url`.
- `release_date`: the same as `date_published`.
- `has_croissant_metadata`: derived from the Croissant file, never stored.
- `croissant_metadata_url`: the same as `croissant_file_s3_object`.
- `title`, `description`, `study_id`, `data_type`, `format`, `repository`,
  `doi`, `access_type`: `NAMPortalDataset` holds them already.

Every `dataset_id` link (files, `AssessmentResult` evidence, `InSilicoModel`
dataset links) names the Synapse Dataset entity, that is, the
`NAMPortalDataset` record.

Comparator data is not a slot of the dataset record. `CredibilityEvidence`
records it (D40, M9).

The dataset FAIR fields need no other new columns. `NAMPortalDataset`
holds `license` and `creator`. Studies holds the grant and the metadata
licence (D28). Investigation holds the institution (M1). People holds the
contact. The M0 FAIR field map gives each field and its key path.

File membership comes from `File.dataset_id` (M10). C2M2:
`file_in_collection`.

### FUSION mapping

`NAMPortalDataset` → `ndhcc:Dataset` (exact). `Assay` → `ndhcc:Assay`
(exact).

## Checks

- The checks in README section 2.
- The Curator diff shows only these changes:
  - The new `Assay` template.
  - `NAMPortalDataset` gains `assay_id`, `dataset_processing_level`,
    `dataset_item_count` and `dataset_size_in_bytes`.
  - `NAMPortalDataset` loses `nam_id`, `species`, `funder` and
    `disease_focus`.
  - The `Datasets` table is retired.
- The `assay` value of a file equals the `assay` of the Assay that the file
  reaches through `dataset_id` and `assay_id`.

## Assumptions

1. Every dataset that a portal page lists has, or gets, a Synapse Dataset
   entity with `NAMPortalDataset` annotations. External datasets get an
   entity with `hosting` set to an external value.
2. Before the PR, check which portal pages and processes read
   syn75404713 and its columns `nam_id`, `assay` and `species`. Do not
   retire the table before this check.

## Open questions

None. D39 resolves the earlier questions. Every dataset, external datasets
too, gets a Synapse Dataset entity. `NAMPortalDataset` is the only dataset
record.
