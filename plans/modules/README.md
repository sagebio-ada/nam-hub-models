# NAMHub model refactor: module plans

These files are the implementation specifications for the NAMHub LinkML
model refactor. Each module plan gives its scope, starting point, changes,
PRs, checks, assumptions and open questions. Each plan refers to the
decisions in section 4 as D1 to D41.

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

### Path of the metadata

Submitters and the Curie extraction tool fill the NAMHub templates in
Curator. Curie extracts values from source documents (protocols,
notebooks, publications, spreadsheets). The templates, with the evidence
for each value (M12), go to the FUSION knowledge base. The FUSION (NDHCC)
LinkML model is the base model. The NAMHub templates are its Curator
projection (D33). `docs/mappings.sssom.tsv` maps the NAMHub templates and
slots to it at a pinned version (D31). NAMHub does not write to the
knowledge base.

### Alignment with the FUSION model

The plans adopt these FUSION design principles. Each is a NAMHub decision
or a module change, so the plans stand alone:

| FUSION principle | NAMHub decision or plan |
|---|---|
| Context of use as a first-class record; model influence, decision consequence and risk | D38; M9 `ContextOfUse` (model influence, decision consequence), `CredibilityAssessment` (risk). The FDA texts are the source, not proprietary standards |
| Results are method-qualified rows, never true/false; thresholds are data | D17; M9 `AssessmentResult`, `AcceptanceCriterion` |
| Source versus modeled descriptors; input versus observed values | D30; M4 `ModelSystem` (`modeled_disease`, `modeled_phenotype`); M6 `tissue`, `cell_type` |
| A gap has a stated reason | D29 (missing values); M12 `resolution_state` |
| Per-value evidence: source, location, quoted text, original and normalized value, method, review state | D32; M12 `Assertion` |
| Curation profiles and how they combine; a run names its resolved specification | D32; M12 `CurationProfile`, `CurationRun` |
| Mappings carry relation, justification and review state; NAMO is never assumed equal by name | D7, D31 |
| Protocols are versioned records; data processing runs a protocol | D24; M7, M10 `ComputationalProtocol` |
| No physical instance is inferred from a plan or a class | M4 (Biospecimen rows only for materials that exist) |
| Controls, replicates and non-chemical interventions | M8 `control_role`, `exposure_type`; M6 `biological_replicate_group` |
| Credibility frameworks for each modality | D9 (FDA primary; OECD secondary) |
| Validation in levels: schema, references, semantics, domain | Section 2 checks; section 8, question 1 |
| The FUSION model is the base model; NAMHub templates are its Curator projection | D33; the table "NAMHub record → FUSION class" below |
| ISA backbone: Investigation → Study → Assay → Dataset → File | D34; M1 `Investigation`; M2 `Assay` |
| A NAM is a plan specification that a Study develops; other studies use it through an Assay | D35; M3 `NAMs.study_id`; M2 `Assay.nam_id` |
| The NAM, its system (model system or device) and its sample are separate records | D36; M4 `ModelSystem`, `MicrophysiologicalDevice`; M6 `Biospecimen` |
| Controlled enum values and a conflict as two assertions | D37; M12 `Assertion` |
| Context-of-use elements: decision supported, model influence, decision consequence, biomarker category, use tags | D38; M9 `ContextOfUse` |
| One Dataset class; one modality-neutral CredibilityAssessment; NAM kind | D39, D40, D41; M2 `NAMPortalDataset`; M9 `CredibilityAssessment`; M3 `nam_kind` |

The FUSION (NDHCC) LinkML model, version 1.2.0-wave2r4, is the pinned
target. The v2 context-of-use and QC modules at version 1.3.0-wave3f1.1 are
also pinned.

Each NAMHub record maps to one FUSION class (`ndhcc:` is the NDHCC
LinkML namespace):

| NAMHub record | FUSION (NDHCC) class | Relation |
|---|---|---|
| Investigation | `ndhcc:Investigation` (with `ndhcc:TechnologyDevelopmentCenter` for the organization slots) | exact |
| Studies | `ndhcc:Study` | exact |
| Grants | `ndhcc:Grant` | exact |
| People | `ndhcc:Person` | exact |
| Publications | `ndhcc:Publication` | exact |
| Landscape | `ndhcc:LandscapeSurveyRecord` | exact |
| Assay | `ndhcc:Assay` | exact |
| NAMPortalDataset | `ndhcc:Dataset` | exact |
| NAMs | `ndhcc:NAM` | exact |
| ModelSystem | `ndhcc:ModelSystem` | exact |
| MicrophysiologicalDevice | `ndhcc:Device` | exact |
| InSilicoModel | `ndhcc:Software` | close |
| Protocol, CultureProtocol, ComputationalProtocol | `ndhcc:ProtocolVersion` (one row is one version) | exact |
| Individual | `ndhcc:Source` | exact |
| Diagnosis, IBDDiagnosis, Treatment | `ndhcc:ClinicalObservation` (`observation_kind` diagnosis or therapy) | close |
| Biospecimen, IBDBiospecimen | `ndhcc:Sample` | exact |
| TestArticle | the `agent` of `ndhcc:Exposure` (a `ControlledValue` bound to CHEBI, with `dsstox_id`) | close |
| Exposure | `ndhcc:Exposure`, or `ndhcc:Intervention` when `exposure_type` is not chemical | close |
| ReferenceCompoundSet, ReferenceCompound | `ndhcc:ReferenceOrComparator` (a reference chemical set) | broad |
| ContextOfUse | `ndhcc:ContextOfUse` | exact |
| AcceptanceCriterion | `ndhcc:AcceptanceCriterion` (`ndhcc:QCThreshold` when scoped to an assay and level) | exact |
| AssessmentResult | `ndhcc:AssessmentResult` (`ndhcc:QualityAssessment` for QC rows) | exact |
| CredibilityAssessment | `ndhcc:CredibilityAssessment` | exact |
| AICredibilityAssessment | `ndhcc:InSilicoCredibility` | close |
| CredibilityEvidence | `ndhcc:CredibilityEvidence` | exact |
| SupportingFile and the sequencing file templates | `ndhcc:DataFile` | exact |
| AccessRequirement | `ndhcc:AccessCondition` | close |
| Assertion | `ndhcc:ControlledValue` with `ndhcc:SourceLocator` (and `ndhcc:EvidenceRecord`) | close |
| CurationRun | `ndhcc:AssertionActivity` | close |
| CurationProfile | none | — |

The plans differ from FUSION in these places:

- One LinkML source generates the Curator templates. No field exists in a
  template without a slot in the model.
- NAMHub keys are the submitter's IDs (D4, D11). FUSION mints its own IRIs
  and keeps the submitter's ID as `source_identifier`.
- A Curator column holds one normalized value. The original value, the
  resolution state and the review state of that value are `Assertion` rows
  (M12), not an inlined FUSION `ControlledValue`.
- The plans do not use the ASME V&V 40 framing (source rule). The FDA
  CDRH 2023 guidance gives the same concepts.

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
    link. Example: `Assay.nam_id` links an assay to a NAM. NAMs has no
    `assay_id`.
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
- `linkml-validate` (linkml 1.11.1, JSON Schema plugin) enforces LinkML
  `rules` (preconditions and postconditions) and `exactly_one_of` on each
  record. It does not report a link to a row that does not exist, and it
  does not report a duplicate `unique_keys` value. The LinkML reference
  validator (`linkml_runtime.processing.referencevalidator`) fails on a
  schema with `rules`; without rules, it did not report either error.
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
| D2 | In vitro model instances are Biospecimen rows. Microphysiological device types are a separate record. Model system types are `ModelSystem` records (D36). The FDA C.5 fields that describe the type move to `ModelSystem`. The instance fields stay on Biospecimen as optional columns. | `main` and CELLxGENE (`tissue_type`) record models as samples. One device type serves many biospecimens. |
| D3 | File-to-file and NAM-to-NAM links are key columns. Submitters do not enter process nodes. | Flat Curator templates cannot hold a process graph. Keys agree with C2M2 and HTAN2. |
| D4 | Keep the key names on `main` (`<entity>_id`), and use the same form for new templates. One generic `parent_file_id`, not one key for each level. | The names work as primary and foreign keys. They agree with C2M2 and HTAN2 (`HTAN_PARENT_ID`). Submitters use them now. |
| D5 | Assays: OBI term as `meaning`, with BAO terms as `exact_mappings`. | C2M2 uses OBI. FAIRshake metric 10 asks for BAO. |
| D6 | Large vocabularies: (a) static enums, extended for each dataset, for fields that submitters fill; (b) CURIE text with a `pattern` for very large lists (Cellosaurus, CHEBI). | Curator needs static lists (section 3). Some ontologies are too large for a list. |
| D7 | NAMO is used through mappings at a pinned commit (`2dba2a3`, the commit that these plans were checked against). NAMO is not imported. | NAMO is not released and changes often. |
| D8 | Required FDA fields: only the minimum set in the M4, M8 and M9 plans. All other FDA fields are optional. Change this when contributors give feedback. | The FDA guidances are not binding. |
| D9 | Credibility of models: FDA guidance is the primary source (CDRH 2023 for mechanistic models, CDER 2025 AI draft for data-driven models, the FDA NAM guidance for all NAMs). OECD documents are secondary sources for points that the FDA guidance does not cover: the (Q)SAR validation principles and the (Q)SAR Assessment Framework, GIVIMP (GD 286), GD 211, the test guidelines and the GLP principles. Explainability is optional free text. | Source rule: the OECD documents are free to read in full. They give modality-specific detail (in vitro methods, (Q)SAR) that the FDA guidance does not. The FDA–EMA principles 7 and 10 ask for explainability. |
| D10 | Animal comparator data is in scope. Animals are Individuals of a non-human species with `strain` and `genotype`. | The FDA NAM guidance compares NAMs with animal studies. `main` already records animals this way. |
| D11 | IDs: study-scoped (`study_id` + local ID, for example `assay_id`) for records; global for catalog entries that cross studies, as `nam_id`, `investigation_id` and `model_system_id` are. M0 open question 1 confirms the scope of the other catalog IDs. | Agrees with C2M2. No renumbering of existing records. |
| D12 | NAMHub will host controlled-access data. | Needs the access-requirement record (M11). |
| D13 | FAIRsharing registration and program name: on hold. | — |
| D14 | One implementation plan for each module. No provenance build is planned, and no module plan depends on one. | Small, reviewable PRs. |
| D15 | Keep `ethnicity` and `reported_ancestry`, and bind them to enums. | Downstream repositories (GDC, dbGaP) use these fields. |
| D16 | Model risk has three levels: low, medium, high. The pair of model influence and decision consequence is on `ContextOfUse` (D38). | The FDA AI draft guidance uses three levels. |
| D17 | Performance, QC and validation values are rows: one result for each target, metric and data split, with its method and version, value, unit or scale, confidence interval, acceptance criterion, date and status. No result is a true/false column. | Rows hold confidence intervals, which the FDA AI draft guidance asks for. Several results for one target can coexist, each with its method and date. |
| D18 | MIFlowCyt and FCS papers can be used. Cite by DOI and use field names only. | The papers are free to read in full. |
| D19 | Paired modalities (for example multiome RNA and ATAC libraries made from the same nuclei) use `paired_file_id`. | An explicit link is clearer than a shared biospecimen. |
| D20 | Replaced by D40. Earlier text: add `comparator_dataset_id` to the dataset record (M2). | NAM data is often compared with patient or reference data. |
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
| D30 | Keep source and modeled descriptors apart. Individual and source Biospecimen rows give where material came from (species, tissue, donor diagnosis). `ModelSystem` gives what a model represents (`species`, `tissue`, `cell_type`, `modeled_disease`, `modeled_phenotype`). A model Biospecimen row reaches them through `model_system_id`. | An iPSC-derived liver organoid has skin as its origin and liver as its modeled tissue. The donor diagnosis is not the modeled disease. |
| D31 | Record every mapping to another model or ontology (NAMO, C2M2, HTAN2, CELLxGENE, the FUSION knowledge base model, enum terms) in `docs/mappings.sssom.tsv`, with its relation, justification, confidence, review state and the pinned version of the target. The schema holds the CURIE; the SSSOM row holds why. A NAMO mapping is `skos:exactMatch` only when a reviewer accepts that the definitions agree. | One machine-readable place for the reason and the review state of each mapping. SSSOM is the standard table format for mappings. |
| D32 | Record the evidence for metadata values in the model (M12): one `Assertion` row for each value (source, location, quoted text, original and normalized value, method, review state), one `CurationRun` row for each extraction or curation run, and `CurationProfile` rows for the extraction rules and how they combine. | Curator and Curie extract metadata from source documents, and the metadata goes to the FUSION knowledge base, which keeps evidence for each value. Without these records the evidence is lost before submission (D26). |
| D33 | The FUSION (NDHCC) LinkML model is the base model. The NAMHub templates are its Curator projection. Each NAMHub class and slot gets an `exact_mappings`, `close_mappings` or `broad_mappings` CURIE to the NDHCC class or slot that it projects, at the pinned version. Start from the slot mappings of the FUSION Curator projection (release 1.1.0), which maps 80 of the 85 slots on `main`. The SSSOM row holds the reason (D31). Where NDHCC uses an ISA, OBI or IAO IRI for a class, the NAMHub class uses the same IRI. | NAMHub builds on FUSION and does not replace it. The knowledge base then reads the templates without a second model. |
| D34 | Use the ISA backbone of FUSION: Investigation → Study → Assay → Dataset → File. Add `Investigation` (M1, global `investigation_id`) and `Assay` (M2, study-scoped `assay_id`). | In FUSION the Assay is the hub: it realizes one NAM in one Study, runs on the NAM's systems, carries the context of use, and produces the datasets. NAMHub had these links on three records. |
| D35 | A NAM is a separate record that one Study develops (FUSION `developed_by_study`). `NAMs.study_id` is required and means "the study that develops this NAM". Other studies use a NAM through `Assay.nam_id`. `nam_id` stays global. | FUSION keeps NAM (a plan specification, IAO:0000104) apart from Study (OBI:0000066) and keys each NAM by its developing study. |
| D36 | Model system types are `ModelSystem` records (M4, global `model_system_id`). They hold the type-level descriptors: species, tissue, cell type, modeled disease and phenotype, organization level, cell source, 3D architecture, co-culture configuration, vendor and catalog number. NAMs link to them with `model_system_id` and to device types with `device_id` (FUSION `uses_system`). A model Biospecimen row is a physical instance and links to its type with `model_system_id`. | FUSION separates the NAM, the NAM system (ModelSystem or Device) and the Sample. One system type serves many NAMs and many specimens (D27). |
| D37 | Use the FUSION enum values verbatim for `resolution_state`, `review_state`, `planning_state`, assessment `status`, `control_role` (FUSION ControlKindEnum) and `confidence` (FUSION MappingConfidenceEnum). Model a conflict the FUSION way: two `Assertion` rows plus a check finding, not a value. FUSION missing-value tokens (`not_stated`, `not_assessed`, `not_applicable`) map to the D29 set in SSSOM; NAMHub enums keep the D29 values. | The values then need no crosswalk. D29 stays the one missing-value rule. |
| D38 | Use the FUSION context-of-use elements. `ContextOfUse` gains `decision_supported`, `model_influence` and `decision_consequence` (moved from `CredibilityAssessment`, FUSION `DecisionSupported`), `biomarker_category` (FDA-NIH BEST) and `use_tags` (FUSION UseTagEnum, the 11 values of the pinned version). `cou_category` (FDA NAM guidance A) stays. `CredibilityAssessment` keeps `model_risk` and its rationale (FUSION `ModelRisk`). | Model influence and decision consequence depend only on the context of use (FDA CDRH 2023). FUSION records them there. Both tag sets give a 1:1 map to FUSION and keep the FDA examples. |
| D39 | `NAMPortalDataset` is the only dataset record (FUSION has one Dataset class). The `Datasets` table (syn75404713) is retired, or kept only as a portal view generated from the Dataset entities, after a check of which portal pages read it. Every dataset, external datasets too, gets a Synapse Dataset entity. | The two records repeated title, description, study, format, DOI, access type, repository, external link and data type (D27). |
| D40 | One credibility record. `ValidationAssessment` folds into `CredibilityAssessment` (FUSION has one modality-neutral CredibilityAssessment with modality subtypes). Comparator data is recorded only on `CredibilityEvidence`. This replaces D20: `comparator_dataset_id` is removed from the dataset record. | One record for each NAM, context of use and framework. FUSION records the comparator with the evidence. |
| D41 | NAM classification uses the FUSION form: `nam_kind` (FUSION NAMKindEnum, required) and `namo_id` (kept from `main`; FUSION `namo_term`). `namo_class` and `namo_category` are removed, because NAMO gives them from `namo_id`. The M3 `nam_type` enum is not added. | Fewer slots, and the values map 1:1 to FUSION. |

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
| M1 program: Investigation, Studies, People, Grants, Publications, Landscape | [M1_program.md](M1_program.md) | Ready |
| M2 assay and dataset: Assay, NAMPortalDataset (`Datasets` retired, D39) | [M2_dataset.md](M2_dataset.md) | Ready |
| M3 NAM catalog | [M3_nam.md](M3_nam.md) | Ready |
| M4 model: ModelSystem, culture protocols, devices, in silico models | [M4_model.md](M4_model.md) | Ready |
| M5 individual: Individual, Diagnosis, Treatment | [M5_individual.md](M5_individual.md) | Ready |
| M6 biospecimen | [M6_biospecimen.md](M6_biospecimen.md) | Ready |
| M7 protocol | [M7_protocol.md](M7_protocol.md) | Ready |
| M8 exposure: TestArticle, Exposure, ReferenceCompoundSet, ReferenceCompound | [M8_exposure.md](M8_exposure.md) | Ready |
| M9 validation: context of use, credibility (`ValidationAssessment` folded in, D40), results | [M9_validation.md](M9_validation.md) | Ready |
| M10 file: shared File and sequencing templates | [M10_file.md](M10_file.md) | Ready |
| M10 further assay families: imaging, plate readouts, mass spectrometry, in silico outputs and code (`SoftwareArtifact`), and others | — | Not started. One plan for each family, after M10 |
| M11 governance | [M11_governance.md](M11_governance.md) | Ready |
| M12 provenance: Assertion, CurationRun, CurationProfile | [M12_provenance.md](M12_provenance.md) | Ready |
| Provenance build | — | Not planned (D14). No module plan depends on it |

## 7. Order

1. M0 PR 1 (module split), then M0 PR 2 (decision log and anchors).
2. M7 adds the `Protocol` record, which M3, M4, M6, M8 and M10 link to.
3. M5, M6 and M10 change the existing sequencing and record templates.
4. M1, M11 and M12 are small and independent. M12 needs the M0
   mappings file (D31). M1 adds `Investigation`, which Studies links to.
5. M3 and M4 change the NAMs table and add model records. M4 PR 1a adds
   `ModelSystem` first, because NAMs and Biospecimen link to it. M4 PR 1
   (Biospecimen fields) starts after M6.
6. M2 adds `Assay`. M2 follows M1, M3 and M4 PR 1a, because Assay links to
   Studies, NAMs and ModelSystem. `Assay.context_of_use_id` is a key
   column from the start; its link check starts when M9 PR 1 adds
   `ContextOfUse`.
7. M8 follows M4 and M5.
8. M9 follows M3, M4, M7, M8 and M12.

## 8. Open questions across modules

1. **Checks that Curator cannot enforce.** Curator drops conditional rules
   and does not check links (section 3). The checks fall in three groups.

   **(i) Rules about one record.** LinkML can state them, and
   `linkml-validate` enforces them (section 3):
   - M4: on a source row (cell line, primary cells), `cell_source_type`
     (on its `ModelSystem`) and one of `lot_number` or `catalog_number`
     (D8).
   - M4: the data-driven fields of `InSilicoModel` when `model_form` is
     data-driven or hybrid.
   - M8: each Exposure row names exactly one of `biospecimen_id` and
     `individual_id`, and names a `test_article_id` unless
     `exposure_type` is physical stimulation.
   - M9: an `AssessmentResult` has `result_value` or `value_text`, and has
     `outcome` when it names a criterion.

   **(ii) Rules across records.** LinkML cannot state them, and the LinkML
   validators do not check them (section 3):
   - Every key link names an existing row (`study_id`, `individual_id`,
     `biospecimen_id`, `parent_biospecimen_id`, `dataset_id`, `nam_id`,
     `investigation_id`, `assay_id`, `model_system_id`,
     `protocol_id`, `device_id`, `test_article_id`,
     `reference_compound_set_id`, `access_requirement_id`,
     `context_of_use_id`, `parent_file_id` when it is a Synapse ID). D26
     counts values reached through keys as present, so a broken link is
     missing data.
   - No identifier names two different rows in one study, and no global
     identifier names two different rows.
   - M12: each `Assertion` names an existing record and field, its `value`
     equals the value in that record, and a computed value names a
     protocol.
   - M9: a numeric result agrees with its criterion and `outcome`. A
     credibility comparator dataset is not a training,
     tuning or calibration dataset of the same model.
     `AICredibilityAssessment` is only for data-driven or hybrid models,
     and a hybrid model has one assessment under each FDA framework.

   **(iii) Rules about the schema.** They run in CI on the schema, not on
   records:
   - D29: the missing-value copies in each enum match the shared set.
   - D31: each mapping in the schema has a row in the SSSOM file.

   Options for (i) and (ii):
   - (a) State group (i) as LinkML `rules`, `exactly_one_of` and `any_of`
     in the schema. `gen-curator` drops them, so the Curator output does
     not change. Implement group (ii) as a custom `linkml-validate` plugin
     that reads `unique_keys` and the link slots from the schema. Run one
     `linkml-validate` command on records exported from Synapse (Curator
     keys mapped back to slot names).
   - (b) A separate QC script that holds all the rules in Python.
   - (c) `if/then` support in linkml-curator (a separate repository; needs
     approval), so that Curator enforces group (i) at entry.

   Recommendation: (a), and (c) as a feature request. With (a), the model
   holds every rule that LinkML can state. The rules are visible beside the
   slots, a schema change and its rules change together, and (c) can later
   move group (i) into Curator without a rewrite. Only group (ii) is code.
   Option (b) puts the rules outside the model, where they can drift from
   it. Who owns the export and the validation run is still open.
2. **Studies `institution` (M1).** `Studies.institution` moves to
   Investigation. A study with a lead institution that differs from the
   organization of its investigation loses that value. Keep an optional
   `Studies.institution` for that case? Recommendation: no. Record it in
   People (`institution` of the study leads).
3. **Animal models (M4).** Is `ModelSystem` also the record for an in vivo
   animal model type (strain, genotype), or do animals stay only on
   Individual (D10)? Recommendation: animals stay on Individual.
