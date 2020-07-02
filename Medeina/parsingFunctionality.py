def makeUnique(headTailDataWMeta):
    seen = set()
    newData = {}
    for head,tail,meta in headTailDataWMeta:
        if (head,tail) in seen: 
            for item in meta.keys():
                if item not in newData[(head,tail)].keys():
                    newData[(head,tail)][item] = meta[item]
            continue
        seen.add((head,tail))
        newData[(head,tail)] = meta
    
    return dictWithMetaToTuples(newData)

def dictWithMetaToTuples(metaDict):
    converted = []
    kz = metaDict.keys()
    for item in kz:
        head,tail = item
        converted.append((head,tail,metaDict[item]))
    
    return converted

def keepInteractionPartOnly(headTailDataWMeta):
    return list(map(lambda tup: (tup[0],tup[1]),headTailDataWMeta))

def verifyValidInteraction(speciesMappingToId,indivSpeciesInteraction):
    head,tail,meta = indivSpeciesInteraction
    return head in speciesMappingToId and tail in speciesMappingToId