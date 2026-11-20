# NAMHub model refactor: module plans

These files are the implementation specifications for the NAMHub LinkML
model refactor. Each module plan gives its scope, starting point, changes,
PRs, checks, assumptions and open questions. Each plan refers to the
decisions in section 4 as D1 to D25.

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
- The CFDE FAIR rubric on FAIRshake (18 metrics). The plans use it as a
  checklist of fields that the Curator metadata must hold.

## 2. Rules for every plan

- **Sourcing principle.** NAMHub does not define new concepts. Each class,
  slot and enum value gets one of these anchors, in this order of
  preference:
  1. An existing IRI: `class_uri`, `slot_uri` or `meaning`.
  2. A mapping (`exact_mappings`, `close_mappings`, `broad_mappings`,
     `narrow_mappings`). NAMO (at the pinned commit, D7), C2M2 fields and
     MC2 attributes are referenced this way.
  3. A document reference: `see_also` (a stable URL) and `source` (the
     document and section).
  4. NAMHub-minted, only when nothing above applies. The decision log
     records the reason.

  Examine each ontology ID in OLS before use. Search without an ontology
  filter first. IDs in these plans are candidates until this check.
- **Enum terms.** Put an exact term in `meaning`. Put a wider term in
  `broad_mappings` and a narrower term in `narrow_mappings`.
- **Source rule.** Use only documents that NAMHub can read in full. Do not
  use proprietary standards (for example ASME V&V 40, ISO 10991, ISO/IEC
  22989) or public copies of them. Where an FDA guidance adapts such a
  definition, use the FDA text.
- **Schema style.** Each `description` is one definitional line. Schema
  files contain no rationale, history or TODOs. Rationale goes in
  `docs/model_decisions.md`.
- **Documentation style.** Plans, the decision log and schema descriptions
  follow ASD-STE100 Simplified Technical English.
- **Existing templates.** Keep an element on `main` when it agrees with an
  established standard. Use the standard when it is better.
- **Restricted content.** The NAMHub landscape review has restricted access.
  Do not copy its content into the repository. Cite it only as "NAMHub
  landscape review (restricted access; contents not reproduced)".
- **Curator metadata only (D26).** No plan depends on a pipeline or a
  build that derives values. A value that an FDA or FAIR check needs must
  be in the Curator metadata. A value that a record reaches through a key
  column counts as present.
- **Normalization (D27).** Store each value once, on the record that owns
  it. Other records reach it through key columns. Do not add a column that
  repeats a value that a key already reaches. Store a property of an enum
  value (for example the platform of an instrument model) once, on the enum
  value.
- **Keys and links.** M0 PR 2 gives the key conventions. In summary:
  - Store each relation once, on the dependent row. Do not add the reverse
    link. Example: `Datasets.nam_id` links a dataset to a NAM. NAMs has no
    `dataset_id`.
  - A link that can point outside Synapse accepts a Synapse ID, a CURIE or
    a URL. These links are `parent_file_id`, `comparator_dataset_id`,
    `training_dataset_id`, `calibration_dataset_id`, `tuning_dataset_id`,
    `pretraining_dataset_id`, `test_dataset_id` and `evidence_dataset_id`.
- **Checks for every PR:**
  - `uv run linkml-lint src/namhub/schema`
  - `uv run curator-lint src/namhub/schema/namhub.yaml`
  - `uv run gen-curator -d <dir> src/namhub/schema/namhub.yaml`, then a
    diff of the generated Curator JSON against the build from `main`.
  - A PR that changes the Curator output increases `version:`. Removing or
    changing a column, a value or a key increases the major version. Adding
    optional columns or values increases the minor version. Synapse
    registration does not accept a version that is already registered.
  - Example records for each template that the PR changes, validated
    against the generated Curator JSON. Valid examples must pass. Invalid
    examples must fail: a record that has only one field, a value that is
    not in the enum, an assay value that belongs to a
    different template, a blank required value, and an empty list in a
    required multivalued field. Record what an unknown column does, because
    the generated JSON does not close `additionalProperties` (section 3).
- **Implementation.** One PR at a time, each with an independent review
  before it is opened.

## 3. Tool behavior that the plans depend on

These facts were tested on copies of the schema (linkml-curator v0.4.0):

- `class_uri`, `slot_uri`, mappings, `see_also` and enum `meaning` do not
  change the generated Curator JSON. They appear in the JSON-LD.
- A schema split into several files with relative imports gives the same
  Curator JSON, and `linkml-lint` passes on the directory.
- `gen-curator` drops LinkML `rules` without a warning. Curator cannot
  enforce a conditional requirement (for example "required when
  `biospecimen_type` is cell line"). Section 8, question 1 covers these
  checks.
- `gen-curator` ignores enum `inherits` and `include`. The inherited or
  included values do not appear in the Curator JSON, and there is no
  warning. An enum must list all its values itself.
- The generated Curator JSON does not set `additionalProperties: false`,
  and every key link is a plain string. Curator does not check that a
  linked row exists (section 8, question 1).
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
| D1 | **Done.** PR #18 and PR #22 merged with the review fixes, as version 4.0.0 (17 November 2026). | Datasets in ingestion use these templates now. The fixes removed and changed columns, so the version is a major version. |
| D2 | In vitro model instances are Biospecimen rows. The FDA C.5 fields are optional Biospecimen columns. Microphysiological device types are a separate record. | `main` and CELLxGENE (`tissue_type`) record models as samples. One device type serves many biospecimens. |
| D3 | File-to-file and NAM-to-NAM links are key columns. Submitters do not enter process nodes. | Flat Curator templates cannot hold a process graph. Keys agree with C2M2 and HTAN2. |
| D4 | Keep the key names on `main` (`<entity>_id`), and use the same form for new templates. One generic `parent_file_id`, not one key for each level. | The names work as primary and foreign keys. They agree with C2M2 and HTAN2 (`HTAN_PARENT_ID`). Submitters use them now. |
| D5 | Assays: OBI term as `meaning`, with BAO terms as `exact_mappings`. | C2M2 uses OBI. FAIRshake metric 10 asks for BAO. |
| D6 | Large vocabularies: (a) static enums, extended for each dataset, for fields that submitters fill; (b) CURIE text with a `pattern` for very large lists (Cellosaurus, CHEBI). | Curator needs static lists (section 3). Some ontologies are too large for a list. |
| D7 | NAMO is used through mappings at a pinned commit (`2dba2a3`, the commit that these plans were checked against). NAMO is not imported. | NAMO is not released and changes often. |
| D8 | Required FDA fields: only the minimum set in the M4, M8 and M9 plans. All other FDA fields are optional. Change this when contributors give feedback. | The FDA guidances are not binding. |
| D9 | Credibility of models: FDA guidance is the primary source (CDRH 2023 for mechanistic models, CDER 2025 AI draft for data-driven models, the FDA NAM guidance for all NAMs). OECD documents are secondary sources for points that the FDA guidance does not cover: the (Q)SAR validation principles and the (Q)SAR Assessment Framework, GIVIMP (GD 286), GD 211, the test guidelines and the GLP principles. Explainability is optional free text. | Source rule: the OECD documents are free to read in full. They give modality-specific detail (in vitro methods, (Q)SAR) that the FDA guidance does not. The FDA–EMA principles 7 and 10 ask for explainability. |
| D10 | Animal comparator data is in scope. Animals are Individuals of a non-human species with `strain` and `genotype`. | The FDA NAM guidance compares NAMs with animal studies. `main` already records animals this way. |
| D11 | IDs: study-scoped (`study_id` + local ID) for records; global for catalog entries that cross studies, as `nam_id` is now. M0 open question 1 confirms the scope of the other catalog IDs. | Agrees with C2M2. No renumbering of existing records. |
| D12 | NAMHub will host controlled-access data. | Needs the access-requirement record (M11). |
| D13 | FAIRsharing registration and program name: on hold. | — |
| D14 | One implementation plan for each module. No provenance build is planned, and no module plan depends on one. | Small, reviewable PRs. |
| D15 | Keep `ethnicity` and `reported_ancestry`, and bind them to enums. | Downstream repositories (GDC, dbGaP) use these fields. |
| D16 | Model risk has three levels: low, medium, high. | The FDA AI draft guidance uses three levels. |
| D17 | Performance, QC and validation values are rows: one result for each target, metric and data split, with its method and version, value, unit or scale, confidence interval, acceptance criterion, date and status. No result is a true/false column. | Rows hold confidence intervals, which the FDA AI draft guidance asks for. Several results for one target can coexist, each with its method and date. |
| D18 | MIFlowCyt and FCS papers can be used. Cite by DOI and use field names only. | The papers are free to read in full. |
| D19 | Paired modalities (for example multiome RNA and ATAC libraries made from the same nuclei) use `paired_file_id`. | An explicit link is clearer than a shared biospecimen. |
| D20 | Add `comparator_dataset_id` to the dataset record (M2). | NAM data is often compared with patient or reference data. |
| D21 | Clinical and sample tables are `SupportingFile` files, with Individual, Diagnosis and Treatment records for the structured fields. No new template. | `main` already gives these tables a home. |
| D22 | HTAN2 mappings use a pinned commit. | HTAN2 changes often and has no IRIs. |
| D23 | Keep the `aild` slot on `IBDDiagnosis`. | Easier for submitters than extra Diagnosis rows. The value "No" cannot be a row. |
| D24 | Protocols are `Protocol` records with a global `protocol_id` (M7). NAMs, Biospecimen, Exposure, every file level and SOP documents link to them. Each row names the protocol that made it: wet-lab protocols for Level 1 files, computational protocols (pipelines, notebooks) for Level 2 and above. `protocol_link` and the workflow fields move onto the records. | A record holds type, version and parameters once, for many files, biospecimens and exposures (D27). |
| D25a | File IDs are Synapse IDs, made automatically on upload. Submitters do not assign file IDs. | Synapse makes IDs for all entities. |
| D25b | `timepoint` becomes a label plus a numeric offset, a UO unit and a reference event. | Timepoints become comparable across studies. |
| D26 | No pipeline. Every value that an FDA or FAIR check needs is in the Curator metadata. A value reached through a key column counts as present. The FAIRshake rubric is a checklist of fields for the Curator metadata. | No pipeline for derived values is planned. Validation reads the Curator metadata. |
| D27 | Normalize. Store each value once, on the record that owns it. Other records reach it through keys. | One source for each value. Copies cannot disagree. |
| D28 | The metadata licence is stored on Studies, one value for each study (`metadata_license`, M1). | The metadata of a study usually has one licence. Every record reaches it through `study_id` (D27). |
| D29 | One shared set of missing values: not reported (`NCIT:C43234`), not collected (`GENEPIO:0001620`), not applicable (`NCIT:C48660`), unknown (`NCIT:C17998`). An enum that needs a missing value uses only values from this set. Each enum lists them itself (section 3). | A required field never forces an invented value. The reason for a gap stays visible. The set follows the INSDC missing-value terms. |
| D30 | Keep source and modeled descriptors apart. Individual and source Biospecimen rows give where material came from (species, tissue, donor diagnosis). NAMs gives what a model represents (`species`, `tissue`, `modeled_disease`, `modeled_phenotype`). A model Biospecimen row gives its modeled tissue; its parent rows give the origin. | An iPSC-derived liver organoid has skin as its origin and liver as its modeled tissue. The donor diagnosis is not the modeled disease. |
| D31 | Record every mapping to another model or ontology (NAMO, C2M2, HTAN2, CELLxGENE, the FUSION knowledge base model, enum terms) in `docs/mappings.sssom.tsv`, with its relation, justification, confidence, review state and the pinned version of the target. The schema holds the CURIE; the SSSOM row holds why. A NAMO mapping is `skos:exactMatch` only when a reviewer accepts that the definitions agree. | One machine-readable place for the reason and the review state of each mapping. SSSOM is the standard table format for mappings. |
| D32 | Record the evidence for metadata values in the model (M12): one `Assertion` row for each value (source, location, quoted text, original and normalized value, method, review state), one `CurationRun` row for each extraction or curation run, and `CurationProfile` rows for the extraction rules and how they combine. | Curator and Curie extract metadata from source documents, and the metadata goes to the FUSION knowledge base, which keeps evidence for each value. Without these records the evidence is lost before submission (D26). |

## 5. Starting point

Every module plan starts from `main` at commit `cb4206a` (version 4.0.0).
This commit includes PR #18 and PR #22 with the fixes from their reviews:

- [PR #18 review](https://github.com/sagebio-ada/nam-hub-models/pull/18#pullrequestreview-5929310530)
- [PR #22 review](https://github.com/sagebio-ada/nam-hub-models/pull/22#pullrequestreview-5929311249)
- `docs/pr18_enum_terms.md` gives the enum terms and the DUO and license
  enums.

Each plan describes the parts of `main` that it changes. If `main` changes
before a module PR starts (for example, PR #19 merges), the PR starts from
the latest `main`.

## 6. Status

| Module | Plan | Status |
|---|---|---|
| PR #18 and PR #22 | — | Merged (D1) |
| M0 core: module split, anchors, key conventions, FAIR field map | [M0_core.md](M0_core.md) | Ready |
| M1 program: Studies, People, Grants, Publications, Landscape | [M1_program.md](M1_program.md) | Ready |
| M2 dataset: Datasets, NAMPortalDataset | [M2_dataset.md](M2_dataset.md) | Ready |
| M3 NAM catalog | [M3_nam.md](M3_nam.md) | Ready |
| M4 model: Biospecimen model fields, culture protocols, devices, in silico models | [M4_model.md](M4_model.md) | Ready |
| M5 individual: Individual, Diagnosis, Treatment | [M5_individual.md](M5_individual.md) | Ready |
| M6 biospecimen | [M6_biospecimen.md](M6_biospecimen.md) | Ready |
| M7 protocol | [M7_protocol.md](M7_protocol.md) | Ready |
| M8 exposure: TestArticle, Exposure, ReferenceCompoundSet, ReferenceCompound | [M8_exposure.md](M8_exposure.md) | Ready |
| M9 validation: context of use, validation, credibility, results | [M9_validation.md](M9_validation.md) | Ready |
| M10 file: shared File and sequencing templates | [M10_file.md](M10_file.md) | Ready |
| M10 further assay families: imaging, plate readouts, mass spectrometry, in silico outputs and code (`SoftwareArtifact`), and others | — | Not started. One plan for each family, after M10 |
| M11 governance | [M11_governance.md](M11_governance.md) | Ready |
| M12 provenance: Assertion, CurationRun, CurationProfile | [M12_provenance.md](M12_provenance.md) | Ready |
| Provenance build | — | Not planned (D14). No module plan depends on it |

## 7. Order

1. M0 PR 1 (module split), then M0 PR 2 (decision log and anchors).
2. M7 adds the `Protocol` record, which M3, M4, M6, M8 and M10 link to.
3. M5, M6 and M10 change the existing sequencing and record templates.
4. M1, M2, M11 and M12 are small and independent. M12 needs the M0
   mappings file (D31).
5. M3 and M4 change the NAMs table and add model records. M4 starts after
   M6.
6. M8 follows M4 and M5.
7. M9 follows M3, M4, M7, M8 and M12.

## 8. Open questions across modules

1. **Checks that Curator cannot enforce.** Curator drops conditional rules
   (section 3). These rules need a check after upload:
   - M4: `cell_source_type` and `lot_number` (or `catalog_number`) on the
     source row of each in vitro model (D8).
   - M4: the data-driven fields of `InSilicoModel` when `model_form` is
     data-driven or hybrid.
   - M8: each Exposure row names exactly one of `biospecimen_id` and
     `individual_id`, and names a `test_article_id` unless `exposure_type`
     is physical stimulation.
   - All modules: every key link names an existing row (`study_id`,
     `individual_id`, `biospecimen_id`, `parent_biospecimen_id`,
     `dataset_id`, `nam_id`, `protocol_id`, `device_id`, `test_article_id`,
     `reference_compound_set_id`, `access_requirement_id`, `parent_file_id`
     when it is a Synapse ID). D26 counts values reached through keys as
     present, so a broken link is missing data.
   - All modules: no identifier names two different rows in one study, and
     no global identifier names two different rows.
   - D29: the missing-value copies in each enum match the shared set.
   - M12: each `Assertion` names an existing record and field, its `value`
     equals the value in that record, and a computed value names a
     protocol.
   - M9: an `AssessmentResult` has `value` or `value_text`, and a numeric
     result agrees with its criterion and `outcome`. A validation or
     credibility comparator dataset is not a training, tuning or
     calibration dataset of the same model. `AICredibilityAssessment` is
     only for data-driven or hybrid models, and a hybrid model has one
     assessment under each FDA framework.

   Options:
   - (a) A QC script in this repository that reads the uploaded records
     from Synapse and reports failures.
   - (b) `if/then` support in linkml-curator (a separate repository; needs
     approval).

   Which option, and who owns the check? Recommendation: (a) now, and (b)
   as a feature request.
