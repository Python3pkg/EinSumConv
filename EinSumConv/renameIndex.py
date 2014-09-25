import tensor
import lists
import namingSymbols
import sympy
import findIndex




def renameDummyIndex_TensorFactorList(tfl, indexGenerator):
    newDummys = {}
    oldDummys = findIndex.findIndex_TensorFactorList(tfl)['dummy']
    for (i,tensor) in enumerate(tfl):
        for (k,ind) in enumerate(tensor['indexList']):
            if not ind in oldDummys:
                continue
            if not ind in newDummys:
                newDummys[ind]=indexGenerator.next()
            tfl[i]['indexList'][k] = newDummys[ind]


def renameDummyIndex_TensorTermList(ttl):
    indexList=[]
    indexGenerator=namingSymbols.getNewDummys(List=indexList)
    return [renameDummyIndex_TensorFactorList(
                tfl,
                namingSymbols.getNext(indexList,indexGenerator))
            for tfl in ttl]


def renameDummyIndex(exp):
    tl=lists.makeTermList(exp)
    ttl=lists.makeTensorTermList(tl)
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




def pdb_test():
    f=sympy.Function('f')
    t=tensor.Tensor('t')
    tf=tensor.TensorFunction('tf')
    x,y,z = sympy. symbols('x,y,z')
    exp = f(t(x), z, tf(x,y)(z, z, tf(z,z)(x,x) ) )
    return renameDummyIndex(exp)
                


