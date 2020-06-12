from EcoNameTranslator import EcoNameTranslator
import requests
from .parsingFunctionality import *
import itertools
from .config import *
from .common import mostCommonInList

#########Translation

def translateToSpeciesScientificFormatOnly(cleanedHeadTailTupleData):
    speciesList = list(set(itertools.chain(*keepInteractionPartOnly(cleanedHeadTailTupleData))))
    speciesMapping = EcoNameTranslator().translate(speciesList)
    cleanedHeadTailTupleData = map(lambda x: \
                                    (speciesMapping[x[0]][1], speciesMapping[x[1]][1],x[2]), \
                                    cleanedHeadTailTupleData \
                               )
    cleanedHeadTailTupleData = map(lambda x: \
                                    (list(itertools.product(x[0],x[1])),x[2]), \
                                    cleanedHeadTailTupleData \
                               )
    cleanedHeadTailTupleData = map(lambda x: 
                                    [(pred,prey,x[1]) for pred,prey in x[0]], \
                                    cleanedHeadTailTupleData \
                               )
    cleanedHeadTailTupleData = list(itertools.chain(*cleanedHeadTailTupleData))
    cleanedHeadTailTupleData = makeUnique(cleanedHeadTailTupleData)
    return cleanedHeadTailTupleData

####GNR-Indexing

def retrieveTaxonomicDataFromAPI(species,includeInvalid):
    responses = []
    for i in range(0,len(species),APIMAX):
        print("Indexing records " + str(i) + " to " + str(min(len(species),i+APIMAX)) + " [of "+str(len(species))+"]")
        responses.extend(callAPIOnDataList(species[i:i+APIMAX]))

    speciesResponses = list(map(processSingleResponse,responses))
    if includeInvalid: return speciesResponses
    return list(filter(lambda x: x[1],speciesResponses))

def processSingleResponse(response):
    result = []
    if response['is_known_name']: 
        result = (response['supplied_name_string'].lower(), True, parseSingleTaxonomyFromAPI(response))
    else:
        result = handleUnknowName(response)
    result[2]['species'] = result[0]
    return result

def handleUnknowName(response):
    if 'results' in response and len(response['results']) > 0:
        return (response['supplied_name_string'].lower(), True, parseSingleTaxonomyFromAPI(response))
    else:
        warnSpeciesNameFailure(response)
        return (response['supplied_name_string'].lower(), False, {})

def callAPIOnDataList(speciesNamesList):
    speciesNamesList = list(map(lambda x: x.capitalize(),speciesNamesList))
    apiString = "|".join(speciesNamesList)
    callToValidateNames = requests.get(f'{APIURL}?names={apiString}')
    return callToValidateNames.json()['data']

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

def warnSpeciesNameFailure(individualResult):
    print("Could not index " + str(individualResult['supplied_name_string']))
