# M8 exposure: TestArticle, Exposure, reference compounds

**Decisions (README section 4):** D4, D6, D8, D10, D11, D24, D27, D29, D30

## Scope

Record what was applied to a model or an animal, when, at what dose, by
which route, and as which control (FDA NAM guidance C.1 and C.7). An
exposure can be a chemical, a biological agent, a genetic perturbation or a
physical stimulation. Record the reference compounds
that benchmark a NAM (FDA C.7).

This module runs after M4, M5, M6 and M7. It reuses the shared agent enum (M5),
`ConcentrationUnitEnum` (M5) and the timepoint slots (M6).

## Changes

One PR adds four templates in `modules/exposure.yaml`. The anchors are
candidates until the OLS check.

### `TestArticle` (new; global `test_article_id`)

| Slot | Source and anchor | Range |
|---|---|---|
| `test_article_id` | Key | string |
| `test_article_name` | schema.org `name` | text |
| `agent` | The shared agent enum from M5 (NCIT, with CHEBI and PubChem mappings) | enum, grown for each dataset |
| `chebi_id` | CHEBI (D6b) | pattern `^CHEBI:\d+$` |
| `pubchem_cid` | PubChem compound ID (C2M2 uses PubChem for substances) | pattern `^\d+$` |
| `dtxsid` | EPA CompTox DSSTox substance ID, the usual ID for toxicology chemicals | pattern `^DTXSID\d+$` |
| `preparation`, `storage`, `vehicle` | FDA C.1 (test substance preparation and storage) | text |

Fill `agent` when the substance is in the enum. Otherwise fill one of
`chebi_id`, `pubchem_cid` or `dtxsid`. One identifier is enough (D27). A
genetic perturbation (for example an siRNA or a guide RNA) is a
`TestArticle` with a name and a description.

A `TestArticle` is an input (D30). The analytes that an assay measures are
observed values and belong to the assay file templates.

### `Exposure` (new; study-scoped `exposure_id`)

One row for each test article or stimulation applied to one model or
animal.

| Slot | Source and anchor | Range |
|---|---|---|
| `exposure_id` | Key, unique with `study_id` | string |
| `biospecimen_id` | In vitro: the model that received the article | `biospecimen_id` |
| `individual_id` | In vivo: the animal that received the dose (D10) | `individual_id` |
| `exposure_type` (required) | ISA treatment; one template holds chemical exposures and other interventions, because they share the same fields | enum: chemical, biological agent, genetic perturbation, physical stimulation |
| `test_article_id` | The article that was applied. Empty for a physical stimulation, whose parameters are on its protocol (`protocol_id`). | `test_article_id` |
| `route_of_administration` | In vivo route; NCIT route terms | enum (for example oral, intravenous, subcutaneous, inhalation), with the D29 missing values |
| `dose`, `dose_unit` | FDA C.1. `dose_unit` uses a new `DoseUnitEnum`. It holds the `ConcentrationUnitEnum` values (M5) and UO mass-per-body-mass units for in vivo doses (for example milligram per kilogram). A separate enum keeps mass-per-body-mass units out of the Treatment drug-level unit. | float and enum |
| `dosing_frequency` | FDA C.1 | text |
| `exposure_duration`, `exposure_duration_unit` | FDA C.1; UO | float and `TimeUnitEnum` |
| `timepoint_offset`, `timepoint_offset_unit`, `timepoint_reference_event` | Reuse the M6 slots. They give the start of the exposure, so that a mixture and a sequence of exposures are different (assumption 2). | float and enums |
| `control_role` (required, D8) | FDA C.7; OBI and BAO control terms | enum: test, positive control, negative control, vehicle control, untreated control, reference material |
| `control_justification` | FDA C.7 | text |
| `protocol_id` | The treatment protocol (M7), with `protocol_type` treatment. For a physical stimulation it holds the stimulation parameters. | `protocol_id` |

ISA anchor: a treatment Process with this row as its parameter values, and
a FactorValue on the Sample. C2M2 anchor: `biosample_substance` (in vitro)
and `subject_substance` (in vivo).

A sequencing file reaches the Exposure through its `biospecimen_id`. The
file templates of later assay families (plate readouts, imaging,
electrophysiology) link to the Exposure with `exposure_id`. Readout files
do not repeat compound fields.

### `ReferenceCompoundSet` (new; global `reference_compound_set_id`)

A set is a list of compounds with known outcomes that benchmark a NAM (FDA
C.7). The ID is global, because one set can benchmark NAMs in many studies.

| Slot | Source | Range |
|---|---|---|
| `reference_compound_set_id` | Key | string |
| `reference_compound_set_name` | — | text |
| `source_reference` | The publication or guideline that gives the set (DOI or URL) | uri |

**Reason for a separate set template:** The name and the source belong to
the set. One row for each set stores them once (D27).

### `ReferenceCompound` (new; key `reference_compound_set_id` + `test_article_id`)

One row for each compound in a set (a link record, M0 key conventions).

| Slot | Source | Range |
|---|---|---|
| `reference_compound_set_id` | The set | `reference_compound_set_id` |
| `test_article_id` | The compound | `test_article_id` |
| `expected_outcome` | FDA C.7. The known result of this compound for the endpoint of the set | text |

M9 `ValidationAssessment` links to `reference_compound_set_id`.

**Reason for one row per compound:** Each compound has its own expected
outcome. M9 compares the NAM result with the expected outcome for each
compound. A single description for the whole set cannot hold this.

## Checks

Do the standard checks (README section 2). The PR adds four templates. No
existing template changes.

## Assumptions

1. An Exposure row names exactly one of `biospecimen_id` and
   `individual_id`. Curator cannot enforce this. README section 8, question
   1 covers the check.
2. A mixture (several articles in one exposure) is several Exposure rows
   with the same biospecimen or individual and the same start offset.
   Exposures in sequence have different start offsets.

## Open questions

None.
