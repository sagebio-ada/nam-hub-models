from __future__ import annotations

import re
import sys
from datetime import (
    date,
    datetime,
    time
)
from decimal import Decimal
from enum import Enum
from typing import (
    Any,
    ClassVar,
    Literal,
    Optional,
    Union
)

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    RootModel,
    SerializationInfo,
    SerializerFunctionWrapHandler,
    field_validator,
    model_serializer
)


metamodel_version = "1.11.0"
version = "None"


class ConfiguredBaseModel(BaseModel):
    model_config = ConfigDict(
        serialize_by_alias = True,
        validate_by_name = True,
        validate_assignment = True,
        validate_default = True,
        extra = "forbid",
        arbitrary_types_allowed = True,
        use_enum_values = True,
        strict = False,
    )





class LinkMLMeta(RootModel):
    root: dict[str, Any] = {}
    model_config = ConfigDict(frozen=True)

    def __getattr__(self, key:str):
        return getattr(self.root, key)

    def __getitem__(self, key:str):
        return self.root[key]

    def __setitem__(self, key:str, value):
        self.root[key] = value

    def __contains__(self, key:str) -> bool:
        return key in self.root


linkml_meta = LinkMLMeta({'default_prefix': 'namhub',
     'default_range': 'string',
     'description': 'NAMHub portal data schemas — backend Synapse tables and the '
                    'Landscape data collection form. Portal tables are backed by '
                    'Synapse project syn74360399. NAM classification uses the New '
                    'Approach Methods Ontology (NAMO) developed by the Monarch '
                    'Initiative (https://github.com/monarch-initiative/namo).',
     'id': 'https://namhub.synapse.org/portal_schemas',
     'imports': ['linkml:types', 'enums'],
     'name': 'namhub',
     'prefixes': {'duo': {'prefix_prefix': 'duo',
                          'prefix_reference': 'http://purl.obolibrary.org/obo/DUO_'},
                  'linkml': {'prefix_prefix': 'linkml',
                             'prefix_reference': 'https://w3id.org/linkml/'},
                  'namhub': {'prefix_prefix': 'namhub',
                             'prefix_reference': 'https://namhub.synapse.org/portal_schemas/'},
                  'namo': {'prefix_prefix': 'namo',
                           'prefix_reference': 'https://github.com/monarch-initiative/namo/'},
                  'schema': {'prefix_prefix': 'schema',
                             'prefix_reference': 'http://schema.org/'}},
     'source_file': 'src/namhub/schema/namhub.yaml'} )

class AssayEnum(str, Enum):
    """
    Experimental method used to generate files in the dataset.
    """
    ATAC_seq = "ATAC-seq"
    CAPP_seq = "CAPP-seq"
    CUTAMPERSANDRUN = "CUT&RUN"
    ChIP_seq = "ChIP-seq"
    ERR_bisulfite_sequencing = "ERR bisulfite sequencing"
    HI_C = "HI-C"
    ISO_seq = "ISO-seq"
    NOMe_seq = "NOMe-seq"
    RNA_array = "RNA array"
    RNA_seq = "RNA-seq"
    SNP_array = "SNP array"
    SaferSeqS = "SaferSeqS"
    Sanger_sequencing = "Sanger sequencing"
    T_cell_receptor_repertoire_sequencing = "T cell receptor repertoire sequencing"
    bisulfite_sequencing = "bisulfite sequencing"
    jumping_library = "jumping library"
    lncRNA_seq = "lncRNA-seq"
    methylation_array = "methylation array"
    miRNA_array = "miRNA array"
    miRNA_seq = "miRNA-seq"
    next_generation_sequencing = "next-generation sequencing"
    next_generation_targeted_sequencing = "next generation targeted sequencing"
    oxBS_seq = "oxBS-seq"
    ribo_seq = "ribo-seq"
    scCGI_seq = "scCGI-seq"
    single_cell_ATAC_seq = "single cell ATAC-seq"
    single_cell_RNA_seq = "single-cell RNA-seq"
    single_nucleus_RNA_seq = "single-nucleus RNA-seq"
    spatial_transcriptomics = "spatial transcriptomics"
    targeted_exome_sequencing = "targeted exome sequencing"
    whole_exome_sequencing = "whole exome sequencing"
    whole_genome_sequencing = "whole genome sequencing"
    number_3D_confocal_imaging = "3D confocal imaging"
    number_3D_electron_microscopy = "3D electron microscopy"
    number_3D_imaging = "3D imaging"
    CODEX = "CODEX"
    DNA_optical_mapping = "DNA optical mapping"
    Fluorescence_In_Situ_Hybridization = "Fluorescence In Situ Hybridization"
    Magnetization_Prepared_Rapid_Gradient_Echo_MRI = "Magnetization-Prepared Rapid Gradient Echo MRI"
    SUSHI = "SUSHI"
    atomic_force_microscopy = "atomic force microscopy"
    autoradiography = "autoradiography"
    brightfield_microscopy = "brightfield microscopy"
    live_imaging = "live imaging"
    histology = "histology"
    confocal_microscopy = "confocal microscopy"
    conventional_MRI = "conventional MRI"
    diffusion_MRI = "diffusion MRI"
    fluorescence_microscopy_assay = "fluorescence microscopy assay"
    functional_MRI = "functional MRI"
    gel_filtration_chromatography = "gel filtration chromatography"
    high_content_screen = "high content screen"
    high_frequency_ultrasound = "high frequency ultrasound"
    immunocytochemistry = "immunocytochemistry"
    immunofluorescence = "immunofluorescence"
    immunohistochemistry = "immunohistochemistry"
    in_vivo_bioluminescence = "in vivo bioluminescence"
    laser_speckle_imaging = "laser speckle imaging"
    magnetic_resonance_angiography = "magnetic resonance angiography"
    magnetic_resonance_spectroscopy = "magnetic resonance spectroscopy"
    optical_coherence_tomography = "optical coherence tomography"
    optical_tomography = "optical tomography"
    phase_contrast_microscopy = "phase-contrast microscopy"
    photograph = "photograph"
    positron_emission_tomography = "positron emission tomography"
    spatial_frequency_domain_imaging = "spatial frequency domain imaging"
    traction_force_microscopy = "traction force microscopy"
    transcranial_doppler_ultrasonography = "transcranial doppler ultrasonography"
    western_blot = "western blot"
    FIA_MSMS = "FIA-MSMS"
    FTIR_spectroscopy = "FTIR spectroscopy"
    MIBSOLIDUSMS = "MIB/MS"
    MudPIT = "MudPIT"
    RPPA = "RPPA"
    TMT_quantitation = "TMT quantitation"
    high_performance_liquid_chromatographySOLIDUStandem_mass_spectrometry = "high-performance liquid chromatography/tandem mass spectrometry"
    label_free_mass_spectrometry = "label free mass spectrometry"
    liquid_chromatography_electrochemical_detection = "liquid chromatography-electrochemical detection"
    liquid_chromatographySOLIDUSmass_spectrometry = "liquid chromatography/mass spectrometry"
    liquid_chromatographySOLIDUStandem_mass_spectrometry = "liquid chromatography/tandem mass spectrometry"
    mass_spectrometry = "mass spectrometry"
    proximity_extension_assay = "proximity extension assay"
    SomaScan = "SomaScan"
    ultra_high_performance_liquid_chromatographySOLIDUStandem_mass_spectrometry = "ultra high-performance liquid chromatography/tandem mass spectrometry"
    AlgometRx_Nociometer = "AlgometRx Nociometer"
    quantitative_sensory_testing = "quantitative sensory testing"
    Child_Behavior_Checklist_for_Ages_1FULL_STOP5_5 = "Child Behavior Checklist for Ages 1.5-5"
    Child_Behavior_Checklist_for_Ages_6_18 = "Child Behavior Checklist for Ages 6-18"
    ChildrenAPOSTROPHEs_Dermatology_Life_Quality_Index_Questionnaire = "Children's Dermatology Life Quality Index Questionnaire"
    Corsi_blocks = "Corsi blocks"
    FACE_Q_Appearance_related_Distress = "FACE-Q Appearance-related Distress"
    Focus_group = "Focus group"
    Interview = "Interview"
    NIH_Toolbox = "NIH Toolbox"
    PROMIS_Cognitive_Function = "PROMIS Cognitive Function"
    Riccardi_and_Ablon_scales = "Riccardi and Ablon scales"
    Skindex_16 = "Skindex-16"
    Social_Responsiveness_Scale = "Social Responsiveness Scale"
    Social_Responsiveness_Scale_Second_Edition = "Social Responsiveness Scale Second Edition"
    Von_Frey_test = "Von Frey test"
    actigraphy = "actigraphy"
    active_avoidance_learning_behavior_assay = "active avoidance learning behavior assay"
    auditory_brainstem_response = "auditory brainstem response"
    blood_chemistry_measurement = "blood chemistry measurement"
    body_size_trait_measurement = "body size trait measurement"
    cNF_Skindex = "cNF-Skindex"
    clinical_data = "clinical data"
    cognitive_assessment = "cognitive assessment"
    contextual_conditioning_behavior_assay = "contextual conditioning behavior assay"
    distortion_product_otoacoustic_emissions = "distortion product otoacoustic emissions"
    elevated_plus_maze_test = "elevated plus maze test"
    feeding_assay = "feeding assay"
    gait_measurement = "gait measurement"
    genotyping = "genotyping"
    grip_strength = "grip strength"
    hand_held_dynamometry = "hand-held dynamometry"
    metabolic_screening = "metabolic screening"
    n_back_task = "n-back task"
    neuropsychological_assessment = "neuropsychological assessment"
    novelty_response_behavior_assay = "novelty response behavior assay"
    open_field_test = "open field test"
    optokinetic_reflex_assay = "optokinetic reflex assay"
    pattern_electroretinogram = "pattern electroretinogram"
    polysomnography = "polysomnography"
    pure_tone_average = "pure tone average"
    questionnaire = "questionnaire"
    rotarod_performance_test = "rotarod performance test"
    scale = "scale"
    six_minute_walk_test = "six-minute walk test"
    weight = "weight"
    survival = "survival"
    word_recognition_score = "word recognition score"
    number_2D_AlamarBlue_absorbance = "2D AlamarBlue absorbance"
    number_2D_AlamarBlue_fluorescence = "2D AlamarBlue fluorescence"
    number_3D_microtissue_viability = "3D microtissue viability"
    ATPase_activity_assay = "ATPase activity assay"
    BrdU_proliferation_assay = "BrdU proliferation assay"
    ELISA = "ELISA"
    EdU_proliferation_assay = "EdU proliferation assay"
    FLIPR_high_throughput_cellular_screening = "FLIPR high-throughput cellular screening"
    HPLC = "HPLC"
    Migration_Assay = "Migration Assay"
    STR_profile = "STR profile"
    TIDE = "TIDE"
    TriKinetics_activity_monitoring = "TriKinetics activity monitoring"
    array = "array"
    blue_native_PAGE = "blue native PAGE"
    SDS_PAGE = "SDS-PAGE"
    bone_histomorphometry = "bone histomorphometry"
    cAMP_Glo_Max_Assay = "cAMP-Glo Max Assay"
    calcium_retention_capacity_assay = "calcium retention capacity assay"
    cell_competition = "cell competition"
    cell_count = "cell count"
    cell_painting = "cell painting"
    cell_permeability_assay = "cell permeability assay"
    cell_proliferation = "cell proliferation"
    cell_viability_assay = "cell viability assay"
    combination_library_screen = "combination library screen"
    combination_screen = "combination screen"
    complex_II_enzyme_activity_assay = "complex II enzyme activity assay"
    compound_screen = "compound screen"
    current_clamp_assay = "current clamp assay"
    differential_scanning_calorimetry = "differential scanning calorimetry"
    dynamic_light_scattering = "dynamic light scattering"
    electrochemiluminescence = "electrochemiluminescence"
    electrophoretic_light_scattering = "electrophoretic light scattering"
    flow_cytometry = "flow cytometry"
    focus_forming_assay = "focus forming assay"
    gel_permeation_chromatography = "gel permeation chromatography"
    immunoassay = "immunoassay"
    in_silico_synthesis = "in silico synthesis"
    in_vitro_tumorigenesis = "in vitro tumorigenesis"
    in_vivo_PDX_viability = "in vivo PDX viability"
    in_vivo_tumor_growth = "in vivo tumor growth"
    light_scattering_assay = "light scattering assay"
    local_field_potential_recording = "local field potential recording"
    long_term_potentiation_assay = "long term potentiation assay"
    massively_parallel_reporter_assay = "massively parallel reporter assay"
    microrheology = "microrheology"
    multi_electrode_array = "multi-electrode array"
    nanoparticle_tracking_analysis = "nanoparticle tracking analysis"
    oscillatory_rheology = "oscillatory rheology"
    oxygen_consumption_assay = "oxygen consumption assay"
    perineurial_cell_thickness = "perineurial cell thickness"
    pharmocokinetic_ADME_assay = "pharmocokinetic ADME assay"
    polymerase_chain_reaction = "polymerase chain reaction"
    quantitative_PCR = "quantitative PCR"
    reactive_oxygen_species_assay = "reactive oxygen species assay"
    reporter_gene_assay = "reporter gene assay"
    split_GFP_assay = "split-GFP assay"
    rheometry = "rheometry"
    sandwich_ELISA = "sandwich ELISA"
    single_molecule_drug_screen_assay = "single molecule drug screen assay"
    small_molecule_library_screen = "small molecule library screen"
    sorbitol_dehydrogenase_activity_level_assay = "sorbitol dehydrogenase activity level assay"
    static_histomorphometry = "static histomorphometry"
    static_light_scattering = "static light scattering"
    trans_endothelial_electrical_resistance = "trans-endothelial electrical resistance"
    twin_spot_assay = "twin spot assay"
    whole_cell_patch_clamp = "whole-cell patch clamp"
    Unknown = "Unknown"


class SpeciesEnum(str, Enum):
    """
    Species of origin.
    """
    Danio_rerio = "Danio rerio"
    Drosophila_melanogaster = "Drosophila melanogaster"
    Gallus_gallus = "Gallus gallus"
    Homo_sapiens = "Homo sapiens"
    Mus_musculus = "Mus musculus"
    Macaca_nemestrina = "Macaca nemestrina"
    Mus_musculus_LEFT_PARENTHESIShumanizedRIGHT_PARENTHESIS = "Mus musculus (humanized)"
    Oryctolagus_cuniculus = "Oryctolagus cuniculus"
    Pan_troglodytes = "Pan troglodytes"
    Rattus_norvegicus = "Rattus norvegicus"
    Rhesus_macaque = "Rhesus macaque"
    Sus_scrofa = "Sus scrofa"
    Unknown = "Unknown"


class FileFormatEnum(str, Enum):
    """
    File extension or format type.
    """
    bai = "bai"
    bam = "bam"
    bcf = "bcf"
    bed = "bed"
    bed_broadPeak = "bed broadPeak"
    bed_gappedPeak = "bed gappedPeak"
    bed_narrowPeak = "bed narrowPeak"
    bedgraph = "bedgraph"
    bgzip = "bgzip"
    cloupe = "cloupe"
    bigwig = "bigwig"
    cnn = "cnn"
    cnr = "cnr"
    cns = "cns"
    crai = "crai"
    cram = "cram"
    csi = "csi"
    ctab = "ctab"
    dup = "dup"
    fasta = "fasta"
    fastq = "fastq"
    flagstat = "flagstat"
    gct = "gct"
    gff3 = "gff3"
    gtf = "gtf"
    hic = "hic"
    maf = "maf"
    mtx = "mtx"
    plink = "plink"
    recal = "recal"
    sam = "sam"
    seg = "seg"
    sf = "sf"
    sra = "sra"
    tagAlign = "tagAlign"
    tbi = "tbi"
    tranches = "tranches"
    vcf = "vcf"
    wiggle = "wiggle"
    DICOM = "DICOM"
    NWB = "NWB"
    PAR = "PAR"
    REC = "REC"
    aci = "aci"
    avi = "avi"
    bmp = "bmp"
    czi = "czi"
    dm3 = "dm3"
    hdr = "hdr"
    img = "img"
    jpg = "jpg"
    lif = "lif"
    mov = "mov"
    nii = "nii"
    ome_tiff = "ome-tiff"
    png = "png"
    svs = "svs"
    sws = "sws"
    tif = "tif"
    tom = "tom"
    Sentrix_descriptor_file = "Sentrix descriptor file"
    bpm = "bpm"
    cel = "cel"
    chp = "chp"
    dat = "dat"
    idat = "idat"
    locs = "locs"
    msf = "msf"
    mzML = "mzML"
    raw = "raw"
    RCC = "RCC"
    csv = "csv"
    excel = "excel"
    parquet = "parquet"
    tsv = "tsv"
    MATLAB_script = "MATLAB script"
    Python_script = "Python script"
    R_script = "R script"
    bash_script = "bash script"
    js = "js"
    MATLAB_data = "MATLAB data"
    RData = "RData"
    SDAT = "SDAT"
    SPAR = "SPAR"
    json = "json"
    prism = "prism"
    rds = "rds"
    sqlite = "sqlite"
    xml = "xml"
    yaml = "yaml"
    number_7z = "7z"
    docker_image = "docker image"
    gzip = "gzip"
    tar = "tar"
    zip = "zip"
    ai = "ai"
    doc = "doc"
    html = "html"
    hyperlink = "hyperlink"
    md = "md"
    pdf = "pdf"
    powerpoint = "powerpoint"
    txt = "txt"
    MPEG_4 = "MPEG-4"
    ab1 = "ab1"
    abf = "abf"
    dna = "dna"
    edat3 = "edat3"
    fcs = "fcs"
    fig = "fig"
    gb = "gb"
    h5 = "h5"
    hdf5 = "hdf5"
    idx = "idx"
    psydat = "psydat"
    pzfx = "pzfx"
    rmd = "rmd"
    sav = "sav"
    sdf = "sdf"
    sif = "sif"
    svg = "svg"
    Unknown = "Unknown"
    Ome_zarr = "Ome-zarr"
    Github_Repo = "Github Repo"


class DataCategoryEnum(str, Enum):
    """
    Categorical label for data contained in a dataset.
    """
    aligned_reads = "aligned reads"
    annotated_germline_variants = "annotated germline variants"
    annotated_somatic_mutation = "annotated somatic mutation"
    audio_transcript = "audio transcript"
    behavioral_data = "behavioral data"
    capsid_sequence = "capsid sequence"
    cellular_physiology = "cellular physiology"
    characteristic = "characteristic"
    chromatin_activity = "chromatin activity"
    clinical = "clinical"
    copy_number_variants = "copy number variants"
    count_matrix = "count matrix"
    data_index = "data index"
    data_sharing_plan = "data sharing plan"
    demographics = "demographics"
    drug_combination_screen = "drug combination screen"
    drug_screen = "drug screen"
    electrophysiology = "electrophysiology"
    epidemiological_data = "epidemiological data"
    gene_expression = "gene expression"
    gene_expression_matrix = "gene expression matrix"
    quantified_gene_expression = "quantified gene expression"
    genomic_features = "genomic features"
    genomic_variants = "genomic variants"
    germline_variants = "germline variants"
    guide_RNA_sequence = "guide RNA sequence"
    image = "image"
    immunoassay = "immunoassay"
    isoform_expression = "isoform expression"
    kinomics = "kinomics"
    mask_image = "mask image"
    mass_spectrometry_data = "mass spectrometry data"
    metabolomics = "metabolomics"
    model = "model"
    molecular_property = "molecular property"
    morphology_parameter = "morphology parameter"
    network = "network"
    nucleic_acid_sequence_record = "nucleic acid sequence record"
    over_representation_data = "over-representation data"
    particle_characterization = "particle characterization"
    pharmacokinetics = "pharmacokinetics"
    physiology_parameter = "physiology parameter"
    plasmid_sequence = "plasmid sequence"
    plot = "plot"
    primer_sequence = "primer sequence"
    probe_sequence = "probe sequence"
    promoter_sequence = "promoter sequence"
    protein_interaction_data = "protein interaction data"
    protein_interaction_raw_data = "protein interaction raw data"
    proteomics = "proteomics"
    raw_counts = "raw counts"
    reference_sequence = "reference sequence"
    report = "report"
    somatic_variants = "somatic variants"
    structural_variants = "structural variants"
    survey_data = "survey data"
    text_data = "text data"
    volume = "volume"
    weight = "weight"
    Unknown = "Unknown"


class ProcessLevelEnum(str, Enum):
    """
    Level of data processing applied to the dataset.
    """
    Level_1 = "Level 1"
    """
    Raw or minimally processed data.
    """
    Level_2 = "Level 2"
    """
    Data that has undergone a basic or initial processing step, like quality control, alignment, or stitching.
    """
    Level_3 = "Level 3"
    """
    Files that contain summary counts, coverage files, or other processed representations of the data.
    """
    Level_4 = "Level 4"
    """
    Files that contain data related to applied models or aggregate representations of the data.
    """
    Auxiliary = "Auxiliary"
    """
    Additional files that contain information or experimental details, but do not contain data or processed derivatives.
    """
    Not_Applicable = "Not Applicable"
    """
    Files that fall outside of the level structure or are uploaded as a package.
    """
    Metadata = "Metadata"
    """
    Files that are or will be stored and shared as metadata.
    """


class NamContextEnum(str, Enum):
    """
    NAM application context associated with files in the dataset.
    """
    Biosamples = "Biosamples"
    Subjects_SOLIDUS_Donors = "Subjects / Donors"
    Files_SOLIDUS_Data_Types = "Files / Data Types"
    In_Chemico_SOLIDUS_Biomaterials = "In Chemico / Biomaterials"
    Assays_SOLIDUS_Conditions = "Assays / Conditions"
    Ontologies_SOLIDUS_Standards = "Ontologies / Standards"
    Imaging_Metadata = "Imaging Metadata"
    Pharmacokinetics_SOLIDUS_ADMET = "Pharmacokinetics / ADMET"
    Analytical_Models = "Analytical Models"


class RepositoryEnum(str, Enum):
    """
    Repository where a dataset is hosted.
    """
    Synapse = "Synapse"
    GEO = "GEO"
    SRA = "SRA"
    Zenodo = "Zenodo"
    Other = "Other"


class AccessTypeEnum(str, Enum):
    """
    Data access level.
    """
    Open = "Open"
    """
    Publicly accessible without restrictions.
    """
    Controlled = "Controlled"
    """
    Requires approval via Synapse Access Requirements.
    """
    Embargoed = "Embargoed"
    """
    Temporarily restricted; will become open after embargo lifts.
    """


class DevelopmentStatusEnum(str, Enum):
    """
    Current development stage of a NAM.
    """
    Validated = "Validated"
    """
    Method has been formally validated.
    """
    In_Development = "In Development"
    """
    Method is being actively developed.
    """
    Prototype = "Prototype"
    """
    Early-stage implementation.
    """
    Deprecated = "Deprecated"
    """
    Method is no longer actively maintained.
    """


class RoleEnum(str, Enum):
    """
    Role of a person in the NAMHub program.
    """
    Principal_Investigator = "Principal Investigator"
    Co_Investigator = "Co-Investigator"
    Collaborator = "Collaborator"
    Coordinating_Center = "Coordinating Center"
    Trainee = "Trainee"
    Other = "Other"



class Landscape(ConfiguredBaseModel):
    """
    Preliminary information about datasets intended to be shared through NAM Hub. Used by TDC teams to declare expected data uploads.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://namhub.synapse.org/portal_schemas',
         'slot_usage': {'contextOfUse': {'name': 'contextOfUse', 'required': True},
                        'dataContributionLead': {'name': 'dataContributionLead',
                                                 'required': True},
                        'datasetAssay': {'name': 'datasetAssay', 'required': True},
                        'datasetCategory': {'name': 'datasetCategory',
                                            'required': True},
                        'datasetDescription': {'name': 'datasetDescription',
                                               'required': True},
                        'datasetFileFormats': {'name': 'datasetFileFormats',
                                               'required': True},
                        'datasetName': {'name': 'datasetName', 'required': True},
                        'datasetSpecies': {'name': 'datasetSpecies', 'required': True},
                        'expectedDataVolume': {'name': 'expectedDataVolume',
                                               'required': False},
                        'expectedNumberOfFiles': {'name': 'expectedNumberOfFiles',
                                                  'required': True},
                        'expectedNumberOfSamples': {'name': 'expectedNumberOfSamples',
                                                    'required': True},
                        'landscapeId': {'name': 'landscapeId', 'required': True},
                        'studyAim': {'name': 'studyAim', 'required': True},
                        'studyName': {'name': 'studyName', 'required': True},
                        'uploadByDate': {'name': 'uploadByDate', 'required': True}}})

    landscapeId: str = Field(default=..., description="""Unique identifier for the landscape entry.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Landscape']} })
    datasetName: str = Field(default=..., description="""Name of the dataset.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Landscape']} })
    datasetDescription: str = Field(default=..., description="""A text description of the files contained in this dataset.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Landscape']} })
    datasetAssay: AssayEnum = Field(default=..., description="""Experimental method used to generate files in the dataset.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Landscape']} })
    datasetSpecies: SpeciesEnum = Field(default=..., description="""Species of origin associated with files in the dataset.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Landscape']} })
    datasetFileFormats: list[FileFormatEnum] = Field(default=..., description="""File extension(s) associated with files in the dataset.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Landscape']} })
    datasetCategory: DataCategoryEnum = Field(default=..., description="""Type of data or scientific content represented in the dataset (e.g. gene expression, imaging, clinical data) — see valid values for the full list.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Landscape']} })
    contextOfUse: list[str] = Field(default=..., description="""Free-text statement of the intended context(s) of use for this dataset — how and for what purpose the data is meant to be used, following the FDA Biomarker Qualification Program's Context of Use framework (https://www.fda.gov/drugs/biomarker-qualification-program/context-use). Multiple values permitted.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Landscape']} })
    applicableStandards: Optional[str] = Field(default=None, description="""Controlled vocabularies or data models used to organize and annotate files.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Landscape']} })
    expectedNumberOfFiles: int = Field(default=..., description="""Number of files expected to be uploaded as part of this dataset.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Landscape']} })
    expectedNumberOfSamples: int = Field(default=..., description="""Estimated total number of physical biospecimen samples represented in the dataset (e.g. 200 participants at 3 time points = 600 total samples). Distinct from expectedNumberOfFiles, which counts the files expected to be submitted.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Landscape']} })
    expectedDataVolume: Optional[str] = Field(default=None, description="""Approximate total storage the dataset is expected to occupy, as a band rather than a figure: one of \"under 1 GB\", \"GBs\", \"tens of GB\", \"hundreds of GB\", \"TBs\", \"tens of TB\", \"hundreds of TB\", \"PBs\", or \"unknown\". Pre-filled with an estimate for the contributing team to confirm or correct; a band is asked for because a precise size is not knowable before the data exists.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Landscape']} })
    uploadByDate: str = Field(default=..., description="""Non-binding estimated date by which files are expected to be uploaded.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Landscape']} })
    dataContributionLead: str = Field(default=..., description="""Name of the individual responsible for uploading files.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Landscape']} })
    studyName: str = Field(default=..., description="""Full display name of the study.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Landscape', 'Studies', 'Datasets']} })
    studyAim: str = Field(default=..., description="""Key connecting the expected data to aims in the research proposal.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Landscape']} })
    comments: Optional[str] = Field(default=None, description="""Additional information not captured in other fields.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Landscape']} })


class Studies(ConfiguredBaseModel):
    """
    One row per Technology Development Center (TDC) study in the NAMHub program. Synapse table: syn75404711.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://namhub.synapse.org/portal_schemas',
         'slot_usage': {'studyId': {'name': 'studyId', 'required': True},
                        'studyName': {'name': 'studyName', 'required': True}}})

    studyId: str = Field(default=..., description="""Study identifier linking to the Studies table (syn75404711).""", json_schema_extra = { "linkml_meta": {'domain_of': ['Studies', 'Datasets', 'People', 'NAMs', 'Publications']} })
    studyName: str = Field(default=..., description="""Full display name of the study.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Landscape', 'Studies', 'Datasets']} })
    studyLeads: Optional[list[str]] = Field(default=None, description="""Principal investigators or study leads.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Studies']} })
    summary: Optional[str] = Field(default=None, description="""Brief description of the study's goals and approach.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Studies']} })
    institution: Optional[list[str]] = Field(default=None, description="""Affiliated institution(s).""", json_schema_extra = { "linkml_meta": {'domain_of': ['Studies', 'People']} })
    fundingAgency: Optional[list[str]] = Field(default=None, description="""Funding agency or agencies (e.g. NIH Common Fund).""", json_schema_extra = { "linkml_meta": {'domain_of': ['Studies', 'Grants']} })
    synapseProjectId: Optional[str] = Field(default=None, description="""Synapse project entity ID housing the study's files.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Studies']} })
    studyDoi: Optional[str] = Field(default=None, description="""Digital Object Identifier (DOI) for the study.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Studies']} })
    diseaseFocus: Optional[list[str]] = Field(default=None, description="""Disease areas or conditions the study addresses.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Studies']} })
    alternateName: Optional[list[str]] = Field(default=None, description="""Acronym or short name for the study.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Studies']} })
    NAMsTechFocus: Optional[list[str]] = Field(default=None, description="""New Approach Methodology technology focus areas.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Studies']} })
    grantId: Optional[str] = Field(default=None, description="""Grant identifier linking to the Grants table (syn75404715).""", json_schema_extra = { "linkml_meta": {'domain_of': ['Studies', 'People', 'Grants', 'Publications']} })

    @field_validator('synapseProjectId')
    def pattern_synapseProjectId(cls, v):
        pattern=re.compile(r"^syn\d+$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid synapseProjectId format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid synapseProjectId format: {v}"
            raise ValueError(err_msg)
        return v


class Datasets(ConfiguredBaseModel):
    """
    One row per dataset — Synapse-hosted or external (e.g. GEO). Links to Studies and NAMs. Synapse table: syn75404713.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://namhub.synapse.org/portal_schemas',
         'slot_usage': {'title': {'name': 'title', 'required': True}}})

    datasetId: Optional[str] = Field(default=None, description="""Synapse Dataset entity ID. Blank for externally hosted datasets.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Datasets', 'NAMs']} })
    title: str = Field(default=..., description="""Display title of the dataset.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Datasets']} })
    description: Optional[str] = Field(default=None, description="""Free-text description.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Datasets', 'NAMs']} })
    studyId: Optional[str] = Field(default=None, description="""Study identifier linking to the Studies table (syn75404711).""", json_schema_extra = { "linkml_meta": {'domain_of': ['Studies', 'Datasets', 'People', 'NAMs', 'Publications']} })
    studyName: Optional[str] = Field(default=None, description="""Full display name of the study.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Landscape', 'Studies', 'Datasets']} })
    assay: Optional[list[AssayEnum]] = Field(default=None, description="""Experimental assay or method.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Datasets', 'Publications']} })
    dataType: Optional[list[DataCategoryEnum]] = Field(default=None, description="""Broad category of the data type.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Datasets', 'Publications']} })
    species: Optional[list[SpeciesEnum]] = Field(default=None, description="""Species of origin.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Datasets']} })
    format: Optional[list[FileFormatEnum]] = Field(default=None, description="""File formats contained in the dataset.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Datasets']} })
    repository: Optional[RepositoryEnum] = Field(default=None, description="""Repository where the dataset is hosted.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Datasets']} })
    externalLink: Optional[str] = Field(default=None, description="""External URL for additional resources.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Datasets', 'NAMs']} })
    doi: Optional[str] = Field(default=None, description="""Digital Object Identifier (DOI).""", json_schema_extra = { "linkml_meta": {'domain_of': ['Datasets', 'Publications']} })
    releaseDate: Optional[date] = Field(default=None, description="""Date the dataset was made publicly available.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Datasets']} })
    datasetItemCount: Optional[int] = Field(default=None, description="""Number of files or items in the dataset.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Datasets']} })
    datasetSizeInBytes: Optional[int] = Field(default=None, description="""Total size of the dataset in bytes.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Datasets']} })
    hasCroissantMetadata: Optional[bool] = Field(default=None, description="""Whether the dataset has associated Croissant-format metadata.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Datasets']} })
    croissantMetadataUrl: Optional[str] = Field(default=None, description="""URL to the Croissant metadata file for this dataset.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Datasets']} })
    accessType: Optional[AccessTypeEnum] = Field(default=None, description="""Data access level.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Datasets', 'NAMs']} })
    namId: Optional[list[str]] = Field(default=None, description="""NAM identifier(s) linking to the NAMs table (syn75404716).""", json_schema_extra = { "linkml_meta": {'domain_of': ['Datasets', 'NAMs', 'Publications']} })

    @field_validator('datasetId')
    def pattern_datasetId(cls, v):
        pattern=re.compile(r"^syn\d+$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid datasetId format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid datasetId format: {v}"
            raise ValueError(err_msg)
        return v


class People(ConfiguredBaseModel):
    """
    Investigators and contributors associated with NAMHub studies. Synapse table: syn75404714.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://namhub.synapse.org/portal_schemas',
         'slot_usage': {'firstName': {'name': 'firstName', 'required': True},
                        'lastName': {'name': 'lastName', 'required': True}}})

    investigatorId: Optional[str] = Field(default=None, description="""Unique identifier for the investigator.""", json_schema_extra = { "linkml_meta": {'domain_of': ['People']} })
    firstName: str = Field(default=..., description="""First name.""", json_schema_extra = { "linkml_meta": {'domain_of': ['People']} })
    lastName: str = Field(default=..., description="""Last name.""", json_schema_extra = { "linkml_meta": {'domain_of': ['People']} })
    institution: Optional[list[str]] = Field(default=None, description="""Affiliated institution(s).""", json_schema_extra = { "linkml_meta": {'domain_of': ['Studies', 'People']} })
    role: Optional[RoleEnum] = Field(default=None, description="""Role in the NAMHub program.""", json_schema_extra = { "linkml_meta": {'domain_of': ['People']} })
    studyId: Optional[str] = Field(default=None, description="""Study identifier linking to the Studies table (syn75404711).""", json_schema_extra = { "linkml_meta": {'domain_of': ['Studies', 'Datasets', 'People', 'NAMs', 'Publications']} })
    grantId: Optional[str] = Field(default=None, description="""Grant identifier linking to the Grants table (syn75404715).""", json_schema_extra = { "linkml_meta": {'domain_of': ['Studies', 'People', 'Grants', 'Publications']} })
    orcidId: Optional[str] = Field(default=None, description="""ORCID persistent digital identifier.""", json_schema_extra = { "linkml_meta": {'domain_of': ['People']} })
    synapseId: Optional[str] = Field(default=None, description="""Synapse user account ID.""", json_schema_extra = { "linkml_meta": {'domain_of': ['People']} })
    email: Optional[str] = Field(default=None, description="""Contact email address.""", json_schema_extra = { "linkml_meta": {'domain_of': ['People']} })
    portalDisplay: Optional[bool] = Field(default=True, description="""Whether this record should be displayed on the public portal.""", json_schema_extra = { "linkml_meta": {'domain_of': ['People', 'NAMs'], 'ifabsent': 'true'} })

    @field_validator('orcidId')
    def pattern_orcidId(cls, v):
        pattern=re.compile(r"^\d{4}-\d{4}-\d{4}-\d{3}[\dX]$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid orcidId format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid orcidId format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator('email')
    def pattern_email(cls, v):
        pattern=re.compile(r"^[^@]+@[^@]+\.[^@]+$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid email format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid email format: {v}"
            raise ValueError(err_msg)
        return v


class Grants(ConfiguredBaseModel):
    """
    Backend grant records linked to Studies. Not directly surfaced on the portal. Synapse table: syn75404715.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://namhub.synapse.org/portal_schemas',
         'slot_usage': {'grantId': {'name': 'grantId', 'required': True}}})

    grantId: str = Field(default=..., description="""Grant identifier linking to the Grants table (syn75404715).""", json_schema_extra = { "linkml_meta": {'domain_of': ['Studies', 'People', 'Grants', 'Publications']} })
    grantName: Optional[str] = Field(default=None, description="""Full title of the grant.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Grants']} })
    grantNumber: Optional[str] = Field(default=None, description="""NIH grant number (e.g. UM1TR006029).""", json_schema_extra = { "linkml_meta": {'domain_of': ['Grants']} })
    grantType: Optional[str] = Field(default=None, description="""Grant mechanism type (e.g. UM1, R01).""", json_schema_extra = { "linkml_meta": {'domain_of': ['Grants']} })
    grantInstitution: Optional[str] = Field(default=None, description="""Institution holding the grant.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Grants']} })
    abstract: Optional[str] = Field(default=None, description="""Grant abstract.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Grants']} })
    investigator: Optional[str] = Field(default=None, description="""Name of the principal investigator.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Grants']} })
    fundingAgency: Optional[list[str]] = Field(default=None, description="""Funding agency or agencies (e.g. NIH Common Fund).""", json_schema_extra = { "linkml_meta": {'domain_of': ['Studies', 'Grants']} })
    nihReporterLink: Optional[str] = Field(default=None, description="""URL to the grant record on NIH Reporter.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Grants']} })


class NAMs(ConfiguredBaseModel):
    """
    One row per New Approach Method (NAM). Modelled after NF/MC2 Tools tables. NAM type classification uses the New Approach Methods Ontology (NAMO) from the Monarch Initiative (https://github.com/monarch-initiative/namo). Governance fields follow Synapse/Sage portal conventions. Synapse table: syn75404716.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://namhub.synapse.org/portal_schemas',
         'see_also': ['https://github.com/monarch-initiative/namo'],
         'slot_usage': {'namId': {'name': 'namId', 'required': True},
                        'namName': {'name': 'namName', 'required': True}}})

    namId: list[str] = Field(default=..., description="""NAM identifier(s) linking to the NAMs table (syn75404716).""", json_schema_extra = { "linkml_meta": {'domain_of': ['Datasets', 'NAMs', 'Publications']} })
    namName: str = Field(default=..., description="""Display name of the NAM.""", json_schema_extra = { "linkml_meta": {'domain_of': ['NAMs']} })
    description: Optional[str] = Field(default=None, description="""Free-text description.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Datasets', 'NAMs']} })
    developmentStatus: Optional[DevelopmentStatusEnum] = Field(default=None, description="""Current development stage of the NAM.""", json_schema_extra = { "linkml_meta": {'domain_of': ['NAMs']} })
    namoClass: Optional[str] = Field(default=None, description="""Specific class name from the New Approach Methods Ontology (NAMO). Examples: Organoid, OrganOnChip, QSARModel, PBPKModel.""", json_schema_extra = { "linkml_meta": {'domain_of': ['NAMs'],
         'see_also': ['https://github.com/monarch-initiative/namo']} })
    namoCategory: Optional[str] = Field(default=None, description="""Top-level branch from the NAMO ontology. Examples: InVitroBiological, InSilico, InChemico.""", json_schema_extra = { "linkml_meta": {'domain_of': ['NAMs'],
         'see_also': ['https://github.com/monarch-initiative/namo']} })
    namoId: Optional[str] = Field(default=None, description="""NAMO ontology term identifier. Format: NAMO:XXXXXXX.""", json_schema_extra = { "linkml_meta": {'domain_of': ['NAMs'],
         'see_also': ['https://github.com/monarch-initiative/namo']} })
    organism: Optional[list[SpeciesEnum]] = Field(default=None, description="""Organism(s) the NAM is derived from or applicable to.""", json_schema_extra = { "linkml_meta": {'domain_of': ['NAMs']} })
    tissueOrCellType: Optional[list[str]] = Field(default=None, description="""Tissue or cell type(s) used in the NAM.""", json_schema_extra = { "linkml_meta": {'domain_of': ['NAMs']} })
    endpointsMeasured: Optional[list[str]] = Field(default=None, description="""Biological or chemical endpoints the NAM measures.""", json_schema_extra = { "linkml_meta": {'domain_of': ['NAMs']} })
    studyId: Optional[str] = Field(default=None, description="""Study identifier linking to the Studies table (syn75404711).""", json_schema_extra = { "linkml_meta": {'domain_of': ['Studies', 'Datasets', 'People', 'NAMs', 'Publications']} })
    datasetId: Optional[str] = Field(default=None, description="""Synapse Dataset entity ID. Blank for externally hosted datasets.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Datasets', 'NAMs']} })
    relatedPublications: Optional[list[str]] = Field(default=None, description="""PubMed IDs of publications describing or using this NAM.""", json_schema_extra = { "linkml_meta": {'domain_of': ['NAMs']} })
    externalLink: Optional[str] = Field(default=None, description="""External URL for additional resources.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Datasets', 'NAMs']} })
    synapseEntityId: Optional[str] = Field(default=None, description="""Synapse project or entity ID (syn-prefixed).""", json_schema_extra = { "linkml_meta": {'domain_of': ['NAMs', 'Publications']} })
    accessType: Optional[AccessTypeEnum] = Field(default=None, description="""Data access level.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Datasets', 'NAMs']} })
    accessRequirements: Optional[str] = Field(default=None, description="""Description of any Synapse Access Requirements governing the underlying data.""", json_schema_extra = { "linkml_meta": {'domain_of': ['NAMs']} })
    duoCode: Optional[list[str]] = Field(default=None, description="""Data Use Ontology (GA4GH DUO) codes restricting data reuse. Examples: GRU (General Research Use), HMB (Health/Medical/Biomedical), DS (Disease Specific).""", json_schema_extra = { "linkml_meta": {'domain_of': ['NAMs'], 'see_also': ['http://purl.obolibrary.org/obo/duo.owl']} })
    acknowledgementStatements: Optional[str] = Field(default=None, description="""Required attribution or acknowledgement text for data reuse.""", json_schema_extra = { "linkml_meta": {'domain_of': ['NAMs']} })
    license: Optional[str] = Field(default=None, description="""License governing reuse of the underlying data (e.g. CC-BY-4.0).""", json_schema_extra = { "linkml_meta": {'domain_of': ['NAMs']} })
    portalDisplay: Optional[bool] = Field(default=True, description="""Whether this record should be displayed on the public portal.""", json_schema_extra = { "linkml_meta": {'domain_of': ['People', 'NAMs'], 'ifabsent': 'true'} })

    @field_validator('namoId')
    def pattern_namoId(cls, v):
        pattern=re.compile(r"^NAMO:\d+$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid namoId format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid namoId format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator('datasetId')
    def pattern_datasetId(cls, v):
        pattern=re.compile(r"^syn\d+$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid datasetId format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid datasetId format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator('synapseEntityId')
    def pattern_synapseEntityId(cls, v):
        pattern=re.compile(r"^syn\d+$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid synapseEntityId format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid synapseEntityId format: {v}"
            raise ValueError(err_msg)
        return v


class Publications(ConfiguredBaseModel):
    """
    Publications associated with NAMHub studies, grants, or NAMs. Synapse table: syn75404744.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://namhub.synapse.org/portal_schemas',
         'slot_usage': {'publicationTitle': {'name': 'publicationTitle',
                                             'required': True}}})

    pubMedId: Optional[str] = Field(default=None, description="""PubMed identifier (PMID).""", json_schema_extra = { "linkml_meta": {'domain_of': ['Publications']} })
    publicationTitle: str = Field(default=..., description="""Full title of the publication.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Publications']} })
    authors: Optional[str] = Field(default=None, description="""Author list.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Publications']} })
    journal: Optional[str] = Field(default=None, description="""Journal name.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Publications']} })
    publicationYear: Optional[int] = Field(default=None, description="""Year of publication.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Publications']} })
    doi: Optional[str] = Field(default=None, description="""Digital Object Identifier (DOI).""", json_schema_extra = { "linkml_meta": {'domain_of': ['Datasets', 'Publications']} })
    pubMedLink: Optional[str] = Field(default=None, description="""URL to the PubMed entry.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Publications']} })
    keywords: Optional[list[str]] = Field(default=None, description="""Publication keywords or MeSH terms.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Publications']} })
    studyId: Optional[str] = Field(default=None, description="""Study identifier linking to the Studies table (syn75404711).""", json_schema_extra = { "linkml_meta": {'domain_of': ['Studies', 'Datasets', 'People', 'NAMs', 'Publications']} })
    grantId: Optional[str] = Field(default=None, description="""Grant identifier linking to the Grants table (syn75404715).""", json_schema_extra = { "linkml_meta": {'domain_of': ['Studies', 'People', 'Grants', 'Publications']} })
    namId: Optional[list[str]] = Field(default=None, description="""NAM identifier(s) linking to the NAMs table (syn75404716).""", json_schema_extra = { "linkml_meta": {'domain_of': ['Datasets', 'NAMs', 'Publications']} })
    dataType: Optional[list[DataCategoryEnum]] = Field(default=None, description="""Broad category of the data type.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Datasets', 'Publications']} })
    assay: Optional[list[AssayEnum]] = Field(default=None, description="""Experimental assay or method.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Datasets', 'Publications']} })
    synapseEntityId: Optional[str] = Field(default=None, description="""Synapse project or entity ID (syn-prefixed).""", json_schema_extra = { "linkml_meta": {'domain_of': ['NAMs', 'Publications']} })

    @field_validator('synapseEntityId')
    def pattern_synapseEntityId(cls, v):
        pattern=re.compile(r"^syn\d+$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid synapseEntityId format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid synapseEntityId format: {v}"
            raise ValueError(err_msg)
        return v


# Model rebuild
# see https://pydantic-docs.helpmanual.io/usage/models/#rebuilding-a-model
Landscape.model_rebuild()
Studies.model_rebuild()
Datasets.model_rebuild()
People.model_rebuild()
Grants.model_rebuild()
NAMs.model_rebuild()
Publications.model_rebuild()
