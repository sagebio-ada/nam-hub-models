# M10 file: shared File and sequencing templates

**Decisions (README section 4):** D4, D5, D6, D11, D19, D21, D22, D24,
D25a, D27, D33, D39

Other assay families (imaging, plate readouts, mass spectrometry, in silico
outputs and code, and others) get one plan for each family, after this
plan.

## Scope

1. Generalize the shared file classes, so that later assay families can use
   them.
2. Add the C2M2 and FAIR file fields.
3. Move the Level 1 fields off Level 2 and above.
4. Make each file name the protocol that made it. Move the workflow fields
   of Level 2 and above into `ComputationalProtocol` records (D24, D27).
5. Align the sequencing templates with HTAN2, GDC and SRA.

Anchors for the sequencing core: HTAN2 `Sequencing`, GDC `read_group` and
`aligned_reads`, and the SRA (INSDC) fields `library_strategy`,
`library_source`, `library_selection`, layout and `instrument_model`. HTAN2
uses a file key and a parent key (`HTAN_DATA_FILE_ID`, `HTAN_PARENT_ID`).
HTAN2 has no IRIs, so NAMHub adds `meaning` and mappings.

## Starting point

`main` has this class tree:

- `File` (abstract): `study_id`, `filename`, `file_format`, `assay`,
  `biospecimen_id` (required, multivalued), `md5`.
- `Sequencing` (abstract, is_a `File`): `sequencing_platform` and
  `library_layout` (both required), `sequencing_batch_id`,
  `technical_replicate_group`, `protocol_link`.
- `SequencingLevel1`: `nucleic_acid_source`, `library_preparation_method`,
  `read_indicator`.
- `SequencingLevel2`: `genomic_reference` (`GenomicReferenceEnum`, with
  `insdc.gcf` assembly terms), `workflow_name`, `workflow_version`,
  `workflow_link`, `parent_file_id`.
- `SequencingLevel3and4` (is_a `SequencingLevel2`):
  `workflow_parameters_description`, `matrix_type`.
- Mixins: `SingleCellMixin` (`cell_total`), `PeakCallingMixin`
  (`peak_calling_software`).
- Templates: single-cell RNA and ATAC (Levels 1, 2 and 3/4), multiome
  (Level 3/4), bulk RNA and ATAC (Levels 1, 2 and 3/4), `SupportingFile`.

`sequencing_platform` holds instrument models (for example Illumina NovaSeq
6000, `EFO:0008637`). `nucleic_acid_source` holds single cell, single
nucleus, bulk cells and bulk nuclei.

## Changes

### PR 1: `DerivedFileMixin` (no output change)

Move `parent_file_id` from `SequencingLevel2` into a `DerivedFileMixin`.
Apply the mixin to `SequencingLevel2` (`SequencingLevel3and4` inherits it).
Later assay families use the mixin for their derived files. PR 3 removes
the workflow slots, so this PR does not move them.

**Check:** The Curator JSON is byte-identical. Keep the slot order. Examine
the generated files.

### PR 2: File fields (output changes)

| Change | Source and anchor (candidate) |
|---|---|
| `File` gains `dataset_id`. It names the Synapse Dataset entity, that is the `NAMPortalDataset` record. The `Datasets` table is retired (D39). | C2M2 `file_in_collection` |
| `File` gains `size_in_bytes` | C2M2 `size_in_bytes` |
| `File` gains `sha256` (optional, as `md5` is) | C2M2 `sha256` |
| `File` gains `file_data_type` (optional). The name is not `data_type`, because `main` uses `data_type` for `DataCategoryEnum` (Datasets, NAMPortalDataset, Publications), and one slot name has one range. | EDAM `data:` (C2M2 `data_type`, exact mapping) |
| `File` gains `compression_format` | EDAM format (C2M2 `compression_format`) |
| `sequencing_platform` and `library_layout` move from `Sequencing` to `SequencingLevel1`. Reason: Level 2 and above can describe files that hold many samples (for example a multi-sample `.h5ad`), so they must not require Level 1 fields. | HTAN2 and GDC `read_group` hold them with the reads (check at the pinned HTAN2 commit) |
| `SequencingLevel1` gains `paired_file_id` (D19) | Same nuclei, other modality. The predicate needs an OLS check. |

A file reaches its individual, NAM, grant and licence through `study_id`,
`biospecimen_id` and `dataset_id` (M0 key conventions, file sources). Do
not add columns for these values to `File` (D27). `File.study_id` stays,
because `biospecimen_id` is unique only within a study. The in silico outputs
family plan adds `in_silico_model_id` to its own templates (M4).
Sequencing files do not use it.

### PR 3: protocols for every file level (output changes)

Each file names the protocol that made it (M7). A Level 1 file names the
wet-lab protocols (library preparation, sequencing). A Level 2, 3 or 4 file
names the computational protocol (a pipeline or a notebook) that made it
from its parent files. The parent link still gives the lineage back to the
library preparation.

| Change | Source and anchor (candidate) |
|---|---|
| `protocol_link` on `Sequencing` is replaced by `protocol_id` on `Sequencing` (all levels). The URL moves to `Protocol.protocol_link`. Optional and multivalued on Level 1 (for example library preparation and sequencing). Required on Level 2 and above, as `workflow_name` and `workflow_version` are now. | ISA Protocol; ISA Process `executesProtocol` |
| New `ComputationalProtocol` (is_a `Protocol`, in `modules/protocol.yaml`). `protocol_type` is data transformation (`OBI:0200000`). `protocol_version` is required. | ISA data transformation protocol; Workflow Run Crate |
| `ComputationalProtocol` gains `analysis_type`: the operation of the protocol | EDAM `operation:` (C2M2 `analysis_type`) |
| `ComputationalProtocol` gains `software` (multivalued): the name and version of each tool, for example MACS2 2.2.7 | schema.org `SoftwareApplication`; Workflow Run Crate `instrument` |
| Remove `peak_calling_software` and `PeakCallingMixin` (its only slot) from the ATAC and multiome Level 3/4 templates. The value moves to `software` on the `ComputationalProtocol` row. | — |
| Remove `workflow_name`, `workflow_version`, `workflow_link` (`SequencingLevel2`) and `workflow_parameters_description` (`SequencingLevel3and4`). Their values move to `protocol_name`, `protocol_version`, `protocol_link` and `parameters_description` on a `ComputationalProtocol` row. | — |

`genomic_reference` stays on the file. It gives the coordinates of the data,
and one protocol can run against different references.

Before this PR merges, make a `ComputationalProtocol` row for each workflow
name and version in the files that are already annotated, with their
parameters and peak-calling software. Then map each file to its row. Do
this as a separate, approved step.

**Reason:** All the files of one pipeline run repeat the same workflow name,
version, link, parameters and software. A protocol record stores them once (D27), and
ISA models data processing as a process that runs a protocol.

### PR 4: HTAN2 and SRA alignment (output changes)

- `SequencingPlatformEnum`: record the SRA platform (for example ILLUMINA)
  once on each value, as an `annotations` entry. Do not add a platform
  column. Reason: the platform depends only on the instrument model, so a
  column would repeat it on every row (D27). SRA and HTAN2 hold the
  platform and the instrument model as two fields; M0 PR 2 maps
  `sequencing_platform` to SRA `instrument_model`. Check that the
  annotations leave the Curator JSON unchanged.
- `ReadIndicatorEnum`: add R3 (10x ATAC barcode read).
- `SequencingLevel2`: add `genome_annotation_url` (HTAN2; for example the
  GENCODE release file). Do not add `genomic_reference_url`: each
  `GenomicReferenceEnum` value has its assembly accession as `meaning`. Add
  a new assembly as a new enum value (D6a).
- Single-cell Level 2 templates: add `barcode_whitelist_link`.
- `SequencingLevel1`: add `read_length` and `library_name`.
- Record the HTAN2 commit SHA for these mappings in the decision log (D22).

**Not changed:**

- No `suspension_type` slot. `nucleic_acid_source` holds cell or nucleus.
  M0 PR 2 maps its values to CELLxGENE `suspension_type`.

## FUSION mapping

Add these rows to `docs/mappings.sssom.tsv` (D31, D33). The target is the
FUSION (NDHCC) LinkML model, version 1.2.0-wave2r4.

| NAMHub record | FUSION class | Relation |
|---|---|---|
| `SupportingFile` and the sequencing file templates | `ndhcc:DataFile` | exact |
| `ComputationalProtocol` | `ndhcc:ProtocolVersion` | exact |

| NAMHub slot | FUSION slot |
|---|---|
| `md5` | `sha256` (not exact; only `sha256` maps exact) |
| `sha256` | `sha256` (exact) |
| `file_format` | `file_format` |
| `size_in_bytes` | `size_in_bytes` |
| `parent_file_id` and `protocol_id` together | `produced_by` (a `ndhcc:DataProcessing`) |
| `umi_tag` | `SequencingLibraryFacts` `umi_tag` |
| `cell_barcode_tag` | `SequencingLibraryFacts` `cell_barcode_tag` |
| `barcode_whitelist_link` | `SequencingLibraryFacts` `cell_barcode_whitelist` |
| `ComputationalProtocol.software` | `ndhcc:Software` |

## Checks

Do the standard checks (README section 2).

- PR 1: the Curator JSON is byte-identical.
- PR 2, PR 3 and PR 4: the Curator diff shows only the listed columns,
  templates and enum values. PR 2 and PR 3 remove columns from Level 2 and
  above (major version). PR 4 adds optional columns and enum values (minor
  version).
- The `assay` value of a file equals the `assay` of the Assay that the file
  reaches through `dataset_id`. The per-template enum narrowing of `assay`
  stays.

## Assumptions

1. All files in NAMHub are Synapse-hosted. External datasets (for example
   GEO) are described at the Dataset level only, with no file templates.
2. The move of `sequencing_platform` and `library_layout` to Level 1 matches
   HTAN2 at the pinned commit. Verify this in PR 2.
3. Submitters can make one `ComputationalProtocol` row for each pipeline or
   notebook version before they annotate the files that it made.

## Open questions

None.
