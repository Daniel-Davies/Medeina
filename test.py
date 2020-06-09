
from webStore import WebStore
import json
import requests
from Web import Web
import networkx as nx
import matplotlib.pyplot as plt
from specStrings import EcoWeb

dct = EcoWeb()[0]
WebStore().add_interactions(dct)
dct = EcoWeb()[20]
WebStore().add_interactions(dct)
dct = EcoWeb()[100]
WebStore().add_interactions(dct)
# f = Web()
# x = f.apply(['ancylus fluviatilis','navicula gregaria','blackbird'])
# y = x.to_list()

# dct = {}
# dct['interactionType'] = "predation"

# dct['encoding'] = {}
# dct['encoding']['interactionFormat'] = 'pair'
# dct['encoding']['head'] = 'consumer'
# dct['encoding']['tail'] = 'resource'
# dct['encoding']['path'] = "C:/Users/davie/Desktop/Masters/Dissertation/Code/DissertationCode/Eigg/Utilities/RelevantDatasets/production/freshwater.csv"

# dct['encoding']['evidencedBy'] = 'link.evidence'
# dct['encoding']['source'] = 'full.source'

# dct = {}
# dct['interactionType'] = 'pollination'
# dct['location'] = "Other Lake,Ukraine"
# dct['evidencedBy'] = "observation"

# dct['encoding'] = {}
# dct['encoding']['interactionFormat'] = 'pair'
# dct['encoding']['head'] = 'consumer'
# dct['encoding']['tail'] = 'resource'
# dct['encoding']['path'] = "C:/Users/davie/Desktop/Masters/Dissertation/Code/DissertationCode/Eigg/Utilities/RelevantDatasets/production/freshwater.csv"

# dct['encoding'] = {}
# dct['encoding']['interactionFormat'] = 'matrix'
# dct['encoding']['headingCorner'] = '(3,2)'
# dct['encoding']['dataCorner'] = '(5,4)'
# dct['encoding']['nameDepth'] = 2
# dct['encoding']['metaData'] = [{'orientation': 'col', 'name': 'order', 'index':2 },{'orientation': 'row', 'name': 'ind', 'index':1 }]
# dct['encoding']['head'] = 'consumer'
# dct['encoding']['tail'] = 'resource'
# dct['encoding']['evidencedBy'] = 'link.evidence'
# dct['encoding']['path'] = "C:/Users/davie/Desktop/Masters/Dissertation/Code/DissertationCode/Eigg/Utilities/RelevantDatasets/production/janePollinators.csv"


# jsonString = json.dumps(json.loads("{\"path\": \"C:/Users/davie/Downloads/test.csv\", \"interactionType\": \"trophic\", \"encoding\":{\"interactionFormat\":\"pair\", \"head\":\"consumer\",\"tail\":\"resource\" }}"))
# WebStore().add_interactions(dct)
# WebStore().export_data([],[])
