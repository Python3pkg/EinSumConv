from tensor import isTensor, tensorName, longTensorName, TensorFunction, Tensor
from findIndex import findIndex
from renameIndex import tensorSimplify, subsIndex


def printStructure(x):
    '''Takes an expression and returns a sring that showes how this epxression is represented as clases and arguments.'''
    if getattr(x, 'args', []):
        return type(x).__name__ + "(" + ", ".join([printStructure(xa) for xa in x.args]) + ")"
    else:
        return str(x)



# To doo list
'''
+ Write unittest for EVERYTHING! 
+ Handle symetric and anti-symetric tensors
+ Fix pretty print
'''
