from collections import defaultdict
from config import *

def filterDatasetByDIds(datasetObject,dIds):
    dIds = set(dIds)
    return {k:v for k, v in datasetObject.items() if k in dIds}

def filterLinksMetasByDIds(linkMetas,dIds):
    dIds = set(dIds)
    return {k:v for k, v in linkMetas.items() if v['dId'] in dIds} 

def filterInteractionsByLinkIds(dict_,linkMetas):
    newInteractions = {}
    tmp = dict_[IDTRACKER]
    del dict_[IDTRACKER]
    newInteractions[IDTRACKER] = tmp
    newInteractions = createNewInteractionDict(newInteractions,dict_,linkMetas)
    dict_[IDTRACKER] = tmp
    return newInteractions

def createNewInteractionDict(newInteractions,dict_,linkMetas):
    for predator in dict_:
        for prey in dict_[predator]:
            newAddition = list(filter(lambda x: x in linkMetas,dict_[predator][prey]))
            if len(newAddition) != 0:
                if predator not in newInteractions: newInteractions[predator] = defaultdict(list)
                newInteractions[predator][prey].extend(newAddition)
    return newInteractions

def filterStringNamesByInteractions(speciesStringDict,interactionDict):
    speciesSet = crushInteractionDict(interactionDict)
    newSpeciesStringDict = {}
    for k,v in speciesStringDict.items():
        if v in speciesSet:
            newSpeciesStringDict[k] = v
    return newSpeciesStringDict

def filterNoLongerNeededTaxa(taxaObj,stringNames):
    validIds = set(stringNames.values())
    newTaxaObj = {}
    for speciesId in taxaObj:
        if speciesId in validIds:
            newTaxaObj[speciesId] = taxaObj[speciesId]
    
    return newTaxaObj

def filterNoLongerNeededTaxaExceptions(taxaExc,stringNames):
    newTaxaExc = {}
    for name in taxaExc:
        if name in stringNames:
            newTaxaExc[name] = taxaExc[name]
        
    return newTaxaExc

def crushInteractionDict(dict_):
    species = set()
    tmp = dict_[IDTRACKER]
    del dict_[IDTRACKER]
    for predator in dict_:
        species.add(predator)
        for prey in dict_[predator]:
            species.add(prey)
    dict_[IDTRACKER] = tmp
    return species

def countInteractionsInDict(dict_):
    total = 0
    tmp = dict_[IDTRACKER]
    del dict_[IDTRACKER]
    for predator in dict_:
        for prey in dict_[predator]:
            total += len(dict_[predator][prey])
    dict_[IDTRACKER] = tmp
    return total

def filterMetasByObs(linkMetas,obs,datasetMetas,strict):
    newLinks = filterLinkMetaData(linkMetas,datasetMetas,obs,strict,obsGenerator,'evidencedBy')
    newDataset = filterDatasetMetaData(datasetMetas,strict,obs,obsGenerator,'evidencedBy')
    return newLinks, newDataset

def filterMetasByCountry(linkMetas,loc,datasetMetas,strict):
    newLinks = filterLinkMetaData(linkMetas,datasetMetas,loc,strict,locGenerator,'location')
    newDataset = filterDatasetMetaData(datasetMetas,strict,loc,locGenerator,'location')
    return newLinks, newDataset

def filterLinkMetaData(linkMetas,datasetMetas,acceptedList,strict,generator,tag): 
    acceptedList = set(acceptedList)
    newLinks, unaccountedFor = takeMatchingFromLinkMetas(linkMetas,acceptedList,generator,tag)
    newLinks, unaccountedFor = takeMatchingFromDatasetMetas(datasetMetas,newLinks,linkMetas,acceptedList,unaccountedFor,generator,tag)
    if not strict: newLinks = inferRemainingLinks(newLinks,unaccountedFor,linkMetas)
    return newLinks

def filterDatasetMetaData(datasetMetas,strict,acceptedList,generator,tag):
    newDataSetMetas = {}
    unaccountedFor = []
    for key,val in datasetMetas.items():
        if tag not in val: unaccountedFor.append(key)
        elif any(generator(val,acceptedList)): newDataSetMetas[key] = val 
    
    if strict: return newDataSetMetas
    newDataSetMetas = inferRemainingLinks(newDataSetMetas,unaccountedFor,datasetMetas)    
    return newDataSetMetas

def takeMatchingFromLinkMetas(linkMetas,obs,generator,keyName):
    unaccountedFor = []
    newLinks = {}
    for key,val in linkMetas.items():
        if keyName not in val: unaccountedFor.append(key)
        elif any(generator(val,obs)): newLinks[key] = val 

    return newLinks, unaccountedFor

def takeMatchingFromDatasetMetas(datasetMetas,newLinks,linkMetas,acceptedList,unaccountedFor,generator,tag):
    stillUnnacountedFor = []
    for link in unaccountedFor:
        linkMetaSingle = linkMetas[link]
        indivDId = linkMetaSingle['dId']

        if tag not in datasetMetas[indivDId]: stillUnnacountedFor.append(link)
        elif any(locGenerator(datasetMetas[indivDId],acceptedList)): newLinks[link] = linkMetaSingle 

    return newLinks, stillUnnacountedFor

def inferRemainingLinks(newLinks,unaccountedFor,metas):
    for link in unaccountedFor:
        vali = metas[link]
        newLinks[link] = vali
    return newLinks

def obsGenerator(val,obs):
    return (x == val['evidencedBy'] for x in obs)

def locGenerator(val,loc):
    return (x == val['location']['country'] for x in loc)


def filterStringNamesByTaxaConstraints(stringNames,taxaConstraints,taxa):
    newStringNames = {}
    taxaConstraints = convertTaxaConstraintsToFastAccess(taxaConstraints)
    
    for name,sId in stringNames.items():
        speciesTaxa = taxa[sId]
        speciesTaxa['species'] = name
        if matchesConstraints(speciesTaxa,taxaConstraints):
            newStringNames[name] = sId 
        del speciesTaxa['species']
    
    return newStringNames

def filterUneededTaxa(taxa,newSpeciesList):
    newTaxa = {}
    newSpeciesSIds = set(newSpeciesList.values())

    for sId in taxa:
        if sId in newSpeciesSIds:
            newTaxa[sId] = taxa[sId]

    return newTaxa 

def matchesConstraints(speciesTaxa,taxaConstraints):
    for group in taxaConstraints:
        if speciesTaxa[group] in taxaConstraints[group]:
            return True
    return False

def convertTaxaConstraintsToFastAccess(taxaConstraints):
    constraintsByLevel = defaultdict(set)
    for name,level in taxaConstraints:
        constraintsByLevel[level].add(name)

    return constraintsByLevel

def filterInvalidInteractions(interactions,stringNames):
    validSpecies = set(stringNames.values())
    newInteractions = {}

    for predator in interactions:
        if predator in validSpecies:
            newInteractions[predator] = {}
            for prey in interactions[predator]:
                if prey in validSpecies:
                    newInteractions[predator][prey] = (interactions[predator][prey])
            if len(newInteractions[predator]) == 0:
                del newInteractions[predator] 
    return newInteractions

def filterInvalidLinks(linkMetas, interactions):
    validLinkIds = crushInteractionsToIdsOnly(interactions)
    newMetas = {}
    for idx,val in linkMetas.items():
        if idx in validLinkIds:
            newMetas[idx] = val 
    
    return validLinkIds

def crushInteractionsToIdsOnly(interactions):
    idx = []
    for predator in interactions:
        for prey in interactions[predator]:
            idx.extend(interactions[predator][prey])
    
    return set(idx)

