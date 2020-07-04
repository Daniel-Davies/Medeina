import sys
import os
import pytest
import pandas as pd
from Medeina import WebStore
from unittest.mock import MagicMock

# import Medeina.common as MC
from mock import patch
from unittest.mock import patch, MagicMock, call, mock_open

IDTRACKER = (
    "numericCounter-b2ca94aee362f455a41493a0d28b98bc5074065b0f96cbb95028ead20b1c72ea"
)


@patch("Medeina.webStore.WebStore.initialiseLinkIdTracker")
@patch("Medeina.webStore.writeObjToDateStore")
@patch("os.path.exists")
def testFileInitWhenExists(patch_exists, test_patch_write, patch_init_tracker):
    def link_tracker_effect():
        return

    patch_init_tracker.side_effect = link_tracker_effect
    patch_exists.return_value = True
    instance = WebStore("dir")
    test_patch_write.assert_not_called()


@patch("Medeina.webStore.WebStore.initialiseLinkIdTracker")
@patch("Medeina.webStore.writeObjToDateStore")
@patch("os.path.exists")
def testFileInitWhenNew(patch_exists, test_patch_write, patch_init_tracker):
    def link_tracker_effect():
        return

    patch_init_tracker.side_effect = link_tracker_effect
    patch_exists.return_value = False
    instance = WebStore("dir")
    instance.assureExistence("f")
    test_patch_write.assert_called_with("dir", "f", {})


@patch("Medeina.webStore.WebStore.assureExistence")
@patch("Medeina.webStore.retrieveObjFromStore")
@patch("Medeina.webStore.writeObjToDateStore")
@patch("os.path.exists")
def testTrackerIdInitWhenExists(
    patch_exists, test_patch_write, test_patch_read, patch_assure
):
    def assure_existence_effect(a):
        return

    test_patch_read.return_value = {}
    patch_assure.side_effect = assure_existence_effect
    instance = WebStore("dir")
    test_patch_write.assert_called_with("dir", "interactionWeb", {IDTRACKER: 0})


@patch("Medeina.webStore.WebStore.assureExistence")
@patch("Medeina.webStore.retrieveObjFromStore")
@patch("Medeina.webStore.writeObjToDateStore")
@patch("os.path.exists")
def testTrackerIdInitWhenNew(
    patch_exists, test_patch_write, test_patch_read, patch_assure
):
    def assure_existence_effect(a):
        return

    test_patch_read.return_value = {IDTRACKER: 1000}
    patch_assure.side_effect = assure_existence_effect
    instance = WebStore("dir")
    test_patch_write.assert_not_called()


@patch("Medeina.webStore.retrieveObjFromStore")
def testThatIncorrectSpecStringThrows(test_patch_read):
    test_patch_read.return_value = {}
    with pytest.raises(ValueError):
        instance = WebStore()
        instance.parseUserInputToStandardJsonString([])

    try:
        instance = WebStore()
        instance.parseUserInputToStandardJsonString({})
        assert 1 == 1
    except Exception as e:
        assert 1 == 2

    try:
        instance = WebStore()
        instance.parseUserInputToStandardJsonString("")
        assert 1 == 1
    except Exception as e:
        assert 1 == 2
