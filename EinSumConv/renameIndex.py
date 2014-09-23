import tensor
import lists
import namingSymbols
import sympy



def newIndex_TensorFactorList(tfl, indexGenerator)
    IndexDict = {}
    dummyIndexDict = {}


def newIndex_FactorList(factorList, indexGenerator):
    indexDict={}
    newFactorList=list(factorList)
    for (i,factor) in enumerate(factorList):
        if not tensor.isTensor(factor):
            continue
        
        indexList=list(factor.index)
        for (k,index) in enumerate(indexList):
            if not isinstance(index, sympy.Dummy):
                continue
            if not index in indexDict:
                indexDict[index]=indexGenerator.next()
            indexList[k]=indexDict[index]
        newFactorList[i]=factor.withNewIndex(indexList)
    return newFactorList



def newIndex_TermList(termList):
    indexList=[]
    indexGenerator=namingSymbols.getNewDummys(List=indexList)
    return [newIndexFactorList(factorList,
                               namingSymbols.getNext(indexList,
                                                     indexGenerator))
            for factorList
            in termList]



def subsIndex(x,oldIndex,newIndex):
    if not tensor.isTensor(x):
        if not getattr(x, 'args', []):
            return x
        return type(x)(*[subsIndex(arg,oldIndex,newIndex) for arg in x.args])

    indexList=list(x.index)
    for (k,index) in enumerate(indexList):
        if index==oldIndex or getattr(x, 'args', None)==oldIndex:
            indexList[k]=newIndex
    if not getattr(x, 'args', []):
        return x.withNewIndex(*indexList)
    return type(x)(*[subsIndex(arg,oldIndex,newIndex) 
                     for arg in x.args]).withNewIndex(*indexList)


                


