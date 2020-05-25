
import pickle
from common import writeObjToDateStore, retrieveObjFromStore
import json
from config import *

def denormaliseData(columns=[],datasets=[]):
    datasets = datasetsToNormalise(datasets)
    exisingData = retrieveObjFromStore(DATASETS)
    existingLinks = retrieveObjFromStore(LINKS)
    out = findLinksInRequestedDatasets(datasets,existingLinks)
    out = map(lambda x: handleLinkMetaData(x,existingLinks),out)
    out = list(map(lambda x: handleDatasetMetaData(x, exisingData),out))
    headers = getHeaders()
    return out, headers

def findLinksInRequestedDatasets(datasets,existingLinks):
    out = []
    interactions = retrieveObjFromStore(WEB)
    del interactions[IDTRACKER]
    for head in interactions:
        for tail in interactions[head]:
            for linkId in interactions[head][tail]:
                if existingLinks[linkId]['dId'] in datasets:
                    out.append(([head,tail],linkId))
    return out

def datasetsToNormalise(datasets):
    if len(datasets) == 0: datasets = retrieveObjFromStore(DATASETS).keys()
    datasets = set(datasets)
    return datasets

def getHeaders():
    headers = []
    headers.append("consumer")
    headers.append("resource")
    headers.extend(LINK_METAS)
    headers.extend(DATASET_METAS)
    return headers

def handleLinkMetaData(tup, existingLinks):
    aggregated, linkId = tup 
    meta = existingLinks[linkId]
    for item in LINK_METAS:
        aggregated.append(meta.get(item,''))
    return (aggregated, meta['dId'])

def handleDatasetMetaData(tup, exisingData):
    aggregated, linkId = tup 
    meta = exisingData[linkId]
    for item in DATASET_METAS:
        aggregated.append(meta.get(item,''))
    return aggregated