from common import *
from config import *
from dataCleaning import cleanSingleSpeciesString

class Web:
    def __init__(self,path=BASEDIR):
        self.storePath = path
        self.interactions = retrieveObjFromStore(self.storePath,WEB)
        self.taxaExceptions = retrieveObjFromStore(self.storePath,EXCEPTIONS)
        self.taxa = retrieveObjFromStore(self.storePath,TAXA)
        self.linkMetas = retrieveObjFromStore(self.storePath,LINKS)
        self.datasetMetas = retrieveObjFromStore(self.storePath,DATASETS)
        self.stringNames = retrieveObjFromStore(self.storePath,REALNAMES)

    def sayHelloMedeina(self):
        print("Hello")
    
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

    def filterByDatasetId():
        pass
    
    def filterByTaxa():
        pass 
    
    def filterByObservationType():
        pass

    def apply():
        pass 

    def audit():
        pass 

