import json 
from .interactionParser import saveNewData
from .config import *
from os import path
import pickle
from .common import writeObjToDateStore, retrieveObjFromStore
from .exportTools import denormaliseData
import csv

class WebStore:
    def __init__(self,storePath=BASEDIR):
        self.storePath = storePath
        requiredFiles = [DATASETS,WEB,TAXA,LINKS,EXCEPTIONS,REALNAMES]
        for file_ in requiredFiles: self.assureExistence(file_) 
        self.initialiseLinkIdTracker()

    def assureExistence(self,file_):
        if not path.exists(f'{self.storePath}/{file_}'):
            writeObjToDateStore(self.storePath,file_,{})

    def initialiseLinkIdTracker(self):
        changeDetected = False
        existingWeb = retrieveObjFromStore(self.storePath,WEB)
        if IDTRACKER not in existingWeb:
            existingWeb[IDTRACKER] = 0
            changeDetected = True 
        
        if changeDetected:
            writeObjToDateStore(self.storePath,WEB,existingWeb)

    def add_interactions(self,userIn,includeInvalid=False):
        jsonFormattedSpecificationString = self.parseUserInputToStandardJsonString(userIn) 
        parsedSpecificationString = json.loads(jsonFormattedSpecificationString)
        parsedSpecificationString['storageLocation'] = self.storePath
        parsedSpecificationString['includeInvalid'] = includeInvalid
        saveNewData(parsedSpecificationString)

    def parseUserInputToStandardJsonString(self,userIn):
        if isinstance(userIn, str): return userIn
        if isinstance(userIn,dict): return json.dumps(userIn)
        raise ValueError('Please supply either a String or Dict type!')
    
    def export_data(self,path,columns,datasets=[]):
        rowsByList, headings = denormaliseData(columns,datasets)
        with open(path+"/"+"out.csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerows([headings])
            writer.writerows(rowsByList)
    
    @staticmethod
    def preLoad():
        return 42





