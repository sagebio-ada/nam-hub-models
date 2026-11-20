# M3 nam: NAM catalog

**Decisions (README section 4):** D2, D4, D7, D11, D24, D27, D30, D31

## Scope

Reshape `NAMs` (syn75404716) to do four things:

1. Classify each NAM with standard terms.
2. Add the method-level fields of the FDA NAM guidance (sections B and C).
3. Link each NAM to related NAMs.
4. Remove the slots that repeat other slots or links.

NAMs is the catalog. Its instances are Biospecimen rows and `InSilicoModel`
records (D2, M4). Training and calibration datasets belong to the
`InSilicoModel` record, not to the catalog entry.

## Starting point

`NAMs` has these slots:

- `nam_id` (global key), `nam_name`, `description`, `development_status`
  (`DevelopmentStatusEnum`).
- `namo_class` and `namo_category` (free text), `namo_id` (pattern
  `^namo:[A-Za-z]+$`, for example `namo:Organoid`).
- `organism` (`SpeciesEnum`, multivalued, close mapping to `species`).
- `tissue_or_cell_type` and `endpoints_measured` (free text, multivalued).
- `study_id`, `related_publications` (PubMed IDs), `external_link`,
  `synapse_entity_id`.
- Governance (M11): `access_type`, `access_requirements`,
  `data_use_modifiers` (DUO), `acknowledgement_statements`, `license`
  (`LicenseEnum`).
- `portal_display`.

Datasets, NAMPortalDataset and Publications link to NAMs with `nam_id`.

The live table syn75404716 has no rows (PR #18 author, commit `eeac44f`).

## Changes

One PR. The Curator output changes (major version: columns are removed).

Add or change:

| Slot | Source and anchor (candidates) | Range | Notes |
|---|---|---|---|
| `nam_type` (new) | NAMO concrete classes (mappings at the pinned commit, D7; relation and review state in the SSSOM file, D31) and generic types that NAMO does not have | enum | Each value gets an NCIT, EFO or OBI `meaning` where one exists after an OLS check. The generic types come from the NAMHub landscape review (restricted access; contents not reproduced). |
| `tissue` (reuse) | `TissueEnum` (UBERON) | enum, multivalued | Modeled role (D30): the tissue or organ that the NAM represents (FDA section B). Not the origin of its cells. |
| `cell_type` (reuse) | `CellTypeEnum` (CL) | enum, multivalued | Input role (D30): the cell types put into the model. |
| `species` (reuse) | `SpeciesEnum` (NCBITaxon) | enum, multivalued | Replaces `organism`. Modeled role (D30): the species whose biology the NAM represents. The origin species is on Individual. |
| `modeled_disease` (new) | MONDO; reuse `DiagnosisEnum` as the range | enum, multivalued | The disease state that the NAM represents (D30). Not the donor diagnosis, which is on Diagnosis. |
| `modeled_phenotype` (new) | HP or MP; new `PhenotypeEnum`, grown for each NAM (D6a) | enum, multivalued | The phenotypes that the NAM is built to reproduce (D30). |
| `biological_organization_level` (new) | NAMO enum (mapping) | enum | |
| `physiological_features_assessed`, `human_relevance_rationale` (new) | FDA NAM guidance section B | text | `see_also` and `source` |
| `endpoints_measured` (keep) | FDA NAM guidance section B (functional readouts) | text, multivalued | Add `see_also` and `source`. The FDA functional readouts are the endpoints that this slot holds, so no second slot is added (D27). |
| `detection_method`, `statistical_method`, `result_classification_criteria` (new) | FDA C.1, C.2 | text | |
| `assay_working_duration` and `_unit` (new) | FDA C.4 | float and `TimeUnitEnum` (UO) | |
| `parent_nam_id` (new) | `prov:wasDerivedFrom` | `nam_id`, multivalued | NAM that this NAM is adapted from |
| `component_nam_id` (new) | `BFO:0000051` has part | `nam_id`, multivalued | For example, the single-organ models of a multi-organ chip |
| `previous_version_nam_id` (new) | `prov:wasRevisionOf` | `nam_id` | |
| `protocol_id` (new) | ISA Protocol (M7) | `protocol_id`, multivalued | The protocols that define the NAM. An instance of the NAM can name the same protocols (M6). |

NAMO concrete classes for `nam_type` (D7): TwoDCellCulture, CellLineModel,
ThreeDCellCulture, Organoid, CoCulture, OrganOnChip, TissueOnChip,
QSARModel, PBPKModel, MLModel, DigitalTwin, MetabolicModel and AnimalModel
(see open question 2).

Remove:

| Slot | Reason |
|---|---|
| `namo_class`, `namo_category`, `namo_id` | `nam_type` replaces them. The NAMO IRIs move to the `exact_mappings` of the enum values. |
| `tissue_or_cell_type` | `tissue` and `cell_type` replace it. |
| `organism` | `species` has the same range and meaning. PR #22 marked the two slots as close mappings. |
| `related_publications` | `Publications.nam_id` holds this link (one direction, README section 2). |

Keep `development_status`. M0 PR 2 adds the anchors of the kept slots.

Update the columns of syn75404716 as a separate, approved step.

## Checks

Do the standard checks (README section 2). The Curator diff shows only the
added and removed `NAMs` columns in the tables above.

## Assumptions

1. syn75404716 has no rows when this PR starts. If it has rows, map them to
   the new slots in a reviewed table before the columns change.
2. The NAMO class IRIs are stable at the pinned commit
   (`https://w3id.org/monarch-initiative/namo/…`).

## Open questions

1. The FDA guidance lists these model architectures: monoculture, coculture,
   spheroid, organoid, reconstructed tissue and organ-chip. They overlap
   `nam_type` and the M4 slots `three_d_architecture` and
   `coculture_configuration`. Add a separate slot for them?
   Recommendation: no. Record the FDA terms as mappings on the `nam_type`
   values.
2. NAMO has `AnimalModel`. An animal model is not a NAM, and D10 records
   animals as Individuals with comparator datasets. Include `AnimalModel` as
   a `nam_type` value? Recommendation: no.
3. A NAM can combine types, for example organoids in an organ-on-chip. Make
   `nam_type` multivalued? Recommendation: yes. Use `component_nam_id` only
   when the parts are separate catalog entries.
