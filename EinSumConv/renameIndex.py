import tensor
import lists
import namingSymbols
import sympy
import findIndex



def renameDummyIndex_TensorFactorList(tfl, indexGenerator):
    newDummys = {}
    oldDummys = findIndex.findIndex_TensorFactorList(tfl)[dummy]
    for (i,tensor) in enumerate(tensor):
        for (k,ind) in enumerate(tensor[2]):
            if not ind in oldDummys:
                continue
            if not ind in newDummys:
                newDummys[ind]=indexGenerator.next()
            tfl[i][2][k] = newDummys[ind]


def newIndex_TensorTermList(termList):
    indexList=[]
    indexGenerator=namingSymbols.getNewDummys(List=indexList)
    return [newIndex_TensorFactorList(
                factorList,
                namingSymbols.getNext(indexList,indexGenerator))
            for factorList
            in termList]



def subsIndex(exp,oldIndex,newIndex):
    if not isTensor(exp):
        if not getattr(x, 'args', []):
            return x
        return type(exp)(*[subsIndex(arg,oldIndex,newIndex) for arg in x.args])
    newIndexList = []
    for ind in exp.index:
        if ind=oldIndex or str(ind=oldIndex):
            newIndexList.append(newIndex)
        else:
            newIndexList.append(ind)
    if not hasattr(exp,'args'):
        return exp.withNewIndex(*newIndexList)
    return type(type(exp))(*newIndexList)(
        *[subsIndex(arg,oldIndex,newIndex) for arg in x.args])





                


