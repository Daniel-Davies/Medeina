
from webStore import WebStore
import json
import requests

dct = {}
dct['interactionType'] = 'trophic'

# dct['encoding'] = {}
# dct['encoding']['interactionFormat'] = 'pair'
# dct['encoding']['head'] = 'consumer'
# dct['encoding']['tail'] = 'resource'
# dct['encoding']['evidencedBy'] = 'link.evidence'
# dct['encoding']['path'] = "C:/Users/davie/Downloads/test.csv"

dct['encoding'] = {}
dct['encoding']['interactionFormat'] = 'matrix'
dct['encoding']['headingCorner'] = '(3,2)'
dct['encoding']['dataCorner'] = '(5,4)'
dct['encoding']['nameDepth'] = 2
dct['encoding']['metaData'] = [{'orientation': 'col', 'name': 'order', 'index':2 }]
# dct['encoding']['head'] = 'consumer'
# dct['encoding']['tail'] = 'resource'
# dct['encoding']['evidencedBy'] = 'link.evidence'
dct['encoding']['path'] = "C:/Users/davie/Desktop/Masters/Dissertation/Code/DissertationCode/Eigg/Utilities/RelevantDatasets/production/janePollinators.csv"


# jsonString = json.dumps(json.loads("{\"path\": \"C:/Users/davie/Downloads/test.csv\", \"interactionType\": \"trophic\", \"encoding\":{\"interactionFormat\":\"pair\", \"head\":\"consumer\",\"tail\":\"resource\" }}"))
WebStore().add_interactions(dct)
# WebStore().export_data([],[])
# callToValidateName = requests.get('http://resolver.globalnames.org/name_resolvers.json?names=Turdus merula|Cyanocitta cristata')
# jsonRes = callToValidateName.json()
# print(jsonRes)