import sys
import os
import pytest
import pandas as pd
from Medeina.Web import Web
from unittest.mock import MagicMock
from Medeina.config import *

# import Medeina.common as MC
from mock import patch
from unittest.mock import patch, MagicMock, call, mock_open

IDTRACKER = (
    "numericCounter-b2ca94aee362f455a41493a0d28b98bc5074065b0f96cbb95028ead20b1c72ea"
)


@patch.object(sys.modules["Medeina.Web"], "retrieveObjFromStore")
@patch.object(sys.modules["Medeina.Web"], "writeObjToDateStore")
def testAddingTaxaExceptionsFresh(patch_write, patch_retr):
    def retrDynamicReturn(a, b):
        if b == REALNAMES:
            return {"panthera tigris": 1}
        return {}

    patch_retr.side_effect = retrDynamicReturn
    species = "panthera tigris"
    consumer = "family"
    resource = "genus"
    instance = Web(path="dir")
    instance.add_taxonomic_exception(species, consumer, resource, True)
    patch_write.assert_called_with(
        "dir",
        "reorderedTaxaInteractions",
        {"panthera tigris": {"consumer": "family", "resource": "genus"}},
    )


@patch.object(sys.modules["Medeina.Web"], "retrieveObjFromStore")
@patch.object(sys.modules["Medeina.Web"], "writeObjToDateStore")
def testAddingTaxaExceptionsExisting(patch_write, patch_retr):
    def retrDynamicReturn(a, b):
        if b == REALNAMES:
            return {"felis catus": 1, "panthera tigris": 2}
        elif b == EXCEPTIONS:
            return {"panthera tigris": {"consumer": "family", "resource": "genus"}}
        return {}

    patch_retr.side_effect = retrDynamicReturn
    species = "felis catus"
    consumer = "family"
    resource = "genus"
    instance = Web(path="dir")
    instance.add_taxonomic_exception(species, consumer, resource, True)
    patch_write.assert_called_with(
        "dir",
        "reorderedTaxaInteractions",
        {
            "panthera tigris": {"consumer": "family", "resource": "genus"},
            "felis catus": {"consumer": "family", "resource": "genus"},
        },
    )


@patch.object(sys.modules["Medeina.Web"], "retrieveObjFromStore")
@patch.object(sys.modules["Medeina.Web"], "writeObjToDateStore")
def testAddingTaxaExceptionsInvalid(patch_write, patch_retr):
    def retrDynamicReturn(a, b):
        if b == REALNAMES:
            return {"felis catus": 1, "panthera tigris": 2}
        elif b == EXCEPTIONS:
            return {}
        return {}

    patch_retr.side_effect = retrDynamicReturn
    species = "felis"
    consumer = "family"
    resource = "genus"
    instance = Web(path="dir")
    with pytest.raises(ValueError):
        instance.add_taxonomic_exception(species, consumer, resource, True)


@patch.object(sys.modules["Medeina.Web"], "retrieveObjFromStore")
def testFilteringByDatasetIdsExpected(patch_retr):
    def retrDynamicReturn(a, b):
        if b == REALNAMES:
            return {"felis catus": 1, "panthera tigris": 2, "vulpes vulpes": 3}
        elif b == EXCEPTIONS:
            return {}
        elif b == WEB:
            return {IDTRACKER: 5, 2: {1: [1, 3], 3: [2]}, 3: {1: [4]}}
        elif b == TAXA:
            return {
                1: {"family": "felidae"},
                2: {"family": "felidae"},
                3: {"family": "canidea"},
            }
        elif b == LINKS:
            return {1: {"dId": 2}, 2: {"dId": 1}, 3: {"dId": 1}, 4: {"dId": 2}}
        elif b == DATASETS:
            return {1: {}, 2: {}}
        return {}

    patch_retr.side_effect = retrDynamicReturn
    instance = Web(path="dir")
    newWeb = instance.filter_by_dataset_id([1])

    assert newWeb.datasetMetas == {1: {}}
    assert newWeb.linkMetas == {2: {"dId": 1}, 3: {"dId": 1}}
    assert newWeb.interactions == {IDTRACKER: 5, 2: {1: [3], 3: [2]}}
    assert newWeb.stringNames == {
        "felis catus": 1,
        "panthera tigris": 2,
        "vulpes vulpes": 3,
    }
    assert newWeb.taxa == {
        1: {"family": "felidae"},
        2: {"family": "felidae"},
        3: {"family": "canidea"},
    }


@patch.object(sys.modules["Medeina.Web"], "retrieveObjFromStore")
def testFilteringByDatasetIdsEmpty(patch_retr):
    def retrDynamicReturn(a, b):
        if b == REALNAMES:
            return {"felis catus": 1, "panthera tigris": 2, "vulpes vulpes": 3}
        elif b == EXCEPTIONS:
            return {}
        elif b == WEB:
            return {IDTRACKER: 5, 2: {1: [1, 3], 3: [2]}, 3: {1: [4]}}
        elif b == TAXA:
            return {
                1: {"family": "felidae"},
                2: {"family": "felidae"},
                3: {"family": "canidea"},
            }
        elif b == LINKS:
            return {1: {"dId": 2}, 2: {"dId": 1}, 3: {"dId": 1}, 4: {"dId": 2}}
        elif b == DATASETS:
            return {1: {}, 2: {}}
        return {}

    patch_retr.side_effect = retrDynamicReturn
    instance = Web(path="dir")
    newWeb = instance.filter_by_dataset_id([])

    assert newWeb.datasetMetas == {}
    assert newWeb.linkMetas == {}
    assert newWeb.interactions == {IDTRACKER: 5}
    assert newWeb.stringNames == {}
    assert newWeb.taxa == {}


@patch.object(sys.modules["Medeina.Web"], "retrieveObjFromStore")
def testFilteringByDatasetIdsFull(patch_retr):
    def retrDynamicReturn(a, b):
        if b == REALNAMES:
            return {"felis catus": 1, "panthera tigris": 2, "vulpes vulpes": 3}
        elif b == EXCEPTIONS:
            return {}
        elif b == WEB:
            return {IDTRACKER: 5, 2: {1: [1, 3], 3: [2]}, 3: {1: [4]}}
        elif b == TAXA:
            return {
                1: {"family": "felidae"},
                2: {"family": "felidae"},
                3: {"family": "canidea"},
            }
        elif b == LINKS:
            return {1: {"dId": 2}, 2: {"dId": 1}, 3: {"dId": 1}, 4: {"dId": 2}}
        elif b == DATASETS:
            return {1: {}, 2: {}}
        return {}

    patch_retr.side_effect = retrDynamicReturn
    instance = Web(path="dir")
    newWeb = instance.filter_by_dataset_id([1, 2])

    assert newWeb.datasetMetas == retrDynamicReturn(1, DATASETS)
    assert newWeb.linkMetas == retrDynamicReturn(1, LINKS)
    assert newWeb.interactions == retrDynamicReturn(1, WEB)
    assert newWeb.stringNames == retrDynamicReturn(1, REALNAMES)
    assert newWeb.taxa == retrDynamicReturn(1, TAXA)


@patch.object(sys.modules["Medeina.Web"], "retrieveObjFromStore")
def testReplicatingWebExpected(patch_retr):
    def retrDynamicReturn(a, b):
        if b == REALNAMES:
            return {"felis catus": 1, "panthera tigris": 2, "vulpes vulpes": 3}
        elif b == EXCEPTIONS:
            return {}
        elif b == WEB:
            return {IDTRACKER: 5, 2: {1: [1, 3], 3: [2]}, 3: {1: [4]}}
        elif b == TAXA:
            return {
                1: {"family": "felidae"},
                2: {"family": "felidae"},
                3: {"family": "canidea"},
            }
        elif b == LINKS:
            return {1: {"dId": 2}, 2: {"dId": 1}, 3: {"dId": 1}, 4: {"dId": 2}}
        elif b == DATASETS:
            return {1: {}, 2: {}}
        return {}

    patch_retr.side_effect = retrDynamicReturn
    instance = Web(path="dir")
    newWeb = instance.replicateWeb()

    assert newWeb.datasetMetas == retrDynamicReturn(1, DATASETS)
    assert newWeb.linkMetas == retrDynamicReturn(1, LINKS)
    assert newWeb.interactions == retrDynamicReturn(1, WEB)
    assert newWeb.stringNames == retrDynamicReturn(1, REALNAMES)
    assert newWeb.taxa == retrDynamicReturn(1, TAXA)


@patch.object(sys.modules["Medeina.Web"], "retrieveObjFromStore")
def testReplicatingWebBlank(patch_retr):
    def retrDynamicReturn(a, b):
        if b == REALNAMES:
            return {}
        elif b == EXCEPTIONS:
            return {}
        elif b == WEB:
            return {IDTRACKER: 0}
        elif b == TAXA:
            return {}
        elif b == LINKS:
            return {}
        elif b == DATASETS:
            return {}
        return {}

    patch_retr.side_effect = retrDynamicReturn
    instance = Web(path="dir")
    newWeb = instance.replicateWeb()

    assert newWeb.datasetMetas == retrDynamicReturn(1, DATASETS)
    assert newWeb.linkMetas == retrDynamicReturn(1, LINKS)
    assert newWeb.interactions == retrDynamicReturn(1, WEB)
    assert newWeb.stringNames == retrDynamicReturn(1, REALNAMES)
    assert newWeb.taxa == retrDynamicReturn(1, TAXA)


@patch.object(sys.modules["Medeina.Web"], "retrieveObjFromStore")
def testFilteringByObservationTypeAllOnLinks(patch_retr):
    def retrDynamicReturn(a, b):
        if b == REALNAMES:
            return {"felis catus": 1, "panthera tigris": 2, "vulpes vulpes": 3}
        elif b == EXCEPTIONS:
            return {}
        elif b == WEB:
            return {IDTRACKER: 5, 2: {1: [1, 3], 3: [2]}, 3: {1: [4]}}
        elif b == TAXA:
            return {
                1: {"family": "felidae"},
                2: {"family": "felidae"},
                3: {"family": "canidea"},
            }
        elif b == LINKS:
            return {
                1: {"dId": 2, "evidencedBy": "observation"},
                2: {"dId": 1, "evidencedBy": "observation"},
                3: {"dId": 1},
                4: {"dId": 2, "evidencedBy": "inferred"},
            }
        elif b == DATASETS:
            return {1: {}, 2: {}}
        return {}

    patch_retr.side_effect = retrDynamicReturn
    instance = Web(path="dir")
    newWeb = instance.filter_by_observation_type(["observation"])
    assert newWeb.datasetMetas == {1: {}, 2: {}}
    assert newWeb.linkMetas == {
        1: {"dId": 2, "evidencedBy": "observation"},
        2: {"dId": 1, "evidencedBy": "observation"},
        3: {"dId": 1},
    }
    assert newWeb.interactions == {2: {1: [1, 3], 3: [2]}, IDTRACKER: 5}
    assert newWeb.stringNames == {
        "felis catus": 1,
        "panthera tigris": 2,
        "vulpes vulpes": 3,
    }
    assert newWeb.taxa == {
        1: {"family": "felidae"},
        2: {"family": "felidae"},
        3: {"family": "canidea"},
    }


@patch.object(sys.modules["Medeina.Web"], "retrieveObjFromStore")
def testFilteringByObservationTypeAllDatasetMetas(patch_retr):
    def retrDynamicReturn(a, b):
        if b == REALNAMES:
            return {"felis catus": 1, "panthera tigris": 2, "vulpes vulpes": 3}
        elif b == EXCEPTIONS:
            return {}
        elif b == WEB:
            return {IDTRACKER: 5, 2: {1: [1, 3], 3: [2]}, 3: {1: [4]}}
        elif b == TAXA:
            return {
                1: {"family": "felidae"},
                2: {"family": "felidae"},
                3: {"family": "canidea"},
            }
        elif b == LINKS:
            return {1: {"dId": 2}, 2: {"dId": 1}, 3: {"dId": 1}, 4: {"dId": 2}}
        elif b == DATASETS:
            return {1: {"evidencedBy": "observation"}, 2: {"evidencedBy": "inferred"}}
        return {}

    patch_retr.side_effect = retrDynamicReturn
    instance = Web(path="dir")
    newWeb = instance.filter_by_observation_type(["observation"])
    assert newWeb.datasetMetas == {1: {"evidencedBy": "observation"}}
    assert newWeb.linkMetas == {2: {"dId": 1}, 3: {"dId": 1}}
    assert newWeb.interactions == {2: {1: [3], 3: [2]}, IDTRACKER: 5}
    assert newWeb.stringNames == {
        "felis catus": 1,
        "panthera tigris": 2,
        "vulpes vulpes": 3,
    }
    assert newWeb.taxa == {
        1: {"family": "felidae"},
        2: {"family": "felidae"},
        3: {"family": "canidea"},
    }


@patch.object(sys.modules["Medeina.Web"], "retrieveObjFromStore")
def testFilteringByObservationTypeMixedDatasetMetasAndLinkMetas(patch_retr):
    def retrDynamicReturn(a, b):
        if b == REALNAMES:
            return {"felis catus": 1, "panthera tigris": 2, "vulpes vulpes": 3}
        elif b == EXCEPTIONS:
            return {}
        elif b == WEB:
            return {IDTRACKER: 5, 2: {1: [1, 3], 3: [2]}, 3: {1: [4]}}
        elif b == TAXA:
            return {
                1: {"family": "felidae"},
                2: {"family": "felidae"},
                3: {"family": "canidea"},
            }
        elif b == LINKS:
            return {
                1: {"dId": 2, "evidencedBy": "observation"},
                2: {"dId": 1},
                3: {"dId": 1},
                4: {"dId": 2, "evidencedBy": "inferred"},
            }
        elif b == DATASETS:
            return {1: {"evidencedBy": "observation"}, 2: {}}
        return {}

    patch_retr.side_effect = retrDynamicReturn
    instance = Web(path="dir")
    newWeb = instance.filter_by_observation_type(["observation"])
    assert newWeb.datasetMetas == {1: {"evidencedBy": "observation"}, 2: {}}
    assert newWeb.linkMetas == {
        1: {"dId": 2, "evidencedBy": "observation"},
        2: {"dId": 1},
        3: {"dId": 1},
    }
    assert newWeb.interactions == {2: {1: [1, 3], 3: [2]}, IDTRACKER: 5}
    assert newWeb.stringNames == {
        "felis catus": 1,
        "panthera tigris": 2,
        "vulpes vulpes": 3,
    }
    assert newWeb.taxa == {
        1: {"family": "felidae"},
        2: {"family": "felidae"},
        3: {"family": "canidea"},
    }


@patch.object(sys.modules["Medeina.Web"], "retrieveObjFromStore")
def testFilteringOnTaxa(patch_retr):
    def retrDynamicReturn(a, b):
        if b == REALNAMES:
            return {"felis catus": 1, "panthera tigris": 2, "vulpes vulpes": 3}
        elif b == EXCEPTIONS:
            return {}
        elif b == WEB:
            return {IDTRACKER: 5, 2: {1: [1, 3], 3: [2]}, 3: {1: [4]}}
        elif b == TAXA:
            return {
                1: {"family": "felidae"},
                2: {"family": "felidae"},
                3: {"family": "canidea"},
            }
        elif b == LINKS:
            return {
                1: {"dId": 2, "evidencedBy": "observation"},
                2: {"dId": 1, "evidencedBy": "observation"},
                3: {"dId": 1},
                4: {"dId": 2, "evidencedBy": "inferred"},
            }
        elif b == DATASETS:
            return {1: {}, 2: {}}
        return {}

    patch_retr.side_effect = retrDynamicReturn
    instance = Web(path="dir")
    newWeb = instance.filterByTaxa([("felidae", "family")])
    assert newWeb.datasetMetas == {1: {}, 2: {}}
    assert newWeb.linkMetas == {
        1: {"dId": 2, "evidencedBy": "observation"},
        3: {"dId": 1},
    }
    assert newWeb.interactions == {2: {1: [1, 3]}}
    assert newWeb.stringNames == {"felis catus": 1, "panthera tigris": 2}
    assert newWeb.taxa == {1: {"family": "felidae"}, 2: {"family": "felidae"}}
