# M1 program: Studies, Grants, People, Publications, Landscape

**Decisions (README section 4):** D4, D6, D11, D13, D26, D27, D28

## Scope

The existing portal tables stay, with their names, because they back live
Synapse tables. This module:

1. Adds two study-design fields to Studies.
2. Binds the free-text institution and funder fields to enums with ROR IDs.

Do not add a `program` slot (D13 is on hold). M0 PR 2 adds the anchors of
the existing slots.

## Starting point

| Template | Synapse table | Keys |
|---|---|---|
| Studies | syn75404711 | `study_id` |
| Datasets (M2) | syn75404713 | `dataset_id` |
| People | syn75404714 | `investigator_id`; links `study_id`, `grant_id` |
| Grants | syn75404715 | `grant_id` |
| Publications | syn75404744 | `pub_med_id`; links `study_id`, `grant_id`, `nam_id` |
| Landscape | none (form) | `landscape_id` |

- The portal reads Studies through the materialized view syn75904610, which
  reads syn75404711.
- `institution` (Studies, People) and `funding_agency` (Studies, Grants)
  are free text and multivalued.
- `funding_agency` has a close mapping to the PR #22 `funder` slot.
  `FunderEnum` gives each funder its ROR ID as `meaning`.
- `disease_focus` uses `DiseaseFocusEnum`, with MONDO, EFO and NCIT terms.

## Changes

One PR. The Curator output changes (major version: values become
constrained).

| Template | Slot | Change | Source and anchor (candidates) | Range |
|---|---|---|---|---|
| Studies | `study_design` (new) | Start with the values that current studies need. | ISA `studyDesignDescriptors`; OBI and EFO study-design terms | enum, grown for each study |
| Studies | `experimental_factor` (new) | Start with the values that current studies need. | ISA Factor; EFO experimental factor terms | enum, multivalued |
| Studies, People | `institution` | Bind to a new `InstitutionEnum`. Each value has its ROR ID as `meaning`. Add values for each study (D6a). | ROR; schema.org `affiliation` | enum, multivalued |
| Studies, Grants | `funding_agency` | Bind to `FunderEnum`. Change the close mapping to `funder` into an exact mapping. | ROR (through `FunderEnum`) | enum, multivalued |
| Studies | `metadata_license` (new) | Metadata licence of the study (D28). Every record reaches it through `study_id`. | FAIR rubric metric 18 | `LicenseEnum` |

- Give each `study_design` and `experimental_factor` value a `meaning` that
  OLS confirms.
- Before this PR merges, map the current `institution` and
  `funding_agency` values in the live tables to the enum values. Update the
  live tables as a separate, approved step.

**Reason for `experimental_factor`:** Studies has no field for the
experimental factors of a study. ISA records them as study factors.

**Reason for the enums:** One column holds both the display name and the
ROR ID, as `FunderEnum` does now. A separate ROR column must stay in step
with a multivalued name column, and the two lists can disagree. The PR #22
templates that `FunderEnum` comes from are now on `main`, so
`funding_agency` can use it.

Studies is the record that holds the grant, the institution and the
metadata licence for every dataset and file of the study (M0 FAIR field
map).

## Checks

- The checks in README section 2.
- The Curator diff shows only these changes:
  - Studies gains `study_design`, `experimental_factor` and
    `metadata_license` (optional).
  - `institution` becomes an enum on Studies and People.
  - `funding_agency` becomes an enum on Studies and Grants.

## Assumptions

1. Changes to optional columns and to values do not break the live Synapse
   tables. The schema manages their columns separately (ARIE-112 separated
   the schema from Synapse registration).
2. Each current institution and funder has a ROR record.
3. A study whose design has no OBI or EFO term gets the value "other" until
   a term is found.

## Open questions

1. PR #19 updates the Publications fields. PR #22 had a public review. PR #19
   has none. Build on PR #19 after it merges, or review it against these
   rules first?
2. `nams_tech_focus` on Studies is free text. Bind it to the M3 `nam_type`
   enum? This changes live table values. This plan leaves it out until
   approved.
3. People holds `email`. People is also the contact for the datasets of a
   study (FAIR rubric metric 16; M0 FAIR field map). Is the table public?
   If not, which public field gives the contact?
4. Some values on `main` repeat values that a key already reaches (D27):
   - `Studies.funding_agency` repeats `Grants.funding_agency` through
     `grant_id`. But `Studies.grant_id` holds one grant, and a study can
     have more than one funder.
   - `People.grant_id` and `Publications.grant_id` repeat
     `Studies.grant_id` through `study_id`, if a person or a publication
     always has the grant of its study.

   Remove these repeats from the live tables? Recommendation: first make
   `Studies.grant_id` multivalued and give every funder a Grants row. Then
   remove `Studies.funding_agency`. Keep `People.grant_id` and
   `Publications.grant_id` if a person or a publication can have a grant
   that is not the grant of its study.
