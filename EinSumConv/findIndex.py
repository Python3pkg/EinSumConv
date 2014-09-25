import lists
import sympy

def findIndex_TensorFactorList(tfl):
    freeIndex = set()
    dummyIndex = set()
    tooMany = set()
    other = set()
    for tensor in tfl:
        for index in tensor[2]:
            if not isinstance(ind,(sympy.Dummy,sympy.Symbol)):
                other.add(ind)
            if ind in dummyIndex:
                tooMany.add(ind)
            elif ind in freeIndex:
                freeIndex.remove(ind)
                dummyIndex.add(ind)
            else:
                freeIndex.add(ind)
    return {'free':freeIndex, 
            'dummy':dummyIndex, 
            'tooMany':tooMany,
            'other':other}


def findIndex_TensorTermList(ttl):
    freeIndexList = []
    freeIndex = set()
    missingFree = set()
    dummyIndex = set()   
    tooMany = set()
    other = set()    
    for tfl in ttl:
        index = findIndex_TensorFactorList(tfl)
        freeIndexList.append(index[free])
        freeIndex |= index[free]
        dummyIndex |= index[dummy]
        tooMany |= index[tooMany]   
        other |= index[other]   
    for free in freeIndexList:
        missingFree |= (freeIndex - free)
    tooManny |= (freeIndex & dummyIndex)
    dummyIndex -= freeIndex 
    return {'free':freeIndex, 
            'dummy':dummyIndex, 
            'tooMany':tooMany,
            'missingFree':missingFree,
            'other':other}

def findIndex(exp):
    return serchIndex_TensorTermList(
        lists.makeTensorTermList(
            lists.makeTermList(exp)))
