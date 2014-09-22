import tensor
import lists
import sympy

class Delta(tensor.AppliedTensor):
    pass

def contractKroneckerDelta(factorList,dim=4):
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
            if i==j or not tensor.isTensor(factor):
                continue
            indexList=list(factor.index)
            for (k,index) in enumerate(factor.index):
                if index==d1:
                    newFactorList[i]=1 #delta=1
                    indexList[k]=d2 #replace index a==d1 with d2
                    newFactorList[j]=factor.withNewIndex(tuple(indexList))
                    return newFactorList
                if index==d2:
                    newFactorList[i]=1 #delta=1
                    indexList[k]=d1 #replace index a==d2 with d1
                    newFactorList[j]=factor.withNewIndex(tuple(indexList))
                    return newFactorList
    return None


def contractAllKroneckerDeltas(factorList, *arg, **kw):
    while True:
        newFactorList=contractKroneckerDelta(factorList, *arg, **kw)
        if newFactorList==None:
            return factorList
        factorList=newFactorList

def contractDeltas(x, *arg, **kw):
    return sympy.Add(*[sympy.Mul(*contractAllKroneckerDeltas(
                                      factorList, *arg, **kw)) 
                       for factorList 
                       in lists.makeTermList(x)])
