# M1 program: Investigation, Studies, Grants, People, Publications, Landscape

**Decisions (README section 4):** D4, D6, D11, D13, D26, D27, D28, D33, D34, D41

## Scope

The existing portal tables stay, with their names, because they back live
Synapse tables. This module:

1. Adds two study-design fields to Studies.
2. Binds the free-text institution and funder fields to enums with ROR IDs.
3. Adds the `Investigation` record, which holds the institution. Each Study
   links to one Investigation (D34).

Do not add a `program` slot (D13 is on hold). M0 PR 2 adds the anchors of
the existing slots.

## Starting point

| Template | Synapse table | Keys |
|---|---|---|
| Studies | syn75404711 | `study_id` |
| Datasets (M2; retired by D39) | syn75404713 | `dataset_id` |
| People | syn75404714 | `investigator_id`; links `study_id`, `grant_id` |
| Grants | syn75404715 | `grant_id` |
| Publications | syn75404744 | `pub_med_id`; links `study_id`, `grant_id`, `nam_id` |
| Landscape | none (form) | `landscape_id` |
| Investigation (new) | none | `investigation_id` |

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
| Investigation, People | `institution` | Bind to a new `InstitutionEnum`. Each value has its ROR ID as `meaning`. Add values for each study (D6a). | ROR; schema.org `affiliation` | enum (multivalued on People) |
| Grants | `funding_agency` | Bind to `FunderEnum`. Change the close mapping to `funder` into an exact mapping. | ROR (through `FunderEnum`) | enum, multivalued |
| Studies | `institution` | Remove. It moves to `Investigation` (D27). People keeps `institution` (personal affiliation). | — | — |
| Studies | `funding_agency` | Remove. `Grants.funding_agency` gives it through `grant_id`. | — | — |
| Studies | `grant_id` | Make multivalued. Give each funder a Grants row. | FUSION `funded_by` | link → Grants, multivalued |
| Studies | `investigation_id` (new) | Required. The Investigation that the study belongs to. | FUSION `investigation` | link → Investigation |
| Studies | `metadata_license` (new) | Metadata licence of the study (D28). Every record reaches it through `study_id`. | FAIR rubric metric 18 | `LicenseEnum` |

### `Investigation` (new; global `investigation_id`)

One funded center's programme of studies. `class_uri` `OBI:0000066`. Exact
mappings: `ndhcc:Investigation` and `isa:investigation`. NDHCC is the
FUSION (NDHCC) LinkML model, version 1.2.0-wave2r4 (D33).

| Slot | Required | Range | Description | Anchor / FUSION slot |
|---|---|---|---|---|
| `investigation_id` | yes | text | Key. Use the `<Institution>-<Program>` prefix that `landscape_id` uses, so that Landscape rows link to the Investigation with no new column. | `landscape_prefix`, `source_identifier` |
| `investigation_name` | yes | text | Name of the programme of studies. | `title` |
| `description` | no | text | (existing slot) | `description` |
| `institution` | yes | `InstitutionEnum` (ROR) | The organization that carries out the investigation. Moved from Studies (D27). | TDC `institution` |
| `consortium_role` | no | new `ConsortiumRoleEnum`: technology development center, data hub, coordinating center, validation partner | The role of the organization in its consortium. | `consortium_role` (values verbatim) |

Grants stay on Studies only (`Studies.grant_id`; FUSION Study `funded_by`).
An investigation reaches its grants through its studies.

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

Studies holds the grant and the metadata licence for every dataset and
file of the study. Studies reaches the institution through
`investigation_id` (M0 FAIR field map).

## Checks

- The checks in README section 2.
- The Curator diff shows only these changes:
  - Studies gains `study_design`, `experimental_factor` and
    `metadata_license` (optional).
  - The new `Investigation` template.
  - Studies gains `investigation_id` (required), and loses `institution`
    and `funding_agency`. `grant_id` becomes multivalued.
  - `institution` becomes an enum on Investigation and People.
  - `funding_agency` becomes an enum on Grants.
- The prefix of each `landscape_id` is an `investigation_id`.

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
2. `nams_tech_focus` on Studies is free text. Bind it to the `nam_kind`
   enum (M3, D41)? This changes live table values. This plan leaves it out
   until approved.
3. People holds `email`. People is also the contact for the datasets of a
   study (FAIR rubric metric 16; M0 FAIR field map). Is the table public?
   If not, which public field gives the contact?
4. Some values on `main` repeat values that a key already reaches (D27):
   - `Studies.funding_agency` repeats `Grants.funding_agency` through
     `grant_id`. Resolved: this plan removes `Studies.funding_agency` and
     makes `Studies.grant_id` multivalued, with one Grants row for each
     funder.
   - `People.grant_id` and `Publications.grant_id` repeat
     `Studies.grant_id` through `study_id`, if a person or a publication
     always has the grant of its study.

   Remove the second repeat from the live tables? Recommendation: keep
   `People.grant_id` and `Publications.grant_id` if a person or a
   publication can have a grant that is not the grant of its study.
5. `Studies.institution` moves to `Investigation`. A study with a lead
   institution that differs from the organization of its investigation
   loses that value. Keep an optional `Studies.institution` for that case?
   Recommendation: no. Record it in People (`institution` of the study
   leads).
