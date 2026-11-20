# M3 nam: NAM catalog

**Decisions (README section 4):** D2, D4, D7, D11, D24, D27, D30, D31, D33, D35, D36, D41

## Scope

Reshape `NAMs` (syn75404716) to do four things:

1. Classify each NAM with standard terms.
2. Add the method-level fields of the FDA NAM guidance (sections B and C).
3. Link each NAM to related NAMs.
4. Remove the slots that repeat other slots or links.

A NAM specifies its system types (`ModelSystem` and `MicrophysiologicalDevice`)
or its software (`InSilicoModel`, FUSION `uses_software`). Assays realize
the NAM (M2). Biospecimen rows are physical instances of its model systems
(D2, D36, M4). One study develops each NAM (D35). Training and calibration
datasets belong to the `InSilicoModel` record, not to the catalog entry.

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
| `nam_kind` (new, required) | FUSION (NDHCC) LinkML model, version 1.2.0-wave2r4: `NAMKindEnum`. FUSION `nam_kind` (D41). | enum, one value | Values: `in_vitro_cellular_system`, `organoid`, `microphysiological_system`, `in_chemico_system`, `in_silico_model`, `in_vivo_system`, `composite_nam`. A composite NAM names its parts in `component_nam_id`. |
| `namo_id` (keep) | NAMO concrete class (mappings at the pinned commit, D7; relation and review state in the SSSOM file, D31). FUSION `namo_term`. | text (existing pattern) | The NAMO class gives the NAMO category. Use a NAMO concrete class, for example TwoDCellCulture, CellLineModel, ThreeDCellCulture, Organoid, CoCulture, OrganOnChip, TissueOnChip, QSARModel, PBPKModel, MLModel, DigitalTwin or MetabolicModel (see open question 2). |
| `study_id` (change, required) | FUSION `developed_by_study` (D35) | link to Studies | The study that develops the NAM. Other studies use the NAM through `Assay.nam_id` (M2). `nam_id` stays global. |
| `model_system_id` (new) | FUSION `uses_system` (D36) | `model_system_id`, multivalued | The model system types that the NAM specifies (M4). They hold species, tissue, cell type, modeled disease and modeled phenotype. |
| `device_id` (new) | FUSION `uses_system` (D36) | `device_id`, multivalued | The device types that the NAM specifies (M4). |
| `physiological_features_assessed`, `human_relevance_rationale` (new) | FDA NAM guidance section B | text | `see_also` and `source` |
| `endpoints_measured` (keep) | FDA NAM guidance section B (functional readouts) | text, multivalued | Add `see_also` and `source`. The FDA functional readouts are the endpoints that this slot holds, so no second slot is added (D27). |
| `detection_method`, `statistical_method`, `result_classification_criteria` (new) | FDA C.1, C.2 | text | |
| `assay_working_duration` and `_unit` (new) | FDA C.4 | float and `TimeUnitEnum` (UO) | |
| `parent_nam_id` (new) | `prov:wasDerivedFrom` | `nam_id`, multivalued | NAM that this NAM is adapted from |
| `component_nam_id` (new) | `BFO:0000051` has part | `nam_id`, multivalued | For example, the single-organ models of a multi-organ chip |
| `previous_version_nam_id` (new) | `prov:wasRevisionOf` | `nam_id` | |
| `protocol_id` (new) | ISA Protocol (M7) | `protocol_id`, multivalued | The protocols that define the NAM. An instance of the NAM can name the same protocols (M6). |

Remove:

| Slot | Reason |
|---|---|
| `namo_class`, `namo_category` | NAMO gives them from `namo_id` (D41). |
| `tissue_or_cell_type`, `organism` | `ModelSystem` holds the species, tissue and cell type (D36). |
| `species`, `tissue`, `cell_type`, `modeled_disease`, `modeled_phenotype`, `biological_organization_level` | They move to `ModelSystem` (M4, D36). The NAM reaches them through `model_system_id`. |
| `access_type`, `access_requirements`, `data_use_modifiers`, `license` | A FUSION NAM has one `access_condition` link, and FUSION projects these four from it. Keep `access_requirement_id` and `acknowledgement_statements`. The dataset record keeps the data access fields (M11). |
| `related_publications` | `Publications.nam_id` holds this link (one direction, README section 2). |

Keep `development_status`. M0 PR 2 adds the anchors of the kept slots.

Update the columns of syn75404716 as a separate, approved step.

### FUSION mapping (D33)

Source: the FUSION (NDHCC) LinkML model, version 1.2.0-wave2r4.

- `NAMs` is an exact mapping to `ndhcc:NAM`.
- `study_id` maps to `developed_by_study`.
- `model_system_id` and `device_id` map to `uses_system`.
- `nam_kind` maps to `nam_kind`.
- `namo_id` maps to `namo_term`.
- `access_requirement_id` maps to `access_condition`.
- `InSilicoModel` (M4) maps to `uses_software` (close mapping).

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
   `nam_kind` and the M4 `ModelSystem` slots `three_d_architecture` and
   `coculture_configuration`. Add a separate slot for them?
   Recommendation: no. Record the FDA terms as mappings on the values of
   those M4 slots.
2. NAMO has `AnimalModel`, and `nam_kind` has `in_vivo_system`. An animal
   model is not a NAM, and D10 records animals as Individuals with
   comparator datasets. Allow `AnimalModel` as a `namo_id` value and
   `in_vivo_system` as a `nam_kind` value? Recommendation: no.
