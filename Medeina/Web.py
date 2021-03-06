import pycountry
from .common import (
    writeObjToDateStore,
    retrieveObjFromStore,
    serialise,
    prettyPrintDict,
)
from .config import *
from .dataCleaning import cleanSingleSpeciesString
from .filterFunctions import *
from .MedeinaCumulativeApplication import MedeinaCumulativeApplication


class Web:
    def __init__(self, path=BASEDIR, *args, **kwargs):
        self.storePath = path
        if len(kwargs) == 0:
            self.interactions = retrieveObjFromStore(self.storePath, WEB)
            self.taxaExceptions = retrieveObjFromStore(self.storePath, EXCEPTIONS)
            self.taxa = retrieveObjFromStore(self.storePath, TAXA)
            self.linkMetas = retrieveObjFromStore(self.storePath, LINKS)
            self.datasetMetas = retrieveObjFromStore(self.storePath, DATASETS)
            self.stringNames = retrieveObjFromStore(self.storePath, REALNAMES)
            self.logbook = []
        else:
            self.interactions = kwargs["interactions"]
            self.taxaExceptions = kwargs["taxaExceptions"]
            self.taxa = kwargs["taxa"]
            self.linkMetas = kwargs["linkMetas"]
            self.datasetMetas = kwargs["datasetMetas"]
            self.stringNames = kwargs["stringNames"]
            self.logbook = kwargs["logbook"]

    def view_session_taxonomic_exceptions(self):
        prettyPrintDict(self.taxaExceptions)

    def add_taxonomic_exception(self, species, consumer, resource, save=False):
        species, consumer, resource = self.ensureValidExceptionInput(
            species, consumer, resource
        )
        self.taxaExceptions[species] = {"consumer": consumer, "resource": resource}
        if save:
            txe = retrieveObjFromStore(self.storePath, EXCEPTIONS)
            txe[species] = {"consumer": consumer, "resource": resource}
            writeObjToDateStore(self.storePath, EXCEPTIONS, txe)

    def ensureValidExceptionInput(self, species, consumer, resource):
        species = cleanSingleSpeciesString(species)
        consumer = consumer.lower()
        resource = resource.lower()
        if species not in self.stringNames:
            raise ValueError("No such species in the data store!")
        if consumer not in TAXA_OF_INTEREST:
            raise ValueError("Consumer taxa not supported")
        if resource not in TAXA_OF_INTEREST:
            raise ValueError("Resource taxa not supported")

        return species, consumer, resource

    def filter_by_dataset_id(self, dIds):
        self.validateDIds(dIds)
        self.logbook.append({"datasetIdFilter": dIds})
        newWeb = self.replicateWeb()
        newWeb.datasetMetas = filterDatasetByDIds(self.datasetMetas, dIds)
        newWeb.linkMetas = filterLinksMetasByDIds(self.linkMetas, dIds)
        newWeb.interactions = filterInteractionsByLinkIds(
            self.interactions, newWeb.linkMetas
        )
        newWeb.stringNames = filterStringNamesByInteractions(
            self.stringNames, newWeb.interactions
        )
        newWeb.taxa = filterNoLongerNeededTaxa(self.taxa, newWeb.stringNames)
        return newWeb

    def validateDIds(self, dIds):
        if not all(isinstance(x, int) for x in dIds):
            raise ValueError("Dataset IDs must be integers!")

    def validateObsType(self, obs):
        if not all(isinstance(x, str) for x in obs):
            raise ValueError("Observation type is a string!")

    def validateInteractionType(self, obs):
        if not all(isinstance(x, str) for x in obs):
            raise ValueError("Interaction type is a string!")

    def validateLocType(self, loc):
        if not all(isinstance(x, str) for x in loc):
            raise ValueError("Location is a string!")

    def validateTaxaConstraints(self, listOfTaxaConstraints):
        if not all(map(self.isValidTaxaConstraint, listOfTaxaConstraints)):
            raise ValueError("Malformed Taxa Specification!")

    def isValidTaxaConstraint(self, taxaConstraintTuple):
        name, level = taxaConstraintTuple
        if not isinstance(name, str):
            return False
        if level not in TAXA_OF_INTEREST:
            return False

        return True

    def standardiseCountries(self, loc):
        newCountries = []
        for item in loc:
            try:
                newCountries.append(pycountry.countries.search_fuzzy(item)[0].name)
            except BaseException:
                raise ValueError("Country not recognised")

        return newCountries

    def filter_by_observation_type(self, obs, strict=False):
        self.validateObsType(obs)
        self.logbook.append({"observationFilter": obs})
        newWeb = self.filterOnMetaData(obs, strict, filterMetasByObs)
        return newWeb

    def filter_by_interaction_type(self, interactionTypes, strict=False):
        self.validateInteractionType(interactionTypes)
        self.logbook.append({"interactionFilter": interactionTypes})
        newWeb = self.filterOnMetaData(
            interactionTypes, strict, filterMetasByInteraction
        )
        return newWeb

    def filter_by_country(self, loc, strict=False):
        self.validateLocType(loc)
        loc = self.standardiseCountries(loc)
        self.logbook.append({"countryFilter": loc})
        newWeb = self.filterOnMetaData(loc, strict, filterMetasByCountry)
        return newWeb

    def filterOnMetaData(self, acceptedList, strict, callHandler):
        newLinkMetas, newDatasetMetas = callHandler(
            self.linkMetas, acceptedList, self.datasetMetas, strict
        )

        newWeb = self.replicateWeb()
        newWeb.linkMetas = newLinkMetas
        newWeb.datasetMetas = newDatasetMetas
        newWeb.interactions = filterInteractionsByLinkIds(
            self.interactions, newWeb.linkMetas
        )
        newWeb.stringNames = filterStringNamesByInteractions(
            self.stringNames, newWeb.interactions
        )
        newWeb.taxa = filterNoLongerNeededTaxa(self.taxa, newWeb.stringNames)
        return newWeb

    def filterByTaxa(self, taxaConstraints):
        self.validateTaxaConstraints(taxaConstraints)
        self.logbook.append({"taxaConstraint": taxaConstraints})
        newWeb = self.replicateWeb()
        newWeb.stringNames = filterStringNamesByTaxaConstraints(
            self.stringNames, taxaConstraints, self.taxa
        )
        newWeb.taxa = filterUneededTaxa(self.taxa, newWeb.stringNames)
        newWeb.interactions = filterInvalidInteractions(
            self.interactions, newWeb.stringNames
        )
        newWeb.linkMetas = filterInvalidLinks(self.linkMetas, newWeb.interactions)
        return newWeb

    def replicateWeb(self):
        names = [
            "interactions",
            "taxaExceptions",
            "taxa",
            "linkMetas",
            "datasetMetas",
            "stringNames",
            "logbook",
        ]
        newData = list(
            map(
                serialise,
                [
                    self.interactions,
                    self.taxaExceptions,
                    self.taxa,
                    self.linkMetas,
                    self.datasetMetas,
                    self.stringNames,
                    self.logbook,
                ],
            )
        )
        kwargsDict = dict(zip(names, newData))
        return Web(path=self.storePath, **kwargsDict)

    def apply(self, species, taxaGeneralisation="exact"):
        ap = MedeinaCumulativeApplication(self.storePath)
        ap.apply(self, species, taxaGeneralisation)
        ap.summary()
        return ap

    def reIndex(self):
        # essentially load everything again, and apply functions from the
        # logbook
        pass

    def summarise(self):
        print("Current Interaction Web has:")
        print(str(len(self.linkMetas)) + " interactions")
        print(str(len(self.stringNames)) + " unique species")

    def sayHelloMedeina(self):
        print("Hello")
