# Auto generated from namhub.yaml by pythongen.py version: 0.0.1
# Generation date: 2026-09-02T13:59:10
# Schema: namhub
#
# id: https://namhub.synapse.org/portal_schemas
# description: NAMHub portal data schemas — backend Synapse tables and the Landscape data collection form. Portal tables are backed by Synapse project syn74360399. NAM classification uses the New Approach Methods Ontology (NAMO) developed by the Monarch Initiative (https://github.com/monarch-initiative/namo).
# license: https://creativecommons.org/publicdomain/zero/1.0/

import dataclasses
import re
from dataclasses import dataclass
from datetime import (
    date,
    datetime,
    time
)
from typing import (
    Any,
    ClassVar,
    Dict,
    List,
    Optional,
    Union
)

from jsonasobj2 import (
    JsonObj,
    as_dict
)
from linkml_runtime.linkml_model.meta import (
    EnumDefinition,
    PermissibleValue,
    PvFormulaOptions
)
from linkml_runtime.utils.curienamespace import CurieNamespace
from linkml_runtime.utils.enumerations import EnumDefinitionImpl
from linkml_runtime.utils.formatutils import (
    camelcase,
    sfx,
    underscore
)
from linkml_runtime.utils.metamodelcore import (
    bnode,
    empty_dict,
    empty_list
)
from linkml_runtime.utils.slot import Slot
from linkml_runtime.utils.yamlutils import (
    YAMLRoot,
    extended_float,
    extended_int,
    extended_str
)
from rdflib import (
    Namespace,
    URIRef
)

from linkml_runtime.linkml_model.types import Boolean, Date, Integer, String, Uri
from linkml_runtime.utils.metamodelcore import Bool, URI, XSDDate

metamodel_version = "1.11.0"
version = None

# Namespaces
DUO = CurieNamespace('duo', 'http://purl.obolibrary.org/obo/DUO_')
LINKML = CurieNamespace('linkml', 'https://w3id.org/linkml/')
NAMHUB = CurieNamespace('namhub', 'https://namhub.synapse.org/portal_schemas/')
NAMO = CurieNamespace('namo', 'https://github.com/monarch-initiative/namo/')
SCHEMA = CurieNamespace('schema', 'http://schema.org/')
DEFAULT_ = NAMHUB


# Types

# Class references



@dataclass(repr=False)
class Landscape(YAMLRoot):
    """
    Preliminary information about datasets intended to be shared through NAM Hub. Used by TDC teams to declare
    expected data uploads.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = NAMHUB["Landscape"]
    class_class_curie: ClassVar[str] = "namhub:Landscape"
    class_name: ClassVar[str] = "Landscape"
    class_model_uri: ClassVar[URIRef] = NAMHUB.Landscape

    landscapeId: str = None
    datasetName: str = None
    datasetDescription: str = None
    datasetAssay: Union[str, "AssayEnum"] = None
    datasetSpecies: Union[str, "SpeciesEnum"] = None
    datasetFileFormats: Union[Union[str, "FileFormatEnum"], list[Union[str, "FileFormatEnum"]]] = None
    datasetCategory: Union[str, "DataCategoryEnum"] = None
    contextOfUse: Union[str, list[str]] = None
    expectedNumberOfFiles: int = None
    expectedNumberOfSamples: int = None
    uploadByDate: str = None
    dataContributionLead: str = None
    studyName: str = None
    studyAim: str = None
    applicableStandards: Optional[str] = None
    expectedDataVolume: Optional[str] = None
    comments: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.landscapeId):
            self.MissingRequiredField("landscapeId")
        if not isinstance(self.landscapeId, str):
            self.landscapeId = str(self.landscapeId)

        if self._is_empty(self.datasetName):
            self.MissingRequiredField("datasetName")
        if not isinstance(self.datasetName, str):
            self.datasetName = str(self.datasetName)

        if self._is_empty(self.datasetDescription):
            self.MissingRequiredField("datasetDescription")
        if not isinstance(self.datasetDescription, str):
            self.datasetDescription = str(self.datasetDescription)

        if self._is_empty(self.datasetAssay):
            self.MissingRequiredField("datasetAssay")
        if not isinstance(self.datasetAssay, AssayEnum):
            self.datasetAssay = AssayEnum(self.datasetAssay)

        if self._is_empty(self.datasetSpecies):
            self.MissingRequiredField("datasetSpecies")
        if not isinstance(self.datasetSpecies, SpeciesEnum):
            self.datasetSpecies = SpeciesEnum(self.datasetSpecies)

        if self._is_empty(self.datasetFileFormats):
            self.MissingRequiredField("datasetFileFormats")
        if not isinstance(self.datasetFileFormats, list):
            self.datasetFileFormats = [self.datasetFileFormats] if self.datasetFileFormats is not None else []
        self.datasetFileFormats = [v if isinstance(v, FileFormatEnum) else FileFormatEnum(v) for v in self.datasetFileFormats]

        if self._is_empty(self.datasetCategory):
            self.MissingRequiredField("datasetCategory")
        if not isinstance(self.datasetCategory, DataCategoryEnum):
            self.datasetCategory = DataCategoryEnum(self.datasetCategory)

        if self._is_empty(self.contextOfUse):
            self.MissingRequiredField("contextOfUse")
        if not isinstance(self.contextOfUse, list):
            self.contextOfUse = [self.contextOfUse] if self.contextOfUse is not None else []
        self.contextOfUse = [v if isinstance(v, str) else str(v) for v in self.contextOfUse]

        if self._is_empty(self.expectedNumberOfFiles):
            self.MissingRequiredField("expectedNumberOfFiles")
        if not isinstance(self.expectedNumberOfFiles, int):
            self.expectedNumberOfFiles = int(self.expectedNumberOfFiles)

        if self._is_empty(self.expectedNumberOfSamples):
            self.MissingRequiredField("expectedNumberOfSamples")
        if not isinstance(self.expectedNumberOfSamples, int):
            self.expectedNumberOfSamples = int(self.expectedNumberOfSamples)

        if self._is_empty(self.uploadByDate):
            self.MissingRequiredField("uploadByDate")
        if not isinstance(self.uploadByDate, str):
            self.uploadByDate = str(self.uploadByDate)

        if self._is_empty(self.dataContributionLead):
            self.MissingRequiredField("dataContributionLead")
        if not isinstance(self.dataContributionLead, str):
            self.dataContributionLead = str(self.dataContributionLead)

        if self._is_empty(self.studyName):
            self.MissingRequiredField("studyName")
        if not isinstance(self.studyName, str):
            self.studyName = str(self.studyName)

        if self._is_empty(self.studyAim):
            self.MissingRequiredField("studyAim")
        if not isinstance(self.studyAim, str):
            self.studyAim = str(self.studyAim)

        if self.applicableStandards is not None and not isinstance(self.applicableStandards, str):
            self.applicableStandards = str(self.applicableStandards)

        if self.expectedDataVolume is not None and not isinstance(self.expectedDataVolume, str):
            self.expectedDataVolume = str(self.expectedDataVolume)

        if self.comments is not None and not isinstance(self.comments, str):
            self.comments = str(self.comments)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Studies(YAMLRoot):
    """
    One row per Technology Development Center (TDC) study in the NAMHub program. Synapse table: syn75404711.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = NAMHUB["Studies"]
    class_class_curie: ClassVar[str] = "namhub:Studies"
    class_name: ClassVar[str] = "Studies"
    class_model_uri: ClassVar[URIRef] = NAMHUB.Studies

    studyId: str = None
    studyName: str = None
    studyLeads: Optional[Union[str, list[str]]] = empty_list()
    summary: Optional[str] = None
    institution: Optional[Union[str, list[str]]] = empty_list()
    fundingAgency: Optional[Union[str, list[str]]] = empty_list()
    synapseProjectId: Optional[str] = None
    studyDoi: Optional[Union[str, URI]] = None
    diseaseFocus: Optional[Union[str, list[str]]] = empty_list()
    alternateName: Optional[Union[str, list[str]]] = empty_list()
    NAMsTechFocus: Optional[Union[str, list[str]]] = empty_list()
    grantId: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.studyId):
            self.MissingRequiredField("studyId")
        if not isinstance(self.studyId, str):
            self.studyId = str(self.studyId)

        if self._is_empty(self.studyName):
            self.MissingRequiredField("studyName")
        if not isinstance(self.studyName, str):
            self.studyName = str(self.studyName)

        if not isinstance(self.studyLeads, list):
            self.studyLeads = [self.studyLeads] if self.studyLeads is not None else []
        self.studyLeads = [v if isinstance(v, str) else str(v) for v in self.studyLeads]

        if self.summary is not None and not isinstance(self.summary, str):
            self.summary = str(self.summary)

        if not isinstance(self.institution, list):
            self.institution = [self.institution] if self.institution is not None else []
        self.institution = [v if isinstance(v, str) else str(v) for v in self.institution]

        if not isinstance(self.fundingAgency, list):
            self.fundingAgency = [self.fundingAgency] if self.fundingAgency is not None else []
        self.fundingAgency = [v if isinstance(v, str) else str(v) for v in self.fundingAgency]

        if self.synapseProjectId is not None and not isinstance(self.synapseProjectId, str):
            self.synapseProjectId = str(self.synapseProjectId)

        if self.studyDoi is not None and not isinstance(self.studyDoi, URI):
            self.studyDoi = URI(self.studyDoi)

        if not isinstance(self.diseaseFocus, list):
            self.diseaseFocus = [self.diseaseFocus] if self.diseaseFocus is not None else []
        self.diseaseFocus = [v if isinstance(v, str) else str(v) for v in self.diseaseFocus]

        if not isinstance(self.alternateName, list):
            self.alternateName = [self.alternateName] if self.alternateName is not None else []
        self.alternateName = [v if isinstance(v, str) else str(v) for v in self.alternateName]

        if not isinstance(self.NAMsTechFocus, list):
            self.NAMsTechFocus = [self.NAMsTechFocus] if self.NAMsTechFocus is not None else []
        self.NAMsTechFocus = [v if isinstance(v, str) else str(v) for v in self.NAMsTechFocus]

        if self.grantId is not None and not isinstance(self.grantId, str):
            self.grantId = str(self.grantId)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Datasets(YAMLRoot):
    """
    One row per dataset — Synapse-hosted or external (e.g. GEO). Links to Studies and NAMs. Synapse table: syn75404713.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = NAMHUB["Datasets"]
    class_class_curie: ClassVar[str] = "namhub:Datasets"
    class_name: ClassVar[str] = "Datasets"
    class_model_uri: ClassVar[URIRef] = NAMHUB.Datasets

    title: str = None
    datasetId: Optional[str] = None
    description: Optional[str] = None
    studyId: Optional[str] = None
    studyName: Optional[str] = None
    assay: Optional[Union[Union[str, "AssayEnum"], list[Union[str, "AssayEnum"]]]] = empty_list()
    dataType: Optional[Union[Union[str, "DataCategoryEnum"], list[Union[str, "DataCategoryEnum"]]]] = empty_list()
    species: Optional[Union[Union[str, "SpeciesEnum"], list[Union[str, "SpeciesEnum"]]]] = empty_list()
    format: Optional[Union[Union[str, "FileFormatEnum"], list[Union[str, "FileFormatEnum"]]]] = empty_list()
    repository: Optional[Union[str, "RepositoryEnum"]] = None
    externalLink: Optional[Union[str, URI]] = None
    doi: Optional[Union[str, URI]] = None
    releaseDate: Optional[Union[str, XSDDate]] = None
    datasetItemCount: Optional[int] = None
    datasetSizeInBytes: Optional[int] = None
    hasCroissantMetadata: Optional[Union[bool, Bool]] = None
    croissantMetadataUrl: Optional[Union[str, URI]] = None
    accessType: Optional[Union[str, "AccessTypeEnum"]] = None
    namId: Optional[Union[str, list[str]]] = empty_list()

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.title):
            self.MissingRequiredField("title")
        if not isinstance(self.title, str):
            self.title = str(self.title)

        if self.datasetId is not None and not isinstance(self.datasetId, str):
            self.datasetId = str(self.datasetId)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        if self.studyId is not None and not isinstance(self.studyId, str):
            self.studyId = str(self.studyId)

        if self.studyName is not None and not isinstance(self.studyName, str):
            self.studyName = str(self.studyName)

        if not isinstance(self.assay, list):
            self.assay = [self.assay] if self.assay is not None else []
        self.assay = [v if isinstance(v, AssayEnum) else AssayEnum(v) for v in self.assay]

        if not isinstance(self.dataType, list):
            self.dataType = [self.dataType] if self.dataType is not None else []
        self.dataType = [v if isinstance(v, DataCategoryEnum) else DataCategoryEnum(v) for v in self.dataType]

        if not isinstance(self.species, list):
            self.species = [self.species] if self.species is not None else []
        self.species = [v if isinstance(v, SpeciesEnum) else SpeciesEnum(v) for v in self.species]

        if not isinstance(self.format, list):
            self.format = [self.format] if self.format is not None else []
        self.format = [v if isinstance(v, FileFormatEnum) else FileFormatEnum(v) for v in self.format]

        if self.repository is not None and not isinstance(self.repository, RepositoryEnum):
            self.repository = RepositoryEnum(self.repository)

        if self.externalLink is not None and not isinstance(self.externalLink, URI):
            self.externalLink = URI(self.externalLink)

        if self.doi is not None and not isinstance(self.doi, URI):
            self.doi = URI(self.doi)

        if self.releaseDate is not None and not isinstance(self.releaseDate, XSDDate):
            self.releaseDate = XSDDate(self.releaseDate)

        if self.datasetItemCount is not None and not isinstance(self.datasetItemCount, int):
            self.datasetItemCount = int(self.datasetItemCount)

        if self.datasetSizeInBytes is not None and not isinstance(self.datasetSizeInBytes, int):
            self.datasetSizeInBytes = int(self.datasetSizeInBytes)

        if self.hasCroissantMetadata is not None and not isinstance(self.hasCroissantMetadata, Bool):
            self.hasCroissantMetadata = Bool(self.hasCroissantMetadata)

        if self.croissantMetadataUrl is not None and not isinstance(self.croissantMetadataUrl, URI):
            self.croissantMetadataUrl = URI(self.croissantMetadataUrl)

        if self.accessType is not None and not isinstance(self.accessType, AccessTypeEnum):
            self.accessType = AccessTypeEnum(self.accessType)

        if not isinstance(self.namId, list):
            self.namId = [self.namId] if self.namId is not None else []
        self.namId = [v if isinstance(v, str) else str(v) for v in self.namId]

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class People(YAMLRoot):
    """
    Investigators and contributors associated with NAMHub studies. Synapse table: syn75404714.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = NAMHUB["People"]
    class_class_curie: ClassVar[str] = "namhub:People"
    class_name: ClassVar[str] = "People"
    class_model_uri: ClassVar[URIRef] = NAMHUB.People

    firstName: str = None
    lastName: str = None
    investigatorId: Optional[str] = None
    institution: Optional[Union[str, list[str]]] = empty_list()
    role: Optional[Union[str, "RoleEnum"]] = None
    studyId: Optional[str] = None
    grantId: Optional[str] = None
    orcidId: Optional[str] = None
    synapseId: Optional[str] = None
    email: Optional[str] = None
    portalDisplay: Optional[Union[bool, Bool]] = True

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.firstName):
            self.MissingRequiredField("firstName")
        if not isinstance(self.firstName, str):
            self.firstName = str(self.firstName)

        if self._is_empty(self.lastName):
            self.MissingRequiredField("lastName")
        if not isinstance(self.lastName, str):
            self.lastName = str(self.lastName)

        if self.investigatorId is not None and not isinstance(self.investigatorId, str):
            self.investigatorId = str(self.investigatorId)

        if not isinstance(self.institution, list):
            self.institution = [self.institution] if self.institution is not None else []
        self.institution = [v if isinstance(v, str) else str(v) for v in self.institution]

        if self.role is not None and not isinstance(self.role, RoleEnum):
            self.role = RoleEnum(self.role)

        if self.studyId is not None and not isinstance(self.studyId, str):
            self.studyId = str(self.studyId)

        if self.grantId is not None and not isinstance(self.grantId, str):
            self.grantId = str(self.grantId)

        if self.orcidId is not None and not isinstance(self.orcidId, str):
            self.orcidId = str(self.orcidId)

        if self.synapseId is not None and not isinstance(self.synapseId, str):
            self.synapseId = str(self.synapseId)

        if self.email is not None and not isinstance(self.email, str):
            self.email = str(self.email)

        if self.portalDisplay is not None and not isinstance(self.portalDisplay, Bool):
            self.portalDisplay = Bool(self.portalDisplay)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Grants(YAMLRoot):
    """
    Backend grant records linked to Studies. Not directly surfaced on the portal. Synapse table: syn75404715.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = NAMHUB["Grants"]
    class_class_curie: ClassVar[str] = "namhub:Grants"
    class_name: ClassVar[str] = "Grants"
    class_model_uri: ClassVar[URIRef] = NAMHUB.Grants

    grantId: str = None
    grantName: Optional[str] = None
    grantNumber: Optional[str] = None
    grantType: Optional[str] = None
    grantInstitution: Optional[str] = None
    abstract: Optional[str] = None
    investigator: Optional[str] = None
    fundingAgency: Optional[Union[str, list[str]]] = empty_list()
    nihReporterLink: Optional[Union[str, URI]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.grantId):
            self.MissingRequiredField("grantId")
        if not isinstance(self.grantId, str):
            self.grantId = str(self.grantId)

        if self.grantName is not None and not isinstance(self.grantName, str):
            self.grantName = str(self.grantName)

        if self.grantNumber is not None and not isinstance(self.grantNumber, str):
            self.grantNumber = str(self.grantNumber)

        if self.grantType is not None and not isinstance(self.grantType, str):
            self.grantType = str(self.grantType)

        if self.grantInstitution is not None and not isinstance(self.grantInstitution, str):
            self.grantInstitution = str(self.grantInstitution)

        if self.abstract is not None and not isinstance(self.abstract, str):
            self.abstract = str(self.abstract)

        if self.investigator is not None and not isinstance(self.investigator, str):
            self.investigator = str(self.investigator)

        if not isinstance(self.fundingAgency, list):
            self.fundingAgency = [self.fundingAgency] if self.fundingAgency is not None else []
        self.fundingAgency = [v if isinstance(v, str) else str(v) for v in self.fundingAgency]

        if self.nihReporterLink is not None and not isinstance(self.nihReporterLink, URI):
            self.nihReporterLink = URI(self.nihReporterLink)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class NAMs(YAMLRoot):
    """
    One row per New Approach Method (NAM). Modelled after NF/MC2 Tools tables. NAM type classification uses the New
    Approach Methods Ontology (NAMO) from the Monarch Initiative (https://github.com/monarch-initiative/namo).
    Governance fields follow Synapse/Sage portal conventions. Synapse table: syn75404716.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = NAMHUB["NAMs"]
    class_class_curie: ClassVar[str] = "namhub:NAMs"
    class_name: ClassVar[str] = "NAMs"
    class_model_uri: ClassVar[URIRef] = NAMHUB.NAMs

    namId: Union[str, list[str]] = None
    namName: str = None
    description: Optional[str] = None
    developmentStatus: Optional[Union[str, "DevelopmentStatusEnum"]] = None
    namoClass: Optional[str] = None
    namoCategory: Optional[str] = None
    namoId: Optional[str] = None
    organism: Optional[Union[Union[str, "SpeciesEnum"], list[Union[str, "SpeciesEnum"]]]] = empty_list()
    tissueOrCellType: Optional[Union[str, list[str]]] = empty_list()
    endpointsMeasured: Optional[Union[str, list[str]]] = empty_list()
    studyId: Optional[str] = None
    datasetId: Optional[str] = None
    relatedPublications: Optional[Union[str, list[str]]] = empty_list()
    externalLink: Optional[Union[str, URI]] = None
    synapseEntityId: Optional[str] = None
    accessType: Optional[Union[str, "AccessTypeEnum"]] = None
    accessRequirements: Optional[str] = None
    duoCode: Optional[Union[str, list[str]]] = empty_list()
    acknowledgementStatements: Optional[str] = None
    license: Optional[str] = None
    portalDisplay: Optional[Union[bool, Bool]] = True

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.namId):
            self.MissingRequiredField("namId")
        if not isinstance(self.namId, list):
            self.namId = [self.namId] if self.namId is not None else []
        self.namId = [v if isinstance(v, str) else str(v) for v in self.namId]

        if self._is_empty(self.namName):
            self.MissingRequiredField("namName")
        if not isinstance(self.namName, str):
            self.namName = str(self.namName)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        if self.developmentStatus is not None and not isinstance(self.developmentStatus, DevelopmentStatusEnum):
            self.developmentStatus = DevelopmentStatusEnum(self.developmentStatus)

        if self.namoClass is not None and not isinstance(self.namoClass, str):
            self.namoClass = str(self.namoClass)

        if self.namoCategory is not None and not isinstance(self.namoCategory, str):
            self.namoCategory = str(self.namoCategory)

        if self.namoId is not None and not isinstance(self.namoId, str):
            self.namoId = str(self.namoId)

        if not isinstance(self.organism, list):
            self.organism = [self.organism] if self.organism is not None else []
        self.organism = [v if isinstance(v, SpeciesEnum) else SpeciesEnum(v) for v in self.organism]

        if not isinstance(self.tissueOrCellType, list):
            self.tissueOrCellType = [self.tissueOrCellType] if self.tissueOrCellType is not None else []
        self.tissueOrCellType = [v if isinstance(v, str) else str(v) for v in self.tissueOrCellType]

        if not isinstance(self.endpointsMeasured, list):
            self.endpointsMeasured = [self.endpointsMeasured] if self.endpointsMeasured is not None else []
        self.endpointsMeasured = [v if isinstance(v, str) else str(v) for v in self.endpointsMeasured]

        if self.studyId is not None and not isinstance(self.studyId, str):
            self.studyId = str(self.studyId)

        if self.datasetId is not None and not isinstance(self.datasetId, str):
            self.datasetId = str(self.datasetId)

        if not isinstance(self.relatedPublications, list):
            self.relatedPublications = [self.relatedPublications] if self.relatedPublications is not None else []
        self.relatedPublications = [v if isinstance(v, str) else str(v) for v in self.relatedPublications]

        if self.externalLink is not None and not isinstance(self.externalLink, URI):
            self.externalLink = URI(self.externalLink)

        if self.synapseEntityId is not None and not isinstance(self.synapseEntityId, str):
            self.synapseEntityId = str(self.synapseEntityId)

        if self.accessType is not None and not isinstance(self.accessType, AccessTypeEnum):
            self.accessType = AccessTypeEnum(self.accessType)

        if self.accessRequirements is not None and not isinstance(self.accessRequirements, str):
            self.accessRequirements = str(self.accessRequirements)

        if not isinstance(self.duoCode, list):
            self.duoCode = [self.duoCode] if self.duoCode is not None else []
        self.duoCode = [v if isinstance(v, str) else str(v) for v in self.duoCode]

        if self.acknowledgementStatements is not None and not isinstance(self.acknowledgementStatements, str):
            self.acknowledgementStatements = str(self.acknowledgementStatements)

        if self.license is not None and not isinstance(self.license, str):
            self.license = str(self.license)

        if self.portalDisplay is not None and not isinstance(self.portalDisplay, Bool):
            self.portalDisplay = Bool(self.portalDisplay)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Publications(YAMLRoot):
    """
    Publications associated with NAMHub studies, grants, or NAMs. Synapse table: syn75404744.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = NAMHUB["Publications"]
    class_class_curie: ClassVar[str] = "namhub:Publications"
    class_name: ClassVar[str] = "Publications"
    class_model_uri: ClassVar[URIRef] = NAMHUB.Publications

    publicationTitle: str = None
    pubMedId: Optional[str] = None
    authors: Optional[str] = None
    journal: Optional[str] = None
    publicationYear: Optional[int] = None
    doi: Optional[Union[str, URI]] = None
    pubMedLink: Optional[Union[str, URI]] = None
    keywords: Optional[Union[str, list[str]]] = empty_list()
    studyId: Optional[str] = None
    grantId: Optional[str] = None
    namId: Optional[Union[str, list[str]]] = empty_list()
    dataType: Optional[Union[Union[str, "DataCategoryEnum"], list[Union[str, "DataCategoryEnum"]]]] = empty_list()
    assay: Optional[Union[Union[str, "AssayEnum"], list[Union[str, "AssayEnum"]]]] = empty_list()
    synapseEntityId: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.publicationTitle):
            self.MissingRequiredField("publicationTitle")
        if not isinstance(self.publicationTitle, str):
            self.publicationTitle = str(self.publicationTitle)

        if self.pubMedId is not None and not isinstance(self.pubMedId, str):
            self.pubMedId = str(self.pubMedId)

        if self.authors is not None and not isinstance(self.authors, str):
            self.authors = str(self.authors)

        if self.journal is not None and not isinstance(self.journal, str):
            self.journal = str(self.journal)

        if self.publicationYear is not None and not isinstance(self.publicationYear, int):
            self.publicationYear = int(self.publicationYear)

        if self.doi is not None and not isinstance(self.doi, URI):
            self.doi = URI(self.doi)

        if self.pubMedLink is not None and not isinstance(self.pubMedLink, URI):
            self.pubMedLink = URI(self.pubMedLink)

        if not isinstance(self.keywords, list):
            self.keywords = [self.keywords] if self.keywords is not None else []
        self.keywords = [v if isinstance(v, str) else str(v) for v in self.keywords]

        if self.studyId is not None and not isinstance(self.studyId, str):
            self.studyId = str(self.studyId)

        if self.grantId is not None and not isinstance(self.grantId, str):
            self.grantId = str(self.grantId)

        if not isinstance(self.namId, list):
            self.namId = [self.namId] if self.namId is not None else []
        self.namId = [v if isinstance(v, str) else str(v) for v in self.namId]

        if not isinstance(self.dataType, list):
            self.dataType = [self.dataType] if self.dataType is not None else []
        self.dataType = [v if isinstance(v, DataCategoryEnum) else DataCategoryEnum(v) for v in self.dataType]

        if not isinstance(self.assay, list):
            self.assay = [self.assay] if self.assay is not None else []
        self.assay = [v if isinstance(v, AssayEnum) else AssayEnum(v) for v in self.assay]

        if self.synapseEntityId is not None and not isinstance(self.synapseEntityId, str):
            self.synapseEntityId = str(self.synapseEntityId)

        super().__post_init__(**kwargs)


# Enumerations
class AssayEnum(EnumDefinitionImpl):
    """
    Experimental method used to generate files in the dataset.
    """
    SaferSeqS = PermissibleValue(text="SaferSeqS")
    CODEX = PermissibleValue(text="CODEX")
    SUSHI = PermissibleValue(text="SUSHI")
    autoradiography = PermissibleValue(text="autoradiography")
    histology = PermissibleValue(text="histology")
    immunocytochemistry = PermissibleValue(text="immunocytochemistry")
    immunofluorescence = PermissibleValue(text="immunofluorescence")
    immunohistochemistry = PermissibleValue(text="immunohistochemistry")
    photograph = PermissibleValue(text="photograph")
    MudPIT = PermissibleValue(text="MudPIT")
    RPPA = PermissibleValue(text="RPPA")
    SomaScan = PermissibleValue(text="SomaScan")
    Interview = PermissibleValue(text="Interview")
    actigraphy = PermissibleValue(text="actigraphy")
    genotyping = PermissibleValue(text="genotyping")
    polysomnography = PermissibleValue(text="polysomnography")
    questionnaire = PermissibleValue(text="questionnaire")
    scale = PermissibleValue(text="scale")
    weight = PermissibleValue(text="weight")
    survival = PermissibleValue(text="survival")
    ELISA = PermissibleValue(text="ELISA")
    HPLC = PermissibleValue(text="HPLC")
    TIDE = PermissibleValue(text="TIDE")
    array = PermissibleValue(text="array")
    electrochemiluminescence = PermissibleValue(text="electrochemiluminescence")
    immunoassay = PermissibleValue(text="immunoassay")
    microrheology = PermissibleValue(text="microrheology")
    rheometry = PermissibleValue(text="rheometry")
    Unknown = PermissibleValue(text="Unknown")

    _defn = EnumDefinition(
        name="AssayEnum",
        description="Experimental method used to generate files in the dataset.",
    )

    @classmethod
    def _addvals(cls):
        setattr(cls, "ATAC-seq",
            PermissibleValue(text="ATAC-seq"))
        setattr(cls, "CAPP-seq",
            PermissibleValue(text="CAPP-seq"))
        setattr(cls, "CUT&RUN",
            PermissibleValue(text="CUT&RUN"))
        setattr(cls, "ChIP-seq",
            PermissibleValue(text="ChIP-seq"))
        setattr(cls, "ERR bisulfite sequencing",
            PermissibleValue(text="ERR bisulfite sequencing"))
        setattr(cls, "HI-C",
            PermissibleValue(text="HI-C"))
        setattr(cls, "ISO-seq",
            PermissibleValue(text="ISO-seq"))
        setattr(cls, "NOMe-seq",
            PermissibleValue(text="NOMe-seq"))
        setattr(cls, "RNA array",
            PermissibleValue(text="RNA array"))
        setattr(cls, "RNA-seq",
            PermissibleValue(text="RNA-seq"))
        setattr(cls, "SNP array",
            PermissibleValue(text="SNP array"))
        setattr(cls, "Sanger sequencing",
            PermissibleValue(text="Sanger sequencing"))
        setattr(cls, "T cell receptor repertoire sequencing",
            PermissibleValue(text="T cell receptor repertoire sequencing"))
        setattr(cls, "bisulfite sequencing",
            PermissibleValue(text="bisulfite sequencing"))
        setattr(cls, "jumping library",
            PermissibleValue(text="jumping library"))
        setattr(cls, "lncRNA-seq",
            PermissibleValue(text="lncRNA-seq"))
        setattr(cls, "methylation array",
            PermissibleValue(text="methylation array"))
        setattr(cls, "miRNA array",
            PermissibleValue(text="miRNA array"))
        setattr(cls, "miRNA-seq",
            PermissibleValue(text="miRNA-seq"))
        setattr(cls, "next-generation sequencing",
            PermissibleValue(text="next-generation sequencing"))
        setattr(cls, "next generation targeted sequencing",
            PermissibleValue(text="next generation targeted sequencing"))
        setattr(cls, "oxBS-seq",
            PermissibleValue(text="oxBS-seq"))
        setattr(cls, "ribo-seq",
            PermissibleValue(text="ribo-seq"))
        setattr(cls, "scCGI-seq",
            PermissibleValue(text="scCGI-seq"))
        setattr(cls, "single cell ATAC-seq",
            PermissibleValue(text="single cell ATAC-seq"))
        setattr(cls, "single-cell RNA-seq",
            PermissibleValue(text="single-cell RNA-seq"))
        setattr(cls, "single-nucleus RNA-seq",
            PermissibleValue(text="single-nucleus RNA-seq"))
        setattr(cls, "spatial transcriptomics",
            PermissibleValue(text="spatial transcriptomics"))
        setattr(cls, "targeted exome sequencing",
            PermissibleValue(text="targeted exome sequencing"))
        setattr(cls, "whole exome sequencing",
            PermissibleValue(text="whole exome sequencing"))
        setattr(cls, "whole genome sequencing",
            PermissibleValue(text="whole genome sequencing"))
        setattr(cls, "3D confocal imaging",
            PermissibleValue(text="3D confocal imaging"))
        setattr(cls, "3D electron microscopy",
            PermissibleValue(text="3D electron microscopy"))
        setattr(cls, "3D imaging",
            PermissibleValue(text="3D imaging"))
        setattr(cls, "DNA optical mapping",
            PermissibleValue(text="DNA optical mapping"))
        setattr(cls, "Fluorescence In Situ Hybridization",
            PermissibleValue(text="Fluorescence In Situ Hybridization"))
        setattr(cls, "Magnetization-Prepared Rapid Gradient Echo MRI",
            PermissibleValue(text="Magnetization-Prepared Rapid Gradient Echo MRI"))
        setattr(cls, "atomic force microscopy",
            PermissibleValue(text="atomic force microscopy"))
        setattr(cls, "brightfield microscopy",
            PermissibleValue(text="brightfield microscopy"))
        setattr(cls, "live imaging",
            PermissibleValue(text="live imaging"))
        setattr(cls, "confocal microscopy",
            PermissibleValue(text="confocal microscopy"))
        setattr(cls, "conventional MRI",
            PermissibleValue(text="conventional MRI"))
        setattr(cls, "diffusion MRI",
            PermissibleValue(text="diffusion MRI"))
        setattr(cls, "fluorescence microscopy assay",
            PermissibleValue(text="fluorescence microscopy assay"))
        setattr(cls, "functional MRI",
            PermissibleValue(text="functional MRI"))
        setattr(cls, "gel filtration chromatography",
            PermissibleValue(text="gel filtration chromatography"))
        setattr(cls, "high content screen",
            PermissibleValue(text="high content screen"))
        setattr(cls, "high frequency ultrasound",
            PermissibleValue(text="high frequency ultrasound"))
        setattr(cls, "in vivo bioluminescence",
            PermissibleValue(text="in vivo bioluminescence"))
        setattr(cls, "laser speckle imaging",
            PermissibleValue(text="laser speckle imaging"))
        setattr(cls, "magnetic resonance angiography",
            PermissibleValue(text="magnetic resonance angiography"))
        setattr(cls, "magnetic resonance spectroscopy",
            PermissibleValue(text="magnetic resonance spectroscopy"))
        setattr(cls, "optical coherence tomography",
            PermissibleValue(text="optical coherence tomography"))
        setattr(cls, "optical tomography",
            PermissibleValue(text="optical tomography"))
        setattr(cls, "phase-contrast microscopy",
            PermissibleValue(text="phase-contrast microscopy"))
        setattr(cls, "positron emission tomography",
            PermissibleValue(text="positron emission tomography"))
        setattr(cls, "spatial frequency domain imaging",
            PermissibleValue(text="spatial frequency domain imaging"))
        setattr(cls, "traction force microscopy",
            PermissibleValue(text="traction force microscopy"))
        setattr(cls, "transcranial doppler ultrasonography",
            PermissibleValue(text="transcranial doppler ultrasonography"))
        setattr(cls, "western blot",
            PermissibleValue(text="western blot"))
        setattr(cls, "FIA-MSMS",
            PermissibleValue(text="FIA-MSMS"))
        setattr(cls, "FTIR spectroscopy",
            PermissibleValue(text="FTIR spectroscopy"))
        setattr(cls, "MIB/MS",
            PermissibleValue(text="MIB/MS"))
        setattr(cls, "TMT quantitation",
            PermissibleValue(text="TMT quantitation"))
        setattr(cls, "high-performance liquid chromatography/tandem mass spectrometry",
            PermissibleValue(text="high-performance liquid chromatography/tandem mass spectrometry"))
        setattr(cls, "label free mass spectrometry",
            PermissibleValue(text="label free mass spectrometry"))
        setattr(cls, "liquid chromatography-electrochemical detection",
            PermissibleValue(text="liquid chromatography-electrochemical detection"))
        setattr(cls, "liquid chromatography/mass spectrometry",
            PermissibleValue(text="liquid chromatography/mass spectrometry"))
        setattr(cls, "liquid chromatography/tandem mass spectrometry",
            PermissibleValue(text="liquid chromatography/tandem mass spectrometry"))
        setattr(cls, "mass spectrometry",
            PermissibleValue(text="mass spectrometry"))
        setattr(cls, "proximity extension assay",
            PermissibleValue(text="proximity extension assay"))
        setattr(cls, "ultra high-performance liquid chromatography/tandem mass spectrometry",
            PermissibleValue(text="ultra high-performance liquid chromatography/tandem mass spectrometry"))
        setattr(cls, "AlgometRx Nociometer",
            PermissibleValue(text="AlgometRx Nociometer"))
        setattr(cls, "quantitative sensory testing",
            PermissibleValue(text="quantitative sensory testing"))
        setattr(cls, "Child Behavior Checklist for Ages 1.5-5",
            PermissibleValue(text="Child Behavior Checklist for Ages 1.5-5"))
        setattr(cls, "Child Behavior Checklist for Ages 6-18",
            PermissibleValue(text="Child Behavior Checklist for Ages 6-18"))
        setattr(cls, "Children's Dermatology Life Quality Index Questionnaire",
            PermissibleValue(text="Children's Dermatology Life Quality Index Questionnaire"))
        setattr(cls, "Corsi blocks",
            PermissibleValue(text="Corsi blocks"))
        setattr(cls, "FACE-Q Appearance-related Distress",
            PermissibleValue(text="FACE-Q Appearance-related Distress"))
        setattr(cls, "Focus group",
            PermissibleValue(text="Focus group"))
        setattr(cls, "NIH Toolbox",
            PermissibleValue(text="NIH Toolbox"))
        setattr(cls, "PROMIS Cognitive Function",
            PermissibleValue(text="PROMIS Cognitive Function"))
        setattr(cls, "Riccardi and Ablon scales",
            PermissibleValue(text="Riccardi and Ablon scales"))
        setattr(cls, "Skindex-16",
            PermissibleValue(text="Skindex-16"))
        setattr(cls, "Social Responsiveness Scale",
            PermissibleValue(text="Social Responsiveness Scale"))
        setattr(cls, "Social Responsiveness Scale Second Edition",
            PermissibleValue(text="Social Responsiveness Scale Second Edition"))
        setattr(cls, "Von Frey test",
            PermissibleValue(text="Von Frey test"))
        setattr(cls, "active avoidance learning behavior assay",
            PermissibleValue(text="active avoidance learning behavior assay"))
        setattr(cls, "auditory brainstem response",
            PermissibleValue(text="auditory brainstem response"))
        setattr(cls, "blood chemistry measurement",
            PermissibleValue(text="blood chemistry measurement"))
        setattr(cls, "body size trait measurement",
            PermissibleValue(text="body size trait measurement"))
        setattr(cls, "cNF-Skindex",
            PermissibleValue(text="cNF-Skindex"))
        setattr(cls, "clinical data",
            PermissibleValue(text="clinical data"))
        setattr(cls, "cognitive assessment",
            PermissibleValue(text="cognitive assessment"))
        setattr(cls, "contextual conditioning behavior assay",
            PermissibleValue(text="contextual conditioning behavior assay"))
        setattr(cls, "distortion product otoacoustic emissions",
            PermissibleValue(text="distortion product otoacoustic emissions"))
        setattr(cls, "elevated plus maze test",
            PermissibleValue(text="elevated plus maze test"))
        setattr(cls, "feeding assay",
            PermissibleValue(text="feeding assay"))
        setattr(cls, "gait measurement",
            PermissibleValue(text="gait measurement"))
        setattr(cls, "grip strength",
            PermissibleValue(text="grip strength"))
        setattr(cls, "hand-held dynamometry",
            PermissibleValue(text="hand-held dynamometry"))
        setattr(cls, "metabolic screening",
            PermissibleValue(text="metabolic screening"))
        setattr(cls, "n-back task",
            PermissibleValue(text="n-back task"))
        setattr(cls, "neuropsychological assessment",
            PermissibleValue(text="neuropsychological assessment"))
        setattr(cls, "novelty response behavior assay",
            PermissibleValue(text="novelty response behavior assay"))
        setattr(cls, "open field test",
            PermissibleValue(text="open field test"))
        setattr(cls, "optokinetic reflex assay",
            PermissibleValue(text="optokinetic reflex assay"))
        setattr(cls, "pattern electroretinogram",
            PermissibleValue(text="pattern electroretinogram"))
        setattr(cls, "pure tone average",
            PermissibleValue(text="pure tone average"))
        setattr(cls, "rotarod performance test",
            PermissibleValue(text="rotarod performance test"))
        setattr(cls, "six-minute walk test",
            PermissibleValue(text="six-minute walk test"))
        setattr(cls, "word recognition score",
            PermissibleValue(text="word recognition score"))
        setattr(cls, "2D AlamarBlue absorbance",
            PermissibleValue(text="2D AlamarBlue absorbance"))
        setattr(cls, "2D AlamarBlue fluorescence",
            PermissibleValue(text="2D AlamarBlue fluorescence"))
        setattr(cls, "3D microtissue viability",
            PermissibleValue(text="3D microtissue viability"))
        setattr(cls, "ATPase activity assay",
            PermissibleValue(text="ATPase activity assay"))
        setattr(cls, "BrdU proliferation assay",
            PermissibleValue(text="BrdU proliferation assay"))
        setattr(cls, "EdU proliferation assay",
            PermissibleValue(text="EdU proliferation assay"))
        setattr(cls, "FLIPR high-throughput cellular screening",
            PermissibleValue(text="FLIPR high-throughput cellular screening"))
        setattr(cls, "Migration Assay",
            PermissibleValue(text="Migration Assay"))
        setattr(cls, "STR profile",
            PermissibleValue(text="STR profile"))
        setattr(cls, "TriKinetics activity monitoring",
            PermissibleValue(text="TriKinetics activity monitoring"))
        setattr(cls, "blue native PAGE",
            PermissibleValue(text="blue native PAGE"))
        setattr(cls, "SDS-PAGE",
            PermissibleValue(text="SDS-PAGE"))
        setattr(cls, "bone histomorphometry",
            PermissibleValue(text="bone histomorphometry"))
        setattr(cls, "cAMP-Glo Max Assay",
            PermissibleValue(text="cAMP-Glo Max Assay"))
        setattr(cls, "calcium retention capacity assay",
            PermissibleValue(text="calcium retention capacity assay"))
        setattr(cls, "cell competition",
            PermissibleValue(text="cell competition"))
        setattr(cls, "cell count",
            PermissibleValue(text="cell count"))
        setattr(cls, "cell painting",
            PermissibleValue(text="cell painting"))
        setattr(cls, "cell permeability assay",
            PermissibleValue(text="cell permeability assay"))
        setattr(cls, "cell proliferation",
            PermissibleValue(text="cell proliferation"))
        setattr(cls, "cell viability assay",
            PermissibleValue(text="cell viability assay"))
        setattr(cls, "combination library screen",
            PermissibleValue(text="combination library screen"))
        setattr(cls, "combination screen",
            PermissibleValue(text="combination screen"))
        setattr(cls, "complex II enzyme activity assay",
            PermissibleValue(text="complex II enzyme activity assay"))
        setattr(cls, "compound screen",
            PermissibleValue(text="compound screen"))
        setattr(cls, "current clamp assay",
            PermissibleValue(text="current clamp assay"))
        setattr(cls, "differential scanning calorimetry",
            PermissibleValue(text="differential scanning calorimetry"))
        setattr(cls, "dynamic light scattering",
            PermissibleValue(text="dynamic light scattering"))
        setattr(cls, "electrophoretic light scattering",
            PermissibleValue(text="electrophoretic light scattering"))
        setattr(cls, "flow cytometry",
            PermissibleValue(text="flow cytometry"))
        setattr(cls, "focus forming assay",
            PermissibleValue(text="focus forming assay"))
        setattr(cls, "gel permeation chromatography",
            PermissibleValue(text="gel permeation chromatography"))
        setattr(cls, "in silico synthesis",
            PermissibleValue(text="in silico synthesis"))
        setattr(cls, "in vitro tumorigenesis",
            PermissibleValue(text="in vitro tumorigenesis"))
        setattr(cls, "in vivo PDX viability",
            PermissibleValue(text="in vivo PDX viability"))
        setattr(cls, "in vivo tumor growth",
            PermissibleValue(text="in vivo tumor growth"))
        setattr(cls, "light scattering assay",
            PermissibleValue(text="light scattering assay"))
        setattr(cls, "local field potential recording",
            PermissibleValue(text="local field potential recording"))
        setattr(cls, "long term potentiation assay",
            PermissibleValue(text="long term potentiation assay"))
        setattr(cls, "massively parallel reporter assay",
            PermissibleValue(text="massively parallel reporter assay"))
        setattr(cls, "multi-electrode array",
            PermissibleValue(text="multi-electrode array"))
        setattr(cls, "nanoparticle tracking analysis",
            PermissibleValue(text="nanoparticle tracking analysis"))
        setattr(cls, "oscillatory rheology",
            PermissibleValue(text="oscillatory rheology"))
        setattr(cls, "oxygen consumption assay",
            PermissibleValue(text="oxygen consumption assay"))
        setattr(cls, "perineurial cell thickness",
            PermissibleValue(text="perineurial cell thickness"))
        setattr(cls, "pharmocokinetic ADME assay",
            PermissibleValue(text="pharmocokinetic ADME assay"))
        setattr(cls, "polymerase chain reaction",
            PermissibleValue(text="polymerase chain reaction"))
        setattr(cls, "quantitative PCR",
            PermissibleValue(text="quantitative PCR"))
        setattr(cls, "reactive oxygen species assay",
            PermissibleValue(text="reactive oxygen species assay"))
        setattr(cls, "reporter gene assay",
            PermissibleValue(text="reporter gene assay"))
        setattr(cls, "split-GFP assay",
            PermissibleValue(text="split-GFP assay"))
        setattr(cls, "sandwich ELISA",
            PermissibleValue(text="sandwich ELISA"))
        setattr(cls, "single molecule drug screen assay",
            PermissibleValue(text="single molecule drug screen assay"))
        setattr(cls, "small molecule library screen",
            PermissibleValue(text="small molecule library screen"))
        setattr(cls, "sorbitol dehydrogenase activity level assay",
            PermissibleValue(text="sorbitol dehydrogenase activity level assay"))
        setattr(cls, "static histomorphometry",
            PermissibleValue(text="static histomorphometry"))
        setattr(cls, "static light scattering",
            PermissibleValue(text="static light scattering"))
        setattr(cls, "trans-endothelial electrical resistance",
            PermissibleValue(text="trans-endothelial electrical resistance"))
        setattr(cls, "twin spot assay",
            PermissibleValue(text="twin spot assay"))
        setattr(cls, "whole-cell patch clamp",
            PermissibleValue(text="whole-cell patch clamp"))

class SpeciesEnum(EnumDefinitionImpl):
    """
    Species of origin.
    """
    Unknown = PermissibleValue(text="Unknown")

    _defn = EnumDefinition(
        name="SpeciesEnum",
        description="Species of origin.",
    )

    @classmethod
    def _addvals(cls):
        setattr(cls, "Danio rerio",
            PermissibleValue(text="Danio rerio"))
        setattr(cls, "Drosophila melanogaster",
            PermissibleValue(text="Drosophila melanogaster"))
        setattr(cls, "Gallus gallus",
            PermissibleValue(text="Gallus gallus"))
        setattr(cls, "Homo sapiens",
            PermissibleValue(text="Homo sapiens"))
        setattr(cls, "Mus musculus",
            PermissibleValue(text="Mus musculus"))
        setattr(cls, "Macaca nemestrina",
            PermissibleValue(text="Macaca nemestrina"))
        setattr(cls, "Mus musculus (humanized)",
            PermissibleValue(text="Mus musculus (humanized)"))
        setattr(cls, "Oryctolagus cuniculus",
            PermissibleValue(text="Oryctolagus cuniculus"))
        setattr(cls, "Pan troglodytes",
            PermissibleValue(text="Pan troglodytes"))
        setattr(cls, "Rattus norvegicus",
            PermissibleValue(text="Rattus norvegicus"))
        setattr(cls, "Rhesus macaque",
            PermissibleValue(text="Rhesus macaque"))
        setattr(cls, "Sus scrofa",
            PermissibleValue(text="Sus scrofa"))

class FileFormatEnum(EnumDefinitionImpl):
    """
    File extension or format type.
    """
    bai = PermissibleValue(text="bai")
    bam = PermissibleValue(text="bam")
    bcf = PermissibleValue(text="bcf")
    bed = PermissibleValue(text="bed")
    bedgraph = PermissibleValue(text="bedgraph")
    bgzip = PermissibleValue(text="bgzip")
    cloupe = PermissibleValue(text="cloupe")
    bigwig = PermissibleValue(text="bigwig")
    cnn = PermissibleValue(text="cnn")
    cnr = PermissibleValue(text="cnr")
    cns = PermissibleValue(text="cns")
    crai = PermissibleValue(text="crai")
    cram = PermissibleValue(text="cram")
    csi = PermissibleValue(text="csi")
    ctab = PermissibleValue(text="ctab")
    dup = PermissibleValue(text="dup")
    fasta = PermissibleValue(text="fasta")
    fastq = PermissibleValue(text="fastq")
    flagstat = PermissibleValue(text="flagstat")
    gct = PermissibleValue(text="gct")
    gff3 = PermissibleValue(text="gff3")
    gtf = PermissibleValue(text="gtf")
    hic = PermissibleValue(text="hic")
    maf = PermissibleValue(text="maf")
    mtx = PermissibleValue(text="mtx")
    plink = PermissibleValue(text="plink")
    recal = PermissibleValue(text="recal")
    sam = PermissibleValue(text="sam")
    seg = PermissibleValue(text="seg")
    sf = PermissibleValue(text="sf")
    sra = PermissibleValue(text="sra")
    tagAlign = PermissibleValue(text="tagAlign")
    tbi = PermissibleValue(text="tbi")
    tranches = PermissibleValue(text="tranches")
    vcf = PermissibleValue(text="vcf")
    wiggle = PermissibleValue(text="wiggle")
    DICOM = PermissibleValue(text="DICOM")
    NWB = PermissibleValue(text="NWB")
    PAR = PermissibleValue(text="PAR")
    REC = PermissibleValue(text="REC")
    aci = PermissibleValue(text="aci")
    avi = PermissibleValue(text="avi")
    bmp = PermissibleValue(text="bmp")
    czi = PermissibleValue(text="czi")
    dm3 = PermissibleValue(text="dm3")
    hdr = PermissibleValue(text="hdr")
    img = PermissibleValue(text="img")
    jpg = PermissibleValue(text="jpg")
    lif = PermissibleValue(text="lif")
    mov = PermissibleValue(text="mov")
    nii = PermissibleValue(text="nii")
    png = PermissibleValue(text="png")
    svs = PermissibleValue(text="svs")
    sws = PermissibleValue(text="sws")
    tif = PermissibleValue(text="tif")
    tom = PermissibleValue(text="tom")
    bpm = PermissibleValue(text="bpm")
    cel = PermissibleValue(text="cel")
    chp = PermissibleValue(text="chp")
    dat = PermissibleValue(text="dat")
    idat = PermissibleValue(text="idat")
    locs = PermissibleValue(text="locs")
    msf = PermissibleValue(text="msf")
    mzML = PermissibleValue(text="mzML")
    raw = PermissibleValue(text="raw")
    RCC = PermissibleValue(text="RCC")
    csv = PermissibleValue(text="csv")
    excel = PermissibleValue(text="excel")
    parquet = PermissibleValue(text="parquet")
    tsv = PermissibleValue(text="tsv")
    js = PermissibleValue(text="js")
    RData = PermissibleValue(text="RData")
    SDAT = PermissibleValue(text="SDAT")
    SPAR = PermissibleValue(text="SPAR")
    json = PermissibleValue(text="json")
    prism = PermissibleValue(text="prism")
    rds = PermissibleValue(text="rds")
    sqlite = PermissibleValue(text="sqlite")
    xml = PermissibleValue(text="xml")
    yaml = PermissibleValue(text="yaml")
    gzip = PermissibleValue(text="gzip")
    tar = PermissibleValue(text="tar")
    zip = PermissibleValue(text="zip")
    ai = PermissibleValue(text="ai")
    doc = PermissibleValue(text="doc")
    html = PermissibleValue(text="html")
    hyperlink = PermissibleValue(text="hyperlink")
    md = PermissibleValue(text="md")
    pdf = PermissibleValue(text="pdf")
    powerpoint = PermissibleValue(text="powerpoint")
    txt = PermissibleValue(text="txt")
    ab1 = PermissibleValue(text="ab1")
    abf = PermissibleValue(text="abf")
    dna = PermissibleValue(text="dna")
    edat3 = PermissibleValue(text="edat3")
    fcs = PermissibleValue(text="fcs")
    fig = PermissibleValue(text="fig")
    gb = PermissibleValue(text="gb")
    h5 = PermissibleValue(text="h5")
    hdf5 = PermissibleValue(text="hdf5")
    idx = PermissibleValue(text="idx")
    psydat = PermissibleValue(text="psydat")
    pzfx = PermissibleValue(text="pzfx")
    rmd = PermissibleValue(text="rmd")
    sav = PermissibleValue(text="sav")
    sdf = PermissibleValue(text="sdf")
    sif = PermissibleValue(text="sif")
    svg = PermissibleValue(text="svg")
    Unknown = PermissibleValue(text="Unknown")

    _defn = EnumDefinition(
        name="FileFormatEnum",
        description="File extension or format type.",
    )

    @classmethod
    def _addvals(cls):
        setattr(cls, "bed broadPeak",
            PermissibleValue(text="bed broadPeak"))
        setattr(cls, "bed gappedPeak",
            PermissibleValue(text="bed gappedPeak"))
        setattr(cls, "bed narrowPeak",
            PermissibleValue(text="bed narrowPeak"))
        setattr(cls, "ome-tiff",
            PermissibleValue(text="ome-tiff"))
        setattr(cls, "Sentrix descriptor file",
            PermissibleValue(text="Sentrix descriptor file"))
        setattr(cls, "MATLAB script",
            PermissibleValue(text="MATLAB script"))
        setattr(cls, "Python script",
            PermissibleValue(text="Python script"))
        setattr(cls, "R script",
            PermissibleValue(text="R script"))
        setattr(cls, "bash script",
            PermissibleValue(text="bash script"))
        setattr(cls, "MATLAB data",
            PermissibleValue(text="MATLAB data"))
        setattr(cls, "7z",
            PermissibleValue(text="7z"))
        setattr(cls, "docker image",
            PermissibleValue(text="docker image"))
        setattr(cls, "MPEG-4",
            PermissibleValue(text="MPEG-4"))
        setattr(cls, "Ome-zarr",
            PermissibleValue(text="Ome-zarr"))
        setattr(cls, "Github Repo",
            PermissibleValue(text="Github Repo"))

class DataCategoryEnum(EnumDefinitionImpl):
    """
    Categorical label for data contained in a dataset.
    """
    characteristic = PermissibleValue(text="characteristic")
    clinical = PermissibleValue(text="clinical")
    demographics = PermissibleValue(text="demographics")
    electrophysiology = PermissibleValue(text="electrophysiology")
    image = PermissibleValue(text="image")
    immunoassay = PermissibleValue(text="immunoassay")
    kinomics = PermissibleValue(text="kinomics")
    metabolomics = PermissibleValue(text="metabolomics")
    model = PermissibleValue(text="model")
    network = PermissibleValue(text="network")
    pharmacokinetics = PermissibleValue(text="pharmacokinetics")
    plot = PermissibleValue(text="plot")
    proteomics = PermissibleValue(text="proteomics")
    report = PermissibleValue(text="report")
    volume = PermissibleValue(text="volume")
    weight = PermissibleValue(text="weight")
    Unknown = PermissibleValue(text="Unknown")

    _defn = EnumDefinition(
        name="DataCategoryEnum",
        description="Categorical label for data contained in a dataset.",
    )

    @classmethod
    def _addvals(cls):
        setattr(cls, "aligned reads",
            PermissibleValue(text="aligned reads"))
        setattr(cls, "annotated germline variants",
            PermissibleValue(text="annotated germline variants"))
        setattr(cls, "annotated somatic mutation",
            PermissibleValue(text="annotated somatic mutation"))
        setattr(cls, "audio transcript",
            PermissibleValue(text="audio transcript"))
        setattr(cls, "behavioral data",
            PermissibleValue(text="behavioral data"))
        setattr(cls, "capsid sequence",
            PermissibleValue(text="capsid sequence"))
        setattr(cls, "cellular physiology",
            PermissibleValue(text="cellular physiology"))
        setattr(cls, "chromatin activity",
            PermissibleValue(text="chromatin activity"))
        setattr(cls, "copy number variants",
            PermissibleValue(text="copy number variants"))
        setattr(cls, "count matrix",
            PermissibleValue(text="count matrix"))
        setattr(cls, "data index",
            PermissibleValue(text="data index"))
        setattr(cls, "data sharing plan",
            PermissibleValue(text="data sharing plan"))
        setattr(cls, "drug combination screen",
            PermissibleValue(text="drug combination screen"))
        setattr(cls, "drug screen",
            PermissibleValue(text="drug screen"))
        setattr(cls, "epidemiological data",
            PermissibleValue(text="epidemiological data"))
        setattr(cls, "gene expression",
            PermissibleValue(text="gene expression"))
        setattr(cls, "gene expression matrix",
            PermissibleValue(text="gene expression matrix"))
        setattr(cls, "quantified gene expression",
            PermissibleValue(text="quantified gene expression"))
        setattr(cls, "genomic features",
            PermissibleValue(text="genomic features"))
        setattr(cls, "genomic variants",
            PermissibleValue(text="genomic variants"))
        setattr(cls, "germline variants",
            PermissibleValue(text="germline variants"))
        setattr(cls, "guide RNA sequence",
            PermissibleValue(text="guide RNA sequence"))
        setattr(cls, "isoform expression",
            PermissibleValue(text="isoform expression"))
        setattr(cls, "mask image",
            PermissibleValue(text="mask image"))
        setattr(cls, "mass spectrometry data",
            PermissibleValue(text="mass spectrometry data"))
        setattr(cls, "molecular property",
            PermissibleValue(text="molecular property"))
        setattr(cls, "morphology parameter",
            PermissibleValue(text="morphology parameter"))
        setattr(cls, "nucleic acid sequence record",
            PermissibleValue(text="nucleic acid sequence record"))
        setattr(cls, "over-representation data",
            PermissibleValue(text="over-representation data"))
        setattr(cls, "particle characterization",
            PermissibleValue(text="particle characterization"))
        setattr(cls, "physiology parameter",
            PermissibleValue(text="physiology parameter"))
        setattr(cls, "plasmid sequence",
            PermissibleValue(text="plasmid sequence"))
        setattr(cls, "primer sequence",
            PermissibleValue(text="primer sequence"))
        setattr(cls, "probe sequence",
            PermissibleValue(text="probe sequence"))
        setattr(cls, "promoter sequence",
            PermissibleValue(text="promoter sequence"))
        setattr(cls, "protein interaction data",
            PermissibleValue(text="protein interaction data"))
        setattr(cls, "protein interaction raw data",
            PermissibleValue(text="protein interaction raw data"))
        setattr(cls, "raw counts",
            PermissibleValue(text="raw counts"))
        setattr(cls, "reference sequence",
            PermissibleValue(text="reference sequence"))
        setattr(cls, "somatic variants",
            PermissibleValue(text="somatic variants"))
        setattr(cls, "structural variants",
            PermissibleValue(text="structural variants"))
        setattr(cls, "survey data",
            PermissibleValue(text="survey data"))
        setattr(cls, "text data",
            PermissibleValue(text="text data"))

class ProcessLevelEnum(EnumDefinitionImpl):
    """
    Level of data processing applied to the dataset.
    """
    Auxiliary = PermissibleValue(
        text="Auxiliary",
        description="""Additional files that contain information or experimental details, but do not contain data or processed derivatives.""")
    Metadata = PermissibleValue(
        text="Metadata",
        description="Files that are or will be stored and shared as metadata.")

    _defn = EnumDefinition(
        name="ProcessLevelEnum",
        description="Level of data processing applied to the dataset.",
    )

    @classmethod
    def _addvals(cls):
        setattr(cls, "Level 1",
            PermissibleValue(
                text="Level 1",
                description="Raw or minimally processed data."))
        setattr(cls, "Level 2",
            PermissibleValue(
                text="Level 2",
                description="""Data that has undergone a basic or initial processing step, like quality control, alignment, or stitching."""))
        setattr(cls, "Level 3",
            PermissibleValue(
                text="Level 3",
                description="""Files that contain summary counts, coverage files, or other processed representations of the data."""))
        setattr(cls, "Level 4",
            PermissibleValue(
                text="Level 4",
                description="""Files that contain data related to applied models or aggregate representations of the data."""))
        setattr(cls, "Not Applicable",
            PermissibleValue(
                text="Not Applicable",
                description="Files that fall outside of the level structure or are uploaded as a package."))

class NamContextEnum(EnumDefinitionImpl):
    """
    NAM application context associated with files in the dataset.
    """
    Biosamples = PermissibleValue(text="Biosamples")

    _defn = EnumDefinition(
        name="NamContextEnum",
        description="NAM application context associated with files in the dataset.",
    )

    @classmethod
    def _addvals(cls):
        setattr(cls, "Subjects / Donors",
            PermissibleValue(text="Subjects / Donors"))
        setattr(cls, "Files / Data Types",
            PermissibleValue(text="Files / Data Types"))
        setattr(cls, "In Chemico / Biomaterials",
            PermissibleValue(text="In Chemico / Biomaterials"))
        setattr(cls, "Assays / Conditions",
            PermissibleValue(text="Assays / Conditions"))
        setattr(cls, "Ontologies / Standards",
            PermissibleValue(text="Ontologies / Standards"))
        setattr(cls, "Imaging Metadata",
            PermissibleValue(text="Imaging Metadata"))
        setattr(cls, "Pharmacokinetics / ADMET",
            PermissibleValue(text="Pharmacokinetics / ADMET"))
        setattr(cls, "Analytical Models",
            PermissibleValue(text="Analytical Models"))

class RepositoryEnum(EnumDefinitionImpl):
    """
    Repository where a dataset is hosted.
    """
    Synapse = PermissibleValue(text="Synapse")
    GEO = PermissibleValue(text="GEO")
    SRA = PermissibleValue(text="SRA")
    Zenodo = PermissibleValue(text="Zenodo")
    Other = PermissibleValue(text="Other")

    _defn = EnumDefinition(
        name="RepositoryEnum",
        description="Repository where a dataset is hosted.",
    )

class AccessTypeEnum(EnumDefinitionImpl):
    """
    Data access level.
    """
    Open = PermissibleValue(
        text="Open",
        description="Publicly accessible without restrictions.")
    Controlled = PermissibleValue(
        text="Controlled",
        description="Requires approval via Synapse Access Requirements.")
    Embargoed = PermissibleValue(
        text="Embargoed",
        description="Temporarily restricted; will become open after embargo lifts.")

    _defn = EnumDefinition(
        name="AccessTypeEnum",
        description="Data access level.",
    )

class DevelopmentStatusEnum(EnumDefinitionImpl):
    """
    Current development stage of a NAM.
    """
    Validated = PermissibleValue(
        text="Validated",
        description="Method has been formally validated.")
    Prototype = PermissibleValue(
        text="Prototype",
        description="Early-stage implementation.")
    Deprecated = PermissibleValue(
        text="Deprecated",
        description="Method is no longer actively maintained.")

    _defn = EnumDefinition(
        name="DevelopmentStatusEnum",
        description="Current development stage of a NAM.",
    )

    @classmethod
    def _addvals(cls):
        setattr(cls, "In Development",
            PermissibleValue(
                text="In Development",
                description="Method is being actively developed."))

class RoleEnum(EnumDefinitionImpl):
    """
    Role of a person in the NAMHub program.
    """
    Collaborator = PermissibleValue(text="Collaborator")
    Trainee = PermissibleValue(text="Trainee")
    Other = PermissibleValue(text="Other")

    _defn = EnumDefinition(
        name="RoleEnum",
        description="Role of a person in the NAMHub program.",
    )

    @classmethod
    def _addvals(cls):
        setattr(cls, "Principal Investigator",
            PermissibleValue(text="Principal Investigator"))
        setattr(cls, "Co-Investigator",
            PermissibleValue(text="Co-Investigator"))
        setattr(cls, "Coordinating Center",
            PermissibleValue(text="Coordinating Center"))

# Slots
class slots:
    pass

slots.studyId = Slot(uri=NAMHUB.studyId, name="studyId", curie=NAMHUB.curie('studyId'),
                   model_uri=NAMHUB.studyId, domain=None, range=Optional[str])

slots.studyName = Slot(uri=NAMHUB.studyName, name="studyName", curie=NAMHUB.curie('studyName'),
                   model_uri=NAMHUB.studyName, domain=None, range=Optional[str])

slots.institution = Slot(uri=NAMHUB.institution, name="institution", curie=NAMHUB.curie('institution'),
                   model_uri=NAMHUB.institution, domain=None, range=Optional[Union[str, list[str]]])

slots.fundingAgency = Slot(uri=NAMHUB.fundingAgency, name="fundingAgency", curie=NAMHUB.curie('fundingAgency'),
                   model_uri=NAMHUB.fundingAgency, domain=None, range=Optional[Union[str, list[str]]])

slots.grantId = Slot(uri=NAMHUB.grantId, name="grantId", curie=NAMHUB.curie('grantId'),
                   model_uri=NAMHUB.grantId, domain=None, range=Optional[str])

slots.description = Slot(uri=NAMHUB.description, name="description", curie=NAMHUB.curie('description'),
                   model_uri=NAMHUB.description, domain=None, range=Optional[str])

slots.doi = Slot(uri=NAMHUB.doi, name="doi", curie=NAMHUB.curie('doi'),
                   model_uri=NAMHUB.doi, domain=None, range=Optional[Union[str, URI]])

slots.assay = Slot(uri=NAMHUB.assay, name="assay", curie=NAMHUB.curie('assay'),
                   model_uri=NAMHUB.assay, domain=None, range=Optional[Union[Union[str, "AssayEnum"], list[Union[str, "AssayEnum"]]]])

slots.dataType = Slot(uri=NAMHUB.dataType, name="dataType", curie=NAMHUB.curie('dataType'),
                   model_uri=NAMHUB.dataType, domain=None, range=Optional[Union[Union[str, "DataCategoryEnum"], list[Union[str, "DataCategoryEnum"]]]])

slots.species = Slot(uri=NAMHUB.species, name="species", curie=NAMHUB.curie('species'),
                   model_uri=NAMHUB.species, domain=None, range=Optional[Union[Union[str, "SpeciesEnum"], list[Union[str, "SpeciesEnum"]]]])

slots.accessType = Slot(uri=NAMHUB.accessType, name="accessType", curie=NAMHUB.curie('accessType'),
                   model_uri=NAMHUB.accessType, domain=None, range=Optional[Union[str, "AccessTypeEnum"]])

slots.namId = Slot(uri=NAMHUB.namId, name="namId", curie=NAMHUB.curie('namId'),
                   model_uri=NAMHUB.namId, domain=None, range=Optional[Union[str, list[str]]])

slots.externalLink = Slot(uri=NAMHUB.externalLink, name="externalLink", curie=NAMHUB.curie('externalLink'),
                   model_uri=NAMHUB.externalLink, domain=None, range=Optional[Union[str, URI]])

slots.synapseEntityId = Slot(uri=NAMHUB.synapseEntityId, name="synapseEntityId", curie=NAMHUB.curie('synapseEntityId'),
                   model_uri=NAMHUB.synapseEntityId, domain=None, range=Optional[str],
                   pattern=re.compile(r'^syn\d+$'))

slots.portalDisplay = Slot(uri=NAMHUB.portalDisplay, name="portalDisplay", curie=NAMHUB.curie('portalDisplay'),
                   model_uri=NAMHUB.portalDisplay, domain=None, range=Optional[Union[bool, Bool]])

slots.landscapeId = Slot(uri=NAMHUB.landscapeId, name="landscapeId", curie=NAMHUB.curie('landscapeId'),
                   model_uri=NAMHUB.landscapeId, domain=None, range=Optional[str])

slots.datasetName = Slot(uri=NAMHUB.datasetName, name="datasetName", curie=NAMHUB.curie('datasetName'),
                   model_uri=NAMHUB.datasetName, domain=None, range=Optional[str])

slots.datasetDescription = Slot(uri=NAMHUB.datasetDescription, name="datasetDescription", curie=NAMHUB.curie('datasetDescription'),
                   model_uri=NAMHUB.datasetDescription, domain=None, range=Optional[str])

slots.datasetAssay = Slot(uri=NAMHUB.datasetAssay, name="datasetAssay", curie=NAMHUB.curie('datasetAssay'),
                   model_uri=NAMHUB.datasetAssay, domain=None, range=Optional[Union[str, "AssayEnum"]])

slots.datasetSpecies = Slot(uri=NAMHUB.datasetSpecies, name="datasetSpecies", curie=NAMHUB.curie('datasetSpecies'),
                   model_uri=NAMHUB.datasetSpecies, domain=None, range=Optional[Union[str, "SpeciesEnum"]])

slots.datasetFileFormats = Slot(uri=NAMHUB.datasetFileFormats, name="datasetFileFormats", curie=NAMHUB.curie('datasetFileFormats'),
                   model_uri=NAMHUB.datasetFileFormats, domain=None, range=Optional[Union[Union[str, "FileFormatEnum"], list[Union[str, "FileFormatEnum"]]]])

slots.expectedDataVolume = Slot(uri=NAMHUB.expectedDataVolume, name="expectedDataVolume", curie=NAMHUB.curie('expectedDataVolume'),
                   model_uri=NAMHUB.expectedDataVolume, domain=None, range=Optional[str])

slots.datasetCategory = Slot(uri=NAMHUB.datasetCategory, name="datasetCategory", curie=NAMHUB.curie('datasetCategory'),
                   model_uri=NAMHUB.datasetCategory, domain=None, range=Optional[Union[str, "DataCategoryEnum"]])

slots.contextOfUse = Slot(uri=NAMHUB.contextOfUse, name="contextOfUse", curie=NAMHUB.curie('contextOfUse'),
                   model_uri=NAMHUB.contextOfUse, domain=None, range=Optional[Union[str, list[str]]])

slots.applicableStandards = Slot(uri=NAMHUB.applicableStandards, name="applicableStandards", curie=NAMHUB.curie('applicableStandards'),
                   model_uri=NAMHUB.applicableStandards, domain=None, range=Optional[str])

slots.expectedNumberOfFiles = Slot(uri=NAMHUB.expectedNumberOfFiles, name="expectedNumberOfFiles", curie=NAMHUB.curie('expectedNumberOfFiles'),
                   model_uri=NAMHUB.expectedNumberOfFiles, domain=None, range=Optional[int])

slots.expectedNumberOfSamples = Slot(uri=NAMHUB.expectedNumberOfSamples, name="expectedNumberOfSamples", curie=NAMHUB.curie('expectedNumberOfSamples'),
                   model_uri=NAMHUB.expectedNumberOfSamples, domain=None, range=Optional[int])

slots.uploadByDate = Slot(uri=NAMHUB.uploadByDate, name="uploadByDate", curie=NAMHUB.curie('uploadByDate'),
                   model_uri=NAMHUB.uploadByDate, domain=None, range=Optional[str])

slots.dataContributionLead = Slot(uri=NAMHUB.dataContributionLead, name="dataContributionLead", curie=NAMHUB.curie('dataContributionLead'),
                   model_uri=NAMHUB.dataContributionLead, domain=None, range=Optional[str])

slots.studyAim = Slot(uri=NAMHUB.studyAim, name="studyAim", curie=NAMHUB.curie('studyAim'),
                   model_uri=NAMHUB.studyAim, domain=None, range=Optional[str])

slots.comments = Slot(uri=NAMHUB.comments, name="comments", curie=NAMHUB.curie('comments'),
                   model_uri=NAMHUB.comments, domain=None, range=Optional[str])

slots.studyLeads = Slot(uri=NAMHUB.studyLeads, name="studyLeads", curie=NAMHUB.curie('studyLeads'),
                   model_uri=NAMHUB.studyLeads, domain=None, range=Optional[Union[str, list[str]]])

slots.summary = Slot(uri=NAMHUB.summary, name="summary", curie=NAMHUB.curie('summary'),
                   model_uri=NAMHUB.summary, domain=None, range=Optional[str])

slots.synapseProjectId = Slot(uri=NAMHUB.synapseProjectId, name="synapseProjectId", curie=NAMHUB.curie('synapseProjectId'),
                   model_uri=NAMHUB.synapseProjectId, domain=None, range=Optional[str],
                   pattern=re.compile(r'^syn\d+$'))

slots.studyDoi = Slot(uri=NAMHUB.studyDoi, name="studyDoi", curie=NAMHUB.curie('studyDoi'),
                   model_uri=NAMHUB.studyDoi, domain=None, range=Optional[Union[str, URI]])

slots.diseaseFocus = Slot(uri=NAMHUB.diseaseFocus, name="diseaseFocus", curie=NAMHUB.curie('diseaseFocus'),
                   model_uri=NAMHUB.diseaseFocus, domain=None, range=Optional[Union[str, list[str]]])

slots.alternateName = Slot(uri=NAMHUB.alternateName, name="alternateName", curie=NAMHUB.curie('alternateName'),
                   model_uri=NAMHUB.alternateName, domain=None, range=Optional[Union[str, list[str]]])

slots.NAMsTechFocus = Slot(uri=NAMHUB.NAMsTechFocus, name="NAMsTechFocus", curie=NAMHUB.curie('NAMsTechFocus'),
                   model_uri=NAMHUB.NAMsTechFocus, domain=None, range=Optional[Union[str, list[str]]])

slots.datasetId = Slot(uri=NAMHUB.datasetId, name="datasetId", curie=NAMHUB.curie('datasetId'),
                   model_uri=NAMHUB.datasetId, domain=None, range=Optional[str],
                   pattern=re.compile(r'^syn\d+$'))

slots.title = Slot(uri=NAMHUB.title, name="title", curie=NAMHUB.curie('title'),
                   model_uri=NAMHUB.title, domain=None, range=Optional[str])

slots.format = Slot(uri=NAMHUB.format, name="format", curie=NAMHUB.curie('format'),
                   model_uri=NAMHUB.format, domain=None, range=Optional[Union[Union[str, "FileFormatEnum"], list[Union[str, "FileFormatEnum"]]]])

slots.repository = Slot(uri=NAMHUB.repository, name="repository", curie=NAMHUB.curie('repository'),
                   model_uri=NAMHUB.repository, domain=None, range=Optional[Union[str, "RepositoryEnum"]])

slots.releaseDate = Slot(uri=NAMHUB.releaseDate, name="releaseDate", curie=NAMHUB.curie('releaseDate'),
                   model_uri=NAMHUB.releaseDate, domain=None, range=Optional[Union[str, XSDDate]])

slots.datasetItemCount = Slot(uri=NAMHUB.datasetItemCount, name="datasetItemCount", curie=NAMHUB.curie('datasetItemCount'),
                   model_uri=NAMHUB.datasetItemCount, domain=None, range=Optional[int])

slots.datasetSizeInBytes = Slot(uri=NAMHUB.datasetSizeInBytes, name="datasetSizeInBytes", curie=NAMHUB.curie('datasetSizeInBytes'),
                   model_uri=NAMHUB.datasetSizeInBytes, domain=None, range=Optional[int])

slots.hasCroissantMetadata = Slot(uri=NAMHUB.hasCroissantMetadata, name="hasCroissantMetadata", curie=NAMHUB.curie('hasCroissantMetadata'),
                   model_uri=NAMHUB.hasCroissantMetadata, domain=None, range=Optional[Union[bool, Bool]])

slots.croissantMetadataUrl = Slot(uri=NAMHUB.croissantMetadataUrl, name="croissantMetadataUrl", curie=NAMHUB.curie('croissantMetadataUrl'),
                   model_uri=NAMHUB.croissantMetadataUrl, domain=None, range=Optional[Union[str, URI]])

slots.investigatorId = Slot(uri=NAMHUB.investigatorId, name="investigatorId", curie=NAMHUB.curie('investigatorId'),
                   model_uri=NAMHUB.investigatorId, domain=None, range=Optional[str])

slots.firstName = Slot(uri=NAMHUB.firstName, name="firstName", curie=NAMHUB.curie('firstName'),
                   model_uri=NAMHUB.firstName, domain=None, range=Optional[str])

slots.lastName = Slot(uri=NAMHUB.lastName, name="lastName", curie=NAMHUB.curie('lastName'),
                   model_uri=NAMHUB.lastName, domain=None, range=Optional[str])

slots.role = Slot(uri=NAMHUB.role, name="role", curie=NAMHUB.curie('role'),
                   model_uri=NAMHUB.role, domain=None, range=Optional[Union[str, "RoleEnum"]])

slots.orcidId = Slot(uri=NAMHUB.orcidId, name="orcidId", curie=NAMHUB.curie('orcidId'),
                   model_uri=NAMHUB.orcidId, domain=None, range=Optional[str],
                   pattern=re.compile(r'^\d{4}-\d{4}-\d{4}-\d{3}[\dX]$'))

slots.synapseId = Slot(uri=NAMHUB.synapseId, name="synapseId", curie=NAMHUB.curie('synapseId'),
                   model_uri=NAMHUB.synapseId, domain=None, range=Optional[str])

slots.email = Slot(uri=NAMHUB.email, name="email", curie=NAMHUB.curie('email'),
                   model_uri=NAMHUB.email, domain=None, range=Optional[str],
                   pattern=re.compile(r'^[^@]+@[^@]+\.[^@]+$'))

slots.grantName = Slot(uri=NAMHUB.grantName, name="grantName", curie=NAMHUB.curie('grantName'),
                   model_uri=NAMHUB.grantName, domain=None, range=Optional[str])

slots.grantNumber = Slot(uri=NAMHUB.grantNumber, name="grantNumber", curie=NAMHUB.curie('grantNumber'),
                   model_uri=NAMHUB.grantNumber, domain=None, range=Optional[str])

slots.grantType = Slot(uri=NAMHUB.grantType, name="grantType", curie=NAMHUB.curie('grantType'),
                   model_uri=NAMHUB.grantType, domain=None, range=Optional[str])

slots.grantInstitution = Slot(uri=NAMHUB.grantInstitution, name="grantInstitution", curie=NAMHUB.curie('grantInstitution'),
                   model_uri=NAMHUB.grantInstitution, domain=None, range=Optional[str])

slots.abstract = Slot(uri=NAMHUB.abstract, name="abstract", curie=NAMHUB.curie('abstract'),
                   model_uri=NAMHUB.abstract, domain=None, range=Optional[str])

slots.investigator = Slot(uri=NAMHUB.investigator, name="investigator", curie=NAMHUB.curie('investigator'),
                   model_uri=NAMHUB.investigator, domain=None, range=Optional[str])

slots.nihReporterLink = Slot(uri=NAMHUB.nihReporterLink, name="nihReporterLink", curie=NAMHUB.curie('nihReporterLink'),
                   model_uri=NAMHUB.nihReporterLink, domain=None, range=Optional[Union[str, URI]])

slots.namName = Slot(uri=NAMHUB.namName, name="namName", curie=NAMHUB.curie('namName'),
                   model_uri=NAMHUB.namName, domain=None, range=Optional[str])

slots.developmentStatus = Slot(uri=NAMHUB.developmentStatus, name="developmentStatus", curie=NAMHUB.curie('developmentStatus'),
                   model_uri=NAMHUB.developmentStatus, domain=None, range=Optional[Union[str, "DevelopmentStatusEnum"]])

slots.namoClass = Slot(uri=NAMHUB.namoClass, name="namoClass", curie=NAMHUB.curie('namoClass'),
                   model_uri=NAMHUB.namoClass, domain=None, range=Optional[str])

slots.namoCategory = Slot(uri=NAMHUB.namoCategory, name="namoCategory", curie=NAMHUB.curie('namoCategory'),
                   model_uri=NAMHUB.namoCategory, domain=None, range=Optional[str])

slots.namoId = Slot(uri=NAMHUB.namoId, name="namoId", curie=NAMHUB.curie('namoId'),
                   model_uri=NAMHUB.namoId, domain=None, range=Optional[str],
                   pattern=re.compile(r'^NAMO:\d+$'))

slots.organism = Slot(uri=NAMHUB.organism, name="organism", curie=NAMHUB.curie('organism'),
                   model_uri=NAMHUB.organism, domain=None, range=Optional[Union[Union[str, "SpeciesEnum"], list[Union[str, "SpeciesEnum"]]]])

slots.tissueOrCellType = Slot(uri=NAMHUB.tissueOrCellType, name="tissueOrCellType", curie=NAMHUB.curie('tissueOrCellType'),
                   model_uri=NAMHUB.tissueOrCellType, domain=None, range=Optional[Union[str, list[str]]])

slots.endpointsMeasured = Slot(uri=NAMHUB.endpointsMeasured, name="endpointsMeasured", curie=NAMHUB.curie('endpointsMeasured'),
                   model_uri=NAMHUB.endpointsMeasured, domain=None, range=Optional[Union[str, list[str]]])

slots.datasetId_list = Slot(uri=NAMHUB.datasetId_list, name="datasetId_list", curie=NAMHUB.curie('datasetId_list'),
                   model_uri=NAMHUB.datasetId_list, domain=None, range=Optional[Union[str, list[str]]])

slots.relatedPublications = Slot(uri=NAMHUB.relatedPublications, name="relatedPublications", curie=NAMHUB.curie('relatedPublications'),
                   model_uri=NAMHUB.relatedPublications, domain=None, range=Optional[Union[str, list[str]]])

slots.accessRequirements = Slot(uri=NAMHUB.accessRequirements, name="accessRequirements", curie=NAMHUB.curie('accessRequirements'),
                   model_uri=NAMHUB.accessRequirements, domain=None, range=Optional[str])

slots.duoCode = Slot(uri=NAMHUB.duoCode, name="duoCode", curie=NAMHUB.curie('duoCode'),
                   model_uri=NAMHUB.duoCode, domain=None, range=Optional[Union[str, list[str]]])

slots.acknowledgementStatements = Slot(uri=NAMHUB.acknowledgementStatements, name="acknowledgementStatements", curie=NAMHUB.curie('acknowledgementStatements'),
                   model_uri=NAMHUB.acknowledgementStatements, domain=None, range=Optional[str])

slots.license = Slot(uri=NAMHUB.license, name="license", curie=NAMHUB.curie('license'),
                   model_uri=NAMHUB.license, domain=None, range=Optional[str])

slots.pubMedId = Slot(uri=NAMHUB.pubMedId, name="pubMedId", curie=NAMHUB.curie('pubMedId'),
                   model_uri=NAMHUB.pubMedId, domain=None, range=Optional[str])

slots.publicationTitle = Slot(uri=NAMHUB.publicationTitle, name="publicationTitle", curie=NAMHUB.curie('publicationTitle'),
                   model_uri=NAMHUB.publicationTitle, domain=None, range=Optional[str])

slots.authors = Slot(uri=NAMHUB.authors, name="authors", curie=NAMHUB.curie('authors'),
                   model_uri=NAMHUB.authors, domain=None, range=Optional[str])

slots.journal = Slot(uri=NAMHUB.journal, name="journal", curie=NAMHUB.curie('journal'),
                   model_uri=NAMHUB.journal, domain=None, range=Optional[str])

slots.publicationYear = Slot(uri=NAMHUB.publicationYear, name="publicationYear", curie=NAMHUB.curie('publicationYear'),
                   model_uri=NAMHUB.publicationYear, domain=None, range=Optional[int])

slots.pubMedLink = Slot(uri=NAMHUB.pubMedLink, name="pubMedLink", curie=NAMHUB.curie('pubMedLink'),
                   model_uri=NAMHUB.pubMedLink, domain=None, range=Optional[Union[str, URI]])

slots.keywords = Slot(uri=NAMHUB.keywords, name="keywords", curie=NAMHUB.curie('keywords'),
                   model_uri=NAMHUB.keywords, domain=None, range=Optional[Union[str, list[str]]])

slots.Landscape_landscapeId = Slot(uri=NAMHUB.landscapeId, name="Landscape_landscapeId", curie=NAMHUB.curie('landscapeId'),
                   model_uri=NAMHUB.Landscape_landscapeId, domain=Landscape, range=str)

slots.Landscape_datasetName = Slot(uri=NAMHUB.datasetName, name="Landscape_datasetName", curie=NAMHUB.curie('datasetName'),
                   model_uri=NAMHUB.Landscape_datasetName, domain=Landscape, range=str)

slots.Landscape_datasetDescription = Slot(uri=NAMHUB.datasetDescription, name="Landscape_datasetDescription", curie=NAMHUB.curie('datasetDescription'),
                   model_uri=NAMHUB.Landscape_datasetDescription, domain=Landscape, range=str)

slots.Landscape_datasetAssay = Slot(uri=NAMHUB.datasetAssay, name="Landscape_datasetAssay", curie=NAMHUB.curie('datasetAssay'),
                   model_uri=NAMHUB.Landscape_datasetAssay, domain=Landscape, range=Union[str, "AssayEnum"])

slots.Landscape_datasetSpecies = Slot(uri=NAMHUB.datasetSpecies, name="Landscape_datasetSpecies", curie=NAMHUB.curie('datasetSpecies'),
                   model_uri=NAMHUB.Landscape_datasetSpecies, domain=Landscape, range=Union[str, "SpeciesEnum"])

slots.Landscape_datasetFileFormats = Slot(uri=NAMHUB.datasetFileFormats, name="Landscape_datasetFileFormats", curie=NAMHUB.curie('datasetFileFormats'),
                   model_uri=NAMHUB.Landscape_datasetFileFormats, domain=Landscape, range=Union[Union[str, "FileFormatEnum"], list[Union[str, "FileFormatEnum"]]])

slots.Landscape_datasetCategory = Slot(uri=NAMHUB.datasetCategory, name="Landscape_datasetCategory", curie=NAMHUB.curie('datasetCategory'),
                   model_uri=NAMHUB.Landscape_datasetCategory, domain=Landscape, range=Union[str, "DataCategoryEnum"])

slots.Landscape_contextOfUse = Slot(uri=NAMHUB.contextOfUse, name="Landscape_contextOfUse", curie=NAMHUB.curie('contextOfUse'),
                   model_uri=NAMHUB.Landscape_contextOfUse, domain=Landscape, range=Union[str, list[str]])

slots.Landscape_expectedNumberOfFiles = Slot(uri=NAMHUB.expectedNumberOfFiles, name="Landscape_expectedNumberOfFiles", curie=NAMHUB.curie('expectedNumberOfFiles'),
                   model_uri=NAMHUB.Landscape_expectedNumberOfFiles, domain=Landscape, range=int)

slots.Landscape_expectedNumberOfSamples = Slot(uri=NAMHUB.expectedNumberOfSamples, name="Landscape_expectedNumberOfSamples", curie=NAMHUB.curie('expectedNumberOfSamples'),
                   model_uri=NAMHUB.Landscape_expectedNumberOfSamples, domain=Landscape, range=int)

slots.Landscape_expectedDataVolume = Slot(uri=NAMHUB.expectedDataVolume, name="Landscape_expectedDataVolume", curie=NAMHUB.curie('expectedDataVolume'),
                   model_uri=NAMHUB.Landscape_expectedDataVolume, domain=Landscape, range=Optional[str])

slots.Landscape_uploadByDate = Slot(uri=NAMHUB.uploadByDate, name="Landscape_uploadByDate", curie=NAMHUB.curie('uploadByDate'),
                   model_uri=NAMHUB.Landscape_uploadByDate, domain=Landscape, range=str)

slots.Landscape_dataContributionLead = Slot(uri=NAMHUB.dataContributionLead, name="Landscape_dataContributionLead", curie=NAMHUB.curie('dataContributionLead'),
                   model_uri=NAMHUB.Landscape_dataContributionLead, domain=Landscape, range=str)

slots.Landscape_studyName = Slot(uri=NAMHUB.studyName, name="Landscape_studyName", curie=NAMHUB.curie('studyName'),
                   model_uri=NAMHUB.Landscape_studyName, domain=Landscape, range=str)

slots.Landscape_studyAim = Slot(uri=NAMHUB.studyAim, name="Landscape_studyAim", curie=NAMHUB.curie('studyAim'),
                   model_uri=NAMHUB.Landscape_studyAim, domain=Landscape, range=str)

slots.Studies_studyId = Slot(uri=NAMHUB.studyId, name="Studies_studyId", curie=NAMHUB.curie('studyId'),
                   model_uri=NAMHUB.Studies_studyId, domain=Studies, range=str)

slots.Studies_studyName = Slot(uri=NAMHUB.studyName, name="Studies_studyName", curie=NAMHUB.curie('studyName'),
                   model_uri=NAMHUB.Studies_studyName, domain=Studies, range=str)

slots.Datasets_title = Slot(uri=NAMHUB.title, name="Datasets_title", curie=NAMHUB.curie('title'),
                   model_uri=NAMHUB.Datasets_title, domain=Datasets, range=str)

slots.People_firstName = Slot(uri=NAMHUB.firstName, name="People_firstName", curie=NAMHUB.curie('firstName'),
                   model_uri=NAMHUB.People_firstName, domain=People, range=str)

slots.People_lastName = Slot(uri=NAMHUB.lastName, name="People_lastName", curie=NAMHUB.curie('lastName'),
                   model_uri=NAMHUB.People_lastName, domain=People, range=str)

slots.Grants_grantId = Slot(uri=NAMHUB.grantId, name="Grants_grantId", curie=NAMHUB.curie('grantId'),
                   model_uri=NAMHUB.Grants_grantId, domain=Grants, range=str)

slots.NAMs_namId = Slot(uri=NAMHUB.namId, name="NAMs_namId", curie=NAMHUB.curie('namId'),
                   model_uri=NAMHUB.NAMs_namId, domain=NAMs, range=Union[str, list[str]])

slots.NAMs_namName = Slot(uri=NAMHUB.namName, name="NAMs_namName", curie=NAMHUB.curie('namName'),
                   model_uri=NAMHUB.NAMs_namName, domain=NAMs, range=str)

slots.Publications_publicationTitle = Slot(uri=NAMHUB.publicationTitle, name="Publications_publicationTitle", curie=NAMHUB.curie('publicationTitle'),
                   model_uri=NAMHUB.Publications_publicationTitle, domain=Publications, range=str)
