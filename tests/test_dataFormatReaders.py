import sys
import os
import pytest
import pandas as pd  
from Medeina.dataFormatReaders import * 

def testConversionOfTupleString():
    assert parseTupleStringToTuple("(1,1)") == (0,0)
    with pytest.raises(ValueError):
        parseTupleStringToTuple("()")
    with pytest.raises(ValueError):
        parseTupleStringToTuple("(1,)")
    with pytest.raises(ValueError):
        parseTupleStringToTuple("(,1)")
    with pytest.raises(ValueError):
        parseTupleStringToTuple("(s,2)")

def testPairMetaExtractionNormal():
    dct = {}
    dct['encoding'] = {}
    dct['encoding']['interactionFormat'] = 'pair'
    dct['encoding']['head'] = 'Predator'
    dct['encoding']['tail'] = 'Prey'
    dct['encoding']['interactionType'] = 'Meta1'
    dct['encoding']['evidencedBy'] = 'Meta2'
    df = pd.DataFrame([['Predator','Prey','Meta1','Meta2'], \
                       ['Pred1', 'Prey1','X1','Y1'], \
                       ['Pred2', 'Prey2','X2','Y2'], \
                       ['Pred3', 'Prey3','X3','Y3'], \
                       ['Pred4', 'Prey4','X4','Y4'], \
                       ['Pred5', 'Prey5','X5','Y5'], \
                      ])
    requiredResults = [{'evidencedBy': 'Y1', 'interactionType': 'X1'}, \
                       {'evidencedBy': 'Y2', 'interactionType': 'X2'}, \
                       {'evidencedBy': 'Y3', 'interactionType': 'X3'}, \
                       {'evidencedBy': 'Y4', 'interactionType': 'X4'}, \
                       {'evidencedBy': 'Y5', 'interactionType': 'X5'}]
    df.columns = df.iloc[0]
    df = df.drop(0,axis=0)

    assert retrieveUserProvidedPairMetaData(df,dct['encoding']) == requiredResults

def testPairMetaExtractionAllBlank():
    dct = {}
    dct['encoding'] = {}
    dct['encoding']['interactionFormat'] = 'pair'
    dct['encoding']['head'] = 'Predator'
    dct['encoding']['tail'] = 'Prey'
    df = pd.DataFrame([['Predator','Prey','Meta1','Meta2'], \
                       ['Pred1', 'Prey1','X1','Y1'], \
                       ['Pred2', 'Prey2','X2','Y2'], \
                       ['Pred3', 'Prey3','X3','Y3'], \
                       ['Pred4', 'Prey4','X4','Y4'], \
                       ['Pred5', 'Prey5','X5','Y5'], \
                      ])
    requiredResults  = [{}] * 5
    df.columns = df.iloc[0]
    df = df.drop(0,axis=0)

def testPairMetaExtractionSomeBlank():
    dct = {}
    dct['encoding'] = {}
    dct['encoding']['interactionFormat'] = 'pair'
    dct['encoding']['head'] = 'Predator'
    dct['encoding']['tail'] = 'Prey'
    dct['encoding']['interactionType'] = 'Meta1'
    dct['encoding']['evidencedBy'] = 'Meta2'
    df = pd.DataFrame([['Predator','Prey','Meta1','Meta2'], \
                       ['Pred1', 'Prey1','',''], \
                       ['Pred2', 'Prey2','X2','Y2'], \
                       ['Pred3', 'Prey3','',''], \
                       ['Pred4', 'Prey4','X4','Y4'], \
                       ['Pred5', 'Prey5','X5','Y5'], \
                      ])
    requiredResults = [{'evidencedBy': '', 'interactionType': ''}, \
                       {'evidencedBy': 'Y2', 'interactionType': 'X2'}, \
                       {'evidencedBy': '', 'interactionType': ''}, \
                       {'evidencedBy': 'Y4', 'interactionType': 'X4'}, \
                       {'evidencedBy': 'Y5', 'interactionType': 'X5'}]
    df.columns = df.iloc[0]
    df = df.drop(0,axis=0)

    assert retrieveUserProvidedPairMetaData(df,dct['encoding']) == requiredResults

def testPairMetaExtractionMissing():
    dct = {}
    dct['encoding'] = {}
    dct['encoding']['interactionFormat'] = 'pair'
    dct['encoding']['head'] = 'Predator'
    dct['encoding']['tail'] = 'Prey'
    dct['encoding']['interactionType'] = 'Meta1'
    dct['encoding']['evidencedBy'] = 'Meta2'
    df = pd.DataFrame([['Predator','Prey','Meta1'], \
                       ['Pred1', 'Prey1','X1','Y1'], \
                       ['Pred2', 'Prey2','X2','Y2'], \
                       ['Pred3', 'Prey3','X3','Y3'], \
                       ['Pred4', 'Prey4','X4','Y4'], \
                       ['Pred5', 'Prey5','X5','Y5'], \
                      ])

    df.columns = df.iloc[0]
    df = df.drop(0,axis=0)

    with pytest.raises(KeyError):
        retrieveUserProvidedPairMetaData(df,dct['encoding'])

def testMergingMetaDicts():
    predatorMetas = [('Meta1',['V','W','X','Y','Z'])]
    preyMetas = [('Meta2',['A','B','C','D','E'])]
    assert mergeRowColMetadataDicts(predatorMetas,preyMetas,2,2) == {'Meta1': 'X', 'Meta2': 'C'}
    assert mergeRowColMetadataDicts(predatorMetas,preyMetas,0,0) == {'Meta1': 'V', 'Meta2': 'A'}
    assert mergeRowColMetadataDicts(predatorMetas,preyMetas,4,4) == {'Meta1': 'Z', 'Meta2': 'E'}

def testMergingMetaDicts():
    predatorMetas = [('Meta1',['V','W','X','Y','Z']),('Meta3',['1','2','3','4','5'])]
    preyMetas = [('Meta2',['A','B','C','D','E'])]
    assert mergeRowColMetadataDicts(predatorMetas,preyMetas,2,2) == {'Meta1': 'X', 'Meta2': 'C', 'Meta3':'3'}
    assert mergeRowColMetadataDicts(predatorMetas,preyMetas,0,0) == {'Meta1': 'V', 'Meta2': 'A', 'Meta3':'1'}
    assert mergeRowColMetadataDicts(predatorMetas,preyMetas,4,4) == {'Meta1': 'Z', 'Meta2': 'E', 'Meta3':'5'}

def testMergingMetaDictsOneOnly():
    predatorMetas = [('Meta1',['V','W','X','Y','Z'])]
    preyMetas = []
    assert mergeRowColMetadataDicts(predatorMetas,preyMetas,1,0) == {'Meta1': 'W'}
    assert mergeRowColMetadataDicts(predatorMetas,preyMetas,0,-1) == {'Meta1': 'V'}
    assert mergeRowColMetadataDicts(predatorMetas,preyMetas,4,1000) == {'Meta1': 'Z'}

def testMergingMetaDictsBothBlank():
    predatorMetas = []
    preyMetas = []
    assert mergeRowColMetadataDicts(predatorMetas,preyMetas,1,0) == {}
    assert mergeRowColMetadataDicts(predatorMetas,preyMetas,0,-1) == {}
    assert mergeRowColMetadataDicts(predatorMetas,preyMetas,4,1000) == {}

def testMatrixInteractionDataCreationNormal():
    dataMatrix = [[1,0,1,0,0],[0,0,0,1,0],[1,0,0,0,1],[1,0,0,0,0],[0,0,0,0,0]]
    predators = ['Pred1','Pred2','Pred3','Pred4','Pred5']
    prey = ['Prey1','Prey2','Prey3','Prey4','Prey5']
    predatorMetas = [('Meta1',['V','W','X','Y','Z'])]
    preyMetas = []

    expectedResults = [('Pred1', 'Prey1', {'Meta1': 'V'}), ('Pred1', 'Prey3', {'Meta1': 'V'}), ('Pred2', 'Prey4', {'Meta1': 'W'}), ('Pred3', 'Prey1', {'Meta1': 'X'}), ('Pred3', 'Prey5', {'Meta1': 'X'}), ('Pred4', 'Prey1', {'Meta1': 'Y'})]

    assert createPairDataFromMatrix(dataMatrix,predators,prey,predatorMetas,preyMetas) == expectedResults

def testMatrixInteractionDataCreationNoMeta():
    dataMatrix = [[1,0,1,0,0],[0,0,0,1,0],[1,0,0,0,1],[1,0,0,0,0],[0,0,0,0,0]]
    predators = ['Pred1','Pred2','Pred3','Pred4','Pred5']
    prey = ['Prey1','Prey2','Prey3','Prey4','Prey5']
    predatorMetas = []
    preyMetas = []

    expectedResults = [('Pred1', 'Prey1', {}), ('Pred1', 'Prey3', {}), ('Pred2', 'Prey4', {}), ('Pred3', 'Prey1', {}), ('Pred3', 'Prey5', {}), ('Pred4', 'Prey1', {})]

    assert createPairDataFromMatrix(dataMatrix,predators,prey,predatorMetas,preyMetas) == expectedResults

def testMatrixInteractionDataCreationUnequalPredPrey():
    dataMatrix = [[1,0,1,0,0],[0,0,0,1,0],[1,0,0,0,1]]
    predators = ['Pred1','Pred2','Pred3']
    prey = ['Prey1','Prey2','Prey3','Prey4','Prey5']
    predatorMetas = []
    preyMetas = []

    expectedResults = [('Pred1', 'Prey1', {}), ('Pred1', 'Prey3', {}), ('Pred2', 'Prey4', {}), ('Pred3', 'Prey1', {}), ('Pred3', 'Prey5', {})]

    assert createPairDataFromMatrix(dataMatrix,predators,prey,predatorMetas,preyMetas) == expectedResults

def testMatrixInteractionDataCreationNonInt():
    dataMatrix = [[1.0,0,1.0,0,0],[0,0,0,1.0,0],[1.0,0,0,0,1.0]]
    predators = ['Pred1','Pred2','Pred3']
    prey = ['Prey1','Prey2','Prey3','Prey4','Prey5']
    predatorMetas = []
    preyMetas = []

    expectedResults = [('Pred1', 'Prey1', {}), ('Pred1', 'Prey3', {}), ('Pred2', 'Prey4', {}), ('Pred3', 'Prey1', {}), ('Pred3', 'Prey5', {})]

    assert createPairDataFromMatrix(dataMatrix,predators,prey,predatorMetas,preyMetas) == expectedResults

def testMatrixInteractionDataCreationHigherNums():
    dataMatrix = [[4.0,0,4.0,0,0],[0,0,0,4,0],[4,0,0,0,4]]
    predators = ['Pred1','Pred2','Pred3']
    prey = ['Prey1','Prey2','Prey3','Prey4','Prey5']
    predatorMetas = []
    preyMetas = []

    expectedResults = [('Pred1', 'Prey1', {}), ('Pred1', 'Prey3', {}), ('Pred2', 'Prey4', {}), ('Pred3', 'Prey1', {}), ('Pred3', 'Prey5', {})]

    assert createPairDataFromMatrix(dataMatrix,predators,prey,predatorMetas,preyMetas) == expectedResults

def testPreyExtraction():
    dataCoord = (1,1)
    headingCoord = (0,0)
    df = pd.DataFrame([['X','Prey1','Prey2','Prey3'], \
                       ['Pred1', '0','0','0'], \
                       ['Pred2', '0','0','0'], \
                       ['Pred3', '0','0','0'], \
                      ])

    preyHeaders = handlePreyData(dataCoord,headingCoord,df).values.tolist() 

    assert preyHeaders == [['Prey1', 'Prey2', 'Prey3']]

def testPreyExtractionMultirow():
    dataCoord = (1,2)
    headingCoord = (0,0)
    df = pd.DataFrame([['X','Prey','Prey','Prey'], \
                       ['X', '1'  , '2' ,  '3'],
                       ['Pred1', '0','0','0'], \
                       ['Pred2', '0','0','0'], \
                       ['Pred3', '0','0','0'], \
                      ])

    preyHeaders = handlePreyData(dataCoord,headingCoord,df).values.tolist() 
    assert preyHeaders == [['Prey', 'Prey', 'Prey'], ['1', '2', '3']]

def testPredExtraction():
    dataCoord = (1,1)
    headingCoord = (0,0)
    df = pd.DataFrame([['X','Prey1','Prey2','Prey3'], \
                       ['Pred1', '0','0','0'], \
                       ['Pred2', '0','0','0'], \
                       ['Pred3', '0','0','0'], \
                      ])

    preyHeaders = handlePredatorData(dataCoord,headingCoord,df).values.tolist() 

    assert preyHeaders == [['Pred1'], ['Pred2'], ['Pred3']]

def testPredExtractionMulticol():
    dataCoord = (2,1)
    headingCoord = (0,0)
    df = pd.DataFrame([['X','X','Prey1','Prey2','Prey3'], \
                       ['Pred','1', '0','0','0'], \
                       ['Pred','2', '0','0','0'], \
                       ['Pred','3', '0','0','0'], \
                      ])

    preyHeaders = handlePredatorData(dataCoord,headingCoord,df).values.tolist() 

    assert preyHeaders == [['Pred','1'], ['Pred','2'], ['Pred','3']]

def testExtractData():
    dataCoord = (1,1)
    df = pd.DataFrame([['X','Prey1','Prey2','Prey3'], \
                       ['Pred1', '0','0','1'], \
                       ['Pred2', '0','1','0'], \
                       ['Pred3', '1','0','0'], \
                      ])
    
    df = handleData(dataCoord,df)
    assert df.values.tolist() == [['0', '0', '1'], ['0', '1', '0'], ['1', '0', '0']]

def testExtractDataUnequal():
    dataCoord = (1,1)
    df = pd.DataFrame([['X','Prey1','Prey2','Prey3','Pred4'], \
                       ['Pred1', '0','0','1','1'], \
                       ['Pred2', '0','1','0','1'], \
                       ['Pred3', '1','0','0','1'], \
                      ])
    
    df = handleData(dataCoord,df)
    assert df.values.tolist() == [['0', '0', '1', '1'], ['0', '1', '0', '1'], ['1', '0', '0', '1']]

def testSafeJoin():
    listOfNames = ['X',None,'Y']
    assert safeJoin(listOfNames) == "X Y"

    listOfNames = ['X']
    assert safeJoin(listOfNames) == "X"

    listOfNames = []
    assert safeJoin(listOfNames) == ""

def testColBasedMetadataExtraction():
    dct = {}
    dct['encoding'] = {}
    dct['encoding']['interactionFormat'] = 'pair'
    dct['encoding']['head'] = 'Predator'
    dct['encoding']['tail'] = 'Prey'
    dct['encoding']['interactionType'] = 'Meta1'
    dct['encoding']['metaData'] = [{'orientation':'col','name':'order','index':1}]

    df = pd.DataFrame([['Meta1','X'    , 'Prey1','Prey2','Prey3'], \
                       ['M1'   ,'Pred1', '0'    ,'0'    ,'0'], \
                       ['M2'   ,'Pred2', '0'    ,'0'    ,'0'], \
                       ['M3'   ,'Pred3', '0'    ,'0'    ,'0'], \
                    ])
    assert extractColBasedMetadata(dct['encoding'],df,(2,1)) == [('order', ['M1', 'M2', 'M3'])]

def testRowBasedMetadataExtraction():
    dct = {}
    dct['encoding'] = {}
    dct['encoding']['interactionFormat'] = 'pair'
    dct['encoding']['head'] = 'Predator'
    dct['encoding']['tail'] = 'Prey'
    dct['encoding']['interactionType'] = 'Meta1'
    dct['encoding']['metaData'] = [{'orientation':'row','name':'order','index':1}]

    df = pd.DataFrame([['X'    , 'M1'   ,'M2'   ,'M3'],
                       ['X'    , 'Prey1','Prey2','Prey3'], \
                       ['Pred1', '0'    ,'0'    ,'0'], \
                       ['Pred2', '0'    ,'0'    ,'0'], \
                       ['Pred3', '0'    ,'0'    ,'0'], \
                    ])
    assert extractRowBasedMetadata(dct['encoding'],df,(1,2)) == [('order', ['M1', 'M2', 'M3'])]

def testMetadataExtractionBlank():
    dct = {}
    dct['encoding'] = {}
    dct['encoding']['interactionFormat'] = 'pair'
    dct['encoding']['head'] = 'Predator'
    dct['encoding']['tail'] = 'Prey'
    dct['encoding']['interactionType'] = 'Meta1'

    df = pd.DataFrame([['X'    , 'Prey1','Prey2','Prey3'], \
                       ['Pred1', '0'    ,'0'    ,'0'], \
                       ['Pred2', '0'    ,'0'    ,'0'], \
                       ['Pred3', '0'    ,'0'    ,'0'], \
                    ])

    assert extractColBasedMetadata(dct['encoding'],df,(1,1)) == []


