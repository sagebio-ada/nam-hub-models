# M0 core: module split, keys, shared mixins, anchoring

**Decisions:** D1, D3, D4, D6, D11, D13, D14, D25a

- D1: Merge PR #18 first, as version 4.0.0, with the review fixes.
- D4: Keep the PR #18 key names.
- D6: Use static enums for submitter fields. Use pattern strings for very large vocabularies.
- D11: PR #18 IDs are study-scoped for records and global for catalog entries.
- D13: On hold.
- D25a: Files use the Synapse ID as key.

## Scope

1. Split `namhub.yaml` into module files. Do not change the generated output.
2. Make `docs/model_decisions.md`.
3. Add anchors to every existing element. Do not change the generated output.
4. Add the shared `Record` and `PublishedRecord` mixins. Add the key conventions that later modules use.

## Starting point

- `src/namhub/schema/namhub.yaml` holds 27 templates, 7 abstract classes and mixins, and all slots. The 27 templates are 26 from PR #18 and `NAMPortalDataset` from PR #22.
- `enums.yaml` holds 45 enums.
- No element has a `class_uri`, `slot_uri` or mapping. Before the review fixes, 76 of 623 enum values have a `meaning`.
- Keys use the form `<entity>_id`.
  - Individual and Biospecimen have `unique_keys` on `study_id` + `<entity>_id`.
  - Treatment has a composite key.
  - Files have no ID slot. Curator annotates the Synapse entity.

### Fixed in PR #18 and PR #22 before this plan starts

The PR #18 review and the PR #22 review (README section 5) ask for these changes. This plan assumes that they are merged.

- Version 4.0.0 (PR #18 review, PR18-1).
- `nam_id` is single-valued in NAMs. `NAMs.dataset_id` and `dataset_id_list` are removed (PR18-2, PR18-3).
- The Diagnosis key is `study_id` + `individual_id` + `diagnosis` (PR18-4).
- `parent_file_id` is optional. It accepts a Synapse ID, a CURIE or a URL (PR18-5).
- `data_use_modifiers` uses `DataUseModifierEnum` (DUO). `license` uses `LicenseEnum` (SPDX) (PR18-6, PR18-7).
- The `namo` prefix, the `namo_id` pattern and the `enums.yaml` `default_prefix` are fixed (PR18-9).
- The PR #18 and PR #22 enums have terms (PR18-10). The terms are in `docs/pr18_enum_terms.md` on the PR #18 branch.
- ID titles use the form "Study ID" (PR18-11).
- `tissue` is a multivalued `TissueEnum` slot (PR18-12).
- `parent_biospecimen_id` is multivalued, for co-cultures (PR18-14).

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

- Put a slot that more than one module uses in `core.yaml`.
- Put a slot that one module uses in that module.
- Make each module import `core` and `enums`.
- Make `namhub.yaml` import every module.
- Do not make a module import another module. This prevents cycles.
- Keep the enums in `enums.yaml` in this PR. Each module PR moves its own enums. This keeps this PR a pure move.
- Move `IBDDiagnosis` to `ext_ibd.yaml` without change.
- Move `endoscopic_status` to `ext_ibd.yaml` in the M6 PR. That change alters the output.
- Update the repository-structure section of `README.md` to list the new files. This is the only documentation change.

**Reason:** A scratch test split records and slots into separate files with a nested relative import. The output stayed byte-identical, and both linters passed.

### PR 2: decision log and anchors, no output change

- Make `docs/model_decisions.md`. Add one entry for each of D1 to D25. Each entry gives what, why, sources and date. Add the source-by-source findings. Later PRs append entries.
- Add anchors to every existing class, slot and enum value.

Classes:

- Use `class_uri` where a standard class IRI exists. Otherwise use `exact_mappings` or `close_mappings`.
- Candidates:

| Class | Candidate anchor |
|---|---|
| Studies | ISA Study; C2M2 `project` |
| Datasets | schema.org `Dataset`; C2M2 `collection` |
| People | schema.org `Person` |
| Publications | schema.org `ScholarlyArticle` |
| Grants | schema.org `Grant` |
| Individual | C2M2 `subject` |
| Biospecimen | OBI specimen; C2M2 `biosample` |
| File | C2M2 `file` |

Slots:

- Use `slot_uri` for a schema.org, Dublin Core, PROV-O or C2M2 field URI where one fits. Examples: `filename`, `md5`, `doi`, `license`, `description`, `release_date`, and `parent_file_id` → `prov:wasDerivedFrom`.
- Otherwise use `see_also` and `source`. Name the document and the field (HTAN2, GDC, MC2, CELLxGENE, GEO).

Enum values:

- PR #18 gives terms to the PR #18 and PR #22 enums (PR18-10). This PR does the other enums.
- For `AssayEnum`, `DataCategoryEnum` and `FileFormatEnum`, start from the NF metadata dictionary terms. 233 of the values have a term. Examine each term in OLS.
- Use the PR18-10 rule. Put an exact term in `meaning`. Put a wider or narrower term in `broad_mappings` or `narrow_mappings`.
- Record a value with no term as NAMHub-minted in the decision log.

Prefixes:

- Add the prefixes that the anchors need: OBI, IAO, HANCESTRO, PROV, dcterms and BAO. PATO and UO come with PR18-10.
- Keep EFO and EDAM on identifiers.org. `linkml-lint` (`canonical_prefixes`) gives a warning for any other namespace.

Checks for this PR:

- The generated Curator JSON is byte-identical. A scratch test showed that `class_uri`, `slot_uri`, `exact_mappings`, `see_also` and enum `meaning` leave it unchanged.
- Run `gen-jsonld`. Check that the anchors appear.

Size: this PR is large. If review gets hard, split it into one PR for each module file. Keep each PR byte-identical.

Open points for the anchors are in the open questions (question 3).

### PR 3: shared mixins and key conventions (output changes)

Make this PR with the first module PR that uses the mixins, or just before it. That PR is M10 or M2.

`Record` mixin:

- Add `persistent_id`. It accepts a DOI, ARK, Synapse ID or CURIE. It never accepts a bare download URL (C2M2 rule).
- Apply it to every template.

`PublishedRecord` mixin, for Datasets, NAMPortalDataset, NAMs and File:

- `license`. NAMs has it with `LicenseEnum` after PR18-7. Move it to `core`.
- `metadata_license` (FAIRshake 17 and 18). Use the same enum.
- `landing_page`, `access_url`, `access_protocol` (FAIRshake 8 and 9).
- `creator`. Reuse the PR #22 slot.
- `contact_email`, `institution_ror` (FAIRshake 7 and 16).
- `grant_id`. It exists (FAIRshake 6).
- `program` waits for D13.

Key conventions. Write them in the decision log. Every module plan uses them.

- Records: use `<entity>_id`. It is unique within a study (`unique_keys` with `study_id`).
- Link records with no ID of their own (Diagnosis, Treatment): use a composite key. The key has `study_id`, the ID of the linked record and the linked value. Example: `study_id` + `individual_id` + `diagnosis`.
- Catalog entries that studies share: use a global `<entity>_id`. Today this is `nam_id`. The other plans add `protocol_id`, `test_article_id` and `device_id`.
- Links reuse the slot name of the target key. Self-links use `parent_<entity>_id`.
- Files: the key is the Synapse ID, made on upload. A link to a parent file accepts a Synapse ID, a CURIE or a URL, because a parent can be in a different repository (PR18-5).
- ID titles use the form "{Term} ID". Example: "Study ID" (PR18-11).
- Give each link slot a `slot_uri` or mapping to its PROV-O or RO predicate.

## Checks

- The checks in README section 2.
- PR 1 and PR 2: the generated Curator JSON is byte-identical to the build from `main` after PR #18 merges.
- Directory-form `linkml-lint` passes on the split scratch copy. `uv run gen-jsonld` is available.

## Assumptions

1. PR #18 merges before PR 1, with the review fixes, as version 4.0.0. PR 1 diffs against that merge. Each later PR that changes the Curator output increases the version from 4.0.0.
2. When `license` moves into `core` and File gets `PublishedRecord`, every file template gets new columns. Submitters can leave them empty.

## Open questions

1. Must the `PublishedRecord` fields be optional everywhere, or required on Datasets only? FAIRshake scores each dataset. Recommendation: make them optional on File and NAMs. Require `license` on Datasets.
2. `persistent_id` on records such as Individual and Biospecimen is usually empty. Apply `Record` only to Datasets, NAMs and File instead?
3. Open points for the class and slot anchors (PR 2):
   - (a) Fields of other data models (C2M2, GDC, HTAN2, CELLxGENE, the NF dataset schema) have no IRI for each field. Declare NAMHub-defined prefixes that point to each specification at a fixed commit, use `see_also`, or leave them out? Recommendation: use the prefixes.
   - (b) Where no property exists, use an NCIT data-element class as `slot_uri`? HTAN2 does the same with caDSR. Recommendation: yes.
   - (c) Some slots are a key in one template and a link in others (`nam_id`, `dataset_id`, `grant_id`). Give them no `slot_uri` and a related mapping to `schema:identifier`? Recommendation: yes.
