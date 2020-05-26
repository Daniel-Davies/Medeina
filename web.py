from common import *
from config import *
from dataCleaning import cleanSingleSpeciesString
from filterFunctions import *

class Web:
    def __init__(self,path=BASEDIR,*args,**kwargs):
        self.storePath = path
        if len(kwargs) == 0:
            self.interactions = retrieveObjFromStore(self.storePath,WEB)
            self.taxaExceptions = retrieveObjFromStore(self.storePath,EXCEPTIONS)
            self.taxa = retrieveObjFromStore(self.storePath,TAXA)
            self.linkMetas = retrieveObjFromStore(self.storePath,LINKS)
            self.datasetMetas = retrieveObjFromStore(self.storePath,DATASETS)
            self.stringNames = retrieveObjFromStore(self.storePath,REALNAMES)
            self.logbook = []
        else:
            self.interactions = kwargs['interactions']
            self.taxaExceptions = kwargs['taxaExceptions']
            self.taxa = kwargs['taxa']
            self.linkMetas = kwargs['linkMetas']
            self.datasetMetas = kwargs['datasetMetas']
            self.stringNames = kwargs['stringNames']
            self.logbook = kwargs['logbook']
    
    def viewSessionTaxonomicExceptions(self):
        prettyPrintDict(self.taxaExceptions)
    
    def addTaxonomicExcpetion(self,species,consumer,resource,save=False):
        species, consumer, resource = self.ensureValidUserInput(species,consumer,resource)
        self.taxaExceptions[species] = {'consumer':consumer, 'resource':resource}
        if save:
            txe = retrieveObjFromStore(self.storePath,EXCEPTIONS)
            txe[species] = {'consumer':consumer, 'resource':resource}
            writeObjToDateStore(self.storePath,EXCEPTIONS,txe)
    
    def ensureValidUserInput(self,species,consumer,resource):
        species = cleanSingleSpeciesString(species)
        consumer = consumer.lower()
        resource = resource.lower()
        if species not in self.stringNames: raise ValueError("No such species in the data store!")
        if consumer not in TAXA_OF_INTEREST: raise ValueError("Consumer taxa not supported")
        if resource not in TAXA_OF_INTEREST: raise ValueError("Resource taxa not supported")

        return species, consumer, resource

    def filterByDatasetId(self,dIds):
        self.validateDIds(dIds)
        self.logbook.append({'datasetIdFilter':dIds})
        newWeb = self.replicateFoodWeb()
        newWeb.datasetMetas = filterDatasetByDIds(self.datasetMetas,dIds)
        newWeb.interactions = filterInteractionsByDIds(self.interactions,dIds)
        newWeb.linkMetas = filterLinksMetasByDIds(self.linkMetas,dIds)
        return newWeb
        # filter all stuff (just interactions & datasets should do)

    def validateDIds(self,dIds):
        return dIds

    def filterByTaxa(self):
        pass 
    
    def filterByObservationType(self):
        pass
    
    def replicateFoodWeb(self):
        names = ['interactions','taxaExceptions','taxa','linkMetas','datasetMetas','stringNames','logbook']
        newData = list(map(serialise,[self.interactions,self.taxaExceptions,self.taxa,self.linkMetas,self.datasetMetas,self.stringNames,self.logbook]))
        kwargsDict = dict(zip(names,newData))
        return Web(**kwargsDict)

    def apply(self):
        # Will probably need a new object?
        pass 

    def audit(self):
        pass 
    
    def reIndex(self):
        # essentially load everything again, and apply functions from the logbook
        pass

    def summarise(self):
        print("Current Interaction Web has:")
        print(str(countInteractionsInDict(self.interactions))+" interactions") 
        

    def sayHelloMedeina(self):
        print("Hello")