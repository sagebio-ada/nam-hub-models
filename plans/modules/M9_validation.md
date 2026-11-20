# M9 validation: context of use, validation, credibility and results

**Decisions (README section 4):** D4, D8, D9, D11, D16, D17, D24, D26, D27,
D29, D30, D32, D33, D37, D38, D40

## Scope

Record what a NAM is used for, how well it does that job, and how much
the results can be trusted:

1. `ContextOfUse`: the question and the role of a NAM in a decision (FDA
   NAM guidance section A; FDA CDRH 2023 and FDA AI draft, steps 1 and 2).
   It also holds the decision supported, the model influence and the
   decision consequence (D38).
2. `CredibilityAssessment`, `AICredibilityAssessment` and
   `CredibilityEvidence`: the validation evidence and the credibility of a
   NAM for one context of use (D40). The FDA NAM guidance (C.3, C.4 and D)
   covers in vitro and other non-computational NAMs. FDA CDRH 2023 covers
   mechanistic models. FDA AI draft covers data-driven models.
3. `AcceptanceCriterion` and `AssessmentResult`: thresholds and results as
   rows (D17). QC, reproducibility, concordance and performance results
   all use these two templates.

Sources (D9): FDA guidance first. OECD documents only where the FDA
guidance does not cover a point: the (Q)SAR validation principles and the
(Q)SAR Assessment Framework (applicability domain, (Q)SAR models), GIVIMP
(in vitro methods), GD 211 (method description), the test guidelines and
the GLP principles. Do not use the factor names of proprietary standards
that the FDA guidance draws on (README section 2, source rule).

## Starting point

- NAMs (M3) holds the method-level fields of the FDA NAM guidance
  (sections B and C): endpoints, detection and statistical methods, result
  classification criteria and working duration.
- `InSilicoModel` (M4) holds the model description, software, scope,
  `model_form` and the training and calibration datasets.
- `ReferenceCompoundSet` and `ReferenceCompound` (M8) hold benchmark
  compounds and their expected outcomes.
- The dataset record (M2) holds no comparator link (D40). Only
  `CredibilityEvidence` names comparator datasets.
- `Protocol` and `ComputationalProtocol` (M7, M10) hold methods and tools.
- `Assertion` (M12) holds the evidence for each value.
- `main` holds context of use only as free text in the Landscape form.

## Changes

Three PRs. Put the templates in a new `modules/validation.yaml`. Each PR adds
templates (minor version), except PR 3, which also adds optional columns
to `InSilicoModel`.

### PR 1: `ContextOfUse`, `AcceptanceCriterion`, `AssessmentResult`

#### `ContextOfUse` (new; global `context_of_use_id`)

One NAM can have several contexts of use. A context of use crosses
studies, so its ID is global (D11).

| Slot | Source and anchor (candidate) | Range |
|---|---|---|
| `context_of_use_id` | Key | string |
| `nam_id` (required) | The NAM | `nam_id` |
| `question_of_interest` (required) | The question that the NAM helps to answer. FDA CDRH 2023; FDA AI draft, step 1 | text |
| `cou_statement` (required) | The role and scope of the NAM in answering the question. FDA NAM guidance A; FDA AI draft, step 2 | text |
| `cou_category` | The examples in FDA NAM guidance A: patient monitoring, dose selection, mechanism of an adverse event, justification for not using an animal species, weight of evidence for risks not measured in humans; other | enum |
| `decision_supported` | The decision that the NAM output informs. FUSION `DecisionSupported.decision_text` | text |
| `model_influence`, `decision_consequence` | The weight of the NAM output in the decision, and the consequence of a wrong decision. FDA CDRH 2023; FDA AI draft, step 3. Each is low, medium or high (D16), with the D29 missing values (D37). They depend only on the context of use (D38). FUSION `DecisionSupported.model_influence`, `.decision_consequence` | enum |
| `biomarker_category` | The FDA-NIH BEST glossary categories: susceptibility/risk, diagnostic, monitoring, prognostic, predictive, pharmacodynamic/response, safety; with the D29 missing values. FUSION `biomarker_category` | enum |
| `use_tags` | The intended uses, as the FUSION (NDHCC) LinkML model, version 1.2.0-wave2r4, gives them in `UseTagEnum`: drug efficacy testing, disease modeling, toxicity prediction, drug safety assessment, drug discovery screening, mechanism elucidation, biomarker discovery, model development or characterisation, regulatory qualification, data infrastructure, training or dissemination. FUSION `use_tags` | enum, multivalued |
| `drug_development_objective` | FDA NAM guidance D: replace, fill a data gap, confirm or complement | enum, multivalued |
| `regulatory_purpose` | FDA NAM guidance A | text |
| `target_population` | The population or system that the decision is about | text |
| `applicability_domain` | Where the NAM's output is claimed to be valid (for example chemical space, concentration range, cell types, time window). OECD (Q)SAR principle 3 for (Q)SAR models | text |
| `oecd_test_guideline` | The OECD test guideline that the method follows, if any (D9) | text |
| `adverse_outcome_pathway` | AOP-Wiki ID | pattern `^AOP:\d+$`, multivalued |
| `previous_version_context_of_use_id` | `prov:wasRevisionOf`. A changed context of use is a new row. | `context_of_use_id` |

FUSION plans to add values to `UseTagEnum` in its next release. NAMHub
adds them when FUSION releases them.

#### `AcceptanceCriterion` (new; global `acceptance_criterion_id`)

A threshold set before the results are known. A criterion can belong to a
context of use, or it can be a general QC threshold for an assay and level.

| Slot | Source and anchor (candidate) | Range |
|---|---|---|
| `acceptance_criterion_id` | Key | string |
| `context_of_use_id` | The context of use that selects the criterion, if any | `context_of_use_id` |
| `metric` (required) | The shared `MetricEnum` (below) | enum |
| `comparator_operator` (required) | at least, at most, equal to, within range | enum |
| `threshold`, `threshold_upper` (`threshold` required) | `threshold_upper` only for "within range" | float |
| `unit` | UO, or dimensionless | enum |
| `applies_to_assay`, `applies_to_level` | Where a general QC threshold applies. Empty means all. | `AssayEnum`; processing level enum |
| `prespecified_date` | The date the criterion was set. FDA CDRH 2023 and FDA AI draft ask that criteria come before the evidence. | date |
| `criterion_source` | The guidance, SOP or protocol that gives the criterion: a protocol (`protocol_id`), a DOI or a URL | string |

#### `AssessmentResult` (new; study-scoped `assessment_result_id`)

One row for each result: one target, one metric, one data split (D17). No
result is a true/false column. Several results for one target can coexist.

| Slot | Source and anchor (candidate) | Range |
|---|---|---|
| `assessment_result_id` | Key, unique with `study_id` | string |
| `study_id` (required) | — | `study_id` |
| `target_template`, `target_id` (required) | What was assessed: any record (for example a Biospecimen, a file, a dataset, a `CredibilityAssessment` or a `CredibilityEvidence` row). Reuse the M12 slots. | enum and string |
| `assessment_dimension` (required) | The `AssessmentDimensionEnum` (below) | enum |
| `metric` (required) | `MetricEnum` | enum |
| `data_split` | training, tuning, test, external (FDA AI draft), with the D29 missing values | enum |
| `result_value` | The numeric result. The name is not `value`, because M12 `Assertion.value` is text. | float |
| `value_text` | A categorical result (for example "pass" for a STR profile match) | text |
| `unit` | UO, or dimensionless | enum |
| `ci_lower`, `ci_upper`, `ci_level` | FDA AI draft: performance estimates come with confidence intervals | float |
| `sample_size` | The number of items assessed | integer |
| `method_protocol_id` | The protocol or computational protocol that made the result (D24) | `protocol_id` |
| `acceptance_criterion_id` | The criterion that the result is compared with | `acceptance_criterion_id` |
| `outcome` | met, not met, inconclusive, with the D29 missing values. Required when `acceptance_criterion_id` is set. | enum |
| `evidence_dataset_id` | The data that the result was computed from. Accepts a Synapse ID, a CURIE or a URL (README section 2). | string, multivalued |
| `results_file_id` | The Synapse ID of the report file that holds the full results (for example a QC report with one value for each sample) | string, pattern `^syn\d+$` |
| `assessment_date` (required) | — | date |
| `assessor` | ORCID of the person, or the name of the organization | string |
| `status` (required) | draft, issued, superseded, withdrawn | enum |
| `supersedes_assessment_result_id` | The result that this row replaces | `assessment_result_id` |

Which results are rows: a result that a context of use or a credibility
claim depends on is a row. High-volume values (for
example the RNA integrity number of each biospecimen) stay in a QC report
file. Add the value `qc_report` to `SupportingFileTypeEnum` for these
files. A summary result row can name the file in `results_file_id`.

**Reason for `outcome`:** A categorical result cannot be compared with a
threshold by a check, so a person states the outcome. For a numeric result,
the check in README section 8 compares `result_value`, the criterion and `outcome`.

`AssessmentDimensionEnum`:

- QC: quality control.
- Technical characterization (FDA NAM guidance C): repeatability,
  intra-laboratory reproducibility, inter-laboratory reproducibility,
  batch-to-batch variation, lot-to-lot stability (C.4).
- Performance (FDA NAM guidance C.3 and D): predictive performance.
- Concordance with the modeled biology (NAMO `StructuredConcordanceResult`,
  mapped in the SSSOM file): molecular, pathway, phenotype, functional,
  cell-type coverage.
- Credibility (FDA CDRH 2023): code verification, calculation
  verification, validation against a comparator, uncertainty
  quantification.

`MetricEnum` starts with the FDA AI draft list and the FDA NAM guidance:
ROC AUC, sensitivity (recall), specificity, positive predictive value
(precision), negative predictive value, true positives, false positives,
true negatives, false negatives, positive likelihood ratio, negative
likelihood ratio, F1 score, false positive rate, false negative rate.
Add: accuracy, balanced accuracy, coefficient of variation, Pearson and
Spearman correlation, R², RMSE, MAE, Z′ factor. Add QC metrics for each
assay as needed (D6a; for example RNA integrity number, mapping rate, cell
viability). Give each value a STATO, OBI or BAO `meaning` after the OLS
check.

### PR 2: `CredibilityAssessment` and `CredibilityEvidence` (all NAMs)

`ValidationAssessment` is not a separate template (D40). `CredibilityAssessment`
holds the validation fields and the credibility fields of every NAM. FUSION
has one modality-neutral `CredibilityAssessment` in the same way.

#### `CredibilityAssessment` (new; study-scoped `credibility_assessment_id`)

One row for each NAM, context of use and framework. A hybrid model has one
row under each framework. The NAM is reached through `context_of_use_id`
and `ContextOfUse.nam_id` (D27).

| Slot | Source and anchor (candidate) | Range |
|---|---|---|
| `credibility_assessment_id` | Key, unique with `study_id` | string |
| `study_id`, `context_of_use_id` (required) | — | keys |
| `in_silico_model_id` | The in silico model. Required when `credibility_framework` is an in silico framework (see Checks). | `in_silico_model_id` |
| `credibility_framework` (required) | FDA NAM guidance (in vitro and other non-computational NAMs); FDA CDRH 2023 (mechanistic); FDA AI draft 2025 (data-driven); OECD (Q)SAR principles and QAF as secondary sources for (Q)SAR models (D9). The value is "FDA NAM guidance" for the first. | enum |
| `validation_status` | FDA NAM guidance: formally validated; fit for purpose, not formally validated; qualified (FDA DDT or ISTAND); with the D29 missing values | enum |
| `other_evidence_used` | The in vitro, in vivo, clinical or process evidence used with the model. FDA CDRH 2023 and FDA AI draft | text |
| `model_risk`, `model_risk_rationale` | FDA CDRH 2023; FDA AI draft, step 3. `model_risk` is low, medium or high (D16), with the D29 missing values (D37). `model_risk` is required only for an in silico framework (see Checks). `model_risk_rationale` is optional. The rationale gives the reason for the rating. The FDA AI draft says that decision consequence considers the question of interest and both the severity and the probability of an adverse outcome. FUSION `ModelRisk.risk_level`, `.rationale` | enum and text |
| `credibility_plan_file_id`, `credibility_report_file_id` | Synapse IDs of the plan and the report (`SupportingFile`) | string |
| `report_availability` | Submitted, or held and available to FDA on request (FDA AI draft, step 6) | enum |
| `plan_deviations` | FDA AI draft, step 6 | text |
| `adequacy_outcome` | Adequate, or one of the FDA AI draft's options when it is not: reduce model influence with more evidence; increase rigor or add development data; establish risk controls; change the modeling approach; reject or revise the context of use (step 7). The FDA CDRH 2023 options fall in this set. | enum |
| `adequacy_rationale` | FDA CDRH 2023; FDA AI draft | text |
| `limitations`, `benefits`, `contribution_to_risk_assessment` | FDA NAM guidance D. `limitations` replaces `model_limitations`. FUSION `Limitation` | text |

The values of the assessment (performance, reproducibility, concordance,
lot-to-lot stability) are `AssessmentResult` rows whose target is this row
(D17, D27).

**Reason for storing `model_risk` beside the context of use:** Both FDA
guidances show the risk matrix as an example, not as a fixed rule. Thus
model risk is a judgment, not a value that `model_influence` and
`decision_consequence` (on `ContextOfUse`) fix.

#### `CredibilityEvidence` (new; study-scoped `credibility_evidence_id`)

One row for each evidence item of any NAM (FDA CDRH 2023 for a mechanistic
model; FDA NAM guidance for other NAMs).

| Slot | Source and anchor (candidate) | Range |
|---|---|---|
| `credibility_evidence_id` | Key, unique with `study_id` | string |
| `credibility_assessment_id` (required) | — | key |
| `evidence_category` (required) | The eight categories of FDA CDRH 2023 Table 2: code verification; model calibration; bench test validation (here: in vitro or NAM comparator validation); in vivo validation; population-based validation; emergent model behavior; model plausibility; calculation verification and uncertainty quantification with context-of-use simulations | enum |
| `credibility_factor` | Free text. The factor names come from a proprietary standard and are not listed (source rule). | text |
| `relevance_to_cou` | FDA CDRH 2023 asks for it for every evidence item | text |
| `credibility_goal`, `achieved_level`, `rationale_if_below_risk` | Gradations that the submitter sets | text |
| `comparator_method` | What the NAM was compared with (for example an animal study, clinical data, a reference method) | text |
| `comparator_dataset_id` | The comparator data. Accepts a Synapse Dataset ID, a CURIE or a URL. This is the only place for it (D40). | string, multivalued |
| `reference_compound_set_id` | The benchmark set (M8) | `reference_compound_set_id` |
| `comparator_data_timing` | Prospective, retrospective or literature (FDA CDRH 2023 Table 3) | enum |
| `analyst_blinded` | yes, no, with the D29 missing values | enum |
| `method_protocol_id` | The protocol that produced the evidence | `protocol_id` |

The values of an evidence item are `AssessmentResult` rows whose target is
this row.

### PR 3: `AICredibilityAssessment` (data-driven models) and `InSilicoModel` additions

#### `AICredibilityAssessment` (new; is_a `CredibilityAssessment`)

The FDA AI draft (step 4) adds these fields for a data-driven or hybrid
model. A row of this template is the `CredibilityAssessment` of that model
under the FDA AI draft.

| Group | Slots | Source |
|---|---|---|
| Test data | `test_dataset_id` (multivalued; Synapse ID, CURIE or URL), `dataset_split_description`, `test_data_independence_method`, `data_overlap_justification`, `test_data_applicability_to_cou` (covers data drift) | FDA AI draft 4.a.ii, 4.b |
| Data fitness | `data_collection_processing_description`, `label_annotation_method`, `data_relevance_rationale`, `data_reliability_rationale`, `data_representativeness`, `known_biases`, `federated_learning` (yes, no, D29) | FDA AI draft 4.a.ii |
| Evaluation | `reference_method`, `evaluation_method_rationale`, `uncertainty_estimation_method`, `human_ai_team_evaluated` (yes, no, D29) | FDA AI draft 4.b |
| Explainability and communication | `explainability_approach`, `explainability_summary`, `plain_language_summary` (optional; D9) | FDA–EMA principles 7 and 10 |
| Standards and controls | `gxp_context` (GLP, GCP, GMP, GVP, not applicable), `risk_controls_description` | FDA–EMA principles 2 and 3 |
| Life cycle | `self_evolving` and `data_drift_monitored` (each yes, no, D29), `monitoring_metrics`, `monitoring_frequency`, `retest_triggers`, `quality_management_reference` | FDA AI draft IV.B; FDA–EMA principle 9 |

The performance of the model, its agreement with the reference method and
its reproducibility are `AssessmentResult` rows with `data_split` set
(D17). Code QA is `InSilicoModel.software_qa_description` (M4). A new model
version is a new `InSilicoModel` row. The FDA AI draft fields stay here (FDA
is the primary source, D9). FUSION `ModelCard` maps close to them.

#### `InSilicoModel` additions (optional)

- `tuning_dataset_id` (multivalued; Synapse ID, CURIE or URL): FDA AI
  draft 4.a.ii.
- `pretraining_dataset_id` (multivalued) and `pretrained_model_source`
  (URL or DOI): FDA AI draft 4.a.iii.

These are development data of the model, so they go on the model with
`training_dataset_id` and `calibration_dataset_id` (M4). Test data depends
on the context of use, so it goes on `AICredibilityAssessment`.

## FUSION mapping

Add these rows to `docs/mappings.sssom.tsv` (D31, D33). The target is the
FUSION (NDHCC) LinkML model, version 1.2.0-wave2r4. The v2 context-of-use
module is version 1.3.0-wave3f1.1.

| NAMHub record | FUSION class | Relation |
|---|---|---|
| `ContextOfUse` | `ndhcc:ContextOfUse` | exact |
| `AcceptanceCriterion` | `ndhcc:AcceptanceCriterion` (`ndhcc:QCThreshold` when scoped to an assay and level) | exact |
| `AssessmentResult` | `ndhcc:AssessmentResult` (`ndhcc:QualityAssessment` for QC rows) | exact |
| `CredibilityAssessment` | `ndhcc:CredibilityAssessment` | exact |
| `AICredibilityAssessment` | `ndhcc:InSilicoCredibility` | close |
| `CredibilityEvidence` | `ndhcc:CredibilityEvidence` | exact |

| NAMHub slot | FUSION slot |
|---|---|
| `ContextOfUse.question_of_interest` | `QuestionOfInterest.question_text` |
| `ContextOfUse.cou_statement` | `narrative_verbatim` |
| `ContextOfUse.target_population` | `TargetPopulation.population_text` |
| `ContextOfUse.applicability_domain` | `ApplicabilityDomain.domain_text` |
| `ContextOfUse.regulatory_purpose` | `regulatory_frame` (close) |
| `ContextOfUse.decision_supported` | `DecisionSupported.decision_text` |
| `ContextOfUse.model_influence`, `.decision_consequence` | `DecisionSupported.model_influence`, `.decision_consequence` |
| `ContextOfUse.biomarker_category` | `biomarker_category` |
| `ContextOfUse.use_tags` | `use_tags` |
| `CredibilityAssessment.model_risk`, `.model_risk_rationale` | `ModelRisk.risk_level`, `.rationale` |
| `CredibilityAssessment.limitations` | `Limitation` |

The FUSION value `not_assessed` maps to the D29 missing values of
`model_influence`, `decision_consequence` and `model_risk` in SSSOM (D37).
The NAMHub enums keep the D29 values.

## Checks

- The checks in README section 2.
- Each PR's Curator diff shows only its new templates. PR 1 also shows the
  `qc_report` value of `SupportingFileTypeEnum`. PR 3 also shows the three
  optional `InSilicoModel` columns.
- README section 8, question 1 adds:
  - An `AssessmentResult` has `result_value` or `value_text`. When it has
    a `result_value` and a criterion, its `outcome` agrees with the
    criterion.
  - A credibility comparator dataset is not a training,
    tuning or calibration dataset of the same model (FDA CDRH 2023:
    calibration is not validation; FDA AI draft: test data independence).
  - When `credibility_framework` is FDA CDRH 2023, FDA AI draft or OECD
    ((Q)SAR), `in_silico_model_id` and `model_risk` have values, and the
    linked `ContextOfUse` has `model_influence` and `decision_consequence`.
    These are the in silico frameworks.
  - An `AICredibilityAssessment` is only for a data-driven or hybrid model.
    A hybrid model has one assessment under each FDA framework.

## Assumptions

1. The required fields above are the D8 minimum for M9. All other fields
   are optional. The checks above make some fields required for an in silico
   framework.
2. The `cou_category` examples, the evidence categories and the adequacy
   options are copied from the FDA texts as these plans quote them. Check
   each value against the guidance text in the PR.
3. FDA AI draft is a draft. If the final guidance changes a list, the
   enum changes in a new version.

## Open questions

None.
