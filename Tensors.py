from sympy.core.function import Function, UndefinedFunction, AppliedUndef
from sympy.core.cache import cacheit
from sympy.core.core import BasicMeta
from sympy.core.sympify import sympify

class Tensor(Function):
    @cacheit
    def __new__(cls, *args, **options):
        # Handle calls like Tensor('F')
        if cls is Tensor:
            return UndefinedTensor(*args, **options)
        
class UndefinedTensor(UndefinedFunction):
    def __new__(mcl, name, **kwargs):
        ret = BasicMeta.__new__(mcl, name, (AppliedTensor,), kwargs)
        ret.__module__ = None
        return ret 
    
    def __eq__(self, other):
        return (isinstance(other, self.__class__) and (self.class_key() == other.class_key()))

#copy pased with UndefinedFunction -> UndefinedTensor. I have no idea what this does
#UndefinedTensor.__eq__ = lambda s, o: (isinstance(o, s.__class__) and 
#   

class AppliedTensor(AppliedUndef):
    def __new__(cls, *args, **options):
        args = list(map(sympify, args))
        obj = super(AppliedTensor, cls).__new__(cls, *args, **options)
        return obj
    
    def __init__(self,*args,**options):
        self.index=args[0]
        self.is_Tensor=True
    

    
#    def index(self):
#        return self.args[0]
    

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
    
    def index(self):
        return self.args
  
    
class Eps(AppliedTensor):

    def index(self):
        return self.args
