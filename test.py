
from webStore import WebStore
import json

fileStr = '‪C:/Users/davie/Downloads/test.csv'
jsonString = json.dumps(json.loads("{\"path\": \"C:/Users/davie/Downloads/test.csv\", \"interactionType\": \"trophic\", \"encoding\":{\"interactionFormat\":\"pair\", \"head\":\"consumer\",\"tail\":\"resource\" }}"))
WebStore().add_interactions(jsonString)