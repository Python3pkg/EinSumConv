import lists



def findIndex_TensorFactorList(tfl):
    freeIndex = set()
    dummyIndex = set()
    tooMany = set()
    for tensor in tfl:
        for index in tensor[2]:
            if ind in dummyIndex:
                tooMany.add(ind)
            elif ind in freeIndex:
                freeIndex.remove(ind)
                dummyIndex.add(ind)
            else:
                freeIndex.add(ind)
    return {'free':freeIndex, 
            'dummy':dummyIndex, 
            'tooMany':tooMany}


def findIndex_TensorTermList(ttl):
    freeIndexList = []
    freeIndex = set()
    missingFree = set()
    dummyIndex = set()   
    tooMany = set()    
    for tfl in ttl:
        index = serchIndex_TensorFactorList(tfl)
        freeIndexList.append(index[free])
        freeIndex |= index[free]
        dummyIndex |= index[dummy]
        tooMany |= index[tooMany]     
    for free in freeIndexList:
        missingFree |= (freeIndex - free)
    return {'free':freeIndex, 
            'dummy':dummyIndex, 
            'tooMany':tooMany
            'missingFree':missingFree}

def findIndex(exp):
    return serchIndex_TensorTermList(lists.makeTensorTermList(exp))
