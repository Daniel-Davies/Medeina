import os.path

DATASETS = "datasets"
WEB = "interactionWeb"
TAXA = "taxonomicIndex"
# CONFIDENCE = 'confidences'
LINKS = "links"
EXCEPTIONS = "reorderedTaxaInteractions"
REALNAMES = "speciesStringNames"

IDTRACKER = (
    "numericCounter-b2ca94aee362f455a41493a0d28b98bc5074065b0f96cbb95028ead20b1c72ea"
)


my_path = os.path.abspath(os.path.dirname(__file__))

ROOT = my_path
ZIPDIR = os.path.join(my_path, "CompressedWebStore.zip")
BASEDIR = os.path.join(my_path, "CompressedWebStore")

TAXA_OF_INTEREST = ["kingdom", "phylum", "order", "class", "family", "genus"]

APIMAX = 100

APIURL = "http://resolver.globalnames.org/name_resolvers.json"

DATASET_METAS = [
    "interactionType",
    "evidencedBy",
    "webName",
    "citation",
    "location",
    "date",
]
LINK_METAS = ["interactionType", "evidencedBy", "location"]

PRECOMPUTER_STORE_PATH = "TaxaMapper/newMappingIndex"
