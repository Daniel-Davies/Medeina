import json 
from interactionParser import saveNewData
from config import *
from os import path
import pickle
from common import writeObjToDateStore, retrieveObjFromStore

class WebStore:
    def __init__(self):
        requiredFiles = [DATASETS,WEB,TAXA,LINKS,EXCEPTIONS,REALNAMES]
        for file_ in requiredFiles: self.assureExistence(file_) 
        self.initialiseLinkIdTracker()

    def assureExistence(self,file_):
        if not path.exists(f'{BASEDIR}/{file_}'):
            with open(f'{BASEDIR}/{file_}','wb') as fh:
                pickle.dump({},fh)
    
    def initialiseLinkIdTracker(self):
        changeDetected = False
        with open(f'{BASEDIR}/{WEB}','rb') as fh:
            existingWeb = pickle.load(fh)
            if IDTRACKER not in existingWeb:
                existingWeb[IDTRACKER] = 0
                changeDetected = True 
        
        if changeDetected:
            with open(f'{BASEDIR}/{WEB}','wb') as fh:
                pickle.dump(existingWeb,fh)

    def add_interactions(self,userIn):
        jsonFormattedSpecificationString = self.parseUserInputToStandardJsonString(userIn) 
        parsedSpecificationString = json.loads(jsonFormattedSpecificationString)
        saveNewData(parsedSpecificationString)

    def parseUserInputToStandardJsonString(self,userIn):
        if isinstance(userIn, str):
            return userIn
        elif isinstance(userIn,dict):
            return json.dumps(userIn)
        
        raise ValueError('Please supply either a String or Dict type!')
    
    def export_data(columns,datasets=[]):
        if len(datasets) == 0: datasets = retrieveObjFromStore(DATASETS).keys()
        datasets = set(datasets)
        out = []

        interactions = retrieveObjFromStore(WEB)
        del interactions[IDTRACKER]

        for head in interactions:
            for tail in interactions[head]:
                for linkId in interactions[head][tail]:
                    if linkId in out:
                        out.append(([head,tail],linkId))
        
        existingLinks = retrieveObjFromStore(LINKS)
        out = map(lambda x: handleLinkMetaData(x,existingLinks),out)

        exisingData = retrieveObjFromStore(DATASETS)
        out = list(map(lambda x: handleDatasetMetaData(x, exisingData),out))

    def handleLinkMetaData(tup, existingLinks):
        aggregated, linkId = tup 

        meta = existingLinks[linkId]
        return tup 

    def handleDatasetMetaData(tup, exisingData):
        return tup


        




