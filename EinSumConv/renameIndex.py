import tensor
import lists
import namingSymbols
import sympy
import findIndex
import delta
import eps




def renameDummyIndex_TensorFactorList(tfl, indexGenerator, oldDummys):
    newDummys = {}
    for (fPos,factor) in enumerate(tfl):
        for (iPos,ind) in enumerate(factor['indexList']):
            if not ind in oldDummys:
                continue
            if not ind in newDummys:
                newDummys[ind]=indexGenerator.next()
            tfl[fPos]['indexList'][iPos] = newDummys[ind]


def renameDummyIndex_TensorTermList(ttl):
    oldIndex = findIndex.findIndex_TensorTermList(tfl)
    oldDummys = oldIndex['dummy']
    freeNames = [ind.name for ind in oldIndex['free'] ]
    indexList=[]
    indexGenerator=namingSymbols.getNewDummys(List=indexList, forbiddenNames=freeNames)
    return [renameDummyIndex_TensorFactorList(
                tfl,
                namingSymbols.getNext(
                    indexList, indexGenerator, oldDummys, freeName) )
            for tfl in ttl]


def renameDummyIndex(exp):
    '''renames all Dummy indecis in the expression'''
    tl=lists.makeTermList(exp)
    ttl=lists.makeTensorTermList(tl)
    sortTensorTermList(ttl)
    renameDummyIndex_TensorTermList(ttl)
    return lists.rebuildAdd(ttl,tl)



def subsIndex(exp,oldIndex,newIndex):
    if not tensor.isTensor(exp):
        if not getattr(exp, 'args', []):
            return exp
        return type(exp)(*[subsIndex(arg,oldIndex,newIndex) 
                           for arg in exp.args])
    newIndexList = []
    for ind in exp.index:
        if ind==oldIndex or str(ind)==oldIndex:
            newIndexList.append(newIndex)
        else:
            newIndexList.append(ind)
    if not hasattr(exp,'args'):
        return exp.withNewIndex(*newIndexList)
    return type(type(exp))(*newIndexList)(
        *[subsIndex(arg,oldIndex,newIndex) for arg in exp.args])



def tensorSimplify(exp, **kw)
    '''
    tyres to simplify a tensor expresion by writing it on a normal form
    If you do not like the result you can try simplifying by had using
    e.g subsIndex, contractDeltas, renameDummyIndex, epsAsDeltas, allEpsAsDeltas
    '''
    termList = delta.contractDeltas_termList(
                    lists.makeTermList(
                        sympy.expand(
                            eps.allEpsAsDeltas(exp,**kw) ) ),
                    **kw)
    return rebuildAdd(
                renameDummyIndex_TensorTermList(
                    lists.makeTensorTermList( termList ) ),
                termList)


                


