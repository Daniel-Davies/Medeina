import sys
import os
import pytest
import pandas as pd
from Medeina.filterFunctions import *
from unittest.mock import MagicMock
from mock import patch
from unittest.mock import patch, MagicMock, call, mock_open

IDTRACKER = (
    "numericCounter-b2ca94aee362f455a41493a0d28b98bc5074065b0f96cbb95028ead20b1c72ea"
)


def testFilteringDatasetIds():
    datasetObject = {1: {}, 2: {}, 3: {}, 4: {}, 5: {}}
    assert filterDatasetByDIds(datasetObject, []) == {}
    assert filterDatasetByDIds(datasetObject, [1, 2]) == {1: {}, 2: {}}
    assert filterDatasetByDIds(datasetObject, [1, 2, 3, 4, 5, 100000]) == datasetObject


def testFilteringDatasetIdsBlank():
    datasetObject = {}
    assert filterDatasetByDIds(datasetObject, []) == {}
    assert filterDatasetByDIds(datasetObject, [1, 2]) == {}
    assert filterDatasetByDIds(datasetObject, [1, 2, 3, 4, 5]) == {}


def testFilterlinksByDIds():
    links = {1: {"dId": 1}, 2: {"dId": 1}, 3: {"dId": 2}, 4: {"dId": 1}, 5: {"dId": 3}}
    assert filterLinksMetasByDIds(links, []) == {}
    assert filterLinksMetasByDIds(links, [1]) == {
        1: {"dId": 1},
        2: {"dId": 1},
        4: {"dId": 1},
    }
    assert filterLinksMetasByDIds(links, [1, 2, 3]) == links
    assert filterLinksMetasByDIds(links, [3, 2]) == {3: {"dId": 2}, 5: {"dId": 3}}


def testFilterlinksByDIdsBlank():
    links = {}
    assert filterLinksMetasByDIds(links, []) == {}
    assert filterLinksMetasByDIds(links, [1]) == {}
    assert filterLinksMetasByDIds(links, [1, 2, 3]) == {}
    assert filterLinksMetasByDIds(links, [3, 2]) == {}


def testFilteringInteractionsByLinkIds():
    interactions = {
        IDTRACKER: 1000000,
        1: {2: [1], 3: [2], 4: [3]},
        2: {5: [4]},
        3: {2: [5], 6: [6]},
    }
    linkMetas = {1: {}, 4: {}, 6: {}, 8: {}}
    expected = {IDTRACKER: 1000000, 1: {2: [1]}, 2: {5: [4]}, 3: {6: [6]}}

    assert filterInteractionsByLinkIds(interactions, linkMetas) == expected

    linkMetas = {1: {}, 4: {}}
    expected = {
        IDTRACKER: 1000000,
        1: {2: [1]},
        2: {5: [4]},
    }

    assert filterInteractionsByLinkIds(interactions, linkMetas) == expected


def testFilteringStringNamesByInteractionsFull():
    speciesStringDict = {"Spec1": 1, "Spec2": 2, "Spec3": 3, "Spec4": 4, "Spec5": 5}
    interactions = {
        IDTRACKER: 1000000,
        1: {2: [1], 3: [2], 4: [3]},
        2: {5: [4]},
        3: {2: [5], 6: [6]},
    }

    expected = speciesStringDict
    assert filterStringNamesByInteractions(speciesStringDict, interactions) == expected


def testFilteringStringNamesByInteractionsPartial():
    speciesStringDict = {"Spec1": 1, "Spec2": 2, "Spec3": 3, "Spec4": 4, "Spec5": 5}
    interactions = {
        IDTRACKER: 1000000,
        1: {3: [2]},
        2: {},
    }

    expected = {"Spec1": 1, "Spec2": 2, "Spec3": 3}
    assert filterStringNamesByInteractions(speciesStringDict, interactions) == expected


def testFilteringStringNamesByInteractionsBlank():
    speciesStringDict = {"Spec1": 1, "Spec2": 2, "Spec3": 3, "Spec4": 4, "Spec5": 5}
    interactions = {IDTRACKER: 1000000}
    assert filterStringNamesByInteractions(speciesStringDict, interactions) == {}


def testFilterByTaxa():
    taxa = {
        1: {"family": "F"},
        2: {"family": "F"},
        3: {"family": "F"},
        4: {"family": "F"},
        5: {"family": "F"},
    }

    speciesStringDict = {"Spec1": 1, "Spec5": 5}

    expected = {1: {"family": "F"}, 5: {"family": "F"}}
    assert filterNoLongerNeededTaxa(taxa, speciesStringDict) == expected

    taxa = {
        1: {"family": "F"},
        2: {"family": "F"},
        3: {"family": "F"},
        4: {"family": "F"},
        5: {"family": "F"},
    }

    speciesStringDict = {"Spec1": 1, "Spec2": 2, "Spec3": 3, "Spec4": 4, "Spec5": 5}

    assert filterNoLongerNeededTaxa(taxa, speciesStringDict) == taxa


def testDictionaryCrushingToHeadTail():
    interactions = {
        IDTRACKER: 1000000,
        1: {2: [1], 3: [2, 7, 8], 4: [3, 9]},
        2: {5: [4]},
        3: {2: [5], 6: [6, 10]},
    }
    assert crushInteractionDict(interactions) == set([1, 2, 3, 4, 5, 6])
    interactions = {IDTRACKER: 1000000}
    assert crushInteractionDict(interactions) == set()
    interactions = {IDTRACKER: 1000000, 1: {}, 2: {}, 3: {}}
    assert crushInteractionDict(interactions) == set([1, 2, 3])


def testDictionaryInteractionCounting():
    interactions = {
        IDTRACKER: 1000000,
        1: {2: [1], 3: [2, 7, 8], 4: [3, 9]},
        2: {5: [4]},
        3: {2: [5], 6: [6, 10]},
    }
    assert countInteractionsInDict(interactions) == 10
    interactions = {IDTRACKER: 1000000}
    assert countInteractionsInDict(interactions) == 0
    interactions = {IDTRACKER: 1000000, 1: {}, 2: {}, 3: {}}
    assert countInteractionsInDict(interactions) == 0


def testFilteringInvalidInteractions():
    interactions = {
        IDTRACKER: 1000000,
        1: {2: [1], 3: [2, 7, 8], 4: [3, 9]},
        2: {5: [4]},
        3: {2: [5], 6: [6, 10]},
    }
    speciesStringDict = {"Spec1": 1, "Spec2": 2, "Spec3": 3, "Spec5": 5}
    expected = {1: {2: [1], 3: [2, 7, 8]}, 2: {5: [4]}, 3: {2: [5]}}

    assert filterInvalidInteractions(interactions, speciesStringDict) == expected


def testFilteringInvalidInteractionsNoIntersection():
    interactions = {
        IDTRACKER: 1000000,
        1: {2: [1], 3: [2, 7, 8], 4: [3, 9]},
        2: {5: [4]},
        3: {2: [5], 6: [6, 10]},
    }
    speciesStringDict = {
        "Spec1": 7,
        "Spec2": 8,
        "Spec3": 9,
    }
    expected = {}
    assert filterInvalidInteractions(interactions, speciesStringDict) == expected


def testFastAccessTaxaDictConversion():
    taxaConstraints = [
        ("Spec1", "family"),
        ("Spec2", "family"),
        ("Spec3", "genus"),
        ("Spec4", "genus"),
        ("Spec5", "order"),
    ]
    expected = {
        "family": {"Spec1", "Spec2"},
        "genus": {"Spec3", "Spec4"},
        "order": {"Spec5"},
    }
    assert convertTaxaConstraintsToFastAccess(taxaConstraints) == expected
    taxaConstraints = {}
    expected = {}
    assert convertTaxaConstraintsToFastAccess(taxaConstraints) == expected


def testTaxonomyFiltering():
    speciesStringDict = {"Spec1": 1, "Spec4": 4, "Spec5": 5}
    taxa = {
        1: {"family": "F"},
        2: {"family": "F"},
        3: {"family": "F"},
        4: {"family": "F"},
        5: {"family": "F"},
    }
    expected = {1: {"family": "F"}, 4: {"family": "F"}, 5: {"family": "F"}}
    assert filterUneededTaxa(taxa, speciesStringDict) == expected
    speciesStringDict = {"Spec1": 1, "Spec2": 2, "Spec3": 3, "Spec4": 4, "Spec5": 5}
    taxa = {
        1: {"family": "F"},
        2: {"family": "F"},
        3: {"family": "F"},
        4: {"family": "F"},
        5: {"family": "F"},
    }
    expected = taxa
    assert filterUneededTaxa(taxa, speciesStringDict) == expected
    speciesStringDict = {}
    taxa = {
        1: {"family": "F"},
        2: {"family": "F"},
        3: {"family": "F"},
        4: {"family": "F"},
        5: {"family": "F"},
    }
    assert filterUneededTaxa(taxa, speciesStringDict) == {}


def testFilteringStringNamesByTaxaConstraints():
    speciesStringDict = {"Spec1": 1, "Spec2": 2, "Spec3": 3, "Spec4": 4, "Spec5": 5}
    taxaConstraints = [
        ("felidae", "family"),
        ("ursus", "genus"),
    ]
    taxa = {
        1: {"family": "felidae"},
        2: {"genus": "ursus"},
        3: {"family": "F"},
        4: {"family": "felidae"},
        5: {"family": "F"},
    }
    expected = {"Spec1": 1, "Spec2": 2, "Spec4": 4}
    assert (
        filterStringNamesByTaxaConstraints(speciesStringDict, taxaConstraints, taxa)
        == expected
    )
    speciesStringDict = {"Spec1": 1, "Spec2": 2, "Spec3": 3, "Spec4": 4, "Spec5": 5}
    taxaConstraints = []
    taxa = {
        1: {"family": "felidae"},
        2: {"genus": "ursus"},
        3: {"family": "F"},
        4: {"family": "felidae"},
        5: {"family": "F"},
    }
    expected = {}
    assert (
        filterStringNamesByTaxaConstraints(speciesStringDict, taxaConstraints, taxa)
        == expected
    )
    speciesStringDict = {"Spec1": 1, "Spec2": 2, "Spec3": 3, "Spec4": 4, "Spec5": 5}
    taxaConstraints = [
        ("felidae", "family"),
        ("ursus", "genus"),
    ]
    taxa = {
        1: {"family": "F"},
        2: {"genus": "U"},
        3: {"family": "F"},
        4: {"family": "F"},
        5: {"family": "F"},
    }
    expected = {}
    assert (
        filterStringNamesByTaxaConstraints(speciesStringDict, taxaConstraints, taxa)
        == expected
    )


def testInferringRemainingLinks():
    newLinks = {2: {}, 3: {}, 5: {}}
    unaccountedFor = [1, 4]
    metas = {1: {}, 2: {}, 3: {}, 4: {}, 5: {}, 6: {}, 7: {}}
    assert inferRemainingLinks(newLinks, unaccountedFor, metas) == {
        1: {},
        2: {},
        3: {},
        4: {},
        5: {},
    }


def testFilteringDatasetMetaNonStrict():
    datasetMetas = {
        1: {"interactionType": "pollination"},
        2: {},
        3: {"interactionType": "predation"},
        4: {},
        5: {"interactionType": "predation"},
    }
    strict = False
    acceptedList = ["predation"]
    tag = "interactionType"
    expected = {
        3: {"interactionType": "predation"},
        5: {"interactionType": "predation"},
        2: {},
        4: {},
    }
    assert (
        filterDatasetMetaData(
            datasetMetas, strict, acceptedList, interactionGenerator, tag
        )
        == expected
    )


def testFilteringDatasetMetaStrict():
    datasetMetas = {
        1: {"interactionType": "pollination"},
        2: {},
        3: {"interactionType": "predation"},
        4: {},
        5: {"interactionType": "predation"},
    }
    strict = True
    acceptedList = ["predation"]
    tag = "interactionType"
    expected = {
        3: {"interactionType": "predation"},
        5: {"interactionType": "predation"},
    }
    assert (
        filterDatasetMetaData(
            datasetMetas, strict, acceptedList, interactionGenerator, tag
        )
        == expected
    )


def testFilteringLinkMetaNonString():
    linkMetas = {
        1: {"interactionType": "pollination"},
        2: {},
        3: {"interactionType": "predation"},
        4: {},
        5: {"interactionType": "predation"},
    }
    strict = False
    obs = ["predation"]
    keyName = "interactionType"
    expected = {
        3: {"interactionType": "predation"},
        5: {"interactionType": "predation"},
    }
    assert takeMatchingFromLinkMetas(linkMetas, obs, interactionGenerator, keyName) == (
        expected,
        [2, 4],
    )


def testSearchingForUnaccountedLinksInDatasetMetas():
    datasetMetas = {
        1: {"interactionType": "pollination"},
        2: {},
        3: {"interactionType": "predation"},
        4: {},
        5: {"interactionType": "predation"},
    }
    newLinks = {2: {}}
    linkMetas = {
        1: {"dId": 1},
        2: {"dId": 2},
        3: {"dId": 1},
        4: {"dId": 1},
        5: {"dId": 3},
    }
    acceptedList = ["predation"]
    unaccountedFor = [1, 3, 4, 5]
    tag = "interactionType"
    expected = ({2: {}, 5: {"dId": 3}}, [])
    assert (
        takeMatchingFromDatasetMetas(
            datasetMetas,
            newLinks,
            linkMetas,
            acceptedList,
            unaccountedFor,
            interactionGenerator,
            tag,
        )
        == expected
    )
