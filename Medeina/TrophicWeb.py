from .Web import Web 
from .config import *

class TrophicWeb(Web):
    def __init__(self,path=BASEDIR,*args,**kwargs):
        super().__init__(path,args,kwargs)
        newWeb = self.filterByInteractionType(["trophic"])
        self.linkMetas = newWeb.linkMetas
        self.datasetMetas = newWeb.datasetMetas
        self.interactions = newWeb.interactions
        self.stringNames = newWeb.stringNames
        self.taxa = newWeb.taxa
        