
from config import *
import pickle
from os import path
import pathlib
import pandas as pd
from collections import defaultdict
import requests
import itertools
import operator 

def saveNewData(parsedSpecificationString):
    dataPath = parsedSpecificationString['path']
    graphType = parsedSpecificationString['encoding']
    interactionFormat = graphType['interactionFormat']

    interactionType = parsedSpecificationString['interactionType']
    dId = createNewDatasetRecord(interactionType)

    if interactionFormat == "pair":
        handlePairwiseInteractions(dataPath,graphType['head'],graphType['tail'],dId)

def handlePairwiseInteractions(dataPath,head,tail,dId):
    df = readPairwiseContentAsDataFrame(dataPath)
    predators = assignUniqueIdsToSpecies(df[head].values.tolist())
    prey = assignUniqueIdsToSpecies(df[tail].values.tolist())
    
    writeInteractionsToDataStore(predators,prey,dId)
    writeTaxonomicInformation(predators)
    writeTaxonomicInformation(prey)

def readPairwiseContentAsDataFrame(dataPath):
    fileType = (pathlib.Path(dataPath).suffix[1:]) 
    data = []
    if fileType == 'csv':
        data = pd.read_csv(dataPath,engine='python')
    
    data = cleanData(data)
    return data

def cleanData(data):
    return data # get names standardised

def assignUniqueIdsToSpecies(species):
    with open(f'{BASEDIR}/{REALNAMES}','rb') as f:
        stringNames = pickle.load(f)

    changeDetected = False    
    idList = []
    for s in species:
        if s in stringNames:
            idList.append(stringNames[s])
        else:
            changeDetected = True
            stringNames[s] = len(stringNames) + 1
            idList.append(stringNames[s])
    
    with open(f'{BASEDIR}/{REALNAMES}','wb') as fh:
        pickle.dump(stringNames,fh)
    
    return idList

def writeInteractionsToDataStore(predators,prey,dId):
    with open(f'{BASEDIR}/{WEB}','rb') as f:
        existingWeb = pickle.load(f)
    
    with open(f'{BASEDIR}/{LINKS}','rb') as f:
        existingLinks = pickle.load(f)

    currentLinkId = existingWeb[IDTRACKER]
    for i in range(len(predators)):
        if predators[i] not in existingWeb:
            existingWeb[predators[i]] = defaultdict(list)
        
        ((existingWeb[predators[i]])[prey[i]]).append(currentLinkId)
        existingLinks[currentLinkId] = [dId]
        currentLinkId += 1
    
    existingWeb[IDTRACKER] = currentLinkId
    with open(f'{BASEDIR}/{WEB}','wb') as f:
        pickle.dump(existingWeb,f) 
    
    with open(f'{BASEDIR}/{LINKS}','wb') as f:
        pickle.dump(existingLinks,f) 

def writeTaxonomicInformation(species):
    politenessLimiter = 100

    toProcess, existingTaxaData, stringNameMapper = determineTaxonomicGaps(species)
    for i in range(0,len(toProcess),politenessLimiter):
        print("Indexing records " + str(i) + " to " + str(min(len(toProcess),i+politenessLimiter)) + " [of "+str(len(toProcess))+"]")
        apiString = "|".join(toProcess[i:i+politenessLimiter])
        url = "http://resolver.globalnames.org/name_resolvers.json"
        callToValidateName = requests.get(f'{url}?names={apiString}')
        jsonRes = callToValidateName.json()['data']

        for individualResult in jsonRes:
            if individualResult['is_known_name']:
                sId = stringNameMapper[individualResult['supplied_name_string']]
                existingTaxaData[sId] = (parseSingleTaxonomyFromAPI(individualResult))
            else:
                print("Could not index " + str(individualResult['supplied_name_string']))
                if 'results' in individualResult:
                    try:
                        print("Did you mean " + str(individualResult['results'][0]['canonical_form']))
                    except: pass
                     
    with open(f'{BASEDIR}/{TAXA}','wb') as f:
        pickle.dump(existingTaxaData,f)
    
def determineTaxonomicGaps(species):
    with open(f'{BASEDIR}/{TAXA}','rb') as f:
        existingTaxaData = pickle.load(f)
    
    with open(f'{BASEDIR}/{REALNAMES}','rb') as f:
        stringNameMapper = pickle.load(f)

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
    try:
        mappingDict = dict(zip(singleTaxaSource['classification_path_ranks'].lower().split("|"),singleTaxaSource['classification_path'].lower().split("|")))
    except:
        mappingDict = {}
    return mappingDict

def runConsensusForSingleSpecies(individualDictionaryMappings):
    finalMapping = {}
    individualDictionaryMappings = list(individualDictionaryMappings)
    for taxaRank in TAXA_OF_INTEREST:
        allItemsOfTaxa = []
        for singleMapping in individualDictionaryMappings:
            if taxaRank in singleMapping:
                val = singleMapping[taxaRank]
                if len(val) > 0:
                    allItemsOfTaxa.append(val)
        if len(allItemsOfTaxa) == 0:
            finalMapping[taxaRank] = ''
        else:
            finalMapping[taxaRank] = most_common(allItemsOfTaxa)               
    
    return finalMapping

def most_common(L):
  SL = sorted((x, i) for i, x in enumerate(L))
  groups = itertools.groupby(SL, key=operator.itemgetter(0))
  def _auxfun(g):
    item, iterable = g
    count = 0
    min_index = len(L)
    for _, where in iterable:
      count += 1
      min_index = min(min_index, where)
    return count, -min_index
  return max(groups, key=_auxfun)[0]

def createNewDatasetRecord(interactionType):
    with open(f'{BASEDIR}/{DATASETS}','rb') as fh:
        existing = pickle.load(fh)

    newId = len(existing) + 1
    existing[newId] = [interactionType]

    with open(f'{BASEDIR}/{DATASETS}','wb') as fh:
        pickle.dump(existing,fh)
    
    return newId