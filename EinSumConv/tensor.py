import sympy.core.cache
# import sympy.core.function
# import sympy.core.compatibility

# Why doesn't it work to use "import sympy.core.compatibility" and call "with_metaclass" as "sympy.core.compatibility.with_metaclass"?
from sympy.core.compatibility import with_metaclass
from sympy.core.function import AppliedUndef, FunctionClass
from sympy.core.core import BasicMeta
from sympy.core.assumptions import ManagedProperties

# this is the function used in other operations to check if something is a tensor.
def isTensor(x):
    return hasattr(x,'indices')

class TensorFunction(BasicMeta):
    def __new__(mcl, name, *arg, **kw):
        if (name == "AppliedTensorFunction"):
            return type.__new__(mcl, name, *arg, **kw)
        return type.__new__(mcl, name, (AppliedTensorFunction,), kw)
    def __init__(self, *arg, **kw):
        pass

class AppliedTensorFunction(FunctionClass):
    __metaclass__ = TensorFunction
    def __new__(mcl, *indices, **kw):
        name = mcl.__name__ + str(indices)
        ret = type.__new__(mcl, name, (AppliedUndef,),kw)
        ret.indices = indices
        return ret

class Tensor(ManagedProperties):
    def __new__(mcl, name, *arg, **kw):
        if (name == "AppliedTensor"):
            return type.__new__(mcl, name, *arg, **kw)
        return type.__new__(mcl, name, (AppliedTensor,),kw)

class AppliedTensor(sympy.Symbol):
    __metaclass__ = Tensor
    def __new__(cls, *indices, **kw):
        name = cls.__name__ + str(indices)
        ret = sympy.Symbol.__new__(cls, name, **kw)  
        ret.indices = indices
        return ret




