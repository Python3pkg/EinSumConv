from sympy.core.function import Function, UndefinedFunction, AppliedUndef, Application, FunctionClass
from sympy.core.cache import cacheit
from sympy.core.core import BasicMeta
from sympy.core.sympify import sympify
from sympy.core.expr import Expr

#class Tensor(Application,Expr):
class Tensor(Function):
    @cacheit
    def __new__(cls, *args, **options):
        # Handle calls like Tensor('F')
        if cls is Tensor:
            return UndefinedTensor(*args, **options)
    
    __slots__ = ['_mhash',              # hash value
                 '_args',               # arguments
                 '_assumptions'
                 'index'                # idecis
                ]

class TensorFunction(Tensor,Function):
    @cacheit
    def __new__(cls, *args, **options):
        # Handle calls like TensorFunction('F')
        if cls is TensorFunction:
            return UndefinedTensorFunction(*args, **options)
    

#class UndefinedTensor():        
class UndefinedTensor(UndefinedFunction):

    def __new__(mcl, name, **kwargs):
        ret = BasicMeta.__new__(mcl, name, (AppliedTensor,), kwargs)
        ret.__module__ = None
        return ret

class UndefinedTensorFunction(UndefinedFunction):

    def __new__(mcl, name, **kwargs):
        ret = BasicMeta.__new__(mcl, name, (AppliedTensorFunction,), kwargs)
        ret.__module__ = None
        return ret


#    def __eq__(self, other):
#        return (isinstance(other, self.__class__) and (self.class_key() == other.class_key()))

#copy pased with UndefinedFunction -> UndefinedTensor. I have no idea what this does
#UndefinedTensor.__eq__ = lambda s, o: (isinstance(o, s.__class__) and 
#   

#class AppliedTensor(Tensor):
class AppliedTensor(AppliedUndef,Tensor):
    def __new__(cls, *index):
        obj = object.__new__(cls)
        obj._assumptions = cls.default_assumptions
        obj._mhash = None  # will be set by __hash__ method.
        
        obj._args = ()
        obj.index = tuple(map(sympify, index))
        return obj

    def __str__(self):
        return type(self).__name__ + str(self.index)


class AppliedTensorFunction(AppliedUndef,Tensor):
    def __new__(cls, index, *args):
        obj = object.__new__(cls)
        obj._assumptions = cls.default_assumptions
        obj._mhash = None  # will be set by __hash__ method.
        
        obj._args = tuple(map(sympify, args))  # all items in args must be Basic objects
        obj.index = tuple(map(sympify, index))
        return obj    

    @property
    def indexAndArgs(self):
        l=[self.index]
        l.extend(self.args)
        return tuple(l)

    def __str__(self):
        return type(self).__name__ + str(self.indexAndArgs)

'''
Tensor is a copy of the contruction of Function with the addition .index() and .is_tensor

User guide: Put the indecis as an tupple, as the rist index in the TensorFunktion

Example1: To get the tensor $T_{a,b}$, witie:
>>> T=TenosrFunction('T')
>>> T((a,b))
Example2: To get the tensor $T_{a,b}(x,y)$, witie:
>>> T=TenosrFunction('T')
>>> T((a,b),x,y)

It is suggested to ouse the class Dummy for indecis and the class Symbol for ordinary variables, to keep them appart.
'''

#Special tesors

class Delta(AppliedTensor):
    pass
  
    
class Eps(AppliedTensor):
    pass
