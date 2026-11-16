# M8 exposure: TestArticle, Exposure, ReferenceCompoundSet

**Decisions:** D4, D8 (`control_role` is required), D10 (in vivo exposures of
animal Individuals are in scope), D11. One slot waits for D24.

## Scope

Record what was applied to a model or an animal, at what dose, and as which
control (FDA NAM guidance C.1 and C.7). This module runs after M4.

## Changes

One PR adds three templates.

### `TestArticle` (new; global `test_article_id`)

| Slot | Source / anchor (candidate) | Range |
|---|---|---|
| `test_article_id` | — | string |
| `test_article_name` | schema.org `name` | text |
| `therapeutic_agent` | Shared agent vocabulary from M5 (`TherapeuticAgentEnum`, NCIT) | enum, grown per dataset |
| `chebi_id` | CHEBI (D6b) | pattern `^CHEBI:\d+$` |
| `pubchem_cid` | PubChem | pattern `^\d+$` |
| `preparation`, `storage`, `vehicle` | FDA C.1 (test substance preparation and storage) | text |

### `Exposure` (new; study-scoped `exposure_id`)

| Slot | Source / anchor (candidate) | Range |
|---|---|---|
| `biospecimen_id` | In vitro: the model that received the article (`RO:0002233` has input) | `biospecimen_id` |
| `individual_id` | In vivo: the animal that received the dose (D10) | `individual_id` |
| `test_article_id` | — | `test_article_id` |
| `dose`, `dose_unit` | FDA C.1; UO concentration and mass units | float and enum |
| `dosing_frequency` | FDA C.1 | text |
| `exposure_duration`, `exposure_duration_unit` | FDA C.1; UO | float and `TimeUnitEnum` |
| `control_role` (required) | FDA C.7; OBI and BAO control terms (positive, negative, vehicle) | enum: test, positive control, negative control, vehicle control |
| `control_justification` | FDA C.7 | text |
| Protocol link | Waits for D24 | — |

ISA anchor: Factor and FactorValue on the Sample. C2M2 anchor:
`biosample_substance`.

Readout files point to the Exposure with `exposure_id` (M10). Thus they do
not repeat compound fields.

### `ReferenceCompoundSet` (new; global `reference_compound_set_id`)

Slots: `reference_compound_set_name`, `test_article_id` (multivalued),
`expected_outcome_description` and `source_reference` (the publication or
guideline that gives the set).

Source: FDA C.7 (reference compounds for benchmarking). M9
`ValidationAssessment` uses this record.

## Checks

Do the standard checks (README section 2). The PR adds three templates. No
existing template changes.

## Assumptions

1. An Exposure row names either `biospecimen_id` or `individual_id`. Curator
   cannot enforce "exactly one", because it drops rules (see M4). A QC
   script checks this.
2. A mixture (several articles in one exposure) is several Exposure rows
   with the same biospecimen and timing.

## Open questions

1. Add `route_of_administration` (NCIT or CDISC route terms through NCIT) for
   in vivo exposures? The slot is standard for animal dosing. It is not in
   the current scope of M8.
2. Should `TestArticle` reuse `TherapeuticAgentEnum` as it is (clinical drug
   names)? Or should the shared vocabulary get a neutral name, for example
   `AgentEnum`, because test articles include non-drug chemicals? A rename
   changes the PR #18 Treatment template.
