import sys
import os
import pytest
import pandas as pd  
from Medeina.interactionParser import * 
from unittest.mock import MagicMock
# import Medeina.common as MC
from mock import patch
from unittest.mock import patch, MagicMock, call, mock_open

def testLocationDataStandardising():
    assert standardiseLocationData('Bristol,UK') == {'country': 'UK', 'region': 'Bristol'}
    assert standardiseLocationData('USA') == {'country': 'USA', 'region': ''}
    assert standardiseLocationData('') == {'country': '', 'region': ''}

def testDatasetMetaDataTaking():
    dct = {}
    dct['interactionType'] = 'Meta1'
    dct['evidencedBy'] = 'Meta2'
    assert takeDatasetMetaData(dct) ==  {'evidencedBy': 'Meta2', 'interactionType': 'Meta1'}

def testDatasetMetaDataTakingBlank():
    dct = {}
    assert takeDatasetMetaData(dct) ==  {}

@patch('Medeina.interactionParser.retrieveObjFromStore')
def testCorrectTaxaGap(test_patch):
    test_patch.return_value = {'spec1':1, \
                               'spec2':2, \
                               'spec3':3}

    assert sorted(determineTaxonomicGaps(['spec1','spec2','spec4','spec5'],'tmp')) \
                               == sorted(['spec4','spec5'])

@patch('Medeina.interactionParser.retrieveObjFromStore')
@patch('Medeina.interactionParser.writeObjToDateStore')
def testAdditionOfTaxaInformation(test_patch_write,test_patch_retr):
    test_patch_retr.return_value = {1:{}, \
                               2:{}, \
                               3:{}}
    writeTaxonomicInformation([['s1',True,{'family':'new'}]],'dir',{'s1':4})
    test_patch_write.assert_called_with('dir', 'taxonomicIndex', {4: {'family': 'new'},1:{}, 2: {}, 3: {}})

@patch('Medeina.interactionParser.retrieveObjFromStore')
@patch('Medeina.interactionParser.writeObjToDateStore')
def testSpeciesNameAdditionToFile(test_patch_write,test_patch_retr):
    test_patch_retr.return_value = {'existingName':1}
    addSpeciesToStringNameMapping([['s1',True,{'family':'new'}]],'dir')
    test_patch_write.assert_called_with('dir','speciesStringNames',{'existingName':1,'s1':2})