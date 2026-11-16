# M3 nam: NAM catalog

**Decisions:** D2 (NAMs is the catalog; instances are Biospecimen rows or
`InSilicoModel` records), D4, D7 (NAMO by `exact_mappings` at a pinned
commit), D11 (`nam_id` is global), D16 (risk levels, in M9). One slot waits
for D24.

## Scope

Reshape `NAMs` (syn75404716) to do three things:

1. Classify each NAM with standard terms.
2. Add the method-level fields of the FDA NAM guidance (sections B and C).
3. Link each NAM to related NAMs.

## Starting point

`NAMs` has these slots: `nam_id`, `nam_name`, `description`,
`development_status`, `namo_class`, `namo_category`, `namo_id` (free text or
pattern), `organism`, `tissue_or_cell_type` (free text), `endpoints_measured`,
`study_id`, `dataset_id`, `related_publications`, `external_link`,
`synapse_entity_id`, governance slots (M11) and `portal_display`.

The fixes to PR #18 and PR #22 change `NAMs` before this plan starts (see M0,
"Fixed in PR #18 and PR #22"):

- `nam_id` is single-valued.
- `dataset_id` is removed. The only link is `Datasets.nam_id`.
- `namo_id` takes a NAMO class CURIE (`^namo:[A-Za-z]+$`, for example
  `namo:Organoid`).
- `duo_code` becomes `data_use_modifiers`, or it gets the DUO enum (PR #18
  review, PR18-6).
- `license` uses `LicenseEnum`.

## Changes

### PR 1: additions (not breaking)

NAMO concrete classes for `nam_type`: TwoDCellCulture, CellLineModel,
ThreeDCellCulture, Organoid, CoCulture, OrganOnChip, TissueOnChip, QSARModel,
PBPKModel, MLModel, DigitalTwin, MetabolicModel and AnimalModel.

| Slot | Source | Range | Notes |
|---|---|---|---|
| `nam_type` | NAMO concrete classes (`exact_mappings`, pinned SHA) plus generic types that NAMO lacks | enum | Each value gets an NCIT, EFO or OBI `meaning` where one exists after an OLS check. The generic types come from the NAMHub landscape review (restricted access; contents not reproduced). |
| `tissue` | Reuse the PR #18 slot and `TissueEnum` (UBERON). The slot is multivalued everywhere after PR18-12. | enum, multivalued | Tissue or organ that the NAM models (FDA section B). Replaces the tissue part of `tissue_or_cell_type`. |
| `cell_type` | Reuse the PR #18 slot and `CellTypeEnum` (CL) | enum, multivalued | Replaces the cell part of `tissue_or_cell_type`. |
| `biological_organization_level` | NAMO enum (mapping) | enum | |
| `physiological_features_assessed`, `functional_readouts`, `human_relevance_rationale` | FDA NAM draft guidance section B | text | `see_also` and `source` |
| `detection_method`, `statistical_method`, `result_classification_criteria` | FDA C.1, C.2 | text | |
| `assay_working_duration` and `_unit` | FDA C.4 | float and `TimeUnitEnum` (UO) | |
| `parent_nam_id` | `prov:wasDerivedFrom` | `nam_id`, multivalued | NAM that is adapted from another NAM |
| `component_nam_id` | `BFO:0000051` has part | `nam_id`, multivalued | For example, a multi-organ chip |
| `previous_version_nam_id` | `prov:wasRevisionOf` | `nam_id` | |
| Protocol link | — | — | Waits for D24 (`protocol_id` or link) |

Keep `development_status`, `organism` and `endpoints_measured`. M0 PR 2 adds
their anchors.

### PR 2: migration (breaking)

1. Map every existing row to `nam_type`. Use `namo_class`, `namo_category`
   and `namo_id` (a `namo:` CURIE after PR18-9).
2. Split `tissue_or_cell_type` into `tissue` and `cell_type`.
3. Make the mapping a table and review it before any change to the live
   table.
4. Remove `namo_class`, `namo_category`, `namo_id` and `tissue_or_cell_type`.
5. Increase `version:`.
6. Update the columns of syn75404716 as a separate, approved step.

## Checks

Do the standard checks (README section 2).

- PR 1 adds optional columns to `NAMs` only.
- PR 2 removes four columns. Its Curator diff must show only those removals.

## Assumptions

1. The live `NAMs` rows can be mapped to `nam_type` by hand. The contents of
   the table were not examined.
2. The NAMO class IRIs are stable at the pinned commit
   (`https://w3id.org/monarch-initiative/namo/…`).
3. Training and calibration datasets belong to the in silico model instance
   (M4 `InSilicoModel`) and not to the catalog entry. M3 does not carry them.

## Open questions

1. The FDA guidance lists these model architectures: monoculture, coculture,
   spheroid, organoid, reconstructed tissue and organ-chip. They overlap
   `nam_type`. Add a separate `model_architecture` slot?
   Recommendation: do not add the slot. Record the FDA terms as mappings on
   the `nam_type` values.
2. Is read access to syn75404716 (or an export) available to draft the
   migration table?
