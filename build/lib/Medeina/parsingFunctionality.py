
def makeUnique(headTailDataWMeta):
    newData = []
    seen = set()
    for head,tail,meta in headTailDataWMeta:
        if (head,tail) in seen: continue
        newData.append((head,tail,meta))
        seen.add((head,tail))
    
    return newData

def keepInteractionPartOnly(headTailDataWMeta):
    return list(map(lambda tup: (tup[0],tup[1]),headTailDataWMeta))

def verifyValidInteraction(speciesMappingToId,indivSpeciesInteraction):
    head,tail,meta = indivSpeciesInteraction
    return head in speciesMappingToId and tail in speciesMappingToId