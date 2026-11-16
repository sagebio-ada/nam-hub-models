# M6 biospecimen: Biospecimen

**Decisions:** D2, D4, D6, D11, D23 (IBD fields go to `ext_ibd`), D25b (structured timepoints). One slot (the protocol link) waits for D24.

## Scope

Fix and extend the PR #18 `Biospecimen` template:

- Add derivation steps.
- Add structured timepoints.
- Move the IBD fields to the extension.

The `tissue` slot cleanup is done in PR #18 (PR #18 review, PR18-12). `tissue` is one multivalued `TissueEnum` slot, also on `Biospecimen`. A biospecimen can come from, or model, more than one tissue. The in vitro model fields are in the M4 PR, which runs after this PR.

## Starting point

PR #18 has these slots: `study_id`, `biospecimen_id`, `individual_id`, `parent_biospecimen_id`, `biospecimen_type`, `tissue` (multivalued `TissueEnum`, PR18-12), `cell_type`, `cell_line`, `cellosaurus_id`, `culture_condition`, `culture_duration` and its unit, `timepoint` (free text), `age_at_collection`, `age_unit`, `endoscopic_status`, `sample_title`.

## Changes

One PR. The Curator output changes.

| Element | Change | Source / anchor (candidate) |
|---|---|---|
| `derivation_method` (new) | How the biospecimen was made from its parent: sectioning, dissociation, nuclei isolation, differentiation, extraction, and others | OBI planned-process terms; MC2 Part E |
| `timepoint` | Keep as the label (for example "baseline", "week 8") | ISA factor value; HTAN timepoint label |
| `timepoint_offset` (new) | Numeric time from the reference event | HTAN "days from index"; ISA factor value with unit |
| `timepoint_offset_unit` (new) | `TimeUnitEnum` | UO |
| `timepoint_reference_event` (new) | Enrollment, diagnosis, birth, first treatment, culture start, and others | MC2 `studyIndexDate` values, extended for in vitro |
| `endoscopic_status` | Move to an `IBDBiospecimen` template (is_a `Biospecimen`) in `ext_ibd.yaml`. Reason: IBD-only fields must not stay on the generic template. | MC2 and HTAN extension pattern |
| `culture_condition` | Narrow the description to culture and differentiation conditions. Test-article exposures go to M8. | — |
| `sample_title` | Add a mapping to GEO `Sample_title` (M0 PR 2). | GEO |
| Protocol link | Waits for D24. | — |

Keep these unchanged:

- The keys.
- The `parent_biospecimen_id` chain (one row for each physically distinct stage).
- `age_at_collection` and `age_unit`.

## Checks

Do the standard checks (README section 2). The Curator diff must show these changes only:

- `Biospecimen` gains four optional columns and loses `endoscopic_status`.
- A new `IBDBiospecimen` template has the columns of the new `Biospecimen` template plus `endoscopic_status`.

## Assumptions

1. IBD datasets that already use `Biospecimen` can switch to `IBDBiospecimen`. The `endoscopic_status` values move unchanged.
2. Offsets are recorded for each biospecimen, not for each individual. Different individuals can then use different reference events.

## Open questions

1. Moving `endoscopic_status` makes IBD submitters change templates. Is this acceptable now, or must `endoscopic_status` stay on `Biospecimen` until the next IBD submission?
2. GDC, HTAN and MC2 all record how a specimen was preserved (frozen, FFPE, fresh, and others). Preservation affects the quality of sequencing and imaging. Add an optional `preservation_method` (OBI or NCIT) in this PR?
