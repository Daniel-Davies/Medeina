import pathlib
import pandas as pd
from dataCleaning import cleanHeadTailTupleData

def handleFormatSpecificData(parsedSpecificationString):
    dataPath = parsedSpecificationString['path']
    graphType = parsedSpecificationString['encoding']
    interactionFormat = graphType['interactionFormat']

    stringPairs = []
    if interactionFormat == "pair":
        stringPairs = formatPairData(dataPath,graphType['head'],graphType['tail'])
    
    return cleanHeadTailTupleData(stringPairs)
    
def formatPairData(dataPath,head,tail):
    df = readPairwiseContentAsDataFrame(dataPath)
    predators = df[head].values.tolist()
    prey = df[tail].values.tolist()
    consumableData = list(zip(predators,prey))
    return consumableData

def readPairwiseContentAsDataFrame(dataPath):
    fileType = (pathlib.Path(dataPath).suffix[1:]) 
    data = []
    if fileType == 'csv':
        data = pd.read_csv(dataPath,engine='python')
    
    data = cleanData(data)
    return data
