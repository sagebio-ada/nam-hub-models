# M4 model: model instances

**Decisions:** D2 (in vitro instances are Biospecimen rows with optional model
columns; MPS devices are a separate record), D4, D8 (start with the
recommended required fields), D10 (animal comparator data is in scope), D11,
D16.

## Scope

1. Add the FDA C.5, FDA C.8 and NAMO fields to Biospecimen for in vitro model
   rows. Add the link to the NAM catalog.
2. Add `MicrophysiologicalDevice` (FDA C.9).
3. Add `InSilicoModel`.
4. Confirm that Individual and Biospecimen cover animal models.

This module runs after the M6 PR. Both edit `modules/biospecimen.yaml`. M6
changes existing slots. M4 adds new slots.

## Starting point

The PR #18 Biospecimen holds these slots: `biospecimen_type` (tissue, primary
cells, cell line, in vitro differentiated cells, organoid, engineered
tissue/MPS, other), `tissue` (tissue modeled), `cell_type` (CL), `cell_line`,
`cellosaurus_id`, `culture_condition`, `culture_duration` and its unit, and
`parent_biospecimen_id`. Individual holds `species`, `strain` and `genotype`.

## Changes

### PR 1: Biospecimen model fields

All slots are optional (D2). The anchors are candidates until the OLS check.

| Slot | Source | Range |
|---|---|---|
| `nam_id` | Instance of a NAM catalog entry; `IAO:0000136` is about | `nam_id` |
| `cell_source_type` | FDA C.5 (primary, immortalized, stem-cell-derived); NAMO `cell_source` mapping | enum (CL / EFO meanings) |
| `vendor`, `catalog_number`, `lot_number` | FDA C.5; schema.org `manufacturer`, `productID`, `serialNumber`-style mappings | text |
| `passage_number` | FDA C.8; NAMO `passage_range` (close mapping) | integer |
| `authentication_method` | NAMO `authentication_method` | enum, multivalued (STR profiling, mycoplasma testing, species verification; OBI/NCIT meanings) |
| `culture_medium`, `serum`, `antibiotics`, `growth_factors`, `surface_coating`, `incubator_conditions` | FDA C.8 | text (`growth_factors` can later bind to CHEBI/PR) |
| `three_d_architecture`, `matrix_composition` | NAMO `three_d_architecture`, `matrix_composition` | enum / text |
| `differentiation_method` | NAMO `differentiation_method`; FDA C.5 | text |
| `coculture_configuration` | NAMO `coculture_configuration` | enum (direct contact, transwell, conditioned medium, …) |
| `device_id` | Device in which the model grew (PR 2) | `device_id` |

**Reason:** FDA C.8 asks for the passage number of cells. NAMO records
the passage range and the authentication method of a cell model. PR #18 has
neither field.

A co-culture is one Biospecimen row with several `parent_biospecimen_id`
values. Each value is one input population. The PR #18 fixes make the slot
multivalued (PR #18 review, PR18-14).

The PR #18 fixes give `biospecimen_type` values their `meaning` terms (PR #18
review, PR18-10):

- tissue: `NCIT:C12801`
- primary cells: `EFO:0002660`
- cell line: `CLO:0000031`
- organoid: `NCIT:C172259`

OLS has no term for in vitro differentiated cells or for engineered tissue.
These two values get `close_mappings` to NAMO classes at the pinned commit.
All values get `exact_mappings` to CELLxGENE `tissue_type` where one exists
(tissue, primary cell culture, cell line, organoid). M0 PR 2 makes the NAMO
and CELLxGENE mappings.

### PR 2: `MicrophysiologicalDevice`

One row for each device type and lot. `device_id` is global (D11: devices
cross studies).

Fields: `device_manufacturer`, `device_model`, `device_lot`, `chip_material`,
`flow_rate` and unit, `shear_stress` and unit, `membrane_type`,
`membrane_pore_size` and unit, `mechanical_stimulation_type`,
`leachables_assessment`, `compound_adsorption_assessment` and
`biocompatibility_assessment`.

Source: FDA C.9, flattened from NAMO `MicrofluidicDesign` and
`MechanicalStimulation`. Do not carry over the NAMO ISO 10991 mappings
(README section 2, source rule). Bind units to UO.

**Reason:** One device lot serves many biospecimens (D2).

### PR 3: `InSilicoModel`

Keys: `in_silico_model_id` (study-scoped), `study_id` and `nam_id`.

- `model_form` (required): first-principles or mechanistic, data-driven, or
  hybrid. This value decides which FDA credibility guidance applies in M9.
- Model description (FDA CDRH 2023, Appendix 2): `computational_method`,
  `governing_equations_description`, `parameter_source_description` and
  `numerical_methods`.
- Software: `software_platform`, `software_version`, `model_version` and
  `software_qa_description`.
- Scope: `prediction_scope` and `quantities_of_interest`.
- Data: `training_dataset_id` and `calibration_dataset_id`. Both are
  multivalued, link to Datasets, and map to `prov:used`.
- Data-driven description (FDA AI draft, step 4): `model_inputs`,
  `model_outputs`, `model_architecture`, `model_features`,
  `feature_selection_method`, `loss_function`, `modeling_approach_rationale`,
  `learning_methodology`, `training_hyperparameters`, `overfitting_control`,
  `ensemble_methods`, `output_calibration`, `software_qa_procedures` and
  `version_tracking`. Offer NAMO `ml_algorithm` as an optional label.

Code and containers link through M10 `SoftwareArtifact` (a later family
plan). Output files link back through `File.in_silico_model_id` (M10).

### Animal models (D10)

Add no new template.

- An animal is an Individual of a non-human species with `strain` and
  `genotype`.
- The samples of the animal are Biospecimens.
- In vivo dosing is an M8 Exposure on the Individual (see M8).
- A comparator animal dataset links through `Datasets.comparator_dataset_id`
  (M2).

## Checks

Do the standard checks (README section 2).

- PR 1 adds optional Biospecimen columns.
- PR 2 and PR 3 each add one template.

Verified fact: `gen-curator` drops LinkML `rules` without a warning. A test
rule ("cell line requires `cellosaurus_id`") gave no condition in
`Biospecimen.json`, and `curator-lint` gave no warning. Curator cannot
enforce conditional requirements today.

## Assumptions

1. Synapse Curator accepts a Biospecimen template with about 20 more optional
   columns. Tissue-only datasets stay usable.
2. The data-driven fields of `InSilicoModel` stay optional in the schema,
   because rules are not available (see Checks). Review or a QC script
   enforces "required when data-driven".

## Open questions

1. D8 asks that `cell_source_type` and `lot_number` (or `catalog_number`) are
   required on in vitro rows only. Curator cannot express this. Options:
   - (a) Leave the fields optional and check them in a QC script after
     upload.
   - (b) Add `if/then` support to linkml-curator (a separate repository,
     sagebio-ada/linkml-curator; needs approval).
   - (c) Split a separate `InVitroModel` template from Biospecimen, with
     those fields required. This conflicts with D2.

   Recommendation: (a) now, and (b) as a separate request.
2. Should `device_id`, `test_article_id` and `protocol_id` be global (a shared
   catalog across studies, as this plan assumes) or study-scoped like records?
   Recommendation: global, because each one can serve more than one study
   (D11).
