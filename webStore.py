import json 
from interactionParser import saveNewData
from config import *
from os import path
import pickle

class WebStore:
    def __init__(self):
        requiredFiles = [DATASETS,WEB,TAXA,CONFIDENCE,LINKS,EXCEPTIONS,REALNAMES]
        for file_ in requiredFiles: self.assureExistence(file_) 

    def assureExistence(self,file_):
        if not path.exists(f'{BASEDIR}/{file_}'):
            with open(f'{BASEDIR}/{file_}','wb') as fh:
                pickle.dump({},fh)

    def add_interactions(self,jsonFormattedSpecificationString):
        parsedSpecificationString = json.loads(jsonFormattedSpecificationString)
        saveNewData(parsedSpecificationString)
