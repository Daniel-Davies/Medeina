import sys
import os
import pytest
import pandas as pd
from Medeina.externalAPIs import *
from unittest.mock import MagicMock
from mock import patch
from unittest.mock import patch, MagicMock, call, mock_open

IDTRACKER = (
    "numericCounter-b2ca94aee362f455a41493a0d28b98bc5074065b0f96cbb95028ead20b1c72ea"
)


@patch("Medeina.externalAPIs.translateSpeciesList")
def testTranslatingTuplesExpectedCase(test_patch_retr):
    cleanedHeadTailTupleData = [
        ("gen1 spec1", "gen2 spec2", {"M1": "M1"}),
        ("gen3 spec3", "gen4 spec4", {"M2": "M2"}),
        ("gen5 spec5", "gen6 spec6", {}),
    ]
    test_patch_retr.return_value = {
        "gen1 spec1": ["gen1 spec1", ["gen1 spec1"]],
        "gen2 spec2": ["gen2 spec2", ["gen2 spec2", "gen22 spec22", "gen222 spec222"]],
        "gen3 spec3": ["gen3 spec3", ["gen3 spec3"]],
        "gen4 spec4": ["gen4 spec4", ["gen4 spec4", "gen44 spec44"]],
        "gen5 spec5": ["gen5 spec5", []],
        "gen6 spec6": ["gen6 spec6", ["gen6 spec6"]],
    }

    expected = [
        ("gen1 spec1", "gen2 spec2", {"M1": "M1"}),
        ("gen1 spec1", "gen22 spec22", {"M1": "M1"}),
        ("gen1 spec1", "gen222 spec222", {"M1": "M1"}),
        ("gen3 spec3", "gen4 spec4", {"M2": "M2"}),
        ("gen3 spec3", "gen44 spec44", {"M2": "M2"}),
    ]

    assert translateToSpeciesScientificFormatOnly(cleanedHeadTailTupleData) == expected


@patch("Medeina.externalAPIs.translateSpeciesList")
def testTranslatingTuplesNoValid(test_patch_retr):
    cleanedHeadTailTupleData = [
        ("gen1 spec1", "gen2 spec2", {}),
        ("gen3 spec3", "gen4 spec4", {}),
        ("gen5 spec5", "gen6 spec6", {}),
    ]
    test_patch_retr.return_value = {
        "gen1 spec1": ["gen1 spec1", []],
        "gen2 spec2": ["gen2 spec2", []],
        "gen3 spec3": ["gen3 spec3", []],
        "gen4 spec4": ["gen4 spec4", []],
        "gen5 spec5": ["gen5 spec5", []],
        "gen6 spec6": ["gen6 spec6", []],
    }

    assert translateToSpeciesScientificFormatOnly(cleanedHeadTailTupleData) == []


@patch("Medeina.externalAPIs.translateSpeciesList")
def testTranslatingTuplesDuplicated(test_patch_retr):
    cleanedHeadTailTupleData = [
        ("gen1 spec1", "gen2 spec2", {"M1": "M1"}),
        ("gen1 spec1", "gen2 spec2", {"M1": "M1"}),
        ("gen5 spec5", "gen6 spec6", {}),
    ]
    test_patch_retr.return_value = {
        "gen1 spec1": ["gen1 spec1", ["gen1 spec1"]],
        "gen2 spec2": ["gen2 spec2", ["gen2 spec2", "gen22 spec22", "gen222 spec222"]],
        "gen5 spec5": ["gen5 spec5", ["gen5 spec5"]],
        "gen6 spec6": ["gen6 spec6", ["gen6 spec6"]],
    }

    expected = [
        ("gen1 spec1", "gen2 spec2", {"M1": "M1"}),
        ("gen1 spec1", "gen22 spec22", {"M1": "M1"}),
        ("gen1 spec1", "gen222 spec222", {"M1": "M1"}),
        ("gen5 spec5", "gen6 spec6", {}),
    ]

    assert translateToSpeciesScientificFormatOnly(cleanedHeadTailTupleData) == expected


@patch("Medeina.externalAPIs.translateSpeciesList")
def testTranslatingTuplesDuplicatedWithVaryingMetas(test_patch_retr):
    cleanedHeadTailTupleData = [
        ("gen1 spec1", "gen2 spec2", {"M1": "M1"}),
        ("gen1 spec1", "gen2 spec2", {"M2": "M2"}),
        ("gen5 spec5", "gen6 spec6", {}),
    ]
    test_patch_retr.return_value = {
        "gen1 spec1": ["gen1 spec1", ["gen1 spec1"]],
        "gen2 spec2": ["gen2 spec2", ["gen2 spec2", "gen22 spec22", "gen222 spec222"]],
        "gen5 spec5": ["gen5 spec5", ["gen5 spec5"]],
        "gen6 spec6": ["gen6 spec6", ["gen6 spec6"]],
    }

    expected = [
        ("gen1 spec1", "gen2 spec2", {"M1": "M1", "M2": "M2"}),
        ("gen1 spec1", "gen22 spec22", {"M1": "M1", "M2": "M2"}),
        ("gen1 spec1", "gen222 spec222", {"M1": "M1", "M2": "M2"}),
        ("gen5 spec5", "gen6 spec6", {}),
    ]

    assert translateToSpeciesScientificFormatOnly(cleanedHeadTailTupleData) == expected


def testTakeIfMatchesGroup():
    data = [
        {"family": "felidae", "X": "Y", "species": "Spec1"},
        {"family": "felidae", "X": "Y", "species": "Spec2"},
        {"family": "unknown", "X": "Y", "species": "Spec3"},
        {"family": "felidae", "X": "Y", "species": "Spec4"},
        {"family": "delphinidae", "X": "Y", "species": "Spec5"},
        {},
    ]
    level = "family"
    group = "felidae"

    expected = 1
    assert takeSpeciesMatchingGroupOnly(group, level, data) == [
        "Spec1",
        "Spec2",
        "Spec4",
    ]


def testTakeIfMatchesGroupBlank():
    data = [
        {"family": "felidae", "X": "Y", "species": "Spec1"},
        {"family": "felidae", "X": "Y", "species": "Spec2"},
        {"family": "unknown", "X": "Y", "species": "Spec3"},
        {"family": "felidae", "X": "Y", "species": "Spec4"},
        {"family": "delphinidae", "X": "Y", "species": "Spec5"},
        {},
    ]
    level = "order"
    group = "felidae"

    assert takeSpeciesMatchingGroupOnly(group, level, data) == []


def testIndexToTuples():
    index = {
        "Spec1": ["Spec1", ["Spec1", "Spec11"]],
        "Spec2": ["Spec2", ["Spec2"]],
        "Spec3": ["Spec3", []],
    }
    expected = [
        ["Spec1", "Spec1", ["Spec1", "Spec11"]],
        ["Spec2", "Spec2", ["Spec2"]],
        ["Spec3", "Spec3", []],
    ]
    assert indexToTuples(index) == expected


def testGroupingExpected():
    values = ["a", "b", "a", "a", "c"]
    assert grouping(values) == {"a": 3, "b": 1, "c": 1}


def testGroupingExpectedBlank():
    values = []
    assert grouping(values) == {}


def testGroupingWithEmptyString():
    values = ["", "", "", "", "a", "a"]
    assert grouping(values) == {"a": 2}


def testSummaryStatsForAllCategoriesExpected():
    results = [
        {"family": "felidae", "species": "Spec1"},
        {"family": "felidae", "species": "Spec2"},
        {"family": "unknown", "species": "Spec1"},
        {"family": "felidae", "species": "Spec3"},
        {"family": "delphinidae", "species": "Spec1"},
        {},
    ]
    expected = {
        "class": {},
        "family": {"delphinidae": 1, "felidae": 3, "unknown": 1},
        "genus": {},
        "kingdom": {},
        "order": {},
        "phylum": {},
    }

    assert summaryStatsPerCategory(results) == expected


def testSummaryStatsForAllCategoriesEmptyStrings():
    results = [
        {"family": "felidae", "species": "Spec1", "order": "O1"},
        {"family": "felidae", "species": "Spec2", "order": ""},
        {"family": "unknown", "species": "Spec1", "order": "O1"},
        {"family": "felidae", "species": "Spec3", "order": "O2"},
        {"family": "delphinidae", "species": "Spec1", "order": ""},
        {},
    ]
    expected = {
        "class": {},
        "family": {"delphinidae": 1, "felidae": 3, "unknown": 1},
        "genus": {},
        "kingdom": {},
        "order": {"O1": 2, "O2": 1},
        "phylum": {},
    }

    assert summaryStatsPerCategory(results) == expected


def testTranslationDecisionsExpected():
    listOfClassifications = [
        {"family": "icteridae", "species": "chrysomus icterocephalus"},
        {"family": "icteridae", "species": "curaeus forbesi"},
        {"family": "icteridae", "species": "chrysomus ruficapillus"},
        {"family": "turdidae", "species": "turdus albocinctus"},
        {"family": "icteridae", "species": "amblyramphus holosericeus"},
        {"family": "icteridae", "species": "nesopsar nigerrimus"},
        {"family": "icteridae", "species": "gnorimopsar chopi"},
        {"family": "turdidae", "species": "turdus poliocephalus"},
        {"family": "icteridae", "species": "euphagus cyanocephalus"},
        {"family": "turdidae", "species": "turdus merula"},
        {"family": "icteridae", "species": "gymnomystax mexicanus"},
        {"family": "icteridae", "species": "agelaioides oreopsar"},
        {"family": "icteridae", "species": "sturnella militaris"},
        {"family": "icteridae", "species": "agelaius humeralis"},
        {"family": "icteridae", "species": "dives warszewiczi"},
        {"family": "icteridae", "species": "dives atroviolaceus"},
        {"family": "icteridae", "species": "agelaius tricolor"},
        {"family": "icteridae", "species": "euphagus carolinus"},
    ]
    expected = [
        "chrysomus icterocephalus",
        "curaeus forbesi",
        "chrysomus ruficapillus",
        "amblyramphus holosericeus",
        "nesopsar nigerrimus",
        "gnorimopsar chopi",
        "euphagus cyanocephalus",
        "gymnomystax mexicanus",
        "agelaioides oreopsar",
        "sturnella militaris",
        "agelaius humeralis",
        "dives warszewiczi",
        "dives atroviolaceus",
        "agelaius tricolor",
        "euphagus carolinus",
    ]

    assert (
        decideTranslationOnGroupStats(
            [("icteridae", 4), ("turdidae", 1)], listOfClassifications
        )
        == expected
    )


def testTranslationDecisionsNotThreeQuarters():
    listOfClassifications = [
        {"family": "F1", "species": "chrysomus icterocephalus"},
        {"family": "F1", "species": "curaeus forbesi"},
        {"family": "F1", "species": "chrysomus ruficapillus"},
        {"family": "F1", "species": "turdus albocinctus"},
        {"family": "F1", "species": "amblyramphus holosericeus"},
        {"family": "F1", "species": "nesopsar nigerrimus"},
        {"family": "F2", "species": "gnorimopsar chopi"},
        {"family": "F2", "species": "turdus poliocephalus"},
        {"family": "F2", "species": "euphagus cyanocephalus"},
        {"family": "F2", "species": "turdus merula"},
        {"family": "F2", "species": "gymnomystax mexicanus"},
        {"family": "F2", "species": "agelaioides oreopsar"},
        {"family": "F3", "species": "sturnella militaris"},
        {"family": "F3", "species": "agelaius humeralis"},
        {"family": "F3", "species": "dives warszewiczi"},
        {"family": "F3", "species": "dives atroviolaceus"},
        {"family": "F3", "species": "agelaius tricolor"},
        {"family": "F3", "species": "euphagus carolinus"},
    ]

    assert (
        decideTranslationOnGroupStats(
            [("F1", 6), ("F2", 6), ("F3", 6)], listOfClassifications
        )
        == []
    )


def testTranslationDecisionsBorder():
    listOfClassifications = [
        {"family": "F1", "species": "chrysomus icterocephalus"},
        {"family": "F1", "species": "curaeus forbesi"},
        {"family": "F1", "species": "chrysomus ruficapillus"},
        {"family": "F1", "species": "turdus albocinctus"},
        {"family": "F1", "species": "amblyramphus holosericeus"},
        {"family": "F1", "species": "nesopsar nigerrimus"},
        {"family": "F2", "species": "gnorimopsar chopi"},
        {"family": "F2", "species": "turdus poliocephalus"},
    ]

    assert (
        decideTranslationOnGroupStats([("F1", 6), ("F2", 2)], listOfClassifications)
        == []
    )


def testTranslationDecisionsMultiCatException():
    listOfClassifications = [
        {"family": "F1", "species": "chrysomus icterocephalus"},
        {"family": "F1", "species": "curaeus forbesi"},
        {"family": "F1", "species": "chrysomus ruficapillus"},
        {"family": "F1", "species": "turdus albocinctus"},
        {"family": "F1", "species": "amblyramphus holosericeus"},
        {"family": "F2", "species": "nesopsar nigerrimus"},
        {"family": "F3", "species": "gnorimopsar chopi"},
        {"family": "F4", "species": "turdus poliocephalus"},
        {"family": "F5", "species": "turdus poliocephalus"},
        {"family": "F6", "species": "turdus poliocephalus"},
    ]

    expected = [
        "chrysomus icterocephalus",
        "curaeus forbesi",
        "chrysomus ruficapillus",
        "turdus albocinctus",
        "amblyramphus holosericeus",
    ]

    assert (
        decideTranslationOnGroupStats(
            [("F1", 5), ("F2", 1), ("F3", 1), ("F4", 1), ("F5", 1), ("F6", 1)],
            listOfClassifications,
        )
        == expected
    )


@patch("Medeina.externalAPIs.classify")
def testEnrichmentOfSpecies(test_patch_retr):
    def dynamicTaxaSelection(speciesNames):
        if "vulpes vulpes" in speciesNames:
            return {
                "vulpes vulpes": [
                    "vulpes vulpes",
                    {"species": "vulpes vulpes", "family": "canidae"},
                ],
                "canis lupus": [
                    "canis lupus",
                    {"species": "canis lupus", "family": "canidae"},
                ],
            }
        elif "panthera tigris" in speciesNames:
            return {
                "panthera tigris": [
                    "panthera tigris",
                    {"species": "panthera tigris", "family": "felidae"},
                ],
                "felis catus": [
                    "felis catus",
                    {"species": "felis catus", "family": "felidae"},
                ],
            }

    test_patch_retr.side_effect = dynamicTaxaSelection
    index = [
        ("Dogs", "Dogs", ["vulpes vulpes", "canis lupus"]),
        ("Cats", "Cats", ["panthera tigris", "felis catus"]),
    ]

    expected = [
        [
            "Dogs",
            "Dogs",
            [
                {"family": "canidae", "species": "vulpes vulpes"},
                {"family": "canidae", "species": "canis lupus"},
            ],
        ],
        [
            "Cats",
            "Cats",
            [
                {"family": "felidae", "species": "panthera tigris"},
                {"family": "felidae", "species": "felis catus"},
            ],
        ],
    ]
    assert enrichSpeciesToFullTaxonomy(index) == expected


@patch("Medeina.externalAPIs.classify")
def testEnrichmentOfSpeciesBlank(test_patch_retr):
    def dynamicTaxaSelection(speciesNames):
        if "vulpes vulpes" in speciesNames:
            return {
                "vulpes vulpes": ["vulpes vulpes", {}],
                "canis lupus": ["canis lupus", {}],
            }
        elif "panthera tigris" in speciesNames:
            return {
                "panthera tigris": ["panthera tigris", {}],
                "felis catus": ["felis catus", {}],
            }

    test_patch_retr.side_effect = dynamicTaxaSelection
    index = [
        ("Dogs", "Dogs", ["vulpes vulpes", "canis lupus"]),
        ("Cats", "Cats", ["panthera tigris", "felis catus"]),
    ]

    expected = [["Dogs", "Dogs", [{}, {}]], ["Cats", "Cats", [{}, {}]]]
    assert enrichSpeciesToFullTaxonomy(index) == expected
