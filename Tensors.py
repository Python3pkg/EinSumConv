from sympy.core.function import Function, UndefinedFunction, AppliedUndef, Application
from sympy.core.cache import cacheit
from sympy.core.core import BasicMeta
from sympy.core.sympify import sympify
from sympy.core.symbol import Symbol
from sympy.core.expr import Expr


class Tensor(Function): 
    @cacheit
    def __new__(cls, *args, **options):
        # Handle calls like Tensor('F')
        if cls is Tensor:
            return UndefinedTensor(*args, **options)

class TensorFunction(Function):  
    @cacheit
    def __new__(cls, *args, **options):
        # Handle calls like TensorFunction('F')
        if cls is TensorFunction:
            return UndefinedTensorFunction(*args, **options)
        
class UndefinedTensor(UndefinedFunction):
    """
    The (meta)class of undefined tensors.
    """
    def __new__(mcl, name, **kwargs):
        ret = BasicMeta.__new__(mcl, name, (AppliedTensor,), kwargs)
        ret.__module__ = None
        return ret 

class UndefinedTensorFunction(UndefinedFunction):
    """
    The (meta)class of undefined tensors.
    """
    def __new__(mcl, name, **kwargs):
        ret = BasicMeta.__new__(mcl, name, (AppliedTensorFunction,), kwargs)
        ret.__module__ = None
        return ret 
    

#copy pased with UndefinedFunction -> UndefinedTensorFunction. I have no idea what this does
UndefinedTensorFunction.__eq__ = lambda s, o: (isinstance(o, s.__class__) and 
                                         (s.class_key() == o.class_key()))
        

class AppliedTensor(Tensor,AppliedUndef):
    def __new__(cls, *args, **options):
        args = list(map(sympify, args))
        obj = super(AppliedTensor, cls).__new__(cls, *args, **options)
        return obj
	@property
	def index(self):
		self.args

class AppliedTensorFunction(TensorFunction,Tensor,AppliedUndef):  
    def __new__(cls, *args, **options):
        args = list(map(sympify, args))
        obj = super(AppliedTensorFunction, cls).__new__(cls, *args, **options)
        return obj
	@property
	def index(self):
		self.args[0]
	

    

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
