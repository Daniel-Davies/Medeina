import os

########################################
############### List Based #############
########################################
def freshwater():
    dct = {}
    dct['interactionType'] = "predation"

    dct['encoding'] = {}
    dct['encoding']['interactionFormat'] = 'pair'
    dct['encoding']['head'] = 'consumer'
    dct['encoding']['tail'] = 'resource'
    dct['encoding']['path'] = "C:/Users/davie/Desktop/Masters/Dissertation/Code/DissertationCode/Eigg/Utilities/RelevantDatasets/production/freshwater.csv"

    dct['encoding']['evidencedBy'] = 'link.evidence'
    dct['encoding']['source'] = 'full.source'
    return [dct]

def GlobAL():
    dct = {}
    dct['encoding'] = {}
    dct['encoding']['interactionFormat'] = 'pair'
    dct['encoding']['head'] = 'con.taxonomy'
    dct['encoding']['tail'] = 'res.taxonomy'
    dct['encoding']['path'] = "C:/Users/davie/Desktop/Masters/Dissertation/Code/DissertationCode/Eigg/Utilities/RelevantDatasets/production/2018GlobAL.csv"

    dct['encoding']['source'] = 'link.citation'
    dct['encoding']['interactionType'] = "interaction.type"
    dct['encoding']['location'] = 'geographic.location'
    return [dct]

def plantInsects():
    dct = {}

    dct['source'] = 'https://iwdb.nceas.ucsb.edu/resources.html'
    dct['interactionType'] = 'plant-insect'

    dct['encoding'] = {}
    dct['encoding']['interactionFormat'] = 'pair'
    dct['encoding']['head'] = 'Insect species'
    dct['encoding']['tail'] = 'Flower Species'
    dct['encoding']['path'] = "C:/Users/davie/Desktop/Masters/Dissertation/Code/DissertationCode/Eigg/Utilities/RelevantDatasets/production/plantInsects.csv"

    dct['encoding']['location'] = 'site'
    return [dct]

def plantPollinator():
    dct = {}
    dct['encoding'] = {}
    dct['encoding']['interactionFormat'] = 'pair'
    dct['encoding']['head'] = 'POLLINATOR_NAME'
    dct['encoding']['tail'] = 'PLANT_NAME'
    dct['encoding']['path'] = "C:/Users/davie/Desktop/Masters/Dissertation/Code/DissertationCode/Eigg/Utilities/RelevantDatasets/production/plantPollinator.csv"

    dct['interactionType'] = 'pollination'
    dct['source'] = "Adams D.E., Perkins W.E. & Estes J.R. (1981). Pollination Systems in Paspalum dilatatum Poir. (Poaceae): An Example of Insect Pollination in a Temperate Grass. American Journal of Botany, 68, 389-394. Asher J. (1997). Butterflies for the New Millennium - project and programme. ITE Monks Wood, Huntingdon. Clifford H.T. (1964). Insect pollination of grasses. Australian Journal of Entomology, 3, 74-74. Hill M.O., Preston C.D. & Roy D. (2004). PLANTATT-attributes of British and Irish plants: status, size, life history, geography and habitats. Centre for Ecology & Hydrology"
    return [dct]

def AtlanticFrugivory():
    dct = {}

    dct['source'] = "Bello, C., Galetti, M., Montan, D., Pizo, M.A., Mariguela, T.C., Culot, L., Bufalo, F., Labecca, F., Pedrosa, F., Constantini, R., Emer, C., Silva, W.R., da Silva, F.R., Ovaskainen, O. and Jordano, P. (2017), Atlantic frugivory: a plant–frugivore interaction data set for the Atlantic Forest. Ecology, 98: 1729-1729. doi:10.1002/ecy.1818"
    dct["interactionType"] = "frugivory"

    dct['encoding'] = {}
    dct['encoding']['interactionFormat'] = 'pair'
    dct['encoding']['head'] = 'Frugivore_Species'
    dct['encoding']['tail'] = 'Plant_Species'
    dct['encoding']['path'] = "C:/Users/davie/Desktop/Masters/Dissertation/Code/DissertationCode/Eigg/Utilities/RelevantDatasets/InsightPending/ATLANTIC_frugivory.csv"
    return [dct]

def Otago():
    dct = {}

    dct['location'] = "Otago, New Zealand"
    dct['source'] = 'Kim N. Mouritsen, Robert Poulin, John P. McLaughlin and David W. Thieltges. 2011. Food web including metazoan parasites for an intertidal ecosystem in New Zealand. Ecology 92:2006.'

    dct['encoding'] = {}
    dct['encoding']['interactionFormat'] = 'pair'
    dct['encoding']['head'] = 'ConsumerSpeciesID'
    dct['encoding']['tail'] = 'ResourceSpeciesID'
    dct['encoding']['path'] = "C:/Users/davie/Desktop/Masters/Dissertation/Code/DissertationCode/Eigg/Utilities/RelevantDatasets/InsightPending/Dropped/Otago/Otago.csv"
    dct['encoding']['interactionType'] = "LinkType"

    return [dct]


def Mangal():
    filenames = os.listdir("C:/Users/davie/Desktop/Masters/Dissertation/Code/DissertationCode/Eigg/Utilities/RelevantDatasets/production/Mangal")
    dcts = []
    for f in filenames:
        dct = {}

        dct['source'] = f[:-4]+" (aka network-id) from Mangal.io"

        dct['encoding'] = {}
        dct['encoding']['interactionFormat'] = 'pair'
        dct['encoding']['head'] = 'Predator'
        dct['encoding']['tail'] = 'Prey'
        dct['encoding']['path'] = "C:/Users/davie/Desktop/Masters/Dissertation/Code/DissertationCode/Eigg/Utilities/RelevantDatasets/production/Mangal/"+f

        dcts.append(dct)

    return dcts

########################################
############# Matrix Based #############
########################################

def janePollinators():
    dct = {}
    dct['source'] = 'Memmott, J. (1999), The structure of a plant‐pollinator food web. Ecology Letters, 2: 276-280. doi:10.1046/j.1461-0248.1999.00087.x'
    dct['location'] = "Bristol, England"
    dct['interactionType'] = 'pollination'
    dct['evidencedBy'] = 'observation'

    dct['encoding'] = {}
    dct['encoding']['interactionFormat'] = 'matrix'
    dct['encoding']['headingCorner'] = '(3,2)'
    dct['encoding']['dataCorner'] = '(5,4)'
    dct['encoding']['nameDepth'] = 2
    dct['encoding']['path'] = "C:/Users/davie/Desktop/Masters/Dissertation/Code/DissertationCode/Eigg/Utilities/RelevantDatasets/production/janePollinators.csv"

    return [dct]

def leatherBritain():
    dct = {}
    
    dct['source'] = 'Leather, Simon R. “Feeding Specialisation and Host Distribution of British and Finnish Prunus Feeding Macrolepidoptera.” Oikos, vol. 60, no. 1, 1991, pp. 40–48. JSTOR, '
    dct['location'] = "United Kingdom"
    dct['interactionType'] = 'plant-herbivore'

    dct['encoding'] = {}
    dct['encoding']['interactionFormat'] = 'matrix'
    dct['encoding']['headingCorner'] = '(1,1)'
    dct['encoding']['dataCorner'] = '(4,4)'
    dct['encoding']['nameDepth'] = 2
    dct['encoding']['path'] = "C:/Users/davie/Desktop/Masters/Dissertation/Code/DissertationCode/Eigg/Utilities/RelevantDatasets/production/leatherBritain.xls"
    return [dct] 

def leatherFinland():
    dct = {}

    dct['source'] = 'Leather, Simon R. “Feeding Specialisation and Host Distribution of British and Finnish Prunus Feeding Macrolepidoptera.” Oikos, vol. 60, no. 1, 1991, pp. 40–48. JSTOR, '
    dct['location'] = "Finland"
    dct['interactionType'] = 'plant-herbivore'

    dct['encoding'] = {}
    dct['encoding']['interactionFormat'] = 'matrix'
    dct['encoding']['headingCorner'] = '(1,1)'
    dct['encoding']['dataCorner'] = '(4,4)'
    dct['encoding']['nameDepth'] = 2
    dct['encoding']['path'] = "C:/Users/davie/Desktop/Masters/Dissertation/Code/DissertationCode/Eigg/Utilities/RelevantDatasets/production/leatherFinland.xls"
    return [dct] 

def sbPredatorPreyMatrix():
    dct = {}

    dct['source'] = 'Parasites dominate food web links Kevin D. Lafferty, Andrew P. Dobson, Armand M. Kuris Proceedings of the National Academy of Sciences Jul 2006, 103 (30) 11211-11216; DOI: 10.1073/pnas.0604755103'
    dct['interactionType'] = 'predation'
    dct['location'] = 'Santa Barbara, California, USA'

    dct['encoding'] = {}
    dct['encoding']['interactionFormat'] = 'matrix'
    dct['encoding']['headingCorner'] = '(2,3)'
    dct['encoding']['dataCorner'] = '(3,4)'
    dct['encoding']['nameDepth'] = 1
    dct['encoding']['path'] = "C:/Users/davie/Desktop/Masters/Dissertation/Code/DissertationCode/Eigg/Utilities/RelevantDatasets/production/sbPredatorPreyMatrix.csv"
    return [dct]

def sorensen_1981_woodland():
    dct = {}

    dct['source'] = 'Sorensen, A.E. Interactions between birds and fruit in a temperate woodland. Oecologia 50, 242–249 (1981). https://doi.org/10.1007/BF00348046'
    dct['interactionType'] = 'frugivory'
    dct['location'] = 'United Kingdom'
    dct['evidencedBy'] = 'observation'

    dct['encoding'] = {}
    dct['encoding']['interactionFormat'] = 'matrix'
    dct['encoding']['headingCorner'] = '(1,1)'
    dct['encoding']['dataCorner'] = '(5,5)'
    dct['encoding']['nameDepth'] = 1
    dct['encoding']['path'] = "C:/Users/davie/Desktop/Masters/Dissertation/Code/DissertationCode/Eigg/Utilities/RelevantDatasets/production/sorensen_1981_woodland.xls"
    return [dct] 

def dryad():
    filenames = ['kongsfjorden_spames','loughhyne_spnames','reef_spnames','stmarks_spnames','weddell_spnames','ythan_spnames']
    filenames = list(map(lambda x: x+'.xls',filenames))
    dcts = []
    for f in filenames:
        dct = {}
        dct['source'] = 'Cirtwill, A.R. and Eklöf, A. (2018), Feeding environment and other traits shape species’ roles in marine food webs. Ecol Lett, 21: 875-884. doi:10.1111/ele.12955'
        dct['interactionType'] = 'predation'

        dct['encoding'] = {}
        dct['encoding']['interactionFormat'] = 'matrix'
        dct['encoding']['headingCorner'] = '(1,1)'
        dct['encoding']['dataCorner'] = '(2,2)'
        dct['encoding']['nameDepth'] = 1
        dct['encoding']['path'] = "C:/Users/davie/Desktop/Masters/Dissertation/Code/DissertationCode/Eigg/Utilities/RelevantDatasets/production/dryad/"+f

        dcts.append(dct)

    return dcts

def FoodsWebsCanberra():
    filenames = ["WEB"+str(i) for i in list(set(range(1,360))-set([90,333]))]
    filenames = list(map(lambda x: x+'.csv',filenames))
    dcts = []
    for f in filenames:
        dct = {}

        dct['source'] = "https://www.globalwebdb.com/ - " + f.lower()
        dct['encoding'] = {}
        dct['encoding']['interactionFormat'] = 'matrix'
        dct['encoding']['headingCorner'] = '(1,2)'
        dct['encoding']['dataCorner'] = '(2,3)'
        dct['encoding']['nameDepth'] = 1
        dct['encoding']['path'] = "C:/Users/davie/Desktop/Masters/Dissertation/Code/DissertationCode/Eigg/Utilities/RelevantDatasets/production/FoodsWebsCanberra/"+f
        dct['encoding']['metaData'] = []

        dcts.append(dct)

    return dcts

def NewZealand():
    filenames = os.listdir('C:/Users/davie/Desktop/Masters/Dissertation/Code/DissertationCode/Eigg/Utilities/RelevantDatasets/newZealandAllPredatorPrey/')
    dcts = []
    for f in filenames:
        dct = {}

        dct['interactionType'] = 'predation'
        dct['source'] = 'Thompson, R.M. and Townsend, C.R. (2005), Energy availability, spatial heterogeneity and ecosystem size predict food‐web structure in streams. Oikos, 108: 137-148. doi:10.1111/j.0030-1299.2005.11600.x' 
        dct['location'] = "New Zealand"

        dct['encoding'] = {}
        dct['encoding']['interactionFormat'] = 'matrix'
        dct['encoding']['headingCorner'] = '(1,1)'
        dct['encoding']['dataCorner'] = '(2,2)'
        dct['encoding']['nameDepth'] = 1
        dct['encoding']['path'] = "C:/Users/davie/Desktop/Masters/Dissertation/Code/DissertationCode/Eigg/Utilities/RelevantDatasets/newZealandAllPredatorPrey/"+f

        dcts.append(dct)
    return dcts

def plantPollinatorUSA():
    dct = {}
    
    dct['source'] = 'Schemske, Douglas & Willson, Mary & Melampy, Michael & Miller, Linda & Verner, Louis & Schemske, Kathleen & Best, Louis. (1978). Flowering Ecology of Some Spring Woodland Herbs. Ecology. 59. 10.2307/1936379. '
    dct['interactionType'] = 'pollination'
    dct['location'] = 'United States'

    dct['encoding'] = {}
    dct['encoding']['interactionFormat'] = 'matrix'
    dct['encoding']['headingCorner'] = '(1,1)'
    dct['encoding']['dataCorner'] = '(4,5)'
    dct['encoding']['nameDepth'] = 2
    dct['encoding']['path'] = "C:/Users/davie/Desktop/Masters/Dissertation/Code/DissertationCode/Eigg/Utilities/RelevantDatasets/production/BaseCSV/plantPollinatorUSA.xls"
    return [dct] 

def plantSeed():
    dct = {}
    
    dct['source'] = 'https://iwdb.nceas.ucsb.edu/resources.html'    
    dct['interactionType'] = 'seed-dispersal'

    dct['encoding'] = {}
    dct['encoding']['interactionFormat'] = 'matrix'
    dct['encoding']['headingCorner'] = '(1,1)'
    dct['encoding']['dataCorner'] = '(5,5)'
    dct['encoding']['nameDepth'] = 1
    dct['encoding']['path'] = "C:/Users/davie/Desktop/Masters/Dissertation/Code/DissertationCode/Eigg/Utilities/RelevantDatasets/production/BaseCSV/plantSeed.xls"
    return [dct] 

def texasGrasslands():
    dct = {}

    dct['source'] = 'Joern, Anthony. (1979). Feeding patterns in grasshoppers (Orthoptera: Acrididae): Factors influencing diet specialization. Oecologia. 38. 325-347. 10.1007/BF00345192. '    
    dct['interactionType'] = 'predation'
    dct['location'] = 'United States'
    
    dct['encoding'] = {}
    dct['encoding']['interactionFormat'] = 'matrix'
    dct['encoding']['headingCorner'] = '(1,1)'
    dct['encoding']['dataCorner'] = '(3,4)'
    dct['encoding']['nameDepth'] = 2
    dct['encoding']['path'] = "C:/Users/davie/Desktop/Masters/Dissertation/Code/DissertationCode/Eigg/Utilities/RelevantDatasets/production/BaseCSV/texasGrasslands.xls"
    return [dct] 

def texasGrasslands2():
    dct = {}
    
    dct['source'] = 'Joern, Anthony. (1979). Feeding patterns in grasshoppers (Orthoptera: Acrididae): Factors influencing diet specialization. Oecologia. 38. 325-347. 10.1007/BF00345192. '    
    dct['interactionType'] = 'predation'
    dct['location'] = 'United States'

    dct['encoding'] = {}
    dct['encoding']['interactionFormat'] = 'matrix'
    dct['encoding']['headingCorner'] = '(1,1)'
    dct['encoding']['dataCorner'] = '(3,4)'
    dct['encoding']['nameDepth'] = 2
    dct['encoding']['path'] = "C:/Users/davie/Desktop/Masters/Dissertation/Code/DissertationCode/Eigg/Utilities/RelevantDatasets/production/BaseCSV/texasGrasslands2.xls"
    dct['encoding']['metaData'] = []
    return [dct] 

def US_Grasslands():
    dct = {}

    dct['interactionType'] = 'predation'
    dct['location'] = 'United States'

    dct['encoding'] = {}
    dct['encoding']['interactionFormat'] = 'matrix'
    dct['encoding']['headingCorner'] = '(2,2)'
    dct['encoding']['dataCorner'] = '(5,5)'
    dct['encoding']['nameDepth'] = 2
    dct['encoding']['path'] = "C:/Users/davie/Desktop/Masters/Dissertation/Code/DissertationCode/Eigg/Utilities/RelevantDatasets/production/BaseCSV/US_Grasslands.xls"
    return [dct] 

def US_Grasslands():
    dct = {}

    dct['interactionType'] = 'predation'
    dct['location'] = 'United States'

    dct['encoding'] = {}
    dct['encoding']['interactionFormat'] = 'matrix'
    dct['encoding']['headingCorner'] = '(2,2)'
    dct['encoding']['dataCorner'] = '(5,5)'
    dct['encoding']['nameDepth'] = 2
    dct['encoding']['path'] = "C:/Users/davie/Desktop/Masters/Dissertation/Code/DissertationCode/Eigg/Utilities/RelevantDatasets/production/BaseCSV/US_Grasslands.xls"
    return [dct] 

def EcoWeb():
    filenames = os.listdir("C:/Users/davie/Desktop/Masters/Dissertation/Code/DissertationCode/Eigg/Utilities/RelevantDatasets/production/EcoWeb")
    dcts = []
    for f in filenames:
        dct = {}

        dct['source'] = f[:-4]+" from Cohen, J. E. (compiler) 2010. Ecologists' Co-Operative Web Bank. Version 1.1. Machine-readable database of food webs. New York: The Rockefeller University."
        dct['interactionType'] = 'predation'

        dct['encoding'] = {}
        dct['encoding']['interactionFormat'] = 'matrix'
        dct['encoding']['headingCorner'] = '(1,1)'
        dct['encoding']['dataCorner'] = '(2,2)'
        dct['encoding']['nameDepth'] = 1
        dct['encoding']['path'] = "C:/Users/davie/Desktop/Masters/Dissertation/Code/DissertationCode/Eigg/Utilities/RelevantDatasets/production/EcoWeb"+"/"+f

        dcts.append(dct)

    return dcts