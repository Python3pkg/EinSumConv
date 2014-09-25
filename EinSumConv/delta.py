import tensor
import lists
import sympy


dim = 4

class Delta(tensor.AppliedTensor):
    pass

def setDim(newDim):
    global dim
    dim = newDim


def contractOneDelta(factorList):
    newFactorList=list(factorList)
    for (i,D) in enumerate(factorList):
        if not isinstance(D,Delta):
            continue
        
        if not len(getattr(D,'index',[]))==2:
            raise TypeError('Error: delta must have precisly two indices')
        (d1,d2)=D.index
        
        if d1==d2:
            newFactorList[i]=dim
            return newFactorList
        
        for (j,factor) in enumerate(factorList):
            if i==j: continue

            if isinstance(factor,tensor.AppliedTensor):
                indexList=list(factor.index)
                if not deltaReplace(indexList,d1,d2):
                    continue
                newFactorList[j]=factor.withNewIndex(*indexList)
                return newFactorList
            
            if not hasattr(factor,'args'): continue

            indexDict, indexList = lists.serchIndexInFactor(factor)
            if not deltaReplace(indexList,d1,d2):
                continue
            newFactorList[j] = lists.withNewIndex(
                                    factor, indexDict, indexList)
            return newFactorList
    return None



def deltaReplace(theList,d1,d2):
    for (i,obj) in enumerate(theList):
        if obj==d1:
            theList[i]=d2
            return True
        if obj==d2:
            theList[i]=d1
            return True
    return False



def contractDeltas_factorList(factorList, *arg, **kw):
    while True:
        newFactorList=contractOneDelta(factorList, *arg, **kw)
        if newFactorList==None:
            return factorList
        factorList=newFactorList


def contractDeltas(exp, *arg, **kw):
    return sympy.Add(*[sympy.Mul(*contractDeltas_factorList(
                                      factorList, *arg, **kw)) 
                       for factorList 
                       in lists.makeTermList(exp)])
