import pathlib
import pandas as pd
from dataCleaning import cleanHeadTailTupleData
from config import LINK_METAS

def parseSpeciesInteractionCells(parsedSpecificationString):
    graphType = parsedSpecificationString['encoding']
    interactionFormat = graphType['interactionFormat']
    dataPath = graphType['path']

    stringPairs = []
    if interactionFormat == "pair":
        stringPairs = formatPairData(graphType)
    
    return cleanHeadTailTupleData(stringPairs)
    
def formatPairData(graphType):
    df = readPairwiseContentAsDataFrame(graphType['path'])

    predators = df[graphType['head']].values.tolist()
    prey = df[graphType['tail']].values.tolist()
    metas = retrieveUserProvidedMetaData(df,graphType)

    consumableData = list(zip(predators,prey,metas))
    return consumableData

def retrieveUserProvidedMetaData(df, graphType):
    df['metas'] = df.apply(lambda x: {item: x[graphType[item]] for item in LINK_METAS if item in graphType},axis=1)
    return df['metas'].values.tolist()

def readPairwiseContentAsDataFrame(dataPath):
    fileType = (pathlib.Path(dataPath).suffix[1:]) 
    data = []
    if fileType == 'csv':
        data = pd.read_csv(dataPath,engine='python')
    return data
