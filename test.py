
from webStore import WebStore
import json
import requests

dct = {}
dct['interactionType'] = 'trophic'
dct['encoding'] = {}

dct['encoding']['interactionFormat'] = 'pair'
dct['encoding']['head'] = 'consumer'
dct['encoding']['tail'] = 'resource'
dct['encoding']['evidencedBy'] = 'link.evidence'
dct['encoding']['path'] = "C:/Users/davie/Downloads/test.csv"


fileStr = '‪C:/Users/davie/Downloads/test.csv'
# jsonString = json.dumps(json.loads("{\"path\": \"C:/Users/davie/Downloads/test.csv\", \"interactionType\": \"trophic\", \"encoding\":{\"interactionFormat\":\"pair\", \"head\":\"consumer\",\"tail\":\"resource\" }}"))
WebStore().add_interactions(dct)

# callToValidateName = requests.get('http://resolver.globalnames.org/name_resolvers.json?names=Turdus merula|Cyanocitta cristata')
# jsonRes = callToValidateName.json()
# print(jsonRes)