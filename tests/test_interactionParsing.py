import sys
import os
import pytest
import pandas as pd  
from Medeina.interactionParser import * 
from unittest.mock import MagicMock
# import Medeina.common as MC
from mock import patch
from unittest.mock import patch, MagicMock, call, mock_open
IDTRACKER = 'numericCounter-b2ca94aee362f455a41493a0d28b98bc5074065b0f96cbb95028ead20b1c72ea'

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

@patch('Medeina.interactionParser.retrieveObjFromStore')
@patch('Medeina.interactionParser.writeTaxonomicInformation')
@patch('Medeina.interactionParser.addSpeciesToStringNameMapping')
@patch('Medeina.interactionParser.getTaxaAndValidateNewNames')
def testSavingTranslatedSpecies(test_add_taxa,test_add_mapping,test_patch_write,test_patch_retr):
    parsedSpecString = {'includeInvalid':True,'storageLocation':'dir'}
    species = [('Spec1','Spec2',{})]
    test_add_taxa.return_value = ['Spec1']
    test_add_mapping.return_value = {'Spec2':1,'Spec1':2}
    test_patch_retr.return_value = {'Spec2':1,'Spec1':2}
    result = indexTranslatedSpecies(species,parsedSpecString)
    test_patch_write.assert_called_with(['Spec1'], 'dir', {'Spec2': 1, 'Spec1': 2})

@patch('Medeina.interactionParser.retrieveObjFromStore')
@patch('Medeina.interactionParser.writeTaxonomicInformation')
@patch('Medeina.interactionParser.addSpeciesToStringNameMapping')
@patch('Medeina.interactionParser.getTaxaAndValidateNewNames')
def testSavingTranslatedSpeciesBlank(test_add_taxa,test_add_mapping,test_patch_write,test_patch_retr):
    parsedSpecString = {'includeInvalid':True,'storageLocation':'dir'}
    species = []
    test_add_taxa.return_value = []
    test_add_mapping.return_value = {'Spec2':1}
    test_patch_retr.return_value = {'Spec2':1}
    result = indexTranslatedSpecies(species,parsedSpecString)
    test_patch_write.assert_not_called()

@patch('Medeina.interactionParser.retrieveObjFromStore')
@patch('Medeina.interactionParser.writeObjToDateStore')
def testWritingInteractionsFresh(test_patch_write,test_patch_retr):
    def my_side_effect_fresh(*args):
        if args[1] == 'interactionWeb':
            return {IDTRACKER:1}
        if args[1] == 'links':
            return {}
    test_patch_retr.side_effect = my_side_effect_fresh
    parsedSpecString = {'includeInvalid':True,'storageLocation':'dir'}
    consumableData = [(5,6,{}),(7,8,{})]
    writeInteractionLinks(consumableData,1,parsedSpecString)
    test_patch_write.assert_has_calls([call( \
                                           'dir', \
                                           'interactionWeb', \
                                           {IDTRACKER: 3, 5: {6: [1]}, 7: {8: [2]}}), \
                                       call('dir', \
                                            'links', \
                                            {1: {'dId': 1}, 2: {'dId': 1}}) \
                                       ])

@patch('Medeina.interactionParser.retrieveObjFromStore')
@patch('Medeina.interactionParser.writeObjToDateStore')
def testWritingInteractionsOnExisting(test_patch_write,test_patch_retr):
    def my_side_effect_existing(*args):
        if args[1] == 'interactionWeb':
            return {IDTRACKER:5, 1:{2:[1],3:[2]},4:{2:[3],5:[4]}  }
        if args[1] == 'links':
            return {1: {'dId': 1}, 2: {'dId': 1}, 3:{'dId':1},4:{'dId':1}}
    test_patch_retr.side_effect = my_side_effect_existing
    parsedSpecString = {'includeInvalid':True,'storageLocation':'dir'}
    consumableData = [(5,6,{}),(7,8,{})]
    writeInteractionLinks(consumableData,2,parsedSpecString)
    test_patch_write.assert_has_calls( [call( \
                                            'dir', \
                                            'interactionWeb', \
                                            {IDTRACKER: 7, \
                                                1: {2: [1], 3: [2]}, \
                                                4: {2: [3], 5: [4]}, \
                                                5: {6: [5]}, \
                                                7: {8: [6]} \
                                            }), \
                                        call( \
                                            'dir', \
                                            'links', \
                                            {   \
                                                1: {'dId': 1}, \
                                                2: {'dId': 1}, \
                                                3: {'dId': 1}, \
                                                4: {'dId': 1}, \
                                                5: {'dId': 2}, \
                                                6: {'dId': 2}
                                            })])

@patch('Medeina.interactionParser.retrieveObjFromStore')
@patch('Medeina.interactionParser.writeObjToDateStore')
def testWritingInteractionsOnOverlapping(test_patch_write,test_patch_retr):
    def my_side_effect_overlapping(*args):
        if args[1] == 'interactionWeb':
            return {IDTRACKER:5, 1:{2:[1],3:[2]},4:{2:[3],5:[4]}  }
        if args[1] == 'links':
            return {1: {'dId': 1}, 2: {'dId': 1}, 3:{'dId':1},4:{'dId':1}}
    test_patch_retr.side_effect = my_side_effect_overlapping
    parsedSpecString = {'includeInvalid':True,'storageLocation':'dir'}
    consumableData = [(1,5,{}),(4,1,{})]
    writeInteractionLinks(consumableData,2,parsedSpecString)
    test_patch_write.assert_has_calls( [call( \
                                            'dir', \
                                            'interactionWeb', \
                                            {IDTRACKER: 7, \
                                                1: {2: [1], 3: [2],5:[5]}, \
                                                4: {2: [3], 5: [4],1:[6]} \
                                            }), \
                                        call( \
                                            'dir', \
                                            'links', \
                                            {   \
                                                1: {'dId': 1}, \
                                                2: {'dId': 1}, \
                                                3: {'dId': 1}, \
                                                4: {'dId': 1}, \
                                                5: {'dId': 2}, \
                                                6: {'dId': 2}
                                            })])


@patch('Medeina.interactionParser.retrieveObjFromStore')
@patch('Medeina.interactionParser.writeObjToDateStore')
def testDatasetRecordCreationBlank(test_patch_write,test_patch_retr):
    dct = {}
    dct['interactionType'] = 'Meta1'
    dct['evidencedBy'] = 'Meta2'
    dct['storageLocation'] = 'dir'
    test_patch_retr.return_value = {}
    newId = createNewDatasetRecord(dct)
    test_patch_write.assert_called_with('dir', 'datasets',{1:{'interactionType':'Meta1','evidencedBy':'Meta2'}})
    assert newId == 1

@patch('Medeina.interactionParser.retrieveObjFromStore')
@patch('Medeina.interactionParser.writeObjToDateStore')
def testDatasetRecordCreationExisting(test_patch_write,test_patch_retr):
    dct = {}
    dct['interactionType'] = 'Meta1'
    dct['evidencedBy'] = 'Meta2'
    dct['storageLocation'] = 'dir'
    test_patch_retr.return_value = {1:{}}
    newId = createNewDatasetRecord(dct)
    test_patch_write.assert_called_with('dir', 'datasets',{1:{},2:{'interactionType':'Meta1','evidencedBy':'Meta2'}})
    assert newId == 2

def testFilteringUnindexableSpecies():
    speciesMappingToId = {
        'Spec1':1,
        'Spec2':2,
        'Spec3':3
    }
    species = [('Spec1','Spec2',{}),('Spec1','Spec3',{}),('Spec3','Spec4',{})]
    parsedSpecString = {'includeInvalid':True,'storageLocation':'dir'}
    speciesWithIds = filterUnindexableSpecies(species,speciesMappingToId,parsedSpecString)
    assert speciesWithIds == [(1, 2, {}), (1, 3, {})]

def testFilteringUnindexableSpeciesAllFalse():
    speciesMappingToId = {
        'Spec1':1,
        'Spec2':2,
        'Spec3':3
    }
    species = [('Spec5','Spec6',{}),('Spec7','Spec8',{}),('Spec9','Spec10',{})]
    parsedSpecString = {'includeInvalid':True,'storageLocation':'dir'}
    speciesWithIds = filterUnindexableSpecies(species,speciesMappingToId,parsedSpecString)
    assert speciesWithIds == []