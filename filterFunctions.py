from collections import defaultdict
from config import *

### Dataset ID
#########################################################################

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
    for predator in dict_:
        for prey in dict_[predator]:
            newAddition = list(filter(lambda x: x in linkMetas,dict_[predator][prey]))
            if len(newAddition) != 0:
                if predator not in newInteractions: newInteractions[predator] = defaultdict(list)
                newInteractions[predator][prey].extend(newAddition)
    
    newInteractions[IDTRACKER] = tmp
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

### Observation Types
#########################################################################

def filterLinkMetasByObs(linkMetas,obs,datasetMetas,strict):
    obs = set(obs)
    unaccountedFor = []
    newLinks = {}
    for key,val in linkMetas.items():
        if 'evidencedBy' not in val:
            unaccountedFor.append(key)
        else:
            for x in obs:
                if val['evidencedBy'] == x:
                    newLinks[key] = val 
                    break

    stillUnnacountedFor = []
    for link in unaccountedFor:
        linkMetaSingle = linkMetas[link]
        indivDId = linkMetaSingle['dId']

        if 'evidencedBy' not in datasetMetas[indivDId]:
            stillUnnacountedFor.append(link)
        else:
            for x in obs:
                if datasetMetas[indivDId]['evidencedBy'] == x:
                    newLinks[link] = linkMetaSingle 
                    break

    if strict: return newLinks

    for link in stillUnnacountedFor:
        vali = linkMetas[link]
        newLinks[link] = vali

    return newLinks

def filterDatasetMetasByObs(datasetMetas,strict,obs):
    newDataSetMetas = {}
    unaccountedFor = []
    for key,val in datasetMetas.items():
        if 'evidencedBy' not in val:
            unaccountedFor.append(key)
        else:
            for x in obs:
                if val['evidencedBy'] == x:
                    newDataSetMetas[key] = val 
                    break
    
    if strict: return newDataSetMetas

    for link in unaccountedFor:
        vali = datasetMetas[link]
        newDataSetMetas[link] = vali
    
    return newDataSetMetas



def crushInteractionDict(dict_):
    species = set()
    del dict_[IDTRACKER]
    for predator in dict_:
        species.add(predator)
        for prey in dict_[predator]:
            species.add(prey)
    
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

