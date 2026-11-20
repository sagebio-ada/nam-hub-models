# M11 governance: access requirements and data use

**Decisions (README section 4):** D4, D11, D12, D27, D33, D39

## Scope

Model the Synapse access requirements (ARs). Reuse the MC2 governance
module. D12 says that NAMHub will host controlled-access data, so the
AccessRequirement record is needed.

## Starting point

- `NAMs` has `access_type` (`AccessTypeEnum`), `access_requirements` (free
  text), `data_use_modifiers` (`DataUseModifierEnum`, 22 DUO terms),
  `acknowledgement_statements` and `license` (`LicenseEnum`, SPDX).
- `NAMPortalDataset` has `access_type` (required), `conditions_of_access`,
  `data_use_modifiers` and `license` (required).
- The MC2 `modules/governance/` module has three templates:
  - `AccessRequirement`: `AccessRequirement_id` (the numeric ID of the
    Synapse AR), `contributorName`, `contributionDate`, `StudyKey`,
    `entityIdList`, `dataUseModifiers`.
  - `Resource`: annotation keys and values that activate an AR, and a
    registered schema URL.
  - A governance `Study`: de-identification type and method, dbGaP
    accession, index date, and participant and sample counts.

## Changes

One PR. Put the new template in `modules/governance.yaml`.

| Element | Change | Source and anchor (candidate) |
|---|---|---|
| `AccessRequirement` (new template) | Slots: `access_requirement_id` (Synapse AR ID; global), `contributor_name`, `contribution_date`, `study_id` and `data_use_modifiers` (reuse the slot and enum). | MC2 `AccessRequirement` (names in NAMHub snake_case); Synapse AR |
| `access_requirement_id` link (new, multivalued) on NAMPortalDataset and NAMs | Multivalued, because Synapse allows more than one AR on an entity. | MC2 `AccessRequirementKey` |
| NAMs | Remove `access_type`, `access_requirements`, `data_use_modifiers` and `license`. NAMs keeps `access_requirement_id` and `acknowledgement_statements`. The FUSION NAM has one `access_condition` link, and the four removed values come from it. NAMPortalDataset keeps its access fields. | FUSION `access_condition` |

### FUSION mapping

`AccessRequirement` → `ndhcc:AccessCondition` (close). `data_use_modifiers`
→ `duo_terms`. NDHCC is the FUSION (NDHCC) LinkML model, version
1.2.0-wave2r4 (D33).

Do not copy the MC2 `entityIdList`. Synapse stores the entities of each AR,
and the dataset rows hold the link (one direction, README section 2).

## Checks

- The checks in README section 2.
- The Curator diff shows only these changes:
  - The new `AccessRequirement` template.
  - NAMPortalDataset and NAMs gain an optional link column.
  - NAMs loses `access_type`, `access_requirements`, `data_use_modifiers`
    and `license` (major version: columns are removed).

## Assumptions

1. Access requirements are made in Synapse first and recorded here by ID, as
   in MC2. NAMHub does not make ARs from this table.

## Open questions

1. MC2 also has a `Resource` template. It drives automatic AR assignment
   from annotations. Does NAMHub need this automation, or only the
   AccessRequirement record?
2. The MC2 governance `Study` records de-identification type and method and
   a dbGaP accession. dbGaP and CRDC submission need these for controlled
   human data. Add them to the NAMHub Studies template (M1)?
3. Allow `access_requirement_id` on files, for files with a different AR
   from the rest of their dataset?
4. After this PR, some values on NAMPortalDataset repeat what the AR
   record holds (D27):
   - `data_use_modifiers` on NAMPortalDataset, and on `AccessRequirement`.
   - The free-text summary `conditions_of_access` (NAMPortalDataset).

   (NAMs no longer has these values.) Store them only on
   `AccessRequirement`? An open dataset has no AR, but it can still have
   DUO terms. The portal facets read the annotations of the Dataset entity.
   Recommendation: store the DUO terms and the summary on
   `AccessRequirement` for controlled data. Keep `data_use_modifiers` on
   NAMPortalDataset only for open data with DUO terms. Confirm with the
   portal team before any change to the live annotations.
