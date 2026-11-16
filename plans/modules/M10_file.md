# M10 file: shared File and PR #18 sequencing templates

**Decisions:** D4, D5 (assay: OBI primary, BAO exact mappings), D6, D11, D19 (`paired_file_id`), D21 (`SupportingFile` plus records for clinical tables), D22 (HTAN2 pinned commit), D25a (files keyed by Synapse IDs). The `protocol_link` slot waits for D24.

Other assay families (imaging, plate readouts, mass spectrometry, and others) get one plan for each family, after this plan.

## Scope

1. Generalize the shared file classes, so that later assay families can use them.
2. Add the C2M2 and FAIR file fields.
3. Move the Level 1 fields off Level 2 and above. Keep lineage (`parent_file_id`) optional (PR #18 review, PR18-5).
4. Align the sequencing templates with HTAN2, GDC and SRA, and make the other fixes in PR 3.

Anchors for the sequencing core: HTAN2 `Sequencing`, GDC `read_group` and `aligned_reads`, and the SRA (INSDC) fields `library_strategy`, `library_source`, `library_selection` and layout. The anchor for an instrument model is an EFO term (for example NovaSeq 6000, EFO:0008637). HTAN2 uses a file key and a parent key (`HTAN_DATA_FILE_ID`, `HTAN_PARENT_ID`). HTAN2 has no IRIs, so NAMHub adds `meaning` and mappings.

## Starting point

PR #18 has this class tree: `File` to `Sequencing`, to `SequencingLevel1` and `SequencingLevel2`, to `SequencingLevel3and4`. It has the mixins `SingleCellMixin` and `PeakCallingMixin`. It has these templates:

- Single-cell RNA and ATAC (Levels 1, 2 and 3/4).
- Multiome (Level 3/4).
- Bulk RNA and ATAC (Levels 1, 2 and 3/4).
- `SupportingFile`.

Merge the PR #18 review fixes first (M0, "Fixed in PR #18 and PR #22").

An earlier check found that `cell_total` was generated as `number`. This issue is closed. linkml-curator v0.4.0 writes integers as text with a digit pattern. The remaining problem is that the pattern accepts negative values. See [linkml-curator #13](https://github.com/Sage-Bionetworks/linkml-curator/issues/13) (README section 3).

## Changes

### PR 1: `DerivedFileMixin` (no output change)

Move `workflow_name`, `workflow_version`, `workflow_link`, `workflow_parameters_description` and `parent_file_id` into a `DerivedFileMixin`. They come from `SequencingLevel2` and `SequencingLevel3and4`. Apply the mixin to those two classes.

**Check:** The Curator JSON is byte-identical. Keep the slot order. Examine the generated files.

### PR 2: File fields and lineage (output changes)

| Change | Source / anchor (candidate) |
|---|---|
| `File` gains `dataset_id` | C2M2 `file_in_collection` |
| `size_in_bytes` | C2M2 `size_in_bytes` |
| `sha256` (optional; `md5` stays required) | C2M2 `sha256` |
| `data_type` | EDAM `data:` (C2M2 `data_type`) |
| `compression_format` | EDAM format (C2M2 `compression_format`) |
| `analysis_type` on `DerivedFileMixin` | EDAM `operation:` (C2M2 `analysis_type`) |
| Optional `individual_id`, `nam_id`, `in_silico_model_id` on `File` | C2M2 `file_describes_subject`; IAO is about |
| `PublishedRecord` on `File` (M0 PR 3) | FAIRshake |
| `parent_file_id` stays optional on `DerivedFileMixin`. It accepts a Synapse ID, a CURIE or a URL (done in PR #18, PR18-5) | `prov:wasDerivedFrom`; HTAN2 `HTAN_PARENT_ID` |
| `sequencing_platform` and `library_layout` move to `SequencingLevel1`. Reason: Level 2 and above can describe files that hold many samples (for example a multi-sample `.h5ad`), so they must not require Level 1 fields | HTAN2 and GDC `read_group` hold them with the reads (check at the pinned HTAN2 commit) |
| `paired_file_id` on `SequencingLevel1` (D19) | Same library, other modality; the predicate needs an OLS check |
| `SupportingFile`: `protocol` gets `OBI:0000272` in PR #18 (PR18-10). OLS has no term for `readme`, `sample_metadata` or `data_dictionary`. Record them as NAMHub-minted | IAO and EDAM `data:` (searched; none found) |

### PR 3: HTAN2 and SRA alignment, and other fixes (output changes)

- Split `sequencing_platform` into platform and `instrument_model`. The current values are instrument models, and they get EFO `meaning` terms in PR #18 (PR18-10). Move them to `instrument_model` with their terms. The new platform values (for example Illumina) need terms.
- `ReadIndicatorEnum`: add R3 (10x ATAC barcode read).
- `SingleCellMixin`: add `suspension_type` (CELLxGENE values: cell, nucleus).
- `LibraryPrepMethodEnum`: add "not reported". Reason: the enum has "other" and "10x 3' version not reported", but not a general "not reported". The EFO terms come in PR #18 (PR18-10).
- `SequencingLevel2`: add `genomic_reference_url` and `genome_annotation_url` (both required in HTAN2). Add `barcode_whitelist_link` for single-cell templates.
- `SequencingLevel1`: add `read_length` and `library_name`.
- `PeakCallingMixin`: make `peak_calling_software` required.
- Record the HTAN2 commit SHA for these mappings in the decision log (D22).

## Checks

Do the standard checks (README section 2).

- PR 1: the Curator JSON is byte-identical.
- PR 2 and PR 3: the Curator diff must show only the listed columns and enum values.

## Assumptions

1. All files in NAMHub are Synapse-hosted. External datasets (for example GEO) are described at the Dataset level only, with no file templates.
2. The move of `sequencing_platform` and `library_layout` to Level 1 matches HTAN2 at the pinned commit. Verify this in PR 2.

## Open questions

1. D24 is not decided. `protocol_link` stays on `Sequencing` as it is. Confirm that PR 2 and PR 3 must not change it.
