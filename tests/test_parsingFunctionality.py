import sys
import os
import pytest
import pandas as pd
from Medeina.interactionParser import *
from unittest.mock import MagicMock

# import Medeina.common as MC
from mock import patch
from unittest.mock import patch, MagicMock, call, mock_open

IDTRACKER = (
    "numericCounter-b2ca94aee362f455a41493a0d28b98bc5074065b0f96cbb95028ead20b1c72ea"
)


def testMakingUnique():
    headTailDataWithMetas = [
        ("Spec1", "Spec2", {}),
        ("Spec3", "Spec4", {}),
        ("Spec5", "Spec2", {}),
        ("Spec1", "Spec2", {}),
        ("Spec6", "Spec7", {}),
        ("Spec3", "Spec4", {}),
    ]
    expected = [
        ("Spec1", "Spec2", {}),
        ("Spec3", "Spec4", {}),
        ("Spec5", "Spec2", {}),
        ("Spec6", "Spec7", {}),
    ]
    assert makeUnique(headTailDataWithMetas) == expected


def testMakingUniqueWithMetas():
    headTailDataWithMetas = [
        ("Spec1", "Spec2", {"M1": "M1"}),
        ("Spec3", "Spec4", {"M2": "M2"}),
        ("Spec5", "Spec2", {"M4": "M4"}),
        ("Spec1", "Spec2", {"M1": "M1"}),
        ("Spec6", "Spec7", {"M3": "M3"}),
        ("Spec3", "Spec4", {"M2": "M2"}),
    ]
    expected = [
        ("Spec1", "Spec2", {"M1": "M1"}),
        ("Spec3", "Spec4", {"M2": "M2"}),
        ("Spec5", "Spec2", {"M4": "M4"}),
        ("Spec6", "Spec7", {"M3": "M3"}),
    ]
    assert makeUnique(headTailDataWithMetas) == expected


def testMakingUniqueWithVaryingMetas():
    headTailDataWithMetas = [
        ("Spec1", "Spec2", {"M1": "M1"}),
        ("Spec3", "Spec4", {"M2": "M2"}),
        ("Spec5", "Spec2", {"M3": "M3"}),
        ("Spec1", "Spec2", {"M4": "M4"}),
        ("Spec6", "Spec7", {"M5": "M5"}),
        ("Spec3", "Spec4", {"M6": "M6"}),
    ]
    expected = [
        ("Spec1", "Spec2", {"M1": "M1", "M4": "M4"}),
        ("Spec3", "Spec4", {"M2": "M2", "M6": "M6"}),
        ("Spec5", "Spec2", {"M3": "M3"}),
        ("Spec6", "Spec7", {"M5": "M5"}),
    ]
    assert makeUnique(headTailDataWithMetas) == expected


def testDictToTuples():
    metaDict = {
        ("Spec1", "Spec2"): {"M1": "M1"},
        ("Spec2", "Spec3"): {"M2": "M2"},
        ("Spec2", "Spec4"): {"M3": "M3"},
        ("Spec1", "Spec4"): {"M4": "M4"},
    }
    expected = [
        ("Spec1", "Spec2", {"M1": "M1"}),
        ("Spec2", "Spec3", {"M2": "M2"}),
        ("Spec2", "Spec4", {"M3": "M3"}),
        ("Spec1", "Spec4", {"M4": "M4"}),
    ]
    assert dictWithMetaToTuples(metaDict) == expected


def testDictToTuplesEmpty():
    metaDict = {}
    expected = []
    assert dictWithMetaToTuples(metaDict) == expected


def testKeepingInteractionPartOnly():
    headTailDataWithMetas = [
        ("Spec1", "Spec2", {"M1": "M1"}),
        ("Spec3", "Spec4", {"M2": "M2"}),
        ("Spec5", "Spec2", {"M3": "M3"}),
        ("Spec1", "Spec2", {"M4": "M4"}),
        ("Spec6", "Spec7", {"M5": "M5"}),
        ("Spec3", "Spec4", {"M6": "M6"}),
    ]
    expected = [
        ("Spec1", "Spec2"),
        ("Spec3", "Spec4"),
        ("Spec5", "Spec2"),
        ("Spec1", "Spec2"),
        ("Spec6", "Spec7"),
        ("Spec3", "Spec4"),
    ]
    assert keepInteractionPartOnly(headTailDataWithMetas) == expected
