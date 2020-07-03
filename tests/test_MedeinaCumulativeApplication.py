import sys
import os
import pytest
import pandas as pd  
from Medeina.MedeinaCumulativeApplication import MedeinaCumulativeApplication  
from Medeina import Web
from unittest.mock import MagicMock
from mock import patch
from unittest.mock import patch, MagicMock, call, mock_open
import unittest
import networkx as nx
IDTRACKER = 'numericCounter-b2ca94aee362f455a41493a0d28b98bc5074065b0f96cbb95028ead20b1c72ea'

def testBuildingLinkIndex():
    mca = MedeinaCumulativeApplication('dir')
    mca.linkEvidence = {
        ('Spec1','Spec2'): [1,2],
        ('Spec3','Spec4'): [3]
    }
    mca.stringNames = {1:'Spec1',2:'Spec2',3:'Spec3',4:'Spec4'}

    mca.interactionWeb = {IDTRACKER:5, 2:{1:[1,3,5],3:[6]},3:{1:[2]}}
    linkIndex = mca.buildLinkIndex()
    assert linkIndex == {1: ('Spec2', 'Spec1'), 2: ('Spec3', 'Spec1'), 3: ('Spec2', 'Spec1')}
    assert IDTRACKER in mca.interactionWeb

def testHandlingSingleInteractionDataWriting():
    mca = MedeinaCumulativeApplication('dir')
    mca.linkEvidence = {
        ('Spec2','Spec1'): [1,3],
        ('Spec3','Spec1'): [4]
    }
    mca.links = {1:{'dId':2},2:{'dId':1},3:{'dId':1},4:{'dId':2}}
    mca.datasets = {1:{},2:{}}
    mca.stringNames = {1:'Spec1',2:'Spec2',3:'Spec3',4:'Spec4'}
    mca.interactionWeb = {IDTRACKER:5, 2:{1:[1,3],3:[2]},3:{1:[4]}}
    evidencingIDs = [1,3]
    invertedLinkIndex =  mca.buildLinkIndex()
    fileDumpStruct = mca.handleSingleInteractionEvidence(evidencingIDs,invertedLinkIndex,'Spec2','Spec1')
    assert fileDumpStruct == [['Spec2', 'Spec1', 'Spec2', 'Spec1', '', '', '', 2],['Spec2', 'Spec1', 'Spec2', 'Spec1', '', '', '', 1]]

def testHandlingSingleInteractionDataWritingDiffNames():
    mca = MedeinaCumulativeApplication('dir')
    mca.linkEvidence = {
        ('S2','S1'): [1,3],
        ('S3','S1'): [4]
    }
    mca.links = {1:{'dId':2},2:{'dId':1},3:{'dId':1},4:{'dId':2}}
    mca.datasets = {1:{},2:{}}
    mca.stringNames = {1:'Spec1',2:'Spec2',3:'Spec3',4:'Spec4'}
    mca.interactionWeb = {IDTRACKER:5, 2:{1:[1,3],3:[2]},3:{1:[4]}}
    evidencingIDs = [1,3]
    invertedLinkIndex =  mca.buildLinkIndex()
    fileDumpStruct = mca.handleSingleInteractionEvidence(evidencingIDs,invertedLinkIndex,'S2','S1')
    assert fileDumpStruct == [['S2', 'S1', 'Spec2', 'Spec1', '', '', '', 2],['S2', 'S1', 'Spec2', 'Spec1', '', '', '', 1]]

def testHandlingSingleInteractionDataWritingDiffNamesBlank():
    mca = MedeinaCumulativeApplication('dir')
    mca.linkEvidence = {
        ('S2','S1'): [1,3],
        ('S3','S1'): [4]
    }
    mca.links = {1:{'dId':2},2:{'dId':1},3:{'dId':1},4:{'dId':2}}
    mca.datasets = {1:{},2:{}}
    mca.stringNames = {1:'Spec1',2:'Spec2',3:'Spec3',4:'Spec4'}
    mca.interactionWeb = {IDTRACKER:5, 2:{1:[1,3],3:[2]},3:{1:[4]}}
    evidencingIDs = []
    invertedLinkIndex =  mca.buildLinkIndex()
    fileDumpStruct = mca.handleSingleInteractionEvidence(evidencingIDs,invertedLinkIndex,'S2','S1')
    assert fileDumpStruct == []

def testInteractionsToNodes():
    mca = MedeinaCumulativeApplication('dir')
    mca.interactionStore = [('S1','S2'),('S2','S3'),('S2','S2')]
    unittest.TestCase().assertCountEqual(mca.interactionsToNodes(),['S1','S2','S3'])

    mca = MedeinaCumulativeApplication('dir')
    mca.interactionStore = []
    unittest.TestCase().assertCountEqual(mca.interactionsToNodes(),[])

    mca = MedeinaCumulativeApplication('dir')
    mca.interactionStore = [('S2','S2')]
    unittest.TestCase().assertCountEqual(mca.interactionsToNodes(), ['S2'])

def testOutputList():
    mca = MedeinaCumulativeApplication('dir')
    mca.interactionStore = [('Spec1','Spec2'),('Spec2','Spec3'),('Spec3','Spec4'),('Spec1','Spec2'),('Spec5','Spec6')]
    expected = [('Spec1','Spec2'),('Spec2','Spec3'),('Spec3','Spec4'),('Spec5','Spec6')]
    unittest.TestCase().assertCountEqual(mca.to_list(),expected)

def testOutputListWithUserMapping():
    mca = MedeinaCumulativeApplication('dir')
    mca.interactionStore = [('Spec1','Spec2'),('Spec2','Spec3'),('Spec3','Spec4'),('Spec1','Spec2'),('Spec5','Spec6')]
    mca.scientificToUser = {
        'Spec1':'USpec1',
        'Spec2':'USpec2',
        'Spec3':'USpec3',
        'Spec4':'USpec4',
        'Spec5':'USpec5',
        'Spec6':'USpec6'
    }
    expectedOne = [('Spec1','Spec2'),('Spec2','Spec3'),('Spec3','Spec4'),('Spec5','Spec6')]
    expectedTwo = [('USpec1','USpec2'),('USpec2','USpec3'),('USpec3','USpec4'),('USpec5','USpec6')]
    expected = list(zip(expectedOne,expectedTwo))
    unittest.TestCase().assertCountEqual(mca.to_list_original(),expected)

def testOutputGraph():
    def orderTuples(itms):
        return list(map(lambda x: (x[0],x[1]) if x[0] < x[1] else (x[1],x[0]),itms))
    mca = MedeinaCumulativeApplication('dir')
    mca.interactionStore = [('Spec1','Spec2'),('Spec2','Spec3'),('Spec3','Spec4'),('Spec1','Spec2'),('Spec5','Spec6')]
    expected = [('Spec5', 'Spec6'), ('Spec4', 'Spec3'), ('Spec3', 'Spec2'), ('Spec2', 'Spec1')]
    unittest.TestCase().assertCountEqual(orderTuples(mca.to_graph().edges),orderTuples(expected))

def testOutputGraphOriginal():
    def orderTuples(itms):
        return list(map(lambda x: (x[0],x[1]) if x[0] < x[1] else (x[1],x[0]),itms))
    mca = MedeinaCumulativeApplication('dir')
    mca.interactionStore = [('Spec1','Spec2'),('Spec2','Spec3'),('Spec3','Spec4'),('Spec1','Spec2'),('Spec5','Spec6')]
    mca.scientificToUser = {
        'Spec1':'USpec1',
        'Spec2':'USpec2',
        'Spec3':'USpec3',
        'Spec4':'USpec4',
        'Spec5':'USpec5',
        'Spec6':'USpec6'
    }
    expected = [('USpec1','USpec2'),('USpec2','USpec3'),('USpec3','USpec4'),('USpec5','USpec6')]
    unittest.TestCase().assertCountEqual(orderTuples(mca.to_graph_original().edges),orderTuples(expected))

def testOutputMatrix():
    def orderTuples(itms):
        return list(map(lambda x: (x[0],x[1]) if x[0] < x[1] else (x[1],x[0]),itms))
    
    def toHashable(listOfLists):
        return list(map(lambda x: tuple(x),listOfLists))
    mca = MedeinaCumulativeApplication('dir')
    mca.interactionStore = [('Spec1','Spec2'),('Spec2','Spec3'),('Spec3','Spec4'),('Spec1','Spec2'),('Spec5','Spec6')]
    expected = [('Spec5', 'Spec6'), ('Spec4', 'Spec3'), ('Spec3', 'Spec2'), ('Spec2', 'Spec1')]
    matrixOut,labelOrder = mca.to_matrix()
    crushed = []
    matrixOut = matrixOut.tolist()
    for kr,row in enumerate(matrixOut):
        for kc,col in enumerate(row):
            if col == 1:
                crushed.append((labelOrder[kr],labelOrder[kc]))
    crushed = list(set(orderTuples(crushed)))
    unittest.TestCase().assertCountEqual(list(set(orderTuples(mca.interactionStore))),crushed)

def testOutputMatrixOriginal():
    def orderTuples(itms):
        return list(map(lambda x: (x[0],x[1]) if x[0] < x[1] else (x[1],x[0]),itms))
    mca = MedeinaCumulativeApplication('dir')
    mca.interactionStore = [('Spec1','Spec2'),('Spec2','Spec3'),('Spec3','Spec4'),('Spec1','Spec2'),('Spec5','Spec6')]
    mca.scientificToUser = {
        'Spec1':'USpec1',
        'Spec2':'USpec2',
        'Spec3':'USpec3',
        'Spec4':'USpec4',
        'Spec5':'USpec5',
        'Spec6':'USpec6'
    }
    crushed = []
    matrixOut,labelOrder = mca.to_matrix_original()
    matrixOut = matrixOut.tolist()
    for kr,row in enumerate(matrixOut):
        for kc,col in enumerate(row):
            if col == 1:
                crushed.append((labelOrder[kr],labelOrder[kc]))
    crushed = list(set(orderTuples(crushed)))
    expected = [('USpec1','USpec2'),('USpec2','USpec3'),('USpec3','USpec4'),('USpec5','USpec6')]
    unittest.TestCase().assertCountEqual(orderTuples(expected),crushed)

def testStringMappingDecision():
    class TempWebClass:
        def __init__(self):
            self.taxa = {}
            self.stringNames = {}
    WebObj = TempWebClass()
    WebObj.taxa = {
            1:{'family':'felidae'},
            2:{'family':'canidae'}
    }
    WebObj.stringNames = {
            'puma concolor': 1,
            'turdus merula': 2
    }
    mca = MedeinaCumulativeApplication('dir')
    expected = {1: 'puma concolor', 2: 'turdus merula'}
    assert mca.determineAppropriateStringMapper(WebObj,'species') == expected
    expected = {1: 'felidae', 2: 'canidae'}
    assert mca.determineAppropriateStringMapper(WebObj,'family') == expected

class TempWebClass:
    def __init__(self):
        self.taxa = {}
        self.stringNames = {}

def getSupportingLargeWebObj():
    WebObj = TempWebClass()
    WebObj.taxa = {
            1:{'family':'felidae'},
            2:{'family':'ursus'},
            3:{'family':'felidae'},
            4:{'family':'felidae'},
            5:{'family':'felidae'},
            6:{'family':'ursus'},
            7:{'family':'canidae'},
            8:{'family':'ursus'},
            9:{'family':'canidae'},
            10:{'family':'canidae'},
            11:{'family':'felidae'},
            12:{'family':'felidae'},
            13:{'family':'canidae'},
            14:{'family':'felidae'},
            15:{'family':'ursus'},
    }
    WebObj.stringNames = {
            'puma concolor': 1,
            'ursus arctos': 2,
            'panthera tigris': 3,
            'panthera leo': 4,
            'acinonyx jubatus': 5,
            'ursus maritimus': 6,
            'canis lupus': 7,
            'ursus americanus': 8,
            'canis latrans': 9,
            'vulpes vulpes': 10,
            'panthera onca': 11,
            'felis catus': 12,
            'vulpes zerda': 13,
            'lynx rufus': 14,
            'helarctos malayanus': 15
    }

    WebObj.interactions = {
        IDTRACKER:41,
        1:{2:[1]},
        2:{3:[2,3]},
        3:{1:[4,5,6],4:[26,31],8:[32]},
        4:{},
        5:{1:[20,15],10:[33]},
        6:{3:[38],2:[34]},
        7:{6:[10]},
        8:{6:[11],3:[35,36,37],11:[40],14:[39]},
        9:{1:[12]},
        10:{2:[14],8:[30],9:[29],11:[28],1:[27]},
        11:{4:[8,9]},
        12:{10:[25]},
        13:{10:[23,24]},
        14:{11:[22],12:[13,16],13:[17]},
        15:{14:[7,21],1:[19],3:[18]}
    }
    return WebObj

def getSupportingSmallWebObj():
    WebObj = TempWebClass()
    WebObj.taxa = {
            1:{'family':'felidae'},
            2:{'family':'ursus'},
            3:{'family':'felidae'},
            4:{'family':'canidae'},
            5:{'family':'felidae'},
    }
    WebObj.stringNames = {
            'puma concolor': 1,
            'ursus arctos': 2,
            'panthera tigris': 3,
            'panthera leo': 4,
            'acinonyx jubatus': 5,
    }

    WebObj.interactions = {
        IDTRACKER:41,
        1:{2:[1]},
        2:{3:[2,3]},
        3:{1:[4,5,6],4:[26,31],8:[32]},
        4:{},
        5:{1:[20,15],10:[33]}
    }
    return WebObj

def testBuildingTaxaBasedInteractionsLarge():
    WebObj = getSupportingLargeWebObj()
    mca = MedeinaCumulativeApplication('dir')
    expected = {'acinonyx jubatus':
                {
                    'puma concolor': [20, 15], 
                    'vulpes vulpes': [33]
                }, 
                'canis latrans': 
                {
                    'puma concolor': [12]
                }, 
                'canis lupus': 
                {
                    'ursus maritimus': [10]
                }, 
                'felis catus': 
                {
                    'vulpes vulpes': [25]
                }, 
                'helarctos malayanus':   
                {
                    'lynx rufus': [7, 21],
                    'panthera tigris': [18],    
                    'puma concolor': [19]
                }, 
                'lynx rufus':
                {
                    'felis catus': [13, 16],
                    'panthera onca': [22],
                    'vulpes zerda': [17]
                }, 
                'panthera onca': 
                {
                    'panthera leo': [8, 9]
                }, 
                'panthera tigris':
                {
                    'panthera leo': [26, 31],
                    'puma concolor': [4, 5, 6],
                    'ursus americanus': [32]
                }, 
                'puma concolor': 
                {
                    'ursus arctos': [1]
                }, 
                'ursus americanus':
                {
                    'lynx rufus': [39], 
                    'panthera onca': [40], 
                    'panthera tigris': [35, 36, 37], 
                    'ursus maritimus': [11]
                }, 
                'ursus arctos': 
                {
                    'panthera tigris': [2, 3]
                }, 
                'ursus maritimus':
                {
                    'panthera tigris': [38],
                    'ursus arctos': [34]
                }, 
                'vulpes vulpes':
                {
                    'canis latrans': [29], 
                    'panthera onca': [28], 
                    'puma concolor': [27], 
                    'ursus americanus': [30], 
                    'ursus arctos': [14]
                }, 
                'vulpes zerda': 
                {
                    'vulpes vulpes': [23, 24]
                }}
    assert mca.buildTaxaBasedInteractions(WebObj,'species') == expected
    expected = {'canidae':
                    {
                        'canidae': [29, 23, 24],
                        'felidae': [12, 28, 27],
                        'ursus': [10, 14, 30]
                    },
                'felidae':
                    {
                        'canidae': [33, 25, 17],
                        'felidae': [4, 5, 6, 26, 31, 20, 15, 8, 9, 22, 13, 16],
                        'ursus': [1, 32]
                    },
                'ursus':
                    {
                        'felidae': [2, 3, 38, 35, 36, 37, 40, 39, 7, 21, 19, 18], 
                        'ursus': [34, 11]
                    }
                }
    assert mca.buildTaxaBasedInteractions(WebObj,'family') == expected

def getSupportingSmallWebObj():
    WebObj = TempWebClass()
    WebObj.taxa = {
        1:{'family':'felidae'},
        2:{'family':'ursus'},
        3:{'family':'felidae'},
        4:{'family':'canidae'},
        5:{'family':'felidae'}
    }
    WebObj.stringNames = {
            'puma concolor': 1,
            'ursus arctos': 2,
            'panthera tigris': 3,
            'panthera leo': 4,
            'acinonyx jubatus': 5,
    }

    WebObj.interactions = {
        IDTRACKER:41,
        1:{2:[1]},
        3:{1:[2],5:[3]},
        4:{},
        5:{4:[4]}
    }
    return WebObj

def getSupportingInvalidNamesWebObj():
    WebObj = TempWebClass()
    WebObj.taxa = {
        1:{'family':''},
        2:{'family':'ursus'},
        3:{'family':'felidae'},
        4:{'family':''},
        5:{'family':'felidae'}
    }
    WebObj.stringNames = {
            'puma concolor': 1,
            '': 2,
            'panthera tigris': 3,
            'panthera leo': 4,
            '': 5,
    }

    WebObj.interactions = {
        IDTRACKER:41,
        1:{2:[1]},
        3:{1:[2],5:[3]},
        4:{},
        5:{4:[4]}
    }
    return WebObj

def testBuildingTaxaBasedInteractionsSmall():
    WebObj = getSupportingSmallWebObj()
    mca = MedeinaCumulativeApplication('dir')
    expected = {'acinonyx jubatus': 
                  {'panthera leo': [4]},
                'panthera tigris':
                  {'acinonyx jubatus': [3],'puma concolor': [2]},
                'puma concolor':
                  {'ursus arctos': [1]}
                }
    assert mca.buildTaxaBasedInteractions(WebObj,'species') == expected

def testBuildingTaxaBasedInteractionsInvalid():
    WebObj = getSupportingInvalidNamesWebObj()
    mca = MedeinaCumulativeApplication('dir')
    expected = {'panthera tigris': {'puma concolor': [2]}}
    assert mca.buildTaxaBasedInteractions(WebObj,'species') == expected
    assert IDTRACKER in WebObj.interactions

def testHandlingOfNonExceptedSpeciesLarge():
    WebObj = getSupportingLargeWebObj()
    WebObj.taxaExceptions = {}
    mca = MedeinaCumulativeApplication('dir')
    speciesWithTaxa = {
        'ursus arctos': {'family':'ursus','species':'ursus arctos'},
        'vulpes vulpes': {'family':'canidae','species':'vulpes vulpes'},
        'canis lupus': {'family':'canidae','species':'canis lupus'},
        'ursus maritimus': {'family':'ursus','species':'ursus maritimus'},
        'panthera tigris': {'family':'felidae','species':'panthera tigris'},
        'felis catus': {'family':'felidae','species':'felis catus'},
        'panthera onca': {'family':'felidae','species':'panthera onca'},
    }

    interactions = mca.handleNonExceptionSpecies(WebObj,speciesWithTaxa,'species')
    expected = [('ursus arctos', 'panthera tigris'),('vulpes vulpes', 'ursus arctos'),('vulpes vulpes', 'panthera onca'),('canis lupus', 'ursus maritimus'),('ursus maritimus', 'ursus arctos'),('ursus maritimus', 'panthera tigris'),('felis catus', 'vulpes vulpes')]
    assert interactions == expected