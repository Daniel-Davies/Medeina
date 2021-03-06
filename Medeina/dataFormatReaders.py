import pathlib
import pandas as pd
from .dataCleaning import cleanHeadTailTupleData, cleanSingleSpeciesString
from .config import LINK_METAS, PRECOMPUTER_STORE_PATH
import re
import itertools


def parseSpeciesInteractionCells(parsedSpecificationString):
    graphType = parsedSpecificationString["encoding"]
    stringPairs = collectFromAppropriateHandlerMethod(graphType)
    return stringPairs


def collectFromAppropriateHandlerMethod(graphType):
    interactionFormat = graphType["interactionFormat"]
    dataPath = graphType["path"]
    stringPairs = []
    if interactionFormat == "pair":
        stringPairs = formatPairData(graphType)
    elif interactionFormat == "matrix":
        stringPairs = formatMatrixData(graphType)

    return stringPairs


def formatPairData(graphType):
    try:
        df = readContentAsDataFrame(graphType["path"])
        predators = df[graphType["head"]].values.tolist()
        prey = df[graphType["tail"]].values.tolist()
        metas = retrieveUserProvidedPairMetaData(df, graphType)
        consumableData = list(zip(predators, prey, metas))
        return consumableData
    except Exception as e:
        print(str(e))
        return []


def retrieveUserProvidedPairMetaData(df, graphType):
    expected = set(
        [
            "interactionFormat",
            "headingCorner",
            "dataCorner",
            "head",
            "tail",
            "nameDepth",
            "path",
            "metaData",
        ]
    )
    linkMetas = list(set(graphType.keys()) - expected)
    df["metas"] = df.apply(
        lambda x: {item: x[graphType[item]] for item in linkMetas if item in graphType},
        axis=1,
    )
    return df["metas"].values.tolist()


def formatMatrixData(graphType):
    df = readContentAsDataFrame(graphType["path"], header=None)
    nameDepth = graphType.get("nameDepth", 100)
    headingCoord = parseTupleStringToTuple(graphType.get("headingCorner", "(1,1)"))
    dataCoord = parseTupleStringToTuple(graphType.get("dataCorner", "(2,2)"))
    dataMatrix = handleData(dataCoord, df).values.tolist()
    predators = extractPredatorsFromFile(dataCoord, headingCoord, df, nameDepth)
    metaPredators = extractColBasedMetadata(graphType, df, dataCoord)
    prey = extractPreyFromFile(dataCoord, headingCoord, df, nameDepth)
    metaPrey = extractRowBasedMetadata(graphType, df, dataCoord)
    return createPairDataFromMatrix(
        dataMatrix, predators, prey, metaPredators, metaPrey
    )


def readContentAsDataFrame(dataPath, header="infer"):
    fileType = pathlib.Path(dataPath).suffix[1:]
    data = []
    if fileType == "csv":
        data = pd.read_csv(dataPath, engine="python", header=header)
    elif "xls" in fileType:
        data = pd.read_excel(dataPath, header=header)
        data = data.dropna(axis=1, how="all")

    data = data.dropna(axis=1, how="all")
    data = data.dropna(axis=0, how="all")
    return data


def extractRowBasedMetadata(graphType, df, dataCoord):
    return processMatrixMetaDataAtOrientation(
        graphType,
        "row",
        lambda x: (x[0], df.iloc[x[1], :].values.tolist()),
        dataCoord[0],
    )


def extractColBasedMetadata(graphType, df, dataCoord):
    return processMatrixMetaDataAtOrientation(
        graphType,
        "col",
        lambda x: (x[0], df.iloc[:, x[1]].values.tolist()),
        dataCoord[1],
    )


def processMatrixMetaDataAtOrientation(graphType, orientation, processFn, startOfData):
    userProvidedColData = list(
        filter(lambda x: x["orientation"] == orientation, graphType.get("metaData", []))
    )
    userProvidedColData = list(
        map(lambda x: (x["name"], int(x["index"]) - 1), userProvidedColData)
    )
    valuesOfInterest = list(map(processFn, userProvidedColData))
    nonNullOrIrrelevantRows = list(
        map(lambda x: (x[0], x[1][startOfData:]), valuesOfInterest)
    )
    return nonNullOrIrrelevantRows


def extractPredatorsFromFile(dataCoord, headingCoord, df, nameDepth):
    predators = handlePredatorData(dataCoord, headingCoord, df).values.tolist()
    predators = list(map(lambda x: x[:nameDepth], predators))
    predators = list(map(safeJoin, predators))
    return predators


def extractPreyFromFile(dataCoord, headingCoord, df, nameDepth):
    prey = handlePreyData(dataCoord, headingCoord, df).values.tolist()
    prey = crushMultiRow(prey)
    prey = list(map(lambda x: x[:nameDepth], prey))
    prey = list(map(safeJoin, prey))
    return prey


def crushMultiRow(multiHeadings):
    return list(zip(*multiHeadings))


def safeJoin(listOfNames):
    filterNone = list(filter(lambda x: isinstance(x, str), listOfNames))
    return " ".join(filterNone)


def handleData(dataCoord, df):
    x, y = dataCoord
    return df.iloc[y:, x:]


def handlePredatorData(dataCoord, headingCoord, df):
    start = headingCoord[0]
    length = dataCoord[0] - headingCoord[0]

    offsetY = dataCoord[1] - headingCoord[1]
    return df.iloc[headingCoord[1] + offsetY :, start : start + length]


def handlePreyData(dataCoord, headingCoord, df):
    start = headingCoord[1]
    length = dataCoord[1] - headingCoord[1]

    offsetX = dataCoord[0] - headingCoord[0]
    return df.iloc[start : start + length, headingCoord[0] + offsetX :]


def parseTupleStringToTuple(coord):
    if not bool(re.match(r"^\([\d]+,[\d]+\)$", coord)):
        raise ValueError("Incorrectly formatted index rows!")

    coord = coord.strip(")").strip("(")
    x, y = coord.split(",")
    return (int(x) - 1, int(y) - 1)


def createPairDataFromMatrix(dataMatrix, predators, prey, metaPredators, metaPrey):
    assert len(predators) == len(dataMatrix)
    assert len(prey) == len(dataMatrix[0])
    consumableData = []
    for i in range(len(predators)):
        for j in range(len(prey)):
            handle = dataMatrix[i][j]
            if not (isinstance(handle, int) or isinstance(handle, float)):
                handle = int(float(re.sub("[^0-9]+", "", dataMatrix[i][j])))
            if handle != 0:
                consumableData.append(
                    (
                        predators[i],
                        prey[j],
                        mergeRowColMetadataDicts(metaPredators, metaPrey, i, j),
                    )
                )
    return consumableData


def mergeRowColMetadataDicts(metaPredators, metaPrey, predIndex, preyIndex):
    individualPredatorMetas = list(
        map(lambda x: {x[0]: x[1][predIndex]}, metaPredators)
    )
    individualPreyMetas = list(map(lambda x: {x[0]: x[1][preyIndex]}, metaPrey))
    predatorMetasAsSingeDict = {
        k: v for d in individualPredatorMetas for k, v in d.items()
    }
    preyMetasAsSingleDict = {k: v for d in individualPreyMetas for k, v in d.items()}
    return {**predatorMetasAsSingeDict, **preyMetasAsSingleDict}
