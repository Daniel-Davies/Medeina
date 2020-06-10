from config import *
import pickle
from os import path
import pathlib
from collections import defaultdict
import requests
import itertools
import operator 
from common import writeObjToDateStore, retrieveObjFromStore, mostCommonInList
from dataFormatReaders import parseSpeciesInteractionCells
import pycountry

def saveNewData(parsedSpecificationString):
    dId = createNewDatasetRecord(parsedSpecificationString)
    stringHeadTailData = parseSpeciesInteractionCells(parsedSpecificationString) 
    standardHeadTailData = storeSpeciesData(stringHeadTailData,parsedSpecificationString['storageLocation'],parsedSpecificationString['includeInvalid'])
    writeInteractionLinks(standardHeadTailData,dId,parsedSpecificationString['storageLocation'])

def createNewDatasetRecord(parsedSpecificationString):
    datasetMeta = takeDatasetMetaData(parsedSpecificationString)
    existing = retrieveObjFromStore(parsedSpecificationString['storageLocation'], DATASETS)
    newId = len(existing) + 1
    existing[newId] = datasetMeta
    writeObjToDateStore(parsedSpecificationString['storageLocation'],DATASETS,existing)
    return newId

def storeSpeciesData(stringHeadTailData,directory,includeInvalid):
    headTailOnly = keepInteractionPartOnly(stringHeadTailData)
    speciesMapping = assignAndStoreUniqueIdsOfSpecies(itertools.chain(*headTailOnly),directory,includeInvalid)
    return list(map(lambda x: (speciesMapping[x[0]], speciesMapping[x[1]], x[2]),filter(lambda x: verifyValidInteraction(speciesMapping,x), stringHeadTailData)))

def verifyValidInteraction(speciesMapping,indivSpeciesInteraction):
    head,tail,meta = indivSpeciesInteraction
    return head in speciesMapping and tail in speciesMapping

def keepInteractionPartOnly(headTailDataWMeta):
    return list(map(lambda tup: (tup[0],tup[1]),headTailDataWMeta))

def writeInteractionLinks(consumableData,dId,directory):
    existingWeb = retrieveObjFromStore(directory,WEB)
    existingLinks = retrieveObjFromStore(directory,LINKS)
    currentLinkId = existingWeb[IDTRACKER]

    for predator, prey, meta in consumableData:
        if predator not in existingWeb: existingWeb[predator] = defaultdict(list)
        
        existingWeb[predator][prey].append(currentLinkId)
        existingLinks[currentLinkId] = processLinkMetaData(meta,dId)
        currentLinkId += 1
    
    existingWeb[IDTRACKER] = currentLinkId
    writeObjToDateStore(directory, WEB, existingWeb)
    writeObjToDateStore(directory, LINKS, existingLinks)

def processLinkMetaData(meta,dId):
    meta['dId'] = dId
    if 'location' in meta: meta['location'] = standardiseLocationData(meta['location'])
    return meta

def callAPIOnDataList(speciesNamesList):
    apiString = "|".join(speciesNamesList)
    callToValidateNames = requests.get(f'{APIURL}?names={apiString}')
    return callToValidateNames.json()['data']

def warnSpeciesNameFailure(individualResult):
    print("Could not index " + str(individualResult['supplied_name_string']))

def assignAndStoreUniqueIdsOfSpecies(species,directory,includeInvalid=False):
    validSpecies = getTaxaAndValidateNewNames(species,directory,includeInvalid)
    if len(validSpecies) > 0: 
        stringNames = addSpeciesToStringNameMapping(validSpecies,directory)
        writeTaxonomicInformation(validSpecies,directory,stringNames)
    return retrieveObjFromStore(directory,REALNAMES)

def addSpeciesToStringNameMapping(validSpecies,directory):
    stringNames = retrieveObjFromStore(directory,REALNAMES)
    for name,valid,taxa in validSpecies: stringNames[name] = len(stringNames) + 1
    writeObjToDateStore(directory, REALNAMES, stringNames)
    return stringNames

def writeTaxonomicInformation(validSpeciesResponses,directory,stringNameMapper):
    existingTaxaData = retrieveObjFromStore(directory,TAXA)
    validSpeciesResponses = list(filter(lambda x: x[1],validSpeciesResponses))
    for name,valid,taxaDict in validSpeciesResponses:
        sId = stringNameMapper[name]
        existingTaxaData[sId] = taxaDict
    writeObjToDateStore(directory, TAXA, existingTaxaData)

def getTaxaAndValidateNewNames(allSpeciesFound,directory,includeInvalid):
    speciesToProcess = determineTaxonomicGaps(allSpeciesFound,directory)
    for i in range(0,len(species),APIMAX):
        print("Indexing records " + str(i) + " to " + str(min(len(species),i+APIMAX)) + " [of "+str(len(species))+"]")
        responses.extend(callAPIOnDataList(species[i:i+APIMAX]))

    speciesResponses = list(map(processSingleResponse,responses))
    if includeInvalid: return speciesResponses
    return list(filter(lambda x: x[1],speciesResponses))

def processSingleResponse(response):
    result = []
    if response['is_known_name']: result = (response['supplied_name_string'], True, parseSingleTaxonomyFromAPI(response))
    result = handleUnknowName(response)
    result[2]['species'] = result[0]
    return result

def handleUnknowName(response):
    if 'results' in response:
        return (response['supplied_name_string'], True, parseSingleTaxonomyFromAPI(response))
    else:
        warnSpeciesNameFailure(response)
        return (response['supplied_name_string'], False, {})
    
def determineTaxonomicGaps(species,directory):
    stringNameMapper = retrieveObjFromStore(directory,REALNAMES)
    return list(set(species) - set(stringNameMapper.keys()))

def parseSingleTaxonomyFromAPI(taxonomicAPIres):
    dataFromMultipleSources = taxonomicAPIres['results']
    dataFromMultipleSources = map(extractTaxaData,dataFromMultipleSources)
    return runConsensusForSingleSpecies(dataFromMultipleSources)
    
def extractTaxaData(singleTaxaSource):
    mappingDict = {}
    try: mappingDict = dict(zip(singleTaxaSource['classification_path_ranks'].lower().split("|"),\
                                singleTaxaSource['classification_path'].lower().split("|")))
    except: pass
    return mappingDict

def runConsensusForSingleSpecies(individualDictionaryMappings):
    finalMapping = {}
    individualDictionaryMappings = list(individualDictionaryMappings)
    for taxaRank in TAXA_OF_INTEREST:
        finalMapping[taxaRank] = runConsensusOnSingleTaxa(taxaRank,individualDictionaryMappings)
        
    return finalMapping

def runConsensusOnSingleTaxa(taxaRank,individualDictionaryMappings):
    allItemsOfTaxa = []
    for singleMapping in individualDictionaryMappings:
        val = singleMapping.get(taxaRank,'')
        if len(val) > 0: allItemsOfTaxa.append(val)
    
    if len(allItemsOfTaxa) == 0: return ''
    return mostCommonInList(allItemsOfTaxa)

def takeDatasetMetaData(parsedSpecificationString):
    joinedMetas = {item: parsedSpecificationString[item] for item in DATASET_METAS if item in parsedSpecificationString}
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