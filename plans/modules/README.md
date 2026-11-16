# NAMHub model refactor: module plans

These files are the implementation specifications for the NAMHub LinkML
model refactor. Each module plan gives its scope, starting point, changes,
PRs, checks, assumptions and open questions. Each plan refers to the
decisions in this file as D1 to D25.

## 1. Goal

Represent NAMs, experiments, protocols, results, analyses, computational
models and simulations, provenance and governance in the NAMHub model. The
model must support experimental reproducibility and the submission of NAM
data to the FDA. The model starts from the templates of PR #18 and PR #22,
which come from datasets that NAMHub ingests now. The refactor anchors these
templates to existing standards and extends them.

The structure comes from three standards:

- **ISA:** the experimental graph (source, sample, extract, data, joined by
  processes that use protocols).
- **C2M2 (CFDE):** the catalog form (namespaced IDs, standard file fields,
  file-to-biosample and file-to-collection links).
- **NAMO (Monarch Initiative):** the NAM types and the data to record for
  each type.

These documents set which fields must exist:

- FDA, *General Considerations for the Use of New Approach Methodologies in
  Drug Development* (CDER, March 2026, draft). Sections B (human biological
  relevance), C (technical characterization) and D (fit for purpose).
- FDA, *Assessing the Credibility of Computational Modeling and Simulation in
  Medical Device Submissions* (CDRH, November 2023, final).
- FDA, *Considerations for the Use of Artificial Intelligence to Support
  Regulatory Decision-Making for Drug and Biological Products* (CDER and
  others, January 2025, draft).
- FDA and EMA, *Guiding Principles of Good AI Practice in Drug Development*
  (January 2026).
- The CFDE FAIR rubric on FAIRshake (18 metrics).

## 2. Rules for every plan

- **Sourcing principle.** NAMHub does not define new concepts. Each class,
  slot and enum value gets one of these anchors, in this order of
  preference:
  1. An existing IRI: `class_uri`, `slot_uri` or `meaning`.
  2. A mapping (`exact_mappings`, `close_mappings`, `broad_mappings`,
     `narrow_mappings`). NAMO (at a pinned commit), C2M2 fields and MC2
     attributes are referenced this way.
  3. A document reference: `see_also` (a stable URL) and `source` (the
     document and section).
  4. NAMHub-minted, only when nothing above applies. The decision log
     records the reason.

  Examine each ontology ID in OLS before use. Search without an ontology
  filter first. IDs in these plans are candidates until this check.
- **Source rule.** Use only documents that NAMHub can read in full. Do not
  use proprietary standards (for example ASME V&V 40, ISO 10991, ISO/IEC
  22989) or public copies of them. Where an FDA guidance adapts such a
  definition, use the FDA text.
- **Schema style.** Each `description` is one definitional line. Schema
  files contain no rationale, history or TODOs. Rationale goes in
  `docs/model_decisions.md`.
- **Documentation style.** Plans, the decision log and schema descriptions
  follow ASD-STE100 Simplified Technical English.
- **Existing templates.** Keep a PR #18 element when it agrees with an
  established standard. Use the standard when it is better.
- **Restricted content.** The NAMHub landscape review has restricted access.
  Do not copy its content into the repository. Cite it only as "NAMHub
  landscape review (restricted access; contents not reproduced)".
- **Keys and links.** See M0, PR 3. A link that can point outside Synapse
  (`parent_file_id`, `comparator_dataset_id`) accepts a Synapse ID, a CURIE
  or a URL.
- **Checks for every PR:**
  - `uv run linkml-lint src/namhub/schema`
  - `uv run curator-lint src/namhub/schema/namhub.yaml`
  - `uv run gen-curator -d <dir> src/namhub/schema/namhub.yaml`, then a
    diff of the generated Curator JSON against the previous build.
  - A PR that changes the Curator output increases `version:`. Synapse
    registration does not accept a version that is already registered.
- **Implementation.** One PR at a time, each with an independent review
  before it is opened.

## 3. Tool behavior that the plans depend on

These facts were tested on copies of the schema (linkml-curator v0.4.0):

- `class_uri`, `slot_uri`, mappings, `see_also` and enum `meaning` do not
  change the generated Curator JSON. They appear in the JSON-LD.
- A schema split into several files with relative imports gives the same
  Curator JSON, and `linkml-lint` passes on the directory.
- `gen-curator` drops LinkML `rules` without a warning. A conditional
  requirement (for example "required when `biospecimen_type` is cell line")
  must be a QC script, unless linkml-curator adds support.
- `gen-curator` cannot use dynamic enums (`reachable_from`). The enum
  becomes empty, and `curator-lint` gives an error.
- Integers become text with the pattern `^-?[0-9]+$`, and `minimum_value`
  is removed. Thus a minimum of 0 is not enforced
  ([linkml-curator #13](https://github.com/Sage-Bionetworks/linkml-curator/issues/13)).
- Property keys are PascalCase (`StudyId`). There is no option for other
  forms.
- `linkml-lint` (`canonical_prefixes`) expects EFO and EDAM on their
  identifiers.org namespaces.

## 4. Decisions

| ID | Decision | Reason |
|---|---|---|
| D1 | Merge PR #18 and PR #22, with the review fixes (section 5), before the module PRs. Version 4.0.0. | Datasets in ingestion use these templates now. The fixes remove and change columns, so the version is a major version. |
| D2 | In vitro model instances are Biospecimen rows. The FDA C.5 and C.8 fields are optional Biospecimen columns. Microphysiological devices are a separate record. | PR #18 and CELLxGENE (`tissue_type`) record models as samples. One device lot serves many biospecimens. |
| D3 | File-to-file and NAM-to-NAM links are key columns. The provenance build derives process nodes from these keys. Submitters do not enter process nodes. | Flat Curator templates cannot hold a process graph. Keys agree with C2M2 and HTAN2. |
| D4 | Keep the PR #18 key names (`<entity>_id`), and use the same form for new templates. One generic `parent_file_id`, not one key for each level. | The names work as primary and foreign keys. They agree with C2M2 and HTAN2 (`HTAN_PARENT_ID`). Submitters use them now. |
| D5 | Assays: OBI term as `meaning`, with BAO terms as `exact_mappings`. | C2M2 uses OBI. FAIRshake metric 10 asks for BAO. |
| D6 | Large vocabularies: (a) static enums, extended for each dataset, for fields that submitters fill; (b) CURIE text with a `pattern` for very large lists (Cellosaurus, CHEBI). | Curator needs static lists (section 3). Some ontologies are too large for a list. |
| D7 | NAMO is used through mappings at a pinned commit. NAMO is not imported. | NAMO is not released and changes often. |
| D8 | Required FDA fields: only the minimum set in the M4, M8 and M9 plans. All other FDA fields are optional. Change this when contributors give feedback. | The FDA guidances are not binding. |
| D9 | Credibility of models: FDA guidance only (CDRH 2023 for mechanistic models, CDER 2025 AI draft for data-driven models). Explainability is optional free text. | Source rule. The FDA–EMA principles 7 and 10 ask for explainability. |
| D10 | Animal comparator data is in scope. Animals are Individuals of a non-human species with `strain` and `genotype`. | The FDA NAM guidance compares NAMs with animal studies. PR #18 already records animals this way. |
| D11 | IDs: study-scoped (`study_id` + local ID) for records; global for catalog entries that cross studies, as `nam_id` is now. M4 open question 2 confirms the scope of `device_id`, `test_article_id` and `protocol_id`. | Agrees with C2M2. No renumbering of PR #18 records. |
| D12 | NAMHub will host controlled-access data. | Needs the access-requirement record (M11). |
| D13 | FAIRsharing registration and program name: on hold. | — |
| D14 | One implementation plan for each module. The provenance build has a separate plan. | Small, reviewable PRs. |
| D15 | Keep `ethnicity` and `reported_ancestry`, and bind them to enums. | Downstream repositories (GDC, dbGaP) use these fields. |
| D16 | Model risk has three levels: low, medium, high. | The FDA AI draft guidance uses three levels. |
| D17 | Performance values: one row for each metric and data split, or fixed columns. **Open.** | Rows hold confidence intervals, which the FDA AI draft guidance asks for. Fixed columns are simpler. Blocks M9. |
| D18 | MIFlowCyt and FCS papers can be used. Cite by DOI and use field names only. | The papers are free to read in full. |
| D19 | Paired modalities (for example multiome RNA and ATAC from one library) use `paired_file_id`. | An explicit link is clearer than a shared biospecimen. |
| D20 | Add `comparator_dataset_id` to dataset templates. | NAM data is often compared with patient or reference data. |
| D21 | Clinical and sample tables are `SupportingFile` files, with Individual, Diagnosis and Treatment records for the structured fields. No new template. | PR #18 already gives these tables a home. |
| D22 | HTAN2 mappings use a pinned commit. | HTAN2 changes often and has no IRIs. |
| D23 | Keep the `aild` slot on `IBDDiagnosis`. | Easier for submitters than extra Diagnosis rows. The value "No" cannot be a row. |
| D24 | Protocols: a `Protocol` record with `protocol_id`, or a link column. **Open.** | A record holds type, version and parameters once, for many files, biospecimens and exposures. A link is simpler. Blocks M7 and one slot in M3, M6, M8 and M10. |
| D25a | File IDs are Synapse IDs, made automatically on upload. Submitters do not assign file IDs. | Synapse makes IDs for all entities. |
| D25b | `timepoint` becomes a label plus a numeric offset, a UO unit and a reference event. | Timepoints become comparable across studies. |

## 5. PR #18 and PR #22 review

The reviews ask for fixes before these PRs merge (D1). Every module plan
starts after these fixes:

- [PR #18 review](https://github.com/sagebio-ada/nam-hub-models/pull/18#pullrequestreview-5929310530)
- [PR #22 review](https://github.com/sagebio-ada/nam-hub-models/pull/22#pullrequestreview-5929311249)
- Enum terms and the DUO and license enums: `docs/pr18_enum_terms.md` on
  the PR #18 branch.

M0 lists the fixes ("Fixed in PR #18 and PR #22"). The review did not add
class and slot anchors; M0 PR 2 adds them.

## 6. Status

| Module | Plan | Status |
|---|---|---|
| M0 core: module split, anchors, shared mixins, keys | [M0_core.md](M0_core.md) | Ready |
| M1 program: Studies, People, Grants, Publications, Landscape | [M1_program.md](M1_program.md) | Ready |
| M2 dataset: Datasets, NAMPortalDataset | [M2_dataset.md](M2_dataset.md) | Ready |
| M3 NAM catalog | [M3_nam.md](M3_nam.md) | Ready. One slot waits for D24 |
| M4 model: Biospecimen model fields, devices, in silico models | [M4_model.md](M4_model.md) | Ready |
| M5 individual: Individual, Diagnosis, Treatment | [M5_individual.md](M5_individual.md) | Ready |
| M6 biospecimen | [M6_biospecimen.md](M6_biospecimen.md) | Ready. One slot waits for D24 |
| M7 protocol | — | Not started. Waits for D24 |
| M8 exposure: TestArticle, Exposure, ReferenceCompoundSet | [M8_exposure.md](M8_exposure.md) | Ready. One slot waits for D24 |
| M9 validation: context of use, validation, performance | — | Not started. Waits for D17 |
| M10 file: shared File and sequencing templates | [M10_file.md](M10_file.md) | Ready. `protocol_link` waits for D24 |
| M10 further assay families | — | Not started. One plan for each family, after M10 |
| M11 governance | [M11_governance.md](M11_governance.md) | Ready |
| Provenance build and exports | — | Not started. Separate plan (D14), after M0 to M10 |

## 7. Order

1. PR #18 and PR #22 merge, with the review fixes (D1).
2. M0 PR 1 (module split), then M0 PR 2 (decision log and anchors).
3. M5, M6 and M10 change the existing PR #18 templates.
4. M1, M2 and M11 are small and independent.
5. M3 and M4 change the live NAMs table and add model records.
6. M8 follows M4.
