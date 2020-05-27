from collections import defaultdict
from config import *

def filterDatasetByDIds(datasetObject,dIds):
    dIds = set(dIds)
    return {k:v for k, v in datasetObject.items() if k in dIds}

def filterLinksMetasByDIds(linkMetas,dIds):
    dIds = set(dIds)
    return {k:v for k, v in linkMetas.items() if v['dId'] in dIds} 

def filterInteractionsByDIds(dict_,linkMetas):
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

def filterStringNamesByDIds(speciesStringDict,interactionDict):
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
