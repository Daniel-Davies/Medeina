from dataCleaning import cleanSingleSpeciesString
import networkx as nx
from common import *
from collections import defaultdict
from interactionParser import *
import itertools

class MedeinaCumulativeApplication:
    def __init__(self,storePath):
        self.interactionStore = []
        self.stringNames = {}
        self.storePath = storePath
    
    def apply(self,WebObj,species,taxaLevel="exact"):
        if taxaLevel == "exact": taxaLevel = "species"
        species = list(set(filter(lambda x: x != '',map(cleanSingleSpeciesString,species))))
        speciesWithTaxonomy = self.indexSpeciesWithTaxaData(species,WebObj)
        return self.handleApplication(WebObj,speciesWithTaxonomy,taxaLevel)

    def indexSpeciesWithTaxaData(self,species,WebObj):
        speciesWithTaxonomy = {}
        self.findAndIndexNewSpecies(species,WebObj,speciesWithTaxonomy)
        self.indexRecordedSpecies(species,WebObj,speciesWithTaxonomy)
        return speciesWithTaxonomy
    
    def findAndIndexNewSpecies(self,species,WebObj,speciesWithTaxonomy):
        newlyEnteredSpeciesResults = self.getMissingTaxaFromAPI(species,WebObj)
        for name,valid,taxaDict in newlyEnteredSpeciesResults:
            if not valid: continue
            speciesWithTaxonomy[name] = taxaDict
    
    def indexRecordedSpecies(self,species,WebObj,speciesWithTaxonomy):
        existingTaxaDict = WebObj.taxa
        existingStringNames = WebObj.stringNames
        for s in species:
            if s not in speciesWithTaxonomy:
                idx = existingStringNames[s]
                speciesWithTaxonomy[s] = existingTaxaDict[idx]
        
    def getMissingTaxaFromAPI(self,species,WebObj):
        species = list(set(species) - set(WebObj.stringNames.keys()))
        responses = []
        for i in range(0,len(species),APIMAX):
            print("Indexing records " + str(i) + " to " + str(min(len(species),i+APIMAX)) + " [of "+str(len(species))+"]")
            responses.extend(callAPIOnDataList(species[i:i+APIMAX]))

        speciesResponses = list(map(processSingleResponse,responses))
        return list(filter(lambda x: x[1],speciesResponses))
    
    def handleApplication(self,WebObj,speciesWithTaxa,taxaLevel):
        genericInteractions = self.handleNonExceptionSpecies(WebObj,speciesWithTaxa,taxaLevel)
        taxaBasedInteractions = self.handleExceptionSpecies(WebObj,speciesWithTaxa)
        totalInteractions = [*genericInteractions,*taxaBasedInteractions]
        self.interactionStore = totalInteractions
    
    def handleExceptionSpecies(self,WebObj,speciesWithTaxa):
        predatorExceptionIDs = self.handlePredatorExceptions(WebObj, speciesWithTaxa) 
        preyExceptionIDs = self.handlePreyExceptions(WebObj, speciesWithTaxa)
        return [*predatorExceptionIDs,*preyExceptionIDs]
    
    def handlePredatorExceptions(self,WebObj,speciesWithTaxa):
        exceptions = WebObj.taxaExceptions
        interactionWeb = WebObj.interactions
        genericSpecies = list(speciesWithTaxa.keys())
        exceptedInteractions = []
        taxa = WebObj.taxa 
        stringNames = WebObj.stringNames
        for species in exceptions:
            consumerBehaviour = exceptions[species]['consumer']
            genericSpeciesAtUserTaxa = set(list(map(lambda x: speciesWithTaxa[x][consumerBehaviour],genericSpecies)))
            preyOfSpeciesAtTaxa = set(list(map(lambda x: taxa[x][consumerBehaviour],interactionWeb.get(stringNames[species],{}).keys()))) - set([''])
            for potentialPrey in genericSpecies:
                if speciesWithTaxa[potentialPrey][consumerBehaviour] in preyOfSpeciesAtTaxa:
                    exceptedInteractions.append((species,potentialPrey))

        return exceptedInteractions

    def handlePreyExceptions(self,WebObj,speciesWithTaxa):
        exceptions = WebObj.taxaExceptions
        taxa = WebObj.taxa
        stringNames = {v:k for k,v in WebObj.stringNames.items()}
        exceptedInteractions = []
        genericSpecies = set(speciesWithTaxa.keys())
        predatorBucket = self.findPredatorsPerExceptedPrey(WebObj,stringNames)
        for exceptedPrey in predatorBucket:
            targetTaxa = exceptions[exceptedPrey]['resource']
            targetTaxaValue = taxa[WebObj.stringNames[exceptedPrey]][targetTaxa]
            if targetTaxaValue == '': continue
            for predator in predatorBucket[exceptedPrey]:
                if predator in genericSpecies:
                    for potentialPrey in genericSpecies:
                        if speciesWithTaxa[potentialPrey][targetTaxa] == targetTaxaValue:
                            exceptedInteractions.append((predator,potentialPrey))

        return exceptedInteractions
    
    def findPredatorsPerExceptedPrey(self,WebObj,stringNames):
        exceptions = WebObj.taxaExceptions
        interactionWeb = WebObj.interactions
        predatorBucket = {} 
        for species in exceptions:
            predatorBucket[species] = []

        tmp = interactionWeb[IDTRACKER]
        del interactionWeb[IDTRACKER]
        for predator in interactionWeb:
            for prey in interactionWeb[predator]:
                if stringNames[prey] in predatorBucket: predatorBucket[stringNames[prey]].append(stringNames[predator])
        interactionWeb[IDTRACKER] = tmp
        return predatorBucket

    def handleNonExceptionSpecies(self,WebObj,speciesWithTaxa,taxaLevel):
        interactionsAtUserDefinedLevel = self.buildTaxaBasedInteractions(WebObj,taxaLevel)
        genericSpecies = self.nonExceptedSpecies(WebObj,speciesWithTaxa)
        genericSpeciesAtUserTaxa = set(list(map(lambda x: speciesWithTaxa[x][taxaLevel],genericSpecies)))
        genericInteractions = []
        for s in genericSpecies:
            nameAtUserTaxaLevel = speciesWithTaxa[s][taxaLevel]
            preyOfSpecies = set(interactionsAtUserDefinedLevel.get(nameAtUserTaxaLevel,{}).keys()) - set([''])            
            for potentialPrey in genericSpecies:
                if speciesWithTaxa[potentialPrey][taxaLevel] in preyOfSpecies:
                    genericInteractions.append((s,potentialPrey))

        return genericInteractions

    def nonExceptedSpecies(self,WebObj,speciesWithTaxa):
        exceptions = WebObj.taxaExceptions
        return list(filter(lambda x: x not in exceptions, speciesWithTaxa.keys()))

    def buildTaxaBasedInteractions(self,WebObj,taxaLevel):
        taxaBasedInteractions = {}
        stringResource = self.determineAppropriateStringMapper(WebObj,taxaLevel)
        interactions = WebObj.interactions
        tmp = interactions[IDTRACKER]
        del interactions[IDTRACKER]
        for predator in interactions:
            for prey in interactions[predator]:
                sourceList = interactions[predator][prey]
                if stringResource[predator] not in taxaBasedInteractions:
                    taxaBasedInteractions[stringResource[predator]] = defaultdict(list)
                taxaBasedInteractions[stringResource[predator]][stringResource[prey]].extend(sourceList)

        interactions[IDTRACKER] = tmp
        return taxaBasedInteractions
    
    def determineAppropriateStringMapper(self,WebObj,taxaLevel):
        stringResource = {}
        if taxaLevel != "species":
            stringResource = {k:v[taxaLevel] for k,v in WebObj.taxa.items()}
        else:
            stringResource = {v:k for k,v in WebObj.stringNames.items()}
        return stringResource
    
    def toList(self):
        return list(map(lambda x: (self.stringNames[x[0]],self.stringNames[x[1]]), self.interactionStore))
    
    def toGraph(self,directed=False):
        nodes = self.stringNames.values()
        G = nx.Graph()
        if directed: G = nx.DiGraph()
        for node in nodes:
            G.add_node(node)
        
        for consumer,resource in self.interactionStore:
            G.add_edge(self.stringNames[consumer],self.stringNames[resource])
        
        return G

    def toMatrix(self):
        G = self.toGraph()
        nodeOrder = list(self.stringNames.values())
        return nx.to_numpy_matrix(G,nodelist=nodeOrder), nodeOrder

    def audit(self):
        print("Complete")
        pass 