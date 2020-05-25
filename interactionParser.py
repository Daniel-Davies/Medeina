from config import *
import pickle
from os import path
import pathlib
import pandas as pd
from collections import defaultdict
import requests
import itertools
import operator 
from common import writeObjToDateStore, retrieveObjFromStore, mostCommonInList
from dataFormatReaders import parseSpeciesInteractionCells

def saveNewData(parsedSpecificationString):
    dId = createNewDatasetRecord(parsedSpecificationString)
    stringHeadTailData = parseSpeciesInteractionCells(parsedSpecificationString) #(predator,prey,meta)
    standardHeadTailData = createAndStoreSpeciesIds(stringHeadTailData,parsedSpecificationString['storageLocation'])
    writeLinksToDataStore(standardHeadTailData,dId,parsedSpecificationString['storageLocation'])
    writeTaxonomicInformationToDataStore(itertools.chain(*keepInteractionPartOnly(standardHeadTailData)),parsedSpecificationString['storageLocation'])

def createNewDatasetRecord(parsedSpecificationString):
    datasetMeta = takeDatasetMetaData(parsedSpecificationString)
    existing = retrieveObjFromStore(parsedSpecificationString['storageLocation'], DATASETS)
    newId = len(existing) + 1
    existing[newId] = datasetMeta
    writeObjToDateStore(parsedSpecificationString['storageLocation'],DATASETS,existing)
    return newId

def takeDatasetMetaData(parsedSpecificationString):
    return {item: parsedSpecificationString[item] for item in DATASET_METAS if item in parsedSpecificationString}

def createAndStoreSpeciesIds(stringHeadTailData,directory):
    headTailOnly = keepInteractionPartOnly(stringHeadTailData)
    speciesMapping = assignAndStoreUniqueIdsOfSpecies(itertools.chain(*headTailOnly),directory)
    return list(map(lambda x: (speciesMapping[x[0]], speciesMapping[x[1]], x[2]),stringHeadTailData))

def keepInteractionPartOnly(headTailDataWMeta):
    return list(map(lambda tup: (tup[0],tup[1]),headTailDataWMeta))

def writeLinksToDataStore(consumableData,dId,directory):
    existingWeb = retrieveObjFromStore(directory,WEB)
    existingLinks = retrieveObjFromStore(directory,LINKS)
    currentLinkId = existingWeb[IDTRACKER]

    for predator, prey, meta in consumableData:
        if predator not in existingWeb: existingWeb[predator] = defaultdict(list)
        
        existingWeb[predator][prey].append(currentLinkId)
        meta['dId'] = dId
        existingLinks[currentLinkId] = meta
        currentLinkId += 1
    
    existingWeb[IDTRACKER] = currentLinkId
    writeObjToDateStore(directory, WEB, existingWeb)
    writeObjToDateStore(directory, LINKS, existingLinks)

def writeTaxonomicInformationToDataStore(species,directory):
    toProcess, existingTaxaData, stringNameMapper = determineTaxonomicGaps(directory,species)
    for i in range(0,len(toProcess),APIMAX):
        print("Indexing records " + str(i) + " to " + str(min(len(toProcess),i+APIMAX)) + " [of "+str(len(toProcess))+"]")
        jsonRes = callAPIOnDataList(toProcess[i:i+APIMAX])
        storeTaxaFromAPI(jsonRes,existingTaxaData,stringNameMapper)      
    writeObjToDateStore(directory, TAXA, existingTaxaData)

def callAPIOnDataList(speciesNamesList):
    apiString = "|".join(speciesNamesList)
    callToValidateNames = requests.get(f'{APIURL}?names={apiString}')
    return callToValidateNames.json()['data']

def storeTaxaFromAPI(jsonRes,existingTaxaData,stringNameMapper):
    for individualResult in jsonRes:
        if individualResult['is_known_name']:
            sId = stringNameMapper[individualResult['supplied_name_string']]
            existingTaxaData[sId] = (parseSingleTaxonomyFromAPI(individualResult))
        else:
            handleSpeciesNameFailure(individualResult)

def handleSpeciesNameFailure(individualResult):
    print("Could not index " + str(individualResult['supplied_name_string']))
    if 'results' in individualResult:
        try: print("Did you mean " + str(individualResult['results'][0]['canonical_form']) + "?")
        except: pass

def assignAndStoreUniqueIdsOfSpecies(species,directory):
    stringNames = retrieveObjFromStore(directory,REALNAMES)
    changeDetected = False    
    for s in species:
        if s not in stringNames:
            changeDetected = True
            stringNames[s] = len(stringNames) + 1
    
    if changeDetected: writeObjToDateStore(directory, REALNAMES, stringNames)
    return stringNames
    
def determineTaxonomicGaps(directory,species):
    existingTaxaData = retrieveObjFromStore(directory,TAXA)
    stringNameMapper = retrieveObjFromStore(directory,REALNAMES)
    invStringMapper = {v: k for k, v in stringNameMapper.items()}
    species = list(set(species))
    toProcess = []
    for s in species:
        if s not in existingTaxaData:
            toProcess.append(invStringMapper[s])
    
    return toProcess, existingTaxaData, stringNameMapper

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

    
