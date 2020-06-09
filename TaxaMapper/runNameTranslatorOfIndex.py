from EcoNameTranslator import EcoNameTranslator
import pickle

# with open("mappingIndex",'rb') as f:
#     index = pickle.load(f)

# translator = EcoNameTranslator()
# newIndex = translator.translate(list(index.keys()))

# with open("newMappingIndex",'wb') as f:
#     pickle.dump(newIndex,f)

with open("newMappingIndex",'rb') as f:
    index = pickle.load(f)

counter = 0
for name in index:
    if len(index[name][1]) == 0 or index[name] == ('',''):
        print(name,index[name])
        counter += 1

print(counter)
