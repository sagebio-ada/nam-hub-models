# M1 program: Studies, Grants, People, Publications, Landscape

**Decisions:** D4, D11, D13

- D4 and D11: Keep the existing keys.
- D13: On hold. Do not add a `program` slot yet.

## Scope

The existing portal tables stay, with their names, because they back live Synapse tables. This module adds three study-design fields and an institution identifier. M0 PR 2 adds their anchors.

## Starting point

| Template | Synapse table | Keys |
|---|---|---|
| Studies | syn75404711 | `study_id` |
| Datasets (M2) | syn75404713 | `dataset_id` |
| People | syn75404714 | `investigator_id`; links `study_id`, `grant_id` |
| Grants | syn75404715 | `grant_id` |
| Publications | syn75404744 | `pub_med_id`; links `study_id`, `grant_id`, `nam_id` |
| Landscape | none (form) | `landscape_id` |

The NAMHub portal reads Studies from `syn75904610` and Datasets from `syn76283922`. It does not read them from the tables above. PR #18 review, PR18-13 asks the PR #18 author if this is intentional. This plan uses the table IDs from the answer.

The PR #18 and PR #22 review fixes merge first (M0, "Fixed in PR #18 and PR #22"). For this module:

- ID titles use the form "Study ID" (PR18-11).
- PR #22 binds `disease_focus` to `DiseaseFocusEnum`. The enum holds NAMHub disease areas, with MONDO or EFO terms (PR18-10 and PR #22 review, PR22-3).

## Changes

One PR.

| Template | Slot | Definition source and anchor (candidates) | Range |
|---|---|---|---|
| Studies | `study_design` | ISA `studyDesignDescriptors`; OBI and EFO study-design terms | enum, grown for each study |
| Studies | `experimental_factor` | ISA Factor; EFO experimental factor terms | enum, multivalued |
| Studies | `institution_ror` | ROR ID; schema.org `affiliation` | pattern `^https://ror\.org/0[a-z0-9]{8}$` |
| People | `institution_ror` | as above | as above |

- Keep the free-text `institution` slot as the display label.
- Start `study_design` and `experimental_factor` with the values that current studies need. Give each value a `meaning` that OLS confirms.
- Make `institution_ror` a pattern string (D6b). ROR is too large to list as an enum.

**Reason for `experimental_factor`:** Studies has no field for the experimental factors of a study. ISA records them as study factors.

## Checks

- The checks in README section 2.
- The Studies and People Curator JSON gain three optional columns. All other templates stay the same.

## Assumptions

1. Optional columns on Studies and People do not break the live Synapse tables. The schema manages their columns separately (ARIE-112 separated the schema from Synapse registration).
2. A study whose design has no OBI or EFO term gets the value "other" until a term is found.

## Open questions

1. PR #19 updates the Publications fields. PR #22 has a public review. PR #19 has none. Build on PR #19 after it merges, or review it against these rules first?
2. `nams_tech_focus` and `funding_agency` on Studies are free text. PR #22 binds `disease_focus`.
   - Bind `nams_tech_focus` to the M3 `nam_type` enum here? This changes live table values. This plan leaves it out until approved.
   - `funding_agency` has a close equivalent in the PR #22 `funder` slot (`FunderEnum`, with a ROR ID). It stays free text until the dataset templates merge.
3. People holds `email`. Is that table restricted to the backend? If it is public, drop `email` from the portal view?
