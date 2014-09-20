
#    def __eq__(self, other):
#        return (isinstance(other, self.__class__) and (self.class_key() == other.class_key()))

#copy pased with UndefinedFunction -> UndefinedTensor. I have no idea what this does
#UndefinedTensor.__eq__ = lambda s, o: (isinstance(o, s.__class__) and 
#   


class AppliedTensor(AppliedUndef,Tensor):
    def __new__(cls, *args):
        obj = object.__new__(cls)
        obj._assumptions = cls.default_assumptions
        obj._mhash = None  # will be set by __hash__ method.

        if isinstance(args[0], tuple):
            obj.index = tuple(map(sympify, args[0]))
            obj._args= tuple(map(sympify, args[1:]))
        else:
            obj._args = ()
            obj.index = tuple(map(sympify, args))
        return obj

    def withNewIndex(self,*index):
        if not self.args:
            return type(self)(*index)
        l=[index]
        l.extend(self.args)
        return type(self)(*l)
        
    @property
    def indexAndArgs(self):
        if not self.args:
            return self.index
        l=[self.index]
        l.extend(self.args)
        return tuple(l)

    def __unicode__(self):
        return type(self).__name__ + unicode(self.indexAndArgs)

#    def __str__(self):
#        return type(self).__name__ + str(self.indexAndArgs)

#    def __repr__(self):
#        return type(self).__name__ + repr(self.indexAndArgs)

    def __eq__(self, other):
        return type(self)==type(other) and self.indexAndArgs==other.indexAndArgs

    def __hash__(self):
        return hash(str(self))

'''
Tensor is a copy of the contruction of Function with the addition .index() and .is_tensor

User guide: Put the indecis as an tupple, as the rist index in the TensorFunktion

Example1: To get the tensor $T_{a,b}$, witie:
>>> T=Tenosr('T')
>>> T((a,b))
Example2: To get the tensor $T_{a,b}(x,y)$, witie:
>>> T=Tenosr('T')
>>> T((a,b),x,y)

It is suggested to ouse the class Dummy for indecis and the class Symbol for ordinary variables, to keep them appart.
'''

