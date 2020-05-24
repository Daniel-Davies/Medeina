import re
from taxon_parser import TaxonParser, UnparsableNameException


def cleanHeadTailTupleData(headTailTuples):
    return list(map(cleanSingleTuple,headTailTuples))

def cleanSingleTuple(tup):
    return (cleanSingleSpeciesString(tup[0]),cleanSingleSpeciesString(tup[1]))

def cleanSingleSpeciesString(species):
    species = species.replace("-"," ")
    species = re.sub(r'\{.*?\}', '', species)
    species = re.sub(r'\(.*?\)', '', species)
    species = re.sub(r'\[.*?\]', '', species)
    species = re.sub('[\W_]+ ',' ', species)
    species = re.sub(' +', ' ', species)
    species = extractEcologicalFlags(species)
    species = species.lower()
    return species

def extractEcologicalFlags(species):
    parser = TaxonParser(species)
    try: 
        parsed_name = parser.parse()
        if not parsed_name.isTrinomial():
            species = parsed_name.genus + " " + parsed_name.getTerminalEpithet()
        else:
            species = parsed_name.genus + " " + parsed_name.specificEpithet
        return species
    except:
        return ''

print(cleanSingleSpeciesString("tundus jun mendosa"))