
from Medeina.exportTools import *
from Medeina.config import *
from mock import patch


def testHeaderGeneration():
    headers = getHeaders()
    assert headers == ['consumer','resource',*LINK_METAS,*DATASET_METAS]

@patch('Medeina.exportTools.retrieveObjFromStore')
def testWhichDatasetsToNormalize(test_patch_retr):
    test_patch_retr.return_value = {1:{},2:{},3:{}}
    assert datasetsToNormalise([]) == set([1,2,3])
    assert datasetsToNormalise([1,2]) == set([1,2]) 
    assert datasetsToNormalise([1]) == set([1])

@patch('Medeina.exportTools.retrieveObjFromStore')
def testLinkMappingAll(test_patch_retr):
    test_patch_retr.return_value = {
        IDTRACKER:5,
        1: {2:[1],3:[4]},
        2: {3:[2]},
        3: {4:[3]}
    }
    existingLinks = {
        1:{'dId':1},
        2:{'dId':2},
        3:{'dId':1},
        4:{'dId':2}
    }
    links = findLinksInRequestedDatasets([1,2],existingLinks) 
    assert links == [([1, 2], 1), ([1, 3], 4), ([2, 3], 2), ([3, 4], 3)]

@patch('Medeina.exportTools.retrieveObjFromStore')
def testLinkMappingPartial(test_patch_retr):
    test_patch_retr.return_value = {
        IDTRACKER:5,
        1: {2:[1],3:[4]},
        2: {3:[2]},
        3: {4:[3]}
    }
    existingLinks = {
        1:{'dId':1},
        2:{'dId':2},
        3:{'dId':1},
        4:{'dId':2}
    }
    links = findLinksInRequestedDatasets([1],existingLinks) 
    assert links == [([1, 2], 1), ([3, 4], 3)]

def testAdditionOfLinkMetaData():
    existingLinks = {
        1:{'dId':1, 'interactionType':'predation'},
    }
    tup = ([1,2],1)
    links = handleLinkMetaData(tup,existingLinks)
    shouldBe = [1, 2, 'predation'] 
    shouldBe.extend(['']*(len(LINK_METAS)-1))
    assert links == (shouldBe, 1)

def testAdditionOfDatasetMetaData():
    existingData = {
        1:{'evidencedBy':'observed'},
    }
    tup = ([1,2,'previousLinkMeta'],1)
    links = handleDatasetMetaData(tup,existingData)
    shouldBe = [1, 2,'previousLinkMeta', '', 'observed'] 
    shouldBe.extend(['']*(len(DATASET_METAS)-2))
    assert links == shouldBe
