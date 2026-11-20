# M4 model: model instances

**Decisions (README section 4):** D2, D4, D6, D8, D10, D11, D24, D27

## Scope

1. Add the FDA C.5, FDA C.8 and NAMO fields to Biospecimen for in vitro
   model rows. Add the link to the NAM catalog.
2. Add `CultureProtocol` (FDA C.8 and C.9 run conditions) and
   `MicrophysiologicalDevice` (FDA C.9).
3. Add `InSilicoModel`.
4. Confirm that Individual and Biospecimen cover animal models.

Test datasets and performance values belong to M9 (D17). M9 PR 4 adds
`tuning_dataset_id`, `pretraining_dataset_id` and `pretrained_model_source`
to `InSilicoModel`.

This module runs after M6 and M7. M4 and M6 both edit
`modules/biospecimen.yaml`. M6 changes existing slots. M4 adds new slots.
Put `MicrophysiologicalDevice` and `InSilicoModel` in `modules/model.yaml`.
Put `CultureProtocol` in `modules/protocol.yaml`, next to `Protocol`, so
that no module imports another module. Put slots that more than one file
uses (`vendor`, `catalog_number`, `lot_number`, `device_id`) in `core.yaml`
(M0 PR 1 rule).

## Starting point

The Biospecimen template on `main` holds these slots:

- `biospecimen_type`: tissue, primary cells, cell line, in vitro
  differentiated cells, organoid, engineered tissue, other.
- `tissue` (UBERON, multivalued), `cell_type` (CL, multivalued),
  `cell_line`, `cellosaurus_id`.
- `culture_condition` (free text), `culture_duration` and its unit.
- `parent_biospecimen_id` (multivalued).
- `individual_id` (required).

Individual holds `species`, `strain` and `genotype`.

## Changes

### PR 1: Biospecimen model fields

All slots are optional (D2). The anchors are candidates until the OLS check.

Fields of the model instance and its source material:

| Slot | Source and anchor | Range |
|---|---|---|
| `nam_id` | The NAM catalog entry that this model is an instance of. Do not use IAO "is about": a biospecimen is not an information entity (M0 open question 2c). | `nam_id` |
| `cell_source_type` | FDA C.5 (primary, immortalized, stem-cell-derived); NAMO `cell_source` mapping | enum (CL and EFO meanings) |
| `vendor`, `catalog_number`, `lot_number` | FDA C.5. `vendor`: schema.org `manufacturer` (close). `catalog_number`: schema.org `productID`. `lot_number`: `IAO:0000132` (lot number). | text |
| `passage_number` | FDA C.8; NAMO `passage_range` (close mapping) | integer |
| `authentication_method` | NAMO `authentication_method` | enum, multivalued (STR profiling, mycoplasma testing, species verification; OBI and NCIT meanings) |
| `three_d_architecture` | NAMO `three_d_architecture` | enum |
| `coculture_configuration` | NAMO `coculture_configuration` | enum (direct contact, transwell, conditioned medium, …) |

Record `cell_source_type`, `vendor`, `catalog_number`, `lot_number` and
`authentication_method` on the row of the source material (for example the
cell line). A derived row (for example an organoid) reaches them through
`parent_biospecimen_id`. Do not repeat them on derived rows (D27).

A co-culture is one Biospecimen row with several `parent_biospecimen_id`
values. Each value is one input population. The cell type of each parent
row shows its part in the co-culture. Matrix, medium and device are not
parent rows: `CultureProtocol` and `device_id` give them.

Make a Biospecimen row only for a material that exists. A NAM catalog entry
or a protocol does not imply a physical model.

**Reason:** `biospecimen_type` gives the form of the material, for example
organoid. It does not give the cell source of an organoid or an engineered
tissue, and FDA C.5 asks for the cell source. FDA C.8 asks for the passage
number. NAMO records the passage range and the authentication method of a
cell model. `main` has none of these fields.

### PR 2: `CultureProtocol` and `MicrophysiologicalDevice`

`CultureProtocol` (is_a `Protocol`, M7) holds the culture parameters once
for every biospecimen that uses the protocol. A biospecimen names it with
`protocol_id` (M6).

| Slot | Source and anchor | Range |
|---|---|---|
| `culture_medium`, `serum`, `antibiotics`, `growth_factors`, `surface_coating`, `incubator_conditions` | FDA C.8 | text |
| `matrix_composition` | NAMO `matrix_composition` | text |
| `flow_rate` and unit, `shear_stress` and unit, `mechanical_stimulation_type` | FDA C.9; NAMO `MicrofluidicDesign`, `MechanicalStimulation` | float and UO unit enums; enum |

A differentiation protocol is a `CultureProtocol` row with `protocol_type`
differentiation. Its name, link and `parameters_description` describe the
method. Thus there is no `differentiation_method` slot. Map NAMO
`differentiation_method` to `Protocol` (close mapping).

`MicrophysiologicalDevice`: one row for each device type (FDA C.9).
`device_id` is global (D11; M0 open question 1).

| Slot | Source |
|---|---|
| `device_id` | Key |
| `vendor`, `catalog_number` | Reuse the PR 1 slots |
| `device_model` | FDA C.9 |
| `chip_material`, `membrane_type`, `membrane_pore_size` and unit | FDA C.9; NAMO `MicrofluidicDesign` |
| `leachables_assessment`, `compound_adsorption_assessment`, `biocompatibility_assessment` | FDA C.9 |

Add to Biospecimen (optional):

- `device_id`: the device type in which the model grew.
- `device_lot_number`: the lot of that device (`IAO:0000132`). It is a
  separate slot from `lot_number`, which gives the lot of the source cells.

Bind units to UO. Do not carry over the NAMO ISO 10991 mappings (README
section 2, source rule).

**Reason:** Many biospecimens share one culture protocol and one device
type. A `CultureProtocol` row and a `MicrophysiologicalDevice` row store
their values once (D27). The device lot changes for each use, so it stays
on Biospecimen.

### PR 3: `InSilicoModel`

Keys: `in_silico_model_id` (study-scoped), `study_id` and `nam_id`.

| Group | Slots | Source |
|---|---|---|
| Form | `model_form` (required): first-principles or mechanistic, data-driven, or hybrid. This value decides which FDA credibility guidance applies in M9. | D9 |
| Description | `computational_method`, `governing_equations_description`, `parameter_source_description`, `numerical_methods` | FDA CDRH 2023, Appendix 2 |
| Software | `software_platform`, `software_version`, `model_version`, `software_qa_description` | FDA CDRH 2023; FDA AI draft, step 4 (quality assurance and version tracking) |
| Scope | `prediction_scope`, `quantities_of_interest` | FDA CDRH 2023 |
| Data | `training_dataset_id`, `calibration_dataset_id`. Both are multivalued, map to `prov:used`, and accept a Synapse ID, a CURIE or a URL (README section 2). | FDA AI draft, step 4 |
| Data-driven description | `model_inputs`, `model_outputs`, `model_architecture` (NAMO `ml_algorithm` as a close mapping), `model_features`, `feature_selection_method`, `loss_function`, `modeling_approach_rationale`, `learning_methodology`, `training_hyperparameters`, `overfitting_control`, `ensemble_methods`, `output_calibration` | FDA AI draft, step 4 |

Code and containers link through `SoftwareArtifact` records. Output files
link back through `in_silico_model_id`. Both are in the in silico outputs
and code family plan (README section 6). Do not add `in_silico_model_id` to
the `File` base class: sequencing files do not use it.

### Animal models (D10)

Add no new template.

- An animal is an Individual of a non-human species with `strain` and
  `genotype`.
- The samples of the animal are Biospecimens.
- In vivo dosing is an M8 Exposure on the Individual.
- A comparator animal dataset links through `comparator_dataset_id` (M2).

## Checks

Do the standard checks (README section 2).

- PR 1 adds optional Biospecimen columns.
- PR 2 adds two templates and the optional `device_id` and
  `device_lot_number` columns on Biospecimen.
- PR 3 adds one template.

## Assumptions

1. Synapse Curator accepts a Biospecimen template with 11 more optional
   columns. Tissue-only datasets stay usable.
2. A cell line from a vendor has an Individual row for its donor, because
   `main` requires `individual_id` on Biospecimen. The donor row holds
   `species` and, where Cellosaurus gives them, `sex` and age.
3. The fields that D8 requires for in vitro models (`cell_source_type`,
   and `lot_number` or `catalog_number`, on the source row) and the
   data-driven fields of
   `InSilicoModel` stay optional in the schema. Curator cannot enforce a
   conditional requirement. README section 8, question 1 covers the check.

## Open questions

1. `culture_condition` (free text, on `main`) repeats what a
   `CultureProtocol` row holds. Remove it from Biospecimen (D27)? The
   change is breaking, and datasets in ingestion use the slot.
   Recommendation: map the existing values to `CultureProtocol` rows, then
   remove the slot in this PR.

README section 8, question 1 (conditional checks) and M0 open question 1
(scope of `device_id`) also apply.
