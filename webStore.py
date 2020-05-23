import json 
from interactionParser import saveNewData
from config import *

class WebStore:
    def __init__():
        requiredFiles = [DATASETS,WEB,TAXA,CONFIDENCE,LINKS,EXCEPTIONS,REALNAMES]
        for file_ in requiredFiles: assureExistence(file_) 

    def assureExistence(file_):
        if not path.exists(f'{BASEDIR}/{file_}'):
            with open(f'{BASEDIR}/{file_}','wb') as fh:
                pickle.dump({},fh)

    @staticmethod
    def add_interactions(jsonFormattedSpecificationString):
        parsedSpecificationString = json.loads(jsonFormattedSpecificationString)
        saveNewData(parsedSpecificationString)
