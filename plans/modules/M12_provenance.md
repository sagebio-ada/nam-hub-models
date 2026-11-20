# M12 provenance: evidence for metadata values

**Decisions (README section 4):** D4, D11, D26, D27, D29, D31, D32, D33, D37, D41

## Scope

Metadata that Curator and Curie extract from source documents goes into the
NAMHub templates, and from there to the FUSION knowledge base. The
knowledge base needs to know where each value came from, how it was read
and who checked it (D32). This module adds three templates:

1. `Assertion`: the evidence for one value in one record: the source, the
   location in the source, the value as the source states it, the method
   and the review state.
2. `CurationRun`: one extraction or curation run: the agent or tool, its
   version, the date and the curation profiles it used.
3. `CurationProfile`: one set of extraction rules (common, program, NAM,
   assay, processing level or source format), with its version and the
   rules that combine it with other profiles.

The record templates keep the current value of each field. The provenance
templates hold the evidence once, beside them (D27). No record template
gets provenance columns.

## Starting point

- `main` has no provenance for any value. `SupportingFile` holds source
  documents that are in Synapse. Publications holds PubMed IDs and DOIs.
- M7 `ComputationalProtocol` holds the tool and version of a computation.
- D29 gives the missing values of a field. It does not say why an
  extraction found no value.

## Changes

One PR. Put the templates in a new `modules/provenance.yaml`. The Curator
output changes (minor version: three new templates).

### `Assertion` (new; study-scoped `assertion_id`)

One row for each value that a run read, computed or reviewed.

| Slot | Source and anchor (candidate) | Range |
|---|---|---|
| `assertion_id` | Key, unique with `study_id` | string |
| `curation_run_id` (required) | The run that made the assertion | `curation_run_id` |
| `target_template` (required) | The template of the record | enum of NAMHub template names |
| `target_id` (required) | The key of the record: the Synapse ID of a file, or the `<entity>_id` of a record in the study | string |
| `target_field` | The slot name. Empty when the assertion is about the whole record. For a link record (Diagnosis, Treatment), the field that is part of the key, with `value`, names the row. | string |
| `value` | The value as the template holds it (normalized) | string |
| `original_value` | The value as the source states it, before normalization | string |
| `source_id` (required unless computed) | The source: a Synapse ID with version (`syn123.4`), a DOI or PubMed CURIE, or a URL | string, pattern |
| `location_type`, `location` | Where in the source: page, section, table, figure, cell, line, time, region or data field, and its label (for example "page 4, table 2, row 3"). W3C Web Annotation selector (`oa:hasSelector`). | enum and text |
| `source_quote` | The exact text that states the value. W3C Web Annotation `oa:TextQuoteSelector`. | text |
| `value_origin` (required) | Stated in the source, inferred from the source, or computed from data | enum |
| `computed_by_protocol_id` | For a computed value: the `ComputationalProtocol` (tool and version) that computed it (M7, M10) | `protocol_id` |
| `assertion_method` (required) | ECO assertion method: manual (`ECO:0000218`) or automatic (`ECO:0000203`) | enum |
| `planning_state` | planned, observed, cannot_tell (for example a planned sample count against the observed one) | enum |
| `resolution_state` (required) | resolved, provisional, gap, not_attempted | enum |
| `review_state` (required) | unreviewed, machine_parsed, curator_accepted, curator_amended, curator_rejected | enum |
| `confidence` | high, medium, low, provisional, as the tool or curator gives it. Not a calibrated probability. | enum |
| `reviewer` | ORCID of the curator who reviewed the assertion | ORCID pattern |

The values of `resolution_state`, `review_state`, `planning_state` and
`confidence` are the values of the FUSION (NDHCC) LinkML model, version
1.2.0-wave2r4, used verbatim (D37). The FUSION missing-value tokens
(`not_stated`, `not_assessed`, `not_applicable`) map to the D29 set in SSSOM.
The NAMHub enums keep the D29 values.

Rules:

- When an extraction finds no value, the record field holds the D29 missing
  value, and the assertion holds `resolution_state` `gap` or `not_attempted`.
  Thus the reason for the gap stays visible.
- A value with two or more candidate concepts stays `gap` until a curator
  selects one candidate.
- Two sources that state different values give two assertions for the same
  target field with different values. Both stay. A check reports the
  conflict, and the curator sets `review_state` on each assertion. No value
  wins without review.
- A computed value (for example a read count from FASTQ files) has
  `value_origin` computed and names its protocol. It is not presented as a
  value read from a document.
- An inferred value has `value_origin` inferred and keeps its
  `source_quote`.

### `CurationRun` (new; global `curation_run_id`)

| Slot | Source and anchor (candidate) | Range |
|---|---|---|
| `curation_run_id` | Key | string |
| `run_method` (required) | Manual, automatic or mixed | enum |
| `curation_agent` (required) | The curator (ORCID) or the tool (name). The name is not `agent`, because M8 `TestArticle.agent` is an enum. | string |
| `agent_version` | The tool version | string |
| `run_date` (required) | — | date |
| `schema_version` (required) | The NAMHub model version that the run filled | string |
| `profile_id` (required) | The curation profiles that the run used. With `schema_version`, they are the resolved curation specification of the run. | `profile_id`, multivalued |
| `study_id` | The study that the run covered, when it covered one study | `study_id` |

PROV-O anchor: `prov:Activity`, with `prov:wasAssociatedWith` the `curation_agent`.

### `CurationProfile` (new; global `profile_id`)

| Slot | Source and anchor (candidate) | Range |
|---|---|---|
| `profile_id` | Key | string |
| `profile_name` (required) | — | text |
| `profile_kind` (required) | Common, program, NAM, assay, processing level, or source format | enum |
| `profile_version` (required) | — | text |
| `previous_version_profile_id` | `prov:wasRevisionOf`. A new version is a new row. | `profile_id` |
| `applies_to_assay`, `applies_to_nam_kind`, `applies_to_level`, `applies_to_source_type` | Where the profile applies. Empty means all. | enums (reuse `AssayEnum`, the FUSION `NAMKindEnum` (D41), the processing levels, the source document types) |
| `instructions_link` (required) | The extraction protocol: which sources to read, how to tell entities apart, what may be inferred, how to record gaps | uri |
| `extends_profile_id` | The profiles that this profile builds on | `profile_id`, multivalued |
| `precedence` | When two profiles set the same rule, the higher value wins | integer |
| `conflict_policy` (required) | What to do when two sources disagree: refuse and report, or keep both and flag | enum |
| `missing_policy` (required) | An absent value means unknown, or the record is refused | enum |

Composition: a run names every profile that it used. A profile that
`extends` another profile includes its rules. When two rules disagree, the
higher `precedence` wins. When two profiles have the same precedence, the
run reports the conflict and does not choose.

### Mappings to the FUSION knowledge base

Add rows to `docs/mappings.sssom.tsv` (D31, D33) from these templates to the
FUSION (NDHCC) LinkML model, version 1.2.0-wave2r4. Add the NDHCC prefix.

| NAMHub record | FUSION class | Relation |
|---|---|---|
| `Assertion` | `ndhcc:ControlledValue` with `ndhcc:SourceLocator` (and `ndhcc:EvidenceRecord`) | close |
| `CurationRun` | `ndhcc:AssertionActivity` | close |
| `CurationProfile` | none | — |

D37 rule: use the FUSION enum values verbatim for `resolution_state`,
`review_state`, `planning_state` and `confidence`. Model a conflict as two
`Assertion` rows and a check finding, not as a value.

**Reason:** The FUSION knowledge base keeps the evidence for each value.
Curator and Curie produce that evidence when they extract the values. If
the templates do not hold it, it is lost before the submission (D26: no
pipeline makes it later).

## Checks

- The checks in README section 2.
- The Curator diff shows only the three new templates.
- README section 8, question 1 adds: each `Assertion` names an existing
  record and field; its `value` equals the value in that record; a computed
  value names a protocol.

## Assumptions

1. Curie writes its output as rows of the NAMHub templates plus
   `Assertion` rows, in the same submission.
2. The FUSION knowledge base reads the NAMHub templates through the SSSOM
   mappings. NAMHub does not write to the knowledge base.
3. Source documents in Synapse keep their versions, so `syn123.4` stays
   valid.

## Open questions

1. Must every value have an `Assertion`, or only automatic extractions?
   Recommendation: required for automatic extraction; optional for manual
   entry, where one record-level assertion (empty `target_field`) is
   enough.
2. Location as one `location_type` and `location` pair, or as separate
   columns (page, section, table, cell)? Recommendation: the pair. It
   covers all source types in two columns.
3. When the FUSION knowledge base makes its own IRI for a record, must
   NAMHub store it? If yes, store it once, on the NAMHub record (a
   `fusion_iri` column), not in the knowledge base and here both.
