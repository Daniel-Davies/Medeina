import sys
import os
import pytest
import pandas as pd  
from Medeina.externalAPIs import * 
from unittest.mock import MagicMock
# import Medeina.common as MC
from mock import patch
from unittest.mock import patch, MagicMock, call, mock_open
IDTRACKER = 'numericCounter-b2ca94aee362f455a41493a0d28b98bc5074065b0f96cbb95028ead20b1c72ea'

@patch('Medeina.externalAPIs.translateSpeciesList')
def testTranslatingTuplesExpectedCase(test_patch_retr):
    cleanedHeadTailTupleData = [('gen1 spec1','gen2 spec2',{'M1':'M1'}),('gen3 spec3','gen4 spec4',{'M2':'M2'}),('gen5 spec5','gen6 spec6',{})]
    test_patch_retr.return_value = {
        'gen1 spec1': ['gen1 spec1',['gen1 spec1']],
        'gen2 spec2': ['gen2 spec2',['gen2 spec2','gen22 spec22','gen222 spec222']],
        'gen3 spec3': ['gen3 spec3',['gen3 spec3']],
        'gen4 spec4': ['gen4 spec4',['gen4 spec4','gen44 spec44']],
        'gen5 spec5': ['gen5 spec5',[]],
        'gen6 spec6': ['gen6 spec6',['gen6 spec6']]
    }
    
    expected = [('gen1 spec1', 'gen2 spec2', {'M1':'M1'}), \
                ('gen1 spec1', 'gen22 spec22', {'M1':'M1'}), \
                ('gen1 spec1', 'gen222 spec222', {'M1':'M1'}), \
                ('gen3 spec3', 'gen4 spec4', {'M2':'M2'}), \
                ('gen3 spec3', 'gen44 spec44', {'M2':'M2'})]

    assert translateToSpeciesScientificFormatOnly(cleanedHeadTailTupleData) == expected

@patch('Medeina.externalAPIs.translateSpeciesList')
def testTranslatingTuplesNoValid(test_patch_retr):
    cleanedHeadTailTupleData = [('gen1 spec1','gen2 spec2',{}),('gen3 spec3','gen4 spec4',{}),('gen5 spec5','gen6 spec6',{})]
    test_patch_retr.return_value = {
        'gen1 spec1': ['gen1 spec1',[]],
        'gen2 spec2': ['gen2 spec2',[]],
        'gen3 spec3': ['gen3 spec3',[]],
        'gen4 spec4': ['gen4 spec4',[]],
        'gen5 spec5': ['gen5 spec5',[]],
        'gen6 spec6': ['gen6 spec6',[]]
    }
    
    assert translateToSpeciesScientificFormatOnly(cleanedHeadTailTupleData) == []

@patch('Medeina.externalAPIs.translateSpeciesList')
def testTranslatingTuplesDuplicated(test_patch_retr):
    cleanedHeadTailTupleData = [('gen1 spec1','gen2 spec2',{'M1':'M1'}),('gen1 spec1','gen2 spec2',{'M1':'M1'}),('gen5 spec5','gen6 spec6',{})]
    test_patch_retr.return_value = {
        'gen1 spec1': ['gen1 spec1',['gen1 spec1']],
        'gen2 spec2': ['gen2 spec2',['gen2 spec2','gen22 spec22','gen222 spec222']],
        'gen5 spec5': ['gen5 spec5',['gen5 spec5']],
        'gen6 spec6': ['gen6 spec6',['gen6 spec6']]
    }
    
    expected = [('gen1 spec1', 'gen2 spec2', {'M1':'M1'}), \
                ('gen1 spec1', 'gen22 spec22', {'M1':'M1'}), \
                ('gen1 spec1', 'gen222 spec222', {'M1':'M1'}), \
                ('gen5 spec5', 'gen6 spec6', {})]

    assert translateToSpeciesScientificFormatOnly(cleanedHeadTailTupleData) == expected

@patch('Medeina.externalAPIs.translateSpeciesList')
def testTranslatingTuplesDuplicatedWithVaryingMetas(test_patch_retr):
    cleanedHeadTailTupleData = [('gen1 spec1','gen2 spec2',{'M1':'M1'}),('gen1 spec1','gen2 spec2',{'M2':'M2'}),('gen5 spec5','gen6 spec6',{})]
    test_patch_retr.return_value = {
        'gen1 spec1': ['gen1 spec1',['gen1 spec1']],
        'gen2 spec2': ['gen2 spec2',['gen2 spec2','gen22 spec22','gen222 spec222']],
        'gen5 spec5': ['gen5 spec5',['gen5 spec5']],
        'gen6 spec6': ['gen6 spec6',['gen6 spec6']]
    }
    
    expected = [('gen1 spec1', 'gen2 spec2', {'M1':'M1','M2':'M2'}), \
                ('gen1 spec1', 'gen22 spec22', {'M1':'M1','M2':'M2'}), \
                ('gen1 spec1', 'gen222 spec222', {'M1':'M1','M2':'M2'}), \
                ('gen5 spec5', 'gen6 spec6', {})]

    assert translateToSpeciesScientificFormatOnly(cleanedHeadTailTupleData) == expected