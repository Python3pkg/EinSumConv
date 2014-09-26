import tensor
import lists
import sympy


'''
<!> Always use sympy.expand(exp) before using makeTermList(exp) <!>
If you ignore this recomendation, stuf might not work as expcted.

Delta is the Kronicer delta.

ContractDeltas contracts all idndices of all Deltas, that are sympy.Symbol or sympy.Dummy

>>> T=tensor.Tensor('T')
>>> a,b,c,d = sympy.symbols('a,b,c,d')
>>> contractDeltas(Delta(a,c)*Detla(b,d)*T(c,d))
T(a, b)

dim is the number of dimensions of the indecis.
>>> constracDeltas(Delta(a,a)) == dim
True

setDim canges dim. Dim is originaly set to 4
>>> dim
4
>>> setDim(4711)
>>> dim
4711

dim can be overrided in spesific calculations
>>> setDim(4)
>>> constracDeltas(Delta(a,a), dim=13)
13

'''




dim = 3

class Delta(tensor.AppliedTensor):
    pass

def setDim(newDim):
    global dim
    dim = newDim

def getDim():
    return dim


def contractOneDelta(factorList, **tempDim):
    if 'dim' in tempDim:
        dim = tempDim['dim']
    else: dim = getDim()
    
    newFactorList=list(factorList)
    for (i,D) in enumerate(factorList):
        if not isinstance(D,Delta):
            continue
        
        if not len(getattr(D,'index',[]))==2:
            raise TypeError('Error: delta must have precisly two indices')
        d1,d2 = D.index
        if not (tensor.isAllowedDummyIndex(d1)
                or tensor.isAllowedDummyIndex(d2)):
            if (isinstance(d1,(sympy.Integer,int)) 
                    and isinstance(d2,(sympy.Integer,int)) ):
                if d1==d2: newFactorList[i]=1
                else: newFactorList[i]=0    
                return newFactorList
            continue
        
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
                newFactorList[i]=1
                return newFactorList

            if not hasattr(factor,'args'): continue

            indexDict, indexList = lists.serchIndexInFactor(factor)
            if not deltaReplace(indexList,d1,d2):
                continue
            newFactorList[j] = lists.withNewIndex(
                                    factor, indexDict, indexList)
            newFactorList[i] = 1
            return newFactorList
    return None



def deltaReplace(theList,d1,d2):
    for (i,obj) in enumerate(theList):
        if tensor.isAllowedDummyIndex(d1) and obj==d1:
            theList[i]=d2
            return True
        if tensor.isAllowedDummyIndex(d2) and obj==d2:
            theList[i]=d1
            return True
    return False



def contractDeltas_factorList(factorList, *arg, **kw):
    while True:
        newFactorList=contractOneDelta(factorList, *arg, **kw)
        if newFactorList==None:
            return factorList
        factorList=newFactorList

def contractDeltas_termList(termList, *arg, **kw):
    return [contractDeltas_factorList(factorList, *arg, **kw)
            for factorList in termList]


def contractDeltas(exp, *arg, **kw):
    termList = lists.makeTermList(exp)
    newTermList = contractDeltas_termList(termList, *arg, **kw)
    return sympy.Add(*[ sympy.Mul(*factorList) for factorList in newTermList ] )


### Here be unittest ###
import unittest

class TestDelta(unittest.TestCase):

    def setUp(self):
        self.t = tensor.Tensor('t')
        self.tf = tensor.TensorFunction('tf')
        self.a = sympy.Dummy('a')
        self.b = sympy.Dummy('b')
        self.c = sympy.Dummy('c')
        self.d = sympy.Dummy('d')
        self.x, self.y, self.z = sympy.symbols('x,y,z')
        self.f = sympy.Function('f')

    def test_Contractdeltas(self):
        t=self.t; tf=self.tf; a=self.a; b=self.b; c=self.c; d=self.d
        x=self.x; y=self.y; z=self.z; f=self.f

        exp = Delta(a,b)*Delta(x,y)*t(b,y)
        self.assertEqual(contractDeltas(exp),t(a,x))

        exp = 13*Delta(a,b)*Delta(b,a)
        self.assertEqual(contractDeltas(exp),13*dim)

        exp = Delta(1,2)*Delta(3,a)*tf(a,3)(x,x)+5
        self.assertEqual(contractDeltas(exp), 5)

        exp = 4711
        self.assertEqual(contractDeltas(exp),4711)

        exp = sympy.diff(Delta(c,a)*tf(a,b)(x,y),y)
        self.assertEqual(contractDeltas(exp),sympy.diff(tf(c,b)(x,y),y))

        exp = tf(x,y)(t(a,b),t(z,z),z)*Delta(y,c)*Delta(a,d) - tf(x,c)(t(d,b),t(z,z),z)
        self.assertEqual(contractDeltas(exp),0)


    def test_dim(self):
        a=self.a
        tempDim=getDim()
        setDim(4)
        self.assertEqual(contractDeltas(Delta(a,a)),4)
        setDim(4711)
        self.assertEqual(contractDeltas(Delta(a,a)),4711)
        setDim(tempDim)
        self.assertEqual(contractDeltas(Delta(a,a),dim=13),13)
        setDim(tempDim)
        self.assertEqual(getDim(),tempDim)

if __name__ == '__main__':
    unittest.main()
