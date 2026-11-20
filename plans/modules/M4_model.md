# M4 model: model instances

**Decisions (README section 4):** D2, D4, D6, D8, D10, D11, D24, D27, D33, D36

## Scope

1. Add `ModelSystem`: the type-level descriptors of a model system (FDA C.5
   and NAMO fields, and the modeled descriptors moved from NAMs). Add the
   FDA C.8 and NAMO instance fields to Biospecimen for in vitro model rows.
   Add the link from Biospecimen to `ModelSystem`.
2. Add `CultureProtocol` (FDA C.8 and C.9 run conditions) and
   `MicrophysiologicalDevice` (FDA C.9).
3. Add `InSilicoModel`.
4. Confirm that Individual and Biospecimen cover animal models.

Test datasets and performance values belong to M9 (D17). M9 PR 4 adds
`tuning_dataset_id`, `pretraining_dataset_id` and `pretrained_model_source`
to `InSilicoModel`.

This module runs after M6 and M7. M4 and M6 both edit
`modules/biospecimen.yaml`. M6 changes existing slots. M4 adds new slots.
Put `ModelSystem`, `MicrophysiologicalDevice` and `InSilicoModel` in
`modules/model.yaml`.
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

### PR 1a: `ModelSystem`

`ModelSystem` is a record of a model system type (global `model_system_id`,
D11). One system type serves many NAMs and many biospecimens (D27, D36). It
holds the type-level descriptors. FUSION (NDHCC) LinkML model, version
1.2.0-wave2r4: `ModelSystem` (a NAM system). Exact mapping
`ndhcc:ModelSystem`. Broad mapping `OBI:0001876` (cell culture).

| Slot | Required | Range | Description | Anchor / FUSION slot |
|---|---|---|---|---|
| `model_system_id` | yes | key | Global ID of the model system type. | ndhcc `source_identifier` |
| `model_system_name` | yes | text | Name of the model system type. | ndhcc `title` |
| `description` | no | text | Reuse the shared slot. | ndhcc `description` |
| `species` | yes | `SpeciesEnum` (NCBITaxon), multivalued (moved from NAMs) | Species of the cells. | ndhcc `origin_species` |
| `tissue` | no | `TissueEnum` (UBERON), multivalued (moved from NAMs) | Tissue that the system represents (modeled role, D30; FDA section B). Not the origin of its cells. | ndhcc `tissue` |
| `cell_type` | no | `CellTypeEnum` (CL), multivalued (moved from NAMs) | Cell types in the system (input role, D30). | ndhcc `cell_types` |
| `modeled_disease` | no | `DiagnosisEnum` (MONDO), multivalued (moved from NAMs) | Disease state that the system represents (D30). Not the donor diagnosis, which is on Diagnosis. | No NDHCC slot (close: CoU `disease_or_use_area`) |
| `modeled_phenotype` | no | New `PhenotypeEnum` (HP or MP), grown for each NAM (D6a); multivalued (moved from NAMs) | Phenotypes that the system is built to reproduce (D30). | No NDHCC slot |
| `biological_organization_level` | no | NAMO enum (mapping) (moved from NAMs) | | No NDHCC slot |
| `cell_source_type` | no | enum (CL and EFO meanings) (moved from Biospecimen) | FDA C.5 (primary, immortalized, stem-cell-derived); NAMO `cell_source` mapping. | ndhcc `derivation` |
| `three_d_architecture` | no | enum (moved from Biospecimen) | NAMO `three_d_architecture`. | ndhcc `geometry` |
| `coculture_configuration` | no | enum (direct contact, transwell, conditioned medium, …) (moved from Biospecimen) | NAMO `coculture_configuration`. | No NDHCC slot |
| `vendor` | no | text (moved from Biospecimen) | Vendor of a commercial model system. FDA C.5. schema.org `manufacturer` (close). | No NDHCC `ModelSystem` slot (Device has `vendor`) |
| `catalog_number` | no | text (moved from Biospecimen) | Vendor catalog number. FDA C.5. schema.org `productID`. | ndhcc ReagentFacts `catalog_number` (close) |

All slots except the three required ones are optional (D2). The anchors are
candidates until the OLS check. NAMs link to `ModelSystem` with
`model_system_id` (M3).

Record the cell source, vendor and catalog number once on the `ModelSystem`
row. A biospecimen reaches them through `model_system_id`. Do not repeat
them on Biospecimen rows (D27).

**Reason:** FUSION keeps the NAM, the NAM system (`ModelSystem` or
`Device`) and the Sample apart. A `ModelSystem` row stores the type-level
values once (D27).

### PR 1: Biospecimen model fields

All slots are optional (D2). The anchors are candidates until the OLS check.

Fields of the model instance:

| Slot | Source and anchor | Range |
|---|---|---|
| `model_system_id` | The `ModelSystem` row that this model is an instance of. It replaces `nam_id`. Blank on source rows. Do not use IAO "is about": a biospecimen is not an information entity (M0 open question 2c). | `model_system_id` |
| `lot_number` | FDA C.5. `IAO:0000132` (lot number). | text |
| `passage_number` | FDA C.8; NAMO `passage_range` (close mapping) | integer |
| `authentication_method` | NAMO `authentication_method` | enum, multivalued (STR profiling, mycoplasma testing, species verification; OBI and NCIT meanings) |
| `device_id`, `device_lot_number` | PR 2 adds them. | see PR 2 |

The fields `cell_source_type`, `three_d_architecture`,
`coculture_configuration`, `vendor` and `catalog_number` are not on
Biospecimen. They sit on `ModelSystem` (PR 1a). Record `lot_number` and
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
tissue, and FDA C.5 asks for the cell source. `ModelSystem` holds the cell
source. FDA C.8 asks for the passage number. NAMO records the passage range
and the authentication method of a cell model. `main` has none of these
fields.

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
| `vendor`, `catalog_number` | Reuse the PR 1a slots |
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

### FUSION mapping (D33)

Source: the FUSION (NDHCC) LinkML model, version 1.2.0-wave2r4.

- `ModelSystem` is an exact mapping to `ndhcc:ModelSystem`.
- `MicrophysiologicalDevice` is an exact mapping to `ndhcc:Device`.
- `CultureProtocol` is an exact mapping to `ndhcc:ProtocolVersion`.
  `matrix_composition` is a close mapping to `matrix_or_scaffold`.
- `InSilicoModel` is a close mapping to `ndhcc:Software`.
- The slot mappings of `ModelSystem` are in the PR 1a table.

## Checks

Do the standard checks (README section 2).

- PR 1a adds one template (`ModelSystem`).
- PR 1 adds optional Biospecimen columns.
- PR 2 adds two templates and the optional `device_id` and
  `device_lot_number` columns on Biospecimen.
- PR 3 adds one template.

## Assumptions

1. Synapse Curator accepts a Biospecimen template with more optional
   columns (`model_system_id`, `lot_number`, `passage_number`,
   `authentication_method`, `device_id`, `device_lot_number`). Tissue-only
   datasets stay usable.
2. A cell line from a vendor has an Individual row for its donor, because
   `main` requires `individual_id` on Biospecimen. The donor row holds
   `species` and, where Cellosaurus gives them, `sex` and age.
3. The fields that D8 requires for in vitro models (`cell_source_type`
   and `catalog_number` on the `ModelSystem` row, and `lot_number` on the
   source Biospecimen row) and the data-driven fields of
   `InSilicoModel` stay optional in the schema. Curator cannot enforce a
   conditional requirement. README section 8, question 1 covers the check.

## Open questions

1. `culture_condition` (free text, on `main`) repeats what a
   `CultureProtocol` row holds. Remove it from Biospecimen (D27)? The
   change is breaking, and datasets in ingestion use the slot.
   Recommendation: map the existing values to `CultureProtocol` rows, then
   remove the slot in this PR.

2. Is `ModelSystem` also the record for an in vivo animal model type
   (strain, genotype), or do animals stay only on Individual (D10)?
   Recommendation: animals stay on Individual.

README section 8, question 1 (conditional checks) and M0 open question 1
(scope of `device_id`) also apply.
