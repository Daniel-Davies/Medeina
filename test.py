
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
dct['encoding']['headingCorner'] = '(1,1)'
dct['encoding']['dataCorner'] = '(2,2)'
# dct['encoding']['head'] = 'consumer'
# dct['encoding']['tail'] = 'resource'
# dct['encoding']['evidencedBy'] = 'link.evidence'
dct['encoding']['path'] = "C:/Users/davie/Desktop/Masters/Dissertation/Code/DissertationCode/Eigg/Utilities/RelevantDatasets/production/dryad/reef_spnames.xls"


# jsonString = json.dumps(json.loads("{\"path\": \"C:/Users/davie/Downloads/test.csv\", \"interactionType\": \"trophic\", \"encoding\":{\"interactionFormat\":\"pair\", \"head\":\"consumer\",\"tail\":\"resource\" }}"))
WebStore('C:/Users/davie/Desktop/MedeinaTest').add_interactions(dct)
# WebStore().export_data([],[])
# callToValidateName = requests.get('http://resolver.globalnames.org/name_resolvers.json?names=Turdus merula|Cyanocitta cristata')
# jsonRes = callToValidateName.json()
# print(jsonRes)