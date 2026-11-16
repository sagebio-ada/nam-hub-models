# M5 individual: Individual, Diagnosis, Treatment (plus `ext_ibd`)

**Decisions:** D4, D6, D10, D11 (keep the PR #18 keys), D15 (keep `ethnicity` and `reported_ancestry`, bind them to enums), D23 (keep the `aild` slot).

## Scope

Fix the PR #18 record templates and bind their slots to enums. Add no new templates.

## Starting point

PR #18 has these templates:

- `Individual`: `study_id`, `individual_id`, `species` (NCBITaxon), `sex` (male, female, unknown), `ethnicity` and `reported_ancestry` (free text), `strain`, `genotype`.
- `Diagnosis`: `diagnosis` (`DiagnosisEnum`: IBD diagnoses and healthy control, MONDO and NCIT), `age_at_diagnosis`, `age_unit`.
- `IBDDiagnosis` (is_a `Diagnosis`): `aild` (MONDO-anchored, multivalued).
- `Treatment`: `therapeutic_agent` (NCIT), `therapeutic_response`, `therapeutic_response_criteria`, `therapeutic_drug_level`, `therapeutic_drug_level_unit` (free text).

Merge the PR #18 review fixes first (README section 5; M0, "Fixed in PR #18 and PR #22"). They include these fixes:

- `Diagnosis` gets the key `study_id` + `individual_id` + `diagnosis` (PR #18 review, PR18-4). `Diagnosis` stays a separate link table. This keeps diagnosis data apart from the other data about the individual.
- Enum terms (PR #18 review, PR18-10; `docs/pr18_enum_terms.md` on the PR #18 branch):
  - `SexEnum` has male and female (PATO).
  - `AgeUnitEnum` and `TimeUnitEnum` use UO terms. "Days post-conception" gets UO "day" as a `broad_mappings` term.
  - `TherapeuticResponseEnum` has no term, because OLS has no NCIT term for responder or non-responder.

## Changes

One PR. The Curator output changes.

| Element | Change | Anchor (candidate) |
|---|---|---|
| `SexEnum` | Change "unknown" to "not reported". Reason: "unknown" and "not reported" are different values. The male and female terms come in PR #18. | NCIT "not reported" |
| `ethnicity` | Bind to an enum. | NCIT terms for the OMB categories (see open question 1) |
| `reported_ancestry` | Bind to an enum. Add values for each dataset. | HANCESTRO |
| `DiagnosisEnum` | Keep the generic name. Add values for each dataset, as `TissueEnum` does. Move the IBD-only usage guidance out of the descriptions. Reason: generic enum names must not carry IBD-only values. | MONDO; healthy control stays NCIT |
| `IBDDiagnosis` | Already in `ext_ibd.yaml` after M0 PR 1. Keep `aild` (D23). | — |
| `therapeutic_drug_level_unit` | Change from free text to an enum of concentration units. | UO (for example microgram per milliliter) |
| `TherapeuticResponseEnum` | Record the values as NAMHub-minted in the decision log. OLS has no term (PR18-10). | — |
| `TherapeuticAgentEnum` | Declare it as the shared agent vocabulary. M8 `TestArticle` uses it again. Add CHEBI and PubChem `exact_mappings` where they exist. | NCIT (done), CHEBI |
| Treatment descriptions | Move usage guidance (for example "add agents as datasets need them") to the decision log. | — |

M0 PR 2 adds the anchors for the classes and the other slots:

- `Individual` to C2M2 `subject`.
- `Diagnosis` to C2M2 `subject_disease` and GDC `diagnosis`.
- `Treatment` to GDC `treatment` and HTAN1 `Therapy`.

## Checks

Do the standard checks (README section 2). The Curator diff must show these changes only:

- `Individual`: `sex` values change. `ethnicity` and `reported_ancestry` become enums.
- `Diagnosis` and `IBDDiagnosis`: descriptions change.
- `Treatment`: the unit becomes an enum. Descriptions change.

The `Diagnosis` key is already in place from PR #18.

## Assumptions

1. Existing rows in datasets that are already ingested can be re-mapped by hand to the new `sex` value and to the `ethnicity` and `reported_ancestry` enums.
2. Animal comparator Individuals (D10) need only `species`, `strain`, `genotype` and `sex`.

## Open questions

1. Which ethnicity standard? GDC and dbGaP use the OMB 1997 categories (Hispanic or Latino, Not Hispanic or Latino). The 2024 OMB revision (SPD 15) combines race and ethnicity in one question. Recommendation: use the OMB 1997 categories through NCIT. The downstream repositories use them.
2. PR #18 has no `race` field. GDC, dbGaP and C2M2 all have one. Add `race` next to `ethnicity`, or leave it out?
3. `strain` is free text. Add an optional `strain_rrid` (pattern `^RRID:\S+$`, for example IMSR or MGI strain records)? An RRID is the standard reproducibility identifier for animal strains.
