import sympy.core.cache
# import sympy.core.function
# import sympy.core.compatibility


'''
Tensor('name') creates a tensor that does not take arguments
>>> T = Tensor('T')
>>> T(*index)

TensorFunction creates a teonsr that do take arguments
>>> TF = TensorFunction('TF')
>>> TF(*index)(*args)

Both Tensor and TensorFuncton takes any number of indices. Anytning can be an index but it is genarly recomended to use sympy.Dummy or sympy.Symbol.

>>> a=sympy.Dymmy('a'); b=sympy.Dymmy('b')
>>> isinstance(Tensor('T')(a,b), sympy.Symbol)
True

>>> a=sympy.Dymmy('a'); b=sympy.Dymmy('b')
>>> isinstance(TensorFunction('TF')(a,b), sympy.FunctionClass)
True

>>> a=sympy.Dymmy('a'); b=sympy.Dummy('b); 
>>> x=sympy.Symbol('x')
>>> isinstance(TensorFunction('TF')(a,b)(x), sympy.Function)
True
'''


# Why doesn't it work to use "import sympy.core.compatibility" and call "with_metaclass" as "sympy.core.compatibility.with_metaclass"?
from sympy.core.compatibility import with_metaclass
from sympy.core.function import AppliedUndef, FunctionClass
from sympy.core.core import BasicMeta
from sympy.core.assumptions import ManagedProperties
from sympy.core.cache import cacheit


# this is the function used in other operations to check if something is a tensor.
def isTensor(x):
    return getattr(x,'is_Tensor',False) and getattr(x,'index',False)

class TensorFunction(BasicMeta):
    @cacheit
    def __new__(mcl, name, *arg, **kw):
        if (name == "AppliedTensorFunction"):
            return type.__new__(mcl, name, *arg, **kw)
        return type.__new__(mcl, name, (AppliedTensorFunction,), kw)
    def __init__(self, *arg, **kw):
        pass

class AppliedTensorFunction(FunctionClass):
    __metaclass__ = TensorFunction

    @cacheit
    def __new__(mcl, *indices, **kw):
        name = mcl.__name__ + str(indices)
        ret = type.__new__(mcl, name, (AppliedUndef,),kw)
        ret.indices = indices
        return ret
    is_Tensor = True

    def withNewIndex(self,*indices):
        return type(type(self))(*indices)(*self.args)

class Tensor(ManagedProperties):
    @cacheit
    def __new__(mcl, name, *arg, **kw):
        if (name == "AppliedTensor"):
            return type.__new__(mcl, name, *arg, **kw)
        return type.__new__(mcl, name, (AppliedTensor,),kw)

class AppliedTensor(sympy.Symbol):
    __metaclass__ = Tensor

    @cacheit
    def __new__(cls, *index, **kw):
        name = cls.__name__ + str(indices)
        ret = sympy.Symbol.__new__(cls, name, **kw)  
        ret.index = index
        return ret
    is_Tensor = True

    def withNewIndex(self,*index):
        return type(self)(*indices)




