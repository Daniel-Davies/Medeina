import sys
import os

from Medeina.dataCleaning import cleanSingleSpeciesString


def test_capitals():
    assert cleanSingleSpeciesString("HELLO HELLO") == "hello hello"
    assert cleanSingleSpeciesString("Vulpes vulpes") == "vulpes vulpes"
    assert cleanSingleSpeciesString("Vulpes Vulpes") == "vulpes vulpes"
    assert cleanSingleSpeciesString("Vulpes") == ""


def test_specials_chars():
    assert cleanSingleSpeciesString("Vulpes-Vulpes") == "vulpes vulpes"
    assert cleanSingleSpeciesString("#vulpes # vulpes") == "vulpes vulpes"
    assert cleanSingleSpeciesString("vulpes.vulpes") == "vulpes vulpes"
    assert cleanSingleSpeciesString("vulpes!!!!") == ""


def test_nomenclature():
    assert cleanSingleSpeciesString("Vulpes vulpes sp") == "vulpes vulpes"
    assert cleanSingleSpeciesString("vulpes cf vulpes") == "vulpes vulpes"
    assert cleanSingleSpeciesString("vulpes (jun) vulpes") == "vulpes vulpes"
    assert cleanSingleSpeciesString("vulpes vulpes agg.") == "vulpes vulpes"


def test_longerNames():
    assert cleanSingleSpeciesString("Vulpes vulpes sp. index") == "vulpes vulpes"
    assert cleanSingleSpeciesString("vulpes vulpes other") == "vulpes vulpes"
