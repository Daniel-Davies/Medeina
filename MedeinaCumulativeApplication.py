from dataCleaning import cleanSingleSpeciesString
import networkx as nx
from common import *
from collections import defaultdict
from interactionParser import *
import itertools

class MedeinaCumulativeApplication:
    def __init__(self,storePath):
        self.interactionStore = []
        self.linkEvidence = defaultdict(list)
        self.storePath = storePath
        self.speciesLen = 0
        self.lenExcepted = 0
        self.lenGeneric = 0
        self.taxaLevel = None
    
    def apply(self,WebObj,species,taxaLevel="exact"):
        if taxaLevel == "exact": taxaLevel = "species"
        self.taxaLevel = taxaLevel
        species = list(set(filter(lambda x: x != '',map(cleanSingleSpeciesString,species))))
        speciesWithTaxonomy = self.indexSpeciesWithTaxaData(species,WebObj)
        self.speciesLen = len(speciesWithTaxonomy)
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
        self.lenExcepted = len(taxaBasedInteractions)
        self.lenGeneric = len(genericInteractions)
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
                    self.addLinkEvidenceForPredExceptionInteraction(species,potentialPrey,interactionWeb,speciesWithTaxa[potentialPrey][consumerBehaviour],WebObj,consumerBehaviour)
                    exceptedInteractions.append((species,potentialPrey))

        return exceptedInteractions
    
    def addLinkEvidenceForPredExceptionInteraction(self,species,potentialPrey,interactionWeb,targetTaxaValue,WebObj,taxaGroup):
        prey = interactionWeb[WebObj.stringNames[species]]
        taxa = WebObj.taxa 
        for p in prey:
            compTaxaVal = taxa[p][taxaGroup]
            if compTaxaVal == targetTaxaValue:
                evidencingIDs = interactionWeb[WebObj.stringNames[species]][p]
                self.linkEvidence[(species,potentialPrey)].extend(evidencingIDs)

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
                            evidencingIDs = WebObj.interactions[WebObj.stringNames[predator]][WebObj.stringNames[exceptedPrey]]
                            self.linkEvidence[(predator,potentialPrey)].extend(evidencingIDs)
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
                    evidencingIDs = interactionsAtUserDefinedLevel[nameAtUserTaxaLevel][speciesWithTaxa[potentialPrey][taxaLevel]]
                    self.linkEvidence[(s,potentialPrey)].extend(evidencingIDs)

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
        return list(map(lambda x: (x[0],x[1]), self.interactionStore))
    
    def toGraph(self,directed=False):
        nodes = self.interactionsToNodes()
        G = nx.Graph()
        if directed: G = nx.DiGraph()
        for node in nodes:
            G.add_node(node)
        
        for consumer,resource in self.interactionStore:
            G.add_edge(consumer,resource)
        
        return G

    def toMatrix(self):
        G = self.toGraph()
        nodeOrder = self.interactionsToNodes()
        return nx.to_numpy_matrix(G,nodelist=nodeOrder), nodeOrder
    
    def interactionsToNodes(self):
        return list(set(itertools.chain(*self.interactionStore)))

    def audit(self):
        print("Complete")
        
        pass 
    
    def summary(self):
        print("Application complete")
        print("--------------------")
        print("User provided " + str(self.speciesLen) + " unique, valid species")
        print("Found " + str(len(self.linkEvidence)) + " unique interactions")
        print("Captured " + str(self.lenGeneric) + " interactions using the \"" + self.taxaLevel + "\" level")
        print("Captured " + str(self.lenExcepted) + " interactions from taxonomic exceptions")
        print("Involvement of " + str(len(set(itertools.chain(*self.linkEvidence.keys())))) + " user provided species captured")
        print("Percentage of user provided species involved in this application: " + str(len(set(itertools.chain(*self.linkEvidence.keys())))*100 / self.speciesLen ) + "%") 
