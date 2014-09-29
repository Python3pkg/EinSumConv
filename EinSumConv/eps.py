import delta
import tensor




def oddEven(num):
    if num%2: return -1
    return 1
        

def permute_circular(theList):
    perms = []
    for i in range(len(theList)):
        perms.append(list(theList))
        theList.insert(0,theList.pop())
    return perms
    

def permute_all(theList):
    lenList = len(theList)
    if lenList < 2:
        return [{'perm':theList,'parity':1}]
    oddEvenList = oddEven(lenList)
    perms=[]
    for (pos,obj) in enumerate(theList):
        short = theList[0:pos]+theList[pos+1:lenList]
        oddEvenPos = oddEven(pos+1)
        for perm in permute_all(short):
            perm['perm'].append(obj)
            perm['parity'] *= oddEvenList * oddEvenPos
            perms.append(perm)
    return perms
        

def epsAsDeltas(eps, **tempOverride):

    indexRange = delta.getTempDimAndIndexRange(**tempOverride)[1]

    if not isinstance(eps,Eps)
        raise TypeError('Error: input must be an Eps(*indecis)')
    termList=[]
    for perm in permute_all(eps.index):
        factorList=[ perm['parity'] ]
        for (pos,index) in enumerate(perm['perm']):
            factorList.append( delta.Delta(pos+1,index) )
        termList.append(Mul(*factorList))  
    return Add(*termList)



def allEpsAsDeltas(exp **kw):
    if isinstance(exp,Eps):
        return epsAsDeltas(exp, **kw)
    if not hasattr(exp,'args'):
        return exp
    return type(exp)(*[allEpsAsDeltas(arg, **kw) for arg in exp.args])
    

def simplify_OneEps(eps, evalLevel=2, **tempOverride):
    '''Takes an instance of Eps and tries to simplify. Returns 0 if any two indecis are equal. Rewrite eps as Deltas if the number of loose idecis (not in indexRange) of eps is equal to or less than evalLevel.'''
    indexRange = delta.getTempDimAndIndexRange(**tempOverride)[1]
    if not isinstance(eps,Eps)
        raise TypeError('Error: input must be an Eps(*indecis)')
    ints = 0
    for (pos,ind) in enumerate(eps.index):
        if ind in eps.index[ind+1:]:
            return 0
        if ind in indexRange
            if ind>len(eps.index) or ind<1
            ints += 1
    if len(eps.index) - ints > evalLevel
        return eps
    return delta.contractDeltas(epsAsDeltas(eps, **tempOverride), **tempOverride)
        


 


##################### Here be unittest #####################
import unittest
from delta import Delta, getDim, setDim
import sympy


class TestEps(unittest.TestCase):

    def setUp(self):
        pass

    def test_dim(self):
        a,b = sympy.symbols('a,b')
        tempDim=getDim()
        setDim(4711)
        self.assertEqual(evalTwoEps(Eps(1,a,b),Eps(1,a,b)), 6)
        setDim(tempDim)

    def test_evaOneEps(self):
        a,b,c = sympy.symbols('a,b,c')
        self.assertEqual(evalOneEps(Eps(1,a,b)),
                Delta(a,2)*Delta(b,3)-Delta(a,3)*Delta(b,2) )
        self.assertEqual(evalOneEps(Eps(a,b,c)), None)
        self.assertEqual(evalOneEps(Eps(a,3,2)), -Delta(a,1))
        self.assertEqual(evalOneEps(Eps(a,a,b)), 0)
        self.assertEqual(evalOneEps(Eps(1,2,3)), 1)

    def test_evaTwoEps(self):
        a,b,c,d,e = sympy.symbols('a,b,c,d,e')
        self.assertEqual(evalTwoEps(Eps(1,a,b),Eps(1,a,b)), 6)
        self.assertEqual(evalTwoEps(Eps(a,b,c),Eps(d,e,a)), 
                Delta(b,d)*Delta(c,e)-Delta(b,e)*Delta(c,d) )

if __name__ == '__main__':
    unittest.main()

