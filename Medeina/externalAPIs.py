from EcoNameTranslator import to_species, classify
import requests
import itertools
from collections import Counter
from .parsingFunctionality import *
from .config import *
from .common import mostCommonInList


def retrieveTaxonomicDataFromAPI(species, includeInvalid):
    index = classify(species)
    index = indexToTuples(index)
    return list(map(lambda x: (x[0], x[2]), index))


def translateToSpeciesScientificFormatOnly(cleanedHeadTailTupleData):
    speciesList = list(
        set(itertools.chain(*keepInteractionPartOnly(cleanedHeadTailTupleData)))
    )
    speciesMapping = translateSpeciesList(speciesList)
    cleanedHeadTailTupleData = list(
        map(
            lambda x: (speciesMapping[x[0]][1], speciesMapping[x[1]][1], x[2]),
            cleanedHeadTailTupleData,
        )
    )
    cleanedHeadTailTupleData = list(
        map(
            lambda x: (list(itertools.product(x[0], x[1])), x[2]),
            cleanedHeadTailTupleData,
        )
    )
    cleanedHeadTailTupleData = list(
        map(
            lambda x: [(pred, prey, x[1]) for pred, prey in x[0]],
            cleanedHeadTailTupleData,
        )
    )
    cleanedHeadTailTupleData = list(itertools.chain(*cleanedHeadTailTupleData))
    cleanedHeadTailTupleData = makeUnique(cleanedHeadTailTupleData)
    return cleanedHeadTailTupleData


def translateSpeciesList(species):
    oIndex = to_species(species, sanityCorrect=True)
    index = indexToTuples(oIndex)
    enrichedResults = enrichSpeciesToFullTaxonomy(index)
    for k, (real, cleaned, lst) in enumerate(enrichedResults):
        groupingByFamily = summaryStatsPerCategory(lst).get("family", "")
        if len(groupingByFamily) < 2:
            enrichedResults[k] = (real, cleaned, oIndex[real][1])
        else:
            rankedGrouping = sorted(
                groupingByFamily.items(), key=lambda x: x[1], reverse=True
            )
            enrichedResults[k] = (
                real,
                cleaned,
                decideTranslationOnGroupStats(rankedGrouping, lst),
            )

    enrichedResults = list(
        map(
            lambda x: (x[0], x[1], list(map(lambda y: y.lower(), x[2]))),
            enrichedResults,
        )
    )
    return dict(list(map(lambda x: [x[0], [*x[1:]]], enrichedResults)))


def enrichSpeciesToFullTaxonomy(index):
    return list(
        map(
            lambda x: [
                x[0],
                x[1],
                list(map(lambda y: y[1][1], list(classify(x[2]).items()))),
            ],
            index,
        )
    )


def decideTranslationOnGroupStats(rankedGrouping, taxaList):
    leading = rankedGrouping[0][1]
    total = sum([item[1] for item in rankedGrouping])
    if (leading / total) <= 0.75:
        out = rankedGrouping[1:]
        if not all([(val[1] <= 0.1 * total and leading >= 0.5 * total) for val in out]):
            return []

    return takeSpeciesMatchingGroupOnly(rankedGrouping[0][0], "family", taxaList)


def summaryStatsPerCategory(result):
    groups = {
        cat: list(map(lambda x: x.get(cat, ""), result)) for cat in TAXA_OF_INTEREST
    }
    summaryStats = {k: grouping(v) for (k, v) in groups.items()}
    if "" in summaryStats:
        del summaryStats[""]
    return summaryStats


def grouping(values):
    baseResults = dict(Counter(values))
    if "" in baseResults:
        del baseResults[""]
    return baseResults


def indexToTuples(index):
    return list(map(lambda x: [x, *index[x]], list(index.keys())))


def takeSpeciesMatchingGroupOnly(group, level, data):
    species = []
    for item in data:
        if item.get(level, "") == group:
            if "species" in item:
                species.append(item["species"])

    return species
