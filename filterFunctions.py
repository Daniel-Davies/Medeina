
def filterDatasetByDIds(datasetObject,dIds):
    dIds = set(dIds)
    return {k:v for k, v in datasetObject.items() if k in dIds}

def filterInteractionsByDIds(interactions,dIds):
    pass 

def filterLinksMetasByDIds(linkMetas,dIds):
    pass 

def countInteractionsInDict(dict_):
    return 42