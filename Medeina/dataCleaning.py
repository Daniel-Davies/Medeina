import re
from taxon_parser import TaxonParser, UnparsableNameException


def cleanHeadTailTupleData(headTailTuples):
    return list(filter(containsEmpty, map(cleanSingleTuple, headTailTuples)))


def containsEmpty(tup):
    return not (len(tup[0]) == 0 or len(tup[1]) == 0)


def cleanSingleTuple(tup):
    return (cleanSingleSpeciesString(tup[0]), cleanSingleSpeciesString(tup[1]), tup[2])


def cleanSingleSpeciesString(species, strict=True):
    species = species.lower()
    species = species.strip()
    species = species.replace("-", " ")
    species = re.sub(r"\{.*?\}", "", species)
    species = re.sub(r"\(.*?\)", "", species)
    species = re.sub(r"\[.*?\]", "", species)
    species = re.sub("[^a-zA-Z ]+", " ", species)
    species = re.sub(" sp ", " ", species)  # Nomenclature flags not cleared
    if species[-2:] == "sp":
        species = species[:-2]
    species = re.sub(r"\b\w{1}\b", "", species)
    species = re.sub(" +", " ", species)
    if strict:
        species = cleanNomenclatureFlags(species)
    else:
        species = bestEffortCleanNomenclatureFlags(species)
    species = species.lower()
    species = re.sub(" +", " ", species)
    species = species.strip()
    return species


def cleanNomenclatureFlags(species):
    parser = TaxonParser(species)
    try:
        parsed_name = parser.parse()
        if parsed_name.genus == "?":
            return parsed_name.specificEpithet + " " + parsed_name.infraspecificEpithet
        if not parsed_name.isTrinomial():
            species = parsed_name.genus + " " + parsed_name.getTerminalEpithet()
        else:
            species = parsed_name.genus + " " + parsed_name.specificEpithet
        return species
    except Exception as e:
        return ""


def bestEffortCleanNomenclatureFlags(species):
    if len(species.split(" ")) == 1:
        return species
    parser = TaxonParser(species)
    try:
        parsed_name = parser.parse()
        if parsed_name.genus == "?":
            return parsed_name.specificEpithet + " " + parsed_name.infraspecificEpithet

        if not parsed_name.isTrinomial():
            species = parsed_name.genus + " " + parsed_name.getTerminalEpithet()
        else:
            species = parsed_name.genus + " " + parsed_name.specificEpithet
        return species
    except Exception as e:
        return species
