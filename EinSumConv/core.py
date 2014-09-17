import sympy
import tensor

def printStructure(x):
    if getattr(x, 'args', []):
        return type(x).__name__ + "(" + ", ".join([printStructure(xa) for xa in x.args]) + ")"
    else:
        return str(x)

def flatten(x):
    result = []
    for el in x:
        if hasattr(el, "__iter__") and not isinstance(el, basestring):
            result.extend(flatten(el))
        else:
            result.append(el)
    return result


def makeFactorList(x):
    if isinstance(x,sympy.Pow) and isinstance(x.args[1],(int,sympy.Integer)) and x.args[1]>1 :
        factorList=[]
        base=makeFactorList(x.args[0])
        for i in range(x.args[1]):
            factorList.append(base)
        return flatten(factorList)
    
    if isinstance(x,sympy.Mul):
        factorList=[]
        for factor in x.args:
            factorList.append(makeFactorList(factor))
        return flatten(factorList)
    return x
    
def makeTermList(x):
    if not isinstance(x,sympy.Add):
        return x
    return [makeFactorList(term) for term in x.args]
