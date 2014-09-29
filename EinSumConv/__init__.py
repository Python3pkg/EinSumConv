from tensor import isTensor, tensorName, longTensorName, TensorFunction, Tensor



def printStructure(x):
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
