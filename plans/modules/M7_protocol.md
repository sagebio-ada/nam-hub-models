# M7 protocol: Protocol

**Decisions (README section 4):** D4, D11, D24, D26, D27, D33

## Scope

Add a `Protocol` record. Each protocol is stored once, with its type,
version, link and parameters. Rows that used a protocol name it with
`protocol_id` (D24, D27).

This module adds the template and the link from SOP documents. Each user
module adds its own `protocol_id` link:

| Module | Template | Change |
|---|---|---|
| M3 | NAMs | `protocol_id` (multivalued): the protocols that define the NAM |
| M4 | `CultureProtocol` (is_a `Protocol`) | Culture parameters (FDA C.8) and device run conditions (FDA C.9) |
| M6 | Biospecimen | `protocol_id` (multivalued): the protocols that made the biospecimen from its parent |
| M8 | Exposure | `protocol_id`: the treatment protocol |
| M10 | `Sequencing` (all levels) | `protocol_id` replaces `protocol_link`. Level 1 names the wet-lab protocols. Level 2 and above name a `ComputationalProtocol` |
| M10 | `ComputationalProtocol` (is_a `Protocol`) | The workflow fields of Level 2 and above, `analysis_type` and `software` |

## Starting point

- `Sequencing` (all levels) has `protocol_link` (uri): "Link to the
  protocol used to prepare and sequence the library."
- Level 2 and above record their processing step in `workflow_name` and
  `workflow_version` (both required), `workflow_link` and
  `workflow_parameters_description`.
- `SupportingFile` has the `supporting_file_type` value `protocol`
  (`OBI:0000272`).
- No template holds the type, version or parameters of a protocol.

## Changes

One PR. Put the template in a new `modules/protocol.yaml`. Put
`protocol_id` in `core.yaml`, because several modules use it (M0 PR 1
rule). The Curator output changes (minor version: new template and one
optional column).

### `Protocol` (new; global `protocol_id`)

| Slot | Source and anchor (candidate) | Range |
|---|---|---|
| `protocol_id` | Key. Global, because studies share protocols (D11; M0 open question 1). | string |
| `protocol_name` (required) | ISA Protocol `name` | text |
| `protocol_type` (required) | ISA Protocol `protocolType`; OBI planned-process terms; C2M2 `biosample.sample_prep_method` for the sample-preparation values | enum: cell culture, differentiation, dissociation, nuclei isolation, sectioning, nucleic acid extraction, library preparation, sequencing, treatment, data transformation (`OBI:0200000`), other |
| `protocol_version` | ISA Protocol `version` | text |
| `protocol_link` | ISA Protocol `uri`. A protocols.io page, a DOI, a code repository, a notebook or another URL. M10 removes this slot from `Sequencing`. | uri |
| `description` | Reuse the shared slot | text |
| `parameters_description` | ISA Protocol parameters; FDA C.1 (test-method detail) | text |
| `previous_version_protocol_id` | `prov:wasRevisionOf` | `protocol_id` |

Make a new row for each new version of a protocol. Rows that used the old
version keep their link to it.

Give each `protocol_type` value an OBI `meaning` after the OLS check. Record
a value with no term as NAMHub-minted.

### `SupportingFile`

Add `protocol_id` (optional). It links an SOP document
(`supporting_file_type` = protocol) to its `Protocol` record. The document
names the protocol. The protocol does not list its documents (one
direction, README section 2).

**Reason:** One protocol serves many biospecimens, exposures and files. A
record stores its type, version and parameters once, and a correction is
made once (D27). Before this module, the only protocol data was a URL that
repeats on every sequencing file.

### FUSION mapping (D33)

Source: the FUSION (NDHCC) LinkML model, version 1.2.0-wave2r4. FUSION
projects its NF protocol template the same way.

- `Protocol` is an exact mapping to `ndhcc:ProtocolVersion`. One row is one
  version.
- `protocol_version` maps to `version_label`.
- `protocol_link` maps to `protocol_uri`.
- `protocol_type` maps to Protocol `protocol_type`.

## Checks

- The checks in README section 2.
- The Curator diff shows only the new `Protocol` template and the optional
  `protocol_id` column on `SupportingFile`.

## Assumptions

1. Submitters fill the `Protocol` rows before the rows that name them.
2. Computational processing is a `Protocol` too: a `ComputationalProtocol`
   row (M10) with `protocol_type` data transformation. ISA models data
   processing as a process that runs a protocol.

## Open questions

1. Parameters as structured rows (name, value and unit for each parameter,
   as ISA ProtocolParameter) or as free text? Recommendation: free text in
   `parameters_description`. The typed fields of `CultureProtocol` (M4)
   hold the FDA C.8 and C.9 parameters, and `ComputationalProtocol` (M10)
   holds `analysis_type` and `software`.
