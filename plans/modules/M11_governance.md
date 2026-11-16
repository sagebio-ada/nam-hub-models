# M11 governance: access requirements and data use

**Decisions:** D4, D11, D12

- D12: NAMHub will host controlled-access data. The MC2 AccessRequirement template is therefore needed.

## Scope

Model the Synapse access requirements. Reuse the MC2 governance module. PR #18 already does the DUO and license enums (PR18-6, PR18-7).

## Starting point

- `NAMs` has `access_type` (`AccessTypeEnum`), `access_requirements` (free text), `duo_code` (free text, multivalued), `acknowledgement_statements` and `license`.
- `Datasets` has `access_type`.
- `NAMPortalDataset` (PR #22) has `access_type`, `conditions_of_access`, `data_use_modifiers` and `license`.
- After the PR #18 review fixes (M0, "Fixed in PR #18 and PR #22"):
  - `data_use_modifiers` uses `DataUseModifierEnum` (22 DUO terms, checked in OLS).
  - `license` uses `LicenseEnum` (SPDX).
  - NAMs uses `data_use_modifiers`.
  - If a different process needs `duo_code`, it stays with the same enum and an `exact_mappings` to `data_use_modifiers`. PR18-6 asks the PR #18 author about this.
- The MC2 `modules/governance/` module has three templates:
  - `AccessRequirement`: `AccessRequirement_id` (the numeric ID of the Synapse AR), `contributorName`, `contributionDate`, `StudyKey`, `entityIdList`, `dataUseModifiers`.
  - `Resource`: annotation keys and values that activate an AR, and a registered schema URL.
  - A governance `Study`: de-identification type and method, dbGaP accession, index date, and participant and sample counts.

## Changes

One PR.

| Element | Change | Source and anchor (candidate) |
|---|---|---|
| `AccessRequirement` (new template) | Add `access_requirement_id` (Synapse AR ID; global), `contributor_name`, `contribution_date`, `study_id`, `entity_id_list` (Synapse IDs) and `data_use_modifiers`. Reuse the slot and enum from PR18-6. | MC2 `AccessRequirement` (names converted to NAMHub snake_case); Synapse AR |
| `access_requirement_id` link (new) on Datasets, NAMPortalDataset and NAMs | Replaces nothing. The `access_requirements` text stays as the human-readable summary. | MC2 `AccessRequirementKey` |
| `AccessTypeEnum` | Add `meaning` values (open, controlled, …) in M0 PR 2. | C2M2 or DUO, or log as minted |

## Checks

- The checks in README section 2.
- The new `AccessRequirement` template exists.
- Datasets, NAMPortalDataset and NAMs gain an optional link column.

## Assumptions

1. Access requirements are made in Synapse first and recorded here by ID, as in MC2. NAMHub does not make ARs from this table.

## Open questions

1. MC2 also has a `Resource` template. It drives automatic AR assignment from annotations. Does NAMHub need this automation, or only the AccessRequirement record?
2. The MC2 governance `Study` records de-identification type and method and a dbGaP accession. dbGaP and CRDC submission need these for controlled human data. Add them to the NAMHub Studies template (M1)?
3. Allow `access_requirement_id` on files, for files with a different AR from the rest of their dataset?
