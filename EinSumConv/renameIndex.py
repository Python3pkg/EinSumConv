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
                namingSymbols.getNext(indexList, indexGenerator) 
                oldDummys)
            for tfl in ttl]


def renameDummyIndex(exp):
    'renames all Dummy indecis in the expression, in a clever way'
    tl=lists.makeTermList(exp)
    ttl=lists.makeTensorTermList(tl)
    sortTensorTermList(ttl)
    renameDummyIndex_TensorTermList(ttl)
    return lists.rebuildAdd(ttl,tl)



def subsIndex(exp,oldIndex,newIndex):
    '''
    Substitute oldIndex for newIndex in exp.
    If oldIndex is given as a string, all indecis with that name will be replaced.
    If oldIndex is not a sring, every index equal to oldIndex will be replaced.
    '''
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
                            eps.epsAsDeltas(exp,**kw) ) ),
                    **kw)
    return rebuildAdd(
                renameDummyIndex_TensorTermList(
                    lists.makeTensorTermList( termList ) ),
                termList)


                

##################### Here be unittest #####################
import unittest

class TestFindIndex(unittest.TestCase):

    def setUp(self):
        pass

    def test_subsIndex(self):
        f=sympy.Function('f')
        t=tensor.Tensor('t')
        tf=tensor.TensorFunction('tf')
        a=sympy.Dummy(a)
        b,c,d=sympy.symbols('b,c,d')
        exp=tf(a,b,c)( t(a,b), b, f(a) )
        self.assertEqual(subsIndex(exp,'a',d),
                         tf(d,b,c)( t(d,b), b, f(a) ) )
        self.assertEqual(subsIndex(exp,b,d),
                         tf(a,d,c)( t(a,d), b, f(a) ) )
        self.assertEqual(subsIndex(exp,c,d),
                         tf(a,b,d)( t(a,b), b, f(a) ) )
        self.assertEqual(subsIndex(exp,'b',d),subsIndex(exp,b,d))

    def test_renameDummyIndex(self):
        A=tensor.Tensor('A')
        B=tensor.Tensor('B')
        a=sympy.Dummy(a)
        b,c,d=sympy.symbols('b,c,d')
        exp = A(a,b,c)*B(b,c) - A(a,c,d)*B(c,d)
        self.assertEqual(renameDummyIndex(exp),0)

    def test_tensorSimplify(self):
        A=tensor.Tensor('A')
        B=tensor.Tensor('B')
        C=tensor.Tensor('C')
        a=sympy.Dummy(a)
        b,c,d=sympy.symbols('b,c,d')
        tempDim=getDim()
        setDim(3)
        self.assertEqual(tensorSimplify(eps.Eps(a,a,c) ),0)
        self.assertEqual(tensorSimplify(eps.Eps(a,b,c)*eps.Eps(c,b,a) ),-6)
        self.assertEqual(tensorSimplify(Eps(a,b,c)*A(a)*B(b)*C(c) ),
                          ( A(1)*B(2)*C(3) - A(1)*B(3)*C(2)
                           +A(2)*B(3)*C(1) - A(2)*B(1)*C(3)
                           +A(3)*B(1)*C(2) - A(3)*B(2)*C(1) )
        exp = A(a,b,c)*B(b,c) - A(a,c,d)*B(c,d)
        self.assertEqual(tensorSimplify(exp),0)
        setDim(tempDim)

if __name__ == '__main__':
    unittest.main()
