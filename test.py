
from webStore import WebStore
import json
import requests

fileStr = '‪C:/Users/davie/Downloads/test.csv'
jsonString = json.dumps(json.loads("{\"path\": \"C:/Users/davie/Downloads/test.csv\", \"interactionType\": \"trophic\", \"encoding\":{\"interactionFormat\":\"pair\", \"head\":\"consumer\",\"tail\":\"resource\" }}"))
WebStore().add_interactions(jsonString)

# callToValidateName = requests.get('http://resolver.globalnames.org/name_resolvers.json?names=Turdus merula|Cyanocitta cristata')
# jsonRes = callToValidateName.json()
# print(jsonRes)