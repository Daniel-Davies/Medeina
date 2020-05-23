
from config import *
import pickle
from os import path
import pathlib
import pandas as pd

def saveNewData(parsedSpecificationString):
    graphType = parsedSpecificationString['encoding']
    interactionFormat = graphType['interactionFormat']

    if interactionFormat == "pair":
        return handlePairwiseInteractions(dataPath,graphType['head'],graphType['tail'])


    dataPath = parsedSpecificationString['path']
    interactionType = parsedSpecificationString['interactionType']

    dId = createNewDatasetRecord(interactionType)

def handlePairwiseInteractions(dataPath,dId,head,tail):
    df = readContentAsDataFrame(dataPath)
    predators = df[head].values.tolist()
    prey = df[tail].values.tolist()

def readContentAsDataFrame(dataPath):
    fileType = (pathlib.Path(dataPath).suffix[1:]) 
    data = []
    if fileType == 'csv':
        data = pd.read_csv(dataPath,engine='python')
    
    data = cleanData(data)

def cleanData(data):
    return data

def crushPairListToDict(predators,prey):
    combines = list(zip(predators,prey))


def createNewDatasetRecord(interactionType):
    with open(f'{BASEDIR}/{DATASETS}','rb') as fh:
        existing = pickle.load(fh)

    newId = len(existing) + 1
    existing[newId] = [interactionType]

    with open(f'{BASEDIR}/{DATASETS}','wb') as fh:
        pickle.dump(existing,fh)
    
    return newId