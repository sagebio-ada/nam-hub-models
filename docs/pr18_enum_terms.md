# Enum terms for PR #18 and PR #22

**Date:** 2026-11-16

This file supports the review comments on PR #18 and PR #22:

- **PR18-10:** ontology terms for the enums that PR #18 and PR #22 add
  (section 3).
- **PR18-6:** the new `DataUseModifierEnum` (section 4).
- **PR18-7:** the new `LicenseEnum` (section 5).

Class and slot anchors are not in this file. They come in a later PR.

## How the terms were found

- Each term was examined in OLS on 2026-11-16. All terms are current, and
  their labels agree with OLS.
- Genome assemblies use NCBI RefSeq accessions. The funder uses a ROR ID.
- License values come from the NF-OSI PortalDataset schema
  (`org.synapse.nf-portaldataset`); their terms are SPDX license IDs.
- DUO terms are the ones in the NF-OSI PortalDataset schema that are current
  in OLS. `DUO:0000044` (NPOA) is in the DUO source file but not in OLS, so
  it is not included.
- No proprietary standard is used.

## 1. Where a term goes

A `meaning` must have the same meaning as the value. Thus:

- An exact term goes in `meaning`.
- A wider term goes in `broad_mappings`.
- A narrower term goes in `narrow_mappings`.
- A value with no term gets no `meaning`. Values such as `not_reported`,
  `other` and `unknown` need no term.

The column "Goes in" in section 3 shows where each term goes. On a copy of
the schema, `meaning` and `broad_mappings` pass both linters, and the
generated Curator templates do not change.

## 2. Prefixes to add to `enums.yaml`

| Prefix | Namespace | Used by |
|---|---|---|
| `CLO` | http://purl.obolibrary.org/obo/CLO_ | `BiospecimenTypeEnum` |
| `DUO` | http://purl.obolibrary.org/obo/DUO_ | `DataUseModifierEnum` |
| `PATO` | http://purl.obolibrary.org/obo/PATO_ | `SexEnum`, `EndoscopicStatusEnum` |
| `UO` | http://purl.obolibrary.org/obo/UO_ | `TimeUnitEnum`, `AgeUnitEnum` |
| `ror` | https://ror.org/ | `FunderEnum` (Bioregistry prefix) |
| `insdc.gcf` | https://www.ncbi.nlm.nih.gov/datasets/genome/ | `GenomicReferenceEnum` (Bioregistry prefix for RefSeq assemblies) |
| `spdx` | https://spdx.org/licenses/ | `LicenseEnum` (Bioregistry prefix for license IDs) |

`enums.yaml` already declares `CL`, `EDAM`, `EFO`, `MONDO`, `NCBITaxon`,
`NCIT`, `OBI` and `UBERON`.

## 3. Enum terms

"Goes in" says where the term goes (section 1). Values with "—" get no term.

| Enum | Value | Term | OLS label | Match | Goes in | Note |
|---|---|---|---|---|---|---|
| `SexEnum` | `male` | PATO:0000384 | male | exact | meaning | NCIT:C20197 Male is an alternative |
| `SexEnum` | `female` | PATO:0000383 | female | exact | meaning | NCIT:C16576 Female is an alternative |
| `SexEnum` | `unknown` | — |  | no term needed | — | placeholder |
| `BiospecimenTypeEnum` | `tissue` | NCIT:C12801 | Tissue | exact | meaning | UBERON:0000479 tissue also exists |
| `BiospecimenTypeEnum` | `primary_cells` | EFO:0002660 | primary cell | exact | meaning | A cell taken directly from a living organism, not immortalized |
| `BiospecimenTypeEnum` | `cell_line` | CLO:0000031 | cell line | exact | meaning | NCIT:C16403 Cell Line also exact; CLO is the dedicated ontology |
| `BiospecimenTypeEnum` | `in_vitro_differentiated_cells` | — |  | none | — | searched unrestricted and NCIT/EFO/CL/OBI; only specific cell lines or iPSC-derived items. CL:0000010 cultured cell is broader but loses the differentiation meaning; not proposed |
| `BiospecimenTypeEnum` | `organoid` | NCIT:C172259 | Organoid | exact | meaning | Not in EFO/OBI. mesh:D009940 Organoids exists in OLS as alternative |
| `BiospecimenTypeEnum` | `engineered_tissue` | — |  | none | — | No OLS class. mesh:D000094182 Microphysiological Systems exists (covers only the MPS half); NCIT:C18075 Tissue Engineering is a process not a material |
| `BiospecimenTypeEnum` | `other` | — |  | no term needed | — | placeholder |
| `SequencingPlatformEnum` | `illumina_novaseq_x_plus` | EFO:0022841 | Illumina NovaSeq X Plus | exact | meaning | OBI equivalent: OBI:0003664 |
| `SequencingPlatformEnum` | `illumina_novaseq_x` | EFO:0022840 | Illumina NovaSeq X | exact | meaning | OBI equivalent: OBI:0003663 |
| `SequencingPlatformEnum` | `illumina_novaseq_6000` | EFO:0008637 | Illumina NovaSeq 6000 | exact | meaning | OBI equivalent: OBI:0002630 |
| `SequencingPlatformEnum` | `illumina_nextseq_2000` | EFO:0010963 | Illumina NextSeq 2000 | exact | meaning |  |
| `SequencingPlatformEnum` | `illumina_nextseq_500` | EFO:0009173 | Illumina NextSeq 500 | exact | meaning | OBI equivalent: OBI:0002021 |
| `SequencingPlatformEnum` | `illumina_hiseq_4000` | EFO:0008563 | Illumina HiSeq 4000 | exact | meaning | OBI equivalent: OBI:0002049 |
| `SequencingPlatformEnum` | `not_reported` | — |  | no term needed | — | placeholder |
| `LibraryPrepMethodEnum` | `ten_x_multiome` | EFO:0030059 | 10x multiome | exact | meaning | EFO:0920135 10x Next-GEM Multiome is a narrower alternative |
| `LibraryPrepMethodEnum` | `ten_x_3prime_v3_1` | EFO:0022980 | 10x 3' v3.1 | exact | meaning |  |
| `LibraryPrepMethodEnum` | `ten_x_3prime_v3` | EFO:0009922 | 10x 3' v3 | exact | meaning |  |
| `LibraryPrepMethodEnum` | `ten_x_3prime_v2` | EFO:0009899 | 10x 3' v2 | exact | meaning |  |
| `LibraryPrepMethodEnum` | `ten_x_5prime` | EFO:0030004 | 10x 5' transcription profiling | exact | meaning | Version-agnostic; EFO also has 10x 5' v1/v2/v3 (EFO:0011025, EFO:0009900, EFO:0022605) |
| `LibraryPrepMethodEnum` | `ten_x_atac_v2` | EFO:0030007 | 10x scATAC-seq | close-broader | broad_mappings | No version-specific EFO term found |
| `LibraryPrepMethodEnum` | `ten_x_atac_v1_1` | EFO:0030007 | 10x scATAC-seq | close-broader | broad_mappings | No version-specific EFO term found |
| `LibraryPrepMethodEnum` | `ten_x_gem_x_epi_multiome` | EFO:0030059 | 10x multiome | close-broader | broad_mappings | No GEM-X-specific term; EFO:0920135 is Next-GEM, not GEM-X |
| `LibraryPrepMethodEnum` | `omni_atac` | EFO:0010014 | Omni-ATAC | exact | meaning |  |
| `LibraryPrepMethodEnum` | `smart_seq2` | EFO:0008931 | Smart-seq2 | exact | meaning |  |
| `LibraryPrepMethodEnum` | `smart_seq4` | EFO:0008930 | Smart-seq | close-broader | broad_mappings | No Smart-seq4 term in OLS (EFO has Smart-seq, Smart-seq2, Smart-seq3) |
| `LibraryPrepMethodEnum` | `drop_seq` | EFO:0008722 | Drop-seq | exact | meaning |  |
| `LibraryPrepMethodEnum` | `ten_x_3prime_version_not_reported` | EFO:0030003 | 10x 3' transcription profiling | exact | meaning | Version-agnostic parent of the versioned 3' terms |
| `LibraryPrepMethodEnum` | `illumina_truseq` | EFO:0022396 | TruSeq | exact | meaning |  |
| `LibraryPrepMethodEnum` | `nebnext_ultra_ii_rna` | — |  | none | — | No NEBNext term in OLS; OBI:0000711 library preparation is generic and not proposed |
| `LibraryPrepMethodEnum` | `kapa` | — |  | none | — | No KAPA library prep kit term in OLS |
| `LibraryPrepMethodEnum` | `atac_seq_buenrostro` | EFO:0007045 | ATAC-seq | close-broader | broad_mappings | Assay term; the Buenrostro protocol is the original ATAC-seq method. NCIT:C156056 ATAC-Seq alternative |
| `LibraryPrepMethodEnum` | `other` | — |  | no term needed | — | placeholder |
| `LibraryLayoutEnum` | `paired_end` | NCIT:C150423 | Paired-End Sequencing | exact | meaning | OBI paired-end terms are assay-specific (paired-end tag), not suitable |
| `LibraryLayoutEnum` | `single_end` | — |  | none | — | No generic single-end sequencing term in OLS (OBI:0002485 is a specific transcript-analysis assay) |
| `NucleicAcidSourceEnum` | `single_nucleus` | NCIT:C178227 | Single Nucleus Specimen | exact | meaning |  |
| `NucleicAcidSourceEnum` | `single_cell` | NCIT:C178226 | Single Cell Specimen | exact | meaning |  |
| `NucleicAcidSourceEnum` | `bulk_nuclei` | — |  | none | — | No bulk nuclei specimen term; NCIT:C204465 Nuclei Suspension for Single-Nuclei Assay is single-nucleus specific |
| `NucleicAcidSourceEnum` | `bulk_cells` | — |  | none | — | No bulk cells specimen term; NCIT:C69010 Bulk is a generic modifier |
| `ReadIndicatorEnum` | `r1` | — |  | none | — | Read-file labels (Illumina FASTQ naming); no ontology term |
| `ReadIndicatorEnum` | `r2` | — |  | none | — | Read-file labels (Illumina FASTQ naming); no ontology term |
| `ReadIndicatorEnum` | `i1` | — |  | none | — | Read-file labels (Illumina FASTQ naming); no ontology term |
| `ReadIndicatorEnum` | `i2` | — |  | none | — | Read-file labels (Illumina FASTQ naming); no ontology term |
| `GenomicReferenceEnum` | `grch38` | insdc.gcf:GCF_000001405.26 | GRCh38 (NCBI Assembly, Homo sapiens) | exact | meaning | Base assembly 2013-12-17 per NCBI revision history. Latest patch GRCh38.p14 = GCF_000001405.40 (verified, dataset_report). Not an OLS term |
| `GenomicReferenceEnum` | `grch37` | insdc.gcf:GCF_000001405.13 | GRCh37 (NCBI Assembly, Homo sapiens) | exact | meaning | Base assembly 2009-02-27; latest patch GRCh37.p13 = GCF_000001405.25. Verified via NCBI revision_history/check; dataset_report returns nothing for superseded accessions |
| `GenomicReferenceEnum` | `grcm39` | insdc.gcf:GCF_000001635.27 | GRCm39 (NCBI Assembly, Mus musculus) | exact | meaning | dataset_report verified |
| `GenomicReferenceEnum` | `grcm38` | insdc.gcf:GCF_000001635.20 | GRCm38 (NCBI Assembly, Mus musculus) | exact | meaning | Base assembly 2012-01-09; latest patch GRCm38.p6 = GCF_000001635.26 |
| `GenomicReferenceEnum` | `other` | — |  | no term needed | — | placeholder |
| `MatrixTypeEnum` | `raw_counts` | EDAM:data_3917 | Count matrix | close-broader | broad_mappings | EDAM definition: unnormalized summarised read counts; matches raw but not tied to single-cell |
| `MatrixTypeEnum` | `normalized_counts` | — |  | none | — | No matching OLS term |
| `MatrixTypeEnum` | `batch_corrected_counts` | — |  | none | — | No matching OLS term |
| `MatrixTypeEnum` | `scaled_counts` | — |  | none | — | No matching OLS term (OBI:0200185 scaling data transformation is a process, not a matrix type) |
| `TimeUnitEnum` | `hours` | UO:0000032 | hour | exact | meaning |  |
| `TimeUnitEnum` | `days` | UO:0000033 | day | exact | meaning |  |
| `TimeUnitEnum` | `weeks` | UO:0000034 | week | exact | meaning |  |
| `AgeUnitEnum` | `years` | UO:0000036 | year | exact | meaning |  |
| `AgeUnitEnum` | `months` | UO:0000035 | month | exact | meaning |  |
| `AgeUnitEnum` | `days` | UO:0000033 | day | exact | meaning |  |
| `AgeUnitEnum` | `days_post_conception` | UO:0000033 | day | close-broader | broad_mappings | Unit is day; post-conception reference is a qualifier not in UO |
| `EndoscopicStatusEnum` | `not_inflamed` | — |  | none | — | No 'not inflamed' / 'uninflamed' term found; do not use negation of PATO:0002104 |
| `EndoscopicStatusEnum` | `inflamed` | PATO:0002104 | inflamed | exact | meaning | NCIT:C3137 Inflammation is a process, not a quality |
| `EndoscopicStatusEnum` | `not_reported` | — |  | no term needed | — | placeholder |
| `TherapeuticResponseEnum` | `responder` | — |  | none | — | No generic responder term in NCIT/OLS; NCIT:C123619 Clinical Response is the broader concept (the attribute, not the value) |
| `TherapeuticResponseEnum` | `non_responder` | — |  | none | — | NCIT:C38014 Refractory ('Not responding to treatment') is close-narrower-ish but disease/treatment-resistance specific; not proposed |
| `TherapeuticResponseEnum` | `not_reported` | — |  | no term needed | — | placeholder |
| `SupportingFileTypeEnum` | `readme` | — |  | none | — | No README term |
| `SupportingFileTypeEnum` | `sample_metadata` | — |  | none | — | No matching term |
| `SupportingFileTypeEnum` | `protocol` | OBI:0000272 | protocol | exact | meaning | NCIT:C42651 Protocol is a looser alternative |
| `SupportingFileTypeEnum` | `data_dictionary` | — |  | none | — | T4FS:0000073 data dictionary exists in OLS but T4FS is an obscure ontology; not proposed |
| `SupportingFileTypeEnum` | `other` | — |  | no term needed | — | placeholder |
| `FunderEnum` | `ncats` | ror:04pw6fb54 | National Center for Advancing Translational Sciences | exact | meaning | ROR ID https://ror.org/04pw6fb54 verified via api.ror.org (active); also indexed in OLS as ror:04pw6fb54 |
| `FunderEnum` | `other` | — |  | no term needed | — | placeholder |
| `HostingEnum` | `synapse` | — |  | none | — | Repository-specific access mode; no ontology term |
| `HostingEnum` | `external_cloud` | — |  | none | — | Repository-specific access mode; no ontology term |
| `HostingEnum` | `external_download` | — |  | none | — | Repository-specific access mode; no ontology term |
| `HostingEnum` | `external_access` | — |  | none | — | Repository-specific access mode; no ontology term |
| `HostingEnum` | `mixed` | — |  | none | — | Repository-specific access mode; no ontology term |
| `HostingEnum` | `unavailable` | — |  | none | — | Repository-specific access mode; no ontology term |
| `AgeGroupEnum` | `infant` | NCIT:C27956 | Infant | exact | meaning | EFO:0001355 infant also exists (no definition) |
| `AgeGroupEnum` | `child` | NCIT:C16423 | Child | exact | meaning |  |
| `AgeGroupEnum` | `adolescent` | NCIT:C27954 | Adolescent | exact | meaning |  |
| `AgeGroupEnum` | `adult` | NCIT:C17600 | Adult | exact | meaning | EFO:0001272 adult also exists |
| `AgeGroupEnum` | `prenatal` | NCIT:C81318 | Prenatal | exact | meaning | Time period before birth. HsapDv:0000037 fetal stage / HsapDv:0000002 embryonic stage are narrower halves |
| `SingleCellLevel3and4FileFormatEnum` | `h5ad` | EDAM:format_3590 | HDF5 | close-broader | broad_mappings | No AnnData/h5ad class in EDAM; h5ad is HDF5-based. NOTE h5 already maps to the same term |
| `SingleCellLevel3and4FileFormatEnum` | `rds` | NCIT:C209895 | R Data Serialization | exact | meaning | No EDAM term; NCIT term verified |
| `SingleCellLevel3and4FileFormatEnum` | `seurat_object` | — |  | none | — | Seurat objects are typically stored as RDS; SWO:1100130 Seurat is the software, not a format |
| `SingleCellLevel3and4FileFormatEnum` | `bed_narrow_peak` | EDAM:format_3613 | ENCODE narrow peak format | exact | meaning |  |
| `BulkRNASeqLevel3and4FileFormatEnum` | `txt` | EDAM:format_1964 | plain text format (unformatted) | close-broader | broad_mappings | Alternative: EDAM:format_2330 Textual format (broader) |
| `BulkRNASeqLevel3and4FileFormatEnum` | `excel` | EDAM:format_3620 | xlsx | close-narrower | narrow_mappings | xls is EDAM:format_3468; no generic Excel class. Choose xlsx only if files are .xlsx |
| `BulkRNASeqLevel3and4FileFormatEnum` | `rds` | NCIT:C209895 | R Data Serialization | exact | meaning |  |
| `BulkRNASeqLevel3and4FileFormatEnum` | `h5ad` | EDAM:format_3590 | HDF5 | close-broader | broad_mappings |  |
| `BulkATACSeqLevel3and4FileFormatEnum` | `bed_narrow_peak` | EDAM:format_3613 | ENCODE narrow peak format | exact | meaning |  |
| `BulkATACSeqLevel3and4FileFormatEnum` | `bed_broad_peak` | EDAM:format_3614 | ENCODE broad peak format | exact | meaning |  |
| `BulkATACSeqLevel3and4FileFormatEnum` | `txt` | EDAM:format_1964 | plain text format (unformatted) | close-broader | broad_mappings | Alternative: EDAM:format_2330 Textual format |
| `BulkATACSeqLevel3and4FileFormatEnum` | `excel` | EDAM:format_3620 | xlsx | close-narrower | narrow_mappings | xls is EDAM:format_3468 |
| `BulkATACSeqLevel3and4FileFormatEnum` | `rds` | NCIT:C209895 | R Data Serialization | exact | meaning |  |
| `SpeciesEnum` | `mus_musculus_humanized` | EFO:0021426 | humanized mouse | close-narrower | narrow_mappings | EFO definition is specific to CYP1A1/CYP1A2 humanized mice, so it's a narrower class than 'humanized'; doubtful. Alternative: keep NCBITaxon:10090 with a note |
| `DiseaseFocusEnum` | `fibrotic_diseases` | EFO:0006890 | fibrosis | close-broader | broad_mappings | No MONDO class for fibrotic disease in general (MONDO:0100430 is liver-specific). EFO fibrosis is a pathological process; doubtful |
| `DiseaseFocusEnum` | `neurology` | NCIT:C16908 | Neurology | close-broader | broad_mappings | Medical specialty, not a disease class. Disease-class alternative: MONDO:0005071 nervous system disorder (check consistency with other DiseaseFocus values, which are MONDO diseases). Also EDAM:topic_3334 |
| `DiseaseFocusEnum` | `neurotoxicology` | — |  | none | — | Field of study. EFO:0011057 neurotoxicity is a phenotype, not the discipline; not proposed |
| `DiseaseFocusEnum` | `chemical_toxicology` | NCIT:C17206 | Toxicology | close-broader | broad_mappings | Also EDAM:topic_2840 Toxicology |
| `DiseaseFocusEnum` | `chemical_safety` | — |  | none | — | Only mesh:D062067 Chemical Safety (MeSH in OLS) found; not an ontology preferred for this domain |
| `DiseaseFocusEnum` | `other` | — |  | no term needed | — | placeholder |

## 4. `DataUseModifierEnum` (PR18-6)

For `enums.yaml`. Titles are the DUO short codes. Descriptions are the DUO
labels. Use it as the range of `data_use_modifiers`.

```yaml
  DataUseModifierEnum:
    description: GA4GH Data Use Ontology (DUO) permissions and modifiers.
    permissible_values:
      gru:
        title: "GRU"
        description: general research use
        meaning: DUO:0000042
      hmb:
        title: "HMB"
        description: health or medical or biomedical research
        meaning: DUO:0000006
      ds:
        title: "DS"
        description: disease specific research
        meaning: DUO:0000007
      poa:
        title: "POA"
        description: population origins or ancestry research only
        meaning: DUO:0000011
      nres:
        title: "NRES"
        description: no restriction
        meaning: DUO:0000004
      cc:
        title: "CC"
        description: clinical care use
        meaning: DUO:0000043
      gso:
        title: "GSO"
        description: genetic studies only
        meaning: DUO:0000016
      nmds:
        title: "NMDS"
        description: no general methods research
        meaning: DUO:0000015
      rs:
        title: "RS"
        description: research specific restrictions
        meaning: DUO:0000012
      col:
        title: "COL"
        description: collaboration required
        meaning: DUO:0000020
      irb:
        title: "IRB"
        description: ethics approval required
        meaning: DUO:0000021
      gs:
        title: "GS"
        description: geographical restriction
        meaning: DUO:0000022
      is:
        title: "IS"
        description: institution specific restriction
        meaning: DUO:0000028
      ncu:
        title: "NCU"
        description: non-commercial use only
        meaning: DUO:0000046
      npuncu:
        title: "NPUNCU"
        description: not for profit, non commercial use only
        meaning: DUO:0000018
      npu:
        title: "NPU"
        description: not for profit organisation use only
        meaning: DUO:0000045
      ps:
        title: "PS"
        description: project specific restriction
        meaning: DUO:0000027
      mor:
        title: "MOR"
        description: publication moratorium
        meaning: DUO:0000024
      pub:
        title: "PUB"
        description: publication required
        meaning: DUO:0000019
      rtn:
        title: "RTN"
        description: return to database or resource
        meaning: DUO:0000029
      ts:
        title: "TS"
        description: time limit on use
        meaning: DUO:0000025
      us:
        title: "US"
        description: user specific restriction
        meaning: DUO:0000026
```

## 5. `LicenseEnum` (PR18-7)

For `enums.yaml`. Titles are the NF-OSI PortalDataset values. 34 of the 46
values have an SPDX license ID as their `meaning`. The other 12 (licenses
with no version, `Public Domain` and `UNKNOWN`) have no SPDX ID. Use it as
the range of `license`.

```yaml
  LicenseEnum:
    description: >-
      License for reuse of the data. Values follow the NF-OSI PortalDataset
      schema. Versioned licenses map to SPDX license identifiers.
    permissible_values:
      cc_by_nc:
        title: "CC BY-NC"
      cc_by_nc_1_0:
        title: "CC BY-NC 1.0"
        meaning: spdx:CC-BY-NC-1.0
      cc_by_nc_2_0:
        title: "CC BY-NC 2.0"
        meaning: spdx:CC-BY-NC-2.0
      cc_by_nc_2_5:
        title: "CC BY-NC 2.5"
        meaning: spdx:CC-BY-NC-2.5
      cc_by_nc_3_0:
        title: "CC BY-NC 3.0"
        meaning: spdx:CC-BY-NC-3.0
      cc_by_nc_4_0:
        title: "CC BY-NC 4.0"
        meaning: spdx:CC-BY-NC-4.0
      cc_by_nc_nd:
        title: "CC BY-NC-ND"
      cc_by_nc_nd_1_0:
        title: "CC BY-NC-ND 1.0"
        meaning: spdx:CC-BY-NC-ND-1.0
      cc_by_nc_nd_2_0:
        title: "CC BY-NC-ND 2.0"
        meaning: spdx:CC-BY-NC-ND-2.0
      cc_by_nc_nd_2_5:
        title: "CC BY-NC-ND 2.5"
        meaning: spdx:CC-BY-NC-ND-2.5
      cc_by_nc_nd_3_0:
        title: "CC BY-NC-ND 3.0"
        meaning: spdx:CC-BY-NC-ND-3.0
      cc_by_nc_nd_4_0:
        title: "CC BY-NC-ND 4.0"
        meaning: spdx:CC-BY-NC-ND-4.0
      cc_by_nc_sa:
        title: "CC BY-NC-SA"
      cc_by_nc_sa_1_0:
        title: "CC BY-NC-SA 1.0"
        meaning: spdx:CC-BY-NC-SA-1.0
      cc_by_nc_sa_2_0:
        title: "CC BY-NC-SA 2.0"
        meaning: spdx:CC-BY-NC-SA-2.0
      cc_by_nc_sa_2_5:
        title: "CC BY-NC-SA 2.5"
        meaning: spdx:CC-BY-NC-SA-2.5
      cc_by_nc_sa_3_0:
        title: "CC BY-NC-SA 3.0"
        meaning: spdx:CC-BY-NC-SA-3.0
      cc_by_nc_sa_4_0:
        title: "CC BY-NC-SA 4.0"
        meaning: spdx:CC-BY-NC-SA-4.0
      cc_by_nd:
        title: "CC BY-ND"
      cc_by_nd_1_0:
        title: "CC BY-ND 1.0"
        meaning: spdx:CC-BY-ND-1.0
      cc_by_nd_2_0:
        title: "CC BY-ND 2.0"
        meaning: spdx:CC-BY-ND-2.0
      cc_by_nd_2_5:
        title: "CC BY-ND 2.5"
        meaning: spdx:CC-BY-ND-2.5
      cc_by_nd_3_0:
        title: "CC BY-ND 3.0"
        meaning: spdx:CC-BY-ND-3.0
      cc_by_nd_4_0:
        title: "CC BY-ND 4.0"
        meaning: spdx:CC-BY-ND-4.0
      cc_by_sa:
        title: "CC BY-SA"
      cc_by_sa_1_0:
        title: "CC BY-SA 1.0"
        meaning: spdx:CC-BY-SA-1.0
      cc_by_sa_2_0:
        title: "CC BY-SA 2.0"
        meaning: spdx:CC-BY-SA-2.0
      cc_by_sa_2_5:
        title: "CC BY-SA 2.5"
        meaning: spdx:CC-BY-SA-2.5
      cc_by_sa_3_0:
        title: "CC BY-SA 3.0"
        meaning: spdx:CC-BY-SA-3.0
      cc_by_sa_4_0:
        title: "CC BY-SA 4.0"
        meaning: spdx:CC-BY-SA-4.0
      cc_0:
        title: "CC-0"
      cc_by:
        title: "CC-BY"
      cc_by_1_0:
        title: "CC-BY 1.0"
        meaning: spdx:CC-BY-1.0
      cc_by_2_0:
        title: "CC-BY 2.0"
        meaning: spdx:CC-BY-2.0
      cc_by_2_5:
        title: "CC-BY 2.5"
        meaning: spdx:CC-BY-2.5
      cc_by_3_0:
        title: "CC-BY 3.0"
        meaning: spdx:CC-BY-3.0
      cc_by_4_0:
        title: "CC-BY 4.0"
        meaning: spdx:CC-BY-4.0
      cc0_1_0:
        title: "CC0 1.0"
        meaning: spdx:CC0-1.0
      odc_by:
        title: "ODC-BY"
      odc_by_1_0:
        title: "ODC-BY 1.0"
        meaning: spdx:ODC-By-1.0
      odc_odbl:
        title: "ODC-ODbL"
      odc_odbl_1_0:
        title: "ODC-ODbL 1.0"
        meaning: spdx:ODbL-1.0
      odc_pddl:
        title: "ODC-PDDL"
      odc_pddl_1_0:
        title: "ODC-PDDL 1.0"
        meaning: spdx:PDDL-1.0
      public_domain:
        title: "Public Domain"
      unknown:
        title: "UNKNOWN"
```
