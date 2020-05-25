import pathlib
import pandas as pd
from dataCleaning import cleanHeadTailTupleData
from config import LINK_METAS
import re

def parseSpeciesInteractionCells(parsedSpecificationString):
    graphType = parsedSpecificationString['encoding']
    stringPairs = runAppropriateHandlerMethod(graphType)
    stringPairs = cleanHeadTailTupleData(stringPairs)
    return stringPairs

def runAppropriateHandlerMethod(graphType):
    interactionFormat = graphType['interactionFormat']
    dataPath = graphType['path']
    stringPairs = []
    if interactionFormat == "pair":
        stringPairs = formatPairData(graphType)
    elif interactionFormat == "matrix":
        stringPairs = formatMatrixData(graphType)
    
    return stringPairs
    
def formatPairData(graphType):
    df = readContentAsDataFrame(graphType['path'])
    predators = df[graphType['head']].values.tolist()
    prey = df[graphType['tail']].values.tolist()
    metas = retrieveUserProvidedPairMetaData(df,graphType)
    consumableData = list(zip(predators,prey,metas))
    return consumableData

def retrieveUserProvidedPairMetaData(df, graphType):
    df['metas'] = df.apply(lambda x: {item: x[graphType[item]] for item in LINK_METAS if item in graphType},axis=1)
    return df['metas'].values.tolist()

def formatMatrixData(graphType):
    df = readContentAsDataFrame(graphType['path'],header=None) 
    headingCoord = parseStringToTuple(graphType.get('headingCorner','(1,1)'))
    dataCoord = parseStringToTuple(graphType.get('dataCorner','(2,2)'))
    dataMatrix = handleData(dataCoord, df).values.tolist()
    predators = handlePredatorData(dataCoord,headingCoord,df).values.tolist()
    predators = list(map(safeJoin,predators))
    prey = handlePreyData(dataCoord,headingCoord,df).values.tolist()
    prey = crushMultiRow(prey)
    consumableData = createPairDataFromMatrix(dataMatrix,predators,prey)    
    return consumableData

def crushMultiRow(multiHeadings):
    return list(map(safeJoin,list(zip(*multiHeadings))))

def safeJoin(listOfNames):
    filterNone = list(filter(lambda x: isinstance(x,str), listOfNames))
    return " ".join(filterNone)

def handleData(dataCoord,df):
    x,y = dataCoord
    return df.iloc[y:,x:]

def handlePredatorData(dataCoord, headingCoord, df):
    start = headingCoord[0]
    length = dataCoord[0] - headingCoord[0]

    offsetY = dataCoord[1] - headingCoord[1]
    return df.iloc[headingCoord[1]+offsetY:,start:start+length]

def handlePreyData(dataCoord, headingCoord, df):
    start = headingCoord[1]
    length = dataCoord[1] - headingCoord[1]

    offsetX = dataCoord[0] - headingCoord[0]
    return df.iloc[start:start+length,headingCoord[0]+offsetX:]

def parseStringToTuple(coord):
    if not bool(re.match('^\([\d]+,[\d]+\)$',coord)):
        raise ValueError("Incorrectly formatted index rows!")
    
    coord = coord.strip(")").strip("(")
    x,y = coord.split(",")
    return (int(x)-1,int(y)-1)

def createPairDataFromMatrix(dataMatrix,predators,prey):
    assert len(predators) == len(dataMatrix)
    assert len(prey) == len(dataMatrix[0])
    consumableData = []
    for i in range(len(predators)):
        for j in range(len(prey)):
            if dataMatrix[i][j] != 0: 
                consumableData.append((predators[i],prey[j],{}))
    return consumableData

def readContentAsDataFrame(dataPath,header='infer'):
    fileType = (pathlib.Path(dataPath).suffix[1:]) 
    data = []
    if fileType == 'csv':
        data = pd.read_csv(dataPath,engine='python',header=header)
    elif 'xls' in fileType:
        data = pd.read_excel(dataPath,header=header)
        data = data.dropna(axis=1, how='all')

    data = data.dropna(axis=1, how='all')
    return data
