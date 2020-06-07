from config import * 
import pathlib
import pickle

def retrievePreComputedTranslationMapping():
    with open(PRECOMPUTER_STORE_PATH, 'rb') as fh:
        preComputedTranslationMapping = pickle.load(fh)
        preComputedTranslationMapping = subTranslatedNamesForKeys(preComputedTranslationMapping)

    return preComputedTranslationMapping    

def subTranslatedNamesForKeys(preComputedTranslationMapping):
    newIndex = {}
    for name in preComputedTranslationMapping:
        cleanedName, translations = preComputedTranslationMapping[name]
        newIndex[cleanedName] = [name,translations]
    return newIndex

def preComputedStoreExists():
    return pathlib.Path(PRECOMPUTER_STORE_PATH).is_file()

def translateStringToMapping(preComputedTranslationMapping,string):
    if string not in preComputedTranslationMapping:
        return [string]
    
    translatedName, value = preComputedTranslationMapping[string]
    if translatedName == '': return [string] 
    if len(value) == 0: return [string] 
    return value