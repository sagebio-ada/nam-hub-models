# M6 biospecimen: Biospecimen

**Decisions (README section 4):** D2, D4, D6, D11, D24, D25b, D27, D29, D30, D33, D36

## Scope

Fix and extend the `Biospecimen` template on `main`:

- Link each biospecimen to the protocols that made it.
- Add structured timepoints and biological replicate groups.
- State the role of `tissue` and `cell_type` (D30).
- Move the IBD-only field to the IBD extension.
- Replace `nam_id` with `model_system_id`, and remove the type-level model
  fields (D36).

This PR runs after M7 (Protocol). The in vitro model fields are in M4,
which runs after this PR.

## Starting point

`Biospecimen` on `main` has these slots: `study_id`, `biospecimen_id`,
`individual_id` (required), `parent_biospecimen_id` (multivalued),
`biospecimen_type`, `tissue` (multivalued `TissueEnum`), `cell_type`,
`cell_line`, `cellosaurus_id`, `culture_condition`, `culture_duration` and
its unit, `timepoint` (free text), `age_at_collection`, `age_unit`,
`endoscopic_status`, `sample_title`.

`culture_condition` is described as "in vitro culture, differentiation or
exposure conditions".

## Changes

One PR. The Curator output changes (major version: a column moves).

| Element | Change | Source and anchor (candidate) |
|---|---|---|
| `protocol_id` (new, multivalued) | The protocols that made the biospecimen from its parent (M7). The `protocol_type` of each protocol gives the derivation step (sectioning, dissociation, nuclei isolation, differentiation, extraction, culture, and others). Do not add a separate `derivation_method` column: it would repeat `protocol_type` (D27). | C2M2 `biosample.sample_prep_method` (through `protocol_type`); MC2 Part E |
| `timepoint` | Keep as the label (for example "baseline", "week 8"). | ISA factor value; HTAN timepoint label |
| `timepoint_offset` (new) | Numeric time from the reference event. | HTAN "days from index"; ISA factor value with unit |
| `timepoint_offset_unit` (new) | `TimeUnitEnum`. | UO |
| `timepoint_reference_event` (new) | New `TimepointReferenceEventEnum`: enrollment, diagnosis, birth, treatment or exposure start, culture start, other. | MC2 `studyIndexDate` values, extended for in vitro |
| `endoscopic_status` | Move to a new `IBDBiospecimen` template (is_a `Biospecimen`) in `ext_ibd.yaml`. Reason: an IBD-only field must not stay on the generic template. | MC2 and HTAN extension pattern |
| `culture_condition` | Change the description to culture and differentiation conditions. Test-article exposures go to M8 `Exposure`. | — |
| `tissue` | Change the description (D30). On a source row (tissue, primary cells, cell line), it is the anatomical origin. On a model row (organoid, engineered tissue, in vitro differentiated cells), it is the modeled tissue, as CELLxGENE does. A model row reaches its modeled descriptors (`species`, `tissue`, `cell_type`, `modeled_disease`, `modeled_phenotype`) through `model_system_id`. The parent rows give the origin. | CELLxGENE `tissue`; UBERON |
| `cell_type` | Change the description (D30): the cell types in the biospecimen (input role). The cell types that an assay observes belong to the assay file templates. | CL |
| `nam_id` | Replace with `model_system_id` (link to `ModelSystem`, M4). Blank on source rows. The model system gives the type-level descriptors of a model row. | — |
| `cell_source_type`, `three_d_architecture`, `coculture_configuration`, `vendor`, `catalog_number` | Do not put these on Biospecimen or `IBDBiospecimen`. They sit on `ModelSystem` (M4). | — |
| `biological_replicate_group` (new) | A label shared by biospecimens that are biological replicates of one condition. The existing `technical_replicate_group` on files groups technical replicates. | EFO biological replicate (candidate); FDA NAM guidance (reproducibility) |

M8 `Exposure` reuses the three timepoint slots for the start of an
exposure. Put them in `core.yaml` (M0 PR 1 rule).

Keep these unchanged:

- The keys.
- The `parent_biospecimen_id` chain (one row for each physically distinct
  stage).
- `age_at_collection` and `age_unit`.

### FUSION mapping (D33)

Source: the FUSION (NDHCC) LinkML model, version 1.2.0-wave2r4.

- `Biospecimen` and `IBDBiospecimen` are exact mappings to `ndhcc:Sample`.
- `biological_replicate_group` maps to the FUSION `ReplicateKindEnum` value
  `biological_replicate`.
- `technical_replicate_group` (on files) maps to the FUSION
  `ReplicateKindEnum` value `technical_replicate`.

## Checks

Do the standard checks (README section 2). The Curator diff shows only these
changes:

- `Biospecimen` gains five optional columns and loses `endoscopic_status`.
  `nam_id` becomes `model_system_id` (blank on source rows).
  The descriptions of `culture_condition`, `tissue` and `cell_type`
  change.
- `TimepointReferenceEventEnum` has the D29 missing values that apply.
- A new `IBDBiospecimen` template has the columns of the new `Biospecimen`
  template plus `endoscopic_status`.

## Assumptions

1. IBD datasets that already use `Biospecimen` can switch to
   `IBDBiospecimen`. The `endoscopic_status` values move unchanged.
2. Offsets are recorded for each biospecimen, not for each individual. Thus
   biospecimens of one study can use different reference events.

## Open questions

1. Moving `endoscopic_status` makes IBD submitters change templates. Is this
   acceptable now, or must `endoscopic_status` stay on `Biospecimen` until
   the next IBD submission?
2. GDC, HTAN and MC2 all record how a specimen was preserved (frozen, FFPE,
   fresh, and others). Preservation affects the quality of sequencing and
   imaging. Add an optional `preservation_method` (OBI or NCIT terms) in
   this PR? Recommendation: yes.
