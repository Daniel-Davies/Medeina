
from config import *
import pickle
from os import path
import pathlib
import pandas as pd

def saveNewData(parsedSpecificationString):
    dataPath = parsedSpecificationString['path']
    graphType = parsedSpecificationString['encoding']
    interactionFormat = graphType['interactionFormat']
    if interactionFormat == "pair":
        handlePairwiseInteractions(dataPath,graphType['head'],graphType['tail'])

    # dataPath = parsedSpecificationString['path']
    # interactionType = parsedSpecificationString['interactionType']

    # dId = createNewDatasetRecord(interactionType)

def handlePairwiseInteractions(dataPath,head,tail):
    df = readPairwiseContentAsDataFrame(dataPath)
    predators = assignUniqueIdsToSpecies(df[head].values.tolist())
    prey = assignUniqueIdsToSpecies(df[tail].values.tolist())
    
    writeInteractionsToDataStore(predators,prey)

def readPairwiseContentAsDataFrame(dataPath):
    fileType = (pathlib.Path(dataPath).suffix[1:]) 
    data = []
    if fileType == 'csv':
        data = pd.read_csv(dataPath,engine='python')
    
    data = cleanData(data)
    return data

def cleanData(data):
    return data

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
    
    with open(f'{BASEDIR}/{REALNAMES}','wb') as fh:
        pickle.dump(stringNames,fh)
    
    return idList

def writeInteractionsToDataStore(predators,prey):
    with open(f'{BASEDIR}/{WEB}','rb') as f:
        existingWeb = pickle.load(f)

    for i in range(len(predators)):
        if predators[i] not in existingWeb:
            existingWeb[predators[i]] = set()
        
        existingWeb[predators[i]].add(prey[i])

def createNewDatasetRecord(interactionType):
    with open(f'{BASEDIR}/{DATASETS}','rb') as fh:
        existing = pickle.load(fh)

    newId = len(existing) + 1
    existing[newId] = [interactionType]

    with open(f'{BASEDIR}/{DATASETS}','wb') as fh:
        pickle.dump(existing,fh)
    
    return newId