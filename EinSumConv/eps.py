import delta
import tensor
import sympy


'''
This module is ment for dim == 3
'''



class Eps(tensor.AppliedTensor):
    pass


def evalTwoEps(eps,ePS):
    for i,j,k in [(eps.index[0], eps.index[1], eps.index[2]),
                  (eps.index[1], eps.index[2], eps.index[0]),
                  (eps.index[2], eps.index[0], eps.index[1])]: 
        for I,J,K in [(ePS.index[0], ePS.index[1], ePS.index[2]),
                      (ePS.index[1], ePS.index[2], ePS.index[0]),
                      (ePS.index[2], ePS.index[0], ePS.index[1])]:
            if not i==I and isinstance(i, (sympy.Symbol, sympy.Dummy)): 
                continue
            return delta.contractDeltas(
                delta.Delta(j,J)*delta.Delta(k,K)
                -delta.Delta(j,K)*delta.Delta(k,J),
                dim=3)
    return None



def evalOneEps(eps):
    e1,e2,e3 = eps.index
    if e1==e2 or e2==e3 or e3==e1:
        return 0    
    for i,j,k in [(e1,e2,e3),
                  (e2,e3,e1),
                  (e3,e1,e2)]: 
        for I,J,K in [(1,2,3),
                      (2,3,1),
                      (3,1,2)]:
            if not i==I: continue
            return delta.contractDeltas(
                delta.Delta(j,J)*delta.Delta(k,K)
                -delta.Delta(j,K)*delta.Delta(k,J),
                dim=3)
 


### Here be unittest ###
import unittest
from delta import Deta


class TestEps(unittest.TestCase):

    def setUp(self):
        pass

    def test_evaOneEsps(self):
        a,b,c = sympy.symbols('a,b,c')
        self.assertEqual(evalOneEps(Eps(1,a,b)),
                Delta(a,2)*Delta(b,3)-Delta(a,3)*Delta(b,2) )
        self.assertEqual(evalOneEps(Eps(a,b,c)), None)
        self.assertEqual(evalOneEps(Eps(a,3,2)), -Delta(a,1))
        self.assertEqual(evalOneEps(Eps(a,a,b)), 0)
        self.assertEqual(evalOneEps(Eps(1,2,3)), 1)

    def test_evaTwoEsps(self):
        a,b,c,d,e = sympy.symbols('a,b,c,d,e')
        self.assertEqual(evalTwoEps(Eps(1,a,b),Eps(1,a,b)), 6)
        self.assertEqual(evalTwoEps(Eps(a,b,c),Eps(d,e,a)), 
                Delta(b,d)*Delta(c,e)-Delta(b,e)*Delta(c,d) )

if __name__ == '__main__':
    unittest.main()

