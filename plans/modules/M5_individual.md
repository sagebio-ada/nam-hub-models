# M5 individual: Individual, Diagnosis, Treatment (plus `ext_ibd`)

**Decisions (README section 4):** D4, D6, D10, D11, D15, D23, D29, D30

## Scope

Fix the record templates on `main` and bind their slots to enums. Add no
new templates.

## Starting point

`main` has these templates:

- `Individual`: `study_id`, `individual_id`, `species` (NCBITaxon), `sex`,
  `ethnicity` and `reported_ancestry` (free text), `strain`, `genotype`.
- `Diagnosis`: key `study_id` + `individual_id` + `diagnosis`.
  `diagnosis` (`DiagnosisEnum`: IBD diagnoses and healthy control, MONDO
  and NCIT), `age_at_diagnosis`, `age_unit`.
- `IBDDiagnosis` (is_a `Diagnosis`): `aild` (MONDO-anchored, multivalued).
  It is in `ext_ibd.yaml` after M0 PR 1.
- `Treatment`: key `study_id` + `individual_id` + `therapeutic_agent`.
  `therapeutic_agent` (`TherapeuticAgentEnum`, NCIT),
  `therapeutic_response`, `therapeutic_response_criteria`,
  `therapeutic_drug_level`, `therapeutic_drug_level_unit` (free text).

Enum terms on `main`:

- `SexEnum`: male and female (PATO). "unknown" has no term.
- `AgeUnitEnum` and `TimeUnitEnum`: UO. "days post-conception" has UO "day"
  as a `broad_mappings` term.
- `TherapeuticResponseEnum`: no terms. OLS has no term for responder or
  non-responder.

## Changes

One PR. The Curator output changes (major version: a value changes).

| Element | Change | Anchor (candidate) |
|---|---|---|
| `SexEnum` | Keep "unknown" and give it its term. Add "not reported" and "not applicable" from the shared set (D29). M0 PR 3 adds them if it runs first. Reason: "unknown" (not known or not determined) and "not reported" (not given by the submitter) are different gaps. | `NCIT:C17998`, `NCIT:C43234`, `NCIT:C48660` |
| `ethnicity` | Bind to an enum, with the D29 missing values. | NCIT terms for the OMB categories (see open question 1) |
| `reported_ancestry` | Bind to an enum, with the D29 missing values. Add values for each dataset. | HANCESTRO |
| `DiagnosisEnum` | Keep the generic name. Add values for each dataset, as `TissueEnum` does. Move the IBD-only usage guidance out of the descriptions. Reason: a generic enum must not carry guidance for one disease. M3 reuses the enum for `modeled_disease`; `diagnosis` keeps the donor role (D30). | MONDO; healthy control stays NCIT |
| `therapeutic_drug_level_unit` | Change from free text to a new `ConcentrationUnitEnum`. M8 reuses this enum for doses. | UO (for example microgram per milliliter) |
| `TherapeuticResponseEnum` | Record the values as NAMHub-minted in the decision log. | — |
| `TherapeuticAgentEnum` | Make it the shared agent vocabulary. M8 `TestArticle` uses it again (see open question 4). Add CHEBI and PubChem `exact_mappings` where they exist. | NCIT (on `main`), CHEBI |
| Treatment descriptions | Move usage guidance (for example "add agents as datasets need them") to the decision log. | — |

M0 PR 2 adds the anchors of the classes and the other slots.

## Checks

Do the standard checks (README section 2). The Curator diff shows only these
changes:

- `Individual`: `sex` gains missing values. `ethnicity` and `reported_ancestry`
  become enums.
- `Diagnosis` and `IBDDiagnosis`: descriptions change.
- `Treatment`: the unit becomes an enum. Descriptions change.

## Assumptions

1. Existing rows in datasets that are already ingested can be re-mapped by
   hand to the new `sex` value and to the `ethnicity` and
   `reported_ancestry` enums.
2. Animal comparator Individuals (D10) need only `species`, `strain`,
   `genotype` and `sex`.

## Open questions

1. Which ethnicity standard? GDC and dbGaP use the OMB 1997 categories
   (Hispanic or Latino, Not Hispanic or Latino). The 2024 OMB revision
   (SPD 15) combines race and ethnicity in one question. Recommendation: use
   the OMB 1997 categories through NCIT. The downstream repositories use
   them.
2. `main` has no `race` field. GDC, dbGaP and C2M2 all have one. Add `race`
   next to `ethnicity`, or leave it out?
3. `strain` is free text. Add an optional `strain_rrid` (pattern
   `^RRID:\S+$`, for example IMSR or MGI strain records)? An RRID is the
   standard reproducibility identifier for animal strains.
4. Test articles include chemicals that are not drugs. Rename
   `TherapeuticAgentEnum` to a neutral name (for example `AgentEnum`) in
   this PR, before M8 uses it? The rename changes the enum name only. The
   Treatment column and its values stay the same. Recommendation: yes.
