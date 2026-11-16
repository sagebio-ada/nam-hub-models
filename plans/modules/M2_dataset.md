# M2 dataset: Datasets and NAMPortalDataset

**Decisions:** D4, D11, D20, D25a

- D4 and D11: Keep `dataset_id`.
- D20: Add `comparator_dataset_id`.
- PR #22 review, PR22-1: keep `Datasets` and the PR #22 `NAMPortalDataset` as separate templates. Mark their equivalent slots.

## Scope

1. Make `Datasets` (syn75404713) and `NAMPortalDataset` (annotations on the Synapse Dataset entity) into C2M2 `collection` records with FAIR record metadata.
2. Record which reference dataset a NAM dataset is compared with.

The two templates stay separate. A later PR can merge them.

## Starting point

`Datasets` has these slots: `dataset_id` (Synapse Dataset ID, pattern `^syn\d+$`, blank for external datasets), `title`, `description`, `study_id`, `study_name`, `assay`, `data_type`, `species`, `format`, `repository`, `external_link`, `doi`, `release_date`, `dataset_item_count`, `dataset_size_in_bytes`, `has_croissant_metadata`, `croissant_metadata_url`, `access_type`, `nam_id`.

`NAMPortalDataset` (PR #22) has the NF-OSI PortalDataset fields, with NAMHub vocabularies. After the review fixes (M0, "Fixed in PR #18 and PR #22"):

- It has `nam_id`.
- `license` uses `LicenseEnum`.
- `data_use_modifiers` uses `DataUseModifierEnum`.
- Its slots have `exact_mappings` or `close_mappings` to the equivalent `Datasets` slots. Example: `measurement_technique` = `assay`.

## Changes

One PR, after M0 PR 3.

| Change | Anchor (candidate) |
|---|---|
| Apply `PublishedRecord` to both templates. It adds licence, metadata licence, landing page, access URL, access protocol, creator, contact and ROR. `NAMPortalDataset` already has `license` and `creator`. The mixin reuses those slots, so it adds only the missing fields. | FAIRshake metrics 7 to 9 and 16 to 18; schema.org `Dataset` properties |
| Add `comparator_dataset_id` (multivalued) to both templates. It names the reference datasets that the NAM results of this dataset are compared with. An example is patient tissue. Like `parent_file_id` (PR18-5), it accepts a Synapse ID, a CURIE (for example `geo:GSE274451`) or a URL. It can point to an external dataset. | No standard predicate for "compared with". Search OLS for an RO or OBI comparison relation. If none exists, use `see_also` to FDA NAM guidance section D (comparator performance) and log it as NAMHub-minted. |
| File membership comes from `File.dataset_id` (M10). | C2M2 `file_in_collection` |

M0 PR 2 anchors the existing slots. Examples: `title` → `dcterms:title`, `doi`, `release_date` → `schema:datePublished`, `species` → NCBITaxon, `format` → EDAM.

## Checks

- The checks in README section 2.
- The Datasets Curator JSON gains the `PublishedRecord` columns and `comparator_dataset_id`.

## Assumptions

1. `license` is required on Datasets (M0 open question 1). Everything else that this module adds is optional.

## Open questions

External datasets (for example GEO) have a blank `dataset_id`. C2M2 requires an ID for every collection. Options:

- (a) Make a Synapse Dataset entity for every external dataset. Then every row has a Synapse ID. This fits the rule that Synapse makes the IDs.
- (b) Allow the external accession (for example GSE…) or a DOI as `dataset_id` for external rows.
- (c) Keep `dataset_id` as a Synapse ID, blank for external rows. Use the PR #22 `external_repository_uri` (a CURIE, for example `geo:GSE274451`) as the ID of the external dataset.

`comparator_dataset_id` works with all three options. It accepts a Synapse ID, a CURIE or a URL (PR18-5 rule).

Recommendation: (c). It uses fields that exist. Keys stay Synapse IDs (D25a).
