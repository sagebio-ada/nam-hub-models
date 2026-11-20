# M2 dataset: Datasets and NAMPortalDataset

**Decisions (README section 4):** D4, D11, D20, D25a, D26, D27

## Scope

1. Record which reference datasets a NAM dataset is compared with.
2. Make the dataset record hold the FAIR fields once (M0 FAIR field map).

`Datasets` (syn75404713) and `NAMPortalDataset` (annotations on the Synapse
Dataset entity) both describe datasets. They stay separate templates (open
question 2). New dataset fields go on `NAMPortalDataset` only. A `Datasets`
row reaches them through `dataset_id`, which is the ID of the same Synapse
Dataset entity (D27).

## Starting point

`Datasets` has these slots: `dataset_id` (Synapse Dataset ID, pattern
`^syn\d+$`, blank for external datasets), `title`, `description`,
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

One PR. The Curator output changes (minor version: one optional column).

| Change | Anchor (candidate) |
|---|---|
| Add `comparator_dataset_id` (multivalued) to `NAMPortalDataset`. It names the reference datasets that the NAM results of this dataset are compared with, for example patient tissue. It accepts a Synapse ID, a CURIE (for example `geo:GSE274451`) or a URL, so it can point to an external dataset. | No standard predicate for "compared with". Search OLS for an RO or OBI comparison relation. If none exists, use `see_also` to FDA NAM guidance section D (comparator performance) and log it as NAMHub-minted. |

The dataset FAIR fields need no new columns. `NAMPortalDataset` holds
`license` and `creator`. Studies holds the grant, the institution and the
metadata licence (D28). People holds the contact. The M0 FAIR
field map gives each field and its key path.

File membership comes from `File.dataset_id` (M10). C2M2:
`file_in_collection`.

## Checks

- The checks in README section 2.
- The Curator diff shows only one change: `NAMPortalDataset` gains
  `comparator_dataset_id`.

## Assumptions

1. A `Datasets` row and the `NAMPortalDataset` annotations of the same
   dataset have the same Synapse Dataset ID (`dataset_id` and the entity
   ID).

## Open questions

1. External datasets (for example GEO) have a blank `dataset_id` in
   `Datasets` and have no `NAMPortalDataset` annotations. Thus they have no
   FAIR fields. Options:
   - (a) Make a Synapse Dataset entity for every external dataset, with
     `NAMPortalDataset` annotations. `hosting` already has values for
     external data. Then every dataset has a Synapse ID and one record.
   - (b) Allow the external accession (for example GSE…) or a DOI as
     `dataset_id` for external rows, and add the FAIR fields to `Datasets`.
   - (c) Keep `dataset_id` blank for external rows. Add
     `external_repository_uri` to `Datasets` as the ID of the external
     dataset.

   `comparator_dataset_id` works with all three options.

   Recommendation: (a). Every dataset then has one record that holds its
   FAIR fields, and no field is stored twice (D27).
2. `Datasets` and `NAMPortalDataset` hold the same values for a dataset:
   `title`, `description`, `study_id`, `nam_id`, `assay` and
   `measurement_technique`, `data_type`, `species`, `format`, `doi`,
   `access_type`, `repository`, and the external link. The PR #22 review
   kept them separate. D27 asks for one record for each dataset. Options:
   - (a) Keep both. New fields go on `NAMPortalDataset` only (this plan).
   - (b) Make `NAMPortalDataset` the only dataset record. Reduce the
     `Datasets` table to `dataset_id` and the fields that
     `NAMPortalDataset` does not have, or retire it. This changes the live
     table syn75404713.

   Recommendation: (b), after a check of which portal pages and processes
   read syn75404713.
3. `Datasets.study_name` repeats `Studies.study_name`, which `study_id`
   reaches. Remove it from `Datasets` (D27)? This changes the live table.
