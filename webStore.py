import json 
from interactionParser import saveNewData
from config import *
from os import path
import pickle

class WebStore:
    def __init__(self):
        requiredFiles = [DATASETS,WEB,TAXA,CONFIDENCE,LINKS,EXCEPTIONS,REALNAMES]
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

    def add_interactions(self,jsonFormattedSpecificationString):
        parsedSpecificationString = json.loads(jsonFormattedSpecificationString)
        saveNewData(parsedSpecificationString)
