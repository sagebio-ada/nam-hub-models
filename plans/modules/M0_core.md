# M0 core: module split, anchors, key conventions

**Decisions (README section 4):** D3, D4, D6, D11, D13, D25a, D26, D27, D28,
D29, D30, D31

## Scope

1. Split `namhub.yaml` into module files. Do not change the generated output.
2. Make `docs/model_decisions.md`.
3. Add anchors to every existing element. Do not change the generated output.
4. Write the key conventions and the FAIR field map that later modules use.
5. Make `docs/mappings.sssom.tsv` (D31).
6. Apply the shared missing values (D29) to the existing enums.

## Starting point

`main` at `cb4206a`, version 4.0.0 (README section 5):

- `src/namhub/schema/namhub.yaml` holds 27 templates, 7 abstract classes and
  mixins, and all slots.
- `enums.yaml` holds 49 enums with 700 values. 181 values have a `meaning`.
  `docs/pr18_enum_terms.md` gives the terms of the PR #18 and PR #22 enums.
- No class has a `class_uri`. No slot has a `slot_uri`. 15 slots have
  `exact_mappings` or `close_mappings` to an equivalent NAMHub slot (for
  example `measurement_technique` = `assay`).
- Keys use the form `<entity>_id`:
  - Individual and Biospecimen: `unique_keys` on `study_id` +
    `<entity>_id`.
  - Diagnosis: `study_id` + `individual_id` + `diagnosis`.
  - Treatment: `study_id` + `individual_id` + `therapeutic_agent`.
  - `nam_id` is the global key of NAMs. Datasets, NAMPortalDataset and
    Publications link to it.
  - Files have no ID slot. Curator annotates the Synapse entity.
    `parent_file_id` accepts a Synapse ID, a CURIE or a URL.
- ID titles use the form "{Term} ID" (for example "Study ID").

## Changes

### PR 1: module split, no output change

Use this layout:

```
src/namhub/schema/
  namhub.yaml          # id, name, version, prefixes; imports only
  core.yaml            # shared slots (study_id, description, assay, species, …) and mixins
  enums.yaml           # unchanged in this PR
  modules/
    program.yaml       # M1: Landscape, Studies, Grants, People, Publications
    dataset.yaml       # M2: Datasets, NAMPortalDataset
    nam.yaml           # M3: NAMs
    individual.yaml    # M5: Individual, Diagnosis, Treatment
    biospecimen.yaml   # M6: Biospecimen
    file.yaml          # M10: File, SupportingFile, Sequencing*, mixins, assay templates
    ext_ibd.yaml       # IBDDiagnosis (moved here unchanged)
```

Later plans add `modules/model.yaml` (M4), `modules/exposure.yaml` (M8) and
`modules/governance.yaml` (M11).

- Put a slot that more than one module uses in `core.yaml`.
- Put a slot that one module uses in that module.
- Make each module import `core` and `enums`.
- Make `namhub.yaml` import every module.
- Do not make a module import another module. This prevents cycles.
- Keep the enums in `enums.yaml` in this PR. Each module PR moves its own
  enums. This keeps this PR a pure move.
- Move `IBDDiagnosis` to `ext_ibd.yaml` without change.
- Update the repository-structure section of `README.md` to list the new
  files. This is the only documentation change.

**Reason:** A split with relative imports gives the same Curator JSON
(README section 3).

### PR 2: decision log and anchors, no output change

- Make `docs/model_decisions.md`. Add one entry for each decision in README
  section 4. Each entry gives what, why, sources and date.
- Add the key conventions and the FAIR field map (below) to the decision
  log.
- Each later module PR adds one entry for each reason in its plan.
- Add anchors to every existing class, slot and enum value.

Classes:

- Use `class_uri` where a standard class IRI exists. Otherwise use
  `exact_mappings` or `close_mappings`.
- Candidates:

| Class | Candidate anchor |
|---|---|
| Studies | ISA Study; C2M2 `project` |
| Datasets, NAMPortalDataset | schema.org `Dataset`; C2M2 `collection` |
| People | schema.org `Person` |
| Publications | schema.org `ScholarlyArticle` |
| Grants | schema.org `Grant` |
| Individual | ISA Source; C2M2 `subject` |
| Diagnosis | C2M2 `subject_disease`; GDC `diagnosis` |
| Treatment | GDC `treatment`; HTAN1 `Therapy` |
| Biospecimen | ISA Sample; OBI specimen; C2M2 `biosample` |
| File | ISA Data; C2M2 `file` |

Slots:

- Use `slot_uri` for a schema.org, Dublin Core, PROV-O or C2M2 field URI
  where one fits. Examples: `title` → `dcterms:title`, `description`,
  `filename`, `md5`, `doi`, `license`, `release_date` →
  `schema:datePublished`, and `parent_file_id` → `prov:wasDerivedFrom`.
- Otherwise use `see_also` and `source`. Name the document and the field
  (HTAN2, GDC, MC2, CELLxGENE, GEO). Examples: `sample_title` → GEO
  `Sample_title`; `sequencing_platform` → SRA `instrument_model`.

Enum values:

- `AssayEnum` (206 values), `DataCategoryEnum` (60) and `FileFormatEnum`
  (129) have no terms. Start from the NF metadata dictionary terms. Examine
  each term in OLS.
- Give terms to the other enum values that have none. Use the enum-term
  rule (README section 2).
- `SupportingFileTypeEnum`: `data_dictionary` gets `T4FS:0000073` (data
  dictionary). OLS has no term for `readme` or `sample_metadata`.
- `BiospecimenTypeEnum`: `in_vitro_differentiated_cells` and
  `engineered_tissue` have no OLS term. Give them `close_mappings` to NAMO
  classes. Give each value an `exact_mappings` to CELLxGENE `tissue_type`
  where one exists (tissue, primary cell culture, cell line, organoid).
- `NucleicAcidSourceEnum`: map `single_cell` and `single_nucleus` to the
  CELLxGENE `suspension_type` values `cell` and `nucleus`.
- `AssayEnum`: record the ISA measurement type of each value (for example
  transcription profiling) once on the value, as an `annotations` entry.
  The value itself names the technology. Keep the two apart (D27, D30).
- Record each value with no term as NAMHub-minted in the decision log.

Mappings (D31):

- Make `docs/mappings.sssom.tsv`. Add one row for each mapping that this PR
  adds, and for each term in `docs/pr18_enum_terms.md`. Columns:
  `subject_id`, `predicate_id`, `object_id`, `mapping_justification`
  (semapv), `confidence`, `author_id`, `mapping_date`,
  `object_source_version` (the pinned commit or release), `comment` (what
  differs between the two sides) and a review state.
- NAMO: use the full class IRI and the pinned commit (D7). Use
  `skos:exactMatch` only when a reviewer accepts that the two definitions
  agree. Otherwise use `skos:closeMatch`, `skos:broadMatch` or
  `skos:narrowMatch`, and say what differs in `comment`.
- Fields of other models with no IRI (open question 2a) get rows with the
  prefix of that model.
- Add a check: each mapping in the schema has a row, and each row names an
  element that exists.

Prefixes:

- Add the prefixes that the anchors need: IAO, HANCESTRO, PROV, dcterms,
  BAO and T4FS. OBI, PATO, UO and the others in `enums.yaml` exist.
- Keep EFO and EDAM on identifiers.org (README section 3).

Checks for this PR:

- The generated Curator JSON is byte-identical (README section 3).
- Run `gen-jsonld`. Check that the anchors appear.

Size: this PR is large. If review gets hard, split it into one PR for each
module file. Keep each PR byte-identical.

### PR 3: shared missing values (output changes)

Apply D29 to the enums on `main`:

- An enum of a required slot gets the missing values that apply to it, so
  that a submitter never invents a value.
- Replace each ad hoc missing value with the shared value: for example
  `SequencingPlatformEnum` and `TherapeuticResponseEnum` `not_reported`, and
  `LibraryPrepMethodEnum` "10x 3' version not reported" (keep it as a
  library value; add "not reported" for the general case). `SexEnum`
  "unknown" stays, with its term (M5).
- Do not add a missing value to a value that means "other".
- `gen-curator` ignores enum `inherits` and `include` (README section 3).
  Thus each enum lists the values itself. List every enum that has the set
  in the decision log. The check in README section 8, question 1 compares
  the copies with the set.

Later module PRs apply the same rule to the enums that they add.

### Key conventions (decision log, PR 2)

Every module plan uses these conventions.

- **Records:** use `<entity>_id`. It is unique within a study
  (`unique_keys` with `study_id`).
- **Link records with no ID of their own** (Diagnosis, Treatment): use a
  composite key. The key has `study_id`, the ID of the linked record and
  the linked value.
- **Catalog entries that studies share:** use a global `<entity>_id`. Today
  this is `nam_id`. Later plans add `device_id` (M4), `test_article_id`
  and `reference_compound_set_id` (M8), `access_requirement_id` (M11),
  `protocol_id` (M7), `context_of_use_id` and `acceptance_criterion_id`
  (M9), and `curation_run_id` and `profile_id` (M12). Open question 1
  confirms this scope.
- **Identifiers:** the key of a record is its identifier (FAIR rubric
  metrics 1 and 4). Synapse entities use the Synapse ID (Bioregistry prefix
  `synapse`). Records that have a DOI also keep `doi`. Do not add a
  separate `persistent_id` column (D27).
- **Links** reuse the slot name of the target key. Self-links use
  `parent_<entity>_id`.
- **One direction:** store a relation once, on the dependent row. Do not
  add the reverse link.
- **Files:** the key is the Synapse ID, made on upload (D25a). A link to a
  parent file accepts a Synapse ID, a CURIE or a URL, because a parent can
  be in a different repository.
- **File sources:** a file links to its most specific source:
  `biospecimen_id`; `individual_id` when no biospecimen exists (for example
  in vivo imaging); or `in_silico_model_id` for a model output. A file
  links to its dataset with `dataset_id`, to its study with `study_id`, and
  to the protocol that made it with `protocol_id` (M7).
  The file reaches its individual, NAM, licence and grant through these
  keys (D26, D27).
- **Source versus modeled (D30):** a descriptor slot has one role. Origin
  values (species, tissue, donor diagnosis) are on Individual and on source
  Biospecimen rows. Modeled values are on NAMs. A model Biospecimen row
  gives its modeled tissue, and its parent rows give the origin. Input
  values (cells and chemicals put into a model) are on Biospecimen and
  `TestArticle`. Observed values (cells and analytes that an assay
  measures) belong to the assay file templates. Each description says the
  role.
- **Titles:** use the form "{Term} ID".
- **Predicates:** give each link-only slot (for example `parent_file_id`,
  `parent_nam_id`) a `slot_uri` for its PROV-O or RO predicate. A key slot
  that other templates reuse as a link (`study_id`, `nam_id`,
  `biospecimen_id`) has one definition. It cannot carry a different
  predicate in each template (open question 2c).

### FAIR field map (decision log, PR 2)

Each field of the CFDE FAIR rubric is stored once, on the record that owns
it (D27). Other records reach it through keys (D26). No template gets a
mixin of FAIR fields.

| Metric | Stored on | Reached from other records through |
|---|---|---|
| 1, 4 Identifier | The key of each record (see Identifiers above); `doi` where one exists | — |
| 5 Program | Waits for D13 | — |
| 6 Project (grant) | Studies `grant_id` → Grants | `study_id` |
| 7 Institution | Studies `institution` (`InstitutionEnum`, ROR terms, M1) | `study_id` |
| 8 Landing page | The Synapse ID, which resolves to the Synapse page. External datasets: NAMPortalDataset `external_url` | `dataset_id` |
| 9 Access protocol | Each `RepositoryEnum` value, once (a `see_also` to the access documentation of the repository) | `repository` |
| 10 to 15 Ontology terms | `assay` (OBI with BAO mappings, D5), `tissue` (UBERON), `diagnosis` and `disease_focus` (MONDO), `file_format` (EDAM), `species` (NCBITaxon), `cellosaurus_id` | — |
| 16 Contact for creators | NAMPortalDataset `creator` (names); People `email` | `study_id` |
| 17 Resource licence | NAMPortalDataset `license`; NAMs `license` | Files: `dataset_id` |
| 18 Metadata licence | Studies `metadata_license` (D28, M1) | `study_id` |

## Checks

- The checks in README section 2.
- PR 1 and PR 2: the generated Curator JSON is byte-identical to the build
  from `main`.
- PR 3: the Curator diff shows only added or renamed missing values (major
  version: values change).

## Assumptions

1. Directory-form `linkml-lint` and `gen-jsonld` work on the split schema,
   as they did on a scratch copy.
2. A Synapse ID resolves to its Synapse page through the Bioregistry
   `synapse` prefix. Thus the Synapse ID of a record serves as its landing
   page (metric 8).
3. The contact for a dataset is a People row of its study. People rows hold
   `email` (M1 open question 3 asks whether it is public).

## Open questions

1. Must `device_id`, `test_article_id`, `reference_compound_set_id` and
   `protocol_id` be global (a shared catalog across studies, as the plans
   assume) or study-scoped like records? Recommendation: global, because
   each one can serve more than one study (D11).
2. Open points for the class and slot anchors (PR 2):
   - (a) Fields of other data models (C2M2, GDC, HTAN2, CELLxGENE, the NF
     dataset schema) have no IRI for each field. Declare NAMHub-defined
     prefixes that point to each specification at a fixed commit, use
     `see_also`, or leave them out? Recommendation: use the prefixes.
   - (b) Where no property exists, use an NCIT data-element class as
     `slot_uri`? HTAN2 does the same with caDSR. Recommendation: yes.
   - (c) Some slots are a key in one template and a link in others
     (`nam_id`, `dataset_id`, `grant_id`, `biospecimen_id`). Give them no
     `slot_uri` and a related mapping to `schema:identifier`, and record
     the meaning of each link in the decision log? Recommendation: yes.
