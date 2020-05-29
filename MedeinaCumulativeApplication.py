from dataCleaning import cleanSingleSpeciesString
import networkx as nx


class MedeinaCumulativeApplication:
    def __init__(self):
        self.interactionStore = []
        self.stringNames = {}
    
    # Taxa & Taxa exceptions
    def apply(self,WebObj,species):
        graphStore = []
        species = list(map(cleanSingleSpeciesString,species))
        species = set(species)
        presentSpeciesInWeb = list(set(WebObj.stringNames.keys()).intersection(species))
        speciesIds = set(list(map(lambda x: WebObj.stringNames[x], presentSpeciesInWeb)))
        idsToStrings = {v:k for k,v in WebObj.stringNames.items()}
        reducedIdsToStrings = {}
        for sId in speciesIds:
            if sId in WebObj.interactions:
                evidencedPreyIds = set((WebObj.interactions[sId]).keys())
                interactions = list(evidencedPreyIds.intersection(speciesIds))
                graphStore.extend(list(map(lambda x: (sId,x), interactions)))

        for id1,id2 in graphStore:
            reducedIdsToStrings[id1] = idsToStrings[id1]
            reducedIdsToStrings[id2] = idsToStrings[id2]

        self.interactionStore = graphStore
        self.stringNames = reducedIdsToStrings
    
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