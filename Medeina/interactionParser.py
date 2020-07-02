from .config import *
import itertools
import operator 
from .common import *
from .parsingFunctionality import *
from .dataFormatReaders import parseSpeciesInteractionCells
import pycountry
from .dataCleaning import cleanHeadTailTupleData
from .externalAPIs import translateToSpeciesScientificFormatOnly, retrieveTaxonomicDataFromAPI

def saveNewData(parsedSpecificationString):
    dId = createNewDatasetRecord(parsedSpecificationString)
    stringHeadTailData = parseSpeciesInteractionCells(parsedSpecificationString) 
    stringHeadTailData = makeUnique(stringHeadTailData)
    stringHeadTailData = translateToSpeciesScientificFormatOnly(stringHeadTailData)
    stringHeadTailData = cleanHeadTailTupleData(stringHeadTailData)
    speciesMappingToId = indexTranslatedSpecies(stringHeadTailData,parsedSpecificationString)
    stringHeadTailData = filterUnindexableSpecies(stringHeadTailData,speciesMappingToId,parsedSpecificationString)
    writeInteractionLinks(stringHeadTailData,dId,parsedSpecificationString)

def filterUnindexableSpecies(species,speciesMappingToId,parsedSpecificationString):
    directory = parsedSpecificationString['storageLocation']
    includeInvalid = parsedSpecificationString['includeInvalid']
    return  list( \
                map(lambda x: \
                    (speciesMappingToId[x[0]], speciesMappingToId[x[1]], x[2]), \
                    filter(lambda x: \
                        verifyValidInteraction(speciesMappingToId,x), \
                        species \
                    ) \
                ) \
            )

def createNewDatasetRecord(parsedSpecificationString):
    datasetMeta = takeDatasetMetaData(parsedSpecificationString)
    existing = retrieveObjFromStore(parsedSpecificationString['storageLocation'], DATASETS)
    newId = len(existing) + 1
    existing[newId] = datasetMeta
    writeObjToDateStore(parsedSpecificationString['storageLocation'],DATASETS,existing)
    return newId

def writeInteractionLinks(consumableData,dId,parsedSpecificationString):
    directory = parsedSpecificationString['storageLocation']
    existingWeb = retrieveObjFromStore(directory,WEB)
    existingLinks = retrieveObjFromStore(directory,LINKS)
    currentLinkId = existingWeb[IDTRACKER]

    for predator, prey, meta in consumableData:
        if predator not in existingWeb: 
            existingWeb[predator] = {}
        if prey not in existingWeb[predator]:
            existingWeb[predator][prey] = []

        existingWeb[predator][prey].append(currentLinkId)
        existingLinks[currentLinkId] = processLinkMetaData(meta,dId)
        currentLinkId += 1
    
    existingWeb[IDTRACKER] = currentLinkId
    writeObjToDateStore(directory, WEB, existingWeb)
    writeObjToDateStore(directory, LINKS, existingLinks)

def processLinkMetaData(meta,dId):
    meta['dId'] = dId
    return meta

def indexTranslatedSpecies(species,parsedSpecificationString):
    directory = parsedSpecificationString['storageLocation'] 
    includeInvalid = parsedSpecificationString['includeInvalid']
    species = list(set(itertools.chain(*keepInteractionPartOnly(species))))
    validSpecies = getTaxaAndValidateNewNames(species,directory,includeInvalid)
    if len(validSpecies) > 0: 
        stringNames = addSpeciesToStringNameMapping(validSpecies,directory)
        writeTaxonomicInformation(validSpecies,directory,stringNames)
    return retrieveObjFromStore(directory,REALNAMES)

def addSpeciesToStringNameMapping(validSpecies,directory):
    stringNames = retrieveObjFromStore(directory,REALNAMES)
    for name,taxa in validSpecies: stringNames[name] = len(stringNames) + 1
    writeObjToDateStore(directory, REALNAMES, stringNames)
    return stringNames

def writeTaxonomicInformation(validSpeciesResponses,directory,stringNameMapper):
    existingTaxaData = retrieveObjFromStore(directory,TAXA)
    validSpeciesResponses = list(filter(lambda x: x[1],validSpeciesResponses))
    for name,taxaDict in validSpeciesResponses:
        sId = stringNameMapper[name]
        existingTaxaData[sId] = taxaDict
    writeObjToDateStore(directory, TAXA, existingTaxaData)

def getTaxaAndValidateNewNames(allSpeciesFound,directory,includeInvalid):
    species = determineTaxonomicGaps(allSpeciesFound,directory)
    stringToTaxaTuples = retrieveTaxonomicDataFromAPI(species,includeInvalid)
    return stringToTaxaTuples
    
def determineTaxonomicGaps(species,directory):
    stringNameMapper = retrieveObjFromStore(directory,REALNAMES)
    return list(set(species) - set(stringNameMapper.keys()))

def takeDatasetMetaData(parsedSpecificationString):
    expected = set(['storageLocation','graphType'])
    datasetMetas = list(set(parsedSpecificationString.keys()) - expected)
    joinedMetas = {item: parsedSpecificationString[item] for item in datasetMetas}
    if 'location' in joinedMetas: joinedMetas['location'] = standardiseLocationData(joinedMetas['location'])
    return joinedMetas

def standardiseLocationData(location):
    indivLocations = location.split(",")[::-1]
    agg = []
    for item in indivLocations:
        try: agg.append(pycountry.countries.search_fuzzy(x)[0].name)
        except: pass 
    
    country = mostCommonInList(indivLocations)
    return {'region': ",".join(indivLocations[::-1][:-1]), 'country':country}

