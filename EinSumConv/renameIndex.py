import tensor
import lists
import namingSymbols
import sympy


def newIndexFactorList(factorList, indexGenerator):
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



def newIndexTermList(termList):
    indexList=[]
    indexGenerator=namingSymbols.getNewDummys(List=indexList)
    return [newIndexFactorList(factorList,
                               namingSymbols.getNext(indexList,
                                                     indexGenerator))
            for factorList
            in termList]
    
    



                


